from tkinter import *
from tkinter import messagebox
import pymysql
from db_config import DB_USER, DB_PASSWORD
from auth_utils import verify_password
from nav_utils import go_to
windows = Tk()
windows.title('Library Management System Login')
windows.geometry('490x300+200+200')
windows.config(bg='#438c9c')
# Button Definition to navigate to registration form
def create_one():
    windows.destroy()
    go_to('userRegistration')

# Function to open the Dashboard from a separate file
def open_dashboard():
    windows.destroy()
    go_to('dashboard')


# Ensure this matches the filename of your dashboard file

# DB Connection and login functionality
def login():
    if idEntry.get() == '' or passwdEntry.get() == '':
        messagebox.showerror('Alert', 'Please enter all entry fields!')
    else:
        db = pymysql.connect(host='localhost', user=DB_USER, password=DB_PASSWORD, database='libraryManagementSystem')
        cur = db.cursor()
        query = 'select * from users where email=%s'
        cur.execute(query, (idEntry.get(),))
        user = cur.fetchone()
        db.close()

        # columns: id, firstname, lastname, email, gender, position, username, passwrd, confirmpasswrd
        if user is None or not verify_password(passwdEntry.get(), user[7]):
            messagebox.showerror('Alert!', 'Incorrect email or password')
        else:
            messagebox.showinfo('Success', 'Login Successful')
            open_dashboard()  # Call to open the dashboard


# Show/hide password functionality
def show():
    passwdEntry.configure(show='*')
    check.configure(command=hide, text='Hide')

def hide():
    passwdEntry.configure(show='')
    check.configure(command=show, text='Show')
#GUI design
frame = Frame(windows, width=480, height=280, bg='#438c9c')  # Gold background for frame as well
frame.place(x=0, y=0)

#Welcome text
welcome_label = Label(frame, text='Welcome to Library Management System', fg='#15272b', bg='#438c9c', font=('Arial', 16, 'bold'))
welcome_label.grid(row=0, column=0, columnspan=3, pady=10, padx=20)

#Instruction text
instruction_label = Label(frame, text='Please Login using your Email and Password', fg='black', bg='#438c9c', font=('Arial', 12, 'italic'))
instruction_label.grid(row=1, column=0, columnspan=3, pady=5)

#Email label
idlabel = Label(frame, text='Email', fg='black', bg='#438c9c', font=('Microsoft YaHei UI Light', 14, 'bold'))
idlabel.grid(row=2, column=0, pady=10, padx=10, sticky=E)

#Email entry
idEntry = Entry(frame, width=30, bd=3)
idEntry.grid(row=2, column=1, columnspan=2, padx=10, pady=10, sticky=W)

#Password label
passwdlabel = Label(frame, text='Password', fg='black', bg='#438c9c', font=('Microsoft YaHei UI Light', 14, 'bold'))
passwdlabel.grid(row=3, column=0, pady=10, padx=10, sticky=E)

#Password entry
passwdEntry = Entry(frame, width=30, bd=3, show='*')  # Hides password by default
passwdEntry.grid(row=3, column=1, columnspan=2, padx=10, pady=10, sticky=W)

#Login button
loginbtn = Button(frame, text='LOGIN', bg='black', pady=10, width=23, fg='#74bdcc', font=('Arial', 9, 'bold'), cursor='hand2', border=0, command=login)
loginbtn.grid(row=4, column=0, columnspan=3, pady=20)

#Create account section
donthaveacctLabel = Label(frame, text="Don't have an account?", fg='black', bg='#438c9c', pady=4, font=('Microsoft YaHei UI Light', 9, 'bold'))
donthaveacctLabel.grid(row=5, column=0, padx=10, pady=10, sticky=E)

createbtn = Button(frame, width=15, text='Create One', border=0, bg='black', cursor='hand2', fg='#438c9c', font=('Arial', 8, 'bold'), command=create_one)
createbtn.grid(row=5, column=1, pady=10, sticky=W)

#Password show checkbox
check = Checkbutton(frame, text='Show', command=show, bg='#438c9c', fg='black', font=('Arial', 9))
check.grid(row=3, column=2, padx=5, sticky=W)





windows.mainloop()

