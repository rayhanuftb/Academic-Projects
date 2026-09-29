const test = require('node:test');
const assert = require('node:assert');
const path = require('node:path');
const fs = require('node:fs');
const { DatabaseManager } = require('../database/db');
const { createServer } = require('../backend/server');
const { seedDatabase } = require('../database/seed');

const TEST_DB_PATH = path.join(__dirname, 'test_classroom.db');

test('Cloud Classroom Platform Test Suite', async (t) => {
    // 1. Setup fresh test database
    if (fs.existsSync(TEST_DB_PATH)) {
        try { fs.unlinkSync(TEST_DB_PATH); } catch (_) {}
    }
    const db = new DatabaseManager(TEST_DB_PATH);
    seedDatabase(TEST_DB_PATH);

    const server = createServer(db);
    await new Promise((resolve) => server.listen(0, resolve));
    const port = server.address().port;
    const baseUrl = `http://localhost:${port}/api`;

    let studentToken = null;
    let instructorToken = null;
    let createdCourseId = null;
    let sampleQuizId = null;

    t.after(() => {
        try { server.close(); } catch (_) {}
        try { db.close(); } catch (_) {}
        try {
            if (fs.existsSync(TEST_DB_PATH)) fs.unlinkSync(TEST_DB_PATH);
        } catch (_) {}
    });

    // Helper request function
    async function request(url, options = {}) {
        const headers = options.headers || {};
        if (options.body && typeof options.body === 'object') {
            headers['Content-Type'] = 'application/json';
            options.body = JSON.stringify(options.body);
        }
        options.headers = headers;
        const res = await fetch(`${baseUrl}${url}`, options);
        const data = await res.json();
        return { status: res.status, data };
    }

    await t.test('1. Should login with demo student account', async () => {
        const res = await request('/auth/login', {
            method: 'POST',
            body: { email: 'student@uftb.edu.bd', password: 'Student@123' }
        });
        assert.strictEqual(res.status, 200);
        assert.ok(res.data.token);
        assert.strictEqual(res.data.user.role, 'student');
        studentToken = res.data.token;
    });

    await t.test('2. Should login with demo instructor account', async () => {
        const res = await request('/auth/login', {
            method: 'POST',
            body: { email: 'instructor@uftb.edu.bd', password: 'Instructor@123' }
        });
        assert.strictEqual(res.status, 200);
        assert.ok(res.data.token);
        assert.strictEqual(res.data.user.role, 'instructor');
        instructorToken = res.data.token;
    });

    await t.test('3. Should register a new student account', async () => {
        const res = await request('/auth/register', {
            method: 'POST',
            body: {
                name: 'New Test User',
                email: 'newuser@uftb.edu.bd',
                password: 'Password@123',
                role: 'student'
            }
        });
        assert.strictEqual(res.status, 201);
        assert.ok(res.data.token);
        assert.strictEqual(res.data.user.email, 'newuser@uftb.edu.bd');
    });

    await t.test('4. Instructor can create a new course', async () => {
        const res = await request('/courses', {
            method: 'POST',
            headers: { Authorization: `Bearer ${instructorToken}` },
            body: {
                code: 'ICTE 4499',
                title: 'Educational Machine Learning & Deep Learning',
                category: 'AI in Education',
                description: 'Advanced neural network applications in modern pedagogical systems.'
            }
        });
        assert.strictEqual(res.status, 201);
        assert.ok(res.data.courseId);
        createdCourseId = res.data.courseId;
    });

    await t.test('5. Non-instructor cannot create a course (RBAC check)', async () => {
        const res = await request('/courses', {
            method: 'POST',
            headers: { Authorization: `Bearer ${studentToken}` },
            body: {
                code: 'FAIL 101',
                title: 'Unauthorized Course'
            }
        });
        assert.strictEqual(res.status, 403);
    });

    await t.test('6. Student can enroll in the created course', async () => {
        const res = await request(`/courses/${createdCourseId}/enroll`, {
            method: 'POST',
            headers: { Authorization: `Bearer ${studentToken}` }
        });
        assert.strictEqual(res.status, 201);
    });

    await t.test('7. Instructor creates a lesson for the course', async () => {
        const res = await request('/lessons', {
            method: 'POST',
            headers: { Authorization: `Bearer ${instructorToken}` },
            body: {
                course_id: createdCourseId,
                title: 'Neural Networks Basics in Educational Data Mining',
                content: 'Introduction to perceptrons, backpropagation, and loss functions.',
                resource_url: 'https://en.wikipedia.org/wiki/Artificial_neural_network',
                sequence_order: 1
            }
        });
        assert.strictEqual(res.status, 201);
        assert.ok(res.data.lessonId);

        // Student marks lesson completed
        const compRes = await request(`/lessons/${res.data.lessonId}/complete`, {
            method: 'POST',
            headers: { Authorization: `Bearer ${studentToken}` }
        });
        assert.strictEqual(compRes.status, 200);
    });

    await t.test('8. Instructor creates an assignment and student submits', async () => {
        const assignRes = await request('/assignments', {
            method: 'POST',
            headers: { Authorization: `Bearer ${instructorToken}` },
            body: {
                course_id: createdCourseId,
                title: 'Neural Network Loss Function Exercise',
                description: 'Implement binary cross-entropy and compute loss for 5 samples.',
                max_score: 50,
                due_date: '2026-11-01'
            }
        });
        assert.strictEqual(assignRes.status, 201);
        const assignId = assignRes.data.assignmentId;

        // Submit assignment
        const subRes = await request(`/assignments/${assignId}/submit`, {
            method: 'POST',
            headers: { Authorization: `Bearer ${studentToken}` },
            body: {
                submission_text: 'Binary cross entropy equation implemented with logarithmic penalty function.'
            }
        });
        assert.strictEqual(subRes.status, 201);
    });

    await t.test('9. Quiz creation and objective automated grading', async () => {
        const quizRes = await request('/quizzes', {
            method: 'POST',
            headers: { Authorization: `Bearer ${instructorToken}` },
            body: {
                course_id: createdCourseId,
                title: 'Quick Check: Activation Functions',
                description: '2 question test on ReLU and Sigmoid functions.',
                time_limit_mins: 10,
                questions: [
                    {
                        question_text: 'Which activation function outputs values in range (0, 1)?',
                        option_a: 'ReLU',
                        option_b: 'Sigmoid',
                        option_c: 'Linear',
                        option_d: 'Step',
                        correct_option: 'B',
                        points: 10
                    },
                    {
                        question_text: 'What does ReLU stand for?',
                        option_a: 'Rectified Linear Unit',
                        option_b: 'Recursive Learning Utility',
                        option_c: 'Residual Layer Unit',
                        option_d: 'Regularized Loss Unit',
                        correct_option: 'A',
                        points: 10
                    }
                ]
            }
        });
        assert.strictEqual(quizRes.status, 201);
        sampleQuizId = quizRes.data.quizId;

        // Fetch quiz questions (ensure answers are not leaked)
        const fetchRes = await request(`/quizzes/${sampleQuizId}`, {
            headers: { Authorization: `Bearer ${studentToken}` }
        });
        assert.strictEqual(fetchRes.status, 200);
        assert.strictEqual(fetchRes.data.questions.length, 2);
        assert.strictEqual(fetchRes.data.questions[0].correct_option, undefined); // Not leaked

        const q1Id = fetchRes.data.questions[0].id;
        const q2Id = fetchRes.data.questions[1].id;

        // Submit quiz: 1 correct (B), 1 wrong (C) -> Score should be 10/20 (50%)
        const answers = {};
        answers[q1Id] = 'B';
        answers[q2Id] = 'C';

        const submitRes = await request(`/quizzes/${sampleQuizId}/submit`, {
            method: 'POST',
            headers: { Authorization: `Bearer ${studentToken}` },
            body: { answers }
        });

        assert.strictEqual(submitRes.status, 200);
        assert.strictEqual(submitRes.data.score, 10);
        assert.strictEqual(submitRes.data.max_score, 20);
        assert.strictEqual(submitRes.data.percentage, 50);
        assert.strictEqual(submitRes.data.breakdown.length, 2);
    });

    await t.test('10. Student dashboard aggregates enrolled courses & progress', async () => {
        const dashRes = await request('/student/dashboard', {
            headers: { Authorization: `Bearer ${studentToken}` }
        });
        assert.strictEqual(dashRes.status, 200);
        assert.ok(dashRes.data.enrolledCourses.length >= 1);
        assert.ok(dashRes.data.recentQuizResults.length >= 1);
    });
});
