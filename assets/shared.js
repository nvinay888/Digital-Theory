/* Shared nav + footer injection. Pages set window.DT_PAGE = 'services' etc. for active state. */
(function(){
  const base = (window.DT_BASE || '');
  const page = window.DT_PAGE || '';
  const logoSvg = `<svg viewBox="0 0 24 24" fill="none" stroke="#8CC63F" stroke-width="1.8"><circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="2.2" fill="#8CC63F"/><circle cx="21" cy="12" r="1.6" fill="#8CC63F" stroke="none"/></svg>`;
  const brand = `<a href="${base}index.html" class="brand nav__brand"><span class="brand__mark">${logoSvg}</span><span>Digital<span class="brand__accent">theory</span></span></a>`;

  const services = [
    ['performance-marketing','Performance Marketing'],
    ['branding','Branding'],
    ['web-development','Web Development'],
    ['app-development','App Development'],
    ['business-consulting','Business Consulting'],
    ['seo','SEO'],
    ['digital-transformation','Digital Transformation'],
    ['crm-retention','CRM & Retention'],
  ];
  const industries = [
    ['D2C & E-commerce','d2c'],
    ['Beauty & Personal Care','bpc'],
    ['Edtech','edtech'],
    ['Consumer Apps','apps'],
    ['Real-money Gaming','gaming'],
    ['Retail & Pharma','retail'],
    ['SaaS & B2B Tech','saas'],
  ];

  const navHtml = `
  <header class="nav">
    <div class="container nav__inner">
      ${brand}
      <nav>
        <ul class="nav__links">
          <li class="has-mega">
            <button class="nav__item ${page==='services'?'is-active':''}" type="button">Services <svg class="nav__caret" viewBox="0 0 12 12" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 4.5l3 3 3-3"/></svg></button>
            <div class="nav__mega">
              <div class="nav__mega-inner">
                <ul class="nav__mega-list">
                  ${services.slice(0,5).map(s=>`<li><a href="${base}services/${s[0]}.html">${s[1]}</a></li>`).join('')}
                </ul>
                <ul class="nav__mega-list">
                  ${services.slice(5).map(s=>`<li><a href="${base}services/${s[0]}.html">${s[1]}</a></li>`).join('')}
                  <li><a href="${base}services.html" style="color:var(--lime-400)">All services →</a></li>
                </ul>
                <div class="nav__mega-quote">
                  <div class="nav__mega-quote__mark">"</div>
                  <p>We engaged with Digitaltheory for branding and performance marketing. They helped us scale our performance marketing with remarkable results.</p>
                  <span class="nav__mega-quote__name">Sumit Singh</span>
                  <span class="nav__mega-quote__role">VP Marketing, Codingal</span>
                </div>
              </div>
            </div>
          </li>
          <li class="has-mega">
            <button class="nav__item" type="button">Industry <svg class="nav__caret" viewBox="0 0 12 12" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 4.5l3 3 3-3"/></svg></button>
            <div class="nav__mega">
              <div class="nav__mega-inner">
                <ul class="nav__mega-list">
                  ${industries.slice(0,4).map(i=>`<li><a href="${base}case-studies.html">${i[0]}</a></li>`).join('')}
                </ul>
                <ul class="nav__mega-list">
                  ${industries.slice(4).map(i=>`<li><a href="${base}case-studies.html">${i[0]}</a></li>`).join('')}
                </ul>
                <div class="nav__mega-quote">
                  <div class="nav__mega-quote__mark">"</div>
                  <p>We engaged with Digitaltheory for D2C business. They helped us improve our profits by 3x with NPD, operations, website maintenance and performance marketing.</p>
                  <span class="nav__mega-quote__name">Abhijeet</span>
                  <span class="nav__mega-quote__role">Marketing Head, Chumbak</span>
                </div>
              </div>
            </div>
          </li>
          <li><a href="${base}case-studies.html" class="nav__item ${page==='work'?'is-active':''}">Our Work</a></li>
          <li><a href="${base}about.html" class="nav__item ${page==='about'?'is-active':''}">About Us</a></li>
          <li><a href="${base}careers.html" class="nav__item ${page==='careers'?'is-active':''}">Careers</a></li>
          <li>
            <button class="nav__item" type="button">Resources <svg class="nav__caret" viewBox="0 0 12 12" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 4.5l3 3 3-3"/></svg></button>
            <ul class="nav__dropdown">
              <li><a href="#">Blogs</a></li>
              <li><a href="${base}case-studies.html">Case Studies</a></li>
              <li><a href="#">Podcasts</a></li>
              <li><a href="#">Web Stories</a></li>
            </ul>
          </li>
        </ul>
      </nav>
      <div class="nav__right">
        <a href="${base}contact.html" class="btn btn--primary btn--sm">Contact Us <span class="btn__arrow">→</span></a>
        <button class="nav__mobile" type="button" id="navMobileBtn" aria-label="Open menu">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 6h16M4 12h16M4 18h16"/></svg>
        </button>
      </div>
    </div>
  </header>
  <div class="nav__mobile-panel" id="navMobilePanel">
    <ul>
      <li><details><summary>Services</summary><ul>
        ${services.map(s=>`<li><a href="${base}services/${s[0]}.html">${s[1]}</a></li>`).join('')}
      </ul></details></li>
      <li><details><summary>Industry</summary><ul>
        ${industries.map(i=>`<li><a href="${base}case-studies.html">${i[0]}</a></li>`).join('')}
      </ul></details></li>
      <li><a href="${base}case-studies.html">Our Work</a></li>
      <li><a href="${base}about.html">About Us</a></li>
      <li><a href="${base}careers.html">Careers</a></li>
      <li><a href="${base}contact.html">Contact Us</a></li>
    </ul>
  </div>`;

  const footerHtml = `
  <footer class="footer">
    <div class="container">
      <div class="footer__top">
        <div>
          <span class="brand footer__brand"><span class="brand__mark">${logoSvg}</span><span>Digital<span class="brand__accent">theory</span></span></span>
          <p class="footer__desc">A data-first growth marketing company. We help brands turn theory into durable growth.</p>
          <p class="footer__cities">Bengaluru · Mumbai · Delhi</p>
        </div>
        <div class="footer__col">
          <h4>Services</h4>
          <ul>${services.slice(0,6).map(s=>`<li><a href="${base}services/${s[0]}.html">${s[1]}</a></li>`).join('')}</ul>
        </div>
        <div class="footer__col">
          <h4>Company</h4>
          <ul>
            <li><a href="${base}about.html">About</a></li>
            <li><a href="${base}case-studies.html">Case Studies</a></li>
            <li><a href="${base}careers.html">Careers</a></li>
            <li><a href="${base}contact.html">Contact</a></li>
          </ul>
        </div>
        <div class="footer__col">
          <h4>Connect</h4>
          <ul>
            <li><a href="mailto:hello@digitaltheory.in">hello@digitaltheory.in</a></li>
            <li><a href="#">LinkedIn</a></li>
            <li><a href="#">Instagram</a></li>
          </ul>
        </div>
      </div>
      <div class="footer__bottom">
        <p>© 2026 Digitaltheory</p>
        <p>Theory, applied to growth.</p>
      </div>
    </div>
  </footer>`;

  const navMount = document.getElementById('dt-nav');
  const footMount = document.getElementById('dt-footer');
  if (navMount) {
    // Split header + mobile panel so panel becomes a body-level sibling, not nested inside header (which has backdrop-filter and breaks position:fixed children)
    const splitIdx = navHtml.indexOf('</header>') + '</header>'.length;
    const headerStr = navHtml.slice(0, splitIdx);
    const panelStr = navHtml.slice(splitIdx);
    navMount.outerHTML = headerStr;
    document.body.insertAdjacentHTML('afterbegin', panelStr);
  }
  if (footMount) footMount.outerHTML = footerHtml;

  /* Mobile nav toggle */
  const btn = document.getElementById('navMobileBtn');
  const panel = document.getElementById('navMobilePanel');
  if (btn && panel) {
    btn.addEventListener('click', () => panel.classList.toggle('open'));
    panel.addEventListener('click', (e) => { if (e.target.tagName === 'A') panel.classList.remove('open'); });
  }
})();
