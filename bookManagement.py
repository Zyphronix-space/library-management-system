import tkinter as tk
from tkinter import ttk, messagebox
import pymysql
from db_config import DB_USER, DB_PASSWORD
from nav_utils import go_to
windows = tk.Tk()
windows.title("Book Management")
windows.config(bg='#438c9c')

db = pymysql.connect(host='localhost', user=DB_USER, password=DB_PASSWORD, database='libraryManagementSystem')
cursor = db.cursor()
#fetch all books from the db
def fetch_books():
    book_tree.delete(*book_tree.get_children())
    cursor.execute("SELECT * FROM books")
    rows = cursor.fetchall()
    for row in rows:
        book_tree.insert("", tk.END, values=row)

#Function to add a new book to the inventory
def add_book():
    title = entry_title.get()
    author = entry_author.get()
    isbn = entry_isbn.get()
    year = entry_year.get()

#Validation checks
    if not title or not author or not isbn or not year:
        messagebox.showwarning("Input Error", "All fields must be filled!")
        return
    elif not isbn.isdigit():
        messagebox.showwarning("Input Error", "ISBN must be numeric!")
        return
    elif not len(entry_year.get()) == 4:
        messagebox.showwarning("Input Error", "Year must be a 4-digit number!")
        return

    #Add book to the database if validation passes
    cursor.execute("INSERT INTO books (title, author, isbn, year) VALUES (%s, %s, %s, %s)", (title, author, isbn, year))
    db.commit()
    messagebox.showinfo("Success", "Book added successfully!")

    clear_entries()

    fetch_books()

#Function to update selected book in the inventory
def update_book():
    selected_item = book_tree.selection()
    if selected_item:
        selected_book = book_tree.item(selected_item)['values']
        book_id = selected_book[0]
        title = entry_title.get()
        author = entry_author.get()
        isbn = entry_isbn.get()
        year = entry_year.get()

        #Validation checks
        if not title or not author or not isbn or not year:
            messagebox.showwarning("Input Error", "All fields must be filled!")
            return
        elif not isbn.isdigit():
            messagebox.showwarning("Input Error", "ISBN must be numeric!")
            return
        elif not len(entry_year.get()) == 4:
            messagebox.showwarning("Input Error", "Year must be a 4-digit number!")
            return

        #Update book in the db
        cursor.execute("UPDATE books SET title=%s, author=%s, isbn=%s, year=%s WHERE id=%s",
                       (title, author, isbn, year, book_id))
        db.commit()
        messagebox.showinfo("Success", "Book updated successfully!")
        clear_entries()
        fetch_books()
    else:
        messagebox.showwarning("Selection Error", "Please select a book to update")


#delete selected book from the inventory with confirmation
def delete_book():
    selected_item = book_tree.selection()
    if selected_item:
        selected_book = book_tree.item(selected_item)['values']
        book_id = selected_book[0]

        #Ask for confirmation before deleting
        confirm = messagebox.askyesno("Confirm Delete",
                                      f"Are you sure you want to delete the book '{selected_book[1]}'?")
        if confirm:
            cursor.execute("DELETE FROM books WHERE id=%s", (book_id,))
            db.commit()
            messagebox.showinfo("Success", "Book deleted successfully!")

            clear_entries()

            # Refresh the table view
            fetch_books()
    else:
        messagebox.showwarning("Selection Error", "Please select a book to delete")

#Function to search books by any detail
def search_books():
    search_query = entry_search.get()
    book_tree.delete(*book_tree.get_children())
    if search_query:
        cursor.execute("SELECT * FROM books WHERE title LIKE %s OR author LIKE %s OR isbn LIKE %s OR year LIKE %s",
                       ('%' + search_query + '%', '%' + search_query + '%', '%' + search_query + '%',
                        '%' + search_query + '%'))
        rows = cursor.fetchall()
        for row in rows:
            book_tree.insert("", tk.END, values=row)
    else:
        fetch_books()

#Function to clear search results and show all books again
def clear_search():
    entry_search.delete(0, tk.END)
    fetch_books()

