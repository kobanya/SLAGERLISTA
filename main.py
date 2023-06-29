import csv

with open('lista.csv', 'r') as file:
    reader = csv.reader(file, delimiter=';')

    # Zeneszámok feldolgozása soronként
    for row in reader:
        eloado = row[0]
        cim = row[1]
        helyezes = int(row[2])
    # Feldolgozott adatok kiíratása táblázat szerűen
        print(f"{eloado:53} |   {cim:40} | {helyezes:4} |")
        print("_"*107)
