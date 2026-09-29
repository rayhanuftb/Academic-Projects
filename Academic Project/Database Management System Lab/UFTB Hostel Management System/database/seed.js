const { getHostelDb } = require('./db');

function seedHostelDatabase(dbPath) {
    const db = getHostelDb(dbPath);

    console.log('[+] Seeding UFTB Hostel Database...');

    db.exec(`
        DELETE FROM maintenance_requests;
        DELETE FROM fee_payments;
        DELETE FROM allocations;
        DELETE FROM students;
        DELETE FROM rooms;
        DELETE FROM blocks;
    `);

    // 1. Insert Blocks
    db.run(`INSERT INTO blocks (block_name, gender_type, total_floors) VALUES (?, ?, ?)`, ['Pioneer Hall (Block A)', 'Male', 4]);
    const blockA = db.get(`SELECT id FROM blocks WHERE block_name = ?`, ['Pioneer Hall (Block A)']).id;

    db.run(`INSERT INTO blocks (block_name, gender_type, total_floors) VALUES (?, ?, ?)`, ['Frontier Hall (Block B)', 'Female', 4]);
    const blockB = db.get(`SELECT id FROM blocks WHERE block_name = ?`, ['Frontier Hall (Block B)']).id;

    // 2. Insert Rooms
    db.run(`INSERT INTO rooms (block_id, room_number, floor_number, capacity, occupied, monthly_rent) VALUES (?, ?, ?, ?, ?, ?)`, [blockA, '101', 1, 4, 2, 1500]);
    const room101 = db.get(`SELECT id FROM rooms WHERE block_id = ? AND room_number = '101'`, [blockA]).id;

    db.run(`INSERT INTO rooms (block_id, room_number, floor_number, capacity, occupied, monthly_rent) VALUES (?, ?, ?, ?, ?, ?)`, [blockA, '102', 1, 4, 1, 1500]);
    const room102 = db.get(`SELECT id FROM rooms WHERE block_id = ? AND room_number = '102'`, [blockA]).id;

    db.run(`INSERT INTO rooms (block_id, room_number, floor_number, capacity, occupied, monthly_rent) VALUES (?, ?, ?, ?, ?, ?)`, [blockB, '201', 2, 4, 1, 1500]);
    const room201 = db.get(`SELECT id FROM rooms WHERE block_id = ? AND room_number = '201'`, [blockB]).id;

    // 3. Insert Students
    db.run(`INSERT INTO students (student_id, name, email, department, phone) VALUES (?, ?, ?, ?, ?)`, ['STD_202101', 'Rayhanul Islam', 'rayhanul@uftb.edu.bd', 'Educational Technology & Engineering', '+8801700000001']);
    const stud1 = db.get(`SELECT id FROM students WHERE student_id = 'STD_202101'`).id;

    db.run(`INSERT INTO students (student_id, name, email, department, phone) VALUES (?, ?, ?, ?, ?)`, ['STD_202102', 'Tanvir Ahmed', 'tanvir@uftb.edu.bd', 'Computer Science & Engineering', '+8801700000002']);
    const stud2 = db.get(`SELECT id FROM students WHERE student_id = 'STD_202102'`).id;

    db.run(`INSERT INTO students (student_id, name, email, department, phone) VALUES (?, ?, ?, ?, ?)`, ['STD_202103', 'Farhana Akter', 'farhana@uftb.edu.bd', 'Software Engineering', '+8801700000003']);
    const stud3 = db.get(`SELECT id FROM students WHERE student_id = 'STD_202103'`).id;

    // 4. Allocations
    db.run(`INSERT INTO allocations (student_id, room_id, status) VALUES (?, ?, 'Active')`, [stud1, room101]);
    db.run(`INSERT INTO allocations (student_id, room_id, status) VALUES (?, ?, 'Active')`, [stud2, room101]);
    db.run(`INSERT INTO allocations (student_id, room_id, status) VALUES (?, ?, 'Active')`, [stud3, room201]);

    // 5. Payments
    db.run(`INSERT INTO fee_payments (student_id, month_year, amount, payment_status) VALUES (?, ?, ?, ?)`, [stud1, 'October 2026', 1500, 'Paid']);
    db.run(`INSERT INTO fee_payments (student_id, month_year, amount, payment_status) VALUES (?, ?, ?, ?)`, [stud2, 'October 2026', 1500, 'Paid']);

    // 6. Maintenance Requests
    db.run(`INSERT INTO maintenance_requests (room_id, issue_description, priority, status) VALUES (?, ?, ?, ?)`, [room101, 'Ceiling fan speed regulator replacement needed', 'Low', 'Open']);

    console.log('[+] Hostel database pre-seeded with sample blocks, rooms, allocations, and payment records.');
}

if (require.main === module) {
    seedHostelDatabase();
}

module.exports = { seedHostelDatabase };
