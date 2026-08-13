import time
from datetime import datetime

def tick(clock_label):
    current_time = time.strftime('%I:%M:%S %p')
    clock_label.config(text=current_time)
    clock_label.after(1000, lambda: tick(clock_label))

def get_formatted_date():
    ts = time.time()
    return datetime.fromtimestamp(ts).strftime('%d-%m-%Y')

def get_day_month_year():
    date = get_formatted_date()
    day, month, year = date.split("-")
    return day, month, year

def get_month_name_map():
    return {
        '01': 'January', '02': 'February', '03': 'March', '04': 'April',
        '05': 'May', '06': 'June', '07': 'July', '08': 'August',
        '09': 'September', '10': 'October', '11': 'November', '12': 'December'
    }
