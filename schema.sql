CREATE DATABASE IF NOT EXISTS libraryManagementSystem;
USE libraryManagementSystem;

CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    firstname VARCHAR(50) NOT NULL,
    lastname VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    gender VARCHAR(10),
    position VARCHAR(50),
    username VARCHAR(50) NOT NULL UNIQUE,
    passwrd VARCHAR(255) NOT NULL,
    confirmpasswrd VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS members (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL,
    phone VARCHAR(20) NOT NULL,
    address VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS books (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    author VARCHAR(100) NOT NULL,
    isbn VARCHAR(20) NOT NULL,
    year INT NOT NULL
);

CREATE TABLE IF NOT EXISTS borrowings (
    id INT AUTO_INCREMENT PRIMARY KEY,
    member_id INT NOT NULL,
    book_id INT NOT NULL,
    borrow_date DATE NOT NULL,
    return_date DATE NULL,
    fine DECIMAL(10,2) NULL DEFAULT 0,
    FOREIGN KEY (member_id) REFERENCES members(id),
    FOREIGN KEY (book_id) REFERENCES books(id)
);

-- Demo data
INSERT INTO members (name, email, phone, address) VALUES
    ('Nimal Perera', 'nimal@example.com', '0771234567', '123 Galle Road, Colombo'),
    ('Kamala Silva', 'kamala@example.com', '0779876543', '45 Kandy Road, Kandy');

INSERT INTO books (title, author, isbn, year) VALUES
    ('Clean Code', 'Robert C. Martin', '9780132350884', 2008),
    ('The Pragmatic Programmer', 'Andrew Hunt', '9780201616224', 1999);
