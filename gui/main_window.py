import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from utils.time_utils import tick, get_day_month_year, get_month_name_map

def initialize_main_window():
    window = tk.Tk()
    window.geometry("1280x720")
    window.resizable(True, False)
    window.title("Attendance System")
    window.configure(bg='#F2F2F2')  # Light background

    # Modern ttk theme
    style = ttk.Style()
    style.theme_use("clam")
    style.configure("TLabel", font=("Segoe UI", 11), background="#F2F2F2")
    style.configure("TButton", font=("Segoe UI", 10, "bold"), padding=6, relief="flat", background="#00BFA6", foreground="white")
    style.map("TButton", background=[("active", "#009e86")])

    # Background image with fade or glass look
    bg_image = Image.open("img2.png").resize((1280, 720))
    bg_photo = ImageTk.PhotoImage(bg_image)
    background_label = tk.Label(window, image=bg_photo)
    background_label.image = bg_photo
    background_label.place(x=0, y=0, relwidth=1, relheight=1)

    # Header Bar
    header = tk.Frame(window, bg="#00BFA6", height=70)
    header.pack(fill="x", side="top")

    tk.Label(header, text="📷 Face Recognition Based Attendance Monitoring System", fg="white",
             bg="#00BFA6", font=('Segoe UI', 22, 'bold')).pack(pady=10)

    # Date and Time Display
    day, month, year = get_day_month_year()
    mont = get_month_name_map()
    current_date = f"{day} {mont[month]} {year}"

    date_time_frame = tk.Frame(window, bg="#F2F2F2")
    date_time_frame.pack(pady=10)

    date_label = ttk.Label(date_time_frame, text=f"📅 {current_date}", foreground="#444", font=('Segoe UI', 12, 'bold'))
    date_label.pack(side="left", padx=20)

    clock = ttk.Label(date_time_frame, text="🕒 Loading...", foreground="#444", font=('Segoe UI', 12, 'bold'))
    clock.pack(side="left", padx=20)
    tick(clock)

    # Navigation buttons (example placeholders)
    nav_frame = tk.Frame(window, bg="#F2F2F2")
    nav_frame.pack(pady=30)

    # ttk.Button(nav_frame, text="Take Attendance").grid(row=0, column=0, padx=20)
    # ttk.Button(nav_frame, text="View Reports").grid(row=0, column=1, padx=20)
    # ttk.Button(nav_frame, text="Exit", command=window.destroy).grid(row=0, column=2, padx=20)

    return window, clock
