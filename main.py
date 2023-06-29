import csv

# ANSI Escape kódok
SARGA = '\033[93m'
ALAP = '\033[0m'
KEK = '\033[94m'

with open('lista.csv', 'r') as file:
    reader = csv.reader(file, delimiter=';')

    # Táblázatszerű kiíratás fejlécének létrehozása
    print(f"{SARGA}_{ALAP}" * 109)
    header = ("Előadó", "Cím", "Helyezés")
    print(f"{SARGA}{header[0]:<53} | {header[1]:<40} | {header[2]:^9} |{ALAP}")
    print(f"{SARGA}={ALAP}" * 109)

    # Zeneszámok feldolgozása soronként
    for row in reader:
        eloado = row[0]
        cim = row[1]
        helyezes = int(row[2])

        # Feldolgozott adatok kiíratása táblázat szerűen
        print(f"{eloado:<53} | {cim:<40} | {helyezes:^9} |")
        print("_" * 109)
