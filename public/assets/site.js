(function () {
  // Mobile menu
  var toggle = document.querySelector('.menu-toggle');
  var nav = document.getElementById('nav');
  if (toggle && nav) {
    toggle.addEventListener('click', function () {
      var open = nav.classList.toggle('open');
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
  }

  // Indicative facility estimator
  var slider = document.getElementById('stock');
  if (slider) {
    var steps = [25000, 50000, 75000, 100000, 150000, 200000, 250000, 300000, 400000, 500000, 750000, 1000000, 1500000, 2000000, 3000000, 5000000];
    var fmt = function (n) {
      if (n >= 1000000) return '£' + (n / 1000000).toFixed(n % 1000000 ? 1 : 0).replace('.0', '') + 'm';
      return '£' + Math.round(n / 1000) + 'k';
    };
    var valueEl = document.getElementById('stock-out');
    var rangeEl = document.getElementById('facility-out');
    var update = function () {
      var v = steps[+slider.value];
      valueEl.textContent = fmt(v) + (+slider.value === steps.length - 1 ? '+' : '');
      rangeEl.textContent = fmt(v * 0.5) + ' – ' + fmt(v * 0.7);
      slider.setAttribute('aria-valuetext', fmt(v) + ' of stock');
    };
    slider.max = steps.length - 1;
    slider.addEventListener('input', update);
    update();
  }

  // Enquiry forms (Netlify Forms, submitted in place)
  document.querySelectorAll('form[data-netlify]').forEach(function (form) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var old = form.querySelector('.form-error');
      if (old) old.remove();
      var missing = Array.prototype.filter.call(form.querySelectorAll('[required]'), function (el) { return !el.value.trim(); });
      if (missing.length) {
        var msg = document.createElement('p');
        msg.className = 'form-error';
        msg.setAttribute('role', 'alert');
        msg.textContent = 'Add your name, company and phone number so we can call you back.';
        form.appendChild(msg);
        missing[0].focus();
        return;
      }
      var btn = form.querySelector('button[type=submit]');
      var label = btn.textContent;
      btn.disabled = true;
      btn.textContent = 'Sending…';
      fetch('/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: new URLSearchParams(new FormData(form)).toString()
      }).then(function (r) {
        if (!r.ok) throw new Error('send failed');
        form.style.display = 'none';
        var done = form.parentNode.querySelector('.form-done');
        if (done) { done.style.display = 'block'; done.focus(); }
        if (typeof gtag === 'function') gtag('event', 'generate_lead', { form_name: form.getAttribute('name'), page_path: location.pathname });
      }).catch(function () {
        btn.disabled = false;
        btn.textContent = label;
        var msg = document.createElement('p');
        msg.className = 'form-error';
        msg.setAttribute('role', 'alert');
        msg.textContent = 'Your enquiry didn’t send. Try again, or call 01392 241669.';
        form.appendChild(msg);
      });
    });
  });

  // Cookie notice — analytics only runs once accepted
  var KEY = 'sf-analytics-consent';
  var stored = null;
  try { stored = localStorage.getItem(KEY); } catch (e) {}
  var grant = function () { if (typeof gtag === 'function') gtag('consent', 'update', { analytics_storage: 'granted' }); };
  if (stored === 'granted') grant();
  var box = document.getElementById('cookie');
  if (box && !stored) {
    box.style.display = 'block';
    box.querySelector('[data-accept]').addEventListener('click', function () {
      try { localStorage.setItem(KEY, 'granted'); } catch (e) {}
      grant();
      box.style.display = 'none';
    });
    box.querySelector('[data-decline]').addEventListener('click', function () {
      try { localStorage.setItem(KEY, 'denied'); } catch (e) {}
      box.style.display = 'none';
    });
  }
})();
