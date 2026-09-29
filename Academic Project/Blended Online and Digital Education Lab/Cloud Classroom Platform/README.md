# Cloud Classroom Platform

**Course:** Blended Online and Digital Education Lab (ICTE 4332)  
**Academic Program:** B.Sc. in Educational Technology and Engineering  
**Institution:** University of Frontier Technology, Bangladesh  
**Author:** Rayhanul Islam

---

## 📌 Project Overview

The **Cloud Classroom Platform** is a responsive, full-stack educational learning management system engineered for blended, synchronous, and asynchronous digital learning environments. It provides role-based workspaces for **Students** and **Instructors**, allowing interactive course delivery, multimedia lesson progression, assignment submissions, objective quiz auto-grading, and real-time student analytics.

---

## 🎯 Key Features

### 👨‍🏫 Instructor Capabilities
- **Course Authoring**: Create, configure, and publish academic courses categorized by subject.
- **Lesson Management**: Publish modular multimedia lessons with sequential order, rich text, and external video/document resource links.
- **Assessment Management**: Create assignments with maximum point criteria and deadlines.
- **Quiz Engine**: Design multi-question objective quizzes (Multiple Choice Questions) with custom points and automatic scoring logic.
- **Course Announcements**: Broadcast real-time announcements to enrolled students.
- **Submission Grading**: Review student assignment submissions and provide qualitative feedback with grades.

### 👩‍🎓 Student Capabilities
- **Course Catalog & Enrollment**: Browse public academic courses and enroll with one click.
- **Lesson Progression**: Access instructional modules, stream materials, and mark lessons completed to update progress bars dynamically.
- **Interactive Quizzes**: Take objective quizzes with instant automated scoring, pass/fail indicators, and question-by-question answer breakdowns.
- **Assignment Submissions**: Submit text or resource links directly to assignments before deadlines.
- **Learning Dashboard**: Track aggregate learning progress, active courses, completed lessons, and quiz score history.

### 🛡️ Security & Architecture
- **Cryptographic Password Security**: Uses salted `scrypt` key derivation with secure random salts.
- **Stateless Authentication**: Cryptographically signed HMAC-SHA256 tokens with role-based access control (RBAC).
- **Relational Data Persistence**: SQLite schema with foreign-key constraints, cascading deletes, and transactional integrity (`node:sqlite`).
- **Zero External Server Dependency**: Built natively on Node.js without requiring third-party cloud accounts or external database installations.

---

## 🏗️ Architecture & Directory Structure

```
Cloud Classroom Platform/
├── backend/
│   ├── server.js               # Node.js REST API & static web server
│   └── middleware/
│       └── auth.js             # scrypt password hashing & token authentication
├── database/
│   ├── db.js                   # SQLite database connector & manager
│   ├── schema.sql              # Relational database schema definition
│   ├── seed.js                 # Seed script with demo accounts & courses
│   └── classroom.db            # Persistent SQLite database file
├── frontend/
│   ├── index.html              # Responsive single-page application UI
│   ├── styles.css              # Modern CSS Grid/Flexbox styling
│   └── app.js                  # Client-side routing, API integration & state
├── tests/
│   └── api.test.js             # Automated end-to-end API & RBAC test suite
├── package.json
└── README.md
```

---

## 👥 Demo Accounts

The database comes pre-seeded with realistic demonstration accounts:

| Role | Email | Password | Pre-configured Data |
|---|---|---|---|
| **Instructor** | `instructor@uftb.edu.bd` | `Instructor@123` | ICTE 4332 & ICTE 4434 courses, 3 lessons, 1 assignment, 1 objective quiz |
| **Student** | `student@uftb.edu.bd` | `Student@123` | Enrolled in ICTE 4332 with 1 completed lesson |

*New student and instructor accounts can also be created on the registration page.*

---

## 🚀 Installation & Local Execution

### 1. Prerequisites
- Node.js v18+ (tested and optimized for Node.js v22/v24).

### 2. Seed Database with Demo Content
```bash
node database/seed.js
```

### 3. Start the Server
```bash
node backend/server.js
```
*(Or `npm start`)*

Open your browser and navigate to:
```
http://localhost:4000
```

---

## 🧪 Running Automated Tests

Run the native test suite covering authentication, RBAC, course creation, enrollment, lesson progress, assignment submission, and quiz grading:

```bash
npm test
```
or
```bash
node --test tests/api.test.js
```
