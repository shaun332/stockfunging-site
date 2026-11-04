"""Builds stockfunding.co.uk into ./public from the page files in ./_src.

Each file in _src/pages has a JSON header (between the first two '---' lines)
followed by the page body HTML. Run:  python3 build.py
"""
import json, pathlib, re, datetime

ROOT = pathlib.Path(__file__).parent
SRC = ROOT / "_src" / "pages"
OUT = ROOT / "public"
SITE = "https://stockfunding.co.uk"
GA = "G-BWWEYZJKR3"
YEAR = datetime.date.today().year

NAV = [
    ("/stock-finance/", "Stock finance"),
    ("/motor-trade-stocking-finance/", "Motor trade"),
    ("/guides/", "Guides"),
    ("/#about", "About us"),
]

ORG_LD = {
    "@context": "https://schema.org",
    "@type": "FinancialService",
    "name": "Stock Funding",
    "logo": SITE + "/assets/logo.svg",
    "url": SITE + "/",
    "telephone": "+44 1392 241669",
    "areaServed": "GB",
    "address": {"@type": "PostalAddress", "streetAddress": "1 Lime Street", "addressLocality": "Moretonhampstead", "postalCode": "TQ13 8LT", "addressCountry": "GB"},
    "parentOrganization": {"@type": "Organization", "name": "AIM Financial Solutions Limited", "url": "https://www.aim-fs.co.uk/"},
}


def head(meta):
    path = meta["path"]
    lds = [ORG_LD] + meta.get("ld", [])
    ld = "\n".join('<script type="application/ld+json">%s</script>' % json.dumps(x, ensure_ascii=False) for x in lds)
    return f"""<!DOCTYPE html>
<html lang="en-GB">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{meta['title']}</title>
<meta name="description" content="{meta['description']}">
<link rel="canonical" href="{SITE}{path}">
<meta property="og:type" content="{meta.get('og_type', 'website')}">
<meta property="og:url" content="{SITE}{path}">
<meta property="og:title" content="{meta.get('og_title', meta['title'])}">
<meta property="og:description" content="{meta['description']}">
<meta property="og:site_name" content="Stock Funding">
<meta property="og:locale" content="en_GB">
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){{dataLayer.push(arguments);}}
  gtag('consent', 'default', {{ analytics_storage: 'denied', ad_storage: 'denied', ad_user_data: 'denied', ad_personalization: 'denied' }});
  gtag('js', new Date());
  gtag('config', '{GA}');
</script>
<script async src="https://www.googletagmanager.com/gtag/js?id={GA}"></script>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Raleway:wght@400;500;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/site.css">
<link rel="icon" href="/assets/favicon.svg" type="image/svg+xml">
{ld}
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
"""


def header(meta):
    links = []
    for href, label in NAV:
        cur = ' aria-current="page"' if meta["path"].startswith(href) and href.startswith("/") else ""
        links.append(f'<a href="{href}"{cur}>{label}</a>')
    return f"""<div class="strip"><div class="wrap"><span>Independent stock funding broker, comparing 150+ lenders</span><a href="tel:01392241669">Call 01392 241669</a></div></div>
<header class="site-header">
  <div class="wrap">
    <a class="brand" href="/"><img src="/assets/logo.svg" alt="Stock Funding" width="264" height="48"></a>
    <button class="menu-toggle" aria-expanded="false" aria-controls="nav" aria-label="Menu">
      <svg width="28" height="28" viewBox="0 0 28 28" aria-hidden="true"><path d="M4 8h20M4 14h20M4 20h20" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"/></svg>
    </button>
    <nav class="nav" id="nav" aria-label="Main">
      {' '.join(links)}
      <a class="btn btn-red" href="#review">Get a funding review</a>
    </nav>
  </div>
</header>
"""


def form(meta):
    pre = meta.get("form_default", "")
    opts = [("Stock finance for my business", "trading"), ("Vehicle stocking plan (motor trade)", "motor"), ("Not sure yet", "unsure")]
    o = "".join(f'<option{" selected" if k == pre else ""}>{t}</option>' for t, k in opts)
    return f"""<div class="form-card" id="review">
  <h2>{meta.get('form_title', 'Get a free stock funding review')}</h2>
  <p>Tell us a little about the business. We’ll call you back within one working day. No cost, no obligation, and no credit search to get started.</p>
  <form name="stock-funding-enquiry" method="POST" data-netlify="true" netlify-honeypot="bot-field" novalidate>
    <input type="hidden" name="form-name" value="stock-funding-enquiry">
    <input type="hidden" name="page" value="{meta['path']}">
    <p class="hidden-trap"><label>Leave this empty <input name="bot-field" tabindex="-1" autocomplete="off"></label></p>
    <div class="field"><label for="f-type-{meta['slug']}">What do you need?</label><select id="f-type-{meta['slug']}" name="funding-type">{o}</select></div>
    <div class="field"><label for="f-value-{meta['slug']}">Approximate stock value <span>(optional)</span></label>
      <select id="f-value-{meta['slug']}" name="stock-value"><option value="">Choose a range</option><option>Under £50,000</option><option>£50,000 – £150,000</option><option>£150,000 – £500,000</option><option>£500,000 – £1m</option><option>Over £1m</option></select></div>
    <div class="field-pair">
      <div class="field"><label for="f-name-{meta['slug']}">Your name</label><input id="f-name-{meta['slug']}" name="full-name" autocomplete="name" required></div>
      <div class="field"><label for="f-co-{meta['slug']}">Company</label><input id="f-co-{meta['slug']}" name="company-name" autocomplete="organization" required></div>
    </div>
    <div class="field-pair">
      <div class="field"><label for="f-tel-{meta['slug']}">Phone</label><input id="f-tel-{meta['slug']}" type="tel" name="phone" autocomplete="tel" required></div>
      <div class="field"><label for="f-mail-{meta['slug']}">Email <span>(optional)</span></label><input id="f-mail-{meta['slug']}" type="email" name="email" autocomplete="email"></div>
    </div>
    <button type="submit" class="btn btn-indigo">Request my funding review</button>
    <p class="form-small">We only use your details to respond to your enquiry. See our <a href="https://www.aim-fs.co.uk/privacy-policy/">privacy policy</a>.</p>
  </form>
  <div class="form-done" tabindex="-1" role="status">
    <h3>Thanks — enquiry received</h3>
    <p>We’ll call you back within one working day. If it’s urgent, call <a href="tel:01392241669">01392 241669</a>.</p>
  </div>
</div>
"""


