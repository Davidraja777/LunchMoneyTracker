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

def main_window():
    # Get month and year
    month = datetime.now().month
    year = datetime.now().year

    # Get the first day of the month and the number of days in the month
    first_day, num_days = calendar.monthrange(year, month)

    # Create calendar layout
    days = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']
    calendar_layout = [[sg.Text(day, size=(10,1)) for day in days]]

    day_buttons = []
    for _ in range(6):  # 6 weeks max
        row = []
        for _ in range(7):  # 7 days
            row.append(sg.Button('', size=(10,2), key=f'Day_{len(day_buttons)+1}', button_color=('black', 'white')))
            day_buttons.append(row[-1])
        calendar_layout.append(row)

    layout = [
        [sg.Text(f'{datetime.now().strftime("%B %Y")}', size=(70,1), justification='center')],
        [sg.Column(calendar_layout)],
        [sg.Text('Select a day from the calendar to add or deduct money.')],
        [sg.Text('Name:'), sg.Combo(['Ho', 'Sing Ying', 'Sekher'], key='Name')],
        [sg.Text('Amount:'), sg.InputText('', key='Amount')],
        [sg.Radio('Add', "RADIO1", default=True, key='Add'), sg.Radio('Deduct', "RADIO1", key='Deduct')],
        [sg.Button('Submit'), sg.Button('Exit')]
    ]

    window = sg.Window('Lunch Money Tracker', layout, resizable=True)

    # Fill in the days of the month
    for i in range(num_days):
        day_button = day_buttons[i + first_day]
        day_button.update(str(i + 1))

    # Update calendar with data
    for name in data:
        for date, amount in data[name].items():
            day = int(date.split("-")[-1])
            day_button = f'Day_{day}'
            if day_button in window.keys():
                current_text = window[day_button].get_text()
                new_text = f"{current_text}\n{name}: {'+' if amount > 0 else ''}{amount}"
                color = 'green' if amount > 0 else 'red'
                window[day_button].update(new_text, button_color=('black', color))

    while True:
        event, values = window.read()

        if event == sg.WIN_CLOSED or event == 'Exit':
            break
        elif 'Day_' in event:
            window['Name'].set_focus()
        elif event == 'Submit':
            name = values['Name']
            date = datetime.now().strftime('%Y-%m-') + event.split('_')[1]
            amount = float(values['Amount']) if values['Add'] else -float(values['Amount'])
            if date not in data[name]:
                data[name][date] = 0
            data[name][date] += amount
            save_data()
            day_button = f'Day_{int(date.split("-")[-1])}'
            current_text = window[day_button].get_text()
            new_text = f"{current_text}\n{name}: {'+' if amount > 0 else ''}{amount}"
            color = 'green' if amount > 0 else 'red'
            window[day_button].update(new_text, button_color=('black', color))

    window.close()

main_window()
