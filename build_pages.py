#!/usr/bin/env python3
"""Generate inner pages for the Digitaltheory site from data."""
import os, json

ROOT = os.path.dirname(os.path.abspath(__file__))
SITE_URL = "https://digitaltheory.in"   # change to your production domain

def page(title, desc, body, base="", active="", path="", seo_title=None, extra_schema=None, breadcrumbs=None):
    """
    title:        used as h1-style label and default OG title
    seo_title:    optional override for the <title> tag (used when the article headline
                  is too long for SERP but we still want it as h1)
    extra_schema: list of dicts to inject as additional JSON-LD
    breadcrumbs:  list of (name, path) tuples; auto-derived from path if None
    """
    full_title = seo_title if seo_title else f"{title} — Digitaltheory"
    canonical = f"{SITE_URL}/{path.lstrip('/')}" if path else SITE_URL + "/"
    og_image = f"{SITE_URL}/assets/og-image.png"

    # Auto-derive breadcrumbs from path if not passed
    if breadcrumbs is None:
        crumbs = [("Home", "")]
        parts = path.split('/') if path else []
        if len(parts) == 2:  # e.g. services/perf.html
            section = parts[0]
            section_label = {"services":"Services","case-studies":"Case Studies","industries":"Industries","blog":"Blog"}.get(section, section.title())
            crumbs.append((section_label, f"{section}.html" if section not in ("blog",) else f"{section}.html"))
            crumbs.append((title, path))
        elif path and path not in ("", "index.html"):
            crumbs.append((title, path))
        breadcrumbs = crumbs

    bc_items = []
    for i, (name, p) in enumerate(breadcrumbs, 1):
        item_url = SITE_URL + "/" if p == "" else f"{SITE_URL}/{p.lstrip('/')}"
        bc_items.append({"@type":"ListItem","position":i,"name":name,"item":item_url})
    bc_schema = {"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":bc_items}

    schema_blocks = [json.dumps(bc_schema, ensure_ascii=False)]
    if extra_schema:
        for s in extra_schema:
            schema_blocks.append(json.dumps(s, ensure_ascii=False))
    schema_html = "\n".join(f'<script type="application/ld+json">{s}</script>' for s in schema_blocks)

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>{full_title}</title>
<meta name="description" content="{desc}" />
<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1" />
<link rel="canonical" href="{canonical}" />
<meta property="og:type" content="website" />
<meta property="og:site_name" content="Digitaltheory" />
<meta property="og:title" content="{full_title}" />
<meta property="og:description" content="{desc}" />
<meta property="og:url" content="{canonical}" />
<meta property="og:image" content="{og_image}" />
<meta name="twitter:card" content="summary_large_image" />
<meta name="twitter:title" content="{full_title}" />
<meta name="twitter:description" content="{desc}" />
<meta name="twitter:image" content="{og_image}" />
<meta name="theme-color" content="#000000" />
<link rel="icon" href="{base}assets/favicon.svg" type="image/svg+xml" />
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link href="https://fonts.googleapis.com/css2?family=Archivo:wght@400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet" />
<link rel="stylesheet" href="{base}assets/styles.css" />
<script>window.DT_BASE = '{base}'; window.DT_PAGE = '{active}';</script>
{schema_html}
</head>
<body>
<div class="page">
<div id="dt-nav"></div>
{body}
<div id="dt-footer"></div>
</div>
<script src="{base}assets/shared.js"></script>
</body>
</html>
"""

CTA_BAND = """
<section class="section cta-final">
  <div class="container container--narrow">
    <span class="eyebrow">Come, say hello</span>
    <h2>Ready to turn data into <span class="accent">durable growth?</span></h2>
    <p class="lead">Tell us where you want to go. We'll bring the strategy, the stack and the creative to get you there.</p>
    <div class="cta-final__row">
      <a href="{base}contact.html" class="btn btn--primary btn--lg">Book a growth consult <span class="btn__arrow">→</span></a>
      <a href="{base}case-studies.html" class="btn btn--secondary btn--lg">See our work</a>
    </div>
  </div>
</section>
"""

# ====================== CASE STUDIES ======================
CASES = [
    {
        "slug": "celio", "brand": "Celio", "industry": "D2C Menswear", "budget": "Yearly Budget ₹2 Cr",
        "hero": "A French menswear heritage brand, scaled across D2C, marketplaces and retail with a unified growth engine.",
        "metrics": [("45","%","ROAS lift"),("23","%","CM3 improvement"),("17","%","Brand search lift")],
        "challenges": [
            "Celio had a strong omnichannel presence but the majority of revenue came from marketplaces and retail chains.",
            "D2C revenue was not growing as expected and unit economics on direct channels were under pressure.",
        ],
        "strategy": [
            "After a thorough audit we identified problems in Paid Search, Paid Social and D2C Operations.",
            "Proposed a <b>pricing strategy</b> that helped improve revenue with a tightened discount structure.",
            "Did deep market research and introduced <b>Shorts and Luxe jeans</b>, lifting incremental sales by 23%.",
            "Optimised performance campaigns with our creative testing framework and quadcore framework to <b>lift ROAS 45% QoQ</b>.",
            "Built a predictive analysis model for demand planning to manage OOS and maintain <b>CM3 at 23% sustainably</b>.",
            "Designed a full-funnel media mix with brand lift study, lifting brand search terms <b>17% QoQ</b>.",
            "Designed a retention strategy with RFM segmentation, lifting retention from <b>9% to 23%</b> and LTV by 21%.",
        ],
        "tags": ["Performance Marketing","CRM & Retention","Business Consulting"],
    },
    {
        "slug": "nutriglow", "brand": "Nutriglow", "industry": "Beauty & Personal Care", "budget": "Yearly Budget ₹1 Cr",
        "hero": "A 200+ SKU beauty and personal care brand turned around from YoY decline to compounding growth.",
        "metrics": [("57","%","ROAS lift"),("40","%","COGS reduction"),("14","%","CM3 improvement")],
        "challenges": [
            "Nutriglow was facing a YoY decline in sales in a hyper-competitive industry.",
            "Profits had dropped 17% YoY despite category expansion across skincare, haircare and personal care.",
        ],
        "strategy": [
            "Audited marketplaces and D2C and identified pricing gaps, non-winning SKUs and COGS leakage.",
            "Split performance budget: <b>60% on marketplace advertising, 40% on D2C website</b>.",
            "Restructured Amazon ads — introduced Sponsored Brand and Sponsored Display on bestsellers.",
            "Optimised strategic supplier sourcing, <b>cutting COGS by 40%</b> and lifting CM1.",
            "Implemented a full-funnel media mix that drove <b>35% QoQ revenue growth</b>.",
            "Helped with NPDs and a launch plan in Amazon and Flipkart, lifting revenue another 33%.",
        ],
        "tags": ["Performance Marketing","Business Consulting","Marketplace"],
    },
    {
        "slug": "codingal", "brand": "Codingal", "industry": "K-12 Edtech", "budget": "Yearly Budget ₹1 Cr",
        "hero": "Scaled a K-12 coding platform to 5L+ students with 10x revenue via international market entry.",
        "metrics": [("66","%","MQL lift"),("70","%","CAC reduction"),("34","%","Revenue lift")],
        "challenges": [
            "CAC was deteriorating 30% MoM as the Indian market saturated.",
            "High CAC was eroding cash flow and limiting growth velocity.",
        ],
        "strategy": [
            "Secondary research identified international markets with high school fees, low competition and category awareness.",
            "Piloted Meta campaigns in three countries and saw <b>CAC ~70% lower</b> than the India baseline.",
            "Scaled spend in primary international markets and expanded into Google Ads.",
            "Adopted a full-funnel media mix with brand-lift study — brand search up <b>33% QoQ</b>.",
            "Designed a sales strategy improving lead follow-ups and lifting paid customer base 15%.",
            "Revamped landing page and form fill — qualified leads up <b>37%</b>.",
            "Revamped student onboarding flow — <b>SQL jumped from 30% to 47%</b>.",
        ],
        "tags": ["Performance Marketing","CRO","International Expansion"],
    },
    {
        "slug": "laundrokart", "brand": "Laundrokart", "industry": "Consumer App (Services)", "budget": "Yearly Budget ₹2 Cr",
        "hero": "Turned a 12-year-old laundry app from declining LTV into a retention-led growth engine.",
        "metrics": [("45","%","Revenue lift"),("55","%","App installs lift"),("23","%","LTV improvement")],
        "challenges": [
            "Business was facing many unqualified users even with high install volume.",
            "LTV started to degrow QoQ, threatening unit economics.",
        ],
        "strategy": [
            "Audited the account and implemented a robust tracking system for high-intent events.",
            "Revamped channel strategy and scaled <b>app-install campaigns 55% MoM</b>.",
            "Ran event-based campaigns optimising for key in-app actions — qualified users up 37% QoQ.",
            "Experimented with affiliates on a transaction-based model — additional 15% revenue.",
            "Implemented CRM nudges across <b>push and WhatsApp</b> — retention up 17%.",
            "Ran RFM analysis on 7 years of data to identify churn risk and high-value cohorts.",
            "Targeted discounts and coupons to win back lost customers — 12% additional revenue.",
            "Designed a loyalty program for high-value customers contributing 3% of overall revenue.",
        ],
        "tags": ["App Marketing","CRM & Retention","Data Science"],
    },
    {
        "slug": "pocket52", "brand": "Pocket52", "industry": "Real-money Gaming", "budget": "Yearly Budget ₹3 Cr",
        "hero": "One of India's fastest 1M-download gaming apps — CAC cut, LTV lifted and organic ranking improved.",
        "metrics": [("45","%","CAC reduction"),("20","%","Organic installs lift"),("18","%","LTV improvement")],
        "challenges": [
            "Pocket52 was unable to reduce CAC despite scaling spend.",
            "Player LTV needed improvement and ASO was untapped.",
        ],
        "strategy": [
            "Top-down approach: segmented channel revenue share across the media mix.",
            "Scored channels on QoQ growth, LTV, ARPU and CAC — identified low-growth, high-CAC channels.",
            "Optimised Google BOF campaigns with better creatives — 3% CAC reduction.",
            "Revamped affiliate marketing framework, paused unprofitable affiliates, scaled high-value ones.",
            "Rebuilt FB targeting with LTV-based audiences — scaled profitably with <b>CAC under 17%</b>.",
            "Built rich media images, revamped description, on-page + off-page ASO — overall CAC down 45%.",
            "RFM analysis and CRM nudges lifted LTV 18%; in-app offers for loyalty customers lifted ARPU 7%.",
        ],
        "tags": ["App Marketing","ASO","CRM & Retention"],
    },
    {
        "slug": "thulasi", "brand": "Thulasi Pharmacy", "industry": "Retail Digital Transformation", "budget": "80+ branches · ₹750 Cr turnover",
        "hero": "Digitised store operations for a South Indian pharmacy chain — inventory, returns and product mix solved end-to-end.",
        "metrics": [("33","%","Inventory cost ↓"),("37","%","Returns reduction"),("19","%","Revenue improvement")],
        "challenges": [
            "Company was facing tough challenges managing inventory and SKU mix across 80+ stores.",
            "Manual fill-in and sell-out processes were error-prone and margin-eroding.",
        ],
        "strategy": [
            "Understood requirements: better inventory management and automated fill-in / sell-out.",
            "Built a <b>digitisation software</b> integrated with their ERP and an in-house inventory tool.",
            "Mapped product mix to store fit — surfaced which SKUs sell best in which branches.",
            "Built a <b>returns dashboard</b> to manage and reduce reverse logistics costs.",
            "Trained an <b>ML model</b> predicting product returns and store-level sell-through.",
        ],
        "tags": ["Digital Transformation","Data Science","Operations"],
    },
]

def render_case_body(c, prev_next):
    metrics_html = ''.join(f'<div class="stat case__metric"><div class="stat__num">{v}<span class="unit">{u}</span></div><div class="stat__label">{l}</div></div>' for v,u,l in c["metrics"])
    chips_html = '<div style="display:flex;flex-wrap:wrap;gap:8px">' + ''.join(f'<span class="case__industry">{t}</span>' for t in c["tags"]) + '</div>'
    challenges_html = ''.join(f'<li>{x}</li>' for x in c["challenges"])
    strategy_html = ''.join(f'<li>{x}</li>' for x in c["strategy"])
    prev_link = f'<a href="{prev_next[0]}.html">← Previous case</a>' if prev_next[0] else '<span></span>'
    next_link = f'<a href="{prev_next[1]}.html">Next case →</a>' if prev_next[1] else '<span></span>'
    return f"""
<section class="page-hero">
  <div class="container">
    <a href="../case-studies.html" style="font-family:var(--font-mono);font-size:12px;letter-spacing:.14em;color:var(--fg-muted);text-transform:uppercase">← All case studies</a>
    <div class="case-detail__head">
      <div>
        <span class="case-detail__chip">{c["industry"]}</span>
        <h1 class="case-detail__title">{c["brand"]}</h1>
        <p class="lead case-detail__sub">{c["hero"]}</p>
        <div style="margin-top:24px;font-family:var(--font-mono);font-size:12px;color:var(--fg-faint);letter-spacing:.08em">{c["budget"]}</div>
        <div style="margin-top:20px">{chips_html}</div>
      </div>
      <div class="case-detail__metrics">
        {''.join(f'<div class="results__cell" style="padding:24px"><div class="stat"><div class="stat__num">{v}<span class="unit">{u}</span></div><div class="stat__label">{l}</div></div></div>' for v,u,l in c["metrics"])}
      </div>
    </div>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="case-detail__split">
      <div class="case-detail__panel">
        <h2>Challenges</h2>
        <ul>{challenges_html}</ul>
      </div>
      <div class="case-detail__panel">
        <h2>Strategy &amp; execution</h2>
        <ul>{strategy_html}</ul>
      </div>
    </div>
    <div class="case-detail__nav">
      {prev_link}
      {next_link}
    </div>
  </div>
</section>

{CTA_BAND.format(base='../')}
"""

# Build case studies hub
def build_cases_hub():
    # Map each case's `industry` string to a tab category
    CAT_MAP = {
        "D2C Menswear":"D2C / E-commerce",
        "Beauty & Personal Care":"Beauty & Personal Care",
        "K-12 Edtech":"Edtech",
        "Consumer App (Services)":"Consumer Apps",
        "Real-money Gaming":"Gaming",
        "Retail Digital Transformation":"Retail & Pharma",
    }
    CAT_ORDER = ["All","D2C / E-commerce","Beauty & Personal Care","Edtech","Consumer Apps","Gaming","Retail & Pharma"]
    # Tag each case
    for c in CASES:
        c["_cat"] = CAT_MAP.get(c["industry"], "Other")
    counts = {cat: sum(1 for c in CASES if c["_cat"]==cat) for cat in CAT_ORDER[1:]}
    counts["All"] = len(CASES)
    tabs_html = "".join(
        f'<button class="work-tab {"is-active" if cat=="All" else ""}" data-tab="{cat}">{cat} <span class="work-tab__count">({counts[cat]})</span></button>'
        for cat in CAT_ORDER if counts.get(cat,0)>0 or cat=="All"
    )
    cards = ''
    for c in CASES:
        m = c["metrics"]
        cards += f'''
        <a class="case" data-cat="{c["_cat"]}" href="case-studies/{c["slug"]}.html">
          <div class="case__head"><div class="case__brand">{c["brand"]}</div><span class="case__industry">{c["industry"]}</span></div>
          <p class="case__desc">{c["hero"]}</p>
          <div class="case__budget">{c["budget"]}</div>
          <div class="case__metrics">
            <div class="stat case__metric"><div class="stat__num">{m[0][0]}<span class="unit">{m[0][1]}</span></div><div class="stat__label">{m[0][2]}</div></div>
            <div class="stat case__metric"><div class="stat__num">{m[1][0]}<span class="unit">{m[1][1]}</span></div><div class="stat__label">{m[1][2]}</div></div>
            <div class="stat case__metric"><div class="stat__num">{m[2][0]}<span class="unit">{m[2][1]}</span></div><div class="stat__label">{m[2][2]}</div></div>
          </div>
          <span class="case__link">Read case study →</span>
        </a>'''
    body = f"""
<section class="page-hero">
  <div class="container page-hero__inner">
    <span class="eyebrow">Case studies</span>
    <h1>Outcomes we've engineered, in their own words.</h1>
    <p class="lead page-hero__lead">A diverse portfolio across D2C, BPC, edtech, consumer apps, gaming and retail digital transformation — every engagement measured by the metric that mattered to the P&amp;L.</p>
  </div>
</section>

<section class="section cases">
  <div class="container">
    <div class="sec-head"><div><span class="eyebrow">Filter by industry</span><h2>Case studies by category</h2></div><p class="lead">Real ROAS, CAC, LTV and margin numbers from real engagements.</p></div>
    <div class="work-tabs" id="caseTabs">{tabs_html}</div>
    <div class="cases-grid" id="caseGrid">{cards}</div>
    <div class="work-empty" id="caseEmpty" style="display:none">No engagements in this category yet — talk to us about being the first.</div>
  </div>
</section>

{CTA_BAND.format(base='')}

