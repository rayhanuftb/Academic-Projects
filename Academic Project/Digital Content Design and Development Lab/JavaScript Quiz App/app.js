// Interactive Quiz Application Logic
let currentIndex = 0;
let score = 0;
let answered = false;

function startQuiz() {
    currentIndex = 0;
    score = 0;
    answered = false;
    document.getElementById('screen-start').classList.add('hidden');
    document.getElementById('screen-result').classList.add('hidden');
    document.getElementById('screen-question').classList.remove('hidden');
    renderQuestion();
}

function renderQuestion() {
    answered = false;
    const q = QUIZ_QUESTIONS[currentIndex];
    const total = QUIZ_QUESTIONS.length;

    // Progress updates
    const pct = ((currentIndex) / total) * 100;
    document.getElementById('progress-fill').style.width = `${pct}%`;
    document.getElementById('question-tracker').textContent = `Question ${currentIndex + 1} of ${total}`;
    document.getElementById('score-tracker').textContent = `Score: ${score}`;

    document.getElementById('q-category').textContent = q.category;
    document.getElementById('q-text').textContent = q.question;

    const optContainer = document.getElementById('options-container');
    const letters = ['A', 'B', 'C', 'D'];
    optContainer.innerHTML = q.options.map((opt, idx) => `
        <button class="option-btn" onclick="selectAnswer(${idx})" id="opt-btn-${idx}">
            <span class="option-letter">${letters[idx]}</span>
            <span>${escapeHtml(opt)}</span>
        </button>
    `).join('');

    const fbBox = document.getElementById('feedback-box');
    fbBox.className = 'feedback-box hidden';
    fbBox.innerHTML = '';
    document.getElementById('next-btn').classList.add('hidden');
}

function selectAnswer(selectedIndex) {
    if (answered) return;
    answered = true;

    const q = QUIZ_QUESTIONS[currentIndex];
    const isCorrect = selectedIndex === q.correctIndex;
    const fbBox = document.getElementById('feedback-box');
    const nextBtn = document.getElementById('next-btn');

    // Disable all options and show colors
    q.options.forEach((_, idx) => {
        const btn = document.getElementById(`opt-btn-${idx}`);
        btn.disabled = true;
        if (idx === q.correctIndex) {
            btn.classList.add('correct');
        } else if (idx === selectedIndex) {
            btn.classList.add('wrong');
        }
    });

    if (isCorrect) {
        score++;
        fbBox.className = 'feedback-box correct-fb';
        fbBox.innerHTML = `<strong>✅ Correct!</strong> ${escapeHtml(q.explanation)}`;
    } else {
        fbBox.className = 'feedback-box wrong-fb';
        fbBox.innerHTML = `<strong>❌ Incorrect.</strong> ${escapeHtml(q.explanation)}`;
    }
    fbBox.classList.remove('hidden');

    document.getElementById('score-tracker').textContent = `Score: ${score}`;
    nextBtn.classList.remove('hidden');
}

function nextQuestion() {
    currentIndex++;
    if (currentIndex < QUIZ_QUESTIONS.length) {
        renderQuestion();
    } else {
        showResults();
    }
}

function showResults() {
    const total = QUIZ_QUESTIONS.length;
    const pct = Math.round((score / total) * 100);

    document.getElementById('progress-fill').style.width = '100%';
    document.getElementById('screen-question').classList.add('hidden');
    document.getElementById('screen-result').classList.remove('hidden');

    document.getElementById('final-score-display').textContent = `${score} / ${total}`;
    document.getElementById('final-pct-display').textContent = `${pct}% Accuracy`;

    const icon = document.getElementById('result-icon');
    const msg = document.getElementById('result-message');
    if (pct >= 80) {
        icon.textContent = '🏆';
        msg.textContent = 'Outstanding achievement! You demonstrated thorough mastery.';
    } else if (pct >= 60) {
        icon.textContent = '👍';
        msg.textContent = 'Good job! A solid understanding of the core concepts.';
    } else {
        icon.textContent = '📖';
        msg.textContent = 'Keep reviewing the learning modules and try again to improve your score.';
    }
}

function escapeHtml(str) {
    if (!str) return '';
    return String(str).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
}
