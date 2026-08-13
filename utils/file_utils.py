import os
import shutil
import tkinter.messagebox as mess

def assure_path_exists(path):
    dir = os.path.dirname(path)
    if not os.path.exists(dir):
        os.makedirs(dir)

def delete_registration_csv():
    registration_csv_path = "StudentDetails/StudentDetails.csv"
    if os.path.exists(registration_csv_path):
        os.remove(registration_csv_path)
        mess.showinfo("Success", "Registration CSV file deleted successfully.")
    else:
        mess.showinfo("Error", "Registration CSV file not found.")

def delete_attendance_csv(date):
    attendance_csv_path = f"Attendance/Attendance_{date}.csv"
    if os.path.exists(attendance_csv_path):
        os.remove(attendance_csv_path)
        mess.showinfo("Success", f"Attendance CSV file for {date} deleted successfully.")
    else:
        mess.showinfo("Error", f"Attendance CSV file for {date} not found.")

def delete_registered_images():
    folder_path = "TrainingImage/"
    if os.path.exists(folder_path):
        for file in os.listdir(folder_path):
            try:
                os.remove(os.path.join(folder_path, file))
            except Exception as e:
                mess.showinfo("Error", f"Failed to delete {file}: {e}")
        mess.showinfo("Success", "Registered images deleted successfully.")
    else:
        mess.showinfo("Error", "TrainingImage folder not found.")
