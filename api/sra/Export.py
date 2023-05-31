from flask import current_app, send_file
from sql import SRA, Zbory, Bus, Pilot
from openpyxl import Workbook
from io import BytesIO


def _export_to_xlsx():
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
            row.append(_bus_type(bus.type))
            row.append(_bus_distance(bus.distance))
            row.append(_parking_mode(bus.parking_mode))

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
        xlsx_stream = BytesIO()
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


def _bus_type(bt):
    return {
        "minibus_9": "minibus 9",
        "minibus_30": "minibus 30",
        "autokar_50": "autokar 50",
        "autokar_70": "autokar 60-70",
        "autobus_12m": "autobus 12m",
        "autobus_18m": "autobus 18m"
    }[bt]


def _parking_mode(pm):
    return {
        "not_needed": "NIE",
        "needed": "TAK",
    }[pm]


def _bus_distance(v):
    return {
        "15km": "15km",
        "25km": "25km",
        "50km": "50km",
        "100km": "100km",
        "200km": "200km",
        "more200km": "> 200km"
    }[v]
