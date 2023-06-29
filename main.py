import csv

with open('lista.csv', 'r') as file:
    reader = csv.reader(file, delimiter=';')

    # Zeneszámok feldolgozása soronként
    for row in reader:
        artist = row[0]
        title = row[1]
        rank = int(row[2])
    # Feldolgozott adatok kiíratása vagy további feldolgozása
        print(f"{artist:55}{title:40}\t{rank}")
