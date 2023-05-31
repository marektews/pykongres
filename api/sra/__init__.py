import io
from flask import Blueprint, request, current_app, send_file
from flask_login import login_required
from sql import db, Zbory, Pilot, Bus, SRA
from mail import sendEmail
from openpyxl import Workbook

sra_api = Blueprint('sra', __name__, url_prefix='/sra')


def _build_pilot_phone(prefix, number):
    return f"{prefix} {number}"


@sra_api.route('/search/congregations/<pattern>')
def search_congregations(pattern):
    """
    Wyszukiwanie zborów na podstawie krótkiego ciągu
    :param pattern: Wzorzec wyszukiwania
    :return: [zbor.name, ...]
    """
    zbory = Zbory.query.order_by(Zbory.name).filter(Zbory.name.contains(pattern)).all()
    return [zbor.name for zbor in zbory]


@login_required
@sra_api.route('/check_pilot_duplicate', methods=['POST'])
def is_pilot_duplicate():
    """
    Sprawdzanie czy podane dane pilota nie są już przypisane do innego autokaru
    :return: HTTP codes: 200, 400
    """
    try:
        data = request.json
        _phone = f"{data['phone']['direct']} {data['phone']['number']}"
        p = Pilot.query.filter_by(phone=_phone).one()
        if p is None:
            return "", 200
        else:
            return "", 400
    except Exception as e:
        current_app.logger.error(f"SRA submit exception: {e}")
        return f"{e}", 500


@login_required
@sra_api.route('/submit', methods=['POST'])
def submit_sra_registration():
    """
    Zapis zgłoszenia do bazy danych
    """
    try:
        data = request.json
        reg_data = data['registration_data']
        confirm_email = data['confirmation_email']

        db.session.begin()

        sra = SRA()
        if len(reg_data['info']) > 0:
            sra.info = reg_data['info']

        zbor = Zbory.query.filter_by(name=reg_data['congregation']).one()
        sra.zbor_id = zbor.id

        bus_data = reg_data['bus']
        bus = Bus(typ=bus_data['type'], distance=bus_data['distance'], parking_mode=bus_data['parking_mode'])
        db.session.add(bus)
        db.session.flush()
        sra.bus_id = bus.id

        pilot1_data = reg_data['pilot'][0]
        pilot1 = Pilot(firstname=pilot1_data['firstname'], lastname=pilot1_data['lastname'],
                       email=pilot1_data['email'], phone=_build_pilot_phone(pilot1_data['phone']['direct'], pilot1_data['phone']['number']))
        db.session.add(pilot1)
        db.session.flush()
        sra.pilot1_id = pilot1.id

        pilot2 = pilot3 = None
        if not reg_data['one_pilot']:
            pilot2_data = reg_data['pilot'][1]
            pilot2 = Pilot(firstname=pilot2_data['firstname'], lastname=pilot2_data['lastname'],
                           email=pilot2_data['email'], phone=_build_pilot_phone(pilot2_data['phone']['direct'], pilot2_data['phone']['number']))
            db.session.add(pilot2)
            db.session.flush()
            sra.pilot2_id = pilot2.id

            pilot3_data = reg_data['pilot'][2]
            pilot3 = Pilot(firstname=pilot3_data['firstname'], lastname=pilot3_data['lastname'],
                           email=pilot3_data['email'], phone=_build_pilot_phone(pilot3_data['phone']['direct'], pilot3_data['phone']['number']))
            db.session.add(pilot3)
            db.session.flush()
            sra.pilot3_id = pilot3.id

        db.session.add(sra)
        db.session.flush()
        db.session.commit()
        current_app.logger.info(f"SRA submit finished")

        # wysłanie maila z potwierdzeniem zgłoszenia
        mail_body = f"""
            DANE POJAZDU
            -------------
            Nazwa zboru: {zbor.name}
            Typ pojazdu: {_bus_type_string(bus.type)}
            Długość trasy: {_bus_distance_string(bus.distance)}
            Parking: {_bus_parking_mode_string(bus.parking_mode)}
        """

        if reg_data['one_pilot']:
            mail_body += f"""
                DANE PILOTA
                -------------
                Imię i nazwisko: {pilot1.fn} {pilot1.ln}
                Numer telefonu: {pilot1.phone}
                E-mail: {pilot1.email}
            """
        else:
            mail_body += f"""
                DANE PILOTÓW
                -------------
                Piątek
                    Imię i nazwisko: {pilot1.fn} {pilot1.ln}
                    Numer telefonu: {pilot1.phone}
                    E-mail: {pilot1.email}
                Sobota
                    Imię i nazwisko: {pilot2.fn} {pilot2.ln}
                    Numer telefonu: {pilot2.phone}
                    E-mail: {pilot2.email}
                Niedziela
                    Imię i nazwisko: {pilot3.fn} {pilot3.ln}
                    Numer telefonu: {pilot3.phone}
                    E-mail: {pilot3.email}
            """

        mail_body += f"""
            UWAGI I DODATKOWE INFORMACJE
            -------------
            {sra.info}
            
            Data wysłania: {sra.timestamp}
        """
        sendEmail(
            recipients=[confirm_email, 'rafal_jankowski@o2.pl', 'lukasglewicz@gmail.com', 'marek.tews@gmail.com'],
            subject="Potwierdzenie zgłoszenia autokaru",
            body=mail_body
        )
        current_app.logger.info(f"SRA send email finished")

        return "", 200
    except Exception as e:
        current_app.logger.error(f"SRA submit exception: {e}")
        db.session.rollback()
        return f"{e}", 500


