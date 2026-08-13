import tkinter as tk

def create_main_frames(window):
    # Blue-themed background color (light modern blue)
    blue_bg = "#e6f0ff"       # Light bluish background
    border_color = "#a3c9f9"  # Border color for subtle shadow

    # Left panel (TreeView, Attendance, Reports)
    frame1 = tk.Frame(
        window,
        bg=blue_bg,
        bd=3,
        highlightbackground=border_color,
        highlightthickness=2,
        relief="ridge"
    )
    frame1.place(relx=0.05, rely=0.17, relwidth=0.40, relheight=0.67)

    # Right panel (Input form, Capture, Training)
    frame2 = tk.Frame(
        window,
        bg=blue_bg,
        bd=3,
        highlightbackground=border_color,
        highlightthickness=2,
        relief="ridge"
    )
    frame2.place(relx=0.55, rely=0.17, relwidth=0.40, relheight=0.67)

    return frame1, frame2
