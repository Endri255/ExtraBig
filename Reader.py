import csv
import os
from datetime import datetime as dt

# Otsitav kuupäev (päev, kuu)
D, M = 25, 6

input_file = 'ExtraBig.csv'
output_file = 'tulemused.csv'

# Kontrollime, kas sisendfail eksisteerib
if not os.path.exists(input_file):
    print(f"Viga: faili '{input_file}' ei leitud.")
else:
    # Kui fail on olemas, jätkame lugemisega
    with open(input_file, encoding='utf-8') as f:
        r = csv.DictReader(f, delimiter=';')
        header = r.fieldnames + ['Vanus']
        rows = []

        for row in r:
            # Teisendame kuupäevad (kui olemas)
            b = dt.strptime(row['Sünniaeg'], "%Y-%m-%d") if row['Sünniaeg'] else None
            d = dt.strptime(row['Surmaaeg'], "%Y-%m-%d") if row['Surmaaeg'] else None

            # Kontrollime kuupäeva vastavust
            if (b and (b.day, b.month) == (D, M)) or (d and (d.day, d.month) == (D, M)):
                # Arvutame vanuse
                row['Vanus'] = (
                    d.year - b.year - ((d.month, d.day) < (b.month, b.day))
                    if b and d else ""
                )

                # Vormindame kuupäevad
                row['Sünniaeg'], row['Surmaaeg'] = (
                    x.strftime("%d.%m.%Y") if x else "" for x in (b, d)
                )

                rows.append(row)

    # Kirjutame tulemused väljundfaili
    with open(output_file, 'w', encoding='utf-8', newline='') as f:
        w = csv.DictWriter(f, header, delimiter=';')
        w.writeheader()
        w.writerows(rows)

    print(f"Tulemused salvestati faili '{output_file}'.")
