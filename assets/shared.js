/* Shared nav + footer injection. Pages set window.DT_PAGE for active state. */
(function(){
  const base = (window.DT_BASE || '');
  const page = window.DT_PAGE || '';
  const logoSvg = `<svg viewBox="0 0 24 24" fill="none" stroke="#8CC63F" stroke-width="1.8"><circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="2.2" fill="#8CC63F"/><circle cx="21" cy="12" r="1.6" fill="#8CC63F" stroke="none"/></svg>`;
  const brand = `<a href="${base}index.html" class="brand nav__brand"><span class="brand__mark">${logoSvg}</span><span>Digital<span class="brand__accent">theory</span></span></a>`;

  const practices = [
    ['revenue-services','Revenue Services','The flagship — outcome-priced growth agents'],
    ['strategy','Strategy & Intelligence','Decision-grade answers in five business days'],
    ['brand','Brand & Influence','Being known is now a ranking factor'],
    ['implementation','Implementation & Systems','Agents + SAP B1, Odoo, Salesforce, SFMC'],
    ['engineering','Product & Platform Engineering','Measured conversion lift, published numbers'],
  ];
  const proof = [
    ['case-studies','Case Studies'],
    ['our-work','Our Work'],
    ['blog','Blog'],
  ];

  const navHtml = `
  <header class="nav">
    <div class="container nav__inner">
      ${brand}
      <nav>
        <ul class="nav__links">
          <li class="has-mega">
            <button class="nav__item ${page==='practices'?'is-active':''}" type="button">Practices <svg class="nav__caret" viewBox="0 0 12 12" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 4.5l3 3 3-3"/></svg></button>
            <div class="nav__mega">
              <div class="nav__mega-inner">
                <ul class="nav__mega-list">
                  ${practices.slice(0,3).map(p=>`<li><a href="${base}${p[0]}.html">${p[1]}</a></li>`).join('')}
                </ul>
                <ul class="nav__mega-list">
                  ${practices.slice(3).map(p=>`<li><a href="${base}${p[0]}.html">${p[1]}</a></li>`).join('')}
                  <li><a href="${base}labs.html" style="color:var(--lime-400)">Digital Theory Labs →</a></li>
                </ul>
                <div class="nav__mega-quote">
                  <div class="nav__mega-quote__mark">"</div>
                  <p>Five practices, one operating model — AI agents built into your business, priced on the number they move.</p>
                  <span class="nav__mega-quote__name">The Growth Engine</span>
                  <span class="nav__mega-quote__role">2-hour audit · 5-day blueprint · 30-day deploy</span>
                </div>
              </div>
            </div>
          </li>
          <li><a href="${base}labs.html" class="nav__item ${page==='labs'?'is-active':''}">Labs</a></li>
          <li><a href="${base}pricing.html" class="nav__item ${page==='pricing'?'is-active':''}">Pricing</a></li>
          <li>
            <button class="nav__item ${page==='proof'?'is-active':''}" type="button">Proof <svg class="nav__caret" viewBox="0 0 12 12" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 4.5l3 3 3-3"/></svg></button>
            <ul class="nav__dropdown">
              ${proof.map(p=>`<li><a href="${base}${p[0]}.html">${p[1]}</a></li>`).join('')}
            </ul>
          </li>
          <li><a href="${base}company.html" class="nav__item ${page==='company'?'is-active':''}">Company</a></li>
        </ul>
      </nav>
      <div class="nav__right">
        <a href="${base}audit.html" class="btn btn--primary btn--sm">Book the 2-hour Growth Audit <span class="btn__arrow">→</span></a>
        <button class="nav__mobile" type="button" id="navMobileBtn" aria-label="Open menu">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 6h16M4 12h16M4 18h16"/></svg>
        </button>
      </div>
    </div>
  </header>
  <div class="nav__mobile-panel" id="navMobilePanel">
    <ul>
      <li><details><summary>Practices</summary><ul>
        ${practices.map(p=>`<li><a href="${base}${p[0]}.html">${p[1]}</a></li>`).join('')}
      </ul></details></li>
      <li><a href="${base}labs.html">Digital Theory Labs</a></li>
      <li><a href="${base}pricing.html">Pricing</a></li>
      <li><details><summary>Proof</summary><ul>
        ${proof.map(p=>`<li><a href="${base}${p[0]}.html">${p[1]}</a></li>`).join('')}
      </ul></details></li>
      <li><a href="${base}company.html">Company</a></li>
      <li><a href="${base}audit.html">Book the 2-hour Growth Audit</a></li>
    </ul>
  </div>`;

  const footerHtml = `
  <footer class="footer">
    <div class="container">
      <div class="footer__top">
        <div>
          <span class="brand footer__brand"><span class="brand__mark">${logoSvg}</span><span>Digital<span class="brand__accent">theory</span></span></span>
          <p class="footer__desc">AI growth and business transformation for mid-market companies. We engineer growth — and take our fee from the growth we create.</p>
          <p class="footer__cities">Bengaluru · Mumbai · India</p>
        </div>
        <div class="footer__col">
          <h4>Practices</h4>
          <ul>${practices.map(p=>`<li><a href="${base}${p[0]}.html">${p[1]}</a></li>`).join('')}</ul>
        </div>
        <div class="footer__col">
          <h4>Company</h4>
          <ul>
            <li><a href="${base}labs.html">Digital Theory Labs</a></li>
            <li><a href="${base}pricing.html">Pricing</a></li>
            <li><a href="${base}company.html">About</a></li>
            <li><a href="${base}case-studies.html">Case Studies</a></li>
            <li><a href="${base}blog.html">Blog</a></li>
            <li><a href="${base}careers.html">Careers</a></li>
          </ul>
        </div>
        <div class="footer__col">
          <h4>Start here</h4>
          <ul>
            <li><a href="${base}audit.html" style="color:var(--lime-400)">The 2-hour Growth Audit →</a></li>
            <li style="color:var(--fg-faint);font-size:13px;line-height:1.5">₹75,000, credited in full against any engagement signed within 30 days.</li>
            <li><a href="mailto:hello@digitaltheory.co.in">hello@digitaltheory.co.in</a></li>
          </ul>
        </div>
      </div>
      <div class="footer__bottom">
        <p>© 2026 Digital Theory</p>
        <p>We engineer growth.</p>
      </div>
    </div>
  </footer>`;

  const navMount = document.getElementById('dt-nav');
  const footMount = document.getElementById('dt-footer');
  if (navMount) {
    const splitIdx = navHtml.indexOf('</header>') + '</header>'.length;
    const headerStr = navHtml.slice(0, splitIdx);
    const panelStr = navHtml.slice(splitIdx);
    navMount.outerHTML = headerStr;
    document.body.insertAdjacentHTML('afterbegin', panelStr);
  }
  if (footMount) footMount.outerHTML = footerHtml;

  const btn = document.getElementById('navMobileBtn');
  const panel = document.getElementById('navMobilePanel');
  if (btn && panel) {
    btn.addEventListener('click', () => panel.classList.toggle('open'));
    panel.addEventListener('click', (e) => { if (e.target.tagName === 'A') panel.classList.remove('open'); });
  }
})();
