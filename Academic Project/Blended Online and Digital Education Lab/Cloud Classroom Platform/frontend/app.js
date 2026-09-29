// Cloud Classroom Platform Frontend Application Logic
const API_BASE = '/api';

let currentUser = null;
let currentToken = null;
let currentCourseId = null;

// Initialize App
document.addEventListener('DOMContentLoaded', () => {
    loadStoredAuth();
    switchView('landing');
    loadCourses();
});

// Toast notification system
function showToast(message, type = 'info') {
    const container = document.getElementById('toast-container');
    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    toast.textContent = message;
    container.appendChild(toast);
    setTimeout(() => {
        toast.remove();
    }, 4000);
}

// Auth State Management
function loadStoredAuth() {
    const token = localStorage.getItem('cc_token');
    const user = localStorage.getItem('cc_user');
    if (token && user) {
        currentToken = token;
        currentUser = JSON.parse(user);
        updateNavUserUI();
    }
}

function updateNavUserUI() {
    const authSection = document.getElementById('nav-auth-section');
    const userSection = document.getElementById('nav-user-section');
    const dashboardLink = document.getElementById('nav-dashboard-link');
    const catalogInstructorAction = document.getElementById('catalog-instructor-action');

    if (currentUser) {
        authSection.classList.add('hidden');
        userSection.classList.remove('hidden');
        dashboardLink.classList.remove('hidden');
        document.getElementById('nav-user-name').textContent = currentUser.name;
        document.getElementById('nav-user-role').textContent = currentUser.role;
        document.getElementById('nav-avatar').textContent = currentUser.name.charAt(0).toUpperCase();

        if (currentUser.role === 'instructor') {
            catalogInstructorAction?.classList.remove('hidden');
        } else {
            catalogInstructorAction?.classList.add('hidden');
        }
    } else {
        authSection.classList.remove('hidden');
        userSection.classList.add('hidden');
        dashboardLink.classList.add('hidden');
        catalogInstructorAction?.classList.add('hidden');
    }
}

function logout() {
    currentUser = null;
    currentToken = null;
    localStorage.removeItem('cc_token');
    localStorage.removeItem('cc_user');
    updateNavUserUI();
    showToast('Logged out successfully', 'info');
    switchView('landing');
}

// Modal management
function openModal(id) {
    document.getElementById(id)?.classList.remove('hidden');
}

function closeModal(id) {
    document.getElementById(id)?.classList.add('hidden');
}

function fillLoginForm(email, password) {
    document.getElementById('login-email').value = email;
    document.getElementById('login-password').value = password;
}

function fillDemoLogin(role) {
    openModal('login-modal');
    if (role === 'instructor') {
        fillLoginForm('instructor@uftb.edu.bd', 'Instructor@123');
    } else {
        fillLoginForm('student@uftb.edu.bd', 'Student@123');
    }
}

// View Routing
function switchView(viewName) {
    document.querySelectorAll('.app-view').forEach(el => el.classList.add('hidden'));
    const target = document.getElementById(`view-${viewName}`);
    if (target) {
        target.classList.remove('hidden');
        window.scrollTo(0, 0);
    }

    if (viewName === 'catalog') {
        loadCourses();
    } else if (viewName === 'dashboard') {
        if (!currentUser) {
            openModal('login-modal');
            showToast('Please sign in to access your dashboard.', 'info');
            switchView('landing');
            return;
        }
        loadDashboard();
    }
}

// API Helper
async function apiFetch(endpoint, options = {}) {
    const headers = options.headers || {};
    if (currentToken) {
        headers['Authorization'] = `Bearer ${currentToken}`;
    }
    if (options.body && typeof options.body === 'object' && !(options.body instanceof FormData)) {
        headers['Content-Type'] = 'application/json';
        options.body = JSON.stringify(options.body);
    }
    options.headers = headers;

    const res = await fetch(`${API_BASE}${endpoint}`, options);
    const data = await res.json();
    if (!res.ok) {
        throw new Error(data.error || 'Server request failed');
    }
    return data;
}

