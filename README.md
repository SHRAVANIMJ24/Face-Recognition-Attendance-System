<div align="center">

# 🎯 Face Recognition-Based Attendance Monitoring System

**A desktop attendance system that registers student faces, recognizes them live via webcam, cross-checks the class timetable, and emails subject-wise attendance reports.**

[![Python](https://img.shields.io/badge/Python-3.x-3776AB?style=flat-square&logo=python&logoColor=white)](#)
[![OpenCV](https://img.shields.io/badge/OpenCV-Haar%20Cascade%20%2B%20LBPH-5C3EE8?style=flat-square&logo=opencv&logoColor=white)](#)
[![Tkinter](https://img.shields.io/badge/GUI-Tkinter-F8DC75?style=flat-square)](#)
[![Status](https://img.shields.io/badge/status-academic%20mini--project-blue?style=flat-square)](#)

[Overview](#-overview) • [Features](#-features) • [Tech Stack](#-tech-stack) • [How It Works](#-how-it-works) • [Getting Started](#-getting-started) • [Usage](#-usage) • [Performance](#-performance) • [Security Note](#-security--privacy-note)

</div>

---

## 📖 Overview

Manual roll-call and card/biometric scanners are slow, error-prone, and not contactless. **This project automates attendance using face recognition**: a student's face is captured once during registration, and afterwards the system recognizes them in real time from a webcam feed and logs their attendance — automatically matched to whichever subject is currently scheduled, according to the class timetable.

It was built as a **Mini Project 2B (Semester VI)** for the Bachelor of Engineering in Information Technology program at **Xavier Institute of Engineering, Mumbai (University of Mumbai)**, AY 2024–25, under the guidance of **Dr. Chhaya Dhavale**.

The system runs fully offline (no server, no cloud dependency) and stores everything as local CSV files, making it lightweight enough to run on a single classroom machine with just a webcam.

## ✨ Features

- **Student registration** — enter an ID and name, capture ~100 face samples via webcam, and save a profile.
- **Real-time face recognition** — detects and identifies registered faces live from the webcam feed.
- **Timetable-aware logging** — reads `TimeTable.csv` and tags each attendance entry with the subject currently in session (or `Free Period` / `No Class`), so attendance is only meaningful when a class is actually on.
- **Duplicate prevention** — a student already marked present for the current subject/date is flagged `(Already Marked)` on-screen instead of being logged twice.
- **Subject-wise CSV logs** — a new `Attendance_<date>.csv` file is created each day, with ID, name, date, time, and subject columns.
- **Attendance reports & charts** — a report window lets you filter by student/subject/date range and view attendance as bar charts and pie charts (via `matplotlib`).
- **Email reporting** — send the day's attendance CSV as an email attachment directly from the GUI.
- **Password-protected admin actions** — a stored password gate for sensitive operations like changing the admin password (`utils/password_utils.py`).
- **Attendance simulator** — `generate_attendance.py.py` can batch-generate realistic demo attendance data from the timetable and student roster, useful for testing or presentations without a live camera.

## 🛠 Tech Stack

| Layer | Technology |
|---|---|
| GUI | Python `tkinter` (custom frames, widgets, report window) |
| Face detection | OpenCV Haar Cascade Classifier (`haarcascade_frontalface_default.xml`) |
| Face recognition | OpenCV LBPH (Local Binary Pattern Histogram) recognizer (`cv2.face.LBPHFaceRecognizer_create()`) |
| Data handling | `pandas`, `numpy`, `csv` |
| Charts | `matplotlib` |
| Date picker | `tkcalendar` |
| Email | Python `smtplib` (Gmail SMTP) |
| Storage | Flat CSV files (no database) |

## 🧠 How It Works

1. **Detection** — Haar Cascade scans each webcam frame for frontal faces (fast, lightweight, works well in normal lighting).
2. **Registration** — during "Take Images", ~100 cropped grayscale face samples are saved per student, labeled with their serial number, ID, and name.
3. **Training** — "Save Profile" trains an LBPH recognizer over all captured faces and saves the model to `TrainingImageLabel/Trainner.yml`.
4. **Recognition** — during "Take Attendance", each detected face is matched against the trained model; a confidence score below the threshold counts as a positive match.
5. **Timetable cross-check** — the current time and weekday are looked up in `TimeTable.csv` to tag the log entry with the correct subject.
6. **Logging** — a match is appended to that day's `Attendance/Attendance_<date>.csv`, skipping students already marked for that subject.

Per the project report, this achieved **~90–95% recognition accuracy** for registered students under consistent lighting, with near-instant recognition once trained (see [Performance](#-performance)).

## 📁 Project Structure

```
Face-Recognition-Attendance-System2/
├── main.py                          # App entry point — builds the GUI and wires up buttons
├── config.py                        # Reserved for shared configuration/global variables
├── facial_recognition/
│   ├── capture.py                   # TakeImages() — webcam face capture for registration
│   ├── train.py                     # TrainImages() — trains the LBPH recognizer
│   └── attendance.py                # TrackImages() — live recognition + timetable-aware logging
├── gui/
│   ├── main_window.py               # Main window, header, background, clock
│   ├── frames.py                    # Layout frames
│   ├── widgets.py                   # Labels, entries, buttons, the attendance treeview
│   └── report_window.py             # Filterable report window with bar/pie charts
├── utils/
│   ├── email_utils.py               # send_email() — emails the day's attendance CSV
│   ├── file_utils.py                # Path helpers, delete-CSV/delete-images admin helpers
│   ├── password_utils.py            # Admin password get/set/change
│   └── time_utils.py                # Clock tick + date formatting helpers
├── generate_attendance.py.py        # Standalone script to simulate/batch-generate attendance for demos
├── haarcascade_frontalface_default.xml   # Pre-trained OpenCV face-detection model
├── TimeTable.csv                    # Weekly timetable used to resolve the current subject
├── StudentDetails/StudentDetails.csv     # Registered students (serial, ID, name)
├── TrainingImage/                   # Captured face samples (generated at runtime, gitignore this)
├── TrainingImageLabel/
│   ├── Trainner.yml                 # Saved LBPH model (generated at runtime)
│   └── psd.txt                      # Stored admin password (generated at runtime)
├── Attendance/                      # One CSV per day, e.g. Attendance_20-04-2025.csv
└── LICENSE                          # MIT
```

## 🚀 Getting Started

### Prerequisites

- **Python 3.x** (project was built/tested on Python 3.12)
- A working **webcam**
- **Windows 10+ or Linux** (Tkinter needs to be available — on Linux, `sudo apt install python3-tk` if it's missing)

### Setup

1. **Clone the repo**
   ```bash
   git clone https://github.com/<your-username>/Face-Recognition-Attendance-System2.git
   cd Face-Recognition-Attendance-System2
   ```

2. **Create a virtual environment (recommended)**
   ```bash
   python -m venv venv
   source venv/bin/activate      # Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install opencv-contrib-python numpy pillow pandas matplotlib tkcalendar
   ```
   > Note: the repo's own `install commands .txt` lists a few extra packages (`tk-tools`, `python-csv`, `times`, `pytest-shutil`) that aren't actually imported anywhere in the code — the list above is the trimmed-down, working set. Use `opencv-contrib-python` specifically (not plain `opencv-python`), since the `cv2.face` module (LBPH) only ships in the contrib build.

4. **Configure email credentials as environment variables** — see the [Security Note](#-security--privacy-note) below before doing anything else with this repo.

5. **Run the app**
   ```bash
   python main.py
   ```

## 🖥 Usage

1. **Register a student** — enter an **ID** and **Name**, click **Take Images** (look at the webcam until sampling finishes), then **Save Profile** to train the recognizer.
2. **Take attendance** — click **Take Attendance**; the webcam opens, detects and labels recognized faces, and logs each match once per subject/day. Press `q` to close the camera window.
3. **View reports** — click **View Reports** to filter attendance by student, subject, or date range, and see it visualized as bar/pie charts.
4. **Email a report** — enter a recipient's email + domain and click **Send Attendance** to email the current day's CSV as an attachment.

## 📊 Performance

From testing on the project's own Third-Year Engineering batch data (see the full report for methodology):

| Metric | Observation |
|---|---|
| Face Detection Time | ~8 seconds per frame |
| Recognition Accuracy | ~90–95% for registered students |
| Training Time | ~2–3 seconds for 101 images/person |
| Recognition Time | Instantaneous (<0.5s) once trained |
| Email Delivery | Successfully sent CSV reports |

Known limitations: accuracy drops under poor lighting, occlusion (masks, angled faces), and hasn't been tested at scale beyond a single classroom-sized batch.

## 🔒 Security & Privacy Note

Before pushing this repo anywhere public, two things need attention:

1. **`utils/email_utils.py` currently hardcodes a real Gmail address and app password.** If this has already been pushed to a public (or even shared private) repo, **treat that app password as compromised — revoke/regenerate it in your Google Account's App Passwords settings right away**, regardless of whether you remove it from the code. Then refactor the credentials to be read from environment variables instead, e.g.:
   ```python
   import os
   from_email = os.environ["ATTENDANCE_EMAIL"]
   password = os.environ["ATTENDANCE_EMAIL_APP_PASSWORD"]
   ```
   and set those in your shell or a local `.env` file that's excluded via `.gitignore` — never committed.

2. **`Attendance/` and `StudentDetails/` contain real names and IDs** of classmates from testing. Add a `.gitignore` so runtime-generated, personal data doesn't ship with the source code:
   ```gitignore
   TrainingImage/
   TrainingImageLabel/
   Attendance/
   StudentDetails/
   venv/
   __pycache__/
   *.pyc
   ```

If you'd like, I can also generate the corrected `email_utils.py`, a `.gitignore`, and a `requirements.txt` for you — and if the credential's already on GitHub, walk you through scrubbing it from history (git filter-repo/BFG) on top of rotating it.

## 🔭 Future Enhancements

*(from the project report's conclusion)*

- Mask detection for post-COVID scenarios
- Move from CSV storage to a central database
- Mobile support or a web-based dashboard
- Higher-accuracy recognition via deep learning (CNN/FaceNet) for larger datasets
- Formal admin authentication for secure data access and management

## 📚 References

Built on the concepts surveyed in the project report's literature review (Haar Cascade + LBPH-based attendance systems) — full citations and research paper links are in the report's Bibliography section.

## 📄 License

MIT License. The project builds on an open-source Tkinter/OpenCV attendance-system template (original template © 2019 Shubham Kumar); the timetable integration, subject-aware logging, report/chart window, and email reporting are original to this project.
