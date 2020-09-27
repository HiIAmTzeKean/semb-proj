
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

def workshop_type():
    workshops = [("Sembawang"),("Bedok"),("Navy"),("Selarang"),("HQ")]
    return workshop