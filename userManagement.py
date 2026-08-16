import tkinter as tk
from tkinter import ttk, messagebox
import pymysql
from db_config import DB_USER, DB_PASSWORD
from auth_utils import hash_password
from nav_utils import go_to
windows = tk.Tk()
windows.title("Library Management System - User Management")
#windows.geometry("800x600")
windows.config(bg='#438c9c')

db = pymysql.connect(host='localhost', user=DB_USER, password=DB_PASSWORD, database='libraryManagementSystem')
cursor = db.cursor()

#get all users from the db
def fetch_users():
    cursor.execute("SELECT * FROM users")
    rows = cursor.fetchall()
#itorating the data
    for row in rows:
        tree.insert("", tk.END, values=row)

#add a user to the db
def add_user():
    firstname = entry_firstname.get()
    lastname = entry_lastname.get()
    email = entry_email.get()
    gender = entry_gender.get()
    position = entry_position.get()
    username = entry_username.get()
    password = entry_password.get()
    confirmpassword = entry_confirmpassword.get()

    if all([firstname, lastname, email, gender, position, username, password, confirmpassword]):
        if password == confirmpassword:
            hashed = hash_password(password)
            cursor.execute("INSERT INTO users (firstname, lastname, email, gender, position, username, passwrd, confirmpasswrd) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                           (firstname, lastname, email, gender, position, username, hashed, hashed))
            db.commit()
            messagebox.showinfo("Success", "User added successfully!")
            clear_fields()
            refresh_table()
        else:
            messagebox.showerror("Error", "Passwords do not match")
    else:
        messagebox.showwarning("Input Error", "Please fill all fields")

#update the selected user in the db
def update_user():
    selected_item = tree.selection()
    if selected_item:
#Get values to selected items
        selected_user = tree.item(selected_item)['values']
        user_id = selected_user[0]
        firstname = entry_firstname.get()
        lastname = entry_lastname.get()
        email = entry_email.get()
        gender = entry_gender.get()
        position = entry_position.get()
        username = entry_username.get()
        password = entry_password.get()
        confirmpassword = entry_confirmpassword.get()

        if all([firstname, lastname, email, gender, position, username, password, confirmpassword]):
            if password == confirmpassword:
                hashed = hash_password(password)
                cursor.execute("UPDATE users SET firstname=%s, lastname=%s, email=%s, gender=%s, position=%s, username=%s, passwrd=%s, confirmpasswrd=%s WHERE id=%s",
                               (firstname, lastname, email, gender, position, username, hashed, hashed, user_id))
                db.commit()
                messagebox.showinfo("Success", "User updated successfully!")
                clear_fields()
                refresh_table()
            else:
                messagebox.showerror("Error", "Passwords do not match")
        else:
            messagebox.showwarning("Input Error", "Please fill all fields")
    else:
        messagebox.showwarning("Selection Error", "Please select a user to update")

#delete selected user from the db with confirmation
def delete_user():
    selected_item = tree.selection()
    if selected_item:
        selected_user = tree.item(selected_item)['values']
        user_id = selected_user[0]
        confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete the user {selected_user[1]}?")
        if confirm:
            cursor.execute("DELETE FROM users WHERE id=%s", (user_id,))
            db.commit()
            messagebox.showinfo("Success", "User deleted successfully!")
            clear_fields()
            refresh_table()
    else:
        messagebox.showwarning("Selection Error", "Please select a user to delete")

#load selected user data into entry fields for update
def load_user_data(event):
    selected_item = tree.selection()
    if selected_item:
        selected_user = tree.item(selected_item)['values']
        entry_firstname.delete(0, tk.END)
        entry_firstname.insert(tk.END, selected_user[1])
        entry_lastname.delete(0, tk.END)
        entry_lastname.insert(tk.END, selected_user[2])
        entry_email.delete(0, tk.END)
        entry_email.insert(tk.END, selected_user[3])
        entry_gender.delete(0, tk.END)
        entry_gender.insert(tk.END, selected_user[4])
        entry_position.delete(0, tk.END)
        entry_position.insert(tk.END, selected_user[5])
        entry_username.delete(0, tk.END)
        entry_username.insert(tk.END, selected_user[6])

# Clear entry fields
def clear_fields():
    entry_firstname.delete(0, tk.END)
    entry_lastname.delete(0, tk.END)
    entry_email.delete(0, tk.END)
    entry_gender.delete(0, tk.END)
    entry_position.delete(0, tk.END)
    entry_username.delete(0, tk.END)
    entry_password.delete(0, tk.END)
    entry_confirmpassword.delete(0, tk.END)

# Refresh table
def refresh_table():
    tree.delete(*tree.get_children())
    fetch_users()

def back_to_dashboard():
    windows.destroy()
    go_to('dashboard')
# Heading for the window
label_heading = tk.Label(windows, text="User Management", bg='#438c9c', font=("Microsoft YaHei UI Light", 16, "bold"))
label_heading.pack(pady=0)

#Table (Tree) to display users
tree = ttk.Treeview(windows, columns=("ID", "First Name", "Last Name", "Email", "Gender", "Position", "Username"), show="headings", height=8)
tree.heading("ID", text="ID")
tree.heading("First Name", text="First Name")
tree.heading("Last Name", text="Last Name")
tree.heading("Email", text="Email")
tree.heading("Gender", text="Gender")
tree.heading("Position", text="Position")
tree.heading("Username", text="Username")
tree.pack(pady=10)

# Bind the row selection event to load user data into entry fields
tree.bind("<ButtonRelease-1>", load_user_data)

# Labels and entry fields for user details
label_firstname = tk.Label(windows, text="First Name", bg='#438c9c')
label_firstname.pack(pady=5)
entry_firstname = tk.Entry(windows)
entry_firstname.pack(pady=5)

label_lastname = tk.Label(windows, text="Last Name", bg='#438c9c')
label_lastname.pack(pady=5)
entry_lastname = tk.Entry(windows)
entry_lastname.pack(pady=5)

label_email = tk.Label(windows, text="Email", bg='#438c9c')
label_email.pack(pady=5)
entry_email = tk.Entry(windows)
entry_email.pack(pady=5)

label_gender = tk.Label(windows, text="Gender", bg='#438c9c')
label_gender.pack(pady=5)
entry_gender = tk.Entry(windows)
entry_gender.pack(pady=5)

label_position = tk.Label(windows, text="Position", bg='#438c9c')
label_position.pack(pady=5)
entry_position = tk.Entry(windows)
entry_position.pack(pady=5)

label_username = tk.Label(windows, text="Username", bg='#438c9c')
label_username.pack(pady=5)
entry_username = tk.Entry(windows)
entry_username.pack(pady=5)

label_password = tk.Label(windows, text="Password", bg='#438c9c')
label_password.pack(pady=5)
entry_password = tk.Entry(windows, show="*")
entry_password.pack(pady=5)

label_confirmpassword = tk.Label(windows, text="Confirm Password", bg='#438c9c')
label_confirmpassword.pack(pady=5)
entry_confirmpassword = tk.Entry(windows, show="*")
entry_confirmpassword.pack(pady=5)

# Buttons for Add, Update, and Delete operations in a horizontal layout
buttons_frame = tk.Frame(windows, bg='#438c9c')
buttons_frame.pack(pady=10)

btn_add = tk.Button(buttons_frame, text="Add User", bg="green", fg="white", command=add_user)
btn_add.grid(row=0, column=0, padx=10)

btn_update = tk.Button(buttons_frame, text="Update User", bg="blue", fg="white", command=update_user)
btn_update.grid(row=0, column=1, padx=10)

btn_delete = tk.Button(buttons_frame, text="Delete User", bg="red", fg="white", command=delete_user)
btn_delete.grid(row=0, column=2, padx=10)

# Back button on bottom-left corner
btn_back = tk.Button(windows, text="Back", bg="red", fg="white", command=back_to_dashboard)
btn_back.place(x=10, y=720)

# Fetch users when the application starts
fetch_users()

windows.mainloop()

cursor.close()
db.close()