from flask import Blueprint, request
from sql import db, Zbory, Pilot, Bus, SRA
from mail import sendEmail

sra_api = Blueprint('sra', __name__, url_prefix='/sra')


@sra_api.route('/search/congregations/<pattern>')
def search_congregations(pattern):
    zbory = Zbory.query.order_by(Zbory.name).filter(Zbory.name.contains(pattern)).all()
    return [zbor.name for zbor in zbory]


@sra_api.route('/submit', methods=['POST'])
def submit_sra_registration():
    try:
        data = request.json
        reg_data = data['registration_data']
        confirm_email = data['confirmation_email']

        db.session.begin()

        sra = SRA()
        if len(reg_data['info']) > 0:
            sra.info = reg_data['info']

        zbor = Zbory.query.filter_by(name=reg_data['congregation']).first()
        sra.zbor_id = zbor.id

        bus_data = reg_data['bus']
        bus = Bus(typ=bus_data['type'], distance=bus_data['distance'], parking_mode=bus_data['parking_mode'])
        db.session.add(bus)
        db.session.flush()
        sra.bus_id = bus.id

        pilot1_data = reg_data['pilot'][0]
        pilot1 = Pilot(firstname=pilot1_data['firstname'], lastname=pilot1_data['lastname'], email=pilot1_data['email'], phone=f"{pilot1_data['phone']['direct']} {pilot1_data['phone']['number']}")
        db.session.add(pilot1)
        db.session.flush()
        sra.pilot1_id = pilot1.id

        pilot2 = pilot3 = None
        if not reg_data['one_pilot']:
            pilot2_data = reg_data['pilot'][1]
            pilot2 = Pilot(firstname=pilot2_data['firstname'], lastname=pilot2_data['lastname'], email=pilot2_data['email'], phone=f"{pilot2_data['phone']['direct']} {pilot2_data['phone']['number']}")
            db.session.add(pilot2)
            db.session.flush()
            sra.pilot2_id = pilot2.id

            pilot3_data = reg_data['pilot'][2]
            pilot3 = Pilot(firstname=pilot3_data['firstname'], lastname=pilot3_data['lastname'], email=pilot3_data['email'], phone=f"{pilot3_data['phone']['direct']} {pilot3_data['phone']['number']}")
            db.session.add(pilot3)
            db.session.flush()
            sra.pilot3_id = pilot3.id

        db.session.add(sra)
        db.session.flush()
        db.session.commit()

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
            recipients=[confirm_email, 'rafal_jankowski@o2.pl'],
            subject="Potwierdzenie zgłoszenia autokaru",
            body=mail_body
        )

        return "", 200
    except Exception as e:
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
