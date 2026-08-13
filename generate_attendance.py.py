import pandas as pd
import numpy as np
import os
from datetime import datetime, timedelta

def generate_attendance_for_date(date_str, timetable_df, roster_df,
                                 min_pct=80, max_pct=100, random_seed=None):
    """
    Generate attendance records for a single date, listing only present students.

    Args:
        date_str (str): Date in 'dd-mm-YYYY' format.
        timetable_df (pd.DataFrame): DataFrame with columns ['TimeFrom', 'Monday', ...].
        roster_df (pd.DataFrame): DataFrame with columns ['Id', 'Name'].
        min_pct (int): Minimum percentage of students present per class.
        max_pct (int): Maximum percentage of students present per class.
        random_seed (int, optional): Seed for reproducibility.

    Returns:
        pd.DataFrame: Attendance rows for present students only,
                      with columns ['Id','Name','Date','Time','Subject'].
    """
    # Parse date & find weekday
    date_obj = datetime.strptime(date_str, '%d-%m-%Y')
    weekday = date_obj.strftime('%A')
    if weekday not in timetable_df.columns:
        raise ValueError(f"Weekday '{weekday}' not in timetable")

    # Extract today's schedule
    schedule = (
        timetable_df[['TimeFrom', weekday]]
        .dropna()
        .rename(columns={'TimeFrom': 'Time', weekday: 'Subject'})
    )

    # Build one row per student per class slot
    rows = []
    for _, student in roster_df.iterrows():
        for _, slot in schedule.iterrows():
            rows.append({
                'Id':      student['Id'],
                'Name':    student['Name'].strip(),
                'Date':    date_str,
                'Time':    slot['Time'],
                'Subject': slot['Subject']
            })
    df = pd.DataFrame(rows)

    # Randomly select present students per slot
    if random_seed is not None:
        np.random.seed(random_seed)

    present_rows = []
    for (time, subj), group in df.groupby(['Time', 'Subject']):
        n = len(group)
        low  = int(np.ceil(min_pct/100 * n))
        high = int(np.floor(max_pct/100 * n))
        count = np.random.randint(low, high + 1)
        present = group.sample(count)
        present_rows.append(present)

    # Concatenate and return only present students
    return pd.concat(present_rows, ignore_index=True)

def generate_attendance_range(start_date_str, end_date_str,
                              timetable_path, roster_path,
                              output_dir,
                              min_pct=80, max_pct=100, random_seed=None):
    """
    Generate attendance CSVs for each date in [start_date_str, end_date_str],
    listing only present students.

    - Skips days whose weekday isn't a column in the timetable (e.g. weekends).
    - Writes files as Attendance_DD-MM-YYYY.csv into output_dir.
    """
    # Load inputs
    tt_df     = pd.read_csv(timetable_path)
    roster_df = pd.read_csv(roster_path)
    os.makedirs(output_dir, exist_ok=True)

    current = datetime.strptime(start_date_str, '%d-%m-%Y')
    end     = datetime.strptime(end_date_str,   '%d-%m-%Y')
    one_day = timedelta(days=1)

    while current <= end:
        date_str = current.strftime('%d-%m-%Y')
        try:
            present_df = generate_attendance_for_date(
                date_str, tt_df, roster_df,
                min_pct=min_pct, max_pct=max_pct,
                random_seed=random_seed
            )
            out_file = os.path.join(output_dir, f'Attendance_{date_str}.csv')
            present_df.to_csv(out_file, index=False)
            print(f"Saved: {out_file}")
        except ValueError:
            # skip if timetable has no column for this weekday
            print(f"Skipping {date_str} (no classes)")
        current += one_day

if __name__ == "__main__":
    # Example: generate from 01-04-2025 to 10-04-2025
    generate_attendance_range(
        start_date_str='01-03-2025',
        end_date_str='17-04-2025',
        timetable_path='TimeTable.csv',
        roster_path='attendance_sheet_corrected.csv',
        output_dir='Attendance',
        min_pct=80,
        max_pct=100,
        random_seed=42
    )
