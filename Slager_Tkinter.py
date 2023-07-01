import csv
import random
import xml.etree.ElementTree as ET
import PySimpleGUI as sg


# ANSI Escape kódok
MENU = '\x1b[1;30;43m'   # sárga alapon fekete betű, vastagon szedve
SARGA = '\033[93m'
ALAP = '\033[0m'
KEK = '\033[94m'
ZOLD = '\033[92m'
BOLD = "\033[1m"
NORMAL = "\033[0m"
TOROL = '\x1b[2J'


class SongManager:
    def __init__(self):
        self.songs = []
        self.original_songs = []
        self.create_layout()
        self.load_songs_from_csv('lista.csv')

    def create_layout(self):
        menu_font = ('Arial', 14, 'bold')
        table_font = ('Arial', 12)
        sg.theme('SystemDefaultForReal')

        menu = [
            [sg.Text('', font=menu_font)]
        ]
        table = [
            [sg.Table(
                values=[],
                headings=['Előadó', 'Cím', 'Helyezés'],
                font=table_font,
                justification='left',
                auto_size_columns=False,
                col_widths=[50, 50, 10],
                key='-TABLE-',
                enable_events=True,
                 )]
        ]
        buttons = [
            [sg.Button('Beolvasás', size=(8, 5), key='-LIST-'),
             sg.Button('Frissítés', size=(8, 5), key='-UPDATE-'),
             sg.Button('1. hely', size=(8, 5), key='-TOP-'),
             sg.Button('XML', size=(8, 5), key='-EXPORT-'),
             sg.Button('Kilépés', size=(8, 5), key='-EXIT-')],
        ]

        layout = [
            [sg.Column(menu)],
            [sg.Column(table)],
            [sg.Column(buttons, justification='center')]
        ]

        self.window = sg.Window('SLÁGERLISTA', layout, finalize=True)

    def load_songs_from_csv(self, filename):
        self.original_songs = []
        with open(filename, 'r') as file:
            reader = csv.reader(file, delimiter=';')
            for row in reader:
                artist, title, votes = row
                votes = int(votes)
                self.original_songs.append({"artist": artist, "title": title, "votes": votes})
        self.update_song_list()

    def update_song_list(self):
        self.songs = list(self.original_songs)
        self.list_songs()

    def list_songs(self):
        sorted_songs = sorted(self.songs, key=lambda x: x["votes"], reverse=True)
        table_data = [[song["artist"], song["title"], song["votes"]] for song in sorted_songs]
        self.window['-TABLE-'].update(values=table_data)

    def update_votes(self):
        for song in self.songs:
            song["votes"] += random.randint(0, 50)
        self.songs = sorted(self.songs, key=lambda x: x["votes"], reverse=True)
        self.list_songs()

    def show_top_song(self):
        top_song = self.songs[0]
        self.window['-TABLE-'].update(values=[[top_song["artist"], top_song["title"], top_song["votes"]]])

    def export_to_xml(self):
        root = ET.Element("songs")
        for song in self.songs:
            song_element = ET.SubElement(root, "song")
            ET.SubElement(song_element, "artist").text = song["artist"]
            ET.SubElement(song_element, "title").text = song["title"]
            ET.SubElement(song_element, "votes").text = str(song["votes"])
        tree = ET.ElementTree(root)
        ET.indent(tree, space="\t", level=0)
        tree.write("songs.xml")
        sg.Popup("Az objektumlista sikeresen exportálva lett XML formátumba")

    def run(self):
        while True:
            event, values = self.window.read()
            if event == sg.WINDOW_CLOSED or event == '-EXIT-':
                break
            elif event == '-LIST-':
                self.load_songs_from_csv('lista.csv')
            elif event == '-UPDATE-':
                self.update_votes()
            elif event == '-TOP-':
                self.show_top_song()
            elif event == '-EXPORT-':
                self.export_to_xml()

        self.window.close()


song_manager = SongManager()
song_manager.run()
