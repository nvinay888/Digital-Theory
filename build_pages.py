#!/usr/bin/env python3
"""Generate inner pages for the Digitaltheory site from data."""
import os, json

ROOT = os.path.dirname(os.path.abspath(__file__))
SITE_URL = "https://digitaltheory.in"   # change to your production domain

def page(title, desc, body, base="", active="", path=""):
    full_title = f"{title} — Digitaltheory"
    canonical = f"{SITE_URL}/{path.lstrip('/')}" if path else SITE_URL + "/"
    og_image = f"{SITE_URL}/assets/og-image.png"
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
        <h3>Challenges</h3>
        <ul>{challenges_html}</ul>
      </div>
      <div class="case-detail__panel">
        <h3>Strategy &amp; execution</h3>
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
    cards = ''
    for c in CASES:
        m = c["metrics"]
        cards += f'''
        <a class="case" href="case-studies/{c["slug"]}.html">
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
    <div class="cases-grid">{cards}</div>
  </div>
</section>

{CTA_BAND.format(base='')}
"""
    return page("Case studies", "Digitaltheory case studies across D2C, BPC, edtech, consumer apps, gaming and retail digital transformation. Real numbers from real engagements.", body, base="", active="cases", path="case-studies.html")

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
        "slug":"digital-transformation","title":"Digital Transformation",
        "hero":"ERP integration, inventory automation, predictive analytics and ML — for measurable margin impact.",
        "intro":"For brick-and-mortar and omnichannel businesses, the next 10% of margin lives in operations, not ads. We digitise inventory, returns, fulfilment and store-level decision-making — and prove it on the P&amp;L.",
        "what":["ERP &amp; OMS integration","Inventory management automation","Returns &amp; reverse logistics dashboards","Predictive analytics &amp; ML","Store operations digitisation"],
        "deliverables":[
            ("Process audit","Map your data, decisions and handoffs — and where they leak time and money."),
            ("Software builds","Custom tools and integrations that sit on top of your existing ERP."),
            ("ML models","Demand forecasting, returns prediction and store-fit scoring."),
            ("Change management","Training, dashboards and ops cadence so the system actually gets used."),
        ],
        "case":"thulasi","case_label":"Thulasi — 33% inventory cost reduction, 37% returns reduction.",
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
    deliverables_html = ''.join(f'<div class="deliverable"><h4>{n}</h4><p>{d}</p></div>' for n,d in s["deliverables"])
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
    method_html = "".join(f'<div class="bc-step"><div class="bc-step__num">{n}</div><h4>{t}</h4><p>{d}</p></div>' for n,t,d in method)
    principles = [
        ("Operators first","Every recommendation comes from someone who has shipped it before — not a framework borrowed from a textbook."),
        ("Numbers, not narratives","If a strategy can&rsquo;t be measured on the P&amp;L, it isn&rsquo;t one. Every workstream owns a metric."),
        ("Skin in the outcome","Engagements are scoped around the result, not the hours. We win when you do — that&rsquo;s the only deal worth having."),
    ]
    principles_html = "".join(f'<div class="bc-principle"><h4>{t}</h4><p>{d}</p></div>' for t,d in principles)

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
        <h4>What we&rsquo;ve shipped</h4>
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
    <div class="services-grid">{cards}</div>
  </div>
</section>

{CTA_BAND.format(base='')}
"""
    return page("Services", "All Digitaltheory services — performance marketing, branding, web development, app development, business consulting, video production, SEO, digital transformation, and CRM & retention.", body, base="", active="services", path="services.html")

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
    return page("Our Work", "Digitaltheory's portfolio across D2C, beauty, edtech, consumer apps, gaming, retail and fintech — filter by industry to see relevant engagements.", body, base="", active="work", path="our-work.html")

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
<section class="section"><div class="container"><div class="services-grid">{cards}</div></div></section>
{CTA_BAND.format(base='')}
"""
    return page("Industries", "Digitaltheory industry expertise across D2C, beauty, edtech, consumer apps, gaming, retail, fintech and B2B SaaS.", body, base="", active="", path="industries.html")

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
      <a class="service" href="services/digital-transformation.html"><span class="service__index">06</span><h3 class="service__title">Digital Transformation</h3><p class="service__body">ERP, inventory, returns and ML for measurable margin impact.</p></a>
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
    return page("About", "Digitaltheory is a data-first growth marketing company helping brands turn theory into durable growth across performance, branding, web, app, and CRM.", body, base="", active="about", path="about.html")

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
    return page("Careers", "Open roles at Digitaltheory across performance marketing, creative, engineering, data and CRM. Work on real brands with real budgets.", body, base="", active="careers", path="careers.html")

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
            <option>SEO</option><option>Digital Transformation</option><option>CRM &amp; Retention</option><option>Not sure yet</option>
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
    return page("Contact", "Contact Digitaltheory — offices in Bengaluru and Mumbai. Performance marketing, branding, web, app, CRM and digital transformation.", body, base="", active="contact", path="contact.html")

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
    write(path, page(f"{c['brand']} case study", f"{c['brand']} ({c['industry']}) — case study by Digitaltheory. {c['hero']}", body, base="../", active="cases", path=path))

write("case-studies.html", build_cases_hub())

# Services
for s in SERVICES:
    body = render_business_consulting_body() if s["slug"] == "business-consulting" else render_service_body(s)
    path = f"services/{s['slug']}.html"
    desc = "Strategy, growth, unit economics, market entry, NPD, M&A diligence — consulting that ships, not just advises." if s["slug"] == "business-consulting" else f"{s['title']} services by Digitaltheory. {s['hero']}"
    write(path, page(s["title"], desc, body, base="../", active="services", path=path))

write("services.html", build_services_hub())
write("our-work.html", build_our_work())

# Industry pages
for ind in INDUSTRIES:
    ipath = f"industries/{ind['slug']}.html"
    write(ipath, page(f"{ind['title']} Growth Marketing", ind["lead"], render_industry_body(ind), base="../", active="", path=ipath))
write("industries.html", build_industries_hub())

write("about.html", build_about())
write("careers.html", build_careers())
write("contact.html", build_contact())

# ====================== SITEMAP & ROBOTS ======================
urls = ["", "services.html", "our-work.html", "case-studies.html", "industries.html", "about.html", "careers.html", "contact.html"]
urls += [f"services/{s['slug']}.html" for s in SERVICES]
urls += [f"case-studies/{c['slug']}.html" for c in CASES]
urls += [f"industries/{i['slug']}.html" for i in INDUSTRIES]

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
