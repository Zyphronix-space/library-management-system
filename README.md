# Library Management System

A desktop library management system built with Python, Tkinter, and MySQL.

## Features

- User registration and login
- Book management (add / search / update / remove)
- Member management
- Borrowing and returns, with fine calculation on late returns

## Stack

- **UI:** Python, Tkinter (stdlib)
- **Database:** MySQL via `pymysql`
- **Images:** Pillow

The app is organized as one module per feature (`bookManagement.py`,
`memberManagement.py`, `borrowingManagement.py`, `userManagement.py`, ...)
rather than a class-based architecture — each module owns its own Tkinter
screen and its own database calls.

## Security notes

Two things worth calling out since they're easy to get wrong in a first
database project: every SQL query is parameterized (`%s` placeholders, never
string-concatenated), and passwords are stored as PBKDF2-HMAC-SHA256 hashes
with a random per-user salt (`auth_utils.py`) rather than plaintext.

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
