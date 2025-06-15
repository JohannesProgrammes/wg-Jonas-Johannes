CATEGORIES = {
    "Spülmaschine ausgeräumt": "data/spülmaschine.csv",
    "Restmüll rausgebracht": "data/restmüll.csv",
    "Biomüll rausgebracht": "data/biomüll.csv",
    "Papiermüll rausgebracht": "data/papierlmüll.csv",
    "Verpackungsmüll rausgebracht": "data/Verpackungsmüll.csv",
    "Altglas": "data/altglas.csv",
    "Backofen geputzt": "data/backofen.csv",
    "Küche gewischt": "data/küche.csv",
    "Fenster geputzt": "data/fenster.csv",
}
y = {x:CATEGORIES[x] for x in CATEGORIES}
print(y==CATEGORIES)

import numpy as np


daten = np.array([['15.03.2025, 14:37 Uhr', 'Johannes', 'Heinzelmännchen'],
 ['15.03.2025, 14:38 Uhr', 'Heinzelmännchen', 'Heinzelmännchen'],
 ['15.03.2025, 20:28 Uhr', 'Johannes', 'Johannes'],
 ['15.03.2025, 20:28 Uhr', 'Johannes', 'Heinzelmännchen'],
 ['15.03.2025, 20:28 Uhr', 'Johannes', 'Heinzelmännchen']])


namen, counts = np.unique(daten[:, 2] , return_counts=True)

name_counts = dict(zip(namen, counts))
print(name_counts, namen, counts)
print(name_counts["Johannes"])
sorted_counts = dict(sorted(name_counts.items(), key=lambda item: item[1], reverse=True))
print(sorted_counts)


daten = [3, 5]

import matplotlib.pyplot as plt

plt.plot(daten)

