# Java Swing GUI Application

> Academic Project / Practical Work

## 📚 Course Information

- **Course Title:** Object Oriented Programming Lab
- **Course Code:** ICT 4252
- **Student:** Rayhanul Islam
- **Institution:** University of Frontier Technology, Bangladesh

---

## 📌 Overview

A Java Swing GUI application implementing a Student Management System. The project demonstrates core OOP concepts including encapsulation, inheritance, polymorphism, exception handling, and event-driven GUI programming.

---

## 🎯 OOP Concepts Demonstrated

| Concept | Implementation |
|---|---|
| **Encapsulation** | Private fields with getters/setters in `Student` class |
| **Inheritance** | `GraduateStudent` extends `Student` |
| **Polymorphism** | `GradeCalculator` interface with `StandardGradeCalculator` and `DetailedGradeCalculator` implementations |
| **Exception Handling** | Custom `StudentNotFoundException`, input validation, try-catch blocks |
| **Abstraction** | `GradeCalculator` interface, `StudentManager` class |
| **Event-Driven Programming** | ActionListener implementations for GUI buttons |

---

## 📁 Project Structure

```
Java Swing GUI Application/
├── README.md
├── src/
│   └── StudentManagementApp.java    Main application with all classes
├── tests/
│   └── StudentTest.java             JUnit tests for OOP classes
└── README.md
```

---

## 🚀 How to Compile and Run

### Compile

```bash
javac -d out src/StudentManagementApp.java
```

### Run

```bash
java -cp out StudentManagementApp
```

### Run Tests (requires JUnit 5)

```bash
javac -cp out:junit-5.jar tests/StudentTest.java
java -jar junit-platform-console-standalone.jar --class-path out:tests --select-class StudentTest
```

---

## ✨ Features

- Add, update, delete, and find students
- GPA validation with custom exceptions
- Grade calculation using polymorphic interface
- JTable display with auto-refresh
- Average GPA calculation
- Graduate vs Undergraduate student differentiation
- Confirmation dialogs for destructive actions

---

## 🎓 Academic Note

This project demonstrates practical application of object-oriented programming concepts including class design, inheritance hierarchies, interface-based polymorphism, custom exception handling, and Swing GUI development. It was developed as part of the Object Oriented Programming Lab coursework.

---

## 👤 Author

**Rayhanul Islam**  
Educational Technology and Engineering  
University of Frontier Technology, Bangladesh