<script>
(function(){{
  const tabs = document.querySelectorAll('#caseTabs .work-tab');
  const cards = document.querySelectorAll('#caseGrid .case');
  const empty = document.getElementById('caseEmpty');
  tabs.forEach(b => b.addEventListener('click', () => {{
    tabs.forEach(x => x.classList.toggle('is-active', x === b));
    const cat = b.dataset.tab;
    let visible = 0;
    cards.forEach(c => {{
      const match = cat === 'All' || c.dataset.cat === cat;
      c.style.display = match ? '' : 'none';
      if (match) visible++;
    }});
    empty.style.display = visible === 0 ? 'block' : 'none';
  }}));
}})();
</script>
"""
    return page("Case Studies — Growth Marketing Outcomes",
                "Digitaltheory case studies across D2C, beauty, edtech, consumer apps, gaming and retail. Real ROAS, CAC, LTV and margin numbers from real engagements.",
                body, base="", active="cases", path="case-studies.html",
                seo_title="Case Studies — Growth Marketing Outcomes | Digitaltheory")

# ====================== SERVICES ======================
SERVICES = [
    {
        "slug":"performance-marketing","title":"Performance Marketing",
        "hero":"Full-funnel paid acquisition engineered for compounding ROAS — across Meta, Google, Amazon and affiliates.",
        "intro":"Performance marketing isn't channels — it's a system. We pair a creative testing framework with full-funnel media planning and cohort-based attribution so every rupee is measured to LTV, not last-click.",
        "what":["Paid Search (Google, Bing)","Paid Social (Meta, LinkedIn, TikTok)","Marketplace (Amazon, Flipkart) ads","Affiliate &amp; influencer performance","Programmatic &amp; native"],
        "deliverables":[
            ("Channel strategy","Audit, hypothesis, channel mix and budget allocation grounded in your unit economics."),
            ("Creative testing framework","A repeatable system for shipping, scoring and scaling ad creative variants weekly."),
            ("Quadcore campaign architecture","Prospecting, retargeting, brand-defence and creator-led — orchestrated as one."),
            ("Weekly &amp; biweekly reviews","Transparent reporting on the metrics that move CAC, LTV and CM3."),
        ],
        "case":"celio","case_label":"Celio — 45% ROAS lift, 23% CM3 lift, 17% brand search growth.",
    },
    {
        "slug":"branding","title":"Branding",
        "seo_title":"Branding & Identity Services | Digitaltheory",
        "hero":"Build a memorable brand story that captivates audiences across every platform.",
        "intro":"Brand is the compounding asset behind performance. We build identity, positioning and creative systems that travel — from packaging to performance ads to founder LinkedIn.",
        "what":["Brand positioning &amp; narrative","Identity systems (logo, type, colour)","Packaging &amp; print","Brand films &amp; founder content","Tone of voice &amp; copy guidelines"],
        "deliverables":[
            ("Positioning workshop","Crystallise category, audience, promise and proof in a one-page narrative."),
            ("Identity system","Logo, type, colour, motion and rules that work across every surface."),
            ("Creative playbook","Templates and guardrails that let in-house teams ship on-brand at velocity."),
            ("Launch plan","Sequenced rollout across owned, earned and paid surfaces."),
        ],
        "case":"celio","case_label":"Celio — heritage brand re-energised across D2C and retail.",
    },
    {
        "slug":"web-development","title":"Web Development",
        "hero":"High-converting D2C storefronts, landing pages and marketing sites — built for speed and scale.",
        "intro":"Performance marketing dies at a slow site. We build on Shopify, Next.js and headless stacks with a CRO mindset, Core Web Vitals as a non-negotiable, and analytics baked in from day one.",
        "what":["Shopify &amp; Shopify Plus","Next.js / React headless","WordPress &amp; Webflow","Landing page systems","A/B testing &amp; CRO"],
        "deliverables":[
            ("D2C storefronts","Storefronts engineered around your AOV, attach-rate and repeat-rate goals."),
            ("Landing page system","Reusable LP modules that performance can spin up per campaign in hours, not weeks."),
            ("Analytics &amp; tracking","GA4, server-side events, CAPI and Mixpanel — wired so every channel sees the same number."),
            ("CRO program","Hypothesis pipeline, A/B testing cadence and uplift documentation."),
        ],
        "case":"codingal","case_label":"Codingal — LP &amp; onboarding revamp lifted SQL from 30% to 47%.",
    },
    {
        "slug":"app-development","title":"App Development",
        "hero":"Native and cross-platform consumer apps with ASO, in-app analytics and event-driven CRM baked in from day one.",
        "intro":"Apps are not just code — they're growth engines. We design and ship native iOS, Android and React Native apps wired for measurable retention, monetisation and organic growth.",
        "what":["iOS &amp; Android native","React Native cross-platform","ASO (app store optimisation)","In-app analytics &amp; events","Push &amp; in-app messaging"],
        "deliverables":[
            ("Product &amp; UX","Flows, prototypes and UX research grounded in installs-to-paid funnel data."),
            ("Engineering","Native and cross-platform builds, store submissions and release management."),
            ("Event taxonomy","An analytics schema that performance, product and CRM all share."),
            ("ASO program","Keyword research, creative refresh and continuous rank monitoring."),
        ],
        "case":"laundrokart","case_label":"Laundrokart — 55% installs lift, 23% LTV improvement.",
    },
    {
        "slug":"business-consulting","title":"Business Consulting",
        "hero":"Strategic counsel grounded in your P&amp;L — pricing, unit economics, NPD and channel mix.",
        "intro":"We're operators first, consultants second. Our consulting is what we'd tell you if your CAC, COGS and inventory were on our own dashboard — and it stays measurable.",
        "what":["Pricing &amp; discount strategy","Unit economics &amp; cohort analysis","NPD &amp; portfolio mix","Channel mix &amp; expansion","International market entry"],
        "deliverables":[
            ("Strategy memo","A short, sharp memo with the decisions, the reasoning and the metrics they should move."),
            ("Financial model","A working unit-economics and channel model — yours to keep and edit."),
            ("Quarterly operating rhythm","Reviews tied to the model so decisions update with reality, not lag it."),
        ],
        "case":"nutriglow","case_label":"Nutriglow — pricing &amp; NPD turnaround drove 35% QoQ growth.",
    },
    {
        "slug":"seo","title":"SEO",
        "seo_title":"SEO Services — Technical, Content & GEO | Digitaltheory",
        "hero":"Technical SEO, content engines and link strategy that lifts organic share-of-search and drives down blended CAC.",
        "intro":"SEO is the cheapest CAC lever most brands ignore. We treat it as a system — technical foundation, programmatic + editorial content, plus a real link program — and report it in the same dashboard as paid.",
        "what":["Technical SEO &amp; site audits","Programmatic SEO","Editorial content engine","Link building &amp; digital PR","Local &amp; international SEO"],
        "deliverables":[
            ("Technical audit","Crawl, indexation, schema, Core Web Vitals and information architecture."),
            ("Content engine","Topic clusters, brief templates and a publishing cadence that compounds."),
            ("Link program","Outreach, digital PR and partnerships earning the kind of links Google actually counts."),
            ("Reporting","Share-of-search, blended CAC and organic-attributed revenue in one view."),
        ],
        "case":"pocket52","case_label":"Pocket52 — ASO + content lifted organic installs 20%.",
    },
    {
        "slug":"sap-b1-implementation","title":"SAP Business One Implementation",
        "hero":"Deploy SAP Business One as the operating spine of your business — finance, sales, inventory, purchasing, MRP and analytics in one system.",
        "intro":"SAP Business One (B1) is the ERP we install when a growing business has outgrown its spreadsheets and disconnected tools. We scope, configure, migrate, integrate and train — and we stay on after go-live so the system actually gets used.",
        "what":["Finance &amp; controlling","Sales, CRM &amp; service","Inventory, warehouse &amp; logistics","Purchasing &amp; procurement","MRP &amp; production planning","Reporting, dashboards &amp; analytics","Mobile access for leadership","E-commerce, marketplace &amp; payment integrations"],
        "deliverables":[
            ("Discovery &amp; blueprint","Process mapping across finance, sales, ops and supply chain — and a phased plan to migrate them onto B1."),
            ("Configuration &amp; customisation","Chart of accounts, document flow, approval procedures, user roles, custom fields and add-on apps tailored to your business."),
            ("Data migration","Master data cleansing and migration — items, BOMs, customers, vendors, opening balances and transaction history — with reconciliation."),
            ("Integrations","Connect B1 to Shopify, Amazon, marketplaces, banks, payment gateways, WhatsApp/CRM tools and BI dashboards via DI-API or service layer."),
            ("Training &amp; change management","Role-based SOPs, user training and a hyper-care window so adoption sticks, not just the implementation."),
            ("Hyper-care &amp; AMC","Post-go-live support, version upgrades, query resolution and continuous improvement against your operating KPIs."),
        ],
        "case":"thulasi","case_label":"Thulasi — ERP-integrated digitisation cut inventory costs 33% and returns 37%.",
    },
    {
        "slug":"sfmc-implementation","title":"Salesforce Marketing Cloud Implementation",
        "hero":"Stand up Salesforce Marketing Cloud as your customer engagement engine — data, journeys, channels and AI personalisation, wired end-to-end.",
        "intro":"SFMC is powerful but only as good as how it&rsquo;s implemented. We design the data model, build the journeys, connect the channels, train the team and tie every campaign back to revenue — so the platform pays back in months, not years.",
        "what":["Journey Builder &amp; orchestration","Email Studio &amp; transactional email","Mobile Studio (SMS, push, WhatsApp)","Audience Studio &amp; segmentation","Data Cloud &amp; CDP integration","Personalization &amp; AI recommendations","Automation Studio &amp; data pipelines","Marketing Cloud Intelligence / Datorama reporting"],
        "deliverables":[
            ("Audit &amp; strategy","Audit existing CRM, CDP and channel stack. Map use cases to journeys, define the data model and prioritise the launch backlog."),
            ("Data model &amp; ingestion","Data extensions, contact model, identity resolution and feeds from your warehouse, CDP and product systems — built to scale, not to demo."),
            ("Journey design &amp; build","Welcome, browse-abandon, cart-abandon, post-purchase, win-back, VIP and lifecycle journeys — orchestrated across email, push, WhatsApp, SMS and in-app."),
            ("Personalisation &amp; AI","Einstein recommendations, send-time optimisation, content personalisation blocks and audience-level dynamic content."),
            ("Reporting &amp; attribution","Marketing Cloud Intelligence dashboards mapping campaign-level activity to LTV, retention and revenue — not opens and clicks."),
            ("Training &amp; ongoing ops","Enablement for the in-house team plus a managed-service option for ongoing campaign ops, QA and continuous improvement."),
        ],
        "case":"laundrokart","case_label":"Laundrokart — RFM-led CRM lifted retention 17% and LTV 23%.",
    },
    {
        "slug":"crm-retention","title":"CRM & Retention",
        "hero":"RFM segmentation, lifecycle journeys and loyalty programs that lift LTV — push, WhatsApp, email and in-app.",
        "intro":"Acquisition is the entrance fee; retention is the business. We build CRM programs around RFM, predictive churn and behavioural triggers — and tie them to revenue, not opens.",
        "what":["RFM segmentation &amp; cohort analysis","Lifecycle &amp; journey orchestration","WhatsApp &amp; push programs","Email &amp; SMS","Loyalty &amp; referral programs"],
        "deliverables":[
            ("Segmentation model","RFM + behavioural clusters tied to actions you can run weekly."),
            ("Journey library","Welcome, browse-abandon, post-purchase, win-back, VIP — wired across channels."),
            ("Loyalty program","Tiering, rewards and program economics that lift repeat without crushing margin."),
            ("LTV reporting","Cohort LTV, repeat rate and program-attributable revenue."),
        ],
        "case":"laundrokart","case_label":"Laundrokart — RFM-led CRM lifted retention 17% and LTV 23%.",
    },
]

def render_service_body(s):
    what_html = ''.join(f'<li>{x}</li>' for x in s["what"])
    deliverables_html = ''.join(f'<div class="deliverable"><h3>{n}</h3><p>{d}</p></div>' for n,d in s["deliverables"])
    return f"""
<section class="page-hero">
  <div class="container page-hero__inner">
    <a href="../services.html" style="font-family:var(--font-mono);font-size:12px;letter-spacing:.14em;color:var(--fg-muted);text-transform:uppercase">← All services</a>
    <span class="eyebrow" style="margin-top:24px;display:inline-flex">Service</span>
    <h1>{s["title"]}</h1>
    <p class="lead page-hero__lead">{s["hero"]}</p>
    <div class="page-hero__cta">
      <a href="../contact.html" class="btn btn--primary btn--lg">Talk to us <span class="btn__arrow">→</span></a>
      <a href="../case-studies/{s["case"]}.html" class="btn btn--secondary btn--lg">See case study</a>
    </div>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="solution__intro">
      <div class="solution__what">
        <span class="eyebrow">What we do</span>
        <h2 style="margin-top:12px;max-width:18ch">A complete {s["title"].lower()} stack, under one roof.</h2>
        <p class="lead" style="margin-top:16px">{s["intro"]}</p>
        <ul>{what_html}</ul>
      </div>
      <div>
        <div class="case-detail__panel">
          <h3>Featured outcome</h3>
          <p class="lead" style="font-size:1.05rem">{s["case_label"]}</p>
          <a href="../case-studies/{s["case"]}.html" class="btn btn--secondary">Read the case study <span class="btn__arrow">→</span></a>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="section" style="background:var(--surface-section);border-block:1px solid var(--line)">
  <div class="container">
    <div class="sec-head">
      <div><span class="eyebrow">Deliverables</span><h2>What you walk away with</h2></div>
      <p class="lead">Tangible artefacts, not slideware. Every deliverable is yours to keep, edit and operate.</p>
    </div>
    <div class="solution__deliverables">{deliverables_html}</div>
  </div>
</section>

{CTA_BAND.format(base='../')}
"""

def render_business_consulting_body():
    icon = lambda name: {
      "growth":'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M3 17l6-6 4 4 8-8"/><path d="M14 7h7v7"/></svg>',
      "entry":'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3a14 14 0 010 18M12 3a14 14 0 000 18"/></svg>',
      "economics":'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M12 1v22M17 5H9.5a3.5 3.5 0 100 7h5a3.5 3.5 0 110 7H6"/></svg>',
      "portfolio":'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="7" width="18" height="13" rx="2"/><path d="M8 7V5a2 2 0 012-2h4a2 2 0 012 2v2"/></svg>',
      "omni":'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="7" height="7" rx="1"/><rect x="14" y="3" width="7" height="7" rx="1"/><rect x="3" y="14" width="7" height="7" rx="1"/><rect x="14" y="14" width="7" height="7" rx="1"/></svg>',
      "ma":'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M16 3h5v5"/><path d="M21 3l-7 7"/><path d="M8 21H3v-5"/><path d="M3 21l7-7"/></svg>',
    }[name]
    pillars = [
        ("01","Growth Strategy","Diagnose where growth is leaking — channel, pricing, portfolio or funnel — and build the operating plan to close it.","growth"),
        ("02","New Market Entry","Validate adjacent geographies and categories before you spend. Pilot first, scale on signal.","entry"),
        ("03","Unit Economics & P&amp;L","Rebuild contribution margin from the SKU up — CM1, CM2, CM3 — and tie every decision back to it.","economics"),
        ("04","Portfolio & NPD","Score your portfolio on margin, velocity and white-space — and ship the next launch with a plan, not a hope.","portfolio"),
        ("05","Omnichannel & D2C","Solve the tension between marketplaces, retail and D2C. Each channel earns its margin or it goes.","omni"),
        ("06","M&amp;A & Diligence","Commercial diligence, target scanning and post-deal integration — built on the same operating chassis we use day-to-day.","ma"),
    ]
    pillars_html = "".join(
        f'<a class="svc-rich__card" href="../contact.html"><div class="svc-rich__cover"><div class="svc-rich__icon">{icon(ic)}</div></div><div class="svc-rich__body"><span class="svc-rich__num">{n}</span><h3 class="svc-rich__title">{t}</h3><p class="svc-rich__desc">{d}</p><span class="svc-rich__link">Explore service</span></div></a>'
        for n,t,d,ic in pillars
    )

    sectors = [
        ("d2c","D2C & E-commerce","Where pricing, channel mix and creative compound or unravel.",
         "We rebuild D2C unit economics from CM3 up — pricing strategy, marketplace vs website split, retention loops and creative testing — and tie every campaign back to LTV, not last-click.",
         ["Pricing &amp; discount architecture","Marketplace vs D2C revenue mix","Quadcore campaign architecture","RFM retention &amp; loyalty design"],
         "celio","Celio — 45% ROAS lift, 23% CM3, 17% brand search"),
        ("bpc","Beauty & Personal Care","SKU velocity, COGS leakage and channel saturation — solved at the P&amp;L level.",
         "200+ SKU portfolios live or die on contribution margin. We diagnose pricing, sourcing and channel mix; ship the right NPDs; restructure Amazon SB/SD; and drive compounding QoQ growth.",
         ["Strategic supplier sourcing &amp; COGS","NPD ideation, gating &amp; launch","Marketplace SB/SD architecture","Full-funnel media mix to LTV"],
         "nutriglow","Nutriglow — 57% ROAS, 40% COGS cut, 14% CM3 lift"),
        ("fashion","Fashion & Apparel","Seasonality, inventory and brand work as one system — or none of them work.",
         "Fashion runs on a tight clock. We pair pricing &amp; discount calendars with creative testing frameworks, retention loops and demand-led inventory planning so margin survives the season.",
         ["Seasonal pricing &amp; markdown plans","Creative testing per drop","RFM clusters by category affinity","Demand-led inventory commitment"],
         "celio","Celio — 17% brand search growth, 23% CM3"),
        ("food","Food & Beverages","Hyperlocal acquisition, perishable inventory and repeat behaviour — all on one P&amp;L.",
         "Food D2C is a retention game. We engineer acquisition by zone, build cohort-based CRM and tighten the cold-chain economics so every cohort pays back in clear weeks, not unclear quarters.",
         ["Zone-by-zone acquisition strategy","Cohort LTV &amp; payback modelling","Subscription &amp; repeat-purchase design","Last-mile / cold-chain economics"],
         None,None),
        ("electronics","Consumer Electronics","High AOV, low repeat — every conversion has to pay for itself.",
         "We optimise the funnel where it costs the most: consideration. Comparison content, finance/EMI flows, marketplace bestseller architecture and review velocity — together driving down blended CAC.",
         ["Marketplace bestseller architecture","EMI / finance attach optimisation","Review velocity &amp; UGC programmes","Cross-sell &amp; bundle design"],
         "pepperfry",None),
        ("health","Consumer Health","Trust, claims and compliance — without slowing the growth flywheel.",
         "We build acquisition that respects category constraints: claims-safe creative, founder-led content, doctor / KOL programs, and CRM journeys built around adherence and habit formation.",
         ["Claims-safe creative framework","Founder &amp; KOL content engine","Adherence &amp; habit CRM journeys","Subscription &amp; refill economics"],
         None,None),
        ("edtech","Edtech","CAC, qualified-lead share and onboarding conversion — fixed in one engagement.",
         "Edtech wins when the funnel is reengineered end-to-end: country prioritisation, landing-page CRO, sales follow-up cadence and student onboarding — all tied back to paid-customer LTV.",
         ["International market entry","Landing-page CRO programme","Sales follow-up &amp; SQL design","Onboarding flow optimisation"],
         "codingal","Codingal — 70% CAC reduction, 10x revenue"),
        ("retail","Retail & Pharma Chains","Store-level inventory, returns and mix — digitised, modelled and managed.",
         "Brick-and-mortar margin lives in the small decisions: SKU mix by store, returns prediction, fill-in / sell-out automation. We integrate ERP and ship the ML behind a digitised back-office.",
         ["SKU mix by store, by season","Returns prediction &amp; reverse logistics","Fill-in / sell-out automation","ERP integration &amp; BI"],
         "thulasi","Thulasi — 33% inventory cost reduction, 37% returns"),
    ]
    list_html = "".join(
        f'<button class="bc-sector-tab {"is-active" if i==0 else ""}" data-sec="{slug}">{title}</button>'
        for i,(slug,title,_,_,_,_,_) in enumerate(sectors)
    )
    def sector_panel(slug,title,sub,body,levers,case,case_label,active):
        levers_html = "".join(f'<li>{x}</li>' for x in levers)
        case_html = f'<a href="../case-studies/{case}.html" class="bc-sectors-panel__case">{case_label} →</a>' if case and case_label else ''
        return f'<div class="bc-sector-panel {"is-active" if active else ""}" data-sec="{slug}"><div class="bc-sectors-panel__eyebrow">Sector · {title}</div><h3>{sub}</h3><p class="bc-sectors-panel__body">{body}</p><ul class="bc-sectors-panel__levers">{levers_html}</ul>{case_html}</div>'
    panels_html = "".join(sector_panel(s,t,sub,body,levers,case,cl,i==0) for i,(s,t,sub,body,levers,case,cl) in enumerate(sectors))

    method = [
        ("01","Diagnose","Two weeks. We sit inside your data — P&amp;L, CRM, marketing platforms, inventory — and write back the three problems that actually matter."),
        ("02","Hypothesise","One week. A small set of bets, each tied to a target metric. No 40-page deck — a one-page memo and a working financial model."),
        ("03","Run the play","Six to twelve weeks. We run the experiments alongside your team — pricing tests, channel pivots, NPD launches, inventory resets."),
        ("04","Operate","Quarterly. The model updates with reality. The wins compound. The losses get cut. The cadence becomes how you run."),
    ]
    method_html = "".join(f'<div class="bc-step"><div class="bc-step__num">{n}</div><h3>{t}</h3><p>{d}</p></div>' for n,t,d in method)
    principles = [
        ("Operators first","Every recommendation comes from someone who has shipped it before — not a framework borrowed from a textbook."),
        ("Numbers, not narratives","If a strategy can&rsquo;t be measured on the P&amp;L, it isn&rsquo;t one. Every workstream owns a metric."),
        ("Skin in the outcome","Engagements are scoped around the result, not the hours. We win when you do — that&rsquo;s the only deal worth having."),
    ]
    principles_html = "".join(f'<div class="bc-principle"><h3>{t}</h3><p>{d}</p></div>' for t,d in principles)

    return f"""
