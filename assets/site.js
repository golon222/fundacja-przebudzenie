(function () {
  var header = document.querySelector('.site-header');
  var toggle = document.querySelector('.nav-toggle');
  var nav = document.getElementById('nav');

  function onScroll() { header.classList.toggle('scrolled', window.scrollY > 24); }
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  function setMenu(open) {
    nav.classList.toggle('open', open);
    header.classList.toggle('menu-open', open);
    toggle.setAttribute('aria-expanded', open);
    toggle.setAttribute('aria-label', open ? 'Zamknij menu' : 'Otwórz menu');
  }
  toggle.addEventListener('click', function () { setMenu(!nav.classList.contains('open')); });
  nav.addEventListener('click', function (e) { if (e.target.closest('a')) setMenu(false); });
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape') setMenu(false); });

  // Kopiowanie adresu e-mail
  document.querySelectorAll('[data-copy]').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var label = btn.querySelector('span');
      var text = btn.getAttribute('data-copy');
      function done() { label.textContent = 'Skopiowano'; setTimeout(function () { label.textContent = 'Kopiuj'; }, 2000); }
      function fallback() {
        var target = document.getElementById('mail');
        if (!target) return;
        var r = document.createRange(); r.selectNodeContents(target);
        var s = window.getSelection(); s.removeAllRanges(); s.addRange(r);
        label.textContent = 'Zaznaczono';
      }
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(text).then(done, fallback);
      } else { fallback(); }
    });
  });

  document.querySelectorAll('.year').forEach(function (el) { el.textContent = new Date().getFullYear(); });

  // Delikatne pojawianie się sekcji. Elementy widoczne od razu po wczytaniu nie są ukrywane.
  var items = [].slice.call(document.querySelectorAll('.reveal'));
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (!('IntersectionObserver' in window) || reduce) return;
  var vh = window.innerHeight;
  var pending = items.filter(function (el) { return el.getBoundingClientRect().top > vh * 0.92; });
  pending.forEach(function (el) { el.classList.add('is-hidden'); });
  var io = new IntersectionObserver(function (entries) {
    var i = 0;
    entries.forEach(function (entry) {
      if (!entry.isIntersecting) return;
      var el = entry.target;
      el.style.transitionDelay = Math.min(i++, 5) * 90 + 'ms';
      el.classList.add('is-visible');
      el.classList.remove('is-hidden');
      io.unobserve(el);
    });
  }, { rootMargin: '0px 0px -8% 0px' });
  pending.forEach(function (el) { io.observe(el); });
})();
