const test = require('node:test');
const assert = require('node:assert');
const path = require('node:path');
const fs = require('node:fs');
const { HostelDatabaseManager } = require('../database/db');
const { createHostelServer } = require('../backend/server');
const { seedHostelDatabase } = require('../database/seed');

const TEST_DB = path.join(__dirname, 'test_hostel.db');

test('UFTB Hostel Management System Test Suite', async (t) => {
    if (fs.existsSync(TEST_DB)) {
        try { fs.unlinkSync(TEST_DB); } catch (_) {}
    }
    const db = new HostelDatabaseManager(TEST_DB);
    seedHostelDatabase(TEST_DB);

    const server = createHostelServer(db);
    await new Promise(res => server.listen(0, res));
    const port = server.address().port;
    const base = `http://localhost:${port}/api`;

    t.after(() => {
        try { server.close(); } catch (_) {}
        try { db.close(); } catch (_) {}
        try { if (fs.existsSync(TEST_DB)) fs.unlinkSync(TEST_DB); } catch (_) {}
    });

    await t.test('1. Should fetch summary stats', async () => {
        const res = await fetch(`${base}/stats`);
        const data = await res.json();
        assert.strictEqual(res.status, 200);
        assert.ok(data.totalStudents >= 3);
        assert.ok(data.totalRooms >= 3);
    });

    await t.test('2. Should register a new student', async () => {
        const res = await fetch(`${base}/students`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                student_id: 'STD_202199',
                name: 'Test Student',
                email: 'test@uftb.edu.bd',
                department: 'Software Engineering'
            })
        });
        assert.strictEqual(res.status, 201);
    });

    await t.test('3. Should allocate room to registered student', async () => {
        const student = db.get(`SELECT id FROM students WHERE student_id = 'STD_202199'`);
        const room = db.get(`SELECT id FROM rooms WHERE room_number = '102'`);

        const res = await fetch(`${base}/allocations`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                student_id: student.id,
                room_id: room.id
            })
        });
        assert.strictEqual(res.status, 201);
    });

    await t.test('4. Should record fee payment', async () => {
        const student = db.get(`SELECT id FROM students WHERE student_id = 'STD_202199'`);
        const res = await fetch(`${base}/payments`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                student_id: student.id,
                month_year: 'November 2026',
                amount: 1500,
                payment_status: 'Paid'
            })
        });
        assert.strictEqual(res.status, 201);
    });

    await t.test('5. Should report maintenance issue', async () => {
        const room = db.get(`SELECT id FROM rooms WHERE room_number = '102'`);
        const res = await fetch(`${base}/maintenance`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                room_id: room.id,
                issue_description: 'Water faucet leakage in washroom',
                priority: 'High'
            })
        });
        assert.strictEqual(res.status, 201);
    });
});