// Authentication Handlers
async function handleLogin(e) {
    e.preventDefault();
    const email = document.getElementById('login-email').value;
    const password = document.getElementById('login-password').value;

    try {
        const res = await apiFetch('/auth/login', {
            method: 'POST',
            body: { email, password }
        });
        currentUser = res.user;
        currentToken = res.token;
        localStorage.setItem('cc_token', currentToken);
        localStorage.setItem('cc_user', JSON.stringify(currentUser));
        updateNavUserUI();
        closeModal('login-modal');
        showToast(`Welcome back, ${currentUser.name}!`, 'success');
        switchView('dashboard');
    } catch (err) {
        showToast(err.message, 'error');
    }
}

async function handleRegister(e) {
    e.preventDefault();
    const name = document.getElementById('reg-name').value;
    const email = document.getElementById('reg-email').value;
    const password = document.getElementById('reg-password').value;
    const role = document.getElementById('reg-role').value;

    try {
        const res = await apiFetch('/auth/register', {
            method: 'POST',
            body: { name, email, password, role }
        });
        currentUser = res.user;
        currentToken = res.token;
        localStorage.setItem('cc_token', currentToken);
        localStorage.setItem('cc_user', JSON.stringify(currentUser));
        updateNavUserUI();
        closeModal('register-modal');
        showToast('Registration successful! Welcome to Cloud Classroom.', 'success');
        switchView('dashboard');
    } catch (err) {
        showToast(err.message, 'error');
    }
}

// Load Course Catalog
async function loadCourses() {
    const container = document.getElementById('course-cards-container');
    container.innerHTML = '<p>Loading courses...</p>';

    try {
        const res = await apiFetch('/courses');
        const courses = res.courses || [];
        if (courses.length === 0) {
            container.innerHTML = '<p>No courses available right now.</p>';
            return;
        }

        container.innerHTML = courses.map(c => `
            <div class="course-card">
                <span class="course-card-code">${escapeHtml(c.code)}</span>
                <h3 class="course-card-title">${escapeHtml(c.title)}</h3>
                <p class="course-card-desc">${escapeHtml(c.description || 'Comprehensive educational module.')}</p>
                <div class="course-card-footer">
                    <div class="course-card-meta">
                        👤 ${escapeHtml(c.instructor_name)}<br>
                        👥 ${c.enrolled_count} Students
                    </div>
                    <button class="btn btn-sm btn-primary" onclick="viewCourse(${c.id})">View Course</button>
                </div>
            </div>
        `).join('');
    } catch (err) {
        container.innerHTML = `<p class="toast-error">Failed to load courses: ${err.message}</p>`;
    }
}

