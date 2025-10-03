'''import tkinter as tk
from tkinter import messagebox
import random
import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Dasvignesh@123",  
    database="student_db",
    auth_plugin='mysql_native_password'
)
cursor = db.cursor()

BG_COLOR = "#0F2027"
FRAME_COLOR = "#1F3C88"
TITLE_BG = "#203A43"
TEXT_COLOR = "#F0F8FF"
BUTTON_BG = "#FF6F61"
BUTTON_FG = "#FFFFFF"
CAPTCHA_BG = "#FFEB3B"
CAPTCHA_FG = "#000000"

class StudentResultApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Result App")
        self.root.geometry("550x700")
        self.root.config(bg=BG_COLOR)

        self.roll_var = tk.StringVar()
        self.captcha_var = tk.StringVar()
        self.captcha_input = tk.StringVar()

        self.create_login_page()

    def create_login_page(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        title = tk.Label(self.root, text="Student Login",
                         font=("Segoe UI", 22, "bold"),
                         bg=TITLE_BG, fg=TEXT_COLOR, pady=15)
        title.pack(fill="x")

        frame = tk.Frame(self.root, bg=FRAME_COLOR, bd=2, relief="ridge")
        frame.pack(pady=40, padx=30)

        tk.Label(frame, text="Roll Number:", font=("Segoe UI", 14, "bold"),
                 bg=FRAME_COLOR, fg=TEXT_COLOR).grid(row=0, column=0, pady=10, sticky="w")
        tk.Entry(frame, textvariable=self.roll_var, font=("Segoe UI", 14),
                 width=20).grid(row=0, column=1, pady=10)

        self.captcha_var.set(self.generate_captcha())
        tk.Label(frame, text="Captcha:", font=("Segoe UI", 14, "bold"),
                 bg=FRAME_COLOR, fg=TEXT_COLOR).grid(row=1, column=0, pady=10, sticky="w")

        captcha_frame = tk.Frame(frame, bg=FRAME_COLOR)
        captcha_frame.grid(row=1, column=1, pady=10, sticky="w")

        self.captcha_label = tk.Label(captcha_frame, textvariable=self.captcha_var,
                                      font=("Segoe UI", 16, "bold"),
                                      bg=CAPTCHA_BG, fg=CAPTCHA_FG, width=8)
        self.captcha_label.pack(side="left")

        tk.Button(captcha_frame, text="🔄", command=self.refresh_captcha,
                  font=("Segoe UI", 12, "bold"), bg=BUTTON_BG, fg=BUTTON_FG,
                  width=3).pack(side="left", padx=5)

        tk.Entry(frame, textvariable=self.captcha_input, font=("Segoe UI", 14),
                 width=20).grid(row=2, column=1, pady=10)

        tk.Button(self.root, text="Login", command=self.verify_login,
                  font=("Segoe UI", 14, "bold"), bg=BUTTON_BG, fg=BUTTON_FG,
                  width=12, bd=3, relief="raised").pack(pady=10)

        tk.Button(self.root, text="Register", command=self.show_register_page,
                  font=("Segoe UI", 14, "bold"), bg="#9B59B6", fg=BUTTON_FG,
                  width=12, bd=3, relief="raised").pack(pady=5)

    def generate_captcha(self):
        return str(random.randint(1000, 9999))

    def refresh_captcha(self):
        self.captcha_var.set(self.generate_captcha())


    def verify_login(self):
        roll = self.roll_var.get().strip()
        captcha = self.captcha_input.get().strip()

        if roll == "" or captcha == "":
            messagebox.showerror("Error", "Please enter Roll Number and Captcha")
            return

        if captcha != self.captcha_var.get():
            messagebox.showerror("Error", "Invalid Captcha")
            self.refresh_captcha()
            self.captcha_input.set("")
            return

        cursor.execute("SELECT * FROM students WHERE roll=%s", (roll,))
        student = cursor.fetchone()

        if student:
            self.show_result_page(student)
        else:
            messagebox.showerror("Error", "Roll Number not found")
            self.roll_var.set("")
            self.refresh_captcha()
            self.captcha_input.set("")

    def show_register_page(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        title = tk.Label(self.root, text="Student Registration",
                         font=("Segoe UI", 22, "bold"),
                         bg="#9B59B6", fg=TEXT_COLOR, pady=15)
        title.pack(fill="x")

        frame = tk.Frame(self.root, bg=FRAME_COLOR, bd=2, relief="ridge")
        frame.pack(pady=20, padx=30)

        self.reg_roll = tk.StringVar()
        self.reg_name = tk.StringVar()
        self.reg_tamil = tk.IntVar()
        self.reg_english = tk.IntVar()
        self.reg_maths = tk.IntVar()
        self.reg_science = tk.IntVar()
        self.reg_social = tk.IntVar()

        self.total_var = tk.IntVar()
        self.percentage_var = tk.StringVar()
        self.grade_var = tk.StringVar()

        fields = [
            ("Roll No", self.reg_roll),
            ("Name", self.reg_name),
            ("Tamil", self.reg_tamil),
            ("English", self.reg_english),
            ("Maths", self.reg_maths),
            ("Science", self.reg_science),
            ("Social", self.reg_social),
        ]

        for i, (label, var) in enumerate(fields):
            tk.Label(frame, text=f"{label}:", font=("Segoe UI", 14, "bold"),
                     bg=FRAME_COLOR, fg=TEXT_COLOR).grid(row=i, column=0, pady=5, sticky="w")
            tk.Entry(frame, textvariable=var, font=("Segoe UI", 14),
                     width=20).grid(row=i, column=1, pady=5)

        # Dynamic result labels
        tk.Label(frame, text="Total:", font=("Segoe UI", 14, "bold"),
                 bg=FRAME_COLOR, fg=TEXT_COLOR).grid(row=7, column=0, pady=5, sticky="w")
        tk.Label(frame, textvariable=self.total_var, font=("Segoe UI", 14),
                 bg="#34495E", fg=CAPTCHA_BG, width=15).grid(row=7, column=1, pady=5)

        tk.Label(frame, text="Percentage:", font=("Segoe UI", 14, "bold"),
                 bg=FRAME_COLOR, fg=TEXT_COLOR).grid(row=8, column=0, pady=5, sticky="w")
        tk.Label(frame, textvariable=self.percentage_var, font=("Segoe UI", 14),
                 bg="#34495E", fg=CAPTCHA_BG, width=15).grid(row=8, column=1, pady=5)

        tk.Label(frame, text="Grade:", font=("Segoe UI", 14, "bold"),
                 bg=FRAME_COLOR, fg=TEXT_COLOR).grid(row=9, column=0, pady=5, sticky="w")
        tk.Label(frame, textvariable=self.grade_var, font=("Segoe UI", 14),
                 bg="#34495E", fg=CAPTCHA_BG, width=15).grid(row=9, column=1, pady=5)

        # Trace changes to update dynamic result
        self.reg_tamil.trace("w", self.update_result)
        self.reg_english.trace("w", self.update_result)
        self.reg_maths.trace("w", self.update_result)
        self.reg_science.trace("w", self.update_result)
        self.reg_social.trace("w", self.update_result)

        tk.Button(self.root, text="Submit", command=self.register_student,
                  font=("Segoe UI", 14, "bold"), bg=BUTTON_BG, fg=BUTTON_FG,
                  width=12, bd=3, relief="raised").pack(pady=10)

        tk.Button(self.root, text="Back", command=self.create_login_page,
                  font=("Segoe UI", 12, "bold"), bg="#E74C3C", fg=BUTTON_FG,
                  width=10, bd=3, relief="raised").pack()

    def update_result(self, *args):
        try:
            tamil = self.reg_tamil.get()
            english = self.reg_english.get()
            maths = self.reg_maths.get()
            science = self.reg_science.get()
            social = self.reg_social.get()

            total = tamil + english + maths + science + social
            percentage = total / 5

            if percentage >= 90:
                grade = "A+"
            elif percentage >= 75:
                grade = "A"
            elif percentage >= 60:
                grade = "B"
            elif percentage >= 40:
                grade = "C"
            else:
                grade = "Fail"

            self.total_var.set(total)
            self.percentage_var.set(f"{percentage:.2f}%")
            self.grade_var.set(grade)
        except:
            self.total_var.set(0)
            self.percentage_var.set("0%")
            self.grade_var.set("N/A")

    def register_student(self):
        roll = self.reg_roll.get().strip()
        name = self.reg_name.get().strip()
        tamil = self.reg_tamil.get()
        english = self.reg_english.get()
        maths = self.reg_maths.get()
        science = self.reg_science.get()
        social = self.reg_social.get()

        if roll == "" or name == "":
            messagebox.showerror("Error", "Roll No and Name are required")
            return

        cursor.execute("SELECT * FROM students WHERE roll=%s", (roll,))
        if cursor.fetchone():
            messagebox.showerror("Error", "Roll Number already exists ❌")
            return

        cursor.execute("""
            INSERT INTO students (roll, name, tamil, english, maths, science, social)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (roll, name, tamil, english, maths, science, social))
        db.commit()

        messagebox.showinfo("Success", f"Student {name} registered successfully ✅")
        self.create_login_page()

    def show_result_page(self, student):
        for widget in self.root.winfo_children():
            widget.destroy()

        roll, name, tamil, english, maths, science, social = student
        total = tamil + english + maths + science + social
        percentage = total / 5

        if percentage >= 90:
            grade = "A+"
        elif percentage >= 75:
            grade = "A"
        elif percentage >= 60:
            grade = "B"
        elif percentage >= 40:
            grade = "C"
        else:
            grade = "Fail"

        title = tk.Label(self.root, text="Student Result",
                         font=("Segoe UI", 22, "bold"),
                         bg=TITLE_BG, fg=TEXT_COLOR, pady=15)
        title.pack(fill="x")

        labels = ["Roll No", "Name", "Tamil", "English", "Maths",
                  "Science", "Social", "Total", "Percentage", "Grade"]
        values = [roll, name, tamil, english, maths, science, social,
                  total, f"{percentage:.2f}%", grade]

        frame = tk.Frame(self.root, bg=FRAME_COLOR, bd=2, relief="ridge")
        frame.pack(pady=20, padx=30)

        for i, (label, value) in enumerate(zip(labels, values)):
            tk.Label(frame, text=f"{label}:", font=("Segoe UI", 14, "bold"),
                     bg=FRAME_COLOR, fg=TEXT_COLOR, anchor="w", width=12).grid(row=i, column=0, pady=5, sticky="w")
            tk.Label(frame, text=value, font=("Segoe UI", 14),
                     bg="#34495E", fg=CAPTCHA_BG, width=15).grid(row=i, column=1, pady=5)

        tk.Button(self.root, text="Back", command=self.create_login_page,
                  font=("Segoe UI", 12, "bold"), bg="#E74C3C", fg=BUTTON_FG,
                  width=10, bd=3, relief="raised").pack(pady=10)
root = tk.Tk()
app = StudentResultApp(root)
root.mainloop()
'''
import tkinter as tk
from tkinter import messagebox
import mysql.connector
import random

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Dasvignesh@123", 
    database="student_db",
    auth_plugin='mysql_native_password'
)
cursor = db.cursor()

