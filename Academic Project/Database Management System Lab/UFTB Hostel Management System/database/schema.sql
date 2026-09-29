-- UFTB Hostel Management System Schema
-- Database Management System Lab (ICT 4254)

CREATE TABLE IF NOT EXISTS blocks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    block_name TEXT NOT NULL UNIQUE,
    gender_type TEXT CHECK(gender_type IN ('Male', 'Female', 'Co-Ed')) NOT NULL,
    total_floors INTEGER DEFAULT 4,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS rooms (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    block_id INTEGER NOT NULL,
    room_number TEXT NOT NULL,
    floor_number INTEGER DEFAULT 1,
    capacity INTEGER DEFAULT 4,
    occupied INTEGER DEFAULT 0,
    monthly_rent REAL DEFAULT 1500.00,
    UNIQUE(block_id, room_number),
    FOREIGN KEY (block_id) REFERENCES blocks(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id TEXT UNIQUE NOT NULL,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    department TEXT NOT NULL,
    phone TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS allocations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER NOT NULL,
    room_id INTEGER NOT NULL,
    allocated_date DATE DEFAULT (DATE('now')),
    status TEXT CHECK(status IN ('Active', 'Vacated', 'Pending')) DEFAULT 'Active',
    UNIQUE(student_id, status),
    FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE,
    FOREIGN KEY (room_id) REFERENCES rooms(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS fee_payments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER NOT NULL,
    month_year TEXT NOT NULL,
    amount REAL NOT NULL,
    payment_status TEXT CHECK(payment_status IN ('Paid', 'Pending', 'Overdue')) DEFAULT 'Paid',
    paid_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS maintenance_requests (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    room_id INTEGER NOT NULL,
    issue_description TEXT NOT NULL,
    priority TEXT CHECK(priority IN ('Low', 'Medium', 'High', 'Emergency')) DEFAULT 'Medium',
    status TEXT CHECK(status IN ('Open', 'In Progress', 'Resolved')) DEFAULT 'Open',
    reported_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (room_id) REFERENCES rooms(id) ON DELETE CASCADE
);
