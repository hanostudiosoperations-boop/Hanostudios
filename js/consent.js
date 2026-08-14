/* ============================================================
   COOKIE CONSENT
   GDPR is opt-in: analytics and marketing tags must not run until the
   visitor has actively agreed (Art. 6(1)(a)). So this file loads in the
   <head>, before any tag, and is the only thing that injects them.

   Adding a tag later means adding it to LOADERS below — never a script
   tag in the HTML, which would fire regardless of choice.
   ============================================================ */
(function () {
  'use strict';

  var STORE = 'hano-consent';
  var VERSION = 1;          /* bump to re-ask everyone after a policy change */

  /* ---- Stored choice -------------------------------------------------- */

  function read() {
    try {
      var raw = window.localStorage.getItem(STORE);
      if (!raw) return null;
      var val = JSON.parse(raw);
      /* An older schema is treated as no answer, so the notice returns. */
      if (!val || val.v !== VERSION) return null;
      return val;
    } catch (e) {
      /* Private mode / storage disabled: behave as if nothing was stored. */
      return null;
    }
  }

  function write(prefs) {
    try {
      window.localStorage.setItem(STORE, JSON.stringify({
        v: VERSION,
        analytics: !!prefs.analytics,
        marketing: !!prefs.marketing,
        at: new Date().toISOString()
      }));
    } catch (e) { /* nothing we can do; the session still applies below */ }
  }

  /* ---- Tag loaders ----------------------------------------------------
     Each runs at most once, and only for a category the visitor accepted.
     META_PIXEL_ID stays null until the site owner supplies their pixel ID
     from Meta Events Manager; with no ID the marketing loader is a no-op,
     so the switch is honest either way. -------------------------------- */

  /* "HanoAnimations Pixel", from the Hano Animations ad account's Events
     Manager. Not the test_event_code shown on that page — that one is a
     temporary debugging token and does not belong in the site. */
  var META_PIXEL_ID = '1282102860523144';

  var loaded = { analytics: false, marketing: false };

  var LOADERS = {
    analytics: function () {
      /* Plausible is cookieless and privacy-first, but it is still an
         analytics tool, so it sits behind the same switch. */
      if (document.querySelector('script[data-domain="hanostudios.xyz"]')) return;
      var s = document.createElement('script');
      s.defer = true;
      s.setAttribute('data-domain', 'hanostudios.xyz');
      s.src = 'https://plausible.io/js/script.js';
      document.head.appendChild(s);
    },

    marketing: function () {
      if (!META_PIXEL_ID) return;
      /* Standard Meta Pixel bootstrap. */
      /* eslint-disable */
      !function(f,b,e,v,n,t,s){if(f.fbq)return;n=f.fbq=function(){n.callMethod?
      n.callMethod.apply(n,arguments):n.queue.push(arguments)};if(!f._fbq)f._fbq=n;
      n.push=n;n.loaded=!0;n.version='2.0';n.queue=[];t=b.createElement(e);t.async=!0;
      t.src=v;s=b.getElementsByTagName(e)[0];s.parentNode.insertBefore(t,s)}
      (window,document,'script','https://connect.facebook.net/en_US/fbevents.js');
      /* eslint-enable */
      window.fbq('init', META_PIXEL_ID);
      window.fbq('track', 'PageView');
    }
  };

  function apply(prefs) {
    Object.keys(LOADERS).forEach(function (key) {
      if (prefs[key] && !loaded[key]) {
        loaded[key] = true;
        LOADERS[key]();
      }
    });
  }

  /* A stored acceptance applies immediately, before the UI exists. */
  var saved = read();
  if (saved) apply(saved);

  /* ---- Funnel events --------------------------------------------------
     visitor -> interested (Contact) -> booked (Lead).

     fbq only exists once marketing consent has loaded the pixel, so every
     call is guarded: without consent these are no-ops rather than errors.
     The listeners are always attached, so a visitor who accepts mid-session
     is tracked from that point on without a reload. --------------------- */

  function track(event) {
    if (typeof window.fbq !== 'function') return false;
    window.fbq('track', event);
    return true;
  }

  /* Every route to the call — the hero CTA, the footer bar, the in-copy
     link and the menu item — is a [data-calendly] trigger, so one delegated
     listener covers them all and keeps working if a page adds another.

     Registered on the CAPTURE phase: main.js's own handler calls
     stopPropagation() on these triggers (it has to, or the menu overlay's
     link handler also runs), which means a bubble-phase listener on
     document never sees the click at all. Capture runs on the way down,
     before the target's handler, so it is unaffected. */
  document.addEventListener('click', function (e) {
    var trigger = e.target.closest && e.target.closest('[data-calendly]');
    if (trigger) track('Contact');
  }, true);

  /* Calendly is embedded inline (Calendly.initInlineWidget in main.js), so
     the booking completes inside our own page and its iframe posts up to us.
     A link out to calendly.com could never report this. */
  var leadSent = false;
  window.addEventListener('message', function (e) {
    /* Only trust Calendly's own frames. */
    if (typeof e.origin !== 'string' || e.origin.indexOf('calendly.com') === -1) return;
    if (!e.data || e.data.event !== 'calendly.event_scheduled') return;
    /* Calendly can emit the event more than once for a single booking;
       Lead must count once per visit. */
    if (leadSent) return;
    leadSent = true;
    track('Lead');
  });

  /* ---- UI ------------------------------------------------------------- */

  document.addEventListener('DOMContentLoaded', function () {
    var root = document.getElementById('cookieConsent');
    if (!root) return;

    var analytics = document.getElementById('ccAnalytics');
    var marketing = document.getElementById('ccMarketing');
    var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    var card = root.querySelector('.cc-card');
    var lastFocus = null;
    var FOCUSABLE = 'a[href], button:not([disabled]), input:not([disabled])';

    function open() {
      lastFocus = document.activeElement;
      root.hidden = false;
      /* Modal: the page behind must not scroll while a choice is pending. */
      document.body.classList.add('cc-locked');
      /* Next frame, so the transition has a start value to animate from. */
      window.requestAnimationFrame(function () {
        window.requestAnimationFrame(function () { root.classList.add('is-open'); });
      });
      /* Focus after the card is painted and laid out. Inside the rAF pair the
         element is still mid-reveal and the call is dropped, which left focus
         on <body> — the dialog would then swallow the first Tab. */
      window.setTimeout(function () {
        /* The accept action, not the policy link that precedes it in the DOM:
           the dialog is here to be answered. */
        var target = card.querySelector('[data-cc="accept"]') ||
                     card.querySelector(FOCUSABLE);
        if (target) target.focus();
      }, reduce ? 0 : 60);
    }

    function close() {
      root.classList.remove('is-open');
      document.body.classList.remove('cc-locked');
      window.setTimeout(function () {
        root.hidden = true;
        root.classList.remove('is-managing');
      }, reduce ? 0 : 350);
      if (lastFocus && lastFocus.focus) lastFocus.focus();
    }

    /* Focus stays inside the dialog while it is up. There is deliberately no
       Escape handler: dismissing without choosing would leave consent
       undecided, which is the thing this dialog exists to prevent. */
    document.addEventListener('keydown', function (e) {
      if (root.hidden || e.key !== 'Tab') return;
      var items = Array.from(card.querySelectorAll(FOCUSABLE)).filter(function (el) {
        return el.offsetParent !== null;   /* skip the hidden view's controls */
      });
      if (!items.length) return;
      var first = items[0];
      var last = items[items.length - 1];
      if (!card.contains(document.activeElement)) {
        e.preventDefault();
        first.focus();
      } else if (e.shiftKey && document.activeElement === first) {
        e.preventDefault();
        last.focus();
      } else if (!e.shiftKey && document.activeElement === last) {
        e.preventDefault();
        first.focus();
      }
    });

    function save(prefs) {
      write(prefs);
      apply(prefs);
      close();
    }

    function manage(on) {
      root.classList.toggle('is-managing', on);
      if (on) {
        var current = read();
        if (analytics) analytics.checked = current ? !!current.analytics : false;
        if (marketing) marketing.checked = current ? !!current.marketing : false;
        var first = root.querySelector('.cc-panel button, .cc-panel input');
        if (first) first.focus();
      }
    }

    root.addEventListener('click', function (e) {
      var act = e.target.closest('[data-cc]');
      if (!act) return;
      e.preventDefault();

      switch (act.getAttribute('data-cc')) {
        case 'accept':                       /* accept everything offered */
          save({ analytics: true, marketing: true });
          break;
        case 'reject':                       /* essential only */
          save({ analytics: false, marketing: false });
          break;
        case 'manage':
          manage(true);
          break;
        case 'back':
          manage(false);
          break;
        case 'save':                         /* whatever the switches say */
          save({
            analytics: !!(analytics && analytics.checked),
            marketing: !!(marketing && marketing.checked)
          });
          break;
      }
    });

    /* The footer's "Cookie Settings" link reopens the panel so a choice can
       be withdrawn as easily as it was given (Art. 7(3)). */
    document.querySelectorAll('[data-cookie-settings]').forEach(function (el) {
      el.addEventListener('click', function (e) {
        e.preventDefault();
        open();
        manage(true);
      });
    });

    /* No stored answer yet — ask. */
    if (!read()) open();
  });
})();
