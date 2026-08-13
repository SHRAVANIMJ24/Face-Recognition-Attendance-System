import tkinter as tk
from gui.main_window import initialize_main_window
from gui.frames import create_main_frames
from gui.widgets import create_labels_entries_buttons, create_treeview
from gui.report_window import open_report_window
import sys
sys.path.append('utils')
sys.path.append('facial_recognition')
from password_utils import change_pass
from capture import TakeImages
from train import TrainImages
from attendance import TrackImages
from email_utils import send_email
from utils.file_utils import delete_registration_csv, delete_attendance_csv, delete_registered_images
from datetime import datetime

# Initialize main window
window, clock = initialize_main_window()

# Create frames and widgets
frame1, frame2 = create_main_frames(window)
txt, txt2, message1, message = create_labels_entries_buttons(frame1, frame2)
tv = create_treeview(frame1)

blue1 = "#0099ff"  # Primary
blue2 = "#d0eaff"  # Light background
blue3 = "#006bb3"  # Dark text on buttons

# Button actions
def clear():
    txt.delete(0, 'end')
    message1.config(text="1)Take Images  >>>  2)Save Profile")

def clear2():
    txt2.delete(0, 'end')
    message1.config(text="1)Take Images  >>>  2)Save Profile")

def psw():
    TrainImages(message1, message)

def send_email_wrapper():
    recipient = recipient_email_entry.get()
    domain = domain_var.get()
    today = datetime.now().strftime('%d-%m-%Y')
    send_email(recipient, domain, today)

def delete_attendance_today():
    today = datetime.now().strftime('%d-%m-%Y')
    delete_attendance_csv(today)

# Buttons
clearButton = tk.Button(frame2, text="Clear", command=clear, bg="#6d00fc", fg="white", font=('comic', 11, 'bold'))
clearButton.place(x=395, y=86)

clearButton2 = tk.Button(frame2, text="Clear", command=clear2, bg="#6d00fc", fg="white", font=('comic', 11, 'bold'))
clearButton2.place(x=395, y=172)

takeImg = tk.Button(frame2, text="Take Images", command=lambda: TakeImages(txt, txt2, message1, message),
                    bg="#6d00fc", fg="white", font=('comic', 15, 'bold'), width=34)
takeImg.place(x=30, y=300)

trainImg = tk.Button(frame2, text="Save Profile", command=psw,
                     bg="#6d00fc", fg="white", font=('comic', 15, 'bold'), width=34)
trainImg.place(x=30, y=380)

trackImg = tk.Button(frame1, text="Take Attendance", command=lambda: TrackImages(tv, message, window),
                     bg="#6d00fc", fg="white", font=('comic', 12, 'bold'), width=13)
trackImg.place(x=80, y=77)

btn_report = tk.Button(frame1, text="View Reports", command=open_report_window,
                       bg="#6d00fc", fg="white", font=('comic', 12, 'bold'), width=13)
btn_report.place(x=250, y=77)

quitWindow = tk.Button(frame1, text="Quit", command=window.destroy,
                       bg="#6d00fc", fg="white", font=('comic', 12, 'bold'), width=10)
quitWindow.place(x=180, y=420)

# Email section
email_domains = ["gmail.com", "yahoo.com", "hotmail.com"]
#recipient_email_entry = tk.Entry(frame1, width=20, font=('comic', 15, 'bold'))
recipient_email_entry = tk.Entry(frame1, width=21, fg="black", bg=blue2, font=('Comic Sans MS', 12, 'bold'), relief='solid', bd=1)
recipient_email_entry.place(x=14, y=46)

recipient_email_label = tk.Label(frame1, text="Recipient's Email", width=30, fg="white", bg=blue1, font=('comic', 9, 'bold'))
recipient_email_label.place(x=14, y=20)

domain_label = tk.Label(frame1, text="Domain:", width=20, fg="white", bg=blue1, font=('comic', 9, 'bold'))
domain_label.place(x=253, y=20)

domain_var = tk.StringVar()
domain_var.set(email_domains[0])
domain_dropdown = tk.OptionMenu(frame1, domain_var, *email_domains)
domain_dropdown.config(fg="white", bg=blue1, width=15, font=('comic', 9, 'bold'))
domain_dropdown.place(x=250, y=44)

at_label = tk.Label(frame1, text="@", width=2, fg="white", bg=blue1, font=('comic', 10, 'bold'))
at_label.place(x=230, y=47)

send_email_button = tk.Button(frame1, text="Send Attendance", command=send_email_wrapper,
                              bg="#6d00fc", fg="white", font=('comic', 8, 'bold'), width=13)
send_email_button.place(x=400, y=44)

# Admin tools
# btn_del_reg = tk.Button(frame1, text="Delete Registration CSV", command=delete_registration_csv,
#                         bg="red", fg="white", font=('comic', 8, 'bold'), width=19)
# btn_del_reg.place(x=5, y=85)

# btn_del_att = tk.Button(frame1, text="Delete Attendance CSV", command=delete_attendance_today,
#                         bg="red", fg="white", font=('comic', 8, 'bold'), width=19)
# btn_del_att.place(x=320, y=85)

# btn_del_images = tk.Button(frame1, text="Delete Registered Images", command=delete_registered_images,
#                            bg="red", fg="white", font=('comic', 8, 'bold'), width=20)
# btn_del_images.place(x=320, y=115)



# Menu
menubar = tk.Menu(window)
filemenu = tk.Menu(menubar, tearoff=0)
# filemenu.add_command(label='Change Password', command=change_pass)
# filemenu.add_command(label='Exit', command=window.destroy)
#menubar.add_cascade(label='Help', menu=filemenu)
menubar.add_cascade(label=' ', menu=filemenu)
window.configure(menu=menubar)

window.mainloop()