def _bus_type_string(typ):
    return {
        "minibus_9": "minibus do 9 osób",
        "minibus_30": "minibus do 30 osób",
        "autokar_50": "autokar do 50 osób",
        "autokar_70": "autokar 60-70 osób",
        "autobus_12m": "autobus miejski - 12m (pojedyńczy)",
        "autobus_18m": "autobus miejski - 18m (przegubowy)"
    }[typ]


def _bus_distance_string(distance):
    return {
        "15km": "do 15 km",
        "25km": "do 25 km",
        "50km": "do 50 km",
        "100km": "do 100 km",
        "200km": "do 200 km",
        "more200km": "powyżej 200 km"
    }[distance]


def _bus_parking_mode_string(mode):
    return {
        "needed": "potrzebne miejsce parkingowe",
        "not_needed": "pojazd tylko dowozi pasażerów, odjeżdza i przyjeżdza odebrać ich po programie"
    }[mode]


@login_required
@sra_api.route('/table')
def get_table():
    try:
        res = []
        all_sra = SRA.query.order_by(SRA.timestamp.desc()).all()
        for sra in all_sra:
            item = dict()
            item["id"] = sra.id
            item["info"] = sra.info
            item["timestamp"] = sra.timestamp.strftime("%a, %x %X")

            zbor = Zbory.query.filter_by(id=sra.zbor_id).one()
            z = dict()
            z["name"] = zbor.name
            z["number"] = zbor.number
            z["lang"] = zbor.lang
            item["zbor"] = z

            bus = Bus.query.filter_by(id=sra.bus_id).one()
            b = dict()
            b["type"] = bus.type
            b["distance"] = bus.distance
            b["parking_mode"] = bus.parking_mode
            item["bus"] = b

            ids = [sra.pilot1_id, sra.pilot2_id, sra.pilot3_id]
            for i in range(3):
                _id = ids[i]
                if _id is not None:
                    pilot = Pilot.query.filter_by(id=_id).one()
                    p = dict()
                    p["fn"] = pilot.fn
                    p["ln"] = pilot.ln
                    p["email"] = pilot.email
                    p["phone"] = pilot.phone
                    item[f"pilot{i+1}"] = p

            res.append(item)
        return res, 200
    except Exception as e:
        current_app.logger.error(f"SRA get table exception: {e}")
        return f"{e}", 500


@login_required
@sra_api.route('/write', methods=['POST'])
def write_sra_registration():
    """
    Aktualizacja istniejącego zgłoszenia
    """
    try:
        data = request.json

        db.session.begin()
        sra = SRA.query.filter_by(id=data['id']).one()
        if len(data['info']) > 0:
            sra.info = data['info']
        else:
            sra.info = None

        # aktualizacja danych autokaru
        bus = Bus.query.filter_by(id=sra.bus_id).one()
        bus.type = data['bus']['type']
        bus.distance = data['bus']['distance']
        bus.parking_mode = data['bus']['parking_mode']
        db.session.flush()

        # pilot 1
        dp1 = data['pilot1']
        pilot = Pilot.query.filter_by(id=sra.pilot1_id).one()
        pilot.fn = dp1['fn']
        pilot.ln = dp1['ln']
        pilot.email = dp1['email']
        pilot.phone = _build_pilot_phone(dp1['prefix'], dp1['number'])
        db.session.flush()

        # pilot 2 - update, insert, remove
        if 'pilot2' in data:
            sra.pilot2_id = _update_pilot(db, sra.pilot2_id, data['pilot2'])
        else:
            sra.pilot2_id = _remove_pilot(db, sra.pilot2_id)

        # pilot 3 - update, insert, remove
        if 'pilot3' in data:
            sra.pilot3_id = _update_pilot(db, sra.pilot3_id, data['pilot3'])
        else:
            sra.pilot3_id = _remove_pilot(db, sra.pilot3_id)

        db.session.commit()
        return '', 200
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"SRA write exception: {e}")
        return f"{e}", 500


