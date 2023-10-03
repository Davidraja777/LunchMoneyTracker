import PySimpleGUI as sg
import json
import os
import calendar
from datetime import datetime

# Constants
FILENAME = f"{datetime.now().strftime('%B_%Y')}.json"

# Check if file exists, if not create one
if not os.path.exists(FILENAME):
    data = {
        "Ho": {},
        "Sing Ying": {},
        "Sekher": {}
    }
    with open(FILENAME, 'w') as file:
        json.dump(data, file)

# Load data from file
with open(FILENAME, 'r') as file:
    data = json.load(file)

def save_data():
    with open(FILENAME, 'w') as file:
        json.dump(data, file)

def update_day_button(window, day):
    date = datetime.now().strftime('%Y-%m-') + str(day)
    texts = [f"Day {day}"]
    for name in ["Ho", "Sing Ying", "Sekher"]:
        amount = data[name].get(date, 0)
        color = 'green' if amount > 0 else 'red'
        texts.append(f"{name}: {'+' if amount > 0 else ''}{amount}")
    window[f'Day_{day}'].update('\n'.join(texts), button_color=('black', color))

def main_window():
    # Get month and year
    month = datetime.now().month
    year = datetime.now().year

    # Get the first day of the month and the number of days in the month
    first_day, num_days = calendar.monthrange(year, month)

    # Create calendar layout
    days = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']
    calendar_layout = [[sg.Text(day, size=(15,1)) for day in days]]

    for _ in range(6):  # 6 weeks max
        row = []
        for _ in range(7):  # 7 days
            row.append(sg.Button('', size=(15,4), key=f'Day_{len(row)+1+len(calendar_layout[1])*len(calendar_layout)}', button_color=('black', 'white')))
        calendar_layout.append(row)

    layout = [
        [sg.Text(f'{datetime.now().strftime("%B %Y")}', size=(105,1), justification='center')],
        [sg.Column(calendar_layout)],
        [sg.Button('Exit')]
    ]

    window = sg.Window('Lunch Money Tracker', layout, resizable=True)

    # Fill in the days of the month
    for i in range(num_days):
        update_day_button(window, i+1)

    while True:
        event, values = window.read()

        if event == sg.WIN_CLOSED or event == 'Exit':
            break
        elif 'Day_' in event:
            day = int(event.split('_')[1])
            date = datetime.now().strftime('%Y-%m-') + str(day)
            layout = [
                [sg.Text(f'Date: {date}')],
                [sg.Text('Name:'), sg.Combo(['Ho', 'Sing Ying', 'Sekher'], key='Name')],
                [sg.Text('Amount:'), sg.InputText('', key='Amount')],
                [sg.Radio('Add', "RADIO1", default=True, key='Add'), sg.Radio('Deduct', "RADIO1", key='Deduct')],
                [sg.Button('Submit'), sg.Button('Close')]
            ]
            edit_window = sg.Window('Edit Transaction', layout)
            while True:
                e_event, e_values = edit_window.read()
                if e_event == sg.WIN_CLOSED or e_event == 'Close':
                    break
                elif e_event == 'Submit':
                    name = e_values['Name']
                    amount = float(e_values['Amount']) if e_values['Add'] else -float(e_values['Amount'])
                    if date not in data[name]:
                        data[name][date] = 0
                    data[name][date] += amount
                    save_data()
                    update_day_button(window, day)
            edit_window.close()

    window.close()

main_window()
