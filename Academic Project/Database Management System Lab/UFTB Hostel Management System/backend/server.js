const http = require('node:http');
const fs = require('node:fs');
const path = require('node:path');
const { getHostelDb } = require('../database/db');

const PORT = process.env.PORT || 4100;
const FRONTEND_DIR = path.join(__dirname, '..', 'frontend');

function parseBody(req) {
    return new Promise((resolve, reject) => {
        let body = '';
        req.on('data', chunk => body += chunk);
        req.on('end', () => {
            if (!body) return resolve({});
            try { resolve(JSON.parse(body)); } catch (e) { reject(new Error('Invalid JSON')); }
        });
        req.on('error', reject);
    });
}

function sendJson(res, statusCode, data) {
    res.writeHead(statusCode, {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type'
    });
    res.end(JSON.stringify(data));
}

function createHostelServer(dbInstance) {
    const db = dbInstance || getHostelDb();

    return http.createServer(async (req, res) => {
        if (req.method === 'OPTIONS') {
            res.writeHead(204, {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type'
            });
            return res.end();
        }

        const url = new URL(req.url, `http://${req.headers.host || 'localhost'}`);
        const pathname = url.pathname;

        try {
            // Stats / Summary
            if (pathname === '/api/stats' && req.method === 'GET') {
                const totalStudents = db.get(`SELECT COUNT(*) as count FROM students`).count;
                const totalRooms = db.get(`SELECT COUNT(*) as count FROM rooms`).count;
                const occupiedBeds = db.get(`SELECT COUNT(*) as count FROM allocations WHERE status = 'Active'`).count;
                const totalCapacity = db.get(`SELECT SUM(capacity) as count FROM rooms`).count || 0;
                const pendingIssues = db.get(`SELECT COUNT(*) as count FROM maintenance_requests WHERE status != 'Resolved'`).count;

                return sendJson(res, 200, {
                    totalStudents,
                    totalRooms,
                    occupiedBeds,
                    totalCapacity,
                    availableBeds: Math.max(0, totalCapacity - occupiedBeds),
                    pendingIssues
                });
            }

            // Students CRUD
            if (pathname === '/api/students' && req.method === 'GET') {
                const students = db.query(`
                    SELECT s.*, r.room_number, b.block_name, a.status as allocation_status
                    FROM students s
                    LEFT JOIN allocations a ON s.id = a.student_id AND a.status = 'Active'
                    LEFT JOIN rooms r ON a.room_id = r.id
                    LEFT JOIN blocks b ON r.block_id = b.id
                    ORDER BY s.student_id ASC
                `);
                return sendJson(res, 200, { students });
            }

            if (pathname === '/api/students' && req.method === 'POST') {
                const { student_id, name, email, department, phone } = await parseBody(req);
                if (!student_id || !name || !email) {
                    return sendJson(res, 400, { error: 'Student ID, Name, and Email are required.' });
                }
                const ins = db.run(
                    `INSERT INTO students (student_id, name, email, department, phone) VALUES (?, ?, ?, ?, ?)`,
                    [student_id.trim(), name.trim(), email.trim(), department || 'General', phone || '']
                );
                return sendJson(res, 201, { message: 'Student registered successfully', id: ins.lastInsertRowid });
            }

            // Rooms & Allocations
            if (pathname === '/api/rooms' && req.method === 'GET') {
                const rooms = db.query(`
                    SELECT r.*, b.block_name, b.gender_type,
                    (SELECT COUNT(*) FROM allocations WHERE room_id = r.id AND status = 'Active') as occupied_count
                    FROM rooms r
                    JOIN blocks b ON r.block_id = b.id
                    ORDER BY b.block_name, r.room_number
                `);
                return sendJson(res, 200, { rooms });
            }

            if (pathname === '/api/allocations' && req.method === 'POST') {
                const { student_id, room_id } = await parseBody(req);
                if (!student_id || !room_id) {
                    return sendJson(res, 400, { error: 'Student ID and Room ID are required.' });
                }

                // Check room capacity
                const room = db.get(`SELECT capacity, (SELECT COUNT(*) FROM allocations WHERE room_id = ? AND status = 'Active') as occupied FROM rooms WHERE id = ?`, [room_id, room_id]);
                if (!room) return sendJson(res, 404, { error: 'Room not found' });
                if (room.occupied >= room.capacity) {
                    return sendJson(res, 400, { error: 'Room has reached maximum capacity.' });
                }

                db.run(
                    `INSERT INTO allocations (student_id, room_id, status) VALUES (?, ?, 'Active')
                     ON CONFLICT(student_id, status) DO UPDATE SET room_id = excluded.room_id`,
                    [student_id, room_id]
                );
                return sendJson(res, 201, { message: 'Room allocated successfully to student' });
            }

            // Payments
            if (pathname === '/api/payments' && req.method === 'GET') {
                const payments = db.query(`
                    SELECT fp.*, s.name as student_name, s.student_id as student_code
                    FROM fee_payments fp
                    JOIN students s ON fp.student_id = s.id
                    ORDER BY fp.paid_at DESC
                `);
                return sendJson(res, 200, { payments });
            }

            if (pathname === '/api/payments' && req.method === 'POST') {
                const { student_id, month_year, amount, payment_status } = await parseBody(req);
                if (!student_id || !month_year || !amount) {
                    return sendJson(res, 400, { error: 'Student ID, Month/Year, and Amount are required.' });
                }
                const runRes = db.run(
                    `INSERT INTO fee_payments (student_id, month_year, amount, payment_status) VALUES (?, ?, ?, ?)`,
                    [student_id, month_year.trim(), parseFloat(amount), payment_status || 'Paid']
                );
                return sendJson(res, 201, { message: 'Payment recorded successfully', id: runRes.lastInsertRowid });
            }

            // Maintenance
            if (pathname === '/api/maintenance' && req.method === 'GET') {
                const issues = db.query(`
                    SELECT m.*, r.room_number, b.block_name
                    FROM maintenance_requests m
                    JOIN rooms r ON m.room_id = r.id
                    JOIN blocks b ON r.block_id = b.id
                    ORDER BY m.reported_at DESC
                `);
                return sendJson(res, 200, { issues });
            }

            if (pathname === '/api/maintenance' && req.method === 'POST') {
                const { room_id, issue_description, priority } = await parseBody(req);
                if (!room_id || !issue_description) {
                    return sendJson(res, 400, { error: 'Room ID and Description are required.' });
                }
                const runRes = db.run(
                    `INSERT INTO maintenance_requests (room_id, issue_description, priority, status) VALUES (?, ?, ?, 'Open')`,
                    [room_id, issue_description.trim(), priority || 'Medium']
                );
                return sendJson(res, 201, { message: 'Maintenance issue reported successfully', id: runRes.lastInsertRowid });
            }

            // Static Files
            let filePath = path.join(FRONTEND_DIR, pathname === '/' ? 'index.html' : pathname);
            if (fs.existsSync(filePath) && fs.statSync(filePath).isFile()) {
                const ext = path.extname(filePath).toLowerCase();
                const mime = { '.html': 'text/html', '.css': 'text/css', '.js': 'application/javascript', '.json': 'application/json' };
                res.writeHead(200, { 'Content-Type': mime[ext] || 'text/plain' });
                return fs.createReadStream(filePath).pipe(res);
            }

            return sendJson(res, 404, { error: 'Not found' });
        } catch (err) {
            console.error('Hostel Server Error:', err);
            return sendJson(res, 500, { error: err.message });
        }
    });
}

if (require.main === module) {
    const server = createHostelServer();
    server.listen(PORT, () => {
        console.log(`[+] UFTB Hostel Management System running at http://localhost:${PORT}`);
    });
}

module.exports = { createHostelServer };
