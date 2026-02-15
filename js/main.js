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

  // Form submission handling + GA4 events
  var forms = document.querySelectorAll('form');
  forms.forEach(function(form) {
    var formStarted = false;
    form.addEventListener('focusin', function() {
      if (!formStarted && typeof gtag === 'function') {
        formStarted = true;
        gtag('event', 'form_started', {
          form_type: 'contact'
        });
      }
    });
    form.addEventListener('submit', function() {
      var submitBtn = form.querySelector('[type="submit"]');
      if (submitBtn) {
        submitBtn.disabled = true;
        submitBtn.textContent = 'Sending...';
      }
      if (typeof gtag === 'function') {
        gtag('event', 'form_submitted', {
          form_type: 'contact'
        });
      }
    });
  });

  // GA4: Pricing page view
  if (window.location.pathname.indexOf('/pricing') === 0 && typeof gtag === 'function') {
    gtag('event', 'pricing_viewed');
  }

  // GA4: CTA button clicks
  document.querySelectorAll('.btn').forEach(function(btn) {
    btn.addEventListener('click', function() {
      if (typeof gtag !== 'function') return;
      var text = this.textContent.trim();
      var section = 'body';
      if (this.closest('.header')) section = 'header';
      else if (this.closest('.footer')) section = 'footer';
      else if (this.closest('.page-hero')) section = 'hero';
      else if (this.closest('.cta-section')) section = 'cta';
      gtag('event', 'cta_clicked', {
        button_text: text,
        page_location: section
      });
    });
  });

  // GA4: FAQ accordion expand
  document.querySelectorAll('.faq-item').forEach(function(details) {
    details.addEventListener('toggle', function() {
      if (this.open && typeof gtag === 'function') {
        var summary = this.querySelector('.faq-item__question');
        gtag('event', 'faq_expanded', {
          question_text: summary ? summary.textContent.trim().substring(0, 100) : ''
        });
      }
    });
  });

  // GA4: Outbound link clicks
  document.querySelectorAll('a[target="_blank"]').forEach(function(link) {
    link.addEventListener('click', function() {
      if (typeof gtag !== 'function') return;
      gtag('event', 'outbound_link_clicked', {
        link_url: this.href,
        link_text: this.textContent.trim().substring(0, 80)
      });
    });
  });

  // GA4: Scroll depth milestones
  var scrollMilestones = { 25: false, 50: false, 75: false, 100: false };
  window.addEventListener('scroll', function() {
    if (typeof gtag !== 'function') return;
    var scrollPct = Math.round((window.scrollY + window.innerHeight) / document.documentElement.scrollHeight * 100);
    [25, 50, 75, 100].forEach(function(milestone) {
      if (scrollPct >= milestone && !scrollMilestones[milestone]) {
        scrollMilestones[milestone] = true;
        gtag('event', 'scroll_depth', {
          percent_scrolled: milestone
        });
      }
    });
  }, { passive: true });

  // Scroll-triggered CTA bar (appears after 60% scroll, not on contact/pricing pages)
  var ctaBarShown = false;
  var ctaBarDismissed = false;
  var skipCtaBar = window.location.pathname.indexOf('/contact') === 0
    || window.location.pathname.indexOf('/pricing') === 0;

  if (!skipCtaBar) {
    window.addEventListener('scroll', function() {
      if (ctaBarShown || ctaBarDismissed) return;
      var pct = Math.round((window.scrollY + window.innerHeight) / document.documentElement.scrollHeight * 100);
      if (pct >= 60) {
        ctaBarShown = true;
        var bar = document.createElement('div');
        bar.className = 'scroll-cta-bar';
        bar.innerHTML = '<p>Need healthcare provider data for your team?</p>'
          + '<a href="/contact/" class="btn btn--primary btn--sm">Get a Sample List</a>'
          + '<button class="scroll-cta-bar__close" aria-label="Dismiss">&times;</button>';
        document.body.appendChild(bar);
        requestAnimationFrame(function() {
          requestAnimationFrame(function() { bar.classList.add('visible'); });
        });
        bar.querySelector('.scroll-cta-bar__close').addEventListener('click', function() {
          bar.classList.remove('visible');
          ctaBarDismissed = true;
          setTimeout(function() { bar.remove(); }, 300);
        });
        if (typeof gtag === 'function') {
          gtag('event', 'scroll_cta_shown', { page_path: window.location.pathname });
        }
      }
    }, { passive: true });
  }

})();
