import tkinter as tk
from tkinter import ttk, messagebox
import pymysql
from db_config import DB_USER, DB_PASSWORD
from datetime import datetime, timedelta
import re
from nav_utils import go_to
windows = tk.Tk()
windows.title("Library Management System - Borrowing Management")
windows.config(bg='#438c9c')

db = pymysql.connect(host='localhost', user=DB_USER, password=DB_PASSWORD, database='libraryManagementSystem')
cursor = db.cursor()

#fetch and display borrowing history
def fetch_borrowing_history():
    history_tree.delete(*history_tree.get_children())
    cursor.execute("""
        SELECT b.id, m.name, bk.title, b.borrow_date, b.return_date, b.fine
        FROM borrowings b
        JOIN members m ON b.member_id = m.id
        JOIN books bk ON b.book_id = bk.id
    """)
    rows = cursor.fetchall()
    for row in rows:
        history_tree.insert("", tk.END, values=row)

#issue a book
def issue_book():
    member_id = entry_member_id.get()
    book_id = entry_book_id.get()
    borrow_date = datetime.now().date()

    #Validation checks
    if not member_id or not book_id:
        messagebox.showwarning("Input Error", "Member ID and Book ID must be filled!")
        return

    try:
        #Insert borrowing record
        cursor.execute("INSERT INTO borrowings (member_id, book_id, borrow_date) VALUES (%s, %s, %s)",
                       (member_id, book_id, borrow_date))
        db.commit()
        messagebox.showinfo("Success", "Book issued successfully!")
    except pymysql.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")

    #Clear the entry fields after issuing
    clear_entries()


#record book return and calculate fines
def return_book():
    borrowing_id = entry_borrowing_id.get()
    return_date = datetime.now().date()

    if not borrowing_id:
        messagebox.showwarning("Input Error", "Borrowing ID must be filled!")
        return

    cursor.execute("SELECT borrow_date, return_date FROM borrowings WHERE id=%s", (borrowing_id,))
    result = cursor.fetchone()

    if result is None:
        messagebox.showerror("Not Found", f"No borrowing record with ID {borrowing_id}.")
        return
    if result[1] is not None:
        messagebox.showwarning("Already Returned", f"Borrowing ID {borrowing_id} was already returned.")
        return

    borrow_date = result[0]

    #Calculate fine if returned late
    due_date = borrow_date + timedelta(days=14)
    fine_amount = max(0, (return_date - due_date).days * 1.00)

    cursor.execute("UPDATE borrowings SET return_date=%s, fine=%s WHERE id=%s",(return_date, fine_amount, borrowing_id))
    db.commit()
    messagebox.showinfo("Success", "Book returned successfully!")

    clear_entries()

#to clear entry fields
def clear_entries():
    entry_member_id.delete(0, tk.END)
    entry_book_id.delete(0, tk.END)
    entry_borrowing_id.delete(0, tk.END)
def back_to_dashboard():
    windows.destroy()
    go_to('dashboard')

#Heading for the window
label_heading = tk.Label(windows, text="Borrowing Management", bg='#438c9c', font=("Microsoft YaHei UI Light", 16, "bold"))
label_heading.pack(pady=10)
# Frame for issuing and returning books
frame_operations = tk.Frame(windows, bg='#438c9c')
frame_operations.pack(pady=10)

#Labels and entry fields for issuing and returning books
label_member_id = tk.Label(frame_operations, text="Member ID", bg='#438c9c')
label_member_id.grid(row=0, column=0, padx=5, pady=5)
entry_member_id = tk.Entry(frame_operations)
entry_member_id.grid(row=0, column=1, padx=5, pady=5)

label_book_id = tk.Label(frame_operations, text="Book ID", bg='#438c9c')
label_book_id.grid(row=1, column=0, padx=5, pady=5)
entry_book_id = tk.Entry(frame_operations)
entry_book_id.grid(row=1, column=1, padx=5, pady=5)

label_borrowing_id = tk.Label(frame_operations, text="Borrowing ID (for return)", bg='#438c9c')
label_borrowing_id.grid(row=2, column=0, padx=5, pady=5)
entry_borrowing_id = tk.Entry(frame_operations)
entry_borrowing_id.grid(row=2, column=1, padx=5, pady=5)

#Buttons for issuing and returning books
btn_issue = tk.Button(frame_operations, text="Issue Book", bg='green', fg="white", command=issue_book)
btn_issue.grid(row=3, column=0, padx=5, pady=5)

btn_return = tk.Button(frame_operations, text="Return Book", bg='blue', fg="white", command=return_book)
btn_return.grid(row=3, column=1, padx=5, pady=5)

#Frame for borrowing history
frame_history = tk.Frame(windows)
frame_history.pack(pady=10)

#Table (Tree)to display borrowing history
history_tree = ttk.Treeview(frame_history, columns=("ID", "Member", "Book", "Borrow Date", "Return Date", "Fine"),
                            show="headings", height=10)
history_tree.heading("ID", text="ID")
history_tree.heading("Member", text="Member")
history_tree.heading("Book", text="Book")
history_tree.heading("Borrow Date", text="Borrow Date")
history_tree.heading("Return Date", text="Return Date")
history_tree.heading("Fine", text="Fine")
history_tree.pack()

#Button to fetch borrowing history
btn_fetch_history = tk.Button(windows, text="View Borrowing History", bg='#adad17', fg="black", command=fetch_borrowing_history)
btn_fetch_history.pack(pady=5)

#Back button at the lower-left corner
btn_back = tk.Button(windows, text="Back", bg="red", fg="black", command=back_to_dashboard)
btn_back.pack(side=tk.LEFT, padx=10, pady=10)

fetch_borrowing_history()

windows.mainloop()

cursor.close()
db.close()