import os
import pandas as pd
import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
from datetime import datetime
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import tkinter.messagebox as mess
import random

def open_report_window():
    report_win = tk.Toplevel()
    report_win.title("Attendance Report")
    report_win.geometry("1200x700")
    report_win.configure(bg='#f8f9fa')

    df_list = []
    for file in os.listdir("Attendance"):
        if file.endswith(".csv"):
            path = os.path.join("Attendance", file)
            try:
                df = pd.read_csv(path)
                if not df.empty and 'Subject' in df.columns:
                    df['Date'] = file.replace("Attendance_", "").replace(".csv", "")
                    df['Date'] = pd.to_datetime(df['Date'], dayfirst=True, errors='coerce')
                    df_list.append(df)
            except Exception as e:
                print(f"Error reading {file}: {e}")

    if not df_list:
        mess.showinfo("No Data", "No attendance data found.")
        report_win.destroy()
        return

    full_df = pd.concat(df_list, ignore_index=True)
    full_df = full_df.dropna(subset=["Date", "Subject", "Name"])

    subjects = sorted(full_df['Subject'].dropna().unique())
    subjects.insert(0, "All")
    students = sorted(full_df['Name'].dropna().unique())

    style = ttk.Style()
    style.theme_use("clam")
    style.configure("Treeview.Heading", font=('Segoe UI', 10, 'bold'), background="#343a40", foreground="white")
    style.configure("Treeview", font=('Segoe UI', 10), rowheight=24)

    tk.Label(report_win, text="Select Subject:", bg="#f8f9fa", font=("Segoe UI", 10)).place(x=20, y=20)
    selected_subject = tk.StringVar(value="All")
    dropdown_subject = ttk.OptionMenu(report_win, selected_subject, selected_subject.get(), *subjects)
    dropdown_subject.place(x=130, y=15)

    tk.Label(report_win, text="Select Student:", bg="#f8f9fa", font=("Segoe UI", 10)).place(x=320, y=20)
    selected_student = tk.StringVar(value="All")
    dropdown_student = ttk.OptionMenu(report_win, selected_student, "All", "All", *students)
    dropdown_student.place(x=440, y=15)

    tk.Label(report_win, text="From:", bg="#f8f9fa", font=("Segoe UI", 10)).place(x=640, y=20)
    from_date = DateEntry(report_win, date_pattern='dd-mm-yyyy')
    from_date.place(x=680, y=15)

    tk.Label(report_win, text="To:", bg="#f8f9fa", font=("Segoe UI", 10)).place(x=800, y=20)
    to_date = DateEntry(report_win, date_pattern='dd-mm-yyyy')
    to_date.place(x=830, y=15)

    tree = ttk.Treeview(report_win, columns=('Name', 'Subject', 'Days Present'), show='headings', height=9)
    tree.heading('Name', text='Name')
    tree.heading('Subject', text='Subject')
    tree.heading('Days Present', text='Days Present')
    tree.column('Name', width=200)
    tree.column('Subject', width=140)
    tree.column('Days Present', width=110)
    tree.place(x=20, y=80)

    ttk.Label(report_win, text="📈 Attendance Chart", font=("Segoe UI", 11, "bold"), background="#f8f9fa").place(x=580, y=40)
    fig_bar, ax_bar = plt.subplots(figsize=(6, 5))  # reduced width by 20%
    canvas_bar = FigureCanvasTkAgg(fig_bar, master=report_win)
    canvas_bar.get_tk_widget().place(x=580, y=70)

    ttk.Label(report_win, text="📊 Subject-wise Distribution", font=("Segoe UI", 11, "bold"), background="#f8f9fa").place(x=20, y=350)
    fig_pie, ax_pie = plt.subplots(figsize=(4.2, 2.6))
    canvas_pie = FigureCanvasTkAgg(fig_pie, master=report_win)
    canvas_pie.get_tk_widget().place(x=20, y=380)

    def get_subject_color_map(subjects):
        colors = [f"#{random.randint(0, 0xFFFFFF):06x}" for _ in subjects]
        return dict(zip(subjects, colors))

    def update_report(*args):
        try:
            subject = selected_subject.get()
            student = selected_student.get()
            try:
                f_date = datetime.strptime(from_date.get(), "%d-%m-%Y") if from_date.get() else None
                t_date = datetime.strptime(to_date.get(), "%d-%m-%Y") if to_date.get() else None
            except ValueError:
                mess.showerror("Invalid Date", "Please select valid dates.")
                return

            filtered_df = full_df.copy()
            if f_date:
                filtered_df = filtered_df[filtered_df['Date'] >= f_date]
            if t_date:
                filtered_df = filtered_df[filtered_df['Date'] <= t_date]
            if subject != "All":
                filtered_df = filtered_df[filtered_df['Subject'] == subject]
            if student != "All":
                filtered_df = filtered_df[filtered_df['Name'] == student]

            unique_days = filtered_df.drop_duplicates(subset=['Name', 'Date', 'Subject'])
            summary = unique_days.groupby(['Name', 'Subject']).size().reset_index(name='Days Present')

            for item in tree.get_children():
                tree.delete(item)
            for _, row in summary.iterrows():
                tree.insert('', 'end', values=(row['Name'], row['Subject'], row['Days Present']))

            ax_bar.clear()
            ax_pie.clear()

            subject_color_map = {}
            pie_df = filtered_df.drop_duplicates(subset=['Name', 'Date', 'Subject'])
            subject_summary = pie_df.groupby('Subject').size().reset_index(name='Attendance Days')
            if not subject_summary.empty:
                subject_color_map = get_subject_color_map(subject_summary['Subject'])
                pie_colors = [subject_color_map[subj] for subj in subject_summary['Subject']]
                ax_pie.pie(subject_summary['Attendance Days'], labels=subject_summary['Subject'],
                           autopct='%1.1f%%', startangle=140, colors=pie_colors)
                ax_pie.axis('equal')
                ax_pie.set_title("Subject-wise Attendance Share")
            else:
                ax_pie.text(0.5, 0.5, 'No data', ha='center', va='center')

            if student == "All" and subject == "All":
                group = unique_days.groupby('Subject').size().reset_index(name='Attendance Days')
                if not group.empty:
                    bar_colors = [subject_color_map[subj] for subj in group['Subject']]
                    ax_bar.bar(group['Subject'], group['Attendance Days'], color=bar_colors)
                    ax_bar.set_title("Total Attendance per Subject")
                    ax_bar.set_ylabel("Total Days")
                    ax_bar.set_xticks(range(len(group)))
                    ax_bar.set_xticklabels(group['Subject'], rotation=30, ha='center', fontsize=8)
            else:
                if not summary.empty:
                    subject_counts = summary.groupby('Subject')['Days Present'].sum().reset_index()
                    bar_colors = [subject_color_map.get(subj, "#4dabf7") for subj in subject_counts['Subject']]
                    ax_bar.bar(subject_counts['Subject'], subject_counts['Days Present'], color=bar_colors)
                    ax_bar.set_title("Attendance per Subject")
                    ax_bar.set_ylabel("Days Present")
                    ax_bar.set_xticks(range(len(subject_counts)))
                    ax_bar.set_xticklabels(subject_counts['Subject'], rotation=30, ha='center', fontsize=8)
                else:
                    ax_bar.text(0.5, 0.5, 'No data', ha='center', va='center')

            canvas_bar.draw()
            canvas_pie.draw()

        except Exception as e:
            mess.showerror("Error", str(e))

    selected_subject.trace_add('write', update_report)
    selected_student.trace_add('write', update_report)
    from_date.bind("<<DateEntrySelected>>", lambda e: update_report())
    to_date.bind("<<DateEntrySelected>>", lambda e: update_report())

    update_report()
