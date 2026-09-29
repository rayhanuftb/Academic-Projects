// Question Bank for JavaScript Quiz App
// Digital Content Design and Development Lab (ICTE 4232)

const QUIZ_QUESTIONS = [
    {
        id: 1,
        category: "JavaScript",
        question: "Which keyword declares a block-scoped, re-assignable variable in modern ES6 JavaScript?",
        options: ["var", "let", "const", "global"],
        correctIndex: 1,
        explanation: "'let' declares a block-scoped variable that can be reassigned, whereas 'const' cannot be reassigned and 'var' is function-scoped."
    },
    {
        id: 2,
        category: "Web Development",
        question: "What does DOM stand for in client-side web development?",
        options: ["Digital Object Model", "Document Object Model", "Dynamic Output Mechanism", "Desktop Operating Mode"],
        correctIndex: 1,
        explanation: "DOM stands for Document Object Model, which represents the HTML document structure as a tree of nodes."
    },
    {
        id: 3,
        category: "Cloud & EdTech",
        question: "Which cloud service model provides fully functional applications accessed via a web browser?",
        options: ["IaaS (Infrastructure as a Service)", "PaaS (Platform as a Service)", "SaaS (Software as a Service)", "BaaS (Backend as a Service)"],
        correctIndex: 2,
        explanation: "SaaS (Software as a Service) delivers turnkey end-user software applications (like Google Classroom or Canvas) directly over the internet."
    },
    {
        id: 4,
        category: "JavaScript",
        question: "What will the expression `typeof null` return in JavaScript?",
        options: ["'null'", "'undefined'", "'object'", "'boolean'"],
        correctIndex: 2,
        explanation: "In JavaScript, 'typeof null' returns 'object' due to a historical legacy implementation in the original JS engine."
    },
    {
        id: 5,
        category: "Data Structures",
        question: "Which data structure operates on a Last-In, First-Out (LIFO) order?",
        options: ["Queue", "Stack", "Binary Tree", "Linked List"],
        correctIndex: 1,
        explanation: "A Stack operates strictly under LIFO order, where the most recently added element is the first one removed."
    }
];

if (typeof module !== 'undefined' && module.exports) {
    module.exports = { QUIZ_QUESTIONS };
}
