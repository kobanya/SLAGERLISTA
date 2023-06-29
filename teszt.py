def draw_rectangle(width, height):
    horizontal_line = "+" + "-" * (width - 2) + "+"
    vertical_line = "|" + " " * (width - 2) + "|"

    print(horizontal_line)
    for _ in range(height - 2):
        print(vertical_line)
    print(horizontal_line)

def draw_menu(menu_options):
    print("Menüpontok:")
    for i, option in enumerate(menu_options, start=1):
        print(f"{i} - {option}")

# Négyzet körvonalának kirajzolása
width = 20
height = 10
draw_rectangle(width, height)

# Menüpontok megjelenítése
menu_options = ["lista", "frissít", "kilép"]
draw_menu(menu_options)
