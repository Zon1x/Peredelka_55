(function () {
    'use strict';

    var toggle = document.getElementById('nav-toggle');
    var nav = document.getElementById('site-nav');
    var backdrop = document.getElementById('nav-backdrop');

    if (toggle && nav) {
        function setOpen(open) {
            document.body.classList.toggle('nav-open', open);
            nav.classList.toggle('is-open', open);
            toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
            toggle.setAttribute('aria-label', open ? 'Закрыть меню' : 'Открыть меню');
            if (backdrop) {
                backdrop.hidden = !open;
                backdrop.setAttribute('aria-hidden', open ? 'false' : 'true');
            }
        }

        function closeNav() {
            setOpen(false);
        }

        toggle.addEventListener('click', function () {
            setOpen(!document.body.classList.contains('nav-open'));
        });

        if (backdrop) {
            backdrop.addEventListener('click', closeNav);
        }

        nav.querySelectorAll('a').forEach(function (link) {
            link.addEventListener('click', function () {
                if (window.matchMedia('(max-width: 900px)').matches) closeNav();
            });
        });

        window.addEventListener('resize', function () {
            if (window.matchMedia('(min-width: 901px)').matches) closeNav();
        });

        document.addEventListener('keydown', function (e) {
            if (e.key === 'Escape') closeNav();
        });
    }

    var currentPath = window.location.pathname.replace(/\/+$/, '') || '/';
    document.querySelectorAll('.nav-link').forEach(function (link) {
        var linkPath = new URL(link.href, window.location.origin).pathname.replace(/\/+$/, '') || '/';
        var isMatch = linkPath === '/'
            ? currentPath === '/'
            : currentPath === linkPath || currentPath.indexOf(linkPath + '/') === 0;
        if (isMatch) {
            link.classList.add('is-active');
            link.setAttribute('aria-current', 'page');
        }
    });

    var scrollTopBtn = document.getElementById('scroll-top');
    var reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    function toggleScrollTop() {
        if (!scrollTopBtn) return;
        scrollTopBtn.classList.toggle('is-visible', window.scrollY > 280);
    }

    if (scrollTopBtn) {
        scrollTopBtn.addEventListener('click', function () {
            window.scrollTo({ top: 0, behavior: reduceMotion ? 'auto' : 'smooth' });
        });
        window.addEventListener('scroll', toggleScrollTop, { passive: true });
        toggleScrollTop();
    }

    var selectorsToStyle = '.contact-form input:not([type="checkbox"]):not([type="radio"]), .contact-form select, .contact-form textarea, .review-link-form input:not([type="checkbox"]):not([type="radio"]), .review-link-form select, .review-link-form textarea, .review-form input:not([type="checkbox"]):not([type="radio"]), .review-form select, .review-form textarea, .quick-contact-form input:not([type="checkbox"]):not([type="radio"]), .quick-contact-form select, .quick-contact-form textarea, .constructor-section input:not([type="checkbox"]):not([type="radio"]), .constructor-section select';
    document.querySelectorAll(selectorsToStyle).forEach(function (field) {
        field.classList.add('form-control');
    });

    document.querySelectorAll('input[type="tel"]').forEach(function (input) {
        input.addEventListener('input', function () {
            input.value = input.value.replace(/[^\d+\-()\s]/g, '');
        });
    });

    var costModal = document.getElementById('cost-modal');
    var closeCostModal = document.getElementById('close-cost-modal');
    if (costModal) {
        function hideCostModal() {
            costModal.style.display = 'none';
        }
        if (closeCostModal) {
            closeCostModal.addEventListener('click', hideCostModal);
        }
        costModal.addEventListener('click', function (e) {
            if (e.target === costModal) hideCostModal();
        });
    }

    document.querySelectorAll('section, .service-card, .portfolio-card, .review-card, .promo-card').forEach(function (el) {
        el.setAttribute('data-animate', '');
    });

    document.querySelectorAll('img').forEach(function (img) {
        if (!img.getAttribute('loading')) img.setAttribute('loading', 'lazy');
        if (!img.getAttribute('decoding')) img.setAttribute('decoding', 'async');

        img.addEventListener('error', function () {
            var parent = img.parentElement;
            if (!parent || parent.querySelector('.image-fallback')) return;
            img.style.display = 'none';
            parent.classList.add('has-image-fallback');
            var fallback = document.createElement('div');
            fallback.className = 'image-fallback';
            fallback.textContent = img.alt || 'Изображение временно недоступно';
            parent.appendChild(fallback);
        });
    });

    if (!reduceMotion && 'IntersectionObserver' in window) {
        var revealObserver = new IntersectionObserver(function (entries, observer) {
            entries.forEach(function (entry) {
                if (!entry.isIntersecting) return;
                entry.target.classList.add('is-visible');
                observer.unobserve(entry.target);
            });
        }, { threshold: 0.12, rootMargin: '0px 0px -30px 0px' });

        document.querySelectorAll('[data-animate]').forEach(function (el) {
            revealObserver.observe(el);
        });
    } else {
        document.querySelectorAll('[data-animate]').forEach(function (el) {
            el.classList.add('is-visible');
        });
    }
})();
