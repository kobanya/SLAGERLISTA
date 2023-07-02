# Csizek Ferenc 2023.07.02

'''
Egy rádióállomás a betelefonáló hallgatóitól kérdezi a kedvenc slágereiket. Ezek nyilvántartására kell konzolos alkalmazást készítenie.
Minden egyes zeneszámot egy sorban, az előadó nevét, a szám címét és a szavazatszámot pontosvesszőkkel elválasztva tárolja az UTF-8 kódolású lista.csv nevű szöveges állomány. A fájl egy állapota már rendelkezésre áll.
A listába csak a legalább egy szavazatot kapott számok kerülhetnek fel, ha ugyanarra jön további szavazat, akkor csak a szavazatszám növekszik eggyel.
1.	A csv állomány tartalmát kell feldolgozni és első lépésként eltárolni objektumorientált módon.
2.	Készíts egy menüpontot, amely a program vezérlését végzi el:
a.	1-es menüpont: Kilistázza az adatokat a szavazatok száma szerinti csökkenő sorrendben.
Az adatok egyes elemeit getter segítségével kell elérni.
b.	2-es menüpont: Frissíti a szavazatok számát véletlenszerűen 0 és 50 közötti szavazathozzáadással
pl. az első sorban található dal adatai: AVA MAX;Sweet But Psycho;104  a frissítés után a korábbi 104 szavazathoz hozzáadunk véletlenszerűen generált 29 szavazatot, így az adat új tartalma az alábbi lesz: AVA MAX;Sweet But Psycho;133
Ezt setter beállításával kell elvégezni.
c.	3-as menüpont: Jelenítse meg a legtöbb szavazattal rendelkező dal adatait az alábbi formában.
pl. TOP 1: ALESSO - Remedy - 102 szavazat
d.	4-es menüpont: Exportálja az objektumlistát XML formátumba.
Az XML-tagek neveit és a fájl nevét szabadon lehet kiválasztani.
e.	0-s menüpont: Kilépés a programból

'''
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox
import xml.etree.ElementTree as ET
from random import randrange


class Slager:
    instances = []

    def __init__(self, eloado, cim, szavazat):
        self.cim = cim
        self.eloado = eloado
        self.szavazat = szavazat
        Slager.instances.append(self)


def beolvas():
    # 1.	A csv állomány tartalmát kell feldolgozni és első lépésként eltárolni objektumorientált módon.
    splitkari = ";"
    with open(r'lista.csv', encoding='utf-8') as file:
        lines = file.readlines()

    for line in lines:
        line = line.strip()
        slager = Slager(line.split(splitkari)[0], line.split(splitkari)[1], int(line.split(splitkari)[2]))


def kiir():
    for instance in Slager.instances:
        print(instance.eloado, instance.cim, instance.szavazat)


def sortedkiir():
    sorted_instances = sorted(Slager.instances, key=lambda x: x.szavazat, reverse=True)
    for instance in sorted_instances:
        print(instance.eloado, instance.cim, instance.szavazat)



def szavazrandom():
    for instance in Slager.instances:
        instance.szavazat += randrange(1, 51)



def legtobbszavazat():
    sorted_instances = sorted(Slager.instances, key=lambda x: x.szavazat, reverse=True)
    # for instance in :
    print(f"TOP1 : {sorted_instances[0].eloado} - {sorted_instances[0].cim} - {sorted_instances[0].szavazat} szavazat")


def exportXML():
    root = ET.Element("Slagerlista")
    sorted_instances = sorted(Slager.instances, key=lambda x: x.szavazat, reverse=True)
    for instance in sorted_instances:
        instance_element = ET.SubElement(root, "Instance")
        eloado_element = ET.SubElement(instance_element, "Eloado")
        eloado_element.text = instance.eloado
        name_element = ET.SubElement(instance_element, "Cim")
        name_element.text = instance.cim
        szavazat_element = ET.SubElement(instance_element, "Szavazat")
        szavazat_element.text = str(instance.szavazat)
    tree = ET.ElementTree(root)
    tree.write("sorted_instances.xml")


def update_listbox():
    # Sort the instances by szavazat attribute in descending order
    sorted_instances = sorted(Slager.instances, key=lambda x: x.szavazat, reverse=True)

    # Clear the listbox
    listbox.delete(0, tk.END)

    # Insert each sorted instance into the listbox
    for instance in sorted_instances:
        listbox.insert(tk.END, f"Előadó: {instance.eloado}, Cím: {instance.cim} Szavazat: {instance.szavazat}")


def update_listbox2():
    # Sort the instances by szavazat attribute in descending order
    for instance in Slager.instances:
        instance.szavazat = instance.szavazat + randrange(1, 50)
    sorted_instances = sorted(Slager.instances, key=lambda x: x.szavazat, reverse=True)

    # Clear the listbox
    listbox.delete(0, tk.END)

    # Insert each sorted instance into the listbox
    for instance in sorted_instances:
        listbox.insert(tk.END, f"Előadó: {instance.eloado}, Cím: {instance.cim} Szavazat: {instance.szavazat}")


def popup1():
    sorted_instances = sorted(Slager.instances, key=lambda x: x.szavazat, reverse=True)
    a = f"{sorted_instances[0].eloado} - {sorted_instances[0].cim} - {sorted_instances[0].szavazat} szavazat"
    messagebox.showinfo("TOP 1", a)



def exit_app():
    if messagebox.askokcancel("Exit", "Are you sure you want to exit?"):
        window.destroy()


beolvas()
sortedkiir()
szavazrandom()
sortedkiir()
legtobbszavazat()
szavazrandom()
exportXML()

window = tk.Tk()
window.attributes('-fullscreen', True)

button = tk.Button(window, text="Sort and Display", command=update_listbox)
button.pack()
button2 = tk.Button(window, text="Több szavazat", command=update_listbox2)
button2.pack()
button3 = tk.Button(window, text="Number One Song", command=popup1)
button3.pack()
button4 = tk.Button(window, text="Save to XML", command=exportXML)
button4.pack()
button_exit = tk.Button(window, text="Exit", command=exit_app)
button_exit.pack()

listbox = tk.Listbox(window)
listbox.pack(fill=tk.BOTH, expand=True)
window.protocol("WM_DELETE_WINDOW", exit_app)

scrollbar = ttk.Scrollbar(window, orient=tk.VERTICAL, command=listbox.yview)
listbox.configure(yscrollcommand=scrollbar.set)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
sizegrip = ttk.Sizegrip(window)
sizegrip.pack(anchor=tk.SE)

window.mainloop()