BG_COLOR = "#F4F6F7"
FRAME_COLOR = "#FFFFFF"
TITLE_BG = "#2C3E50"
TITLE_FG = "#ECF0F1"
TEXT_COLOR = "#2C3E50"
BUTTON_BG = "#3498DB"
BUTTON_FG = "#FFFFFF"
BUTTON_HOVER = "#2980B9"
CAPTCHA_FG = "#2C3E50"

class StudentResultApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Result App")
        self.root.geometry("650x750")
        self.root.config(bg=BG_COLOR)

        # Vars
        self.roll_var = tk.StringVar()
        self.captcha_var = tk.StringVar()
        self.captcha_input = tk.StringVar()

        self.create_main_page()

    def create_main_page(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        title = tk.Label(self.root, text=" Student Result Management System",
                         font=("Segoe UI", 22, "bold"),
                         bg=TITLE_BG, fg=TITLE_FG, pady=20)
        title.pack(fill="x", pady=20)

        tk.Button(self.root, text="Student Login", command=self.create_student_login,
                  font=("Segoe UI", 16, "bold"), bg=BUTTON_BG, fg=BUTTON_FG,
                  activebackground=BUTTON_HOVER, relief="flat", width=18, height=2).pack(pady=30)

        tk.Button(self.root, text="Admin Login", command=self.create_admin_login,
                  font=("Segoe UI", 16, "bold"), bg="#27AE60", fg=BUTTON_FG,
                  activebackground="#1E8449", relief="flat", width=18, height=2).pack(pady=10)

    def create_student_login(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        title = tk.Label(self.root, text="Student Login",
                         font=("Segoe UI", 20, "bold"),
                         bg=TITLE_BG, fg=TITLE_FG, pady=15)
        title.pack(fill="x")

        frame = tk.Frame(self.root, bg=FRAME_COLOR, bd=1, relief="solid")
        frame.pack(pady=40, padx=40, ipadx=20, ipady=20)

        tk.Label(frame, text="Roll Number:", font=("Segoe UI", 14),
                 bg=FRAME_COLOR, fg=TEXT_COLOR).grid(row=0, column=0, pady=10, sticky="w")
        tk.Entry(frame, textvariable=self.roll_var, font=("Segoe UI", 14),
                 width=22, bd=1, relief="solid").grid(row=0, column=1, pady=10)

        # Captcha
        self.captcha_var.set(self.generate_captcha())
        tk.Label(frame, text="Captcha:", font=("Segoe UI", 14),
                 bg=FRAME_COLOR, fg=TEXT_COLOR).grid(row=1, column=0, pady=10, sticky="w")

        captcha_frame = tk.Frame(frame, bg=FRAME_COLOR)
        captcha_frame.grid(row=1, column=1, pady=10, sticky="w")

        self.captcha_label = tk.Label(captcha_frame, textvariable=self.captcha_var,
                                      font=("Segoe UI", 16, "bold"),
                                      bg=self.random_captcha_bg(), fg=CAPTCHA_FG,
                                      width=8, bd=1, relief="solid")
        self.captcha_label.pack(side="left")

        tk.Button(captcha_frame, text="🔄", command=self.refresh_captcha,
                  font=("Segoe UI", 12, "bold"), bg=BUTTON_BG, fg=BUTTON_FG,
                  relief="flat", width=3).pack(side="left", padx=5)

        tk.Entry(frame, textvariable=self.captcha_input, font=("Segoe UI", 14),
                 width=22, bd=1, relief="solid").grid(row=2, column=1, pady=10)

        tk.Button(self.root, text="Login", command=self.verify_student_login,
                  font=("Segoe UI", 14, "bold"), bg=BUTTON_BG, fg=BUTTON_FG,
                  relief="flat", width=15, height=2).pack(pady=20)

        tk.Button(self.root, text="⬅ Back", command=self.create_main_page,
                  font=("Segoe UI", 12, "bold"), bg="#E74C3C", fg=BUTTON_FG,
                  relief="flat", width=10).pack(pady=10)

    def create_admin_login(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        title = tk.Label(self.root, text="Admin Login",
                         font=("Segoe UI", 20, "bold"),
                         bg=TITLE_BG, fg=TITLE_FG, pady=15)
        title.pack(fill="x")

        frame = tk.Frame(self.root, bg=FRAME_COLOR, bd=1, relief="solid")
        frame.pack(pady=40, padx=40, ipadx=20, ipady=20)

        self.admin_user = tk.StringVar()
        self.admin_pass = tk.StringVar()
        self.captcha_input.set("")

        tk.Label(frame, text="Username:", font=("Segoe UI", 14),
                 bg=FRAME_COLOR, fg=TEXT_COLOR).grid(row=0, column=0, pady=10, sticky="w")
        tk.Entry(frame, textvariable=self.admin_user, font=("Segoe UI", 14),
                 width=22, bd=1, relief="solid").grid(row=0, column=1, pady=10)

        tk.Label(frame, text="Password:", font=("Segoe UI", 14),
                 bg=FRAME_COLOR, fg=TEXT_COLOR).grid(row=1, column=0, pady=10, sticky="w")
        tk.Entry(frame, textvariable=self.admin_pass, font=("Segoe UI", 14),
                 width=22, show="*", bd=1, relief="solid").grid(row=1, column=1, pady=10)

        # Captcha
        self.captcha_var.set(self.generate_captcha())
        tk.Label(frame, text="Captcha:", font=("Segoe UI", 14),
                 bg=FRAME_COLOR, fg=TEXT_COLOR).grid(row=2, column=0, pady=10, sticky="w")

        captcha_frame = tk.Frame(frame, bg=FRAME_COLOR)
        captcha_frame.grid(row=2, column=1, pady=10, sticky="w")

        self.captcha_label = tk.Label(captcha_frame, textvariable=self.captcha_var,
                                      font=("Segoe UI", 16, "bold"),
                                      bg=self.random_captcha_bg(), fg=CAPTCHA_FG,
                                      width=8, bd=1, relief="solid")
        self.captcha_label.pack(side="left")

        tk.Button(captcha_frame, text="🔄", command=self.refresh_captcha,
                  font=("Segoe UI", 12, "bold"), bg=BUTTON_BG, fg=BUTTON_FG,
                  relief="flat", width=3).pack(side="left", padx=5)

        tk.Entry(frame, textvariable=self.captcha_input, font=("Segoe UI", 14),
                 width=22, bd=1, relief="solid").grid(row=3, column=1, pady=10)

        tk.Button(self.root, text="Login", command=self.verify_admin_login,
                  font=("Segoe UI", 14, "bold"), bg="#27AE60", fg=BUTTON_FG,
                  relief="flat", width=15, height=2).pack(pady=20)

        tk.Button(self.root, text="⬅ Back", command=self.create_main_page,
                  font=("Segoe UI", 12, "bold"), bg="#E74C3C", fg=BUTTON_FG,
                  relief="flat", width=10).pack(pady=10)

    def generate_captcha(self):
        return ''.join(random.choices("ABCDEFGHJKLMNPQRSTUVWXYZ23456789", k=6))

    def random_captcha_bg(self):
        return random.choice(["#FAD7A0", "#A9DFBF", "#AED6F1", "#F5B7B1", "#D7BDE2"])

    def refresh_captcha(self):
        self.captcha_var.set(self.generate_captcha())
        self.captcha_label.config(bg=self.random_captcha_bg())

    def verify_admin_login(self):
        if self.admin_user.get() == "admin" and self.admin_pass.get() == "admin123":
            self.create_admin_panel()
        else:
            messagebox.showerror("Error", "Invalid Admin Credentials ")

    def create_admin_panel(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        title = tk.Label(self.root, text="➕ Register Student Marks",
                         font=("Segoe UI", 20, "bold"),
                         bg=TITLE_BG, fg=TITLE_FG, pady=15)
        title.pack(fill="x")

        frame = tk.Frame(self.root, bg=FRAME_COLOR, bd=2, relief="solid")
        frame.pack(pady=20, padx=40, ipadx=20, ipady=20)

        self.new_roll = tk.StringVar()
        self.new_name = tk.StringVar()
        self.marks = {sub: tk.StringVar() for sub in ["Tamil","English","Maths","Science","Social"]}

        tk.Label(frame, text="Roll No:", font=("Segoe UI", 14), bg=FRAME_COLOR).grid(row=0, column=0, pady=5, sticky="w")
        tk.Entry(frame, textvariable=self.new_roll, font=("Segoe UI", 14)).grid(row=0, column=1, pady=5)

        tk.Label(frame, text="Name:", font=("Segoe UI", 14), bg=FRAME_COLOR).grid(row=1, column=0, pady=5, sticky="w")
        tk.Entry(frame, textvariable=self.new_name, font=("Segoe UI", 14)).grid(row=1, column=1, pady=5)

        i=2
        for sub, var in self.marks.items():
            tk.Label(frame, text=f"{sub}:", font=("Segoe UI", 14), bg=FRAME_COLOR).grid(row=i, column=0, pady=5, sticky="w")
            tk.Entry(frame, textvariable=var, font=("Segoe UI", 14)).grid(row=i, column=1, pady=5)
            i+=1

        tk.Button(self.root, text="Save Student", command=self.save_student,
                  font=("Segoe UI", 14, "bold"), bg=BUTTON_BG, fg=BUTTON_FG,
                  relief="flat", width=15, height=2).pack(pady=20)

        tk.Button(self.root, text="⬅ Back", command=self.create_main_page,
                  font=("Segoe UI", 12, "bold"), bg="#E74C3C", fg=BUTTON_FG,
                  relief="flat", width=10).pack(pady=10)

    def save_student(self):
        try:
            data = (self.new_roll.get(), self.new_name.get(),
                    int(self.marks["Tamil"].get()),
                    int(self.marks["English"].get()),
                    int(self.marks["Maths"].get()),
                    int(self.marks["Science"].get()),
                    int(self.marks["Social"].get()))
            cursor.execute("INSERT INTO students VALUES (%s,%s,%s,%s,%s,%s,%s)", data)
            db.commit()
            messagebox.showinfo("Success", "Student record added ✅")
        except Exception as e:
            messagebox.showerror("Error", f"Could not save: {e}")

    def verify_student_login(self):
        roll = self.roll_var.get().strip()
        captcha = self.captcha_input.get().strip()

        if roll == "" or captcha == "":
            messagebox.showerror("Error", "All fields required ")
            return

        if captcha != self.captcha_var.get():
            messagebox.showerror("Error", "Invalid Captcha ")
            self.refresh_captcha()
            self.captcha_input.set("")
            return

        cursor.execute("SELECT * FROM students WHERE roll=%s", (roll,))
        student = cursor.fetchone()

        if student:
            self.show_result_page(student)
        else:
            messagebox.showerror("Error", "Roll Number not found ❌")

    def show_result_page(self, student):
        for widget in self.root.winfo_children():
            widget.destroy()

        roll, name, tamil, english, maths, science, social = student
        total = tamil + english + maths + science + social
        percentage = total / 5

        if percentage >= 90:
            grade = "A+"
        elif percentage >= 75:
            grade = "A"
        elif percentage >= 60:
            grade = "B"
        elif percentage >= 40:
            grade = "C"
        else:
            grade = "Fail"

        title = tk.Label(self.root, text="📄 Student Result",
                         font=("Segoe UI", 22, "bold"),
                         bg=TITLE_BG, fg=TITLE_FG, pady=15)
        title.pack(fill="x")

        labels = ["Roll No", "Name", "Tamil", "English", "Maths",
                  "Science", "Social", "Total", "Percentage", "Grade"]
        values = [roll, name, tamil, english, maths, science, social,
                  total, f"{percentage:.2f}%", grade]

        frame = tk.Frame(self.root, bg=FRAME_COLOR, bd=2, relief="solid")
        frame.pack(pady=20, padx=40, ipadx=20, ipady=20)

        for i, (label, value) in enumerate(zip(labels, values)):
            tk.Label(frame, text=f"{label}:", font=("Segoe UI", 14, "bold"),
                     bg=FRAME_COLOR, fg=TEXT_COLOR, anchor="w", width=12).grid(row=i, column=0, pady=5, sticky="w")
            tk.Label(frame, text=value, font=("Segoe UI", 14),
                     bg="#ECF0F1", fg="#000000", width=15, anchor="w").grid(row=i, column=1, pady=5)

        tk.Button(self.root, text="⬅ Back", command=self.create_student_login,
                  font=("Segoe UI", 12, "bold"), bg="#E74C3C", fg=BUTTON_FG,
                  relief="flat", width=10).pack(pady=20)

# Run app
root = tk.Tk()
app = StudentResultApp(root)
root.mainloop()
