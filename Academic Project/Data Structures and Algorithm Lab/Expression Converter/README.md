# Expression Converter and Evaluator

**Course:** Data Structures and Algorithm Lab (ICT 4156)  
**Academic Program:** B.Sc. in Educational Technology and Engineering  
**Institution:** University of Frontier Technology, Bangladesh  
**Author:** Rayhanul Islam

---

## 📌 Project Overview

This project implements a complete stack-based **Expression Converter and Arithmetic Evaluator** in Python. It supports converting expressions between **Infix**, **Postfix (Reverse Polish Notation)**, and **Prefix (Polish Notation)** formats, and dynamically evaluating expressions following standard operator precedence, associativity rules, and bracket balancing.

---

## 🎯 Key Features & Algorithm Design

1. **Custom Stack Implementation (`src/stack.py`)**: LIFO data structure with $O(1)$ `push()`, `pop()`, `peek()`, `is_empty()`, and `size()` operations.
2. **Shunting-Yard Algorithm (`src/converter.py`)**: Converts Infix to Postfix and Prefix notations in linear $O(N)$ time.
3. **Operator Precedence & Associativity**:
   - `^` (Exponentiation): Precedence 3 (Right-Associative)
   - `*`, `/` (Multiplication & Division): Precedence 2 (Left-Associative)
   - `+`, `-` (Addition & Subtraction): Precedence 1 (Left-Associative)
4. **Comprehensive Error Handling**: Mismatched parentheses detection, syntax validation, and zero-division exception protection.
5. **Multi-Digit & Floating-Point Support**: Correctly handles multi-digit numbers (e.g. `10 + 250 / 5`) and algebraic variable tokens (e.g. `(A + B) * C`).

---

## 📊 Complexity Analysis

| Operation | Time Complexity | Auxiliary Space Complexity |
|---|---|---|
| Infix to Postfix | $\mathcal{O}(N)$ | $\mathcal{O}(N)$ |
| Infix to Prefix | $\mathcal{O}(N)$ | $\mathcal{O}(N)$ |
| Postfix to Infix | $\mathcal{O}(N)$ | $\mathcal{O}(N)$ |
| Expression Evaluation | $\mathcal{O}(N)$ | $\mathcal{O}(N)$ |

---

## 🚀 Execution Instructions

### 1. Infix to Postfix & Prefix Conversion
```bash
python main.py --infix "(A + B) * (C - D) / E ^ F"
```

### 2. Numerical Expression Evaluation
```bash
python main.py --infix "(10 + 20) / (3 * 2) + 2 ^ 3"
```

### 3. Postfix Expression Evaluation
```bash
python main.py --postfix "3 5 2 * +"
```

### 4. Run Automated Unit Tests
```bash
python -m unittest discover -s tests
```