<section class="bc-hero">
  <div class="container bc-hero__inner">
    <a href="../services.html" style="font-family:var(--font-mono);font-size:12px;letter-spacing:.14em;color:var(--fg-muted);text-transform:uppercase">← All services</a>
    <span class="eyebrow" style="margin-top:24px;display:inline-flex">Business Consulting</span>
    <h1>Solving for the new economics of consumer growth.</h1>
    <p class="bc-hero__lead">Channels fragment. CAC compounds. Marketplaces, D2C and retail fight for the same shopper. We help consumer leadership teams find the wedge that still pays — and the operating discipline to run it.</p>
    <div class="bc-hero__cta">
      <a href="../contact.html" class="btn btn--primary btn--lg">Book a discovery call <span class="btn__arrow">→</span></a>
      <a href="#services" class="btn btn--secondary btn--lg">Explore consulting services</a>
    </div>
  </div>
</section>

<nav class="bc-anchors"><div class="container bc-anchors__inner">
  <a href="#overview">Overview</a><a href="#services">Services</a><a href="#sectors">Sectors</a><a href="#approach">Approach</a><a href="#principles">Principles</a><a href="#cases">Case Studies</a>
</div></nav>

<section class="section" id="overview">
  <div class="container">
    <div class="bc-overview">
      <div>
        <span class="eyebrow">The opportunity</span>
        <h2>Consumer growth is harder, faster and more expensive than ever.</h2>
        <div class="bc-overview__body">
          <p>The old playbook — buy traffic, run discounts, hope retention shows up — is over. Acquisition costs are rising every quarter, marketplaces are commoditising D2C, and the brands compounding through it are the ones with sharp pricing, deep retention loops, and a real grip on contribution margin.</p>
          <p>We work inside consumer businesses — D2C, beauty, fashion, food, electronics, edtech, health, retail — to engineer the operating model behind the growth: pricing, channel mix, portfolio, unit economics, market entry. Then we stay long enough to ship it.</p>
        </div>
      </div>
      <div class="bc-overview__visual">
        <h3>What we&rsquo;ve shipped</h3>
        <div class="bc-overview__stats">
          <div class="stat"><div class="stat__num">50<span class="unit">+</span></div><div class="stat__label">Brands advised</div></div>
          <div class="stat"><div class="stat__num">100<span class="unit">Cr+</span></div><div class="stat__label">Ad spend modelled</div></div>
          <div class="stat"><div class="stat__num">8</div><div class="stat__label">Consumer sub-sectors</div></div>
          <div class="stat"><div class="stat__num">3<span class="unit">x</span></div><div class="stat__label">Avg profit improvement</div></div>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="section" id="services" style="background:var(--surface-section);border-block:1px solid var(--line)">
  <div class="container">
    <div class="sec-head">
      <div><span class="eyebrow">Our consulting services</span><h2 style="max-width:20ch">Six pillars, one operating model.</h2></div>
      <p class="lead">Each engagement is scoped to the lever that moves the business — not a fixed scope of deliverables. We pull from any combination of these six.</p>
    </div>
    <div class="svc-rich">{pillars_html}</div>
  </div>
</section>

<section class="section" id="sectors">
  <div class="container">
    <div class="sec-head">
      <div><span class="eyebrow">Explore consumer sub-sectors</span><h2 style="max-width:24ch">Deep operating reps across the consumer stack.</h2></div>
      <p class="lead">Pick a sub-sector to see the levers we pull, the playbooks we&rsquo;ve run, and the outcomes we&rsquo;ve already shipped.</p>
    </div>
    <div class="bc-sectors-wrap" id="bcSectorsWrap">
      <div class="bc-sectors-list" id="bcSectorsList">{list_html}</div>
      <div class="bc-sectors-panel" id="bcSectorsPanel">{panels_html}</div>
    </div>
  </div>
</section>

<section class="section" id="approach" style="background:var(--surface-section);border-block:1px solid var(--line)">
  <div class="container">
    <div class="sec-head">
      <div><span class="eyebrow">How we work</span><h2 style="max-width:20ch">Strategy to execution, in one engagement.</h2></div>
      <p class="lead">No slide-only deliverables. Every phase ships with a working artefact — a model, a memo, a tested campaign or a launched SKU.</p>
    </div>
    <div class="bc-method">{method_html}</div>
  </div>
</section>

<section class="section" id="principles">
  <div class="container">
    <div class="sec-head"><div><span class="eyebrow">What we believe</span><h2>Principles we don&rsquo;t flex on</h2></div></div>
    <div class="bc-principles">{principles_html}</div>
  </div>
</section>

<section class="section" id="cases" style="background:var(--surface-section);border-top:1px solid var(--line)">
  <div class="container">
    <div class="sec-head">
      <div><span class="eyebrow">Featured outcomes</span><h2>Engagements that moved the P&amp;L</h2></div>
      <p class="lead">When a tile isn&rsquo;t enough, the case study has the strategy, the experiments and the numbers behind the outcome.</p>
    </div>
    <div class="bc-cases">
      <a class="case" href="../case-studies/nutriglow.html"><div class="case__head"><div class="case__brand">Nutriglow</div><span class="case__industry">Beauty &amp; Personal Care</span></div><p class="case__desc">200+ SKU beauty brand turned around from YoY decline to compounding growth via pricing, sourcing and channel mix.</p><div class="case__metrics"><div class="stat case__metric"><div class="stat__num">57<span class="unit">%</span></div><div class="stat__label">ROAS lift</div></div><div class="stat case__metric"><div class="stat__num">40<span class="unit">%</span></div><div class="stat__label">COGS cut</div></div><div class="stat case__metric"><div class="stat__num">14<span class="unit">%</span></div><div class="stat__label">CM3 lift</div></div></div><span class="case__link">Read case study →</span></a>
      <a class="case" href="../case-studies/celio.html"><div class="case__head"><div class="case__brand">Celio</div><span class="case__industry">D2C Menswear</span></div><p class="case__desc">Heritage French menswear brand. Pricing strategy, creative testing and predictive inventory drove ROAS and CM3 lift in parallel.</p><div class="case__metrics"><div class="stat case__metric"><div class="stat__num">45<span class="unit">%</span></div><div class="stat__label">ROAS lift</div></div><div class="stat case__metric"><div class="stat__num">23<span class="unit">%</span></div><div class="stat__label">CM3 lift</div></div><div class="stat case__metric"><div class="stat__num">17<span class="unit">%</span></div><div class="stat__label">Brand search</div></div></div><span class="case__link">Read case study →</span></a>
    </div>
  </div>
</section>

{CTA_BAND.format(base='../')}

<script>
(function(){{
  const tabs = document.querySelectorAll('#bcSectorsList .bc-sector-tab');
  const panels = document.querySelectorAll('#bcSectorsPanel .bc-sector-panel');
  tabs.forEach(b => b.addEventListener('click', () => {{
    tabs.forEach(x => x.classList.toggle('is-active', x === b));
    panels.forEach(p => p.classList.toggle('is-active', p.dataset.sec === b.dataset.sec));
  }}));
}})();
</script>
"""

def build_services_hub():
    cards = ''
    for s in SERVICES:
        cards += f'''
        <a class="service" href="services/{s["slug"]}.html">
          <span class="service__index">→</span>
          <h3 class="service__title">{s["title"]}</h3>
          <p class="service__body">{s["hero"]}</p>
        </a>'''
    body = f"""
<section class="page-hero">
  <div class="container page-hero__inner">
    <span class="eyebrow">Services</span>
    <h1>A 360° growth engine, built around your goals.</h1>
    <p class="lead page-hero__lead">Strategy, creative and technology under one roof — orchestrated by data at every step. Pick the service that fits your stage; we'll bring the pod that fits the service.</p>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="sec-head">
      <div><span class="eyebrow">All services</span><h2>Every service, one operating model</h2></div>
      <p class="lead">Pick the service that fits your stage; we'll bring the pod that fits the service.</p>
    </div>
    <div class="services-grid">{cards}</div>
  </div>
</section>

{CTA_BAND.format(base='')}
"""
    return page("Growth Marketing Services",
                "Performance marketing, branding, web & app development, business consulting, SEO, CRM & retention, and platform implementations from Digitaltheory.",
                body, base="", active="services", path="services.html",
                seo_title="Growth Marketing Services — Digitaltheory")

# ====================== OUR WORK ======================
WORKS = [
    # D2C / E-commerce
    {"brand":"Celio","domain":"celio.in","industry":"D2C / E-commerce","tags":["Performance","D2C","Retention"],"desc":"Heritage French menswear brand. Rebuilt paid search, paid social and D2C ops — 45% ROAS lift, 23% CM3 improvement.","initials":"Cl","case":"celio"},
    {"brand":"Pepperfry","domain":"pepperfry.com","industry":"D2C / E-commerce","tags":["Performance","Marketplace"],"desc":"Furniture &amp; home D2C. Scaled performance media across high-AOV categories and marketplace listings.","initials":"Pf"},
    {"brand":"Chumbak","domain":"chumbak.com","industry":"D2C / E-commerce","tags":["Performance","Operations","NPD"],"desc":"Lifestyle D2C brand. 3x profit improvement via NPD, operations, website maintenance and performance marketing.","initials":"Cm"},
    {"brand":"Meatton","domain":"meatton.com","industry":"D2C / E-commerce","tags":["Performance","Local SEO"],"desc":"D2C meat &amp; protein brand. Scaled cohort-based acquisition with strong unit economics across paid + organic.","initials":"Mt"},
    {"brand":"Ira Soleil","domain":"irasoleil.com","industry":"D2C / E-commerce","tags":["Branding","Performance"],"desc":"Premium ethnic wear D2C. Brand-led acquisition with retention loops tied to occasion and seasonality.","initials":"Is"},
    {"brand":"put-chi","domain":"put-chi.com","industry":"D2C / E-commerce","tags":["Branding","Performance"],"desc":"Premium kids &amp; family D2C. Built brand storytelling and performance funnel from scratch.","initials":"Pc"},
    {"brand":"august","domain":"itsaugust.co","industry":"D2C / E-commerce","tags":["Performance","CRM"],"desc":"Wellness D2C brand. Drove acquisition with creative testing framework and lifecycle CRM nudges.","initials":"Au"},
    # Beauty & Personal Care
    {"brand":"Nutriglow","domain":"nutriglowcosmetics.com","industry":"Beauty & Personal Care","tags":["Performance","Consulting","Marketplace"],"desc":"200+ SKU beauty brand. Pricing, sourcing &amp; channel-mix turnaround drove 35% QoQ revenue growth.","initials":"Ng","case":"nutriglow"},
    {"brand":"svaa.life","domain":"svaa.life","industry":"Beauty & Personal Care","tags":["Branding","Performance"],"desc":"Wellness &amp; personal care D2C. Identity, narrative and full-funnel media built to compound.","initials":"Sv"},
    # Edtech
    {"brand":"Codingal","domain":"codingal.com","industry":"Edtech","tags":["Performance","CRO","International"],"desc":"K-12 coding platform. International market entry with 70% lower CAC; SQL share lifted from 30% to 47%.","initials":"Cd","case":"codingal"},
    {"brand":"upGrad","domain":"upgrad.com","industry":"Edtech","tags":["Performance","SEO"],"desc":"Higher-ed platform. Performance + SEO playbooks across multiple verticals to drive qualified inquiries.","initials":"uG"},
    {"brand":"Eurokids","domain":"eurokidsindia.com","industry":"Edtech","tags":["Performance","Local SEO"],"desc":"Pre-school chain. Geo-fenced acquisition + admission funnel optimisation across 100+ centres.","initials":"Ek"},
    {"brand":"School Basix","domain":"schoolbasix.com","industry":"Edtech","tags":["Branding","Web"],"desc":"K-12 school operating platform. Identity system + web build for category positioning and lead capture.","initials":"Sb"},
    # Consumer Apps & Services
    {"brand":"Laundrokart","domain":"laundrokart.com","industry":"Consumer Apps","tags":["App","CRM","Loyalty"],"desc":"12-year-old laundry app. RFM-led CRM + loyalty program lifted retention 17% and LTV 23%.","initials":"Lk","case":"laundrokart"},
    {"brand":"Evolutions Fitness","domain":"evolutionsfitness.in","industry":"Consumer Apps","tags":["Branding","Performance"],"desc":"Fitness club chain. Local acquisition engine + retention program for member LTV uplift.","initials":"Ev"},
    # Gaming
    {"brand":"Pocket52","domain":"pocket52.com","industry":"Gaming","tags":["App","ASO","CRM"],"desc":"Real-money gaming app. Channel scoring + ASO program cut CAC 45% and lifted organic installs 20%.","initials":"P5","case":"pocket52"},
    # Retail / Pharma
    {"brand":"Thulasi Pharmacy","domain":"thulasipharmacies.lk","industry":"Retail & Pharma","tags":["Digital Transformation","ML","Operations"],"desc":"80+ branch pharmacy chain. ERP integration + ML for store-level product fit drove margin and sell-through.","initials":"Tp","case":"thulasi"},
    # Fintech
    {"brand":"Groww","domain":"groww.in","industry":"Fintech","tags":["Performance","Brand Lift"],"desc":"Investment platform. Brand lift &amp; performance media collaboration for user acquisition.","initials":"Gr"},
    {"brand":"Onecheq","domain":"onecheq.com","industry":"Fintech","tags":["Branding","Web"],"desc":"Fintech startup. Identity, narrative and go-to-market positioning for category creation.","initials":"Oc"},
]

INDUSTRY_ORDER = ["All","D2C / E-commerce","Beauty & Personal Care","Edtech","Consumer Apps","Gaming","Retail & Pharma","Fintech"]

# Public brand logos via Clearbit's free logo API (domain -> served logo).
# onerror in the markup falls back to a styled text card if a domain isn't found.
LOGO_BRANDS = [
    ("Groww","groww.in"),
    ("upGrad","upgrad.com"),
    ("Pepperfry","pepperfry.com"),
    ("Celio","celio.in"),
    ("Codingal","codingal.com"),
    ("Pocket52","pocket52.com"),
    ("Chumbak","chumbak.com"),
    ("Nutriglow","nutriglowcosmetics.com"),
    ("Eurokids","eurokidsindia.com"),
    ("Thulasi","thulasipharmacies.com"),
    ("Meatton","meatton.com"),
    ("Laundrokart","laundrokart.com"),
]

def build_our_work():
    counts = {ind: sum(1 for w in WORKS if w["industry"]==ind) for ind in INDUSTRY_ORDER[1:]}
    counts["All"] = len(WORKS)
    tabs_html = "".join(
        f'<button class="work-tab {"is-active" if ind=="All" else ""}" data-tab="{ind}">{ind} <span class="work-tab__count">({counts[ind]})</span></button>'
        for ind in INDUSTRY_ORDER
    )
    def tile(w):
        case_link = f'<span class="work-tile__link">Read case study →</span>' if w.get("case") else ''
        href = f'case-studies/{w["case"]}.html' if w.get("case") else '#'
        tag_class = "a" if w.get("case") else "div"
        tags_html = "".join(f'<span class="work-tile__tag">{t}</span>' for t in w["tags"])
        return f'''<{tag_class} class="work-tile" data-industry="{w["industry"]}" {f'href="{href}"' if w.get("case") else ''}>
          <div class="work-tile__cover">
            <div class="work-tile__logo">
              <img src="https://www.google.com/s2/favicons?domain={w["domain"]}&sz=128" alt="{w["brand"]} logo" loading="lazy" onerror="this.style.display='none';this.nextElementSibling.style.display='block'" />
              <span class="work-tile__initials" style="display:none">{w["initials"]}</span>
            </div>
          </div>
          <div class="work-tile__body">
            <div class="work-tile__meta">{w["industry"]}</div>
            <div class="work-tile__brand">{w["brand"]}</div>
            <p class="work-tile__desc">{w["desc"]}</p>
            <div class="work-tile__tags">{tags_html}</div>
            {case_link}
          </div>
        </{tag_class}>'''
    tiles_html = "".join(tile(w) for w in WORKS)
    logos_html = "".join(
        f'<div class="logo-cell" title="{n}"><img src="https://www.google.com/s2/favicons?domain={d}&sz=128" alt="{n} logo" loading="lazy" onerror="this.parentElement.classList.add(\'logo-cell--fallback\');this.outerHTML=\'<span>{n}</span>\'" /><span class="logo-cell__name">{n}</span></div>'
        for n,d in LOGO_BRANDS
    )

    body = f"""
