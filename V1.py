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
print("Reloaded data:", data)

def save_data(data_to_save, window):
    print("Attempting to save data...")
    with open(FILENAME, 'w') as file:
        json.dump(data_to_save, file)
    print(f"Data saved to {FILENAME}")

    # Reload data after saving
    with open(FILENAME, 'r') as file:
        reloaded_data = json.load(file)
    print("Reloaded data:", reloaded_data)
    
    return reloaded_data  # Return the reloaded data

def update_all_buttons(window):
    """Update all day buttons in the GUI."""
    _, num_days = calendar.monthrange(datetime.now().year, datetime.now().month)
    for i in range(1, num_days+1):
        update_day_button(window, i)

def get_cumulative_balance(name, day):
    """
    Calculate the cumulative balance for a given name and day.

    Parameters:
    - name (str): The name of the individual.
    - day (int): The day for which the balance is to be calculated.

    Returns:
    - float: The cumulative balance for the given name and day.
    """
    # Convert the day into the desired date format
    date = datetime.now().strftime('%Y-%m-') + str(day)
    
    # Access the balance for the given name and date
    balance = data.get(name, {}).get(date, 0)
    
    # Calculate the cumulative balance up to the given day
    cumulative_balance = sum(data.get(name, {}).get(datetime.now().strftime('%Y-%m-') + str(i), 0) for i in range(1, day + 1))
    
    return cumulative_balance

def update_day_button(window, day):
    date = datetime.now().strftime('%Y-%m-') + str(day)
    texts = [f"Day {day}"]
    
    for name in ["Ho", "Sing Ying", "Sekher"]:
        balance = get_cumulative_balance(name, day)
        color = '#d4a373' if balance > 0 else '#d4a373'
        texts.append(f"{name}: {balance:.2f}")
        
    window[f'Day_{day}'].update('\n'.join(texts), button_color=('black', color))
    window.refresh()  # Force window to refresh

def show_balance():
    current_day = datetime.now().day
    balances = {
        "Ho": get_cumulative_balance("Ho", current_day),
        "Sing Ying": get_cumulative_balance("Sing Ying", current_day),
        "Sekher": get_cumulative_balance("Sekher", current_day)
    }
    
    balance_layout = [
        [sg.Text(f"{name}: {amount}", size=(15,1)) for name, amount in balances.items()],
        [sg.Button('Close')]
    ]
    
    balance_window = sg.Window('Current Balances', balance_layout)
    while True:
        b_event, b_values = balance_window.read()
        if b_event == sg.WIN_CLOSED or b_event == 'Close':
            break
    balance_window.close()

def select_month():
    month_names = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    layout = [[sg.Button(month)] for month in month_names] + [[sg.Button('Exit')]]
    
    window = sg.Window('Select Month', layout, background_color='#faedcd')
    
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Exit':
            window.close()
            return None
        elif event in month_names:
            window.close()
            return event

def main_window(month_name=None):
    global data
    if not month_name:
        month = datetime.now().month
    else:
        month = datetime.strptime(month_name, '%B').month
    year = datetime.now().year

    global FILENAME
    FILENAME = f"{month_name}_{year}.json"

    # Ensure data is loaded every time main_window is called
    if not os.path.exists(FILENAME):
        data = {
            "Ho": {},
            "Sing Ying": {},
            "Sekher": {}
        }
        with open(FILENAME, 'w') as file:
            json.dump(data, file)
    else:
        with open(FILENAME, 'r') as file:
            data = json.load(file)
    print("Reloaded data:", data)

    first_day, num_days = calendar.monthrange(year, month)
    days = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']
    calendar_layout = [[sg.Text(day, size=(13,0), justification = 'center', background_color='#faedcd', text_color='black', font=('Any', 19)) for day in days]]
    day_counter = 1

    for _ in range(6):  # 6 weeks max
        row = []
        for j in range(7):  # 7 days
            if day_counter > num_days:
                row.append(sg.Button('', size=(15,3), button_color=('black', '#fefae0')))
            elif len(calendar_layout) == 1 and j < first_day:
                row.append(sg.Button('', size=(15,3), button_color=('black', '#fefae0')))
            else:
                row.append(sg.Button('', size=(15,3), key=f'Day_{day_counter}', button_color=('black', 'white',), font=('Any', 9)))
                day_counter += 1
        calendar_layout.append(row)

    layout = [
        [sg.Text(f'{month_name} {year}', size=(92,0), justification='center', background_color='#faedcd', text_color='black', font=('Any', 20))],
        [sg.Column(calendar_layout, background_color='#faedcd')],
        [sg.Button('See Balance'), sg.Button('Exit')]
    ]

    window = sg.Window('Lunch Money Tracker', layout, resizable=True, finalize=True, background_color='#faedcd')

    for i in range(1, num_days+1):
        update_day_button(window, i)

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
                [sg.Radio('Add', "RADIO1", default=True, key='Radio_Add'), sg.Radio('Deduct', "RADIO1", key='Radio_Deduct')],
                [sg.Button('Submit'), sg.Button('Close')]
            ]
            edit_window = sg.Window('Edit Transaction', layout, modal=True)
            while True:
                e_event, e_values = edit_window.read()
                if e_event == sg.WIN_CLOSED or e_event == 'Close':
                    break
                elif e_event == 'Submit':
                    name = e_values['Name']
                    if e_values['Radio_Add']:
                        transaction = {"amount": float(e_values['Amount']), "type": "add"}
                    elif e_values['Radio_Deduct']:
                        transaction = {"amount": float(e_values['Amount']), "type": "deduct"}
                    
                    if date not in data[name]:
                        data[name][date] = []
                    data[name][date].append(transaction)
                    
                    data = save_data(data, window)  # Save, reload the data, and assign it back to the data variable
                    update_day_button(window, day)  # Update the button immediately after modifying the data
                    window.refresh()

                elif e_event == 'View Transactions':
                    transactions_text = []
                    for name, transactions in data.items():
                        if date in transactions:
                            for transaction in transactions[date]:
                                transactions_text.append(f"{name}: {'+' if transaction['type'] == 'add' else '-'}{transaction['amount']}")
                    transactions_window = sg.Window('Transactions', [[sg.Text('\n'.join(transactions_text))], [sg.Button('Close')]])
                    transactions_window.read()
                    transactions_window.close()
                    
                    edit_window.close()
            update_all_buttons(window)
        elif event == 'See Balance':
            show_balance()

    window.close()

selected_month = select_month()
if selected_month:
    main_window(selected_month)
