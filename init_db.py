import sqlite3

def init_db():
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()

    # Create Employees table
    cur.execute('''
        CREATE TABLE IF NOT EXISTS Employees (
            ID INTEGER PRIMARY KEY,
            Name TEXT NOT NULL,
            Department TEXT NOT NULL,
            Salary INTEGER,
            Hire_Date TEXT
        )
    ''')

    # Create Departments table
    cur.execute('''
        CREATE TABLE IF NOT EXISTS Departments (
            ID INTEGER PRIMARY KEY,
            Name TEXT NOT NULL,
            Manager TEXT
        )
    ''')

    # Insert sample data for Employees
    employees_data = [
        (1, 'Alice', 'Sales', 50000, '2021-01-10'),
        (2, 'Bob', 'Engineering', 70000, '2020-06-10'),
        (3, 'Charlie', 'Marketing', 60000, '2022-03-20'),
        (4, 'David', 'Sales', 55000, '2021-01-10'),
        (5, 'Eve', 'Engineering', 72000, '2020-06-10'),
        (6, 'Frank', 'Marketing', 58000, '2022-03-20'),
        (7, 'Grace', 'Sales', 53000, '2021-01-10'),
        (8, 'Hank', 'Engineering', 75000, '2020-06-10'),
        (9, 'Ivy', 'Marketing', 61000, '2022-03-20'),
        (10, 'Jack', 'Sales', 51000, '2021-01-10'),
        (11, 'Karen', 'Engineering', 73000, '2020-06-10'),
        (12, 'Leo', 'Marketing', 59000, '2022-03-20')
    ]
    cur.executemany('''
        INSERT OR REPLACE INTO Employees (ID, Name, Department, Salary, Hire_Date)
        VALUES (?, ?, ?, ?, ?)
    ''', employees_data)

    # Insert sample data for Departments
    departments_data = [
        (1, 'Sales', 'Alice'),
        (2, 'Engineering', 'Bob'),
        (3, 'Marketing', 'Eve')  # Sample manager for Marketing; update as needed.
    ]
    cur.executemany('''
        INSERT OR REPLACE INTO Departments (ID, Name, Manager)
        VALUES (?, ?, ?)
    ''', departments_data)

    conn.commit()
    conn.close()
    print("Database initialized successfully.")

if __name__ == '__main__':
    init_db()