<section class="page-hero">
  <div class="container page-hero__inner">
    <span class="eyebrow">Our Work</span>
    <h1>Built for outcomes. Run by operators. Trusted by 50+ brands.</h1>
    <p class="lead page-hero__lead">A working portfolio across D2C, beauty, edtech, consumer apps, gaming, retail and fintech — built around performance marketing, branding, web &amp; app, SEO and digital transformation.</p>
    <div class="page-hero__cta">
      <a href="contact.html" class="btn btn--primary btn--lg">Start your engagement <span class="btn__arrow">→</span></a>
    </div>
  </div>
</section>

<div class="logo-strip">
  <div class="container">
    <p class="logo-strip__label">Trusted by category leaders</p>
    <div class="logos-grid">{logos_html}</div>
  </div>
</div>

<section class="section">
  <div class="container">
    <div class="manifesto">
      <div>
        <span class="eyebrow">Why we exist</span>
        <h2 style="margin-top:14px;max-width:18ch">Most agencies sell activity. We sell the outcome.</h2>
        <p class="lead" style="margin-top:20px;max-width:46ch">Performance marketing has become a commodity. Decks have replaced decisions, dashboards have replaced thinking, and brands are paying premium fees for output that doesn&rsquo;t move the P&amp;L. We started Digitaltheory to flip that — to be the team that thinks like an operator, ships like a startup, and gets measured by the only number that matters: yours.</p>
      </div>
      <ol class="manifesto__points">
        <li>Strategy without execution is theatre. We do both, in the same engagement.</li>
        <li>Channels are tools, not strategies. The brief is the business, not the platform.</li>
        <li>Creative is the lever, not the deliverable. We test it like a hypothesis.</li>
        <li>Retention is the business. Acquisition is the entrance fee.</li>
        <li>Data is useless without a decision attached. Every dashboard ends with a call.</li>
        <li>AI is a tool — we&rsquo;re the edge. Models scale us; they don&rsquo;t replace us.</li>
      </ol>
    </div>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="bc-stats" style="margin-top:0;padding-top:0;border-top:0">
      <div class="stat"><div class="stat__num">50<span class="unit">+</span></div><div class="stat__label">Brands shipped</div></div>
      <div class="stat"><div class="stat__num">7</div><div class="stat__label">Industries served</div></div>
      <div class="stat"><div class="stat__num">100<span class="unit">Cr+</span></div><div class="stat__label">Ad spend managed</div></div>
      <div class="stat"><div class="stat__num">8</div><div class="stat__label">Services delivered</div></div>
    </div>
  </div>
</section>

<section class="section" style="background:var(--surface-section);border-block:1px solid var(--line)">
  <div class="container">
    <div class="sec-head" style="margin-bottom:var(--space-6)">
      <div><span class="eyebrow">By industry</span><h2 style="max-width:22ch">Pick a category. See the operating reps.</h2></div>
      <p class="lead">Patterns travel across categories, specifics don&rsquo;t. We bring both — the playbooks we&rsquo;ve run before, and the depth to adapt them to your category, customer and funnel.</p>
    </div>
    <div class="work-tabs" id="workTabs">{tabs_html}</div>
    <div class="work-grid" id="workGrid">{tiles_html}</div>
    <div class="work-empty" id="workEmpty" style="display:none">No engagements in this category yet — talk to us about being the first.</div>
  </div>
</section>

{CTA_BAND.format(base='')}

<script>
(function(){{
  const tabs = document.querySelectorAll('#workTabs .work-tab');
  const tiles = document.querySelectorAll('#workGrid .work-tile');
  const empty = document.getElementById('workEmpty');
  function filter(ind) {{
    let visible = 0;
    tiles.forEach(t => {{
      const match = ind === 'All' || t.dataset.industry === ind;
      t.classList.toggle('is-hidden', !match);
      if (match) visible++;
    }});
    empty.style.display = visible === 0 ? 'block' : 'none';
  }}
  tabs.forEach(b => b.addEventListener('click', () => {{
    tabs.forEach(x => x.classList.toggle('is-active', x === b));
    filter(b.dataset.tab);
  }}));
}})();
</script>
"""
    return page("Our Work — 50+ Brands, 7 Industries",
                "Digitaltheory's portfolio across D2C, beauty, edtech, consumer apps, gaming, retail and fintech — filter by industry to see relevant engagements.",
                body, base="", active="work", path="our-work.html",
                seo_title="Our Work — 50+ Brands, 7 Industries | Digitaltheory")

# ====================== BLOG ======================
BLOG_POSTS = [
    {
        "slug":"quadcore-campaign-framework",
        "cat":"Performance Marketing","cat_key":"performance",
        "title":"The quadcore framework: why two-motion paid accounts stop compounding",
        "seo_title":"The Quadcore Paid Media Framework | Digitaltheory",
        "excerpt":"Most performance accounts run two motions — prospecting and retargeting — and then plateau. Here's the four-motion structure that replaces it.",
        "date":"2026-05-22","read":"7 min read",
        "body":"""
<p class="post__lead">If a paid-media account has only two campaigns &mdash; broad prospecting and a retargeting catch-all &mdash; it is not actually a system. It is a couple of levers being yanked in opposite directions. Here is the four-motion structure that replaces it.</p>

<h2>Why two motions stop working</h2>
<p>The two-motion account is the default Meta or Google build. Prospecting carries 70&ndash;80% of spend with broad targeting, lookalikes and a few interest stacks. Retargeting catches the bounce. It works for the first six months of a brand's life. Then auction inflation, creative fatigue and saturation eat the margin from both ends.</p>
<p>What you start seeing inside the account is predictable: prospecting CPMs climb 25&ndash;40% quarter on quarter, retargeting frequency caps choke incremental conversions, and the absolute number of net-new customers per rupee falls quietly while the dashboard still says ROAS is fine. Blended LTV stays flat because the cohort mix doesn't shift.</p>

<h2>The four motions</h2>
<p>Quadcore splits a paid account into four orthogonal motions. Each has its own brief, audience definition, creative system and target metric. They run in parallel and never trade attribution against one another.</p>

<h3>1. Prospecting</h3>
<p>Pure cold acquisition with broad audiences and creative engineered for the first-touch unaware buyer. Optimised on landing page view + add to cart, not purchase, so the algorithm gets enough signal density to actually learn. KPI: CPA against blended LTV target, not first-purchase ROAS.</p>

<h3>2. Retargeting</h3>
<p>Tight remarketing audiences segmented by intent (PDP viewers, ATC abandoners, checkout abandoners) with bespoke creative per stage. Capped frequency, with explicit suppression of recent purchasers. KPI: window-level conversion lift over a holdout group, not raw ROAS.</p>

<h3>3. Brand defence</h3>
<p>Branded search + branded social terms + the high-intent audience that is already looking for the brand. This is the most under-built motion in most accounts. It protects margin while branded share-of-search grows; without it, marketplace and competitor bids pick off the best traffic at the worst CPC. KPI: branded share-of-search, branded CTR, share of clicks against competitor bidders.</p>

<h3>4. Creator-led</h3>
<p>UGC, founder-led, performance creator content. Different brief, different production pipeline, different reporting. Not influencer marketing in the brand-build sense &mdash; performance creator content that runs as paid ad creative under the same campaign objective. KPI: hook rate &times; conversion rate, scored per variant.</p>

<h2>What happens when all four run together</h2>
<p>Three things tend to compound once the account moves from two motions to four:</p>
<ul>
  <li><strong>Brand defence</strong> catches traffic that marketplace bids were eating. Branded search terms grow QoQ. CPC on protected terms drops because organic share grows alongside paid.</li>
  <li><strong>Creator-led</strong> creative gives the algorithm fresh inventory at the top of the funnel. Hook rates on UGC variants typically beat hero-product creative by 1.5&ndash;2x, which feeds back into cheaper prospecting CPMs.</li>
  <li><strong>Retargeting</strong> stops competing with prospecting for the same audience. Frequency caps + suppression make the catch incremental rather than additive.</li>
</ul>
<p>The framework itself is not the point. The point is that paid acquisition is four problems, not two &mdash; and most accounts solve only the first two until the unit economics break.</p>

<h2>What to do next week</h2>
<p>Audit the account. Count the motions. If there are only two, there is rebuild work to do. Start with brand defence &mdash; it is the cheapest motion to set up and has the largest immediate margin impact. Set up creator-led as a second wave: a small batch of UGC variants tested against existing creative within four weeks. Then split retargeting from prospecting properly &mdash; suppress, cap frequency, and stop optimising both for the same conversion event.</p>
<p>The compounding only starts once all four motions are running in parallel with their own briefs and their own KPIs.</p>
"""
    },
    {
        "slug":"60-40-marketplace-d2c-budget",
        "cat":"D2C & E-commerce","cat_key":"d2c",
        "title":"How to split D2C performance budget between marketplaces and own site",
        "seo_title":"D2C Budget Split: Marketplaces vs Own Site | Digitaltheory",
        "excerpt":"Most D2C brands either over-index on Amazon or over-index on Shopify. Neither stance is right. Here's how to model the split properly.",
        "date":"2026-04-30","read":"6 min read",
        "body":"""
<p class="post__lead">In most D2C brands, marketplaces and the own-site are treated like competing channels. Separate budget, separate team, separate dashboard. Neither tends to be profitable in isolation. The fix isn't to pick one. It's to wire them into a single funnel with a budget split that comes from a SKU-level model.</p>

<h2>The two failure modes</h2>
<p>D2C brands tend to fall into one of two camps. Camp one believes Amazon (or Flipkart, Nykaa, etc.) is the discovery channel and the website is for high-intent repeat. Camp two believes the website is the brand-builder and marketplace is a discount-eating necessary evil. Both are wrong, and both lose money quietly.</p>
<p>Camp one ends up subsidising marketplace search ranking with paid spend until the COGS-to-fees math collapses. Camp two ends up paying marketplace prices to Meta and Google to acquire customers their competitors are quietly serving on Amazon at half the CAC.</p>

<h2>How to model the split</h2>
<p>Start with a channel-level unit-economics model, not a budget guess. For each SKU, compute the four things that matter: marketplace fee structure, ad take rate, return rate, and contribution margin per channel. Then score each SKU on which channel pays it back faster &mdash; not which channel sells more.</p>
<p>What usually drops out: a small subset of SKUs (typically 15&ndash;25% of the catalogue) drives the majority of own-site revenue at acceptable CM3. The rest pays back only on marketplaces, where the customer is already shopping the category and intent is higher.</p>
<p>Once the model is in place, the split writes itself. The number can be 60/40, 70/30, 50/50 &mdash; what matters is that it came from SKU-level economics, not a CEO preference.</p>

<h2>What "marketplace majority" should mean</h2>
<p>It is not all the spend poured into Sponsored Products. The marketplace ad architecture is itself three motions:</p>
<ul>
  <li><strong>Sponsored Products</strong> on bestsellers and high-velocity SKUs &mdash; defending top-of-search.</li>
  <li><strong>Sponsored Brands</strong> as the category-shaping motion &mdash; a banner that owns the head term and drives traffic into the storefront, not the PDP.</li>
  <li><strong>Sponsored Display</strong> as the audience-driven motion &mdash; retargeting marketplace viewers and similar-category shoppers, where ROAS doesn't include the same fee drag.</li>
</ul>
<p>Re-introducing SB and SD on top of an SP-only account is one of the cheapest wins available in beauty &amp; personal care, fashion and food categories. It shifts revenue mix toward higher-margin storefront sessions and lets you defend share without bleeding margin into bid wars on SP alone.</p>

<h2>What "own-site minority" should mean</h2>
<p>The own-site share gets concentrated on the SKUs that earned it. Full-funnel media mix &mdash; prospecting + brand defence + creator-led &mdash; pushed against retention loops on the website (RFM-segmented winbacks, refill journeys, bundle prompts). The website becomes a retention asset for the brand's best customers, not an acquisition substitute for marketplaces.</p>

<h2>The supply-side change that makes it work</h2>
<p>Performance is half the rebuild. The other half is sourcing. COGS reductions on the hero portfolio lift CM1 enough that the marketplace majority actually has margin to play with. Without COGS work, the marketplace share usually stays in the red &mdash; performance is asked to do something the supply chain made impossible.</p>

<blockquote>The wrong question is "marketplace or D2C". The right question is "which customer am I winning, on which channel, at what margin?".</blockquote>

<p>The split won't be 60/40 for everyone &mdash; maybe yours is 70/30 in fashion, 50/50 in food, 80/20 in electronics. The number isn't the lesson. The lesson is that the split has to come from a SKU-level model, not a budget hunch.</p>
"""
    },
    {
        "slug":"rfm-cohort-retention-guide",
        "cat":"CRM & Retention","cat_key":"crm",
        "title":"Why RFM still wins: a practical guide to cohort-based retention",
        "seo_title":"RFM: A Practical Cohort Retention Guide | Digitaltheory",
        "excerpt":"Predictive ML and real-time personalisation are great. None of them work if your customer base isn't first segmented into cohorts you can act on weekly.",
        "date":"2026-04-08","read":"8 min read",
        "body":"""
<p class="post__lead">When a consumer business has years of transaction data and unit economics that are quietly degrading, the answer is rarely a new acquisition channel. It is almost always inside the data already sitting in the warehouse. Here is the cleanest first cut.</p>

<h2>Why RFM still wins</h2>
<p>Retention frameworks come and go. Predictive ML, propensity scoring, real-time personalisation engines &mdash; all worth shipping, none of them mean anything if the customer base isn't first segmented into cohorts that can be acted on weekly. RFM (recency, frequency, monetary) is still the cleanest first cut.</p>
<p>The discipline it forces is useful: for each customer, compute when they last bought, how often they buy and how much they spend. Score each dimension on a 1&ndash;5 scale, and bucket the base into 12&ndash;15 cohort archetypes (champion, loyal, at-risk, hibernating, lost, new high-value, etc.). Then decide what action belongs to each.</p>

<h2>What the cohorts usually tell you</h2>
<p>The story RFM tells in most consumer transaction histories is consistent enough to be predictable:</p>
<ul>
  <li><strong>The high-value cohort is tiny but compounding.</strong> The top 5&ndash;10% of customers typically drive 30&ndash;40% of revenue &mdash; and crucially, they're still active, still buying, but receiving the same generic comms as the bottom 70%.</li>
  <li><strong>Win-back economics are inverted.</strong> The cost to reactivate a churned customer (via discount + push + WhatsApp) is usually lower than the cost to acquire a fresh install. Most brands just aren't doing it systematically.</li>
  <li><strong>Day-30 retention is the kill metric.</strong> Customers who come back inside 30 days of first order tend to have a 3&ndash;5x higher 12-month LTV than those who come back at day 30&ndash;60. Anything after day 60 is effectively a lost customer, regardless of how much discount is thrown at it.</li>
  <li><strong>Push fatigue is real.</strong> Notification open rates fall off a cliff past 4 sends per week. WhatsApp tolerates more because the format is different and the user opted in.</li>
</ul>

<h2>The four workstreams of a proper RFM-led rebuild</h2>

<h3>Cohort-based comms</h3>
<p>Twelve cohorts, each with their own message frequency, channel mix and offer structure. Champions get refill nudges and early-access drops. At-risk customers get win-back triggers tied to the day-30 cliff. Hibernating customers get one big push and then go quiet. Lost customers get a final discount and then suppression.</p>

<h3>Day-30 trigger journeys</h3>
<p>The single highest-impact change. A behavioural trigger fires if a first-time customer doesn't transact again within 25 days. The journey is push + WhatsApp + email + an in-app banner, sequenced over 5 days with declining intensity. Day-30 retention improves measurably and 12-month LTV moves with it.</p>

<h3>A loyalty program designed for the top decile</h3>
<p>A tiered loyalty program designed explicitly for the high-value cohort that the data surfaces. The tiers should come with bookable-priority service slots, early access or category-relevant perks &mdash; not just discounts. A customer who is already paying full price values bookability more than 5% off. Programs designed this way tend to contribute a small but pure-margin and self-reinforcing percentage of overall revenue.</p>

<h3>Win-back coupons for the lost-but-recoverable</h3>
<p>Targeted discounts to a specific cohort &mdash; defined by their RFM bucket &mdash; rather than blasted to the full file. The economics work because the offer doesn't reach active customers who would have bought anyway. The discount is a recovery tool, not a sales tool.</p>

<h2>The discipline most retention programs lack</h2>
<p>If a business has more than two years of transaction data, RFM gives 80% of the ML value at 5% of the effort. The interesting bit isn't the segmentation &mdash; segmentation is easy. The interesting bit is what action gets assigned to each cohort, and the discipline of suppressing comms to cohorts where there's no action that pays back. Half of every retention program is improved by sending less, not more.</p>
"""
    },
    {
        "slug":"edtech-international-expansion",
        "cat":"Edtech","cat_key":"edtech",
        "title":"When edtech CAC won't fall, leave the market: an international expansion playbook",
        "seo_title":"Edtech International Expansion Playbook | Digitaltheory",
        "excerpt":"For Indian edtech businesses, the temptation when CAC climbs is to optimise harder against Indian auctions. Often, the cheaper answer is an entirely different country.",
        "date":"2026-03-18","read":"6 min read",
        "body":"""
<p class="post__lead">For an Indian edtech, the default response when CAC climbs is to optimise harder against Indian auctions. There is an argument for doing the opposite: leave the market first, scale later.</p>

<h2>The home-market trap</h2>
<p>Indian edtech CAC has been climbing for four years. The category is saturated; spending is concentrated in a handful of segments (K-12, test prep, upskilling); and the unit-economics floor keeps dropping as players bid each other up on the same set of intent terms. For most consumer edtech businesses, the maths on a per-paying-customer basis tightens every month.</p>
<p>Most teams respond by trying to win the same auctions harder &mdash; better creative, better landing pages, smarter bid strategies. All worth doing. None of them solve the underlying problem, which is that an auction with N motivated bidders cannot give any one bidder a structural CAC advantage.</p>

<h2>Where the cheap CAC is</h2>
<p>The hypothesis worth testing: there are international markets where category awareness is high, willingness-to-pay is materially higher than India, and competition is thinner because Indian players haven't scaled outside.</p>
<p>Score candidate countries on four criteria:</p>
<ul>
  <li><strong>International-school fees</strong> &mdash; a proxy for parent willingness to spend on extracurricular learning at premium price points.</li>
  <li><strong>Category competition</strong> &mdash; how many global and local edtech competitors are already bidding the category terms.</li>
  <li><strong>Category awareness</strong> &mdash; whether parents in the market are actively shopping the concept or have to be educated into it.</li>
  <li><strong>Operational tractability</strong> &mdash; payment methods, language fit, time-zone reach for live classes.</li>
