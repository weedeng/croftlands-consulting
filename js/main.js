/* ============================================================
   CROFTLANDS CONSULTING — Main JS
   Nav scroll behaviour · Mobile menu · Active link
   ============================================================ */

(function () {
  'use strict';

  /* ── Nav ──────────────────────────────────────────────── */
  const nav    = document.querySelector('.nav');
  const toggle = document.querySelector('.nav-toggle');
  const links  = document.querySelector('.nav-links');

  // Scroll: transparent ↔ solid (home page only)
  function updateNav () {
    if (!nav) return;
    if (nav.classList.contains('nav--page')) return; // inner pages always solid
    if (window.scrollY > 40) {
      nav.classList.remove('nav--transparent');
      nav.classList.add('nav--solid');
    } else {
      nav.classList.remove('nav--solid');
      nav.classList.add('nav--transparent');
    }
  }

  if (nav && !nav.classList.contains('nav--page')) {
    updateNav();
    window.addEventListener('scroll', updateNav, { passive: true });
  }

  // Mobile toggle
  if (toggle && links) {
    toggle.addEventListener('click', function () {
      const open = links.classList.toggle('open');
      toggle.classList.toggle('open', open);
      toggle.setAttribute('aria-expanded', open);
    });

    // Close on link click
    links.querySelectorAll('a').forEach(function (a) {
      a.addEventListener('click', function () {
        links.classList.remove('open');
        toggle.classList.remove('open');
        toggle.setAttribute('aria-expanded', 'false');
      });
    });

    // Close on outside click
    document.addEventListener('click', function (e) {
      if (!nav.contains(e.target)) {
        links.classList.remove('open');
        toggle.classList.remove('open');
      }
    });
  }

  /* ── Active nav link ──────────────────────────────────── */
  const path = window.location.pathname.replace(/\/$/, '') || '/';
  document.querySelectorAll('.nav-links a').forEach(function (a) {
    const href = a.getAttribute('href').replace(/\/$/, '') || '/';
    if (
      href === path ||
      (href !== '/' && href !== '/index.html' && path.startsWith(href))
    ) {
      a.classList.add('active');
    }
  });

  /* ── Smooth reveal on scroll ──────────────────────────── */
  const revealEls = document.querySelectorAll(
    '.service-card, .insight-card, .case-study, .sector-card, .qual-card, .tl-item'
  );
  if ('IntersectionObserver' in window && revealEls.length) {
    const observer = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            entry.target.style.opacity    = '1';
            entry.target.style.transform  = 'translateY(0)';
            observer.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.08, rootMargin: '0px 0px -40px 0px' }
    );
    revealEls.forEach(function (el) {
      el.style.opacity   = '0';
      el.style.transform = 'translateY(18px)';
      el.style.transition = 'opacity 0.45s ease, transform 0.45s ease';
      observer.observe(el);
    });
  }

})();