// Load Dashboard
async function loadDashboard() {
    const title = document.getElementById('dashboard-title');
    const subtitle = document.getElementById('dashboard-subtitle');
    const statsContainer = document.getElementById('dashboard-stats-container');
    const contentArea = document.getElementById('dashboard-content-area');
    const instructorActions = document.getElementById('instructor-quick-actions');

    if (currentUser.role === 'instructor') {
        title.textContent = 'Instructor Dashboard';
        subtitle.textContent = 'Manage your created courses, learning materials, and student submissions.';
        instructorActions.classList.remove('hidden');

        try {
            const res = await apiFetch('/courses');
            const myCourses = res.courses.filter(c => c.instructor_id === currentUser.id);

            statsContainer.innerHTML = `
                <div class="stat-card">
                    <div class="stat-value">${myCourses.length}</div>
                    <div class="stat-label">Active Courses</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">${myCourses.reduce((acc, c) => acc + c.enrolled_count, 0)}</div>
                    <div class="stat-label">Total Enrollments</div>
                </div>
            `;

            contentArea.innerHTML = `
                <h3 style="margin-bottom: 1rem;">Courses You Instruct</h3>
                <div class="course-grid">
                    ${myCourses.map(c => `
                        <div class="course-card">
                            <span class="course-card-code">${escapeHtml(c.code)}</span>
                            <h3 class="course-card-title">${escapeHtml(c.title)}</h3>
                            <p class="course-card-desc">${escapeHtml(c.description || '')}</p>
                            <div class="course-card-footer">
                                <span>👥 ${c.enrolled_count} Enrolled</span>
                                <button class="btn btn-sm btn-primary" onclick="viewCourse(${c.id})">Manage Course</button>
                            </div>
                        </div>
                    `).join('')}
                </div>
            `;
        } catch (err) {
            contentArea.innerHTML = `<p>Error loading dashboard: ${err.message}</p>`;
        }

    } else {
        // Student Dashboard
        title.textContent = 'Student Learning Dashboard';
        subtitle.textContent = 'Track your learning milestones, completed lessons, and quiz scores.';
        instructorActions.classList.add('hidden');

        try {
            const res = await apiFetch('/student/dashboard');
            const courses = res.enrolledCourses || [];
            const quizzes = res.recentQuizResults || [];

            const totalLessons = courses.reduce((acc, c) => acc + c.total_lessons, 0);
            const completedLessons = courses.reduce((acc, c) => acc + c.completed_lessons, 0);
            const overallPct = totalLessons > 0 ? Math.round((completedLessons / totalLessons) * 100) : 0;

            statsContainer.innerHTML = `
                <div class="stat-card">
                    <div class="stat-value">${courses.length}</div>
                    <div class="stat-label">Enrolled Courses</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">${overallPct}%</div>
                    <div class="stat-label">Overall Progress</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">${quizzes.length}</div>
                    <div class="stat-label">Quizzes Completed</div>
                </div>
            `;

            contentArea.innerHTML = `
                <h3 style="margin-bottom: 1rem;">My Enrolled Courses</h3>
                <div class="course-grid">
                    ${courses.length === 0 ? '<p>You are not enrolled in any courses yet. <a href="#" onclick="switchView(\'catalog\')">Browse catalog</a></p>' : ''}
                    ${courses.map(c => {
                        const pct = c.total_lessons > 0 ? Math.round((c.completed_lessons / c.total_lessons) * 100) : 0;
                        return `
                            <div class="course-card">
                                <span class="course-card-code">${escapeHtml(c.code)}</span>
                                <h3 class="course-card-title">${escapeHtml(c.title)}</h3>
                                <div class="progress-container">
                                    <div class="progress-bar-bg">
                                        <div class="progress-bar-fill" style="width: ${pct}%"></div>
                                    </div>
                                    <div class="progress-text">
                                        <span>Progress: ${c.completed_lessons}/${c.total_lessons} Lessons</span>
                                        <strong>${pct}%</strong>
                                    </div>
                                </div>
                                <div class="course-card-footer">
                                    <span>Instructor: ${escapeHtml(c.instructor_name)}</span>
                                    <button class="btn btn-sm btn-primary" onclick="viewCourse(${c.id})">Continue Learning</button>
                                </div>
                            </div>
                        `;
                    }).join('')}
                </div>
            `;
        } catch (err) {
            contentArea.innerHTML = `<p>Error loading dashboard: ${err.message}</p>`;
        }
    }
}

