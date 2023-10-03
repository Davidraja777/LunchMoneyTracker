import PySimpleGUI as sg
import json
import os
from datetime import datetime

# Constants
FILENAME = f"{datetime.now().strftime('%B_%Y')}.json"

# Check if file exists, if not create one
if not os.path.exists(FILENAME):
    data = {
        "Ho": [],
        "Sing Ying": [],
        "Sekher": []
    }
    with open(FILENAME, 'w') as file:
        json.dump(data, file)

# Load data from file
with open(FILENAME, 'r') as file:
    data = json.load(file)

def save_data():
    with open(FILENAME, 'w') as file:
        json.dump(data, file)

def main_window():
    layout = [
        [sg.Text('Ho:'), sg.Text(sum(data['Ho']), key='Ho'), sg.Button('Add', key='Add_Ho'), sg.Button('Deduct', key='Deduct_Ho')],
        [sg.Text('Sing Ying:'), sg.Text(sum(data['Sing Ying']), key='Sing Ying'), sg.Button('Add', key='Add_Sing Ying'), sg.Button('Deduct', key='Deduct_Sing Ying')],
        [sg.Text('Sekher:'), sg.Text(sum(data['Sekher']), key='Sekher'), sg.Button('Add', key='Add_Sekher'), sg.Button('Deduct', key='Deduct_Sekher')],
        [sg.CalendarButton('View Transactions', target='Input', format='%Y-%m-%d')],
        [sg.InputText('', key='Input', visible=False), sg.Button('Show')],
        [sg.Button('Exit')]
    ]

    window = sg.Window('Lunch Money Tracker', layout)

    while True:
        event, values = window.read()

        if event == sg.WIN_CLOSED or event == 'Exit':
            break
        elif 'Add' in event:
            name = event.split('_')[1]
            amount = sg.popup_get_text(f'Enter amount to add for {name}')
            if amount:
                data[name].append(float(amount))
                save_data()
                window[name].update(sum(data[name]))
        elif 'Deduct' in event:
            name = event.split('_')[1]
            amount = sg.popup_get_text(f'Enter amount to deduct for {name}')
            if amount:
                data[name].append(-float(amount))
                save_data()
                window[name].update(sum(data[name]))
        elif event == 'Show':
            date = values['Input']
            sg.popup(f"Transactions for {date}:\n\n" + '\n'.join([f"{name}: {sum([amt for d, amt in data[name] if d == date])}" for name in data]))

    window.close()

main_window()

