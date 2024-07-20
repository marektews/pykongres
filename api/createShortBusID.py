
def createShortBusID(letter, sektor, tura):
    """
        Budowanie identyfikatora autokaru
        Format: T16, D11, W23, itp.
    """
    return f"{letter}{tura}{sektor}"
