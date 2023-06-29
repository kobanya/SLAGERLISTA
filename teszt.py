# ANSI Escape kódok
SARGA = '\033[93m'
ALAP = '\033[0m'
KEK = '\033[94m'
ZOLD = '\033[92m'
import os

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

# Fő program
while True:
    clear_screen()

    print(f"{SARGA}----- MENÜ -----")
    print("1. Kilistázza az adatokat a szavazatok száma szerinti csökkenő sorrendben.")
    print("2. Frissíti a szavazatok számát véletlenszerűen 0 és 50 közötti szavazathozzáadással.")
    print("3. Jelenítse meg a legtöbb szavazattal rendelkező dal adatait.")
    print("4. Exportálja az objektumlistát XML formátumba.")
    print(f"0. Kilépés a programból.{ALAP}\n")

    choice = input(f"{ZOLD}Válasszon menüpontot: {ALAP}")

    # Menükezelés és további folytatás...
