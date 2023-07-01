import PySimpleGUI as sg

layout = [
    [sg.Button('Kilépés', button_type=7)]
]

window = sg.Window('My Window', layout)

while True:
    event, values = window.read()
    if event == sg.WINDOW_CLOSED:
        break

window.close()
