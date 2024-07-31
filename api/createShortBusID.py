
def createShortBusID(sra, sektor, tura):
    """
        Budowanie identyfikatora autokaru
        Format: T16, D11, W23, itp.
    """
    if sra.static_identifier is not None:
        return sra.static_identifier
    else:
        return f"{sra.prefix}{tura}{sektor}"
