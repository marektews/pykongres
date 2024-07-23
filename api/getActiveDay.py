from datetime import datetime


def getActiveDay():
    """
        Zwraca:
        "d1" - każdego innego dnia niż sobota i niedziela
        "d2" - w sobotę
        "d3" - w niedzielę

        Zastępuje wartość z konfiguracji: current_app.config['ACTIVE_DAY']
    """
    wd = datetime.now().isoweekday()
    if wd == 6:
        return 'd2'
    if wd == 7:
        return 'd3'
    return 'd1'
