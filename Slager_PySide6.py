import sys
import csv
import random
import xml.etree.ElementTree as ET
from PySide6.QtWidgets import QApplication,QLabel, QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor


class SongManager(QWidget):
    def __init__(self):
        super().__init__()
        self.table = QTableWidget()
        self.songs = []
        self.original_songs = []
        self.create_layout()
        self.load_songs_from_csv()
        self.setFixedSize(970, 500)  # ablak mérete
        self.setWindowTitle('SLÁGERLISTA')
    def create_layout(self):
        menu_font = ('Arial', 14, 'bold')
        table_font = ('Arial', 12)

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(['Előadó', 'Cím', 'Helyezés'])

        # Oszlopok szélességének beállítása
        self.table.setColumnWidth(0, 500)  # Előadó oszlop szélessége: 150 pixel
        self.table.setColumnWidth(1, 300)  # Cím oszlop szélessége: 200 pixel
        self.table.setColumnWidth(2, 100)
        layout.addWidget(self.table)

        # Elválasztó elem hozzáadása
        separator_label = QLabel()
        separator_label.setStyleSheet("")
        layout.addWidget(separator_label)


        button_layout = QVBoxLayout()

        load_button = QPushButton('Beolvasás')
        load_button.setFont(menu_font)
        load_button.clicked.connect(self.load_songs_from_csv)

        update_button = QPushButton('Frissítés')
        update_button.setFont(menu_font)
        update_button.clicked.connect(self.update_votes)

        top_button = QPushButton('1. hely')
        top_button.setFont(menu_font)
        top_button.clicked.connect(self.show_top_song)

        export_button = QPushButton('XML')
        export_button.setFont(menu_font)
        export_button.clicked.connect(self.export_to_xml)

        exit_button = QPushButton('Kilépés')
        exit_button.setFont(menu_font)
        exit_button.setStyleSheet("background-color: red; color: white;")
        exit_button.clicked.connect(self.close)

        button_layout.addWidget(load_button)
        button_layout.addWidget(update_button)
        button_layout.addWidget(top_button)
        button_layout.addWidget(export_button)
        button_layout.addWidget(exit_button)

        layout.addLayout(button_layout)

    def load_songs_from_csv(self):
        self.original_songs = []
        filename = 'lista.csv'
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
        self.table.setRowCount(len(self.songs))
        sorted_songs = sorted(self.songs, key=lambda x: x["votes"], reverse=True)
        for row, song in enumerate(sorted_songs):
            artist_item = QTableWidgetItem(song["artist"])
            title_item = QTableWidgetItem(song["title"])
            votes_item = QTableWidgetItem(str(song["votes"]))
            self.table.setItem(row, 0, artist_item)
            self.table.setItem(row, 1, title_item)
            self.table.setItem(row, 2, votes_item)

    def update_votes(self):
        for song in self.songs:
            song["votes"] += random.randint(0, 50)
        self.list_songs()

    def show_top_song(self):
        if self.songs:
            top_song = max(self.songs, key=lambda x: x["votes"])
            self.table.clearSelection()
            item = None  # Változó inicializálása a cikluson kívül
            for row in range(self.table.rowCount()):
                if self.table.item(row, 0).text() == top_song["artist"] and \
                        self.table.item(row, 1).text() == top_song["title"] and \
                        self.table.item(row, 2).text() == str(top_song["votes"]):
                    for col in range(self.table.columnCount()):
                        item = self.table.item(row, col)
                        item.setBackground(QColor(Qt.yellow))
                        item.setForeground(QColor(Qt.black))
                        font = item.font()
                        font.setBold(True)
                        item.setFont(font)
                    self.table.scrollToItem(item)
                    break

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
        print("Az objektumlista sikeresen exportálva lett XML formátumba")


if __name__ == '__main__':
    app = QApplication([])
    song_manager = SongManager()
    song_manager.show()
    sys.exit(app.exec())