#load selected book data into entry fields for update
def load_book_data(event):
    selected_item = book_tree.selection()
    if selected_item:
        selected_book = book_tree.item(selected_item)['values']
        entry_title.delete(0, tk.END)
        entry_title.insert(tk.END, selected_book[1])
        entry_author.delete(0, tk.END)
        entry_author.insert(tk.END, selected_book[2])
        entry_isbn.delete(0, tk.END)
        entry_isbn.insert(tk.END, selected_book[3])
        entry_year.delete(0, tk.END)
        entry_year.insert(tk.END, selected_book[4])

#Function to clear entry fields
def clear_entries():
    entry_title.delete(0, tk.END)
    entry_author.delete(0, tk.END)
    entry_isbn.delete(0, tk.END)
    entry_year.delete(0, tk.END)
#Function to go back to the dashboard
def go_back():
    windows.destroy()
    go_to('dashboard')

#Heading for the window
label_heading = tk.Label(windows, text="Book Management", bg='#438c9c', font=("Microsoft YaHei UI Light", 16, "bold"))
label_heading.pack(pady=10)

#Table (Tree) to display books
book_tree = ttk.Treeview(windows, columns=("ID", "Title", "Author", "ISBN", "Year"), show="headings", height=8)
book_tree.heading("ID", text="ID")
book_tree.heading("Title", text="Title")
book_tree.heading("Author", text="Author")
book_tree.heading("ISBN", text="ISBN")
book_tree.heading("Year", text="Year")
book_tree.pack(pady=10)

#getting selected data to entry fields
book_tree.bind("<ButtonRelease-1>", load_book_data)

#Labels and entry fields for book details
form_frame = tk.Frame(windows, bg='#438c9c')
form_frame.pack(pady=10)

label_title = tk.Label(form_frame, text="Title", bg='#438c9c')
label_title.grid(row=0, column=0, padx=5, pady=5)
entry_title = tk.Entry(form_frame)
entry_title.grid(row=0, column=1, padx=5, pady=5)

label_author = tk.Label(form_frame, text="Author", bg='#438c9c')
label_author.grid(row=1, column=0, padx=5, pady=5)
entry_author = tk.Entry(form_frame)
entry_author.grid(row=1, column=1, padx=5, pady=5)

label_isbn = tk.Label(form_frame, text="ISBN", bg='#438c9c')
label_isbn.grid(row=2, column=0, padx=5, pady=5)
entry_isbn = tk.Entry(form_frame)
entry_isbn.grid(row=2, column=1, padx=5, pady=5)

label_year = tk.Label(form_frame, text="Year", bg='#438c9c')
label_year.grid(row=3, column=0, padx=5, pady=5)
entry_year = tk.Entry(form_frame)
entry_year.grid(row=3, column=1, padx=5, pady=5)

# Search field and button
search_frame = tk.Frame(windows, bg='#438c9c')
search_frame.pack(pady=10)

label_search = tk.Label(search_frame, text="Search by Title, Author, ISBN or Year", bg='#438c9c')
label_search.grid(row=0, column=0, padx=5)
entry_search = tk.Entry(search_frame)
entry_search.grid(row=0, column=1, padx=5)
btn_search = tk.Button(search_frame, text="Search", command=search_books)
btn_search.grid(row=0, column=2, padx=5)

#Button to clear search results and return to default list
btn_clear_search = tk.Button(search_frame, text="Clear Search", command=clear_search)
btn_clear_search.grid(row=0, column=3, padx=5)

#Buttons for Add, Update, Delete operations
button_frame = tk.Frame(windows, bg='#438c9c')
button_frame.pack(pady=10)

btn_add = tk.Button(button_frame, text="Add Book", bg="green", fg="white", command=add_book, width=12)
btn_add.grid(row=0, column=0, padx=5)

btn_update = tk.Button(button_frame, text="Update Book", bg="blue", fg="white", command=update_book, width=12)
btn_update.grid(row=0, column=1, padx=5)

btn_delete = tk.Button(button_frame, text="Delete Book", bg="red", fg="white", command=delete_book, width=12)
btn_delete.grid(row=0, column=2, padx=5)

# Back button at the bottom left
back_button = tk.Button(windows, text="Back", bg='red', fg="black" , command=go_back)
back_button.pack(side=tk.LEFT, padx=10, pady=10)

fetch_books()

windows.mainloop()

cursor.close()
db.close()