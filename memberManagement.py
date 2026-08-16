import tkinter as tk
from tkinter import ttk, messagebox
import pymysql
from db_config import DB_USER, DB_PASSWORD
import re
from nav_utils import go_to
windows = tk.Tk()
windows.title("Library Management System - Member Management")
windows.geometry("900x700")
windows.config(bg='#438c9c')

db = pymysql.connect(host='localhost', user=DB_USER, password=DB_PASSWORD, database='libraryManagementSystem')
cursor = db.cursor()


#fetch all members from the database
def fetch_members():
    member_tree.delete(*member_tree.get_children())  #Empty the table before insert
    cursor.execute("SELECT * FROM members")
    rows = cursor.fetchall()
    for row in rows:
        member_tree.insert("", tk.END, values=row)

#add a new member to the db with validation
def add_member():
    name = entry_name.get()
    email = entry_email.get()
    phone = entry_phone.get()
    address = entry_address.get()

    if not name or not email or not phone or not address:
        messagebox.showwarning("Input Error", "All fields must be filled!")
        return
    elif len(entry_phone.get()) != 10:
        messagebox.showwarning("Input Error", "Phone number must be exactly 10 digits!")
        return
    elif not entry_email.get().__contains__('@'):
        messagebox.showwarning("Input Error", "Invalid email format!")
        return

    #Add member to the db if validation passes
    cursor.execute("INSERT INTO members (name, email, phone, address) VALUES (%s, %s, %s, %s)",
                   (name, email, phone, address))
    db.commit()
    messagebox.showinfo("Success", "Member added successfully!")

    clear_entries()

    # Refresh the table view
    fetch_members()


#update selected member in the db with validation
def update_member():
    selected_item = member_tree.selection()
    if selected_item:
        selected_member = member_tree.item(selected_item)['values']
        member_id = selected_member[0]
        name = entry_name.get()
        email = entry_email.get()
        phone = entry_phone.get()
        address = entry_address.get()

        #Validation checks
        if not name or not email or not phone or not address:
            messagebox.showwarning("Input Error", "All fields must be filled!")
            return
        elif len(entry_phone.get()) != 10:
            messagebox.showwarning("Input Error", "Phone number must be exactly 10 digits!")
            return
        elif not entry_email.get().__contains__('@'):
            messagebox.showwarning("Input Error", "Invalid email format!")
            return

        #Update member in the database
        cursor.execute("UPDATE members SET name=%s, email=%s, phone=%s, address=%s WHERE id=%s",
                       (name, email, phone, address, member_id))
        db.commit()
        messagebox.showinfo("Success", "Member updated successfully!")

        clear_entries()

        #Refresh the table view
        fetch_members()
    else:
        messagebox.showwarning("Selection Error", "Please select a member to update")


#delete selected member from the db with confirmation
def delete_member():
    selected_item = member_tree.selection()
    if selected_item:
        selected_member = member_tree.item(selected_item)['values']
        member_id = selected_member[0]

        #confirm before deleting
        confirm = messagebox.askyesno("Confirm Delete",
                                      f"Are you sure you want to delete the member {selected_member[1]}?")
        if confirm:
            cursor.execute("DELETE FROM members WHERE id=%s", (member_id,))
            db.commit()
            messagebox.showinfo("Success", "Member deleted successfully!")
            clear_entries()

            #Refresh the table view
            fetch_members()
    else:
        messagebox.showwarning("Selection Error", "Please select a member to delete")


#search member by name or email
def search_member():
    search_query = entry_search.get()
    member_tree.delete(*member_tree.get_children())
    if search_query:
        cursor.execute("SELECT * FROM members WHERE name LIKE %s OR email LIKE %s",
                       ('%' + search_query + '%', '%' + search_query + '%'))
        rows = cursor.fetchall()
        for row in rows:
            member_tree.insert("", tk.END, values=row)
    else:
        fetch_members()


#clear search results and show all members again
def clear_search():
    entry_search.delete(0, tk.END)
    fetch_members()  # Reload the full member list


#load selected member data into entry fields for update
def load_member_data(event):
    selected_item = member_tree.selection()
    if selected_item:
        selected_member = member_tree.item(selected_item)['values']
        entry_name.delete(0, tk.END)
        entry_name.insert(tk.END, selected_member[1])
        entry_email.delete(0, tk.END)
        entry_email.insert(tk.END, selected_member[2])
        entry_phone.delete(0, tk.END)
        entry_phone.insert(tk.END, selected_member[3])
        entry_address.delete(0, tk.END)
        entry_address.insert(tk.END, selected_member[4])


#clear entry fields
def clear_entries():
    entry_name.delete(0, tk.END)
    entry_email.delete(0, tk.END)
    entry_phone.delete(0, tk.END)
    entry_address.delete(0, tk.END)
def back_to_dashboard():
    windows.destroy()
    go_to('dashboard')


# Heading for the window
label_heading = tk.Label(windows, text="Member Management", bg='#438c9c', font=("Microsoft YaHei UI Light", 16, "bold"))
label_heading.pack(pady=10)

# Table (Tree)display members
member_tree = ttk.Treeview(windows, columns=("ID", "Name", "Email", "Phone", "Address"), show="headings", height=8)
member_tree.heading("ID", text="ID")
member_tree.heading("Name", text="Name")
member_tree.heading("Email", text="Email")
member_tree.heading("Phone", text="Phone")
member_tree.heading("Address", text="Address")
member_tree.pack(pady=20, fill='x')

#getting selected data to entry fields
member_tree.bind("<ButtonRelease-1>", load_member_data)

# Labels and entry fields for member details
label_name = tk.Label(windows, text="Name", bg='#438c9c')
label_name.pack(pady=5)
entry_name = tk.Entry(windows)
entry_name.pack(pady=5)

label_email = tk.Label(windows, text="Email", bg='#438c9c')
label_email.pack(pady=5)
entry_email = tk.Entry(windows)
entry_email.pack(pady=5)

label_phone = tk.Label(windows, text="Phone", bg='#438c9c')
label_phone.pack(pady=5)
entry_phone = tk.Entry(windows)
entry_phone.pack(pady=5)

label_address = tk.Label(windows, text="Address", bg='#438c9c')
label_address.pack(pady=5)
entry_address = tk.Entry(windows)
entry_address.pack(pady=5)

# Search field and button
label_search = tk.Label(windows, text="Search by Name or Email", bg='#438c9c')
label_search.pack(pady=5)
entry_search = tk.Entry(windows)
entry_search.pack(pady=5)
btn_search = tk.Button(windows, text="Search", command=search_member)
btn_search.pack(pady=5)

# Button to clear search results and return to default list
btn_clear_search = tk.Button(windows, text="Clear Search", command=clear_search)
btn_clear_search.pack(pady=5)

buttons_frame = tk.Frame(windows, bg='#438c9c')
buttons_frame.pack(pady=10)

btn_add = tk.Button(buttons_frame, text="Add Member", bg="green", fg="white", command=add_member)
btn_add.grid(row=0, column=0, padx=10)

btn_update = tk.Button(buttons_frame, text="Update Member", bg="blue", fg="white", command=update_member)
btn_update.grid(row=0, column=1, padx=10)

btn_delete = tk.Button(buttons_frame, text="Delete Member", bg="red", fg="white", command=delete_member)
btn_delete.grid(row=0, column=2, padx=10)

btn_back = tk.Button(windows, text="Back", bg="red", fg="black", command=back_to_dashboard)
btn_back.place(x=10, y=660)

# Fetch members when the app starts
fetch_members()

windows.mainloop()

# Close MySQL connection
cursor.close()
db.close()