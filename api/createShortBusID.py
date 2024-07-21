
def createShortBusID(letter, sektor, tura, static_identifier=None):
    """
        Budowanie identyfikatora autokaru
        Format: T16, D11, W23, itp.
    """
    if static_identifier is not None:
        return static_identifier
    else:
        return f"{letter}{tura}{sektor}"
