/**
 * আভরণ (Abhoron) - Interactive Quiz Module
 */

(function () {
    'use strict';

    var questions = [
        {
            question: "Python-এ একটি ভেরিয়েবল ডিক্লেয়ার করার সঠিক উপায় কোনটি?",
            options: ["var x = 5", "int x = 5", "x = 5", "declare x = 5"],
            correct: 2
        },
        {
            question: "HTML-এ একটি লিংক তৈরি করতে কোন ট্যাগ ব্যবহার করা হয়?",
            options: ["<link>", "<a>", "<href>", "<url>"],
            correct: 1
        },
        {
            question: "CSS-এ একটি এলিমেন্টের ব্যাকগ্রাউন্ড কালার পরিবর্তন করতে কোন প্রোপার্টি ব্যবহার করা হয়?",
            options: ["color", "background-color", "bg-color", "fill"],
            correct: 1
        },
        {
            question: "Python-এ একটি লিস্টের শেষে একটি আইটেম যোগ করতে কোন মেথড ব্যবহার করা হয়?",
            options: ["add()", "append()", "insert()", "push()"],
            correct: 1
        },
        {
            question: "JavaScript-এ একটি ফাংশন ডিক্লেয়ার করার সঠিক সিনট্যাক্স কোনটি?",
            options: ["function = myFunc() {}", "def myFunc() {}", "function myFunc() {}", "func myFunc() {}"],
            correct: 2
        },
        {
            question: "SQL-এ একটি টেবিল থেকে ডেটা সিলেক্ট করতে কোন স্টেটমেন্ট ব্যবহার করা হয়?",
            options: ["GET", "RETRIEVE", "SELECT", "FIND"],
            correct: 2
        },
        {
            question: "CSS-এ 'display: flex;' ব্যবহার করে কী করা যায়?",
            options: ["অ্যানিমেশন", "ফ্লেক্সিবল লেআউট", "রেসপন্সিভ ইমেজ", "ডার্ক মোড"],
            correct: 1
        },
        {
            question: "Python-এ 'print()' ফাংশনের মূল কাজ কী?",
            options: ["ডেটা ইনপুট নেওয়া", "ফাইল সেভ করা", "আউটপুট প্রিন্ট করা", "ক্যালকুলেশন করা"],
            correct: 2
        },
        {
            question: "HTML5-এ সেমান্টিক ট্যাগ কোনটি?",
            options: ["<div>", "<span>", "<section>", "<font>"],
            correct: 2
        },
        {
            question: "Git-এ একটি নতুন ব্রাঞ্চ তৈরি করার কমান্ড কোনটি?",
            options: ["git new branch", "git branch", "git create", "git add branch"],
            correct: 1
        }
    ];

    var currentQuestion = 0;
    var score = 0;
    var answered = false;

    var questionEl = document.getElementById('quiz-question');
    var optionsEl = document.getElementById('quiz-options');
    var feedbackEl = document.getElementById('quiz-feedback');
    var progressEl = document.getElementById('quiz-progress');
    var nextBtn = document.getElementById('next-btn');
    var restartBtn = document.getElementById('restart-btn');
    var resultEl = document.getElementById('quiz-result');
    var finalScoreEl = document.getElementById('final-score');
    var quizCard = document.getElementById('quiz-card');

    function loadQuestion() {
        if (currentQuestion >= questions.length) {
            showResult();
            return;
        }

        answered = false;
        var q = questions[currentQuestion];
        questionEl.textContent = q.question;
        progressEl.textContent = 'প্রশ্ন ' + (currentQuestion + 1) + ' / ' + questions.length;
        feedbackEl.textContent = '';
        nextBtn.style.display = 'none';
        restartBtn.style.display = 'none';

        optionsEl.innerHTML = '';
        q.options.forEach(function (opt, idx) {
            var btn = document.createElement('button');
            btn.className = 'btn btn-outline';
            btn.style.display = 'block';
            btn.style.width = '100%';
            btn.style.marginBottom = '8px';
            btn.style.textAlign = 'left';
            btn.textContent = opt;
            btn.setAttribute('data-index', idx);
            btn.addEventListener('click', function () {
                if (!answered) {
                    checkAnswer(idx);
                }
            });
            optionsEl.appendChild(btn);
        });
    }

    function checkAnswer(selected) {
        answered = true;
        var q = questions[currentQuestion];
        var buttons = optionsEl.querySelectorAll('button');

        buttons.forEach(function (btn) {
            var idx = parseInt(btn.getAttribute('data-index'));
            if (idx === q.correct) {
                btn.style.background = '#4caf50';
                btn.style.color = '#fff';
                btn.style.borderColor = '#4caf50';
            } else if (idx === selected && idx !== q.correct) {
                btn.style.background = '#f44336';
                btn.style.color = '#fff';
                btn.style.borderColor = '#f44336';
            }
            btn.disabled = true;
        });

        if (selected === q.correct) {
            score++;
            feedbackEl.textContent = 'সঠিক উত্তর!';
            feedbackEl.style.color = '#4caf50';
        } else {
            feedbackEl.textContent = 'ভুল উত্তর। সঠিক উত্তর: ' + q.options[q.correct];
            feedbackEl.style.color = '#f44336';
        }

        if (currentQuestion < questions.length - 1) {
            nextBtn.style.display = 'inline-block';
        } else {
            restartBtn.style.display = 'inline-block';
        }
    }

    function showResult() {
        if (quizCard) {
            quizCard.style.display = 'none';
        }
        if (resultEl) {
            resultEl.style.display = 'block';
            finalScoreEl.textContent = score + ' / ' + questions.length;
        }
    }

    if (nextBtn) {
        nextBtn.addEventListener('click', function () {
            currentQuestion++;
            loadQuestion();
        });
    }

    if (restartBtn) {
        restartBtn.addEventListener('click', function () {
            currentQuestion = 0;
            score = 0;
            if (quizCard) {
                quizCard.style.display = 'block';
            }
            if (resultEl) {
                resultEl.style.display = 'none';
            }
            loadQuestion();
        });
    }

    loadQuestion();

})();
