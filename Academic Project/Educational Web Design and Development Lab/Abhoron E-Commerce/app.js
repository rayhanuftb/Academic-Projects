/**
 * আভরণ (Abhoron) Educational Platform - Main Application
 */

(function () {
    'use strict';

    // ========== Navigation Toggle ==========
    const navToggle = document.querySelector('.nav-toggle');
    const navMenu = document.getElementById('nav-menu');

    if (navToggle && navMenu) {
        navToggle.addEventListener('click', function () {
            const expanded = this.getAttribute('aria-expanded') === 'true';
            this.setAttribute('aria-expanded', !expanded);
            navMenu.classList.toggle('open');
        });

        document.querySelectorAll('.nav-link').forEach(function (link) {
            link.addEventListener('click', function () {
                navMenu.classList.remove('open');
                navToggle.setAttribute('aria-expanded', 'false');
            });
        });
    }

    // ========== Dark Mode Toggle ==========
    const themeToggle = document.getElementById('theme-toggle');
    const STORAGE_KEY = 'abhoron-theme';

    function applyTheme(theme) {
        document.documentElement.setAttribute('data-theme', theme);
        if (themeToggle) {
            themeToggle.innerHTML = theme === 'dark'
                ? '<span aria-hidden="true">&#9728;</span>'
                : '<span aria-hidden="true">&#9790;</span>';
        }
    }

    if (themeToggle) {
        const savedTheme = localStorage.getItem(STORAGE_KEY) || 'light';
        applyTheme(savedTheme);

        themeToggle.addEventListener('click', function () {
            const current = document.documentElement.getAttribute('data-theme');
            const next = current === 'dark' ? 'light' : 'dark';
            localStorage.setItem(STORAGE_KEY, next);
            applyTheme(next);
        });
    }

    // ========== Counter Animation ==========
    function animateCounters() {
        document.querySelectorAll('.stat-number[data-count]').forEach(function (el) {
            const target = parseInt(el.getAttribute('data-count'), 10);
            const duration = 2000;
            const start = performance.now();

            function update(now) {
                const elapsed = now - start;
                const progress = Math.min(elapsed / duration, 1);
                const eased = 1 - Math.pow(1 - progress, 3);
                el.textContent = Math.round(target * eased);
                if (progress < 1) {
                    requestAnimationFrame(update);
                }
            }
            requestAnimationFrame(update);
        });
    }

    // ========== Intersection Observer for Animations ==========
    if ('IntersectionObserver' in window) {
        const observer = new IntersectionObserver(function (entries) {
            entries.forEach(function (entry) {
                if (entry.isIntersecting) {
                    if (entry.target.classList.contains('hero-stats')) {
                        animateCounters();
                    }
                    entry.target.classList.add('visible');
                    observer.unobserve(entry.target);
                }
            });
        }, { threshold: 0.2 });

        document.querySelectorAll('.hero-stats, .feature-card, .course-card, .testimonial-card').forEach(function (el) {
            observer.observe(el);
        });
    } else {
        animateCounters();
    }

    // ========== Newsletter Form ==========
    var newsletterForm = document.querySelector('.newsletter-form');
    if (newsletterForm) {
        newsletterForm.addEventListener('submit', function (e) {
            e.preventDefault();
            var emailInput = this.querySelector('input[type="email"]');
            if (emailInput && emailInput.value) {
                alert('ধন্যবাদ! আপনি সফলভাবে সাবস্ক্রাইব করেছেন।');
                emailInput.value = '';
            }
        });
    }

    // ========== Active Nav Link ==========
    var currentPage = window.location.pathname.split('/').pop() || 'index.html';
    document.querySelectorAll('.nav-link').forEach(function (link) {
        var href = link.getAttribute('href');
        if (href === currentPage) {
            link.classList.add('active');
        } else {
            link.classList.remove('active');
        }
    });

    // ========== Scroll Progress Indicator ==========
    var progressBar = document.createElement('div');
    progressBar.style.cssText = 'position:fixed;top:0;left:0;height:3px;background:var(--color-primary);z-index:100;transition:width 0.1s;width:0';
    document.body.appendChild(progressBar);

    window.addEventListener('scroll', function () {
        var scrollTop = document.documentElement.scrollTop;
        var scrollHeight = document.documentElement.scrollHeight - document.documentElement.clientHeight;
        var progress = scrollHeight > 0 ? (scrollTop / scrollHeight) * 100 : 0;
        progressBar.style.width = progress + '%';
    });

})();
