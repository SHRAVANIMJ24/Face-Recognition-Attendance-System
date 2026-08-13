import tkinter as tk
from tkinter import ttk

def create_labels_entries_buttons(frame1, frame2):
    blue1 = "#0099ff"  # Primary
    blue2 = "#d0eaff"  # Light background
    blue3 = "#006bb3"  # Dark text on buttons

    lbl = tk.Label(frame2, text="Enter ID", width=10, height=1, fg="white", bg=blue1, font=('Comic Sans MS', 17, 'bold'))
    lbl.place(x=30, y=45)
    txt = tk.Entry(frame2, width=28, fg="black", bg=blue2, font=('Comic Sans MS', 15, 'bold'), relief='solid', bd=1)
    txt.place(x=30, y=88)

    lbl2 = tk.Label(frame2, text="Enter Name", width=10, fg="white", bg=blue1, font=('Comic Sans MS', 17, 'bold'))
    lbl2.place(x=30, y=130)
    txt2 = tk.Entry(frame2, width=28, fg="black", bg=blue2, font=('Comic Sans MS', 15, 'bold'), relief='solid', bd=1)
    txt2.place(x=30, y=173)

    message1 = tk.Label(frame2, text="1) Take Images  >>>  2) Save Profile", bg=blue1, fg="white",
                        width=34, height=1, font=('Comic Sans MS', 15, 'bold'))
    message1.place(x=30.1, y=230)

    message = tk.Label(frame2, text="", bg=blue2, fg="black", width=1, height=1, font=('Comic Sans MS', 1, 'bold'))
    message.place(x=7, y=450)

    lbl3 = tk.Label(frame1, text="Attendance", width=20, fg="white", bg=blue1, height=1, font=('Comic Sans MS', 13, 'bold'))
    lbl3.place(x=130, y=125)

    return txt, txt2, message1, message

def create_treeview(frame1):
    style = ttk.Style()
    style.theme_use("default")

    # Blue theme colors
    bg_even = "#e3f3ff"
    bg_odd = "#cbe6ff"
    select_bg = "#3399ff"
    heading_bg = "#007acc"
    heading_active = "#005b99"

    # Configure Treeview style
    style.configure("Treeview",
                    background=bg_even,
                    foreground="black",
                    rowheight=30,
                    fieldbackground=bg_even,
                    font=('Segoe UI', 11))
    style.map("Treeview", background=[('selected', select_bg)])

    style.configure("Treeview.Heading",
                    background=heading_bg,
                    foreground="white",
                    font=('Segoe UI Semibold', 12),
                    relief="flat")
    style.map("Treeview.Heading", background=[('active', heading_active)])

    # Tags for zebra striping
    def tag_rows(tree):
        for i, item in enumerate(tree.get_children()):
            tree.item(item, tags=('evenrow' if i % 2 == 0 else 'oddrow'))
        tree.tag_configure('evenrow', background=bg_even)
        tree.tag_configure('oddrow', background=bg_odd)

    # Create Treeview
    tv = ttk.Treeview(frame1, style="Treeview", height=7, columns=('name', 'date', 'time', 'subject'))

    # Define columns
    tv.column('#0', width=60, anchor='center')
    tv.column('name', width=100, anchor='center')
    tv.column('date', width=100, anchor='center')
    tv.column('time', width=100, anchor='center')
    tv.column('subject', width=100, anchor='center')

    # Headings with sorting
    tv.heading('#0', text='ID', command=lambda: sort_column(tv, '#0', False))
    tv.heading('name', text='NAME', command=lambda: sort_column(tv, 'name', False))
    tv.heading('date', text='DATE', command=lambda: sort_column(tv, 'date', False))
    tv.heading('time', text='TIME', command=lambda: sort_column(tv, 'time', False))
    tv.heading('subject', text='SUBJECT', command=lambda: sort_column(tv, 'subject', False))

    # Place using absolute coordinates
    tv.place(x=20, y=160)

    # Vertical scrollbar
    scroll_y = ttk.Scrollbar(frame1, orient='vertical', command=tv.yview)
    scroll_y.place(x=467, y=184, height=210)  # Adjust x and height to align properly
    tv.configure(yscrollcommand=scroll_y.set)

    # Apply row tag method
    tv._tag_rows = lambda: tag_rows(tv)

    return tv

def sort_column(treeview, col, reverse):
    data = [(treeview.set(k, col), k) for k in treeview.get_children('')]
    try:
        data.sort(key=lambda t: float(t[0]) if t[0].replace('.', '', 1).isdigit() else t[0], reverse=reverse)
    except:
        data.sort(key=lambda t: t[0], reverse=reverse)

    for index, (val, k) in enumerate(data):
        treeview.move(k, '', index)

    treeview.heading(col, command=lambda: sort_column(treeview, col, not reverse))

    if hasattr(treeview, '_tag_rows'):
        treeview._tag_rows()
