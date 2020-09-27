def statuses_type():
    statuses = {
            'P': 'PRESENT',
            'AO': 'ATTACHED OUT',
            'DUTY': 'DUTY',
            'OS': 'OUT STATION',
            'OC': 'ON COURSE',
            'OFF': 'OFF',
            'LL': 'LOCAL LEAVE',
            'OL': 'OVERSEAS LEAVE',
            'MC': 'MC',
            'MA': 'MA',
            'RSO': 'RSO',
            'RSI': 'RSI',
            'SOL': 'SOL',
            'DR': 'DUTY REST',
            'OTHERS': 'OTHERS'
        }
    return statuses


def fmd_type():
    fmd = [(93),(92),(9)]
    return fmd

def workshop_type(fmd):
    if fmd == 9:
        workshop = [("9HQ")]
    elif fmd == 92:
        workshop = [("Kranji"),("92HQ")]
    elif fmd == 93:
        workshop = [("Sembawang"),("Bedok"),("Navy"),("Selarang"),("93HQ")]
    return workshop