def footer():
    return f"""<footer class="site-footer">
  <div class="wrap">
    <div class="foot-grid">
      <div>
        <img class="foot-logo" src="/assets/logo-white.svg" alt="Stock Funding" width="264" height="48">
        <p>Stock and inventory finance for UK trading businesses and motor dealers, from a whole-of-market broker with a panel of 150+ lenders.</p>
        <p>Stock Funding is part of <a href="https://www.aim-fs.co.uk/">AIM Financial Solutions</a>.</p>
        <p><a href="tel:01392241669">01392 241669</a></p>
      </div>
      <div><h3>Stock funding</h3><ul>
        <li><a href="/stock-finance/">Stock finance for trading businesses</a></li>
        <li><a href="/motor-trade-stocking-finance/">Vehicle stocking finance</a></li>
        <li><a href="/guides/">Guides</a></li>
        <li><a href="#review">Free funding review</a></li></ul></div>
      <div><h3>From AIM</h3><ul>
        <li><a href="https://www.aim-fs.co.uk/invoice-factoring/">Invoice factoring</a></li>
        <li><a href="https://www.aim-fs.co.uk/invoice-discounting/">Invoice discounting</a></li>
        <li><a href="https://www.aim-fs.co.uk/asset-finance-brokers/">Asset finance</a></li>
        <li><a href="https://www.aim-fs.co.uk/business-loans/">Business loans</a></li></ul></div>
      <div><h3>Company</h3><ul>
        <li><a href="https://www.aim-fs.co.uk/about-us/">About AIM</a></li>
        <li><a href="https://www.aim-fs.co.uk/contact-us/">Contact</a></li>
        <li><a href="https://www.aim-fs.co.uk/privacy-policy/">Privacy policy</a></li>
        <li><a href="https://www.aim-fs.co.uk/cookie-policy/">Cookie policy</a></li>
        <li><a href="https://www.aim-fs.co.uk/complaints">Complaints</a></li></ul></div>
    </div>
    <div class="foot-legal">
      <p>Aim Financial Solutions Limited is an appointed representative of Legal Webb UK LTD which is authorised and regulated by the FCA. Ref: 913004.</p>
      <p>We are a credit broker, not a lender. Finance is subject to status and the lender’s assessment. Any figures on this site are indicative only. 1 Lime Street, Moretonhampstead, TQ13 8LT.</p>
      <p>© {YEAR} AIM Financial Solutions Ltd.</p>
    </div>
  </div>
</footer>
<div class="cookie" id="cookie" role="dialog" aria-label="Cookies">
  <p>We’d like to use analytics cookies to see how people use this site. They’re only set if you accept. <a href="https://www.aim-fs.co.uk/cookie-policy/">Cookie policy</a></p>
  <div class="btns"><button class="btn btn-indigo" data-accept>Accept analytics</button><button class="btn btn-line" data-decline>No thanks</button></div>
</div>
<script src="/assets/site.js" defer></script>
</body>
</html>
"""


def build():
    OUT.mkdir(exist_ok=True)
    urls = []
    for f in sorted(SRC.glob("*.html")):
        raw = f.read_text()
        _, hdr, body = raw.split("---", 2)
        meta = json.loads(hdr)
        meta["slug"] = f.stem
        body = body.replace("{{form}}", form(meta))
        html = head(meta) + header(meta) + body + footer()
        dest = OUT / meta["path"].strip("/") / "index.html" if meta["path"] != "/" else OUT / "index.html"
        if meta["path"] == "/404":
            dest = OUT / "404.html"
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(html)
        if meta["path"] != "/404":
            urls.append(meta["path"])
    today = datetime.date.today().isoformat()
    sm = "".join(f"  <url><loc>{SITE}{u}</loc><lastmod>{today}</lastmod></url>\n" for u in urls)
    (OUT / "sitemap.xml").write_text(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{sm}</urlset>\n')
    (OUT / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n")
    print("built", urls)


if __name__ == "__main__":
    build()
