const http = require('node:http');
const fs = require('node:fs');
const path = require('node:path');
const { getDb } = require('../database/db');
const { hashPassword, verifyPassword, generateToken, verifyToken } = require('./middleware/auth');

const PORT = process.env.PORT || 4000;
const FRONTEND_DIR = path.join(__dirname, '..', 'frontend');

// Helper to parse JSON request body
function parseBody(req) {
    return new Promise((resolve, reject) => {
        let body = '';
        req.on('data', chunk => {
            body += chunk;
            if (body.length > 2 * 1024 * 1024) {
                reject(new Error('Payload Too Large'));
            }
        });
        req.on('end', () => {
            if (!body) return resolve({});
            try {
                resolve(JSON.parse(body));
            } catch (err) {
                reject(new Error('Invalid JSON format'));
            }
        });
        req.on('error', reject);
    });
}

// JSON response helper
function sendJson(res, statusCode, data) {
    res.writeHead(statusCode, {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type, Authorization'
    });
    res.end(JSON.stringify(data));
}

// Auth extraction helper
function getAuthUser(req) {
    const authHeader = req.headers['authorization'];
    if (!authHeader || !authHeader.startsWith('Bearer ')) return null;
    return verifyToken(authHeader.substring(7));
}

function createServer(dbInstance) {
    const db = dbInstance || getDb();

    return http.createServer(async (req, res) => {
        // Handle CORS Preflight
        if (req.method === 'OPTIONS') {
            res.writeHead(204, {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type, Authorization'
            });
            return res.end();
        }

        const url = new URL(req.url, `http://${req.headers.host || 'localhost'}`);
        const pathname = url.pathname;

        try {
            // ==========================================
            // AUTHENTICATION ROUTES
            // ==========================================
            if (pathname === '/api/auth/register' && req.method === 'POST') {
                const { name, email, password, role } = await parseBody(req);
                if (!name || !email || !password) {
                    return sendJson(res, 400, { error: 'Name, email, and password are required.' });
                }
                const normalizedEmail = email.trim().toLowerCase();
                const userRole = role === 'instructor' ? 'instructor' : 'student';

                const existing = db.get(`SELECT id FROM users WHERE email = ?`, [normalizedEmail]);
                if (existing) {
                    return sendJson(res, 409, { error: 'A user with this email already exists.' });
                }

                const { salt, hash } = hashPassword(password);
                const insertRes = db.run(
                    `INSERT INTO users (name, email, password_hash, salt, role) VALUES (?, ?, ?, ?, ?)`,
                    [name.trim(), normalizedEmail, hash, salt, userRole]
                );

                const userId = insertRes.lastInsertRowid;
                const token = generateToken({ id: userId, name: name.trim(), email: normalizedEmail, role: userRole });

                return sendJson(res, 201, {
                    message: 'Registration successful',
                    token,
                    user: { id: userId, name: name.trim(), email: normalizedEmail, role: userRole }
                });
            }

            if (pathname === '/api/auth/login' && req.method === 'POST') {
                const { email, password } = await parseBody(req);
                if (!email || !password) {
                    return sendJson(res, 400, { error: 'Email and password are required.' });
                }
                const normalizedEmail = email.trim().toLowerCase();
                const user = db.get(`SELECT * FROM users WHERE email = ?`, [normalizedEmail]);

                if (!user || !verifyPassword(password, user.password_hash, user.salt)) {
                    return sendJson(res, 401, { error: 'Invalid email or password.' });
                }

                const token = generateToken({ id: user.id, name: user.name, email: user.email, role: user.role });
                return sendJson(res, 200, {
                    message: 'Login successful',
                    token,
                    user: { id: user.id, name: user.name, email: user.email, role: user.role }
                });
            }

            if (pathname === '/api/auth/me' && req.method === 'GET') {
                const user = getAuthUser(req);
                if (!user) return sendJson(res, 401, { error: 'Unauthorized' });
                return sendJson(res, 200, { user });
            }

            // ==========================================
            // COURSES ROUTES
            // ==========================================
            if (pathname === '/api/courses' && req.method === 'GET') {
                const courses = db.query(`
                    SELECT c.*, u.name as instructor_name,
                    (SELECT COUNT(*) FROM enrollments WHERE course_id = c.id) as enrolled_count
                    FROM courses c
                    JOIN users u ON c.instructor_id = u.id
                    ORDER BY c.created_at DESC
                `);
                return sendJson(res, 200, { courses });
            }

            if (pathname === '/api/courses' && req.method === 'POST') {
                const user = getAuthUser(req);
                if (!user || user.role !== 'instructor') {
                    return sendJson(res, 403, { error: 'Only instructors can create courses.' });
                }
                const { code, title, description, category } = await parseBody(req);
                if (!code || !title) {
                    return sendJson(res, 400, { error: 'Course code and title are required.' });
                }
                const runRes = db.run(
                    `INSERT INTO courses (code, title, description, instructor_id, category) VALUES (?, ?, ?, ?, ?)`,
                    [code.trim(), title.trim(), description || '', user.id, category || 'Educational Technology']
                );
                return sendJson(res, 201, {
                    message: 'Course created successfully',
                    courseId: runRes.lastInsertRowid
                });
            }

            // Get single course details
            const courseMatch = pathname.match(/^\/api\/courses\/(\d+)$/);
            if (courseMatch && req.method === 'GET') {
                const courseId = parseInt(courseMatch[1]);
                const course = db.get(`
                    SELECT c.*, u.name as instructor_name,
                    (SELECT COUNT(*) FROM enrollments WHERE course_id = c.id) as enrolled_count
                    FROM courses c
                    JOIN users u ON c.instructor_id = u.id
                    WHERE c.id = ?
                `, [courseId]);

                if (!course) return sendJson(res, 404, { error: 'Course not found' });

                const lessons = db.query(`SELECT * FROM lessons WHERE course_id = ? ORDER BY sequence_order ASC`, [courseId]);
                const assignments = db.query(`SELECT * FROM assignments WHERE course_id = ? ORDER BY created_at DESC`, [courseId]);
                const quizzes = db.query(`SELECT id, course_id, title, description, time_limit_mins, created_at FROM quizzes WHERE course_id = ?`, [courseId]);
                const announcements = db.query(`SELECT * FROM announcements WHERE course_id = ? ORDER BY posted_at DESC`, [courseId]);

                return sendJson(res, 200, {
                    course,
                    lessons,
                    assignments,
                    quizzes,
                    announcements
                });
            }

            // Enroll in course
            const enrollMatch = pathname.match(/^\/api\/courses\/(\d+)\/enroll$/);
            if (enrollMatch && req.method === 'POST') {
                const user = getAuthUser(req);
                if (!user) return sendJson(res, 401, { error: 'Authentication required' });
                const courseId = parseInt(enrollMatch[1]);

                try {
                    db.run(`INSERT INTO enrollments (course_id, student_id) VALUES (?, ?)`, [courseId, user.id]);
                    return sendJson(res, 201, { message: 'Enrolled successfully in course' });
                } catch (err) {
                    return sendJson(res, 409, { error: 'Already enrolled in this course' });
                }
            }

            // Student Enrolled Courses & Progress Overview
            if (pathname === '/api/student/dashboard' && req.method === 'GET') {
                const user = getAuthUser(req);
                if (!user) return sendJson(res, 401, { error: 'Authentication required' });

                const enrolledCourses = db.query(`
                    SELECT c.*, u.name as instructor_name, e.enrolled_at,
                    (SELECT COUNT(*) FROM lessons WHERE course_id = c.id) as total_lessons,
                    (SELECT COUNT(*) FROM lesson_progress lp JOIN lessons l ON lp.lesson_id = l.id WHERE l.course_id = c.id AND lp.student_id = ? AND lp.completed = 1) as completed_lessons,
                    (SELECT COUNT(*) FROM assignments WHERE course_id = c.id) as total_assignments,
                    (SELECT COUNT(*) FROM submissions s JOIN assignments a ON s.assignment_id = a.id WHERE a.course_id = c.id AND s.student_id = ?) as submitted_assignments
                    FROM courses c
                    JOIN enrollments e ON c.id = e.course_id
                    JOIN users u ON c.instructor_id = u.id
                    WHERE e.student_id = ?
                `, [user.id, user.id, user.id]);

                const recentQuizResults = db.query(`
                    SELECT qs.*, q.title as quiz_title, c.code as course_code
                    FROM quiz_submissions qs
                    JOIN quizzes q ON qs.quiz_id = q.id
                    JOIN courses c ON q.course_id = c.id
                    WHERE qs.student_id = ?
                    ORDER BY qs.submitted_at DESC
                `, [user.id]);

                return sendJson(res, 200, {
                    enrolledCourses,
                    recentQuizResults
                });
            }

            // ==========================================
            // LESSONS & PROGRESS
            // ==========================================
            if (pathname === '/api/lessons' && req.method === 'POST') {
                const user = getAuthUser(req);
                if (!user || user.role !== 'instructor') {
                    return sendJson(res, 403, { error: 'Only instructors can create lessons.' });
                }
                const { course_id, title, content, resource_url, sequence_order } = await parseBody(req);
                if (!course_id || !title) {
                    return sendJson(res, 400, { error: 'Course ID and title are required.' });
                }

                const ins = db.run(
                    `INSERT INTO lessons (course_id, title, content, resource_url, sequence_order) VALUES (?, ?, ?, ?, ?)`,
                    [course_id, title.trim(), content || '', resource_url || '', sequence_order || 1]
                );
                return sendJson(res, 201, { message: 'Lesson created successfully', lessonId: ins.lastInsertRowid });
            }

            const completeLessonMatch = pathname.match(/^\/api\/lessons\/(\d+)\/complete$/);
            if (completeLessonMatch && req.method === 'POST') {
                const user = getAuthUser(req);
                if (!user) return sendJson(res, 401, { error: 'Authentication required' });
                const lessonId = parseInt(completeLessonMatch[1]);

                try {
                    db.run(
                        `INSERT INTO lesson_progress (lesson_id, student_id, completed) VALUES (?, ?, 1)
                         ON CONFLICT(lesson_id, student_id) DO UPDATE SET completed = 1, completed_at = CURRENT_TIMESTAMP`,
                        [lessonId, user.id]
                    );
                    return sendJson(res, 200, { message: 'Lesson marked as completed' });
                } catch (err) {
                    return sendJson(res, 500, { error: err.message });
                }
            }

            // ==========================================
            // ASSIGNMENTS & SUBMISSIONS
            // ==========================================
            if (pathname === '/api/assignments' && req.method === 'POST') {
                const user = getAuthUser(req);
                if (!user || user.role !== 'instructor') {
                    return sendJson(res, 403, { error: 'Only instructors can create assignments.' });
                }
                const { course_id, title, description, max_score, due_date } = await parseBody(req);
                if (!course_id || !title || !description) {
                    return sendJson(res, 400, { error: 'Course ID, title, and description are required.' });
                }

                const runRes = db.run(
                    `INSERT INTO assignments (course_id, title, description, max_score, due_date) VALUES (?, ?, ?, ?, ?)`,
                    [course_id, title.trim(), description.trim(), max_score || 100, due_date || '']
                );
                return sendJson(res, 201, { message: 'Assignment created successfully', assignmentId: runRes.lastInsertRowid });
            }

            const submitAssignmentMatch = pathname.match(/^\/api\/assignments\/(\d+)\/submit$/);
            if (submitAssignmentMatch && req.method === 'POST') {
                const user = getAuthUser(req);
                if (!user) return sendJson(res, 401, { error: 'Authentication required' });
                const assignmentId = parseInt(submitAssignmentMatch[1]);
                const { submission_text, resource_url } = await parseBody(req);

                if (!submission_text || !submission_text.trim()) {
                    return sendJson(res, 400, { error: 'Submission content cannot be empty.' });
                }

                try {
                    db.run(
                        `INSERT INTO submissions (assignment_id, student_id, submission_text, resource_url) VALUES (?, ?, ?, ?)
                         ON CONFLICT(assignment_id, student_id) DO UPDATE SET submission_text = excluded.submission_text, resource_url = excluded.resource_url, submitted_at = CURRENT_TIMESTAMP`,
                        [assignmentId, user.id, submission_text.trim(), resource_url || '']
                    );
                    return sendJson(res, 201, { message: 'Assignment submitted successfully' });
                } catch (err) {
                    return sendJson(res, 500, { error: err.message });
                }
            }

            // Instructor grade submission
            const gradeMatch = pathname.match(/^\/api\/submissions\/(\d+)\/grade$/);
            if (gradeMatch && req.method === 'POST') {
                const user = getAuthUser(req);
                if (!user || user.role !== 'instructor') {
                    return sendJson(res, 403, { error: 'Only instructors can grade assignments.' });
                }
                const submissionId = parseInt(gradeMatch[1]);
                const { score, feedback } = await parseBody(req);

                db.run(
                    `UPDATE submissions SET score = ?, feedback = ?, graded_at = CURRENT_TIMESTAMP WHERE id = ?`,
                    [score, feedback || '', submissionId]
                );
                return sendJson(res, 200, { message: 'Submission graded successfully' });
            }

            // ==========================================
            // QUIZZES & AUTOMATED SCORING
            // ==========================================
            if (pathname === '/api/quizzes' && req.method === 'POST') {
                const user = getAuthUser(req);
                if (!user || user.role !== 'instructor') {
                    return sendJson(res, 403, { error: 'Only instructors can create quizzes.' });
                }
                const { course_id, title, description, time_limit_mins, questions } = await parseBody(req);
                if (!course_id || !title || !questions || !Array.isArray(questions)) {
                    return sendJson(res, 400, { error: 'Course ID, title, and questions array are required.' });
                }

                const quizRes = db.run(
                    `INSERT INTO quizzes (course_id, title, description, time_limit_mins) VALUES (?, ?, ?, ?)`,
                    [course_id, title.trim(), description || '', time_limit_mins || 15]
                );
                const quizId = quizRes.lastInsertRowid;

                for (const q of questions) {
                    db.run(
                        `INSERT INTO quiz_questions (quiz_id, question_text, option_a, option_b, option_c, option_d, correct_option, points) VALUES (?, ?, ?, ?, ?, ?, ?, ?)`,
                        [quizId, q.question_text, q.option_a, q.option_b, q.option_c, q.option_d, q.correct_option.toUpperCase(), q.points || 1]
                    );
                }

                return sendJson(res, 201, { message: 'Quiz created successfully', quizId });
            }

            const quizDetailMatch = pathname.match(/^\/api\/quizzes\/(\d+)$/);
            if (quizDetailMatch && req.method === 'GET') {
                const quizId = parseInt(quizDetailMatch[1]);
                const quiz = db.get(`SELECT * FROM quizzes WHERE id = ?`, [quizId]);
                if (!quiz) return sendJson(res, 404, { error: 'Quiz not found' });

                // Return questions WITHOUT exposing correct_option to students
                const questions = db.query(`SELECT id, quiz_id, question_text, option_a, option_b, option_c, option_d, points FROM quiz_questions WHERE quiz_id = ?`, [quizId]);
                return sendJson(res, 200, { quiz, questions });
            }

            const quizSubmitMatch = pathname.match(/^\/api\/quizzes\/(\d+)\/submit$/);
            if (quizSubmitMatch && req.method === 'POST') {
                const user = getAuthUser(req);
                if (!user) return sendJson(res, 401, { error: 'Authentication required' });
                const quizId = parseInt(quizSubmitMatch[1]);
                const { answers } = await parseBody(req); // e.g. { questionId: 'B' }

                const questions = db.query(`SELECT id, correct_option, points FROM quiz_questions WHERE quiz_id = ?`, [quizId]);
                if (questions.length === 0) {
                    return sendJson(res, 400, { error: 'Quiz has no questions.' });
                }

                let earnedScore = 0;
                let maxScore = 0;
                const feedbackItems = [];

                for (const q of questions) {
                    const studentChoice = (answers && answers[q.id]) ? String(answers[q.id]).toUpperCase() : null;
                    const isCorrect = studentChoice === q.correct_option;
                    const pts = q.points || 1;
                    maxScore += pts;
                    if (isCorrect) earnedScore += pts;

                    feedbackItems.push({
                        question_id: q.id,
                        selected: studentChoice,
                        correct_option: q.correct_option,
                        is_correct: isCorrect,
                        points_earned: isCorrect ? pts : 0
                    });
                }

                const percentage = maxScore > 0 ? (earnedScore / maxScore) * 100 : 0;

                db.run(
                    `INSERT INTO quiz_submissions (quiz_id, student_id, score, max_score, percentage) VALUES (?, ?, ?, ?, ?)`,
                    [quizId, user.id, earnedScore, maxScore, Math.round(percentage * 10) / 10]
                );

                return sendJson(res, 200, {
                    message: 'Quiz submitted and auto-graded successfully',
                    score: earnedScore,
                    max_score: maxScore,
                    percentage: Math.round(percentage * 10) / 10,
                    breakdown: feedbackItems
                });
            }

            // ==========================================
            // ANNOUNCEMENTS
            // ==========================================
            if (pathname === '/api/announcements' && req.method === 'POST') {
                const user = getAuthUser(req);
                if (!user || user.role !== 'instructor') {
                    return sendJson(res, 403, { error: 'Only instructors can post announcements.' });
                }
                const { course_id, title, content } = await parseBody(req);
                if (!course_id || !title || !content) {
                    return sendJson(res, 400, { error: 'Course ID, title, and content are required.' });
                }
                const resAnn = db.run(
                    `INSERT INTO announcements (course_id, title, content) VALUES (?, ?, ?)`,
                    [course_id, title.trim(), content.trim()]
                );
                return sendJson(res, 201, { message: 'Announcement posted successfully', id: resAnn.lastInsertRowid });
            }

            // ==========================================
            // STATIC FRONTEND SERVING
            // ==========================================
            let filePath = path.join(FRONTEND_DIR, pathname === '/' ? 'index.html' : pathname);
            if (fs.existsSync(filePath) && fs.statSync(filePath).isFile()) {
                const ext = path.extname(filePath).toLowerCase();
                const mimeTypes = {
                    '.html': 'text/html; charset=utf-8',
                    '.css': 'text/css; charset=utf-8',
                    '.js': 'application/javascript; charset=utf-8',
                    '.json': 'application/json; charset=utf-8',
                    '.png': 'image/png',
                    '.svg': 'image/svg+xml'
                };
                res.writeHead(200, { 'Content-Type': mimeTypes[ext] || 'text/plain' });
                return fs.createReadStream(filePath).pipe(res);
            }

            // 404
            return sendJson(res, 404, { error: 'Endpoint or static resource not found' });

        } catch (err) {
            console.error('Server Internal Error:', err);
            return sendJson(res, 500, { error: err.message || 'Internal Server Error' });
        }
    });
}

// Start server if directly executed
if (require.main === module) {
    const server = createServer();
    server.listen(PORT, () => {
        console.log(`[+] Cloud Classroom Platform Server running on http://localhost:${PORT}`);
    });
}

module.exports = { createServer };
