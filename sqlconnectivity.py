import tkinter as tk
from tkinter import messagebox
import mysql.connector
from datetime import date

# DB Connection
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="urpassword",
    database="GymDB"
)
cursor = conn.cursor()

# Add Member Function
def add_member():
    name = entry_name.get()
    age = entry_age.get()
    gender = entry_gender.get()
    membership = entry_membership.get()

    if name and age and gender and membership:
        query = "INSERT INTO Members (name, age, gender, membership_type, join_date) VALUES (%s, %s, %s, %s, %s)"
        values = (name, int(age), gender, membership, date.today())
        cursor.execute(query, values)
        conn.commit()
        messagebox.showinfo("Success", "Member Added Successfully!")
        clear_entries()
    else:
        messagebox.showwarning("Input Error", "Please fill all fields.")

# View Total Equipment
def show_equipment():
    cursor.callproc("TotalEquipment", [0])
    for result in cursor.stored_results():
        total = result.fetchone()[0]
        messagebox.showinfo("Total Equipment", f"Total equipment in the gym: {total}")

# View All Trainers
def show_trainers():
    cursor.callproc("ShowTrainers")
    trainers = []
    for result in cursor.stored_results():
        for row in result.fetchall():
            trainers.append(row[0])
    messagebox.showinfo("Trainers", "\n".join(trainers))

# Clear Fields
def clear_entries():
    entry_name.delete(0, tk.END)
    entry_age.delete(0, tk.END)
    entry_gender.delete(0, tk.END)
    entry_membership.delete(0, tk.END)

# Tkinter GUI
app = tk.Tk()
app.title("Gym Management System")
app.geometry("400x400")

tk.Label(app, text="Name").pack()
entry_name = tk.Entry(app)
entry_name.pack()

tk.Label(app, text="Age").pack()
entry_age = tk.Entry(app)
entry_age.pack()

tk.Label(app, text="Gender").pack()
entry_gender = tk.Entry(app)
entry_gender.pack()

tk.Label(app, text="Membership Type").pack()
entry_membership = tk.Entry(app)
entry_membership.pack()

tk.Button(app, text="Add Member", command=add_member).pack(pady=10)
tk.Button(app, text="Show Equipment Count", command=show_equipment).pack(pady=5)
tk.Button(app, text="List All Trainers", command=show_trainers).pack(pady=5)

app.mainloop()

# Close DB connection when app is closed
cursor.close()
conn.close()
