# Library Management System

A desktop library management system built with Python, Tkinter, and MySQL.

## Features
- User registration and login
- Book management
- Member management
- Borrowing/returns management

## Running it
1. Install dependencies: `pip install pymysql pillow`
2. Create the database: `mysql -u root -p < schema.sql`
3. Set your DB credentials as environment variables (defaults to user `root`,
   empty password):
   ```
   set DB_USER=root
   set DB_PASSWORD=your_password
   ```
4. Run `python dashboard.py`
