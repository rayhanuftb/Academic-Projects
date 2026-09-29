const path = require('node:path');
const { getDb } = require('./db');
const { hashPassword } = require('../backend/middleware/auth');

function seedDatabase(dbPath) {
    const db = getDb(dbPath);

    console.log('[+] Initializing database tables and seed data...');

    // Clear existing data for fresh seed
    db.exec(`
        DELETE FROM quiz_submissions;
        DELETE FROM quiz_questions;
        DELETE FROM quizzes;
        DELETE FROM submissions;
        DELETE FROM assignments;
        DELETE FROM announcements;
        DELETE FROM lesson_progress;
        DELETE FROM lessons;
        DELETE FROM enrollments;
        DELETE FROM courses;
        DELETE FROM users;
    `);

    // 1. Insert Demo Users
    const instPwd = hashPassword('Instructor@123');
    const studPwd = hashPassword('Student@123');

    db.run(
        `INSERT INTO users (name, email, password_hash, salt, role) VALUES (?, ?, ?, ?, ?)`,
        ['Prof. Dr. Rahman (Demo Instructor)', 'instructor@uftb.edu.bd', instPwd.hash, instPwd.salt, 'instructor']
    );
    const instructorId = db.get(`SELECT id FROM users WHERE email = ?`, ['instructor@uftb.edu.bd']).id;

    db.run(
        `INSERT INTO users (name, email, password_hash, salt, role) VALUES (?, ?, ?, ?, ?)`,
        ['Rayhanul Islam (Demo Student)', 'student@uftb.edu.bd', studPwd.hash, studPwd.salt, 'student']
    );
    const studentId = db.get(`SELECT id FROM users WHERE email = ?`, ['student@uftb.edu.bd']).id;

    // 2. Insert Demo Courses
    db.run(
        `INSERT INTO courses (code, title, description, instructor_id, category) VALUES (?, ?, ?, ?, ?)`,
        [
            'ICTE 4332',
            'Blended, Online and Digital Education',
            'Pedagogical frameworks, LMS architectures, instructional design, and cloud-delivered educational platforms.',
            instructorId,
            'Educational Technology'
        ]
    );
    const courseId1 = db.get(`SELECT id FROM courses WHERE code = ?`, ['ICTE 4332']).id;

    db.run(
        `INSERT INTO courses (code, title, description, instructor_id, category) VALUES (?, ?, ?, ?, ?)`,
        [
            'ICTE 4434',
            'Big Data and Analytics in Education',
            'Learning analytics, predictive modeling, NLP text mining, and longitudinal student performance tracking.',
            instructorId,
            'Data Science'
        ]
    );
    const courseId2 = db.get(`SELECT id FROM courses WHERE code = ?`, ['ICTE 4434']).id;

    // 3. Enroll Student in Course 1
    db.run(
        `INSERT INTO enrollments (course_id, student_id) VALUES (?, ?)`,
        [courseId1, studentId]
    );

    // 4. Insert Lessons for Course 1
    db.run(
        `INSERT INTO lessons (course_id, title, content, resource_url, sequence_order) VALUES (?, ?, ?, ?, ?)`,
        [
            courseId1,
            'Module 1: Foundations of Blended Learning Environments',
            'Understanding synchronous vs asynchronous learning modalities, community of inquiry framework, and multimedia learning theory.',
            'https://en.wikipedia.org/wiki/Blended_learning',
            1
        ]
    );
    const lessonId1 = db.get(`SELECT id FROM lessons WHERE course_id = ? AND sequence_order = 1`, [courseId1]).id;

    db.run(
        `INSERT INTO lessons (course_id, title, content, resource_url, sequence_order) VALUES (?, ?, ?, ?, ?)`,
        [
            courseId1,
            'Module 2: Cloud Architectures in Education (LMS & SaaS)',
            'Exploration of microservices, database persistence, RESTful APIs, and scalable cloud hosting for modern education.',
            'https://aws.amazon.com/education/',
            2
        ]
    );

    db.run(
        `INSERT INTO lessons (course_id, title, content, resource_url, sequence_order) VALUES (?, ?, ?, ?, ?)`,
        [
            courseId1,
            'Module 3: Assessment Design & Learning Analytics',
            'Formative vs summative automated evaluation, rubric structures, and real-time student mastery dashboards.',
            'https://www.solaresearch.org/about/what-is-learning-analytics/',
            3
        ]
    );

    // Mark lesson 1 completed for student
    db.run(
        `INSERT INTO lesson_progress (lesson_id, student_id, completed) VALUES (?, ?, 1)`,
        [lessonId1, studentId]
    );

    // 5. Insert Announcements
    db.run(
        `INSERT INTO announcements (course_id, title, content) VALUES (?, ?, ?)`,
        [
            courseId1,
            'Welcome to Spring Semester 2026',
            'Please complete Module 1 readings before our upcoming interactive seminar on cloud architecture.'
        ]
    );

    // 6. Insert Assignment
    db.run(
        `INSERT INTO assignments (course_id, title, description, max_score, due_date) VALUES (?, ?, ?, ?, ?)`,
        [
            courseId1,
            'Laboratory Assignment: LMS Architecture Design',
            'Submit a detailed architectural diagram and 500-word design rationale describing a scalable cloud classroom platform.',
            100,
            '2026-10-15'
        ]
    );

    // 7. Insert Quiz and Objective Questions
    db.run(
        `INSERT INTO quizzes (course_id, title, description, time_limit_mins) VALUES (?, ?, ?, ?)`,
        [
            courseId1,
            'Quiz 1: Blended Learning & Cloud Fundamentals',
            'Objective 4-question assessment testing core concepts of digital pedagogy and cloud delivery.',
            15
        ]
    );
    const quizId = db.get(`SELECT id FROM quizzes WHERE course_id = ?`, [courseId1]).id;

    db.run(
        `INSERT INTO quiz_questions (quiz_id, question_text, option_a, option_b, option_c, option_d, correct_option, points) VALUES (?, ?, ?, ?, ?, ?, ?, ?)`,
        [
            quizId,
            'What is the primary definition of blended learning?',
            '100% face-to-face traditional lecturing',
            'Combining online digital media with traditional classroom instruction',
            'Only self-paced video streaming without instructor interaction',
            'Replacing teachers entirely with AI agents',
            'B',
            25
        ]
    );

    db.run(
        `INSERT INTO quiz_questions (quiz_id, question_text, option_a, option_b, option_c, option_d, correct_option, points) VALUES (?, ?, ?, ?, ?, ?, ?, ?)`,
        [
            quizId,
            'Which architectural model allows educational apps to scale dynamically based on student traffic?',
            'Monolithic desktop application',
            'Flat file text storage on local hard drives',
            'Cloud-based microservices and auto-scaling REST APIs',
            'Static HTML files on CD-ROM',
            'C',
            25
        ]
    );

    db.run(
        `INSERT INTO quiz_questions (quiz_id, question_text, option_a, option_b, option_c, option_d, correct_option, points) VALUES (?, ?, ?, ?, ?, ?, ?, ?)`,
        [
            quizId,
            'Which cryptographic method is essential for storing user passwords securely in an LMS database?',
            'Plain text storage in SQLite',
            'Salted one-way cryptographic hashing (e.g., scrypt/bcrypt)',
            'Base64 simple reversible encoding',
            'Storing passwords in browser localStorage without encryption',
            'B',
            25
        ]
    );

    db.run(
        `INSERT INTO quiz_questions (quiz_id, question_text, option_a, option_b, option_c, option_d, correct_option, points) VALUES (?, ?, ?, ?, ?, ?, ?, ?)`,
        [
            quizId,
            'What is the main goal of Learning Analytics in higher education?',
            'Measuring, collecting, and analyzing data about learners to optimize learning and environments',
            'Deleting student records periodically',
            'Selling student information to advertising networks',
            'Locking down internet access completely',
            'A',
            25
        ]
    );

    console.log('[+] Database seed completed successfully.');
    console.log('    Demo Instructor: instructor@uftb.edu.bd / Instructor@123');
    console.log('    Demo Student   : student@uftb.edu.bd    / Student@123');
}

if (require.main === module) {
    seedDatabase();
}

module.exports = { seedDatabase };
