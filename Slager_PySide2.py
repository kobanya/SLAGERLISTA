import csv
import random
import xml.etree.ElementTree as ET
from PySide2.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QTableWidget, QTableWidgetItem


class SongManager:
    def __init__(self):
        self.songs = []
        self.original_songs = []
        self.load_songs_from_csv('lista.csv')

        self.window = QMainWindow()
        self.central_widget = QWidget()
        self.window.setCentralWidget(self.central_widget)
        self.create_layout()

    def create_layout(self):
        menu_font = 'Arial, 16, bold'
        table_font = 'Arial, 14'

        menu_label = QLabel('')
        menu_label.setStyleSheet(f'font: {menu_font};')

        table = QTableWidget()
        table.setColumnCount(3)
        table.setHorizontalHeaderLabels(['Előadó', 'Cím', 'Helyezés'])
        table.setStyleSheet(f'font: {table_font};')
        table.setEditTriggers(QTableWidget.NoEditTriggers)

        list_button = QPushButton('Beolvasás')
        update_button = QPushButton('Frissítés')
        top_button = QPushButton('1. hely')
        export_button = QPushButton('XML')
        exit_button = QPushButton('Kilépés')

        button_layout = QHBoxLayout()
        button_layout.addWidget(list_button)
        button_layout.addWidget(update_button)
        button_layout.addWidget(top_button)
        button_layout.addWidget(export_button)
        button_layout.addWidget(exit_button)

        layout = QVBoxLayout()
        layout.addWidget(menu_label)
        layout.addWidget(table)
        layout.addLayout(button_layout)

        self.central_widget.setLayout(layout)

        list_button.clicked.connect(self.list_songs)
        update_button.clicked.connect(self.update_votes)
        top_button.clicked.connect(self.show_top_song)
        export_button.clicked.connect(self.export_to_xml)
        exit_button.clicked.connect(self.window.close)

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

    def list_songs(self):
        table = self.central_widget.findChild(QTableWidget)
        table.setRowCount(len(self.songs))
        sorted_songs = sorted(self.songs, key=lambda x: x["votes"], reverse=True)
        for i, song in enumerate(sorted_songs):
            artist = song["artist"]
            title = song["title"]
            votes = song["votes"]
            table.setItem(i, 0, QTableWidgetItem(artist))
            table.setItem(i, 1, QTableWidgetItem(title))
            table.setItem(i, 2, QTableWidgetItem(str(votes)))

    def update_votes(self):
        for song in self.songs:
            song["votes"] += random.randint(0, 50)
        self.list_songs()

    def show_top_song(self):
        top_song = self.songs[0]
        table = self.central_widget.findChild(QTableWidget)
        table.setRowCount(1)
        table.setItem(0, 0, QTableWidgetItem(top_song["artist"]))
        table.setItem(0, 1, QTableWidgetItem(top_song["title"]))
        table.setItem(0, 2, QTableWidgetItem(str(top_song["votes"])))

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

    def run(self):
        self.window.show()


if __name__ == '__main__':
    app = QApplication([])
    song_manager = SongManager()
    song_manager.run()
    app.exec_()
