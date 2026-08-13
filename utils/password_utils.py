import os
import tkinter as tk
import tkinter.simpledialog as tsd
import tkinter.messagebox as mess
from utils.file_utils import assure_path_exists

def save_pass(old, new, nnew, master):
    assure_path_exists("TrainingImageLabel/")
    psd_path = "TrainingImageLabel/psd.txt"
    if os.path.isfile(psd_path):
        with open(psd_path, "r") as tf:
            key = tf.read()
    else:
        master.destroy()
        new_pas = tsd.askstring('Old Password not found', 'Please enter a new password below', show='*')
        if not new_pas:
            mess._show(title='No Password Entered', message='Password not set!! Please try again')
        else:
            with open(psd_path, "w") as tf:
                tf.write(new_pas)
            mess._show(title='Password Registered', message='New password was registered successfully!!')
        return

    op, newp, nnewp = old.get(), new.get(), nnew.get()
    if op == key:
        if newp == nnewp:
            with open(psd_path, "w") as txf:
                txf.write(newp)
            mess._show(title='Password Changed', message='Password changed successfully!!')
            master.destroy()
        else:
            mess._show(title='Error', message='Confirm new password again!!!')
    else:
        mess._show(title='Wrong Password', message='Please enter correct old password.')

def change_pass():
    master = tk.Toplevel()
    master.geometry("400x160")
    master.resizable(False, False)
    master.title("Change Password")
    master.configure(background="white")

    def save():
        save_pass(old, new, nnew, master)

    tk.Label(master, text='Enter Old Password', bg='white', font=('comic', 12, 'bold')).place(x=10, y=10)
    old = tk.Entry(master, width=25, show='*', relief='solid', font=('comic', 12, 'bold'))
    old.place(x=180, y=10)

    tk.Label(master, text='Enter New Password', bg='white', font=('comic', 12, 'bold')).place(x=10, y=45)
    new = tk.Entry(master, width=25, show='*', relief='solid', font=('comic', 12, 'bold'))
    new.place(x=180, y=45)

    tk.Label(master, text='Confirm New Password', bg='white', font=('comic', 12, 'bold')).place(x=10, y=80)
    nnew = tk.Entry(master, width=25, show='*', relief='solid', font=('comic', 12, 'bold'))
    nnew.place(x=180, y=80)

    tk.Button(master, text="Cancel", command=master.destroy, bg="red", fg="black", width=25, font=('comic', 10, 'bold')).place(x=200, y=120)
    tk.Button(master, text="Save", command=save, bg="#00fcca", fg="black", width=25, font=('comic', 10, 'bold')).place(x=10, y=120)
