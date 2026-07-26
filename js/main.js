/* ============================================================
   HANO STUDIOS — interactions
   ============================================================ */

(function () {
  'use strict';

  // Claim the `js` class only once this file is actually executing, so a
  // failed/blocked script can never leave `.reveal` content stuck invisible.
  document.documentElement.classList.add('js');

  const reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const hasGSAP = typeof gsap !== 'undefined' && typeof ScrollTrigger !== 'undefined';

  if (hasGSAP) gsap.registerPlugin(ScrollTrigger);

  /* ---------------- Menu ---------------- */

  const menuBtn = document.getElementById('menuBtn');
  const menuOverlay = document.getElementById('menuOverlay');
  const hero = document.querySelector('.hero');

  const FOCUSABLE = 'a[href],button:not([disabled]),input,select,textarea,[tabindex]:not([tabindex="-1"])';

  function isMenuOpen() {
    return menuOverlay.classList.contains('is-open');
  }

  // Take the page behind the overlay out of the tab order and the accessibility
  // tree. Only aria-hidden we added ourselves is removed again — .split and
  // .wipe are decorative and carry their own in the markup.
  function setBehindInert(on) {
    Array.from(document.body.children).forEach(el => {
      if (el === menuOverlay || el === menuBtn) return;
      if (on) {
        el.setAttribute('inert', '');
        if (!el.hasAttribute('aria-hidden')) {
          el.setAttribute('aria-hidden', 'true');
          el.dataset.menuHid = '';
        }
      } else {
        el.removeAttribute('inert');
        if ('menuHid' in el.dataset) {
          el.removeAttribute('aria-hidden');
          delete el.dataset.menuHid;
        }
      }
    });
  }

  // The button sits outside the overlay but is its only visible dismiss control
  // while open, so it belongs in the cycle. DOM order already puts it first.
  function focusCycle() {
    return [menuBtn].concat(Array.from(menuOverlay.querySelectorAll(FOCUSABLE)));
  }

  function toggleMenu(open, restoreFocus) {
    const next = open !== undefined ? open : !isMenuOpen();
    menuOverlay.classList.toggle('is-open', next);
    menuBtn.classList.toggle('is-open', next);
    menuBtn.setAttribute('aria-expanded', String(next));
    menuOverlay.setAttribute('aria-hidden', String(!next));
    menuBtn.setAttribute('aria-label', next ? 'Close menu' : 'Open menu');
    document.body.style.overflow = next ? 'hidden' : '';
    setBehindInert(next);

    if (next) {
      menuOverlay.removeAttribute('inert');
      const first = menuOverlay.querySelector('.menu-links a');
      if (first) first.focus();
    } else {
      // Move focus out before inerting, otherwise the browser drops it to <body>.
      if (restoreFocus !== false) menuBtn.focus();
      menuOverlay.setAttribute('inert', '');
    }
  }

  menuBtn.addEventListener('click', () => toggleMenu());
  menuOverlay.addEventListener('click', e => {
    // Following a link hands focus to the target section — don't pull it back.
    if (e.target.tagName === 'A') toggleMenu(false, false);
  });

  document.addEventListener('keydown', e => {
    if (!isMenuOpen()) return;

    if (e.key === 'Escape') {
      toggleMenu(false);
      return;
    }
    if (e.key !== 'Tab') return;

    const items = focusCycle();
    if (!items.length) return;
    const first = items[0];
    const last = items[items.length - 1];
    const active = document.activeElement;

    if (active !== menuBtn && !menuOverlay.contains(active)) {
      e.preventDefault();
      first.focus();
    } else if (e.shiftKey && active === first) {
      e.preventDefault();
      last.focus();
    } else if (!e.shiftKey && active === last) {
      e.preventDefault();
      first.focus();
    }
  });

  // Menu button only appears once the hero has scrolled past
  const heroObserver = new IntersectionObserver(
    entries => entries.forEach(en => menuBtn.classList.toggle('is-visible', !en.isIntersecting)),
    { threshold: 0.15 }
  );
  if (hero) heroObserver.observe(hero);

  /* ---------------- Scroll reveals ---------------- */

  const revealObserver = new IntersectionObserver(
    entries => {
      entries.forEach(en => {
        if (!en.isIntersecting) return;
        en.target.animate(
          [
            { opacity: 0, transform: 'translateY(26px)' },
            { opacity: 1, transform: 'translateY(0)' }
          ],
          { duration: reduce ? 1 : 900, easing: 'cubic-bezier(.22,1,.36,1)', fill: 'forwards' }
        );
        revealObserver.unobserve(en.target);
      });
    },
    { threshold: 0.12, rootMargin: '0px 0px -8% 0px' }
  );
  document.querySelectorAll('.reveal').forEach(el => revealObserver.observe(el));

  /* ---------------- Counting stats ---------------- */

  const statObserver = new IntersectionObserver(
    entries => {
      entries.forEach(en => {
        if (!en.isIntersecting) return;
        const el = en.target;
        const target = parseInt(el.dataset.count, 10);
        if (reduce) {
          el.textContent = target + '+';
          statObserver.unobserve(el);
          return;
        }
        const start = performance.now();
        const dur = 1400;
        (function step(now) {
          const p = Math.min((now - start) / dur, 1);
          const eased = 1 - Math.pow(1 - p, 3);
          el.textContent = Math.round(target * eased) + '+';
          if (p < 1) requestAnimationFrame(step);
        })(start);
        statObserver.unobserve(el);
      });
    },
    { threshold: 0.5 }
  );
  document.querySelectorAll('.stats dt').forEach(el => statObserver.observe(el));

  /* ---------------- Services hover preview ---------------- */

  const serviceList = document.getElementById('serviceList');
  const preview = document.getElementById('servicePreview');

  if (serviceList && preview) {
    serviceList.querySelectorAll('li').forEach(li => {
      li.addEventListener('mouseenter', () => {
        preview.setAttribute('data-tone', li.dataset.tone);
        if (li.dataset.img) preview.style.backgroundImage = "url('" + li.dataset.img + "')";
        preview.classList.add('is-on');
      });
    });
    serviceList.addEventListener('mouseleave', () => preview.classList.remove('is-on'));
  }

  /* ---------------- Showcase arrows ---------------- */

  const stage = document.getElementById('showStage');
  const prev = document.getElementById('showPrev');
  const next = document.getElementById('showNext');

  function slide(dir) {
    if (!stage) return;
    const card = stage.querySelector('.phone');
    const step = card ? card.offsetWidth + 30 : 260;
    stage.scrollBy({ left: step * dir, behavior: reduce ? 'auto' : 'smooth' });
  }
  if (prev) prev.addEventListener('click', () => slide(-1));
  if (next) next.addEventListener('click', () => slide(1));

  /* ---------------- Contact form ---------------- */

  const form = document.getElementById('contactForm');

  if (form) {
    const status = document.getElementById('formStatus');
    const submitBtn = form.querySelector('.cta-bar');
    const fields = Array.from(form.querySelectorAll('input:not([type="hidden"]), select, textarea'))
      .filter(el => !el.closest('.hp'));

    // Only now that this script is running do we take validation off the browser.
    // Without it, a plain POST still gets native required/type checks.
    form.noValidate = true;

    let attempted = false;

    function validate(el) {
      const wrap = el.closest('.field');
      if (!wrap) return true;
      const msg = wrap.querySelector('.field-msg');
      const value = el.value.trim();
      let error = '';

      if (el.required && !value) {
        error = el.tagName === 'SELECT' ? 'Please choose an option.' : 'This one is required.';
      } else if (el.type === 'email' && value && !/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(value)) {
        error = 'That does not look like an email address.';
      }

      wrap.classList.toggle('is-invalid', !!error);
      wrap.classList.toggle('is-valid', !error && !!value);
      el.setAttribute('aria-invalid', error ? 'true' : 'false');
      if (msg) msg.textContent = error;
      return !error;
    }

    // Stay quiet until the first submit, then correct in real time.
    fields.forEach(el => {
      el.addEventListener('blur', () => { if (attempted) validate(el); });
      el.addEventListener('input', () => { if (attempted) validate(el); });
      el.addEventListener('change', () => { if (attempted) validate(el); });
    });

    function setStatus(text, isError) {
      status.textContent = text;
      status.classList.toggle('is-error', !!isError);
    }

    form.addEventListener('submit', e => {
      e.preventDefault();
      attempted = true;

      const allValid = fields.map(validate).every(Boolean);
      if (!allValid) {
        setStatus('Please check the highlighted fields.', true);
        const firstBad = form.querySelector('.field.is-invalid input, .field.is-invalid select, .field.is-invalid textarea');
        if (firstBad) firstBad.focus();
        return;
      }

      const label = submitBtn.textContent;
      submitBtn.disabled = true;
      submitBtn.textContent = 'Sending…';
      setStatus('', false);

      fetch(form.action, {
        method: 'POST',
        body: new FormData(form),
        headers: { Accept: 'application/json' }
      })
        .then(res => {
          if (!res.ok) throw new Error('HTTP ' + res.status);
          form.classList.add('is-done');
          form.innerHTML =
            '<div class="form-done" tabindex="-1" role="status">' +
            '<strong>Thanks — that has landed.</strong>' +
            '<span>We read every enquiry ourselves and reply within one working day.</span>' +
            '</div>';
          const done = form.querySelector('.form-done');
          if (done) done.focus();
          // Conversion goal. The head stub means this is safe even if the
          // analytics script was blocked or has not loaded yet.
          if (window.plausible) window.plausible('Contact form submitted');
        })
        .catch(() => {
          submitBtn.disabled = false;
          submitBtn.textContent = label;
          setStatus('That did not send. Please try again, or email hello@hano.studios directly.', true);
        });
    });
  }

  /* ---------------- GSAP scroll sequences ---------------- */

  if (!hasGSAP || reduce) return;

  // Hero title lifts and fades as you leave
  gsap.to('.hero-bottom', {
    yPercent: -18,
    opacity: 0,
    ease: 'none',
    scrollTrigger: { trigger: '.hero', start: 'bottom 92%', end: 'bottom 30%', scrub: true }
  });

  // Split transition — words pull apart, square rotates through
  const splitTL = gsap.timeline({
    scrollTrigger: { trigger: '.split', start: 'top top', end: 'bottom bottom', scrub: 0.6 }
  });
  splitTL
    .fromTo('.split-left', { xPercent: 34, filter: 'blur(0px)' }, { xPercent: -46, filter: 'blur(7px)', ease: 'none' }, 0)
    .fromTo('.split-right', { xPercent: -34, filter: 'blur(0px)' }, { xPercent: 46, filter: 'blur(7px)', ease: 'none' }, 0)
    .fromTo('.split-square', { rotate: -18, scale: 0.72 }, { rotate: 4, scale: 1.18, ease: 'none' }, 0);

  // Works — horizontal scroll pinned
  const track = document.getElementById('worksTrack');
  if (track) {
    const distance = () => Math.max(0, track.scrollWidth - window.innerWidth);
    gsap.to(track, {
      x: () => -distance(),
      ease: 'none',
      scrollTrigger: {
        trigger: '.works',
        start: 'top top',
        end: () => '+=' + distance(),
        scrub: 0.8,
        pin: '.works-pin',
        anticipatePin: 1,
        invalidateOnRefresh: true
      }
    });
  }

  // Circle wipe into the light services section
  const wipeCircle = document.getElementById('wipeCircle');
  if (wipeCircle) {
    ScrollTrigger.create({
      trigger: '.wipe',
      start: 'top top',
      end: 'bottom bottom',
      scrub: 0.5,
      onUpdate: self => {
        wipeCircle.style.setProperty('--scale', (0.06 + self.progress * 2.6).toFixed(3));
      }
    });
  }

  // Footer watermark parallax
  gsap.to('.footer-mark', {
    xPercent: -6,
    ease: 'none',
    scrollTrigger: { trigger: '.footer', start: 'top bottom', end: 'bottom bottom', scrub: true }
  });

  window.addEventListener('load', () => ScrollTrigger.refresh());
})();
