from tkinter import *
from tkinter import messagebox
import pymysql
from db_config import DB_USER, DB_PASSWORD
from auth_utils import hash_password
from nav_utils import go_to
windows = Tk()
windows.title('User Registration Form')
windows.geometry('540x640')
windows.config(bg='#438c9c')
# Show/hide password functionality
def show():
    passwordEntry.configure(show='*')
    check1.configure(command=hide)

def hide():
    passwordEntry.configure(show='')
    check1.configure(command=show)

def show1():
    renterpasswordEntry.configure(show='*')
    check2.configure(command=hide1)

def hide1():
    renterpasswordEntry.configure(show='')
    check2.configure(command=show1)
#Back button functionality
def back():
    windows.destroy()
    go_to('userLogin')

#Field Validations and DB connection
def submit():
    if (firstnameEntry.get() == '' or lastnameEntry.get() == '' or emailentry.get() == '' or
            gender.get() == '' or position.get() == 'Select Position' or usernameEntry.get() == '' or
            passwordEntry.get() == '' or renterpasswordEntry.get() == ''):
        messagebox.showerror('Alert!', 'All fields must be entered')
    elif len(passwordEntry.get()) < 6:
        messagebox.showerror('Alert!', 'Password must be at least 6 characters long.')
    elif passwordEntry.get() != renterpasswordEntry.get():
        messagebox.showerror('Alert!', 'Passwords did not match.')
    elif not emailentry.get().__contains__('@'):
        messagebox.showerror('Alert!', 'Invalid Email Address.')
    else:
        try:
            db = pymysql.connect(host='localhost', user=DB_USER, password=DB_PASSWORD)
            cur = db.cursor()
            query = 'use libraryManagementSystem'
            cur.execute(query)

            # Insert data into DB
            hashed = hash_password(passwordEntry.get())
            query = 'insert into users(firstname, lastname, email, gender, position, username, passwrd, confirmpasswrd) values(%s,%s,%s,%s,%s,%s,%s,%s)'
            cur.execute(query, (firstnameEntry.get(), lastnameEntry.get(), emailentry.get(), gender.get(), position.get(),
                                usernameEntry.get(), hashed, hashed))
            db.commit()
            db.close()

            messagebox.showinfo('Success', 'Successful Registration. Please log in.')
            clear_fields()

            windows.destroy()
            go_to('userLogin')
        except Exception as e:
            messagebox.showerror('Error', str(e))

# Clear fields after successful registration
def clear_fields():
    firstnameEntry.delete(0, END)
    lastnameEntry.delete(0, END)
    emailentry.delete(0, END)
    usernameEntry.delete(0, END)
    passwordEntry.delete(0, END)
    renterpasswordEntry.delete(0, END)
    gender.set(0)
    position.set('Select Position')

# Variables to hold user input
firstname = StringVar()
lastname = StringVar()
email = StringVar()
gender = StringVar()
position = StringVar()
username = StringVar()
passwrd = StringVar()
confirmpasswrd = StringVar()

# Frame setup
frame = Frame(windows, width=610, height=640, bg='#438c9c')
frame.place(x=0, y=0)

# Labels and Entry fields
heading = Label(frame, text='Personal Registration Form', fg='black', bg='#438c9c', font=('Microsoft YaHei UI Light', 20, 'bold'))
heading.place(x=90, y=3)

firstnameLabel = Label(frame, text="First Name:", fg='black', bg='#438c9c', font=('Microsoft YaHei UI Light', 14, 'bold'))
firstnameLabel.place(x=10, y=70)

firstnameEntry = Entry(frame, width=30, borderwidth=2)
firstnameEntry.place(x=240, y=70)

lastnameLabel = Label(frame, text="Last Name:", fg='black', bg='#438c9c', font=('Microsoft YaHei UI Light', 14, 'bold'))
lastnameLabel.place(x=10, y=110)

lastnameEntry = Entry(frame, width=30, borderwidth=2)
lastnameEntry.place(x=240, y=110)

idlabelEmail = Label(frame, text='Email:', fg='black', bg='#438c9c', font=('Microsoft YaHei UI Light', 14, 'bold'))
idlabelEmail.place(x=10, y=150)

emailentry = Entry(frame, width=30, borderwidth=2)
emailentry.place(x=240, y=150)

genderLabel = Label(frame, text='Select Gender:', fg='black', bg='#438c9c', font=('Microsoft YaHei UI Light', 14, 'bold'))
genderLabel.place(x=10, y=200)

gender.set(0)
genderRadio1 = Radiobutton(frame, text='Male', variable=gender, value='Male', font=('Microsoft YaHei UI Light', 12), bg='#438c9c')
genderRadio1.place(x=240, y=200)

genderRadio2 = Radiobutton(frame, text='Female', variable=gender, value='Female', font=('Microsoft YaHei UI Light', 12), bg='#438c9c')
genderRadio2.place(x=350, y=200)

positionLabel = Label(frame, text='Select Position:', fg='black', bg='#438c9c', font=('Microsoft YaHei UI Light', 14, 'bold'))
positionLabel.place(x=10, y=250)

# Dropdown for selecting position
positions = ['Librarian', "Assistant Librarian", 'Other']
position.set('Select Position')

positionLabelDropdown = OptionMenu(frame, position, *positions)
positionLabelDropdown.place(x=240, y=250)
positionLabelDropdown.config(width=18, font=('Microsoft YaHei UI Light', 12), bg='white', fg='black')

usernamelbl = Label(frame, text='Username:', fg='black', bg='#438c9c', font=('Microsoft YaHei UI Light', 14, 'bold'))
usernamelbl.place(x=10, y=300)

usernameEntry = Entry(frame, width=30, borderwidth=2)
usernameEntry.place(x=240, y=300)

passwordlbl = Label(frame, text='Password:', fg='black', bg='#438c9c', font=('Microsoft YaHei UI Light', 14, 'bold'))
passwordlbl.place(x=10, y=350)

passwordEntry = Entry(frame, width=30, borderwidth=2, show='*')  # Hides password by default
passwordEntry.place(x=240, y=350)

renterpasswordlbl = Label(frame, text='Confirm Password:', fg='black', bg='#438c9c', font=('Microsoft YaHei UI Light', 14, 'bold'))
renterpasswordlbl.place(x=10, y=400)

renterpasswordEntry = Entry(frame, width=30, borderwidth=2, show='*')
renterpasswordEntry.place(x=240, y=400)

# Buttons
bckbtn = Button(frame, text='Back', width=7, height=2, bg='black', fg='#b3c6c9', cursor='hand2', command=back)
bckbtn.place(x=10, y=580)

submit1btn = Button(frame, text='Submit', width=15, height=2, bg='black', fg='#b3c6c9', font=('Microsoft YaHei UI Light', 14, 'bold'),
                    cursor='hand2', command=submit)
submit1btn.place(x=150, y=500)

# Show/hide password checkboxes
check1 = Checkbutton(frame, text='', command=show, bg='#438c9c')
check1.place(x=420, y=350)

check2 = Checkbutton(frame, text='', command=show1, bg='#438c9c')
check2.place(x=420, y=400)

windows.mainloop()