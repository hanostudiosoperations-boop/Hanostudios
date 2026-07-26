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

  // Take the page behind an open overlay out of the tab order and the
  // accessibility tree, keeping only the elements in `keep` live. Shared by the
  // menu and the booking modal. Only aria-hidden we added ourselves is removed
  // again — .split and .wipe are decorative and carry their own in the markup.
  function setPageInert(on, keep) {
    Array.from(document.body.children).forEach(el => {
      if (keep.indexOf(el) !== -1) return;
      if (on) {
        el.setAttribute('inert', '');
        if (!el.hasAttribute('aria-hidden')) {
          el.setAttribute('aria-hidden', 'true');
          el.dataset.inertHid = '';
        }
      } else {
        el.removeAttribute('inert');
        if ('inertHid' in el.dataset) {
          el.removeAttribute('aria-hidden');
          delete el.dataset.inertHid;
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
    setPageInert(next, [menuOverlay, menuBtn]);

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

  // Menu button appears once you have scrolled past the first screen. This used
  // to watch .hero with an IntersectionObserver, but the hero is pinned now, so
  // it stays fully on screen through the whole split and the button never showed.
  // Scroll position works whether or not GSAP is driving the pin.
  const revealMenuBtn = () => {
    menuBtn.classList.toggle('is-visible', window.scrollY > window.innerHeight * 0.6);
  };
  window.addEventListener('scroll', revealMenuBtn, { passive: true });
  revealMenuBtn();

  // Invert the button while a light section is under it. The root is squeezed to
  // a band across the top of the viewport, so this tracks what is actually
  // behind the button rather than whether the section is on screen at all.
  const lightSections = document.querySelectorAll('.services');
  if (lightSections.length) {
    const overLight = new Set();
    const contrastObserver = new IntersectionObserver(
      entries => {
        entries.forEach(en => {
          if (en.isIntersecting) overLight.add(en.target);
          else overLight.delete(en.target);
        });
        menuBtn.classList.toggle('on-light', overLight.size > 0);
      },
      { rootMargin: '0px 0px -90% 0px' }
    );
    lightSections.forEach(s => contrastObserver.observe(s));
  }

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

  /* ---------------- Showcase carousel + video ---------------- */

  const stage = document.getElementById('showStage');
  const prev = document.getElementById('showPrev');
  const next = document.getElementById('showNext');

  if (stage) {
    const phones = Array.from(stage.querySelectorAll('.phone'));
    let current = 0;

    function centreOn(index, smooth) {
      const phone = phones[index];
      if (!phone) return;
      // Centre the target within the stage rather than scrollBy'ing a guessed
      // step, so the active slide lines up exactly however wide the phones are.
      const left = phone.offsetLeft - (stage.clientWidth - phone.offsetWidth) / 2;
      stage.scrollTo({ left: left, behavior: smooth && !reduce ? 'smooth' : 'auto' });
    }

    // A video only gets a src the first time it becomes active, so nothing is
    // fetched for slides the visitor never reaches. A phone with no data-src has
    // no clip yet — it keeps showing its poster and the carousel still works, so
    // the section degrades to exactly what it was before rather than 404ing.
    function play(index) {
      phones.forEach((phone, i) => {
        const video = phone.querySelector('.phone-video');
        phone.classList.toggle('is-active', i === index);
        if (!video || !video.dataset.src) return;

        if (i === index) {
          if (!video.src && video.dataset.src) video.src = video.dataset.src;
          // Autoplay is refused in some contexts and rejects; the poster stays,
          // so swallow it rather than throwing.
          const attempt = video.play();
          if (attempt && attempt.catch) attempt.catch(() => {});
        } else {
          video.pause();
          if (video.currentTime) video.currentTime = 0;
        }
      });
    }

    function goTo(index, smooth) {
      current = (index + phones.length) % phones.length;
      centreOn(current, smooth);
      if (!reduce) play(current);
    }

    // Auto-advance when a clip finishes.
    phones.forEach((phone, i) => {
      const video = phone.querySelector('.phone-video');
      if (video) video.addEventListener('ended', () => { if (i === current) goTo(current + 1, true); });
      // Clicking a phone makes it the active slide.
      phone.addEventListener('click', () => goTo(i, true));
    });

    if (prev) prev.addEventListener('click', () => goTo(current - 1, true));
    if (next) next.addEventListener('click', () => goTo(current + 1, true));

    // Only start once the carousel is actually on screen, and stop when it is not,
    // so a video is never playing off-screen.
    const showObserver = new IntersectionObserver(
      entries => entries.forEach(en => {
        if (reduce) return;
        if (en.isIntersecting) play(current);
        else phones.forEach(p => {
          const v = p.querySelector('.phone-video');
          if (v) v.pause();
        });
      }),
      { threshold: 0.35 }
    );
    showObserver.observe(stage);
  }

  /* ---------------- FAQ smooth open/close ---------------- */

  // <details> snaps open — there is no native way to transition it. Drive the
  // panel height ourselves. Sits before the GSAP block's early return so this
  // still runs under prefers-reduced-motion, just without the tween.
  document.querySelectorAll('.faq-list details').forEach(item => {
    const summary = item.querySelector('summary');
    const panel = item.querySelector('p');
    if (!summary || !panel) return;

    let anim = null;

    summary.addEventListener('click', e => {
      e.preventDefault();

      if (reduce) {
        item.open = !item.open;
        return;
      }
      if (anim) anim.cancel();

      const opening = !item.open;
      // Height has to be measured with the panel rendered, so open first and
      // animate from zero when opening.
      if (opening) item.open = true;

      const pad = getComputedStyle(panel).paddingBottom;
      const full = panel.scrollHeight + 'px';

      const from = { height: opening ? '0px' : full, paddingBottom: opening ? '0px' : pad, opacity: opening ? 0 : 1 };
      const to   = { height: opening ? full : '0px', paddingBottom: opening ? pad : '0px', opacity: opening ? 1 : 0 };

      anim = panel.animate([from, to], {
        duration: opening ? 380 : 300,
        easing: 'cubic-bezier(.22,1,.36,1)'
      });

      anim.onfinish = () => {
        if (!opening) item.open = false;
        panel.style.height = '';
        anim = null;
      };
    });
  });

  /* ---------------- Calendly booking modal ---------------- */

  const calModal = document.getElementById('calModal');

  if (calModal) {
    const calEmbed = document.getElementById('calEmbed');
    const calPanel = calModal.querySelector('.cal-panel');
    let lastFocus = null;
    let requested = false;

    function calFallback() {
      const url = (calEmbed.dataset.url || '').split('?')[0];
      calEmbed.innerHTML =
        '<div class="cal-fallback"><p>The booking widget could not load.</p>' +
        '<a href="' + url + '" target="_blank" rel="noopener">Open the booking page &rarr;</a>' +
        '<a href="mailto:hello@hano.studios">Or email hello@hano.studios</a></div>';
    }

    // Fetched on first open only — visitors who never book pay nothing for it.
    function loadCalendly() {
      if (requested) return;
      requested = true;

      const css = document.createElement('link');
      css.rel = 'stylesheet';
      css.href = 'https://assets.calendly.com/assets/external/widget.css';
      document.head.appendChild(css);

      const script = document.createElement('script');
      script.src = 'https://assets.calendly.com/assets/external/widget.js';
      script.async = true;
      script.onload = () => {
        if (window.Calendly && calEmbed.dataset.url) {
          window.Calendly.initInlineWidget({
            url: calEmbed.dataset.url,
            parentElement: calEmbed
          });
        } else {
          calFallback();
        }
      };
      script.onerror = calFallback;      // blocked CDN, ad blocker, offline
      document.head.appendChild(script);
    }

    function openCal(returnTo) {
      lastFocus = returnTo;
      calModal.hidden = false;
      requestAnimationFrame(() => calModal.classList.add('is-open'));
      document.body.style.overflow = 'hidden';
      setPageInert(true, [calModal]);
      loadCalendly();
      const close = calModal.querySelector('.cal-close');
      if (close) close.focus();
      if (window.plausible) window.plausible('Booking opened');
    }

    function closeCal() {
      calModal.classList.remove('is-open');
      document.body.style.overflow = '';
      setPageInert(false, []);
      if (lastFocus) lastFocus.focus();
      window.setTimeout(() => { calModal.hidden = true; }, reduce ? 0 : 300);
    }

    document.querySelectorAll('[data-calendly]').forEach(trigger => {
      trigger.addEventListener('click', e => {
        e.preventDefault();
        // Stop the overlay's own link handler from also running — it would
        // clear the inert state this modal is about to set.
        e.stopPropagation();
        const fromMenu = menuOverlay.contains(trigger);
        if (isMenuOpen()) toggleMenu(false, false);
        // A trigger inside the menu is inert once the menu closes, so send
        // focus back to the menu button instead.
        openCal(fromMenu ? menuBtn : trigger);
      });
    });

    calModal.addEventListener('click', e => {
      if (e.target.hasAttribute('data-cal-close')) closeCal();
    });

    document.addEventListener('keydown', e => {
      if (calModal.hidden) return;

      if (e.key === 'Escape') {
        closeCal();
        return;
      }
      if (e.key !== 'Tab') return;

      const items = Array.from(calPanel.querySelectorAll(FOCUSABLE));
      if (!items.length) return;
      const first = items[0];
      const last = items[items.length - 1];
      const active = document.activeElement;

      if (!calPanel.contains(active)) {
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
  }

  /* ---------------- GSAP scroll sequences ---------------- */

  if (!hasGSAP || reduce) return;

  // Hero sequence, one pinned timeline (Figma frames 1 -> 151 -> 152):
  //   0.00-0.30  tagline, nav and logomark fade; the title rises from the bottom
  //              of the hero to the vertical centre of the screen
  //   0.26-0.62  the title divides — HANO left, STUDIOS right — blurring out
  //   0.24-1.00  the square fades in between them, untwists from its kite, and
  //              grows past the viewport diagonal carrying the next section's
  //              gradient, until the words are gone and it covers the screen
  //
  // The hero title IS the splitting element — there is no second copy of the
  // words in a separate section any more.
  const heroSquare = document.querySelector('.hero-square');
  const heroTitle = document.getElementById('heroTitle');

  if (heroSquare && heroTitle && hero) {
    // How far the title must travel to sit on the viewport's centre line.
    const toCentre = () => {
      const r = heroTitle.getBoundingClientRect();
      const centreOfTitle = r.top + window.scrollY + r.height / 2;
      const heroTop = hero.getBoundingClientRect().top + window.scrollY;
      return (window.innerHeight / 2) - (centreOfTitle - heroTop);
    };
    const coverScale = () => {
      const size = heroSquare.offsetWidth || 1;
      return (Math.hypot(window.innerWidth, window.innerHeight) / size) * 1.08;
    };

    const heroTL = gsap.timeline({
      scrollTrigger: {
        trigger: hero,
        start: 'top top',
        end: () => '+=' + window.innerHeight * 1.7,
        scrub: 0.6,
        pin: true,
        pinSpacing: true,
        anticipatePin: 0,
        invalidateOnRefresh: true
      }
    });

    heroTL
      .to('.hero-tagline', { opacity: 0, y: -40, ease: 'none', duration: 0.24 }, 0)
      .to('.hero-mark',    { opacity: 0, ease: 'none', duration: 0.24 }, 0)
      .to('.hero-nav',     { opacity: 0, y: 30, ease: 'none', duration: 0.22 }, 0)
      // Title climbs to the middle of the screen before anything divides.
      .to(heroTitle, { y: toCentre, ease: 'none', duration: 0.3 }, 0)
      // Then the two words part. They start at their natural positions so the
      // headline reads "HANO STUDIOS." right up until it divides.
      .fromTo('.ht-a',
        { xPercent: 0, filter: 'blur(0px)', opacity: 1 },
        { xPercent: -92, filter: 'blur(9px)', opacity: 0, ease: 'none', duration: 0.36 }, 0.26)
      .fromTo('.ht-b',
        { xPercent: 0, filter: 'blur(0px)', opacity: 1 },
        { xPercent: 92, filter: 'blur(9px)', opacity: 0, ease: 'none', duration: 0.36 }, 0.26)
      // Square appears between them as they go, then takes the screen. Scale is
      // one continuous tween so it never dips; rotation runs alongside.
      .fromTo(heroSquare,
        { opacity: 0, scale: 0.22 },
        { opacity: 1, ease: 'none', duration: 0.1 }, 0.24)
      .fromTo(heroSquare,
        { rotate: -42 },
        { rotate: 0, ease: 'none', duration: 0.42 }, 0.24)
      .fromTo(heroSquare,
        { scale: 0.22, borderRadius: '10px' },
        { scale: coverScale, borderRadius: '0px', ease: 'none', duration: 0.74 }, 0.24);
  }

  // Statement copy: the block pins, its lines reveal one per scroll step, then it
  // floats up and releases into the client grid. Lines are staggered across the
  // first 70% of the pin so the last one lands before the float begins.
  const statementPin = document.getElementById('statementPin');
  const scLines = document.querySelectorAll('.sc-line > span');

  if (statementPin && scLines.length) {
    const stTL = gsap.timeline({
      scrollTrigger: {
        trigger: statementPin,
        start: 'center center',
        end: () => '+=' + window.innerHeight * 1.5,
        scrub: 0.55,
        pin: true,
        pinSpacing: true,
        anticipatePin: 0,
        invalidateOnRefresh: true
      }
    });

    const step = 0.7 / scLines.length;
    scLines.forEach((line, i) => {
      stTL.fromTo(line,
        { yPercent: 105, opacity: 0 },
        { yPercent: 0, opacity: 1, ease: 'power2.out', duration: step * 0.9 },
        i * step);
    });

    // Float to the top of the pin once every line has landed.
    stTL.to('.statement-copy', { yPercent: -14, ease: 'none', duration: 0.28 }, 0.72);
  }

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
        // anticipatePin pins early based on scroll velocity, which made the
        // Works panel jump over the client logos on a fast scroll. Off.
        scrub: 0.6,
        pin: '.works-pin',
        pinSpacing: true,
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

  // Team panel grows out of the white services section — a narrow rounded card
  // at the bottom of the viewport that widens to full bleed as it scrolls up.
  // Default CSS is the finished state, so no GSAP means no broken half-state.
  if (document.querySelector('.team-riser')) {
    gsap.fromTo('.team',
      { width: '64%', borderTopLeftRadius: '44px', borderTopRightRadius: '44px' },
      {
        width: '100%',
        borderTopLeftRadius: '0px',
        borderTopRightRadius: '0px',
        ease: 'none',
        scrollTrigger: {
          trigger: '.team-riser',
          start: 'top 95%',
          end: 'top 22%',
          scrub: 0.7,
          invalidateOnRefresh: true
        }
      }
    );
  }

  // Showcase carousel drifts as the section passes, so the phones read as a
  // moving strip rather than a static row.
  const showcaseStage = document.getElementById('showStage');
  if (showcaseStage) {
    gsap.fromTo(showcaseStage,
      { x: () => Math.min(160, window.innerWidth * 0.10) },
      {
        x: () => -Math.min(160, window.innerWidth * 0.10),
        ease: 'none',
        scrollTrigger: {
          trigger: '.showcase',
          start: 'top bottom',
          end: 'bottom top',
          scrub: 0.8,
          invalidateOnRefresh: true
        }
      }
    );
  }

  // Footer watermark rises into place. A horizontal parallax was the wrong move
  // once the mark was sized to fit inside the page margins — with no overflow
  // there is nothing to reveal, so sideways travel just read as a wobble.
  // .footer already clips, so the mark climbs out from behind the bottom edge.
  // Default CSS is the settled state, so no GSAP leaves it in place and visible.
  gsap.fromTo('.footer-mark',
    { yPercent: 42, opacity: 0 },
    {
      yPercent: 0,
      opacity: 1,
      ease: 'none',
      scrollTrigger: { trigger: '.footer', start: 'top 82%', end: 'bottom bottom', scrub: 0.6 }
    }
  );

  window.addEventListener('load', () => ScrollTrigger.refresh());
})();
