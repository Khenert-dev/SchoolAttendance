KCP Attendance System (View in code mode for better readability)

A fast, simple, and reliable attendance tracking system built with Flask and SQLite.

1. Features

✅ Register students manually or import from CSV

✅ Mark attendance for events

✅ View attendance records

✅ View all registered students

✅ Delete individual students or all students

✅ Export attendance backup as CSV

2. Directory Setup

Make sure your project folder looks like this. Do not move files outside this structure, or Flask may fail to locate templates and static files:

KCP-Attendance/
├─ app.py # Main Flask application
├─ attendance.db # SQLite database (created automatically)
├─ attendance_backup.csv # Backup CSV file (generated automatically)
├─ templates/ # HTML templates
│ ├─ index.html
│ ├─ register.html
│ ├─ attendance.html
│ ├─ records.html
│ ├─ students.html
│ └─ import.html
├─ static/ # CSS, JS, images
│ └─ style.css
└─ README.md # Instructions file

Important: If you move files or folders, Flask may not find templates or static files, causing errors.

3. How to Run

Clone or download the repository. Keep the folder structure intact.

Install Python and Flask. Make sure Python 3.x is installed. In a terminal, run:
pip install flask

Start the app. Open a terminal inside the KCP-Attendance folder and run:
python app.py
Then open your browser and go to:
http://127.0.0.1:5000/

4. Using the System

Register Student: Add new students manually.

Mark Attendance: Enter student ID and event to record attendance.

View Records: See all attendance records.

View Registered Students: Search, delete individual students, or delete all.

Import Students: Upload a CSV file with Name,Student_ID columns.

Export Backup: Download the attendance backup CSV.

5. Reset Database

To reset, delete attendance.db.

When you rerun the app, the database will be recreated automatically.

6. Notes

🔒 Keep attendance.db private; do not push it to GitHub.

Use a .gitignore file to ignore attendance.db and other sensitive files.

Always keep the folder structure intact to avoid errors.
