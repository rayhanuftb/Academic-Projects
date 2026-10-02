# Future of Cardiac Care: Predicting Heart Disease with Machine Learning SafeRx AI

> Academic Project / Practical Work

## 📚 Course Information

- **Course Title:** Software Engineering, Testing and Quality Assurance Lab
- **Course Code:** ICT 4458
- **Student:** Rayhanul Islam
- **Institution:** University of Frontier Technology, Bangladesh

---

## ⚠️ IMPORTANT DISCLAIMER

This is an **EDUCATIONAL** software engineering project. It does **NOT** provide real medical advice and must **NOT** be used for clinical decision-making. The drug interaction data is limited and for demonstration only.

---

## 📌 Overview

SafeRx AI is an educational medication safety checker demonstrating software engineering principles, testing practices, and quality assurance. The project implements a modular Python application with drug interaction checking, allergy screening, and patient-specific contraindication analysis.

---

## 🎯 Learning Objectives

1. Apply software engineering principles to a real-world domain
2. Implement modular, testable code architecture
3. Write comprehensive unit tests
4. Practice input validation and error handling
5. Demonstrate quality assurance practices

---

## 🏗️ System Architecture

```
SafeRx AI
├── models.py              Data models (Medication, Patient, Alert)
├── safety_checker.py      Core safety checking engine
├── validation.py          Input validation module
└── __init__.py            Package initialization
```

### Key Design Patterns

- **Dataclass Models:** Clean, typed data structures
- **Enum Types:** Risk levels and severity classifications
- **Separation of Concerns:** Validation, models, and logic separated
- **Defensive Programming:** Input validation at boundaries

---

## 🛠️ Technologies Used

- **Language:** Python 3.10+
- **Testing:** pytest
- **Design:** Dataclasses, Enums, Type hints

---

## 📊 Features

| Feature | Description |
|---|---|
| Drug Interaction Check | Identifies known drug-drug interactions |
| Allergy Screening | Flags medications that conflict with patient allergies |
| Age-Based Warnings | Alerts for elderly patients |
| Pregnancy Checks | Identifies contraindicated medications |
| Organ Function | Adjusts for kidney/liver impairment |
| Risk Classification | LOW, MODERATE, HIGH, CRITICAL severity levels |

---

## 🚀 How to Run

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run Tests

```bash
pytest tests/ -v
```

---

## 🧪 Testing Strategy

- **Unit Tests:** Individual function testing
- **Edge Cases:** Empty inputs, boundary values
- **Integration:** Full safety check pipeline
- **Coverage:** Validation, models, and core logic

---

## 📁 Project Structure

```
SafeRx AI/
├── README.md
├── requirements.txt
├── src/
│   └── saferx/
│       ├── __init__.py
│       ├── models.py
│       ├── safety_checker.py
│       └── validation.py
└── tests/
    ├── test_validation.py
    └── test_safety_checker.py
```

---

## 🎓 Academic Note

This project demonstrates software engineering practices including modular design, input validation, comprehensive testing, documentation, and quality assurance. It was developed as part of the Software Engineering, Testing and Quality Assurance Lab coursework.

---

## 👤 Author

**Rayhanul Islam**  
Educational Technology and Engineering  
University of Frontier Technology, Bangladesh
