KCP Attendance System

A fast, simple, and reliable attendance tracking system built with Flask and SQLite.

1. Features

Register students manually or import from CSV

Mark attendance for events

View attendance records

View all registered students

Delete individual students or all students

Export attendance backup as CSV

2. Directory Setup

Keep the project folder structure intact. Do not move files outside this structure, or Flask may fail to locate templates and static files:

KCP-Attendance/
├─ app.py                  # Main Flask application
├─ attendance.db           # SQLite database (created automatically)
├─ attendance_backup.csv   # Backup CSV file (generated automatically)
├─ templates/              # HTML templates
│  ├─ index.html
│  ├─ register.html
│  ├─ attendance.html
│  ├─ records.html
│  ├─ students.html
│  └─ import.html
├─ static/                 # CSS, JS, images
│  └─ style.css
└─ README.md               # Instructions file


Important: Moving files or folders may cause errors.

3. Requirements

Python 3.x

Flask

SQLite (built-in with Python)

Install Flask using pip:

pip install flask


If your environment is externally managed, use a virtual environment:

python3 -m venv venv
source venv/bin/activate
pip install flask

4. How to Run

Open a terminal inside the KCP-Attendance folder

Run the app:

python app.py


Open your browser and go to: http://127.0.0.1:5000/

5. Using the System

Register Student: Add new students manually

Mark Attendance: Enter student ID and event to record attendance

View Records: See all attendance records

View Registered Students: Search, delete individual students, or delete all

Import Students: Upload a CSV file with Name,Student_ID columns

Export Backup: Download the attendance backup CSV

6. Reset Database

Delete attendance.db to reset the database

When you rerun the app, the database will be recreated automatically

7. Notes

Keep attendance.db private; do not push it to GitHub

Use a .gitignore file to ignore sensitive files: attendance.db, attendance_backup.csv, venv/

Always keep the folder structure intact to avoid errors
