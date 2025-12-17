koodijupp


def kontrolli_punktid(sisend, hetke_summa, max_punktid):
    if sisend.upper() == "X":
        return "X"
    if sisend == "-":
        return None
    try:
        punkt = float(sisend)
    except ValueError:
        return False
    if punkt < 0:
        return False
    if hetke_summa + punkt > max_punktid:
        return False
    return punkt
