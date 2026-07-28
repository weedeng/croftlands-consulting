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

  /* ── Booking modal (Microsoft Bookings) ───────────────── */
  const BOOKING_URL =
    'https://outlook.office.com/owa/calendar/CroftlandsConsulting@croftlandsconsulting.com/bookings/?ismsaljsauthenabled';

  const bookModal = document.createElement('div');
  bookModal.className = 'book-modal';
  bookModal.setAttribute('role', 'dialog');
  bookModal.setAttribute('aria-modal', 'true');
  bookModal.setAttribute('aria-label', 'Book a discovery call');
  bookModal.innerHTML =
    '<div class="book-modal-panel">' +
      '<div class="book-modal-bar">' +
        '<span>Book a Discovery Call</span>' +
        '<button type="button" class="book-modal-close" aria-label="Close">&times;</button>' +
      '</div>' +
      '<div class="book-modal-body"></div>' +
    '</div>';
  document.body.appendChild(bookModal);

  const bookBody  = bookModal.querySelector('.book-modal-body');
  const bookClose = bookModal.querySelector('.book-modal-close');

  function openBooking () {
    // Lazy-load the iframe only on first open
    if (!bookBody.querySelector('iframe')) {
      const f = document.createElement('iframe');
      f.src = BOOKING_URL;
      f.title = 'Microsoft Bookings — Croftlands Consulting';
      f.setAttribute('loading', 'lazy');
      bookBody.appendChild(f);
    }
    bookModal.classList.add('open');
    document.body.classList.add('book-modal-lock');
    bookClose.focus();
  }
  function closeBooking () {
    bookModal.classList.remove('open');
    document.body.classList.remove('book-modal-lock');
  }

  bookClose.addEventListener('click', closeBooking);
  bookModal.addEventListener('click', function (e) {
    if (e.target === bookModal) closeBooking();
  });
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && bookModal.classList.contains('open')) closeBooking();
  });

  // Any "Book a Discovery Call" link/button (or [data-book]) opens the modal.
  // The underlying href="contact.html" remains a fallback if JS fails to load.
  document.querySelectorAll('a, button').forEach(function (el) {
    const txt = (el.textContent || '').trim().toLowerCase();
    if (el.hasAttribute('data-book') || txt === 'book a discovery call') {
      el.addEventListener('click', function (e) {
        e.preventDefault();
        openBooking();
      });
    }
  });

})();
