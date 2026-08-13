import os
import csv
import time
import cv2
import pandas as pd
from datetime import datetime
import tkinter.messagebox as mess

def get_current_subject_from_csv():
    now = datetime.now()
    current_day = now.strftime('%A')
    try:
        df = pd.read_csv("TimeTable.csv")
        for _, row in df.iterrows():
            start_time = datetime.strptime(row['TimeFrom'], '%H:%M').time()
            end_time = datetime.strptime(row['TimeTo'], '%H:%M').time()
            if start_time <= now.time() < end_time:
                subject = row.get(current_day)
                return subject if pd.notna(subject) else "Free Period"
        return "No Class"
    except Exception as e:
        print("Error reading timetable:", e)
        return None

def TrackImages(tv, message, window):
    if not os.path.isfile("TrainingImageLabel/Trainner.yml"):
        mess._show(title='Data Missing', message='Please click on Save Profile to reset data!!')
        return

    for k in tv.get_children():
        tv.delete(k)

    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read("TrainingImageLabel/Trainner.yml")
    faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
    cam = cv2.VideoCapture(0)
    font = cv2.FONT_HERSHEY_SIMPLEX
    df = pd.read_csv("StudentDetails/StudentDetails.csv")

    subject = get_current_subject_from_csv()
    current_date = datetime.now().strftime('%d-%m-%Y')
    file_path = f"Attendance/Attendance_{current_date}.csv"
    write_header = not os.path.exists(file_path)

    existing_records = set()
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                if len(row) >= 9:
                    existing_records.add((row[0], row[4], row[8]))

    attendance_data = []
    while True:
        ret, im = cam.read()
        gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(gray, 1.2, 5)

        for (x, y, w, h) in faces:
            cv2.rectangle(im, (x, y), (x + w, y + h), (225, 0, 0), 2)
            serial, conf = recognizer.predict(gray[y:y + h, x:x + w])
            if conf < 50:
                name = df.loc[df['SERIAL NO.'] == serial]['NAME'].values
                ID = df.loc[df['SERIAL NO.'] == serial]['ID'].values
                ID, name = str(ID)[1:-1], str(name)[2:-2]
                timeStamp = datetime.now().strftime('%I:%M:%S %p')

                if (ID, current_date, subject) not in existing_records:
                    row = [str(ID), '', name, '', current_date, '', timeStamp, '', subject]
                    attendance_data.append(row)
                    existing_records.add((ID, current_date, subject))
                    cv2.putText(im, name, (x, y + h), font, 1, (255, 255, 255), 2)
                else:
                    cv2.putText(im, f"{name} (Already Marked)", (x, y + h), font, 0.6, (0, 0, 255), 2)
            else:
                cv2.putText(im, "Unknown", (x, y + h), font, 1, (255, 255, 255), 2)

        cv2.imshow('Taking Attendance', im)
        if cv2.waitKey(1) == ord('q'):
            break

    with open(file_path, 'a+', newline='') as f:
        writer = csv.writer(f)
        if write_header:
            writer.writerow(['Id', '', 'Name', '', 'Date', '', 'Time', '', 'Subject'])
        for row in attendance_data:
            writer.writerow(row)

    for row in attendance_data:
        tv.insert('', 0, text=row[0], values=(row[2], row[4], row[6], row[8]))

    cam.release()
    cv2.destroyAllWindows()
