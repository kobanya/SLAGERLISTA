import wx
import csv
import random
import xml.etree.ElementTree as ET
import wx.grid as gridlib


class SongManager(wx.Frame):
    def __init__(self):
        super().__init__(None, title="SLÁGERLISTA", size=(990, 500))

        self.panel = wx.Panel(self)
        self.message_box = wx.TextCtrl(self.panel, style=wx.TE_MULTILINE | wx.TE_READONLY)
        self.table = gridlib.Grid(self.panel)


        self.songs = []
        self.original_songs = []

        self.create_layout()
        self.load_songs_from_csv()

    def create_layout(self):
        sizer = wx.BoxSizer(wx.VERTICAL)
        self.panel.SetSizer(sizer)

        self.table.CreateGrid(0, 3)
        self.table.SetColLabelValue(0, "Előadó")
        self.table.SetColLabelValue(1, "Cím")
        self.table.SetColLabelValue(2, "Helyezés")
        self.table.SetColSize(0, 500)
        self.table.SetColSize(1, 300)
        self.table.SetColSize(2, 110)

        sizer.Add(self.table, 1, wx.EXPAND | wx.ALL, 5)

        self.message_box.SetMinSize((0, 50))
        sizer.Add(self.message_box, 0, wx.EXPAND | wx.ALL, 5)

        button_sizer = wx.BoxSizer(wx.HORIZONTAL)

        load_button = wx.Button(self.panel, label="Beolvasás")
        load_button.Bind(wx.EVT_BUTTON, self.load_songs_from_csv)
        button_sizer.Add(load_button, 0, wx.ALL, 5)

        update_button = wx.Button(self.panel, label="Frissítés - Szavazás")
        update_button.Bind(wx.EVT_BUTTON, self.update_votes)
        button_sizer.Add(update_button, 0, wx.ALL, 5)

        top_button = wx.Button(self.panel, label="1. hely")
        top_button.Bind(wx.EVT_BUTTON, self.show_top_song)
        button_sizer.Add(top_button, 0, wx.ALL, 5)

        export_button = wx.Button(self.panel, label="XML")
        export_button.Bind(wx.EVT_BUTTON, self.export_to_xml)
        button_sizer.Add(export_button, 0, wx.ALL, 5)

        exit_button = wx.Button(self.panel, label="Kilépés")
        exit_button.Bind(wx.EVT_BUTTON, self.OnClose)
        exit_button.SetBackgroundColour("red")
        exit_button.SetForegroundColour("white")
        button_sizer.Add(exit_button, 0, wx.ALL, 5)

        sizer.Add(button_sizer, 0, wx.ALIGN_RIGHT)

    def load_songs_from_csv(self, event=None):
        self.original_songs = []
        filename = "lista.csv"
        with open(filename, "r") as file:
            reader = csv.reader(file, delimiter=";")
            for row in reader:
                artist, title, votes = row
                votes = int(votes)
                self.original_songs.append({"artist": artist, "title": title, "votes": votes})
        self.update_song_list()
        self.clear_message_box()

    def clear_message_box(self):
        self.message_box.Clear()

    def update_song_list(self):
        self.songs = list(self.original_songs)
        self.list_songs()
        self.clear_message_box()

    def list_songs(self):
        self.table.ClearGrid()
        sorted_songs = sorted(self.songs, key=lambda x: x["votes"], reverse=True)
        self.table.AppendCols(3)
        self.table.SetColLabelValue(0, "Előadó")
        self.table.SetColLabelValue(1, "Cím")
        self.table.SetColLabelValue(2, "Helyezés")
        self.table.AppendRows(len(sorted_songs))
        for row, song in enumerate(sorted_songs):
            self.table.SetCellValue(row, 0, song["artist"])
            self.table.SetCellValue(row, 1, song["title"])
            self.table.SetCellValue(row, 2, str(song["votes"]))

    def update_votes(self, event=None):
        for song in self.songs:
            song["votes"] += random.randint(0, 50)
        self.list_songs()
        self.clear_message_box()

    def show_top_song(self, event=None):
        global row
        if self.songs:
            top_song = max(self.songs, key=lambda x: x["votes"])
            self.table.ClearSelection()
            for row in range(self.table.GetNumberRows()):
                if self.table.GetCellValue(row, 0) == top_song["artist"] and \
                        self.table.GetCellValue(row, 1) == top_song["title"] and \
                        self.table.GetCellValue(row, 2) == str(top_song["votes"]):
                    for col in range(self.table.GetNumberCols()):
                        self.table.SetCellBackgroundColour(row, col, wx.YELLOW)
                        self.table.SetCellTextColour(row, col, wx.BLACK)
                        font = self.table.GetCellFont(row, col)
                        font.SetWeight(wx.BOLD)
                        self.table.SetCellFont(row, col, font)
                    self.table.MakeCellVisible(row, 0)
                    break

            message = f"A legtöbb szavazatot kapott sláger:\n" \
                      f"Előadó: {self.table.GetCellValue(row, 0)}," \
                      f"   Cím:  {self.table.GetCellValue(row, 1)}," \
                      f"   Pontszám: {self.table.GetCellValue(row, 2)}"

            self.message_box.SetValue(message)

    def export_to_xml(self, event=None):
        root = ET.Element("songs")
        for song in self.songs:
            song_element = ET.SubElement(root, "song")
            ET.SubElement(song_element, "artist").text = song["artist"]
            ET.SubElement(song_element, "title").text = song["title"]
            ET.SubElement(song_element, "votes").text = str(song["votes"])
        tree = ET.ElementTree(root)
        ET.indent(tree, space="\t", level=0)
        tree.write("songs.xml")
        self.message_box.SetValue("Az objektumlista exportálása XML formátumba, sikeres!")

    def OnClose(self, event):
        self.Close()


if __name__ == "__main__":
    app = wx.App()
    song_manager = SongManager()
    song_manager.Show()
    app.MainLoop()
