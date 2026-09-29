const test = require('node:test');
const assert = require('node:assert');
const { QUIZ_QUESTIONS } = require('../questions');

test('JavaScript Quiz App Unit Tests', async (t) => {
    await t.test('1. Question bank is well-formed', () => {
        assert.ok(Array.isArray(QUIZ_QUESTIONS));
        assert.ok(QUIZ_QUESTIONS.length >= 5);
    });

    await t.test('2. Each question has valid structure and 4 options', () => {
        for (const q of QUIZ_QUESTIONS) {
            assert.ok(q.id > 0);
            assert.ok(typeof q.question === 'string' && q.question.length > 5);
            assert.strictEqual(q.options.length, 4);
            assert.ok(q.correctIndex >= 0 && q.correctIndex < 4);
            assert.ok(typeof q.explanation === 'string' && q.explanation.length > 5);
        }
    });

    await t.test('3. Verify sample answer evaluation logic', () => {
        const q1 = QUIZ_QUESTIONS[0];
        assert.strictEqual(q1.correctIndex, 1); // 'let'
        assert.strictEqual(q1.options[q1.correctIndex], 'let');
    });
});