</ul>
<p>Shortlist three countries that score high on all four. None of them are usually the obvious first guesses.</p>

<h2>How to pilot</h2>
<p>Launch Meta pilots in all three markets simultaneously, at small budgets, with three creative variants per market. Within 14 days the signal is usually unambiguous: CAC in well-chosen international markets tends to run at 30&ndash;50% of the Indian baseline.</p>
<p>Some of that is lower auction competition. Some of it is higher willingness to pay, which lets the brand run higher-AOV plans at the same conversion rate. Some of it is a surprisingly responsive parent segment in markets where awareness exists but supply is thin.</p>
<p>Once the pilot signal is clear, scale spend, layer Google search (lower volume but high intent), and run a small brand-lift study so that branded search begins to compound in markets where the brand is unknown.</p>

<h2>The funnel rebuild that has to come alongside</h2>
<p>Cutting CAC by 70% will still leave a broken funnel if the sales motion doesn't keep up. Three parts usually need work:</p>
<ul>
  <li><strong>Landing page</strong> &mdash; rewritten for the international parent. Different testimonials, different proof points, different price anchoring. Qualified-lead percentage tends to lift measurably.</li>
  <li><strong>Sales follow-up cadence</strong> &mdash; rebuilt around the time-zone reality (sales calls have to happen inside the parent's working hours, not Indian working hours).</li>
  <li><strong>Onboarding</strong> &mdash; rebuilt around the new student archetype. SQL share can typically move 10&ndash;20 percentage points if the flow is redesigned for the new market.</li>
</ul>

<blockquote>If CAC is rising MoM in the home market, the most expensive thing a brand can do is keep buying the same auctions. The cheapest is to run a serious secondary-research sprint on adjacent markets.</blockquote>

<p>The decision is strategic, not tactical. No amount of bid optimisation inside a saturated market will produce the same step-change as a market with structurally lower competition and structurally higher AOV.</p>
"""
    },
    {
        "slug":"channel-scoring-consumer-apps",
        "cat":"Growth Strategy","cat_key":"strategy",
        "title":"Channel scoring for consumer apps: the four-dimensional model that beats CAC-only thinking",
        "seo_title":"Channel Scoring for Consumer Apps | Digitaltheory",
        "excerpt":"Most channel decisions get made on last-week's CAC. The interesting decisions get made on per-channel LTV trajectories. Here's the scoring model that surfaces them.",
        "date":"2026-02-28","read":"7 min read",
        "body":"""
<p class="post__lead">When CAC won't fall, the temptation is to throw money at whichever channel has the lowest CAC last week. That is exactly the wrong frame. CAC is a price paid for an asset (the customer). The asset has a value (LTV). And both vary by channel in ways that aren't visible until they're scored properly.</p>

<h2>The standard failure mode</h2>
<p>In consumer apps &mdash; gaming, services, fintech &mdash; channel mixes drift toward whichever source produced the cheapest install last quarter. Affiliate marketing tends to carry meaningful spend but with opaque mix: nobody can clearly say which affiliates send high-LTV users versus pure install volume. Installs scale, unit economics don't.</p>
<p>The problem isn't the channels. The problem is the scoring.</p>

<h2>A four-dimensional channel score</h2>
<p>Every channel gets scored on four weighted dimensions:</p>
<ul>
  <li><strong>QoQ growth rate</strong> &mdash; is the channel still scaling or already plateauing?</li>
  <li><strong>LTV trajectory</strong> &mdash; is per-channel LTV improving, flat or degrading quarter over quarter?</li>
  <li><strong>ARPU</strong> &mdash; what's the average revenue per user from this channel, calculated at day 60 and day 180?</li>
  <li><strong>CAC</strong> &mdash; the obvious one, but always last in the order.</li>
</ul>
<p>Scored honestly, the matrix usually produces surprises:</p>
<ul>
  <li>Google often drives more growth than its CAC suggests &mdash; LTV trajectory is strong because audience intent is high.</li>
  <li>Affiliates tend to carry both ends of the bell curve &mdash; some deliver the highest-value users in the whole account; others deliver installs that churn inside 7 days at no margin.</li>
  <li>Organic is usually under-invested &mdash; flat growth there is rarely a platform problem; it's a missing ASO program.</li>
</ul>

<h2>What to do with the score</h2>

<h3>Affiliate framework rebuild</h3>
<p>Build it around a user-engagement model. Score each affiliate on the LTV of users they deliver, not their raw install volume. Pause the bottom quartile. Scale the top quartile with direct incentive alignment.</p>

<h3>Bottom-of-funnel Google optimisation</h3>
<p>Sharper creative and tighter targeting on BOF Google campaigns. A few points of CAC reduction tends to come from this alone.</p>

<h3>Meta LTV audiences</h3>
<p>Move Meta targeting away from broad lookalikes toward LTV-based custom audiences. The audience base gets higher quality, ad costs stabilise, and CAC tends to drop materially for the cohorts that lookalike-modelling alone wasn't reaching.</p>

<h3>ASO program</h3>
<p>Usually the biggest single CAC win. Rebuilt rich media images, a description rewritten against a primary keyword set, on-page and off-page SEO across landing pages and the app store. Organic install share tends to lift double digits and overall CAC drops sharply &mdash; organic is structurally cheaper than any paid channel.</p>

<h3>RFM and in-app monetisation</h3>
<p>RFM segmentation lets the CRM team design nudges that lift LTV. Coordinate with product to ship features and in-app offers for the loyalty cohort, which tends to lift ARPU 5&ndash;10% on top.</p>

<h2>The discipline behind the framework</h2>
<p>If channels get scored only on CAC, the account will pay the lowest CAC for the lowest-LTV traffic, indefinitely. Score on the full quadruple &mdash; growth, LTV trajectory, ARPU, CAC &mdash; and pause the ones that look cheap but produce churners. The biggest wins are often in channels that have been under-invested for the wrong reasons.</p>
"""
    },
    {
        "slug":"multi-branch-retail-margin",
        "cat":"Growth Strategy","cat_key":"strategy",
        "title":"Where the next 10 points of margin live in multi-branch retail",
        "seo_title":"Multi-Branch Retail Margin Playbook | Digitaltheory",
        "excerpt":"The fix isn't a new ERP. The fix is a tool on top of the ERP you already have, built around the operations team — plus an ML layer on the cleaned data.",
        "date":"2026-02-04","read":"8 min read",
        "body":"""
<p class="post__lead">In a multi-branch retail business, the next 10 points of margin are rarely on the marketing line. They are in the small operational decisions that happen 50,000 times a week and get logged in spreadsheets. Here is where the leaks usually are.</p>

<h2>The standard back-office failure</h2>
<p>Mid-sized retail chains &mdash; pharmacies, grocers, kirana networks, multi-branch QSRs &mdash; tend to share a common pattern. The headline problem looks like inventory imbalance: bestsellers going out of stock at one branch while sitting as dead stock at another. The underlying issue is that operational decisions are happening downstream of an ERP nobody uses as a real-time decision tool.</p>
<p>Fill-in and sell-out are spreadsheet-driven. Returns are handled at each branch with no central visibility. SKU-mix decisions are made on intuition, not data. Each of those is a small leak; together they are a meaningful margin drag.</p>

<h2>The three workstreams that compound</h2>

<h3>ERP integration plus an inventory tool</h3>
<p>The first job is to make branch-level inventory visible in real time &mdash; not as a monthly close-out report but as a working tool for the operations team. The fill-in and sell-out automation that follows is downstream of that visibility. A thin digitisation layer that integrates with the existing ERP and surfaces the data the ops team needs in a tool they can actually use is usually a 6&ndash;8-week build, not a replatforming project.</p>

<h3>Returns dashboard</h3>
<p>Returns are the silent margin leak. A dashboard that surfaces returns by product, by branch and by month, with reverse-logistics cost attached, makes the leak visible. Once visible, the ops team can prioritise interventions &mdash; usually returns drop 25&ndash;40% within two quarters of getting the dashboard live.</p>

<h3>Store-level product-fit ML</h3>
<p>The most interesting workstream. A model that predicts which SKUs will sell better at which branch, based on historical sales patterns, returns data, seasonality and category indices. The model doesn't replace category-manager judgement &mdash; it makes the judgement cheaper to scale across dozens of branches.</p>
<p>Concretely, models of this kind surface patterns like: certain antibiotic SKUs have structurally higher sell-through in branches with a hospital within 800 metres; certain wellness SKUs have near-zero sell-through outside dense urban catchments. None of these are surprising in hindsight. The point is none of them were being acted on systematically.</p>

<h2>The order of operations matters</h2>
<p>Three principles, in order of importance:</p>
<ol>
  <li><strong>Plug into the existing ERP rather than replacing it.</strong> Replatforming projects in mid-sized retail businesses fail more often than they succeed. Don't try.</li>
  <li><strong>Build around the operations team, not around a dashboard for leadership.</strong> The tool gets used because the people doing the work can use it. Dashboards only the CXO sees don't change behaviour.</li>
  <li><strong>ML is a layer on top of structured data, not a substitute for the structured data.</strong> The model works because the integration work that came first made the inputs clean.</li>
</ol>

<h2>What this is worth on the P&amp;L</h2>
<p>A reasonable expectation, fully shipped: inventory costs down 25&ndash;35%, returns down 30&ndash;40%, revenue up 10&ndash;20%. The revenue lift comes downstream of the inventory work &mdash; SKUs that previously stocked-out at the wrong branches start being available where the demand is.</p>
<p>If a chain has more than 20 branches, it already has a returns problem it can't see, a SKU-fit problem it can't measure, and a fill-in problem that's eating 5&ndash;10 points of CM. The fix isn't a new ERP. The fix is a tool on top of the ERP that already exists, built around the operations team. The ML model is the last 20% &mdash; the first 80% is the visibility and the workflow.</p>

<blockquote>Brick-and-mortar margin lives in the small decisions. The small decisions only get better when they're visible at the moment they're being made.</blockquote>
"""
    },

    # ====== Six fresh posts, original DT-voice writing on adjacent topic areas ======

    {
        "slug":"agentic-ai-growth-team-workflow",
        "cat":"MarTech","cat_key":"martech",
        "title":"Where agentic AI fits in a growth team's actual workflow (and where it doesn't)",
        "seo_title":"Agentic AI in Growth Teams: Where It Fits | Digitaltheory",
        "excerpt":"Agentic AI is being sold as a replacement for performance teams. In practice, it's a force multiplier on a narrow set of jobs and a liability on the rest.",
        "date":"2026-06-04","read":"6 min read",
        "body":"""
<p class="post__lead">The pitch for agentic AI in growth is that an autonomous system can pick the campaign, write the creative, allocate the budget and report back &mdash; closing the loop without a human. The pitch is wrong about most of those, right about a few of them, and useful only if a team knows which is which.</p>

<h2>What agentic AI is actually good at</h2>
<p>An agent that has a clear objective function, a constrained action space and a fast feedback loop will outperform a human on three jobs:</p>
<ul>
  <li><strong>Bid and budget reallocation</strong> within an existing campaign architecture. The signal-to-noise is high, the action space is bounded, and the feedback (CPA, CVR) is daily. Algorithmic bidding already does most of this; agentic wrappers around it mostly add reporting clarity.</li>
  <li><strong>Creative variant generation</strong> at the asset level. Hook permutations, copy variants, CTA wording. Not concepts &mdash; concepts still need a creative brief from a human. But variants of an existing concept can be generated and shipped 5&ndash;10x faster.</li>
  <li><strong>Anomaly detection and alerting</strong>. CPM spike at 3 am, conversion rate cratering on a single placement, frequency creeping past the cap. These are the jobs analysts spend hours doing badly. Agents do them in seconds, well.</li>
</ul>

<h2>What it's bad at, and where it costs you money</h2>
<p>Three jobs that agentic systems are being sold for but mostly fail at:</p>
<ul>
  <li><strong>Strategy.</strong> An agent cannot decide whether to enter Indonesia, whether to pivot from D2C to wholesale, whether to launch an NPD. These are not optimisation problems; they are framing problems. The agent has no access to the framing.</li>
  <li><strong>Creative concepting.</strong> The variant generator works at the asset level. The concept generator hallucinates. A campaign concept needs a brand POV the agent doesn't have.</li>
  <li><strong>Cross-channel attribution decisions.</strong> The agent will optimise within a channel because the signal is there. It will not correctly reweight channel mix because last-click and view-through attribution are both noise.</li>
</ul>

<h2>How to actually deploy it</h2>
<p>The team that gets value out of agentic AI does it in three steps:</p>
<ol>
  <li><strong>Pick one bounded job.</strong> Not "growth", not "campaign management". One job &mdash; creative variant generation, or anomaly alerting, or audience refresh cadence.</li>
  <li><strong>Wrap it in a review loop.</strong> The agent ships variants; a human approves them before they go live. The loop tightens over time as confidence builds.</li>
  <li><strong>Measure the displacement, not the output.</strong> Did the marketer spend two fewer hours a week on this job? Yes &mdash; keep it. No &mdash; the tool is theatre.</li>
</ol>

<h2>The deeper point</h2>
<p>Agentic AI doesn't replace growth teams. It changes which jobs growth teams should be doing. Variant generation and budget reallocation become commodities. Brand POV, strategy and cross-channel calls become the only jobs worth a senior performance marketer's time. The teams that don't make the shift will be displaced not by the AI but by the teams that do.</p>
"""
    },

    {
        "slug":"martech-stack-triage",
        "cat":"MarTech","cat_key":"martech",
        "title":"MarTech stack triage: when to consolidate, when to add, when to rip out",
        "seo_title":"MarTech Stack Triage — A Practical Guide | Digitaltheory",
        "excerpt":"Most marketing teams own 30+ tools and use 12. The triage isn't a procurement exercise — it's a workflow audit.",
        "date":"2026-05-12","read":"5 min read",
        "body":"""
<p class="post__lead">If a marketing team has been operating for more than four years, the MarTech stack is no longer designed; it's accreted. Tools were bought for a campaign, kept for a quarter, forgotten for a year. Here's how to triage the result without either over-consolidating or over-spending.</p>

<h2>The three categories every tool falls into</h2>
<p>Run an audit and put every tool in one of three boxes:</p>
<ul>
  <li><strong>Workflow critical</strong>: someone uses it weekly, it's tied to a revenue process, and removing it breaks a campaign. Keep, regardless of cost.</li>
  <li><strong>Workflow optional</strong>: someone uses it monthly, the output is nice-to-have, and a more expensive tool covers 80% of its function. Negotiate or consolidate.</li>
  <li><strong>Workflow theatre</strong>: licensed because it was free with another tool, or because a vendor pitched it well in 2024, and nobody can name the workflow it supports. Cancel.</li>
</ul>

<h2>The mistake most consolidation projects make</h2>
<p>Procurement-led MarTech consolidations optimise for licence cost and end up breaking workflows. The team rips out a niche tool that "the all-in-one platform also does" &mdash; and discovers a quarter later that the all-in-one's version of that feature is two years behind and half-functional. The savings on licences cost more in marketer time than they recovered.</p>
<p>The fix: do the audit workflow-first, not licence-first. Start from the campaign, work backwards to the tools. If two tools both support the same workflow well, then consolidate. If one tool barely supports a workflow that's critical, the niche tool stays.</p>

<h2>The three buys worth making</h2>
<p>For most mid-stage growth teams, three categories of tool consistently under-spend relative to their value:</p>
<ul>
  <li><strong>Server-side event tracking and CAPI infrastructure</strong>. iOS attribution is broken; client-side cookies are degrading. Server-side is no longer a nice-to-have.</li>
  <li><strong>A real CDP, even a small one</strong>. The cost of segmenting customers properly is dwarfed by the cost of not segmenting them.</li>
  <li><strong>An LLM-backed content production tool with a brand voice guard</strong>. Volume is the lever; brand consistency is the constraint. Both need tooling.</li>
</ul>

<h2>The two-year cycle</h2>
<p>MarTech stacks need triage every 24 months. The vendor landscape shifts faster than that, but workflow change at the team level is slower. Triage cycles longer than two years compound the accretion problem. Triage cycles shorter than 18 months introduce churn the team can't absorb.</p>
<p>Run the audit. Categorise every tool. Kill the theatre. Re-buy where the workflow is exposed. The point isn't a smaller stack &mdash; it's a stack that maps to the campaigns the team actually runs.</p>
"""
    },

    {
        "slug":"geo-b2b-llm-discovery",
        "cat":"SEO","cat_key":"seo",
        "title":"Generative Engine Optimization for B2B: how to rank inside LLM answers",
        "seo_title":"GEO for B2B: Ranking Inside LLM Answers | Digitaltheory",
        "excerpt":"Search traffic is no longer the only entry point. ChatGPT and Perplexity answers are. Here's what a serious GEO program looks like for a B2B brand.",
        "date":"2026-05-05","read":"6 min read",
        "body":"""
<p class="post__lead">For B2B brands, the buyer no longer always starts at Google. A meaningful share of consideration journeys now begin inside ChatGPT, Perplexity, Gemini or Claude. The brands that get cited inside those answers will own discovery; the rest will pay rising CPCs to acquire the buyers who didn't get cited.</p>

<h2>What GEO actually optimises for</h2>
<p>SEO optimises for ranking on a SERP. GEO optimises for two distinct things:</p>
<ol>
  <li><strong>Inclusion</strong>: being one of the sources an LLM cites when it answers a question.</li>
  <li><strong>Attribution</strong>: being named as the brand of record for a concept, framework or proof point inside the answer.</li>
</ol>
<p>Inclusion is the table-stakes outcome. Attribution is the moat &mdash; if the model says "B2B teams typically use the X framework", and the model learned the framework from one specific source, that source becomes the brand of record for the concept.</p>

<h2>The four-part GEO playbook</h2>

<h3>1. Canonical content on category-defining concepts</h3>
<p>Pick the four to six concepts the brand wants to own. Write the canonical resource on each &mdash; long-form, structured, with named frameworks and original perspectives. Make sure the content is the source LLMs prefer to cite, which means it has to be well-structured, factual, and indexable.</p>

<h3>2. Schema and structured data</h3>
<p>Schema.org markup helps LLMs parse the content correctly. FAQ schema, How-To schema, Article schema with author and date. The crawler still needs the metadata; LLMs increasingly rely on it for credibility signals.</p>

<h3>3. Earned mentions in authoritative third-party sources</h3>
<p>LLMs weight sources they've seen referenced elsewhere. A guest post in an authoritative trade publication that links back to the canonical resource creates a reinforcement loop &mdash; the model sees the brand referenced and weights it higher when generating answers in the category.</p>

<h3>4. A brand POV worth citing</h3>
<p>The single biggest GEO mistake B2B brands make is publishing generic content. LLMs don't cite generic content because they already have it from a thousand sources. They cite content with a clear, named, contestable POV. The framework that has a name and a defender is the framework that gets cited.</p>

<h2>How to measure it</h2>
<p>Track three things: brand mentions inside LLM answers for category queries (manually sampled weekly until tooling matures), referral traffic from LLM citations (measurable once LLMs add referrer headers, which they're slowly doing), and direct traffic from category-defining phrases. The first is the leading indicator; the others lag.</p>

<h2>What changes for SEO budgets</h2>
<p>Traditional SEO &mdash; technical, content, link-building &mdash; remains useful but no longer sufficient. GEO is the new line item. The B2B brands that already had a clear point of view and well-structured content win this transition cheaply. The brands that built SEO on volume and thin pages have to rebuild from scratch.</p>
"""
    },

    {
        "slug":"march-2026-core-update-d2c",
        "cat":"SEO","cat_key":"seo",
        "title":"What the March 2026 core update actually changes for D2C SEO",
        "seo_title":"March 2026 Google Core Update for D2C SEO | Digitaltheory",
        "excerpt":"Core updates have been compressing thin-content sites for years. The latest cycle tightens the screws on aggregator pages and lifts brand-led editorial.",
        "date":"2026-04-22","read":"5 min read",
        "body":"""
<p class="post__lead">Google's spring core update has shifted the SERP landscape for D2C brands again. The direction of travel is the same as the last three updates: thin product-feed pages lose, brand-led editorial wins. Here is what's worth doing about it.</p>

<h2>What the update favours</h2>
<p>Three signals appear to have been weighted up in this cycle:</p>
<ul>
  <li><strong>Original editorial alongside the catalogue.</strong> Brands that publish category guides, buying advice, and product comparisons in a serious editorial register (not thin SEO copy) are seeing category-query rankings hold and grow.</li>
  <li><strong>Author and brand entity signals.</strong> Bylined content with structured author markup, and brands whose Knowledge Graph entry is well-formed, are ranking measurably better. Anonymous content is degrading.</li>
  <li><strong>Site-level UX signals.</strong> Core Web Vitals weren't a tie-breaker before; they appear to be one now. Mobile interactivity in particular.</li>
</ul>

<h2>What the update penalises</h2>
<p>The losers are predictable but worth naming:</p>
<ul>
  <li><strong>Faceted-navigation pages with thin content.</strong> The pages that exist only because they map to a filter combination, with no editorial voice, are getting compressed.</li>
  <li><strong>Aggregator-style PLP pages</strong> that pull in product data without categorical narrative are losing share to brand-led editorial PLPs.</li>
  <li><strong>Affiliate-thin content</strong>. "Top 10" pages with shallow takes are getting demoted in favour of brand-published editorial with a clearer POV.</li>
</ul>

<h2>The three moves that pay back in 2026</h2>

<h3>1. Convert top PLPs into editorial pages</h3>
<p>Take the top 20 product listing pages by traffic and rebuild each with a category guide on top, then the catalogue below. Same SKU set, much stronger ranking signal.</p>

<h3>2. Build a real author program</h3>
<p>Named editors, bylined content, author bios with credentials and links. The signal looks small; the ranking impact compounds.</p>

<h3>3. Fix Core Web Vitals as a sprint, not a project</h3>
<p>If the brand is on Shopify, this is mostly a theme overhaul plus image optimisation. If it's headless, it's a sprint of LCP and INP fixes. Either way, two-week effort, measurable lift.</p>

<h2>What not to do</h2>
<p>Don't move budget away from SEO into paid in panic. Core updates create volatility, not a verdict. The teams that win the next 12 months are the ones that lean into editorial and entity signals, not the ones that abandon the channel.</p>
"""
    },

    {
        "slug":"brand-measurement-performance-cadence",
        "cat":"Performance Marketing","cat_key":"performance",
        "title":"How to measure brand at a performance cadence",
        "seo_title":"How to Measure Brand at a Performance Cadence | Digitaltheory",
        "excerpt":"Brand is usually measured quarterly with surveys nobody reads. Performance is measured daily. Track brand at weekly cadence using signals already in the stack.",
        "date":"2026-03-30","read":"6 min read",
        "body":"""
<p class="post__lead">The argument between brand and performance is usually about which gets the budget. The real problem is that brand is measured quarterly with surveys nobody reads, while performance is measured daily. No CFO is going to reallocate from a daily-measured channel to a quarterly-measured one. The fix is to measure brand at performance cadence.</p>

<h2>Three signals you already have</h2>
<p>The brand-measurement industry has done a good job convincing marketers that brand health requires expensive tracker studies. It doesn't. Three signals already in most stacks give a usable weekly read:</p>

<h3>1. Branded share-of-search</h3>
<p>Search volume on the brand's name, divided by total category search volume. Tracked weekly, this is the cleanest brand-strength signal that exists. Volume grows = brand grows. Volume shrinks = brand shrinks. The data is free and weekly.</p>

<h3>2. Direct-traffic and branded-CPC trajectory</h3>
<p>Direct traffic that's grown 30% while paid spend is flat means brand strength is rising. Branded CPC that's stable while category CPC rises means competitor bidders aren't beating the brand on its own terms. Both are weekly-trackable.</p>

<h3>3. Organic mention velocity</h3>
<p>Mentions of the brand on social, in podcasts, in editorial &mdash; not paid placements, organic mentions. Measurable via standard social listening tools, weighted by source authority. Trends weekly.</p>

<h2>What weekly cadence changes</h2>
<p>When brand is tracked weekly, three things shift:</p>
<ul>
  <li><strong>Brand campaigns get budget defended.</strong> A CFO who sees branded SOS climbing 3% week-over-week during a brand campaign will renew the budget. A CFO who sees a quarterly tracker survey three months later won't.</li>
  <li><strong>Brand-lift experiments become possible.</strong> Run a brand campaign in three regions, hold out a fourth, compare branded SOS trajectories. Two-week test, decisive read.</li>
  <li><strong>Performance becomes cheaper.</strong> Branded SOS growth flows back into lower branded CPC and higher overall ROAS. The brand spend literally pays for itself in the performance line item, but only if both are measured together.</li>
</ul>

<h2>The framework</h2>
<p>Pick the three signals above. Set up a weekly dashboard. Tie every brand campaign to a target trajectory on at least one signal. Run brand-lift studies as A/B tests across regions or audiences. Report brand metrics in the same weekly review as performance metrics, in the same room, to the same audience.</p>
<p>The brand-versus-performance war ends when both are measured at the same cadence, in front of the same people, with the same accountability.</p>
"""
    },

    {
        "slug":"abm-without-noise",
        "cat":"B2B Marketing","cat_key":"b2b",
        "title":"ABM without the noise: a stripped-down B2B playbook",
        "seo_title":"ABM Without the Noise: A B2B Playbook | Digitaltheory",
        "excerpt":"Account-based marketing has been over-engineered into a discipline only enterprise teams can afford. The stripped-down version works for mid-market SaaS too.",
        "date":"2026-03-10","read":"6 min read",
        "body":"""
<p class="post__lead">ABM has been over-engineered. The category is dominated by enterprise-software vendors selling intent-data platforms, predictive scoring, signal orchestration and customer-journey graphs. None of which a 30-person SaaS team needs to ship a working program. Here is the stripped-down version.</p>

<h2>Three tiers, three motions</h2>
<p>Group target accounts into three tiers. Each gets a different motion. None of them require a six-figure stack.</p>

<h3>Tier 1: 50 accounts, white-glove</h3>
<p>Hand-picked, named, and treated like deals already in the pipeline. Each gets a personalised mini-site or a tailored deck, named-account sequences across email and LinkedIn, and direct outbound from a senior salesperson. Marketing's job is to produce the assets; sales's job is to run the play.</p>

<h3>Tier 2: 500 accounts, 1-to-few</h3>
<p>Segmented by ICP, vertical and stage. Each segment gets a tailored campaign &mdash; not personalised per account, but personalised per cohort. The asset is a category-specific guide; the channel is paid LinkedIn and a sequenced email program. Sales takes inbound replies; marketing runs the campaign.</p>

<h3>Tier 3: the broad ICP, 1-to-many</h3>
<p>The standard demand-gen motion. Top-of-funnel content, paid distribution, lead capture, nurture. Most teams are already doing this; the ABM frame just sharpens the targeting.</p>

<h2>What you don't need</h2>
<p>Three things the ABM vendor pitch will tell you are mandatory but aren't, at least at mid-market scale:</p>
<ul>
  <li><strong>An intent-data platform.</strong> Intent data is useful at enterprise scale. At mid-market, it's noisy and over-priced. LinkedIn engagement, website behaviour and outbound replies tell most of the same story for free.</li>
  <li><strong>A predictive scoring model.</strong> ICP fit + a recent trigger event (funding round, hiring spike, leadership change) covers 80% of what a model would surface. Triggers are scrapeable.</li>
  <li><strong>A full ABM platform.</strong> A CRM, a sequencing tool, an email tool and LinkedIn cover the workflow. The platform mostly adds dashboards.</li>
</ul>

<h2>What you do need</h2>
<p>The three things that make or break a stripped-down ABM program:</p>
<ul>
  <li><strong>Sales-marketing alignment on the tier definitions.</strong> If sales and marketing disagree on what a tier-1 account is, the program collapses.</li>
  <li><strong>A weekly account review.</strong> Sales and marketing in the same room, reviewing tier-1 and tier-2 engagement, deciding what moves next.</li>
  <li><strong>Patience.</strong> ABM programs take 6&ndash;9 months to show pipeline impact. The teams that kill them at month four don't get the compounding.</li>
</ul>

<h2>The deeper point</h2>
<p>ABM works at mid-market scale. It just doesn't work the way the enterprise-vendor pitch describes it. Strip out the platform spend, keep the strategy, run the three motions, and report on pipeline by tier monthly. The discipline is in the segmentation and the alignment, not the tooling.</p>
"""
    },
]
BLOG_CATEGORIES = ["All","Performance Marketing","D2C & E-commerce","CRM & Retention","Edtech","Growth Strategy","SEO","MarTech","B2B Marketing"]

def fmt_date(iso):
    months = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
    y,m,d = iso.split("-")
    return f"{int(d)} {months[int(m)-1]} {y}"

def render_blog_post(p):
    return f"""
<section class="page-hero" style="padding-block:clamp(2.5rem,5vw,4rem) 0;background:var(--ink-1000)">
  <div class="container">
    <a href="../blog.html" style="font-family:var(--font-mono);font-size:12px;letter-spacing:.14em;color:var(--fg-muted);text-transform:uppercase">← All blogs</a>
  </div>
</section>
<article class="container">
  <div class="post">
    <header class="post__head">
      <span class="post__cat">{p["cat"]}</span>
      <h1 class="post__title">{p["title"]}</h1>
      <div class="post__meta">
        <span>By Digitaltheory</span>
        <span>{fmt_date(p["date"])}</span>
        <span>{p["read"]}</span>
      </div>
    </header>
    <div class="post__body">{p["body"]}</div>
  </div>
</article>
{CTA_BAND.format(base='../')}
"""

def build_blog_hub():
    counts = {cat: sum(1 for p in BLOG_POSTS if p["cat"]==cat) for cat in BLOG_CATEGORIES[1:]}
    counts["All"] = len(BLOG_POSTS)
    tabs_html = "".join(
        f'<button class="work-tab {"is-active" if cat=="All" else ""}" data-tab="{cat}">{cat} <span class="work-tab__count">({counts[cat]})</span></button>'
        for cat in BLOG_CATEGORIES if counts.get(cat,0) > 0 or cat=="All"
    )
    cards = ""
    for p in BLOG_POSTS:
        words = p["title"].split()
        big_text = " ".join(words[:5]) + ("..." if len(words) > 5 else "")
        cards += f'''
        <a class="blog-card" data-cat="{p["cat"]}" href="blog/{p["slug"]}.html">
          <div class="blog-card__cover"><span class="blog-card__cover-text">{big_text}</span></div>
          <div class="blog-card__body">
            <span class="blog-card__cat">{p["cat"]}</span>
            <h3 class="blog-card__title">{p["title"]}</h3>
            <p class="blog-card__excerpt">{p["excerpt"]}</p>
            <div class="blog-card__meta"><span>{fmt_date(p["date"])}</span><span>{p["read"]}</span></div>
          </div>
        </a>'''
    body = f"""
<section class="page-hero">
  <div class="container page-hero__inner">
    <span class="eyebrow">The Digitaltheory blog</span>
    <h1>Growth Marketing Trends, Strategies and Expert Insights</h1>
  </div>
</section>
<section class="section">
  <div class="container">
    <div class="sec-head"><div><span class="eyebrow">Latest articles</span><h2>Field notes from inside our engagements</h2></div><p class="lead">Frameworks, playbooks and post-mortems from performance, D2C, edtech and MarTech work.</p></div>
    <div class="work-tabs" id="blogTabs">{tabs_html}</div>
    <div class="blog-grid" id="blogGrid">{cards}</div>
    <div class="work-empty" id="blogEmpty" style="display:none">No posts in this category yet — more on the way.</div>
  </div>
</section>
{CTA_BAND.format(base='')}
<script>
(function(){{
  const tabs = document.querySelectorAll('#blogTabs .work-tab');
  const cards = document.querySelectorAll('#blogGrid .blog-card');
  const empty = document.getElementById('blogEmpty');
  tabs.forEach(b => b.addEventListener('click', () => {{
    tabs.forEach(x => x.classList.toggle('is-active', x === b));
    const cat = b.dataset.tab;
    let visible = 0;
    cards.forEach(c => {{
      const match = cat === 'All' || c.dataset.cat === cat;
      c.style.display = match ? '' : 'none';
      if (match) visible++;
    }});
    empty.style.display = visible === 0 ? 'block' : 'none';
  }}));
}})();
</script>
"""
    return page("Growth Marketing Blog — Trends & Frameworks",
                "Digitaltheory blog — field notes on performance marketing, retention, D2C unit economics, MarTech and SEO grounded in real engagements.",
                body, base="", active="", path="blog.html")

# ====================== INDUSTRY PAGES ======================
INDUSTRIES = [
    {
        "slug":"d2c-ecommerce","title":"D2C & E-commerce",
        "h1":"D2C and E-commerce growth marketing, engineered to the P&amp;L.",
        "lead":"From paid acquisition to retention loops to creative testing, we build the operating engine behind D2C brands that compound — not just spike.",
        "intro_h":"The D2C playbook has changed. Yours should too.",
        "intro":"CAC is rising every quarter, marketplaces are commoditising direct channels, and most performance-only playbooks die at the contribution-margin line. We work inside D2C and e-commerce businesses to rebuild the system — pricing, channel mix, creative, retention — so growth pays.",
        "challenges":[
            ("Rising CAC, falling ROAS","Auction prices climb every quarter and yesterday&rsquo;s playbook stops paying back.","trend"),
            ("Marketplace vs D2C tension","Amazon and Flipkart cannibalise the direct channel — and unit economics fracture across both.","grid"),
            ("Low repeat rate","Acquisition spend keeps growing because LTV isn&rsquo;t growing fast enough alongside it.","repeat"),
            ("Creative fatigue","Ad creative dies in two weeks and there&rsquo;s no system to ship fresh hypotheses fast.","sparkle"),
            ("Inventory &amp; OOS chaos","Bestsellers go out of stock; long-tail sits in the warehouse — both hit the P&amp;L.","box"),
            ("Attribution &amp; reporting fog","Platforms claim wildly different numbers and nobody trusts the dashboard.","chart"),
        ],
        "solutions":[
            "Full-funnel media mix tied to LTV, not last-click attribution",
            "Quadcore campaign architecture across prospecting, retargeting, brand defence and creator-led",
            "RFM segmentation, lifecycle journeys and loyalty programs that lift retention 15–25%",
            "Creative testing framework that ships weekly batches scored against hypotheses",
            "Predictive inventory modelling to manage OOS and CM3 sustainability",
            "Marketplace + D2C pricing parity, MAP enforcement and channel-level margin tracking",
        ],
        "clients":[("Celio","celio.in"),("Pepperfry","pepperfry.com"),("Chumbak","chumbak.com"),("Meatton","meatton.com"),("Ira Soleil","irasoleil.com"),("put-chi","put-chi.com")],
        "cases":[("celio","Celio","D2C Menswear","Heritage menswear brand. Rebuilt paid search, paid social, D2C ops, pricing and retention loops — 45% ROAS lift, 23% CM3.","45","%","ROAS lift","23","%","CM3 lift"),
                 ("nutriglow","Nutriglow","Beauty & Personal Care","200+ SKU brand. Pricing, sourcing &amp; channel-mix turnaround drove 35% QoQ growth.","57","%","ROAS lift","40","%","COGS cut")],
    },
    {
        "slug":"beauty-personal-care","title":"Beauty & Personal Care",
        "h1":"Beauty &amp; personal care growth, solved at the contribution-margin line.",
        "lead":"Hyper-competitive auctions, fragile SKU velocity, marketplaces eating margin — we rebuild beauty brands from COGS and channel mix upward.",
        "intro_h":"Beauty &amp; PC is a margin game now. Not just a topline game.",
        "intro":"Topline grew, then profit didn&rsquo;t. Sound familiar? In beauty &amp; personal care, 200+ SKU portfolios live or die on contribution margin. We diagnose pricing, sourcing and channel mix, ship the right NPDs, restructure your Amazon SB/SD, and tie every campaign back to LTV.",
        "challenges":[
            ("SKU velocity dropping","Hero SKUs lose share, long-tail eats your shelf and your media spend.","trend"),
            ("COGS leakage","Sourcing margins erode quietly and CM1 slips without anyone catching it.","chart"),
            ("Marketplace saturation","Amazon &amp; Nykaa are crowded — basic SB/SD architectures don&rsquo;t cut through anymore.","grid"),
            ("Claims compliance","Creative gets blocked, then approved, then blocked — and no one tracks the cost.","shield"),
            ("Content velocity","UGC and creator content need to ship weekly, not quarterly.","sparkle"),
            ("NPD launch waste","New products launch without a plan and quietly fail in the bestseller flywheel.","box"),
        ],
        "solutions":[
            "Strategic supplier sourcing that lowers COGS 30–40%",
            "Marketplace Sponsored Brand &amp; Sponsored Display architecture rebuilt on bestseller hierarchy",
            "NPD ideation, gating and launch playbooks integrated with media plan",
            "Full-funnel media mix tied to retention and LTV, not just first-purchase ROAS",
            "Claims-safe creative testing framework that ships weekly batches",
            "RFM-led CRM journeys for refill, replenishment and cross-category cross-sell",
        ],
        "clients":[("Nutriglow","nutriglowcosmetics.com"),("svaa.life","svaa.life"),("august","itsaugust.co")],
        "cases":[("nutriglow","Nutriglow","Beauty & Personal Care","Turned a 17% YoY profit decline into 35% QoQ growth via pricing, sourcing and full-funnel media.","57","%","ROAS lift","14","%","CM3 lift")],
    },
    {
        "slug":"edtech","title":"Edtech",
        "h1":"Edtech growth without the CAC death spiral.",
        "lead":"Lower CAC. Lift SQL share. Reengineer onboarding. We help K-12 and higher-ed platforms compound — and expand internationally when the India market saturates.",
        "intro_h":"Edtech is funnel engineering, end to end.",
        "intro":"The Indian edtech market is saturated and CAC won&rsquo;t come down by tweaking bids. We identify under-penetrated international markets, rebuild the funnel from LP to sales follow-up to student onboarding, and drive paid LTV that justifies the spend.",
        "challenges":[
            ("CAC rising MoM","Bids climb every month and the cash flow doesn&rsquo;t hold.","trend"),
            ("Low MQL→SQL conversion","Marketing fills the top of the funnel but sales can&rsquo;t close fast enough.","repeat"),
            ("LP &amp; form-fill drop-off","Landing pages convert below industry; nobody knows which element to fix first.","chart"),
            ("Saturated home market","India CAC is plateauing and international expansion isn&rsquo;t scoped.","grid"),
            ("Onboarding completion","SQL share stuck below 30%; students drop before paying.","box"),
            ("Brand search flat","Performance keeps spending but branded search isn&rsquo;t growing alongside.","sparkle"),
        ],
        "solutions":[
            "International market entry — country prioritisation, pilot campaigns, scale strategy",
            "Landing page CRO program scoring hypotheses weekly",
            "Sales follow-up cadence and SQL design tied to paid LTV",
            "Student onboarding flow optimisation that lifts SQL from 30% to 47%",
            "Full-funnel media mix with brand-lift studies for branded search growth",
            "ASO program for app-led admissions / installs",
        ],
        "clients":[("Codingal","codingal.com"),("upGrad","upgrad.com"),("Eurokids","eurokidsindia.com"),("School Basix","schoolbasix.com")],
        "cases":[("codingal","Codingal","K-12 Edtech","Scaled to 5L+ students with 10x revenue. 70% lower CAC via international expansion, 47% SQL share post-onboarding revamp.","66","%","MQL lift","70","%","CAC cut")],
    },
    {
        "slug":"consumer-apps","title":"Consumer Apps",
        "h1":"Consumer app growth: install quality first, retention second, monetisation always.",
        "lead":"Mobile-first growth done right — event-driven acquisition, RFM-led CRM, loyalty programs and ASO that compound LTV.",
        "intro_h":"Installs are vanity. LTV is the business.",
        "intro":"Most consumer apps optimise for installs and watch LTV degrow. We rebuild tracking around high-intent events, segment your audience with RFM, layer in CRM nudges across push and WhatsApp, and ship a loyalty program that lifts repeat purchase — all tied to a CAC that pays back.",
        "challenges":[
            ("Unqualified installs","Volume looks great until you check Day-7 retention.","trend"),
            ("LTV degrowth","Quarter-over-quarter LTV falls and unit economics quietly invert.","chart"),
            ("RFM blindness","No segmentation between high-value, churning and lost users — same comms to all.","grid"),
            ("Attribution gaps","Event tracking is shallow and platforms claim conflicting attribution.","shield"),
            ("Push fatigue","Notifications get muted; retention CRM stops working.","sparkle"),
            ("ASO untapped","App store rank is left to chance — organic installs flatten.","box"),
        ],
        "solutions":[
            "Robust event tracking and high-intent event modelling",
            "RFM segmentation across 12+ months of data identifying churn-risk and high-value cohorts",
            "CRM nudges across push, WhatsApp, email and in-app, with cadence engineered to retention",
            "Loyalty program design with tiering and rewards engineered for repeat",
            "Affiliate marketing on transaction-based payouts to add 10–15% incremental revenue",
            "Full ASO program — keyword research, rich media, on/off-page SEO for organic installs",
        ],
        "clients":[("Laundrokart","laundrokart.com")],
        "cases":[("laundrokart","Laundrokart","Consumer App","12-year-old laundry app. Event tracking + RFM + loyalty drove 45% revenue lift, 23% LTV improvement.","55","%","Installs lift","23","%","LTV lift")],
    },
    {
        "slug":"gaming","title":"Real-money Gaming",
        "h1":"Gaming growth without the CAC spiral.",
        "lead":"Channel scoring, affiliate frameworks rebuilt around player value, and an ASO program that drives organic installs while CAC compresses.",
        "intro_h":"Gaming is a player-economics game.",
        "intro":"Every player has an ARPU, an LTV and a churn curve. We score channels against those, kill what doesn&rsquo;t pay, scale what does, and run the ASO + creative + CRM loop that delivers profitable installs at scale.",
        "challenges":[
            ("CAC not coming down","Spend grows, CAC doesn&rsquo;t fall — and cash flow gets brittle.","trend"),
            ("LTV improvement plateau","Player LTV stops growing despite product releases.","chart"),
            ("Affiliate waste","High-volume affiliates send low-value players; nobody is unwinding it.","grid"),
            ("ASO untapped","Organic install share stays flat; brand search doesn&rsquo;t compound.","box"),
            ("Creative fatigue","Performance creative cycles die fast in regulated categories.","sparkle"),
            ("Compliance creative drag","Disclaimers and regulations slow down testing cadence.","shield"),
        ],
        "solutions":[
            "Channel scoring on QoQ growth, LTV, ARPU and CAC — kill the low-value, scale the high",
            "Affiliate framework rebuilt on player engagement model, not install volume",
            "LTV-based Meta and Google audience modelling",
            "Rich media images, ASO description rewrite and on/off-page SEO",
            "RFM-led CRM nudges and in-app offers for loyalty cohorts",
            "Creative testing framework adapted for regulated-category constraints",
        ],
        "clients":[("Pocket52","pocket52.com")],
        "cases":[("pocket52","Pocket52","Real-money Gaming","One of India&rsquo;s fastest 1M-download gaming apps. 45% CAC cut, 20% organic installs lift, 18% LTV improvement.","45","%","CAC cut","20","%","Organic lift")],
    },
    {
        "slug":"retail-pharma","title":"Retail & Pharma",
        "h1":"Retail &amp; pharma operations: digitised, modelled, profitable.",
        "lead":"Inventory automation, store-level SKU fit modelling, returns prediction and ERP integration — for chains where margin lives in the operations.",
        "intro_h":"Brick-and-mortar margin lives in the small decisions.",
        "intro":"SKU mix by store. Returns by month. Fill-in vs sell-out by season. For multi-branch retail and pharmacy chains, the next 10% of margin lives in those decisions. We integrate ERPs, ship inventory tools and train ML models that predict store-level product fit.",
        "challenges":[
            ("Inventory imbalance","Bestsellers OOS at one branch, dead stock at another — both eat margin.","box"),
            ("Manual fill-in / sell-out","Operations are spreadsheet-driven and error-prone.","grid"),
            ("Returns leakage","Reverse logistics costs are invisible until quarterly close.","repeat"),
            ("SKU mix opacity","Nobody knows which SKUs sell best in which stores or seasons.","chart"),
            ("Demand prediction","Forecasting is a once-a-quarter exercise instead of an operating loop.","trend"),
            ("Margin leakage","Store-level P&amp;L is a black box; central can&rsquo;t see what&rsquo;s breaking.","shield"),
        ],
        "solutions":[
            "Digitisation software integrated with your existing ERP",
            "In-house inventory management tool with branch-level visibility",
            "Returns dashboards mapping product, branch and reverse-logistics cost",
            "ML models for store-level product fit and returns prediction",
            "BI reporting that surfaces the right decisions to the right roles",
            "Training, SOPs and change-management so adoption sticks",
        ],
        "clients":[("Thulasi","thulasipharmacies.lk")],
        "cases":[("thulasi","Thulasi Pharmacy","Retail & Pharma","80+ branch chain. ERP integration + ML for store fit drove 33% inventory cost cut, 37% returns reduction, 19% revenue lift.","33","%","Inventory cost ↓","37","%","Returns ↓")],
    },
    {
        "slug":"fintech","title":"Fintech",
        "h1":"Fintech growth inside the regulatory rails.",
        "lead":"Compliance-aware creative, trust-building funnels and full-funnel media — built for investment, payments and lending categories where trust is the unlock.",
        "intro_h":"Fintech wins when trust scales with growth.",
        "intro":"KYC drop-off, compliance review cycles, trust-signal scarcity — fintech CAC is rarely about traffic, it&rsquo;s about conversion. We build creative that respects category constraints, retention CRM that drives habit, and brand-lift studies that grow branded search over time.",
        "challenges":[
            ("KYC drop-off","Onboarding funnels lose users at the regulatory steps.","shield"),
            ("Compliance creative drag","Every ad goes through review cycles that slow the testing cadence.","grid"),
            ("Trust signal scarcity","First-time users need proof; competitors have it, you&rsquo;re building it.","chart"),
            ("Habit formation","Retention depends on weekly engagement, not just first purchase.","repeat"),
            ("Attribution noise","Long consideration windows blur attribution and confuse channel decisions.","trend"),
            ("Brand search flat","Performance spending grows, brand search doesn&rsquo;t — and CAC keeps rising.","sparkle"),
        ],
        "solutions":[
            "Compliance-aware creative testing framework with pre-approved variations",
            "KYC and onboarding CRO with friction-point removal",
            "Retention CRM around habit-forming actions — invest, repay, transact",
            "Full-funnel media mix with brand-lift studies for branded search growth",
            "Affiliate and partnership programs with quality-scored payouts",
            "Long-window attribution modelling tying channel to LTV, not first-touch",
        ],
        "clients":[("Groww","groww.in"),("Onecheq","onecheq.com")],
        "cases":[],
    },
    {
        "slug":"saas-b2b-tech","title":"SaaS & B2B Tech",
        "h1":"SaaS growth marketing tied to pipeline, not impressions.",
        "lead":"Account-based marketing, intent-led content engines, lifecycle nurturing and sales-marketing alignment — engineered to MQL→SQL→revenue.",
        "intro_h":"B2B is a buying-committee game.",
        "intro":"Long sales cycles, fragmented buying committees, deep ICP nuance — B2B SaaS marketing only pays when it&rsquo;s wired to pipeline. We build the ABM program, the content engine and the attribution stack that gets your CFO behind the spend.",
        "challenges":[
            ("Long sales cycles","Pipeline takes months to mature; nobody can prove what worked.","repeat"),
            ("ICP fit opacity","Marketing fills the funnel; sales rejects it as poor-fit.","grid"),
            ("Content velocity","Subject-matter content needs to ship weekly, not quarterly.","sparkle"),
            ("Account-based gap","Top accounts get the same messaging as the long tail.","trend"),
            ("Low MQL→SQL conversion","Form fills don&rsquo;t become opportunities and nobody knows why.","chart"),
            ("Attribution &amp; reporting","Marketing claims influence on every deal; sales claims none.","shield"),
        ],
        "solutions":[
            "ABM strategy across tier-1, tier-2 and broad accounts with role-based messaging",
            "Intent-led content engine that ships weekly across blog, LinkedIn and email",
            "Lifecycle nurturing journeys mapped to buying-committee personas",
            "Sales-marketing alignment with shared definitions of MQL, SQL and SAL",
            "Attribution model linking marketing activity to closed-won revenue",
            "Conversion-optimised demo flow, free-trial onboarding and pricing-page CRO",
        ],
        "clients":[],
        "cases":[],
    },
]

def render_industry_body(ind):
    icon_svg = {
        "trend":'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M3 17l6-6 4 4 8-8"/><path d="M14 7h7v7"/></svg>',
        "grid":'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="7" height="7" rx="1"/><rect x="14" y="3" width="7" height="7" rx="1"/><rect x="3" y="14" width="7" height="7" rx="1"/><rect x="14" y="14" width="7" height="7" rx="1"/></svg>',
        "repeat":'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M17 1l4 4-4 4"/><path d="M3 11V9a4 4 0 014-4h14"/><path d="M7 23l-4-4 4-4"/><path d="M21 13v2a4 4 0 01-4 4H3"/></svg>',
        "sparkle":'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3v4M12 17v4M3 12h4M17 12h4M5.6 5.6l2.8 2.8M15.6 15.6l2.8 2.8M5.6 18.4l2.8-2.8M15.6 8.4l2.8-2.8"/></svg>',
        "box":'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M21 16V8a2 2 0 00-1-1.73l-7-4a2 2 0 00-2 0l-7 4A2 2 0 003 8v8a2 2 0 001 1.73l7 4a2 2 0 002 0l7-4A2 2 0 0021 16z"/><path d="M3.27 6.96L12 12l8.73-5.04M12 22V12"/></svg>',
        "chart":'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="20" x2="18" y2="10"/><line x1="12" y1="20" x2="12" y2="4"/><line x1="6" y1="20" x2="6" y2="14"/></svg>',
        "shield":'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>',
    }
    challenges_html = "".join(
        f'<div class="ind-tile"><div class="ind-tile__icon">{icon_svg.get(ic, icon_svg["grid"])}</div><h3>{t}</h3><p>{d}</p></div>'
        for t,d,ic in ind["challenges"]
    )
    solutions_html = "".join(f"<li>{s}</li>" for s in ind["solutions"])
    clients_html = "".join(
        f'<div class="logo-cell" title="{n}"><img src="https://www.google.com/s2/favicons?domain={d}&sz=128" alt="{n} logo" loading="lazy" onerror="this.parentElement.classList.add(\'logo-cell--fallback\');this.outerHTML=\'<span>{n}</span>\'" /><span class="logo-cell__name">{n}</span></div>'
        for n,d in ind["clients"]
    ) if ind["clients"] else ""
    cases_html = "".join(
        f'<a class="case" href="../case-studies/{slug}.html"><div class="case__head"><div class="case__brand">{brand}</div><span class="case__industry">{cat}</span></div><p class="case__desc">{desc}</p><div class="case__metrics"><div class="stat case__metric"><div class="stat__num">{m1v}<span class="unit">{m1u}</span></div><div class="stat__label">{m1l}</div></div><div class="stat case__metric"><div class="stat__num">{m2v}<span class="unit">{m2u}</span></div><div class="stat__label">{m2l}</div></div></div><span class="case__link">Read case study →</span></a>'
        for slug,brand,cat,desc,m1v,m1u,m1l,m2v,m2u,m2l in ind["cases"]
    )
    clients_block = f'<section class="ind-clients"><div class="container"><p class="ind-clients__label">Clients we&rsquo;ve grown in this space</p><div class="logos-grid">{clients_html}</div></div></section>' if clients_html else ''
    cases_block = f'<section class="section"><div class="container"><div class="sec-head"><div><span class="eyebrow">Success stories</span><h2>Growth marketing case studies</h2></div><p class="lead">When a tile isn&rsquo;t enough, the case study has the strategy, the experiments and the numbers behind the outcome.</p></div><div class="bc-cases">{cases_html}</div></div></section>' if cases_html else ''

    return f"""
<section class="ind-hero">
  <div class="container ind-hero__inner">
    <a href="../case-studies.html" style="font-family:var(--font-mono);font-size:12px;letter-spacing:.14em;color:var(--fg-muted);text-transform:uppercase">← Industries</a>
    <span class="eyebrow" style="margin-top:24px;justify-content:center;display:inline-flex">{ind["title"]}</span>
    <h1>{ind["h1"]}</h1>
    <p class="ind-hero__lead">{ind["lead"]}</p>
    <div class="ind-hero__cta">
      <a href="../contact.html" class="btn btn--primary btn--lg">Talk to our experts <span class="btn__arrow">→</span></a>
      <a href="#solutions" class="btn btn--secondary btn--lg">See our approach</a>
    </div>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="ind-intro">
      <span class="eyebrow" style="justify-content:center">The opportunity</span>
      <h2>{ind["intro_h"]}</h2>
      <p>{ind["intro"]}</p>
    </div>
  </div>
</section>

<section class="section" style="background:var(--surface-section);border-block:1px solid var(--line)">
  <div class="container">
    <div class="sec-head">
      <div><span class="eyebrow">Challenges</span><h2 style="max-width:22ch">What we see inside {ind["title"]} businesses</h2></div>
      <p class="lead">Different brand, same six problems. Here&rsquo;s where the value usually leaks — and where we usually start.</p>
    </div>
    <div class="ind-grid">{challenges_html}</div>
  </div>
</section>

<section class="section" id="solutions">
  <div class="container">
    <div class="ind-solutions">
      <div>
        <span class="eyebrow">Our solutions</span>
        <h2 style="margin-top:14px;max-width:18ch">How we engineer growth in {ind["title"]}</h2>
        <p class="lead" style="margin-top:18px">Each engagement is scoped to the lever that moves the business — not a fixed scope of deliverables. We pull from any combination of these.</p>
        <ul>{solutions_html}</ul>
        <a href="../contact.html" class="btn btn--primary btn--lg" style="margin-top:28px">Connect with us <span class="btn__arrow">→</span></a>
      </div>
      <div class="ind-solutions__visual">
        <h3>By the numbers</h3>
        <div class="bc-overview__stats">
          <div class="stat"><div class="stat__num">50<span class="unit">+</span></div><div class="stat__label">Brands scaled</div></div>
          <div class="stat"><div class="stat__num">100<span class="unit">Cr+</span></div><div class="stat__label">Ad spend managed</div></div>
          <div class="stat"><div class="stat__num">45<span class="unit">%</span></div><div class="stat__label">Avg ROAS lift</div></div>
          <div class="stat"><div class="stat__num">5L<span class="unit">+</span></div><div class="stat__label">Users acquired</div></div>
        </div>
      </div>
    </div>
  </div>
</section>

{clients_block}

{cases_block}

{CTA_BAND.format(base='../')}
"""

def build_industries_hub():
    cards = ''
    for i in INDUSTRIES:
        cards += f'<a class="service" href="industries/{i["slug"]}.html"><span class="service__index">→</span><h3 class="service__title">{i["title"]}</h3><p class="service__body">{i["lead"]}</p></a>'
    body = f"""
<section class="page-hero">
  <div class="container page-hero__inner">
    <span class="eyebrow">Industries</span>
    <h1>Deep operating reps across consumer and tech.</h1>
    <p class="lead page-hero__lead">Patterns travel across categories; specifics don&rsquo;t. Pick the industry that matches yours to see the levers we pull and the outcomes we&rsquo;ve already shipped.</p>
  </div>
</section>
<section class="section"><div class="container">
<div class="sec-head"><div><span class="eyebrow">All industries</span><h2>Categories we've operated inside</h2></div><p class="lead">Deep operating reps across consumer and tech verticals.</p></div>
<div class="services-grid">{cards}</div></div></section>
{CTA_BAND.format(base='')}
"""
    return page("Industries We Serve — D2C, Edtech, Fintech & More",
                "Digitaltheory industry expertise across D2C, beauty, edtech, consumer apps, gaming, retail, fintech and B2B SaaS.",
                body, base="", active="", path="industries.html",
                seo_title="Industries We Serve — D2C, Edtech, Fintech & More | Digitaltheory")

# ====================== ABOUT ======================
def build_about():
    body = f"""
<section class="page-hero">
  <div class="container page-hero__inner">
    <span class="eyebrow">About us</span>
    <h1>We are a growth marketing company that helps you with end-to-end business strategy.</h1>
    <p class="lead page-hero__lead">We help brand and business owners who need help determining the right marketing strategy — and the team to execute it. There are several benefits business owners feel when partnering with us.</p>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="solution__intro">
      <div>
        <span class="eyebrow">Vision &amp; mission</span>
        <h2 style="margin-top:12px">Real intelligence &gt; Artificial intelligence.</h2>
        <p class="lead" style="margin-top:16px">Our vision is to revolutionise the landscape of digital growth by seamlessly blending innovation, data-driven strategies and creative brilliance. We aspire to be the catalyst for our clients' exponential success — fostering lasting connections and driving sustainable growth.</p>
      </div>
      <div>
        <div class="case-detail__panel">
          <h3>By the numbers</h3>
          <div style="display:grid;grid-template-columns:1fr 1fr;gap:24px">
            <div class="stat"><div class="stat__num">50<span class="unit">+</span></div><div class="stat__label">Brands scaled</div></div>
            <div class="stat"><div class="stat__num">100<span class="unit">Cr+</span></div><div class="stat__label">Ad spend</div></div>
            <div class="stat"><div class="stat__num">5L<span class="unit">+</span></div><div class="stat__label">Users acquired</div></div>
            <div class="stat"><div class="stat__num">45<span class="unit">%</span></div><div class="stat__label">Avg ROAS lift</div></div>
          </div>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="section" style="background:var(--surface-section);border-block:1px solid var(--line)">
  <div class="container">
    <div class="sec-head"><div><span class="eyebrow">What we believe</span><h2>The values behind the work</h2></div></div>
    <div class="values-grid">
      <div class="value"><div class="value__num">01</div><h3>Proof, not promises</h3><p>Every claim we make is backed by a number. Every plan we ship has a metric attached to it. No vanity dashboards.</p></div>
      <div class="value"><div class="value__num">02</div><h3>Operators, not consultants</h3><p>We've run the brands, run the ads, shipped the apps. Our recommendations come from execution scars, not frameworks.</p></div>
      <div class="value"><div class="value__num">03</div><h3>Compounding, not spikes</h3><p>Anyone can buy a spike. We build engines that compound — across acquisition, retention and brand — quarter on quarter.</p></div>
    </div>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="sec-head"><div><span class="eyebrow">What we do</span><h2>End-to-end across the growth stack</h2></div></div>
    <div class="services-grid">
      <a class="service" href="services/performance-marketing.html"><span class="service__index">01</span><h3 class="service__title">Performance Marketing</h3><p class="service__body">Full-funnel paid acquisition across Meta, Google, Amazon and affiliates.</p></a>
      <a class="service" href="services/branding.html"><span class="service__index">02</span><h3 class="service__title">Branding</h3><p class="service__body">Identity, positioning and creative systems that travel across every surface.</p></a>
      <a class="service" href="services/web-development.html"><span class="service__index">03</span><h3 class="service__title">Web Development</h3><p class="service__body">D2C storefronts, landing pages and marketing sites that convert.</p></a>
      <a class="service" href="services/app-development.html"><span class="service__index">04</span><h3 class="service__title">App Development</h3><p class="service__body">Consumer apps with ASO, analytics and CRM baked in from day one.</p></a>
      <a class="service" href="services/business-consulting.html"><span class="service__index">05</span><h3 class="service__title">Business Consulting</h3><p class="service__body">Pricing, unit economics, NPD and channel-mix counsel grounded in your P&amp;L.</p></a>
      <a class="service" href="services/crm-retention.html"><span class="service__index">06</span><h3 class="service__title">CRM &amp; Retention</h3><p class="service__body">RFM segmentation, lifecycle journeys and loyalty programs that lift LTV.</p></a>
    </div>
  </div>
</section>

<section class="section" style="background:var(--surface-section);border-top:1px solid var(--line)">
  <div class="container">
    <div class="sec-head"><div><span class="eyebrow">In their words</span><h2>What clients say</h2></div></div>
    <div class="quotes">
      <figure class="quote"><div class="quote__mark">"</div><blockquote class="quote__body">We engaged with Digitaltheory for branding and performance marketing. They helped us scale our performance marketing with remarkable results.</blockquote><figcaption class="quote__who"><span class="quote__name">Sumit Singh</span><span class="quote__role">VP Marketing, Codingal</span></figcaption></figure>
      <figure class="quote"><div class="quote__mark">"</div><blockquote class="quote__body">We engaged with Digitaltheory for D2C business. They helped us improve our profits by 3x with NPD, operations, website maintenance and performance marketing.</blockquote><figcaption class="quote__who"><span class="quote__name">Abhijeet</span><span class="quote__role">Marketing Head, Chumbak</span></figcaption></figure>
    </div>
  </div>
</section>

{CTA_BAND.format(base='')}
"""
    return page("About Digitaltheory — Data-First Growth Marketing",
                "Digitaltheory is a data-first growth marketing company helping brands turn theory into durable growth across performance, branding, web, app and CRM.",
                body, base="", active="about", path="about.html")

# ====================== CAREERS ======================
def build_careers():
    roles = [
        ("Senior Performance Marketing Manager","Bengaluru","Full-time"),
        ("Creative Strategist","Mumbai / Remote","Full-time"),
        ("Data Analyst — Growth","Bengaluru","Full-time"),
        ("Brand Designer","Mumbai","Full-time"),
        ("React Native Engineer","Remote","Full-time"),
        ("CRM &amp; Lifecycle Lead","Bengaluru","Full-time"),
        ("Video Editor — Performance Creative","Mumbai","Full-time"),
        ("Account Manager — D2C","Bengaluru","Full-time"),
    ]
    role_html = ''.join(f'<div class="role"><div class="role__title">{t}</div><div class="role__meta">{loc}</div><div class="role__meta">{ty}</div><a href="mailto:careers@digitaltheory.in?subject={t}" class="btn btn--secondary btn--sm">Apply <span class="btn__arrow">→</span></a></div>' for t,loc,ty in roles)
    body = f"""
<section class="page-hero">
  <div class="container page-hero__inner">
    <span class="eyebrow">Careers</span>
    <h1>Build the growth engines that move the P&amp;L.</h1>
    <p class="lead page-hero__lead">We hire operators. People who own outcomes, not deliverables. If you want to do the best work of your career on brands you'll actually recognise, come talk to us.</p>
    <div class="page-hero__cta">
      <a href="#roles" class="btn btn--primary btn--lg">See open roles <span class="btn__arrow">→</span></a>
      <a href="mailto:careers@digitaltheory.in" class="btn btn--secondary btn--lg">Drop us a line</a>
    </div>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="sec-head"><div><span class="eyebrow">Why Digitaltheory</span><h2>What you can expect</h2></div></div>
    <div class="values-grid">
      <div class="value"><div class="value__num">01</div><h3>Real ownership</h3><p>Pods of 3–5 own a brand end-to-end. You see the brief, the budget, the dashboard and the outcome.</p></div>
      <div class="value"><div class="value__num">02</div><h3>Real budgets</h3><p>You'll work on accounts deploying ₹1 Cr–₹5 Cr a year, not ₹10 lakh test pots.</p></div>
      <div class="value"><div class="value__num">03</div><h3>Real upside</h3><p>Performance tied to outcomes — both for our clients and for you. Compensation, not promises.</p></div>
    </div>
  </div>
</section>

<section class="section" id="roles" style="background:var(--surface-section);border-block:1px solid var(--line)">
  <div class="container">
    <div class="sec-head"><div><span class="eyebrow">Open roles</span><h2>Currently hiring</h2></div><p class="lead">Don't see your role? Email us anyway — careers@digitaltheory.in</p></div>
    <div class="role-list">{role_html}</div>
  </div>
</section>

{CTA_BAND.format(base='')}
"""
    return page("Careers — Digitaltheory Growth Team",
                "Open roles at Digitaltheory across performance marketing, creative, engineering, data and CRM. Work on real brands with real budgets.",
                body, base="", active="careers", path="careers.html")

# ====================== CONTACT ======================
def build_contact():
    body = f"""
<section class="page-hero">
  <div class="container page-hero__inner">
    <span class="eyebrow">Come, say hello</span>
    <h1>Tell us where you want to go.</h1>
    <p class="lead page-hero__lead">We'll bring the strategy, the stack and the creative to get you there. Fill the form below or reach us directly — we usually reply within a business day.</p>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="contact-grid">
      <form class="form" onsubmit="event.preventDefault(); this.querySelector('button').textContent='Thanks — we\\'ll be in touch.';">
        <div><label>Your name</label><input type="text" required placeholder="Jane Doe" /></div>
        <div><label>Work email</label><input type="email" required placeholder="jane@brand.com" /></div>
        <div><label>Company</label><input type="text" placeholder="Brand Co." /></div>
        <div><label>What do you need help with?</label>
          <select>
            <option>Performance Marketing</option><option>Branding</option><option>Web Development</option>
            <option>App Development</option><option>Business Consulting</option>
            <option>SEO</option><option>CRM &amp; Retention</option><option>Not sure yet</option>
          </select>
        </div>
        <div><label>A bit about the project</label><textarea placeholder="Stage, goals, timelines, current numbers if you have them..."></textarea></div>
        <button type="submit" class="btn btn--primary btn--lg" style="margin-top:8px">Send message <span class="btn__arrow">→</span></button>
      </form>
      <div class="contact-info">
        <div class="contact-info__row">
          <div class="contact-info__label">Email</div>
          <div class="contact-info__value"><a href="mailto:hello@digitaltheory.in">hello@digitaltheory.in</a></div>
        </div>
        <div class="contact-info__row">
          <div class="contact-info__label">Careers</div>
          <div class="contact-info__value"><a href="mailto:careers@digitaltheory.in">careers@digitaltheory.in</a></div>
        </div>
        <div class="contact-info__row">
          <div class="contact-info__label">Bengaluru</div>
          <div class="contact-info__value">Indiranagar, Bengaluru 560038</div>
        </div>
        <div class="contact-info__row">
          <div class="contact-info__label">Mumbai</div>
          <div class="contact-info__value">Bandra West, Mumbai 400050</div>
        </div>
        <div class="contact-info__row">
          <div class="contact-info__label">Hours</div>
          <div class="contact-info__value">Mon–Fri · 10:00–19:00 IST</div>
        </div>
      </div>
    </div>
  </div>
</section>
"""
    return page("Contact Digitaltheory — Talk to Our Growth Team",
                "Contact Digitaltheory — offices in Bengaluru and Mumbai. Performance marketing, branding, web, app, CRM and consulting.",
                body, base="", active="contact", path="contact.html")

# ====================== WRITE ALL ======================
def write(path, content):
    full = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w") as f:
        f.write(content)
    print("wrote", path)

# Cases
slugs = [c["slug"] for c in CASES]
for idx, c in enumerate(CASES):
    prev_slug = slugs[idx-1] if idx > 0 else None
    next_slug = slugs[idx+1] if idx < len(CASES)-1 else None
    body = render_case_body(c, (prev_slug, next_slug))
    path = f"case-studies/{c['slug']}.html"
    desc = f"{c['brand']} ({c['industry']}) — case study by Digitaltheory. {c['hero']}"
    if len(desc) > 165:
        desc = desc[:155].rsplit(" ",1)[0] + "…"
    case_schema = {
        "@context":"https://schema.org","@type":"Article",
        "headline": f"{c['brand']} case study",
        "description": c["hero"],
        "author":{"@type":"Organization","name":"Digitaltheory","url":SITE_URL+"/"},
        "publisher":{"@type":"Organization","name":"Digitaltheory","url":SITE_URL+"/","logo":{"@type":"ImageObject","url":SITE_URL+"/assets/favicon.svg"}},
        "about":{"@type":"Organization","name": c["brand"]},
        "articleSection": c["industry"],
        "mainEntityOfPage":{"@type":"WebPage","@id": f"{SITE_URL}/{path}"},
        "url": f"{SITE_URL}/{path}","inLanguage":"en",
    }
    crumbs = [("Home",""),("Case Studies","case-studies.html"),(c["brand"], path)]
    write(path, page(f"{c['brand']} Case Study", desc, body, base="../", active="cases", path=path,
                     seo_title=(f"{c['brand']} Case Study | Digitaltheory" if len(c['brand'])+len(c['industry']) > 40 else f"{c['brand']} Case Study — {c['industry']} | Digitaltheory"),
                     extra_schema=[case_schema], breadcrumbs=crumbs))

write("case-studies.html", build_cases_hub())

# Services
for s in SERVICES:
    body = render_business_consulting_body() if s["slug"] == "business-consulting" else render_service_body(s)
    path = f"services/{s['slug']}.html"
    desc = "Strategy, growth, unit economics, market entry, NPD, M&A diligence — consulting that ships, not just advises." if s["slug"] == "business-consulting" else f"{s['title']} services by Digitaltheory. {s['hero']}"
    if len(desc) > 165:
        desc = desc[:155].rsplit(" ",1)[0] + "…"
    service_schema = {
        "@context":"https://schema.org","@type":"Service",
        "name": s["title"],
        "description": s["hero"],
        "provider": {"@type":"Organization","name":"Digitaltheory","url":SITE_URL+"/"},
        "areaServed": ["IN","AE","US","SG"],
        "serviceType": s["title"],
        "url": f"{SITE_URL}/{path}",
    }
    crumbs = [("Home",""),("Services","services.html"),(s["title"], path)]
    write(path, page(s["title"], desc, body, base="../", active="services", path=path,
                     seo_title=s.get("seo_title"),
                     extra_schema=[service_schema], breadcrumbs=crumbs))

write("services.html", build_services_hub())
write("our-work.html", build_our_work())

# Industry pages
for ind in INDUSTRIES:
    ipath = f"industries/{ind['slug']}.html"
    desc = ind["lead"]
    if len(desc) > 165:
        desc = desc[:155].rsplit(" ",1)[0] + "…"
    ind_schema = {
        "@context":"https://schema.org","@type":"Service",
        "name": f"{ind['title']} Growth Marketing",
        "description": ind["lead"],
        "provider":{"@type":"Organization","name":"Digitaltheory","url":SITE_URL+"/"},
        "audience":{"@type":"BusinessAudience","audienceType": ind["title"]},
        "url": f"{SITE_URL}/{ipath}",
    }
    crumbs = [("Home",""),("Industries","industries.html"),(ind["title"], ipath)]
    write(ipath, page(f"{ind['title']} Growth Marketing", desc, render_industry_body(ind), base="../", active="", path=ipath,
                      extra_schema=[ind_schema], breadcrumbs=crumbs))
write("industries.html", build_industries_hub())

# Blog
for p in BLOG_POSTS:
    bpath = f"blog/{p['slug']}.html"
    article_schema = {
        "@context":"https://schema.org","@type":"Article",
        "headline": p["title"],
        "description": p["excerpt"],
        "datePublished": p["date"],
        "dateModified": p["date"],
        "author": {"@type":"Organization","name":"Digitaltheory","url":SITE_URL+"/"},
        "publisher": {"@type":"Organization","name":"Digitaltheory","url":SITE_URL+"/","logo":{"@type":"ImageObject","url":SITE_URL+"/assets/favicon.svg"}},
        "articleSection": p["cat"],
        "mainEntityOfPage": {"@type":"WebPage","@id": f"{SITE_URL}/{bpath}"},
        "url": f"{SITE_URL}/{bpath}",
        "inLanguage":"en",
    }
    crumbs = [("Home",""),("Blog","blog.html"),(p["cat"],"blog.html"),(p["title"], bpath)]
    write(bpath, page(p["title"], p["excerpt"], render_blog_post(p),
                      base="../", active="", path=bpath,
                      seo_title=p.get("seo_title"),
                      extra_schema=[article_schema], breadcrumbs=crumbs))
write("blog.html", build_blog_hub())

write("about.html", build_about())
write("careers.html", build_careers())
write("contact.html", build_contact())

# ====================== SITEMAP & ROBOTS ======================
urls = ["", "services.html", "our-work.html", "case-studies.html", "industries.html", "blog.html", "about.html", "careers.html", "contact.html"]
urls += [f"services/{s['slug']}.html" for s in SERVICES]
urls += [f"case-studies/{c['slug']}.html" for c in CASES]
urls += [f"industries/{i['slug']}.html" for i in INDUSTRIES]
urls += [f"blog/{p['slug']}.html" for p in BLOG_POSTS]

today = "2026-06-07"  # update on rebuild
sitemap_entries = []
for u in urls:
    loc = f"{SITE_URL}/" if u == "" else f"{SITE_URL}/{u}"
    priority = "1.0" if u == "" else ("0.8" if "services.html" in u or "case-studies.html" in u else "0.6")
    sitemap_entries.append(f"  <url>\n    <loc>{loc}</loc>\n    <lastmod>{today}</lastmod>\n    <changefreq>monthly</changefreq>\n    <priority>{priority}</priority>\n  </url>")
sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "\n".join(sitemap_entries) + "\n</urlset>\n"
write("sitemap.xml", sitemap)

robots = f"""User-agent: *
Allow: /

Sitemap: {SITE_URL}/sitemap.xml
"""
write("robots.txt", robots)

print("\nDone. Pages + sitemap + robots built.")
