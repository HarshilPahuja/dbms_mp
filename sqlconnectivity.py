import tkinter as tk
from tkinter import messagebox
import mysql.connector
from datetime import date

# Database connection
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Welcome2006#",  # Replace with your MySQL password
    database="GymDB"
)
cursor = conn.cursor()

# Admin credentials
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "1234"

# Functions
def add_member():
    member_id = entry_member_id.get()
    name = entry_name.get()
    age = entry_age.get()
    gender = entry_gender.get()
    membership = entry_membership.get()

    if member_id and name and age and gender and membership:
        query = "INSERT INTO Members (member_id, name, age, gender, membership_type, join_date) VALUES (%s, %s, %s, %s, %s, %s)"
        values = (int(member_id), name, int(age), gender, membership, date.today())
        try:
            cursor.execute(query, values)
            conn.commit()
            messagebox.showinfo("Success", "Member Added Successfully!")
            clear_member_entries()
        except mysql.connector.errors.IntegrityError:
            messagebox.showerror("Error", "Member ID already exists.")
    else:
        messagebox.showwarning("Input Error", "Please fill all fields.")

def update_member():
    member_id = entry_member_id.get()
    if not member_id:
        messagebox.showwarning("Input Error", "Please enter Member ID to update.")
        return
    query = "UPDATE Members SET name=%s, age=%s, gender=%s, membership_type=%s WHERE member_id=%s"
    values = (
        entry_name.get(),
        entry_age.get(),
        entry_gender.get(),
        entry_membership.get(),
        int(member_id)
    )
    cursor.execute(query, values)
    conn.commit()
    messagebox.showinfo("Success", "Member Updated Successfully!")
    clear_member_entries()

def delete_member():
    member_id = entry_member_id.get()
    if not member_id:
        messagebox.showwarning("Input Error", "Please enter Member ID to delete.")
        return
    cursor.execute("DELETE FROM Members WHERE member_id=%s", (int(member_id),))
    conn.commit()
    messagebox.showinfo("Success", "Member Deleted Successfully!")
    clear_member_entries()

def add_equipment():
    name = entry_eq_name.get()
    qty = entry_eq_qty.get()
    if name and qty:
        query = "INSERT INTO Equipment (name, quantity, maintenance_date) VALUES (%s, %s, %s)"
        values = (name, int(qty), date.today())
        cursor.execute(query, values)
        conn.commit()
        messagebox.showinfo("Success", "Equipment Added Successfully!")
        entry_eq_name.delete(0, tk.END)
        entry_eq_qty.delete(0, tk.END)
    else:
        messagebox.showwarning("Input Error", "Fill equipment name and quantity.")

def add_trainer():
    name = entry_tr_name.get()
    specialization = entry_tr_spec.get()
    experience = entry_tr_exp.get()
    if name and specialization and experience:
        query = "INSERT INTO Trainers (name, specialization, experience) VALUES (%s, %s, %s)"
        values = (name, specialization, int(experience))
        cursor.execute(query, values)
        conn.commit()
        messagebox.showinfo("Success", "Trainer Added Successfully!")
        entry_tr_name.delete(0, tk.END)
        entry_tr_spec.delete(0, tk.END)
        entry_tr_exp.delete(0, tk.END)
    else:
        messagebox.showwarning("Input Error", "Fill all trainer fields.")

def show_equipment():
    cursor.callproc("TotalEquipment", [0])
    cursor.execute("SELECT @TotalEquipment_total AS total")
    total = cursor.fetchone()[0]
    if total is not None:
        messagebox.showinfo("Total Equipment", f"Total quantity of equipment in the gym: {total}")
    else:
        messagebox.showinfo("Total Equipment", "No equipment found.")

def show_trainers():
    cursor.callproc("ShowTrainers")
    trainers = []
    for result in cursor.stored_results():
        for row in result.fetchall():
            trainers.append(row[0])
    messagebox.showinfo("Trainers", "\n".join(trainers))

def show_experience_levels():
    query = "SELECT name, experience, ExperienceLevel(experience) AS level FROM Trainers"
    cursor.execute(query)
    rows = cursor.fetchall()
    if rows:
        info = "\n".join([f"{name} - {exp} yrs - {level}" for name, exp, level in rows])
        messagebox.showinfo("Trainer Experience Levels", info)
    else:
        messagebox.showinfo("Trainer Experience Levels", "No trainers found.")

def clear_member_entries():
    entry_member_id.delete(0, tk.END)
    entry_name.delete(0, tk.END)
    entry_age.delete(0, tk.END)
    entry_gender.delete(0, tk.END)
    entry_membership.delete(0, tk.END)

