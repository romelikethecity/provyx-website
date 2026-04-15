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

  // Header scroll effect using IntersectionObserver
  var header = document.querySelector('.header');
  var sentinel = document.createElement('div');
  sentinel.style.cssText = 'position:absolute;top:100px;height:1px;width:1px;pointer-events:none';
  document.body.prepend(sentinel);

  var headerObs = new IntersectionObserver(function(entries) {
    if (entries[0].isIntersecting) {
      header.classList.remove('header--scrolled');
    } else {
      header.classList.add('header--scrolled');
    }
  });
  headerObs.observe(sentinel);

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

  // GA4: Scroll depth milestones via IntersectionObserver
  if (typeof gtag === 'function') {
    [25, 50, 75, 100].forEach(function(pct) {
      var marker = document.createElement('div');
      marker.style.cssText = 'position:absolute;left:0;width:1px;height:1px;pointer-events:none';
      marker.style.top = pct + '%';
      document.body.appendChild(marker);

      var obs = new IntersectionObserver(function(entries) {
        if (entries[0].isIntersecting) {
          gtag('event', 'scroll_depth', { percent_scrolled: pct });
          obs.disconnect();
        }
      });
      obs.observe(marker);
    });
  }

  // Scroll-triggered CTA bar (appears after 60% scroll, not on contact/pricing pages)
  // Uses static trusted HTML only - no user input involved
  var skipCtaBar = window.location.pathname.indexOf('/contact') === 0
    || window.location.pathname.indexOf('/pricing') === 0;

  if (!skipCtaBar && !sessionStorage.getItem('provyx-cta-dismissed')) {
    var ctaMarker = document.createElement('div');
    ctaMarker.style.cssText = 'position:absolute;left:0;top:60%;width:1px;height:1px;pointer-events:none';
    document.body.appendChild(ctaMarker);

    var ctaObs = new IntersectionObserver(function(entries) {
      if (entries[0].isIntersecting) {
        ctaObs.disconnect();

        var bar = document.createElement('div');
        bar.className = 'scroll-cta-bar';

        var p = document.createElement('p');
        p.textContent = 'Need healthcare provider data for your team?';
        bar.appendChild(p);

        var link = document.createElement('a');
        link.href = '/contact/';
        link.className = 'btn btn--primary btn--sm';
        link.textContent = 'Get a Sample List';
        bar.appendChild(link);

        var closeBtn = document.createElement('button');
        closeBtn.className = 'scroll-cta-bar__close';
        closeBtn.setAttribute('aria-label', 'Dismiss');
        closeBtn.textContent = '\u00D7';
        bar.appendChild(closeBtn);

        document.body.appendChild(bar);
        requestAnimationFrame(function() {
          requestAnimationFrame(function() { bar.classList.add('visible'); });
        });
        closeBtn.addEventListener('click', function() {
          bar.classList.remove('visible');
          sessionStorage.setItem('provyx-cta-dismissed', '1');
          setTimeout(function() { bar.remove(); }, 300);
        });
        if (typeof gtag === 'function') {
          gtag('event', 'scroll_cta_shown', { page_path: window.location.pathname });
        }
      }
    });
    ctaObs.observe(ctaMarker);
  }

})();
