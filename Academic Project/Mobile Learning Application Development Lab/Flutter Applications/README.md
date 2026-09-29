# Flutter Application Design and Development

> Academic Project / Practical Work

## 📚 Course Information

- **Course Title:** Mobile Learning Application Development Lab
- **Course Code:** ICT 4460
- **Student:** Rayhanul Islam
- **Institution:** University of Frontier Technology, Bangladesh

---

## 📌 Overview

A Flutter-based mobile learning application called "আভরণ শিখুন" (Abhoron Shikhun), designed to provide Bangladeshi students with an interactive mobile learning experience. The app features course browsing, interactive quizzes, bookmarking, and progress tracking.

---

## 🎯 Key Features

- **Home Dashboard:** Welcome screen with progress overview and popular courses
- **Course Catalog:** Browse available courses with difficulty levels and progress
- **Interactive Quiz:** Answer questions with immediate feedback and scoring
- **Bookmarks:** Save and manage favorite lessons
- **User Profile:** View statistics and app information
- **Responsive UI:** Material Design 3 with light/dark theme support
- **State Management:** Provider pattern for efficient state handling

---

## 🛠️ Technologies Used

- **Framework:** Flutter 3.x
- **Language:** Dart 3.x
- **State Management:** Provider 6.x
- **UI:** Material Design 3

---

## 📁 Project Structure

```
edu_bangla/
├── pubspec.yaml
├── lib/
│   ├── main.dart                    App entry point & navigation
│   ├── models/
│   │   └── models.dart              Data models (Course, Lesson, Quiz, Bookmark)
│   ├── providers/
│   │   └── learning_provider.dart   State management
│   └── screens/
│       ├── home_screen.dart         Dashboard & course grid
│       ├── courses_screen.dart      Course list with details
│       ├── quiz_screen.dart         Interactive quiz interface
│       ├── bookmarks_screen.dart    Saved bookmarks
│       └── profile_screen.dart      User profile & stats
├── assets/
│   └── images/
└── README.md
```

---

## 🚀 How to Run

### Prerequisites

- Flutter SDK 3.x installed
- Dart SDK 3.x
- Android Studio / VS Code with Flutter extension

### Installation

```bash
cd edu_bangla
flutter pub get
flutter run
```

### Build

```bash
# Android
flutter build apk

# iOS
flutter build ios
```

---

## 📱 Screens

1. **Home:** Welcome card, progress stats, popular courses grid
2. **Courses:** Full course list with difficulty badges and progress bars
3. **Quiz:** 6 questions with immediate feedback and scoring
4. **Bookmarks:** Saved lessons with remove functionality
5. **Profile:** User stats, about dialog, theme info

---

## 🎓 Academic Note

This project demonstrates practical skills in Flutter mobile application development, including UI design, state management, navigation, data modeling, and responsive layouts. It was developed as part of the Mobile Learning Application Development Lab coursework.

---

## 👤 Author

**Rayhanul Islam**  
Educational Technology and Engineering  
University of Frontier Technology, Bangladesh
