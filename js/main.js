/**
 * Provyx Website - Main JavaScript
 *
 * Mobile navigation toggle is handled inline in each page's nav HTML
 * (baked in at build time by scripts/templates.py).
 */

(function() {
  'use strict';

  // Smooth scroll for anchor links
  document.querySelectorAll('a[href^="#"]').forEach(function(anchor) {
    anchor.addEventListener('click', function(e) {
      var targetId = this.getAttribute('href');
      if (targetId === '#') return;

      var target = document.querySelector(targetId);
      if (target) {
        e.preventDefault();
        var headerHeight = document.querySelector('.header').offsetHeight;
        var targetPosition = target.getBoundingClientRect().top + window.pageYOffset - headerHeight;

        window.scrollTo({
          top: targetPosition,
          behavior: 'smooth'
        });
      }
    });
  });

  // Header scroll effect
  var header = document.querySelector('.header');

  function updateHeader() {
    if (window.scrollY > 100) {
      header.style.boxShadow = '0 2px 10px rgba(0, 0, 0, 0.08)';
    } else {
      header.style.boxShadow = 'none';
    }
  }

  window.addEventListener('scroll', updateHeader, { passive: true });

  // Form submission handling
  var forms = document.querySelectorAll('form');
  forms.forEach(function(form) {
    form.addEventListener('submit', function() {
      var submitBtn = form.querySelector('[type="submit"]');
      if (submitBtn) {
        submitBtn.disabled = true;
        submitBtn.textContent = 'Sending...';
      }
    });
  });

})();
