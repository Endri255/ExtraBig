import csv
from datetime import datetime as dt

D, M = 25, 6

with open('ExtraBig.csv', encoding='utf-8') as f:
    r = csv.DictReader(f, delimiter=';')
    header = r.fieldnames + ['Vanus']
    rows = []

    for row in r:
        b = dt.strptime(row['Sünniaeg'], "%Y-%m-%d") if row['Sünniaeg'] else None
        d = dt.strptime(row['Surmaaeg'], "%Y-%m-%d") if row['Surmaaeg'] else None

        if (b and (b.day, b.month) == (D, M)) or (d and (d.day, d.month) == (D, M)):
            row['Vanus'] = d.year - b.year - ((d.month, d.day) < (b.month, b.day)) if b and d else ""
            row['Sünniaeg'], row['Surmaaeg'] = (x.strftime("%d.%m.%Y") if x else "" for x in (b, d))
            rows.append(row)

with open('tulemused.csv', 'w', encoding='utf-8', newline='') as f:
    w = csv.DictWriter(f, header, delimiter=';')
    w.writeheader()
    w.writerows(rows)
