from datetime import datetime


def whichTura():
    dt_tura3 = datetime(2024, 8, 5)     # data graniczna
    dt_now = datetime.now()
    tura = 2 if dt_now < dt_tura3 else 3
    return tura
