import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3
from datetime import datetime

# Create a database connection
conn = sqlite3.connect('attendance_system.db')
c = conn.cursor()

# Create tables if they don't exist
c.execute('''
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY,
        name TEXT,
        age INTEGER,
        grade TEXT
    )
''')

c.execute('''
    CREATE TABLE IF NOT EXISTS attendance (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER,
        date TEXT,
        status TEXT,
        FOREIGN KEY (student_id) REFERENCES students (id)
    )
''')

conn.commit()

def add_student(student_id, name, age, grade):
    c.execute('INSERT INTO students (id, name, age, grade) VALUES (?, ?, ?, ?)', (student_id, name, age, grade))
    conn.commit()
    update_student_list()

def mark_attendance(student_id, date, status):
    c.execute('INSERT INTO attendance (student_id, date, status) VALUES (?, ?, ?)', (student_id, date, status))
    conn.commit()

def get_students():
    c.execute('SELECT * FROM students')
    return c.fetchall()

def get_attendance(student_id):
    c.execute('SELECT date, status FROM attendance WHERE student_id = ?', (student_id,))
    return c.fetchall()

def update_student_list():
    student_list.delete(*student_list.get_children())
    students = get_students()
    for student in students:
        student_list.insert("", "end", values=(student[0], student[1], student[2], student[3]))

def on_add_student():
    student_id = student_id_entry.get()
    name = student_name_entry.get()
    age = student_age_entry.get()
    grade = student_grade_entry.get()
    
    if student_id and name and age and grade:
        try:
            add_student(int(student_id), name, int(age), grade)
            student_id_entry.delete(0, tk.END)
            student_name_entry.delete(0, tk.END)
            student_age_entry.delete(0, tk.END)
            student_grade_entry.delete(0, tk.END)
        except ValueError:
            messagebox.showwarning("Input Error", "Please enter valid numeric values for ID and Age.")
    else:
        messagebox.showwarning("Input Error", "Please fill in all fields.")

def on_mark_attendance():
    student_id = attendance_id_entry.get()
    status = attendance_status_var.get()
    date = datetime.now().strftime("%Y-%m-%d")
    
    if student_id and status:
        try:
            student_id = int(student_id)
            # Check if the student exists
            c.execute('SELECT * FROM students WHERE id = ?', (student_id,))
            if c.fetchone() is None:
                messagebox.showwarning("Error", "Student ID not found.")
                return
            
            mark_attendance(student_id, date, status)
            attendance_id_entry.delete(0, tk.END)
            messagebox.showinfo("Success", f"Attendance marked for Student ID: {student_id} on {date}")
        except ValueError:
            messagebox.showwarning("Input Error", "Please enter a valid numeric student ID.")
    else:
        messagebox.showwarning("Input Error", "Please fill in all fields.")

def on_view_attendance():
    student_id = attendance_id_entry.get()
    
    if student_id:
        try:
            student_id = int(student_id)
            # Check if the student exists
            c.execute('SELECT * FROM students WHERE id = ?', (student_id,))
            if c.fetchone() is None:
                messagebox.showwarning("Error", "Student ID not found.")
                return

            records = get_attendance(student_id)
            if not records:
                messagebox.showinfo("No Records", "No attendance records found for this student.")
                return
            
            attendance_list.delete(*attendance_list.get_children())
            for record in records:
                attendance_list.insert("", "end", values=(record[0], record[1]))  # Display date and status
        except ValueError:
            messagebox.showwarning("Input Error", "Please enter a valid numeric student ID.")
    else:
        messagebox.showwarning("Input Error", "Please enter a student ID to view attendance.")

# Create main window
root = tk.Tk()
root.title("Advanced Attendance System")

# Add Student Section
add_student_frame = tk.LabelFrame(root, text="Add Student")
add_student_frame.pack(padx=10, pady=10, fill="x")

tk.Label(add_student_frame, text="ID:").grid(row=0, column=0, padx=5, pady=5)
student_id_entry = tk.Entry(add_student_frame)
student_id_entry.grid(row=0, column=1, padx=5, pady=5)

tk.Label(add_student_frame, text="Name:").grid(row=1, column=0, padx=5, pady=5)
student_name_entry = tk.Entry(add_student_frame)
student_name_entry.grid(row=1, column=1, padx=5, pady=5)

tk.Label(add_student_frame, text="Age:").grid(row=2, column=0, padx=5, pady=5)
student_age_entry = tk.Entry(add_student_frame)
student_age_entry.grid(row=2, column=1, padx=5, pady=5)

tk.Label(add_student_frame, text="Grade:").grid(row=3, column=0, padx=5, pady=5)
student_grade_entry = tk.Entry(add_student_frame)
student_grade_entry.grid(row=3, column=1, padx=5, pady=5)

tk.Button(add_student_frame, text="Add Student", command=on_add_student).grid(row=4, columnspan=2, pady=10)

# Student List
tk.Label(root, text="Student List:").pack(pady=10)
student_list = ttk.Treeview(root, columns=("ID", "Name", "Age", "Grade"), show="headings")
student_list.heading("ID", text="ID")
student_list.heading("Name", text="Name")
student_list.heading("Age", text="Age")
student_list.heading("Grade", text="Grade")
student_list.pack(padx=10, pady=10, fill="both")

update_student_list()

# Attendance Section
attendance_frame = tk.LabelFrame(root, text="Mark Attendance")
attendance_frame.pack(padx=10, pady=10, fill="x")

tk.Label(attendance_frame, text="Student ID:").grid(row=0, column=0, padx=5, pady=5)
attendance_id_entry = tk.Entry(attendance_frame)
attendance_id_entry.grid(row=0, column=1, padx=5, pady=5)

attendance_status_var = tk.StringVar()
tk.Radiobutton(attendance_frame, text="Present", variable=attendance_status_var, value="Present").grid(row=1, column=0, padx=5, pady=5)
tk.Radiobutton(attendance_frame, text="Absent", variable=attendance_status_var, value="Absent").grid(row=1, column=1, padx=5, pady=5)

tk.Button(attendance_frame, text="Mark Attendance", command=on_mark_attendance).grid(row=2, columnspan=2, pady=10)

# Attendance Record Section
tk.Label(root, text="Attendance Record:").pack(pady=10)
attendance_list = ttk.Treeview(root, columns=("Date", "Status"), show="headings")
attendance_list.heading("Date", text="Date")
attendance_list.heading("Status", text="Status")
attendance_list.pack(padx=10, pady=10, fill="both")

tk.Button(root, text="View Attendance", command=on_view_attendance).pack(pady=10)

root.mainloop()

# Close the database connection when the application exits
conn.close()