def launch_main_app():
    app = tk.Tk()
    app.title("Gym Management System")
    app.geometry("1000x650")
    app.configure(bg="#e0f7fa")

    title = tk.Label(app, text="🏋️‍♂️ Gym Management System 🏋️‍♀️", font=("Arial", 24, "bold"), bg="#006064", fg="white")
    title.pack(fill=tk.X, pady=10)

    frame = tk.Frame(app, bg="#e0f7fa")
    frame.pack(pady=10)

    # MEMBER FRAME
    member_frame = tk.LabelFrame(frame, text="Manage Members", font=("Arial", 14, "bold"), bg="#e1f5fe", padx=10, pady=10)
    member_frame.grid(row=0, column=0, padx=10)

    labels = ["Member ID", "Name", "Age", "Gender", "Membership"]
    global entry_member_id, entry_name, entry_age, entry_gender, entry_membership
    entries = []

    for i, label in enumerate(labels):
        tk.Label(member_frame, text=label, bg="#e1f5fe", anchor="w").grid(row=i, column=0, sticky="w", pady=2)
        entry = tk.Entry(member_frame)
        entry.grid(row=i, column=1, pady=2)
        entries.append(entry)

    entry_member_id, entry_name, entry_age, entry_gender, entry_membership = entries

    tk.Button(member_frame, text="Add", command=add_member, bg="#4caf50", fg="white", width=12).grid(row=5, column=0, pady=5)
    tk.Button(member_frame, text="Update", command=update_member, bg="#ff9800", fg="white", width=12).grid(row=5, column=1, pady=5)
    tk.Button(member_frame, text="Delete", command=delete_member, bg="#f44336", fg="white", width=12).grid(row=6, column=0, columnspan=2)

    # EQUIPMENT FRAME
    equipment_frame = tk.LabelFrame(frame, text="Manage Equipment", font=("Arial", 14, "bold"), bg="#e8f5e9", padx=10, pady=10)
    equipment_frame.grid(row=0, column=1, padx=10)

    global entry_eq_name, entry_eq_qty
    tk.Label(equipment_frame, text="Name", bg="#e8f5e9").grid(row=0, column=0)
    entry_eq_name = tk.Entry(equipment_frame)
    entry_eq_name.grid(row=0, column=1)

    tk.Label(equipment_frame, text="Quantity", bg="#e8f5e9").grid(row=1, column=0)
    entry_eq_qty = tk.Entry(equipment_frame)
    entry_eq_qty.grid(row=1, column=1)

    tk.Button(equipment_frame, text="Add Equipment", command=add_equipment, bg="#0277bd", fg="white", width=20).grid(row=2, column=0, columnspan=2, pady=5)
    tk.Button(equipment_frame, text="Show Equipment Count", command=show_equipment, bg="#00695c", fg="white", width=20).grid(row=3, column=0, columnspan=2)

    # TRAINER FRAME
    trainer_frame = tk.LabelFrame(frame, text="Manage Trainers", font=("Arial", 14, "bold"), bg="#f3e5f5", padx=10, pady=10)
    trainer_frame.grid(row=0, column=2, padx=10)

    global entry_tr_name, entry_tr_spec, entry_tr_exp
    tk.Label(trainer_frame, text="Name", bg="#f3e5f5").grid(row=0, column=0)
    entry_tr_name = tk.Entry(trainer_frame)
    entry_tr_name.grid(row=0, column=1)

    tk.Label(trainer_frame, text="Specialization", bg="#f3e5f5").grid(row=1, column=0)
    entry_tr_spec = tk.Entry(trainer_frame)
    entry_tr_spec.grid(row=1, column=1)

    tk.Label(trainer_frame, text="Experience (yrs)", bg="#f3e5f5").grid(row=2, column=0)
    entry_tr_exp = tk.Entry(trainer_frame)
    entry_tr_exp.grid(row=2, column=1)

    tk.Button(trainer_frame, text="Add Trainer", command=add_trainer, bg="#8e24aa", fg="white", width=20).grid(row=3, column=0, columnspan=2, pady=5)
    tk.Button(trainer_frame, text="List All Trainers", command=show_trainers, bg="#c62828", fg="white", width=20).grid(row=4, column=0, columnspan=2)
    tk.Button(trainer_frame, text="Trainer Experience Levels", command=show_experience_levels, bg="#6a1b9a", fg="white", width=20).grid(row=5, column=0, columnspan=2, pady=5)

    app.mainloop()

# LOGIN SCREEN
def login_window():
    login = tk.Tk()
    login.title("Admin Login")
    login.geometry("300x200")
    login.configure(bg="#cfd8dc")

    tk.Label(login, text="Username", bg="#cfd8dc", font=("Arial", 12)).pack(pady=5)
    username_entry = tk.Entry(login)
    username_entry.pack()

    tk.Label(login, text="Password", bg="#cfd8dc", font=("Arial", 12)).pack(pady=5)
    password_entry = tk.Entry(login, show="*")
    password_entry.pack()

    def check_login():
        username = username_entry.get()
        password = password_entry.get()
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            login.destroy()
            launch_main_app()
        else:
            messagebox.showerror("Login Failed", "Invalid credentials")

    tk.Button(login, text="Login", command=check_login, bg="#37474f", fg="white", width=15).pack(pady=15)
    login.mainloop()

# Start the login process
login_window()

cursor.close()
conn.close()
