import csv
import random
import xml.etree.ElementTree as ET


# ANSI Escape kódok
SARGA = '\033[93m'
ALAP = '\033[0m'
KEK = '\033[94m'
ZOLD = '\033[92m'
BOLD = "\033[1m"
NORMAL = "\033[0m"


# Adatok inicializálása
songs = []

def list_songs():
    # Táblázatszerű kiíratás fejlécének létrehozása
    print(f"_" * 109)
    header = ("Előadó", "Cím", "Helyezés")
    print(f"{header[0]:<53} | {header[1]:<40} | {header[2]:^9} |")
    print(f"=" * 109)

    # Zeneszámok rendezése szavazatok száma szerint csökkenő sorrendben
    sorted_songs = sorted(songs, key=lambda x: x["votes"], reverse=True)

    # Zeneszámok feldolgozása soronként
    for i, song in enumerate(sorted_songs, start=1):
        eloado = song["artist"]
        cim = song["title"]
        helyezes = song["votes"]

        # Feldolgozott adatok kiíratása táblázat szerűen
        print(f"{eloado:<53} | {cim:<40} | {helyezes:^9} |")
        print("─" * 109)

# Fő program
with open('lista.csv', 'r') as file:
    reader = csv.reader(file, delimiter=';')
    for row in reader:
        artist, title, votes = row
        votes = int(votes)
        songs.append({"artist": artist, "title": title, "votes": votes})

while True:
    print('\033c')

    print(f"{SARGA}{BOLD}----- MENÜ -----{NORMAL}")
    print("1. Kilistázza az adatokat a szavazatok száma szerinti csökkenő sorrendben.")
    print("2. Frissíti a szavazatok számát véletlenszerűen 0 és 50 közötti szavazathozzáadással.")
    print("3. Jelenítse meg a legtöbb szavazattal rendelkező dal adatait.")
    print("4. Exportálja az objektumlistát XML formátumba.")
    print(f"0. Kilépés a programból.{ALAP}\n")

    choice = input(f"{ZOLD}{BOLD}Válasszon menüpontot: {ALAP}{NORMAL}")
    print()
    print()

    if choice == "1":
        print("----- Dalok a szavazatok szerinti csökkenő sorrendben -----")
        list_songs()
    elif choice == "2":
        print("----- Szavazatok frissítése -----")
        # Frissítés véletlenszerűen 0 és 50 közötti értékekkel
        for song in songs:
            song["votes"] += random.randint(0, 50)
        print("A szavazatok frissítése sikeres.")
        list_songs()
    elif choice == "3":
        print("----- Legtöbb szavazattal rendelkező dal -----")
        top_song = max(songs, key=lambda x: x["votes"])
        print(f"{KEK}TOP 1: {top_song['artist']} - {top_song['title']} - {top_song['votes']} szavazat{ALAP}")
    elif choice == "4":
        print("----- Objektumlista exportálása XML formátumba -----")
        root = ET.Element("songs")
        for song in songs:
            song_element = ET.SubElement(root, "song")
            ET.SubElement(song_element, "artist").text = song["artist"]
            ET.SubElement(song_element, "title").text = song["title"]
            ET.SubElement(song_element, "votes").text = str(song["votes"])
        tree = ET.ElementTree(root)
        ET.indent(tree, space="\t", level=0)  # formázás
        tree.write("songs.xml")
        print(f'{KEK}Az objektumlista sikeresen exportálva lett XML formátumba.{ALAP}')
    elif choice == "0":
        print("Kilépés a programból.")
        break
    else:
        print("Érvénytelen választás. Kérem, válasszon egy érvényes menüpontot.")
