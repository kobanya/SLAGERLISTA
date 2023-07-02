import csv
import random
import xml.etree.ElementTree as ET
from tkinter import *
from tkinter import ttk

class SongManager:
    def __init__(self, root):
        self.root = root
        self.root.title('SLÁGERLISTA')
        self.songs = []
        self.original_songs = []
        self.create_layout()
        self.load_songs_from_csv()

    def create_layout(self):
        self.table = ttk.Treeview(self.root, columns=('Előadó', 'Cím', 'Pontszám'), show='headings')
        self.table.heading('Előadó', text='Előadó')
        self.table.heading('Cím', text='Cím')
        self.table.heading('Pontszám', text='Pontszám')
        self.table.column('Előadó', width=800)
        self.table.column('Cím', width=400)
        self.table.column('Pontszám', width=170)
    # sormagassság, hogy ne csósszanak össze
        style = ttk.Style()
        style.configure("Treeview", rowheight=35)
        self.table.pack()



        self.separator = ttk.Separator(self.root, orient='horizontal')
        self.separator.pack(pady=10)

        self.message_box = Text(self.root, height=2, width=82)
        self.message_box.configure(background='lightgray')
        self.message_box.pack()

        self.separator = ttk.Separator(self.root, orient='horizontal')
        self.separator.pack(pady=10)

        button_frame = Frame(self.root)
        button_frame.pack()

        load_button = Button(button_frame, text='Beolvasás', command=self.load_songs_from_csv)
        load_button.pack(side='left', padx=50)

        update_button = Button(button_frame, text='Frissítés - Szavazás', command=self.update_votes)
        update_button.pack(side='left', padx=50)

        top_button = Button(button_frame, text='1. hely', command=self.show_top_song)
        top_button.pack(side='left', padx=50)

        export_button = Button(button_frame, text='XML', command=self.export_to_xml)
        export_button.pack(side='left', padx=50)

        exit_button = Button(button_frame, text='Kilépés', command=self.close, bg = '#960000', fg='white')

        exit_button.pack(side='right', padx=50)

        self.separator = ttk.Separator(self.root, orient='horizontal')
        self.separator.pack(pady=20)

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
        self.clear_message_box()

    def clear_message_box(self):
        self.message_box.delete(1.0, END)

    def update_song_list(self):
        self.songs = list(self.original_songs)
        self.list_songs()

    def list_songs(self):
        self.clear_table()
        sorted_songs = sorted(self.songs, key=lambda x: x["votes"], reverse=True)
        for song in sorted_songs:
            self.add_song_to_table(song)

    def add_song_to_table(self, song):
        row = len(self.table.get_children())
        self.table.insert('', 'end',values=(song["artist"], song["title"], song["votes"]))

    def clear_table(self):
        self.table.delete(*self.table.get_children())

    def update_votes(self):
        for song in self.songs:
            song["votes"] += random.randint(0, 50)
        self.list_songs()
        self.clear_message_box()

    def show_top_song(self):
        if self.songs:
            top_song = max(self.songs, key=lambda x: x["votes"])
            item = self.get_song_item(top_song)
            if item:
                self.table.selection_set(item)
                self.table.focus(item)
                self.table.see(item)

                artist = top_song["artist"]
                title = top_song["title"]
                votes = top_song["votes"]
                message = f"A legtöbb szavazatot kapott sláger:\n" \
                          f"{artist}, {title}, {votes} ponttal"
                self.clear_message_box()
                self.message_box.insert(END, message)

    def get_song_item(self, song):
        items = self.table.get_children()
        for item in items:
            values = self.table.item(item)['values']
            if values[0] == song['artist'] and values[1] == song['title'] and values[2] == song['votes']:
                return item
        return None

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
        self.clear_message_box()
        self.message_box.insert(END, "Az objektumlista exportálása XML formátumba, sikeres!")

    def close(self):
        self.root.quit()

if __name__ == '__main__':
    root = Tk()
    song_manager = SongManager(root)
    root.mainloop()
