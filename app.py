from flask import Flask, render_template, request, redirect, url_for, send_file
import sqlite3
from datetime import datetime
import csv
import os
import io

app = Flask(__name__)
DB_NAME = os.path.join(os.path.dirname(__file__), "attendance.db")

# -----------------------
# Initialize DB
# -----------------------
def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            student_id TEXT UNIQUE NOT NULL
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS attendance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER,
            event TEXT NOT NULL,
            timestamp TEXT NOT NULL,
            FOREIGN KEY(student_id) REFERENCES students(id)
        )
    """)
    conn.commit()
    conn.close()

# -----------------------
# Backup function
# -----------------------
def backup_attendance():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""
        SELECT students.name, students.student_id, attendance.event, attendance.timestamp
        FROM attendance
        JOIN students ON students.id = attendance.student_id
    """)
    records = c.fetchall()
    conn.close()
    backup_file = os.path.join(os.path.dirname(__file__), "attendance_backup.csv")
    with open(backup_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Name", "Student_ID", "Event", "Timestamp"])
        writer.writerows(records)

# -----------------------
# Jinja filters for backup info
# -----------------------
@app.template_filter('file_exists')
def file_exists_filter(filename):
    return os.path.exists(filename)

@app.template_filter('file_mtime')
def file_mtime_filter(filename):
    if os.path.exists(filename):
        return datetime.fromtimestamp(os.path.getmtime(filename)).strftime("%Y-%m-%d %H:%M:%S")
    return "N/A"

# -----------------------
# Routes
# -----------------------
@app.route("/")
def home():
    return render_template("index.html")

# Register student
@app.route("/register", methods=["GET", "POST"])
def register():
    message = ""
    if request.method == "POST":
        name = request.form["name"].strip()
        student_id = request.form["student_id"].strip()
        if name and student_id:
            conn = sqlite3.connect(DB_NAME)
            c = conn.cursor()
            try:
                c.execute("INSERT INTO students (name, student_id) VALUES (?, ?)", (name, student_id))
                conn.commit()
                message = f"Student '{name}' registered successfully!"
            except sqlite3.IntegrityError:
                message = f"Student ID '{student_id}' already exists!"
            conn.close()
    return render_template("register.html", message=message)

# Mark attendance
@app.route("/attendance", methods=["GET", "POST"])
def attendance():
    message = ""
    success = False  # <-- added flag
    if request.method == "POST":
        student_id_num = request.form["student_id"].strip()
        event = request.form["event"].strip()
        
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute("SELECT id, name FROM students WHERE student_id=?", (student_id_num,))
        student = c.fetchone()
        
        if student:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            c.execute(
                "INSERT INTO attendance (student_id, event, timestamp) VALUES (?, ?, ?)",
                (student[0], event, timestamp)
            )
            conn.commit()
            backup_attendance()
            message = f"Attendance recorded for {student[1]} in event '{event}'"
            success = True
        else:
            message = f"Student ID '{student_id_num}' not found!"
            success = False
        conn.close()
    return render_template("attendance.html", message=message, success=success)
# View records
@app.route("/records")
def records():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""
        SELECT attendance.id, students.name, students.student_id, attendance.event, attendance.timestamp
        FROM attendance
        JOIN students ON students.id = attendance.student_id
        ORDER BY attendance.timestamp DESC
    """)
    records_data = c.fetchall()
    conn.close()
    return render_template("records.html", records=records_data)
# Delete record
@app.route("/delete/<int:record_id>", methods=["POST"])
def delete_record(record_id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("DELETE FROM attendance WHERE id=?", (record_id,))
    conn.commit()
    conn.close()
    backup_attendance()
    return redirect(url_for("records"))

# Import students from CSV (FIXED)
@app.route("/import", methods=["GET", "POST"])
def import_students():
    message = ""
    if request.method == "POST":
        file = request.files.get("file")
        if file and file.filename:
            try:
                # Read the uploaded file into memory as text
                file.stream.seek(0)
                content = file.stream.read().decode('utf-8').splitlines()
                reader = csv.reader(content)
                next(reader, None)  # skip header row if present

                conn = sqlite3.connect(DB_NAME)
                c = conn.cursor()
                count = 0
                for row in reader:
                    if len(row) >= 2 and row[0].strip() and row[1].strip():
                        name, student_id = row[0].strip(), row[1].strip()
                        try:
                            c.execute(
                                "INSERT OR IGNORE INTO students (name, student_id) VALUES (?, ?)",
                                (name, student_id)
                            )
                            count += 1
                        except sqlite3.IntegrityError:
                            continue
                conn.commit()
                conn.close()
                message = f"{count} students imported successfully!"
            except Exception as e:
                message = f"Error importing CSV: {e}"
        else:
            message = "No file selected."
    return render_template("import.html", message=message)

# Export attendance
@app.route("/export")
def export_attendance():
    backup_file = os.path.join(os.path.dirname(__file__), "attendance_backup.csv")
    if not os.path.exists(backup_file):
        backup_attendance()
    return send_file(
        backup_file,
        as_attachment=True,
        download_name="attendance_backup.csv",
        mimetype="text/csv"
    )

# View all registered students
@app.route("/students")
def students():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT id, name, student_id FROM students ORDER BY name ASC")
    students_data = c.fetchall()
    conn.close()
    return render_template("students.html", students=students_data)

# Delete student
@app.route("/delete_student/<int:student_id>", methods=["POST"])
def delete_student(student_id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    # Also delete their attendance records
    c.execute("DELETE FROM attendance WHERE student_id=?", (student_id,))
    c.execute("DELETE FROM students WHERE id=?", (student_id,))
    conn.commit()
    conn.close()
    return redirect(url_for("students"))

# Delete all students
@app.route("/delete_all_students", methods=["POST"])
def delete_all_students():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("DELETE FROM attendance")  # delete all attendance first
    c.execute("DELETE FROM students")    # delete all students
    conn.commit()
    conn.close()
    return redirect(url_for("students"))


# -----------------------
# Run app
# -----------------------
if __name__ == "__main__":
    init_db()
    app.run(debug=True)