// Course Detail View
async function viewCourse(courseId) {
    currentCourseId = courseId;
    switchView('course-detail');

    try {
        const res = await apiFetch(`/courses/${courseId}`);
        const c = res.course;

        document.getElementById('cd-code').textContent = c.code;
        document.getElementById('cd-title').textContent = c.title;
        document.getElementById('cd-desc').textContent = c.description || '';
        document.getElementById('cd-instructor').textContent = c.instructor_name;

        // Render Enrollment Button / Status
        const enrollStatus = document.getElementById('cd-enrollment-status');
        if (currentUser && currentUser.role === 'student') {
            enrollStatus.innerHTML = `<button class="btn btn-sm btn-primary" onclick="enrollInCurrentCourse()">Enroll in Course</button>`;
        } else {
            enrollStatus.innerHTML = '';
        }

        // Render Lessons
        const lessonsCont = document.getElementById('cd-lessons-container');
        if (res.lessons.length === 0) {
            lessonsCont.innerHTML = '<p>No lessons published yet.</p>';
        } else {
            lessonsCont.innerHTML = res.lessons.map((l, idx) => `
                <div class="item-card">
                    <div class="item-card-header">
                        <span class="item-card-title">${idx + 1}. ${escapeHtml(l.title)}</span>
                        ${currentUser && currentUser.role === 'student' ? `
                            <button class="btn btn-sm btn-outline" onclick="markLessonComplete(${l.id})">✓ Mark Completed</button>
                        ` : ''}
                    </div>
                    <p style="color: var(--text-muted); margin-bottom: 0.75rem;">${escapeHtml(l.content || '')}</p>
                    ${l.resource_url ? `<p>🔗 <a href="${escapeHtml(l.resource_url)}" target="_blank" rel="noopener">Learning Resource Link</a></p>` : ''}
                </div>
            `).join('');
        }

        // Render Quizzes
        const quizzesCont = document.getElementById('cd-quizzes-container');
        if (res.quizzes.length === 0) {
            quizzesCont.innerHTML = '<p>No quizzes available for this course.</p>';
        } else {
            quizzesCont.innerHTML = res.quizzes.map(q => `
                <div class="item-card">
                    <div class="item-card-header">
                        <span class="item-card-title">📝 ${escapeHtml(q.title)}</span>
                        <button class="btn btn-sm btn-primary" onclick="startQuiz(${q.id})">Take Quiz</button>
                    </div>
                    <p style="color: var(--text-muted);">${escapeHtml(q.description || '')}</p>
                    <small>⏱️ Time Limit: ${q.time_limit_mins} minutes</small>
                </div>
            `).join('');
        }

        // Render Assignments
        const assignCont = document.getElementById('cd-assignments-container');
        if (res.assignments.length === 0) {
            assignCont.innerHTML = '<p>No assignments posted for this course.</p>';
        } else {
            assignCont.innerHTML = res.assignments.map(a => `
                <div class="item-card">
                    <div class="item-card-header">
                        <span class="item-card-title">📂 ${escapeHtml(a.title)}</span>
                        <span class="course-code-badge">Max Score: ${a.max_score}</span>
                    </div>
                    <p style="margin-bottom: 0.75rem;">${escapeHtml(a.description)}</p>
                    ${a.due_date ? `<small>📅 Due Date: ${escapeHtml(a.due_date)}</small>` : ''}
                    ${currentUser && currentUser.role === 'student' ? `
                        <div style="margin-top: 1rem;">
                            <textarea id="assign-sub-${a.id}" class="form-group" rows="2" placeholder="Write or paste your assignment submission..." style="width: 100%; margin-bottom: 0.5rem;"></textarea>
                            <button class="btn btn-sm btn-primary" onclick="submitAssignment(${a.id})">Submit Assignment</button>
                        </div>
                    ` : ''}
                </div>
            `).join('');
        }

        // Render Announcements
        const annCont = document.getElementById('cd-announcements-container');
        if (res.announcements.length === 0) {
            annCont.innerHTML = '<p>No announcements published yet.</p>';
        } else {
            annCont.innerHTML = res.announcements.map(ann => `
                <div class="item-card">
                    <div class="item-card-header">
                        <span class="item-card-title">📢 ${escapeHtml(ann.title)}</span>
                        <small style="color: var(--text-muted);">${ann.posted_at}</small>
                    </div>
                    <p>${escapeHtml(ann.content)}</p>
                </div>
            `).join('');
        }

    } catch (err) {
        showToast(err.message, 'error');
    }
}

function switchCourseTab(tabName) {
    document.querySelectorAll('.course-tab-content').forEach(el => el.classList.add('hidden'));
    document.querySelectorAll('.course-tabs .tab-btn').forEach(b => b.classList.remove('active'));
    document.getElementById(`tab-${tabName}`)?.classList.remove('hidden');
    event.target.classList.add('active');
}

async function enrollInCurrentCourse() {
    if (!currentUser) return openModal('login-modal');
    try {
        const res = await apiFetch(`/courses/${currentCourseId}/enroll`, { method: 'POST' });
        showToast(res.message, 'success');
        viewCourse(currentCourseId);
    } catch (err) {
        showToast(err.message, 'info');
    }
}

async function markLessonComplete(lessonId) {
    try {
        const res = await apiFetch(`/lessons/${lessonId}/complete`, { method: 'POST' });
        showToast(res.message, 'success');
    } catch (err) {
        showToast(err.message, 'error');
    }
}

async function submitAssignment(assignmentId) {
    const textarea = document.getElementById(`assign-sub-${assignmentId}`);
    const text = textarea ? textarea.value : '';
    if (!text.trim()) {
        return showToast('Please enter your submission content before submitting.', 'error');
    }

    try {
        const res = await apiFetch(`/assignments/${assignmentId}/submit`, {
            method: 'POST',
            body: { submission_text: text }
        });
        showToast(res.message, 'success');
        textarea.value = '';
    } catch (err) {
        showToast(err.message, 'error');
    }
}

