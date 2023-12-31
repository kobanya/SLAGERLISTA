import csv
import random
import xml.etree.ElementTree as ET
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.uix.textinput import TextInput
from kivy.uix.image import Image


class SongManager(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.spacing = 20
        self.message_box = TextInput(multiline=True, readonly=True, font_size='35sp')
        self.message_box.vertical_align = 'center'
        self.message_box.size_hint_y = None
        self.message_box.height = 100

        self.table_layout = BoxLayout(orientation='vertical', size_hint=(1, None), spacing=20)
        self.table_scroll_view = ScrollView(size_hint=(1, None), size=(100, 300))
        self.table_layout.bind(minimum_height=self.table_layout.setter('height'))
        self.table_scroll_view.add_widget(self.table_layout)
        self.create_layout()
        self.load_songs_from_csv()
        self.add_widget(self.message_box)
        self.add_widget(self.table_scroll_view)

    def create_layout(self):
        Window.size = (890, 1310)

        button_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.1))

        load_button = Button(text='Beolvasás', font_size='28sp', size_hint=(0.1, 1))
        load_button.bind(on_release=self.load_songs_from_csv)
        button_layout.add_widget(load_button)

        update_button = Button(text='Frissítés', font_size='28sp', size_hint=(0.1, 1))
        update_button.bind(on_release=self.update_votes)
        button_layout.add_widget(update_button)

        top_button = Button(text='1. hely', font_size='28sp', size_hint=(0.1, 1))
        top_button.bind(on_release=self.show_top_song)
        button_layout.add_widget(top_button)

        export_button = Button(text='XML', font_size='28sp', size_hint=(0.1, 1))
        export_button.bind(on_release=self.export_to_xml)
        button_layout.add_widget(export_button)

        exit_button = Button(text='Kilépés', font_size='28sp', size_hint=(0.1, 1), background_color=(1, 0, 0, 1))
        exit_button.bind(on_release=self.close)
        button_layout.add_widget(exit_button)

        self.add_widget(button_layout)

        self.table_scroll_view.size_hint_y = 0.7

    def load_songs_from_csv(self, *args):
        self.message_box.text = ""
        self.table_layout.clear_widgets()
        filename = 'lista.csv'
        with open(filename, 'r') as file:
            reader = csv.reader(file, delimiter=';')
            for row in reader:
                artist, title, votes = row
                votes = int(votes)
                row_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=120)
                image = Image(source='cd.png', size_hint=(None, None), size=(100, 100))
                button_box = BoxLayout(orientation='vertical')
                row_layout.add_widget(image)
                row_layout.add_widget(button_box)
                song_label = Button(
                    text=f"Előadó: {artist}\nCím: {title}\nHelyezés: {votes}",
                    disabled=True,
                    background_color=(1, 1, 1, 1),
                    color=(0, 0, 0, 1),
                    padding=(20, 20),
                    size_hint=(1, None),
                    height=120,
                    font_size=29
                )
                button_box.add_widget(song_label)
                self.table_layout.add_widget(row_layout)

    def update_votes(self, *args):
        self.message_box.text = ""

        for row_layout in self.table_layout.children:
            if isinstance(row_layout, BoxLayout) and len(row_layout.children) > 1:
                song_button = None
                if len(row_layout.children[1].children) > 0:
                    song_button = row_layout.children[1].children[0] if len(
                        row_layout.children[1].children) > 0 else None
                if song_button is not None and isinstance(song_button, Button):
                    votes = song_button.text.split("Helyezés: ")[1].split("\n")[0].strip()
                    votes = int(votes)
                    song_button.background_color = (1, 1, 1, 1)
                    votes += random.randint(0, 50)
                    song_button.text = song_button.text.split("Helyezés: ")[0] + f"Helyezés: {votes}\n"

    def show_top_song(self, *args):
        top_song = None
        max_votes = 0
        for row_layout in self.table_layout.children:
            if isinstance(row_layout, BoxLayout) and len(row_layout.children) > 1:
                song_button = None
                if len(row_layout.children[1].children) > 0:
                    song_button = row_layout.children[1].children[0] if len(
                        row_layout.children[1].children) > 0 else None
                if song_button is not None and isinstance(song_button, Button):
                    votes = song_button.text.split("Helyezés: ")[1].split("\n")[0].strip()
                    votes = int(votes)
                    if votes > max_votes:
                        top_song = song_button
                        max_votes = votes

        if top_song is not None:
            top_song.color = (1, 1, 0, 1)
            self.table_scroll_view.scroll_to(top_song)
            artist = top_song.text.split('\n')[0].split(': ')[1]
            title = top_song.text.split('\n')[1].split(': ')[1]
            votes = top_song.text.split('\n')[2].split(': ')[1]
            message = f"{artist}, {title}, Pontszám: {votes}"
            self.message_box.text = message

    def export_to_xml(self, *args):
        root = ET.Element("songs")
        top_song = None
        max_votes = 0
        for row_layout in self.table_layout.children:
            if isinstance(row_layout, BoxLayout) and len(row_layout.children) > 1:
                song_label = row_layout.children[1].children[0] if len(row_layout.children[1].children) > 0 else None
                if song_label is not None and isinstance(song_label, Label):
                    artist = song_label.text.split('Előadó: ')[1].split('\nCím:')[0]
                    title = song_label.text.split('Cím: ')[1].split('\nHelyezés:')[0]
                    votes = int(song_label.text.split('Helyezés: ')[1])
                    song_element = ET.SubElement(root, "song")
                    ET.SubElement(song_element, "artist").text = artist
                    ET.SubElement(song_element, "title").text = title
                    ET.SubElement(song_element, "votes").text = str(votes)
                    if votes > max_votes:
                        max_votes = votes
                        top_song = song_element

        tree = ET.ElementTree(root)
        ET.indent(tree, space="\t", level=0)
        tree.write("songs.xml")
        self.message_box.text = "Az objektumlista exportálása XML formátumba sikeres!"

        if top_song is not None:
            top_song_artist = top_song.find("artist").text
            top_song_title = top_song.find("title").text
            top_song_votes = top_song.find("votes").text
            top_song_label = f"A legtöbb szavazatot kapott sláger:\n" \
                             f"{top_song_artist}, {top_song_title}, Pontszám: {top_song_votes}"
            self.message_box.text += f"\n\n{top_song_label}"

    def close(self, *args):
        App.get_running_app().stop()


class SongManagerApp(App):
    def build(self):
        return SongManager()


if __name__ == '__main__':
    SongManagerApp().run()

