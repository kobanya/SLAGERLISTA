import csv
import random
import xml.etree.ElementTree as ET

class ANSIStyle:
    SARGA = '\033[93m'
    ALAP = '\033[0m'
    KEK = '\033[94m'
    ZOLD = '\033[92m'
    PIROS = '\033[91m'
    BOLD = "\033[1m"
    NORMAL = "\033[0m"

class SongManager:
    def __init__(self):
        self.songs = []

    def load_songs_from_csv(self, filename):
        with open(filename, 'r') as file:
            reader = csv.reader(file, delimiter=';')
            self.songs = [{"artist": artist, "title": title, "votes": int(votes)} for artist, title, votes in reader]

    def list_songs(self):
        print(f"_" * 109)
        header = ("Előadó", "Cím", "Helyezés")
        print(f"{ANSIStyle.BOLD}{header[0]:<53}{ANSIStyle.NORMAL} | {header[1]:<40} | {header[2]:^9} |")
        print(f"=" * 109)

        sorted_songs = sorted(self.songs, key=lambda x: x["votes"], reverse=True)
        for i, song in enumerate(sorted_songs, start=1):
            print(f"{ANSIStyle.BOLD}{song['artist']:<53}{ANSIStyle.NORMAL} | {song['title']:<40} | {song['votes']:^9} |")
            print("─" * 109)

    def update_votes(self):
        for song in self.songs:
            song["votes"] += random.randint(0, 50)

    def show_top_song(self):
        top_song = max(self.songs, key=lambda x: x["votes"])
        print(f"{ANSIStyle.KEK}{ANSIStyle.BOLD}TOP 1: {top_song['artist']} - {top_song['title']} - {top_song['votes']} szavazat{ANSIStyle.ALAP}")

    def export_to_xml(self, filename):
        root = ET.Element("songs")
        for song in self.songs:
            song_element = ET.SubElement(root, "song")
            ET.SubElement(song_element, "artist").text = song["artist"]
            ET.SubElement(song_element, "title").text = song["title"]
            ET.SubElement(song_element, "votes").text = str(song["votes"])
        tree = ET.ElementTree(root)
        ET.indent(tree, space="\t", level=0)
        tree.write(filename)
        print(f'{ANSIStyle.KEK}Az objektumlista sikeresen exportálva lett XML formátumba.{ANSIStyle.ALAP}')

song_manager = SongManager()
song_manager.load_songs_from_csv('lista.csv')

while True:
    print('\033c')

    print(f"{ANSIStyle.SARGA}{ANSIStyle.BOLD}----- MENÜ -----{ANSIStyle.NORMAL}")
    print("1. Kilistázza az adatokat a szavazatok száma szerinti csökkenő sorrendben.")
    print("2. Frissíti a szavazatok számát véletlenszerűen 0 és 50 közötti szavazathozzáadással.")
    print("3. Jelenítse meg a legtöbb szavazattal rendelkező dal adatait.")
    print("4. Exportálja az objektumlistát XML formátumba.")
    print(f"0. Kilépés a programból.{ANSIStyle.ALAP}\n")

    choice = input(f"{ANSIStyle.ZOLD}{ANSIStyle.BOLD}Válasszon menüpontot: {ANSIStyle.NORMAL}")
    print()

    if choice == "1":
        print("----- Dalok a szavazatok szerinti csökkenő sorrendben -----")
        song_manager.list_songs()
    elif choice == "2":
        print("----- Szavazatok frissítése -----")
        song_manager.update_votes()
        print("A szavazatok frissítése sikeres.")
        song_manager.list_songs()
    elif choice == "3":
        print("----- Legtöbb szavazattal rendelkező dal -----")
        song_manager.show_top_song()
    elif choice == "4":
        print("----- Objektumlista exportálása XML formátumba -----")
        song_manager.export_to_xml('songs.xml')
    elif choice == "0":
        print("Kilépés a programból.")
        break
    else:
        print(f"{ANSIStyle.PIROS}Érvénytelen választás. Kérem, válasszon egy érvényes menüpontot.{ANSIStyle.NORMAL}")