// Start Quiz Module
async function startQuiz(quizId) {
    if (!currentUser) {
        openModal('login-modal');
        return showToast('Please sign in to take the quiz.', 'info');
    }

    try {
        const res = await apiFetch(`/quizzes/${quizId}`);
        const q = res.quiz;
        const questions = res.questions;

        document.getElementById('quiz-modal-title').textContent = q.title;
        const body = document.getElementById('quiz-modal-body');

        body.innerHTML = `
            <form id="active-quiz-form" onsubmit="submitQuizAnswers(event, ${quizId})">
                ${questions.map((item, idx) => `
                    <div class="quiz-question-box">
                        <div class="quiz-q-title">${idx + 1}. ${escapeHtml(item.question_text)} (${item.points} pt)</div>
                        <div class="quiz-options">
                            <label class="quiz-opt-label">
                                <input type="radio" name="q_${item.id}" value="A" required> A) ${escapeHtml(item.option_a)}
                            </label>
                            <label class="quiz-opt-label">
                                <input type="radio" name="q_${item.id}" value="B"> B) ${escapeHtml(item.option_b)}
                            </label>
                            <label class="quiz-opt-label">
                                <input type="radio" name="q_${item.id}" value="C"> C) ${escapeHtml(item.option_c)}
                            </label>
                            <label class="quiz-opt-label">
                                <input type="radio" name="q_${item.id}" value="D"> D) ${escapeHtml(item.option_d)}
                            </label>
                        </div>
                    </div>
                `).join('')}
                <button type="submit" class="btn btn-primary btn-block">Submit Quiz for Automatic Grading</button>
            </form>
        `;
        openModal('quiz-modal');
    } catch (err) {
        showToast(err.message, 'error');
    }
}

async function submitQuizAnswers(e, quizId) {
    e.preventDefault();
    const form = e.target;
    const formData = new FormData(form);
    const answers = {};

    for (let [k, v] of formData.entries()) {
        const qId = k.replace('q_', '');
        answers[qId] = v;
    }

    try {
        const res = await apiFetch(`/quizzes/${quizId}/submit`, {
            method: 'POST',
            body: { answers }
        });

        const body = document.getElementById('quiz-modal-body');
        const isPassed = res.percentage >= 70;

        body.innerHTML = `
            <div style="text-align: center; padding: 1.5rem 0;">
                <div style="font-size: 3rem; margin-bottom: 0.5rem;">${isPassed ? '🎉' : '📚'}</div>
                <h2>Quiz Score: ${res.score} / ${res.max_score} (${res.percentage}%)</h2>
                <p style="color: var(--text-muted); margin: 0.75rem 0;">${isPassed ? 'Great job! You demonstrated mastery of this module.' : 'Review the course module materials and try again.'}</p>
                <hr style="margin: 1.5rem 0;">
                <h4 style="margin-bottom: 1rem; text-align: left;">Detailed Question Breakdown:</h4>
                <div style="text-align: left;">
                    ${res.breakdown.map((b, idx) => `
                        <div style="padding: 0.5rem 0; border-bottom: 1px solid var(--border);">
                            <strong>Question ${idx + 1}:</strong> ${b.is_correct ? '✅ Correct' : '❌ Incorrect'}
                            <br><small>Your Answer: Option ${b.selected || 'None'} | Correct Option: Option ${b.correct_option}</small>
                        </div>
                    `).join('')}
                </div>
                <button class="btn btn-primary" style="margin-top: 1.5rem;" onclick="closeModal('quiz-modal'); switchView('dashboard');">Return to Dashboard</button>
            </div>
        `;
        showToast('Quiz evaluated and submitted successfully!', 'success');
    } catch (err) {
        showToast(err.message, 'error');
    }
}

async function handleCreateCourse(e) {
    e.preventDefault();
    const code = document.getElementById('cc-code').value;
    const title = document.getElementById('cc-title').value;
    const category = document.getElementById('cc-category').value;
    const description = document.getElementById('cc-desc').value;

    try {
        const res = await apiFetch('/courses', {
            method: 'POST',
            body: { code, title, category, description }
        });
        showToast(res.message, 'success');
        closeModal('create-course-modal');
        switchView('dashboard');
    } catch (err) {
        showToast(err.message, 'error');
    }
}

function escapeHtml(str) {
    if (!str) return '';
    return String(str)
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#039;');
}
