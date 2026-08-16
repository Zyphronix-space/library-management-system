import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from nav_utils import go_to
windows = tk.Tk()
windows.title("Library Management System - Dashboard")
windows.geometry("600x400")
def open_user_management():
    windows.destroy()
    go_to('userManagement')

def open_member_management():
    windows.destroy()
    go_to('memberManagement')

def open_book_management():
    windows.destroy()
    go_to('bookManagement')

def open_borrowing_management():
    windows.destroy()
    go_to('borrowingManagement')


#log out function
def log_out():
    confirm = messagebox.askyesno("Log Out", "Are you sure you want to log out?")
    if confirm:
        windows.destroy()
        go_to('userLogin')

def load_cropped_background(path, target_width, target_height):
    """Center-crop to the target aspect ratio before resizing, so
    portrait/mismatched-ratio source images fill the frame without
    stretching/distortion."""
    image = Image.open(path)
    src_width, src_height = image.size
    target_ratio = target_width / target_height
    src_ratio = src_width / src_height

    if src_ratio > target_ratio:
        # source is relatively wider than target -> crop left/right
        new_width = int(src_height * target_ratio)
        left = (src_width - new_width) // 2
        image = image.crop((left, 0, left + new_width, src_height))
    else:
        # source is relatively taller than target -> crop top/bottom
        new_height = int(src_width / target_ratio)
        top = (src_height - new_height) // 2
        image = image.crop((0, top, src_width, top + new_height))

    return image.resize((target_width, target_height))


bg_image = load_cropped_background("images/library.jpg", 600, 400)
bg_photo = ImageTk.PhotoImage(bg_image)

#frame for bg image
canvas = tk.Canvas(windows, width=600, height=400)
canvas.pack(fill="both", expand=True)

# Display the bg image
canvas.create_image(0, 0, image=bg_photo, anchor="nw")

#header for "Library Management System"
header_label = tk.Label(windows, text="Library Management System", font=("Microsoft YaHei UI Light", 24, "bold"), bg="#111", fg="yellow")
canvas.create_window(300, 50, window=header_label)  # Place the header in the center-top

#Create the subheading for "Dashboard"
dashboard_label = tk.Label(windows, text="Dashboard", font=("Microsoft YaHei UI Light", 20, "bold"), bg="#111", fg="#f0e68c")
canvas.create_window(300, 100, window=dashboard_label)  # Place the dashboard label below the main header

#button styles
btn_font = ("Helvetica", 14)
btn_bg = "#141413"  # black
btn_fg = "#adad9c"  #dark yellow
btn_width = 20

#buttons for navigation
btn_user_mgmt = tk.Button(windows, text="User Management", font=btn_font, bg=btn_bg, fg=btn_fg, width=btn_width, command=open_user_management)
canvas.create_window(300, 150, window=btn_user_mgmt)

btn_member_mgmt = tk.Button(windows, text="Member Management", font=btn_font, bg=btn_bg, fg=btn_fg, width=btn_width, command=open_member_management)
canvas.create_window(300, 200, window=btn_member_mgmt)

btn_book_mgmt = tk.Button(windows, text="Book Management", font=btn_font, bg=btn_bg, fg=btn_fg, width=btn_width, command=open_book_management)
canvas.create_window(300, 250, window=btn_book_mgmt)

btn_borrow_mgmt = tk.Button(windows, text="Borrowing Management", font=btn_font, bg=btn_bg, fg=btn_fg, width=btn_width, command=open_borrowing_management)
canvas.create_window(300, 300, window=btn_borrow_mgmt)

#log out button placed at the bottom-right corner
btn_logout = tk.Button(windows, text="Log Out", font=("Helvetica", 10), bg="red", fg="white", width=10, command=log_out)
canvas.create_window(550, 370, window=btn_logout)

windows.mainloop()