def _update_pilot(_db, pilot_id, pilot_data):
    if pilot_id is not None:
        # update
        pilot = Pilot.query.filter_by(id=pilot_id).one()
        pilot.fn = pilot_data['fn']
        pilot.ln = pilot_data['ln']
        pilot.email = pilot_data['email']
        pilot.phone = _build_pilot_phone(pilot_data['prefix'], pilot_data['number'])
        _db.session.flush()
        return pilot.id
    else:
        # insert
        pilot = Pilot(firstname=pilot_data['fn'], lastname=pilot_data['ln'],
                      email=pilot_data['email'], phone=_build_pilot_phone(pilot_data['prefix'], pilot_data['number']))
        _db.session.add(pilot)
        _db.session.flush()
        return pilot.id


def _remove_pilot(_db, pilot_id) -> [None, int]:
    if pilot_id is not None:
        pilot = Pilot.query.filter_by(id=pilot_id).one()
        _db.session.delete(pilot)
        return None
    else:
        return pilot_id


@login_required
@sra_api.route('/export/xlsx')
def build_xlsx():
    try:
        wb = Workbook()
        sheet = wb.active
        sheet.title = "Zgłoszenia"

        # budowanie nagłówka
        row = ['#', 'Data zgłoszenia',
               'Zbór-Język', 'Zbór-Numer', 'Zbór-Nazwa',
               'Bus-Typ', 'Bus-Trasa', 'Bus-Parking',
               'Pilot-Piątek-Imię', 'Pilot-Piątek-Nazwisko', 'Pilot-Piątek-Email', 'Pilot-Piątek-Telefon',
               'Pilot-Sobota-Imię', 'Pilot-Sobota-Nazwisko', 'Pilot-Sobota-Email', 'Pilot-Sobota-Telefon',
               'Pilot-Niedziela-Imię', 'Pilot-Niedziela-Nazwisko', 'Pilot-Niedziela-Email', 'Pilot-Niedziela-Telefon',
               'Info']
        sheet.append(row)

        # budowanie tabeli
        index = 1
        all_sra = SRA.query.order_by(SRA.timestamp.desc()).all()
        for sra in all_sra:
            row = [index, sra.timestamp]

            zbor = Zbory.query.filter_by(id=sra.zbor_id).one()
            row.append(zbor.lang)
            row.append(zbor.number)
            row.append(zbor.name)

            bus = Bus.query.filter_by(id=sra.bus_id).one()
            row.append(bus_type(bus.type))
            row.append(bus_distance(bus.distance))
            row.append(parking_mode(bus.parking_mode))

            ids = [sra.pilot1_id, sra.pilot2_id, sra.pilot3_id]
            for i in range(3):
                _id = ids[i]
                if _id is not None:
                    pilot = Pilot.query.filter_by(id=_id).one()
                    row.append(pilot.fn)
                    row.append(pilot.ln)
                    row.append(pilot.email)
                    row.append(pilot.phone)
                else:
                    row.append('')
                    row.append('')
                    row.append('')
                    row.append('')

            if sra.info is not None:
                row.append(sra.info)
            else:
                row.append('')
            sheet.append(row)

        # zapis arkusza do strumienia
        xlsx_stream = io.BytesIO()
        wb.save(xlsx_stream)

        # przygotuj odczyt ze strumienia
        xlsx_stream.seek(0)
        return send_file(
            xlsx_stream,
            mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            as_attachment=True,
            download_name="Ankiety autokarów.xlsx"
        )
    except Exception as e:
        current_app.logger.error(f"SRA export to XLSX exception: {e}")
        return f"{e}", 500


def bus_type(bt):
    return {
        "minibus_9": "minibus 9",
        "minibus_30": "minibus 30",
        "autokar_50": "autokar 50",
        "autokar_70": "autokar 60-70",
        "autobus_12m": "autobus 12m",
        "autobus_18m": "autobus 18m"
    }[bt]


def parking_mode(pm):
    return {
        "not_needed": "NIE",
        "needed": "TAK",
    }[pm]


def bus_distance(v):
    return {
        "15km": "15km",
        "25km": "25km",
        "50km": "50km",
        "100km": "100km",
        "200km": "200km",
        "more200km": "> 200km"
    }[v]
