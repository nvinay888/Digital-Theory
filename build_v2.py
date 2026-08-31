#!/usr/bin/env python3
"""Digital Theory V2 — repositioning site generator.
Service pages follow the classic catalog format: what we offer, offerings grid,
deliverables, process, FAQ, related services, CTA. Market-argument content lives
on the homepage and pricing page, not on service pages.
"""
import os, json

ROOT = os.path.dirname(os.path.abspath(__file__))
SITE_URL = "https://digitaltheory.co.in"

# ---------------------------------------------------------------- helpers
def page(title, desc, body, active="", path="", seo_title=None, extra_schema=None, breadcrumbs=None):
    full_title = seo_title if seo_title else f"{title} — Digital Theory"
    canonical = f"{SITE_URL}/{path.lstrip('/')}" if path else SITE_URL + "/"
    og_image = f"{SITE_URL}/assets/og-image.png"
    if breadcrumbs is None:
        crumbs = [("Home", "")]
        if path and path not in ("", "index.html"):
            crumbs.append((title, path))
        breadcrumbs = crumbs
    bc_items = []
    for i, (name, p) in enumerate(breadcrumbs, 1):
        item_url = SITE_URL + "/" if p == "" else f"{SITE_URL}/{p.lstrip('/')}"
        bc_items.append({"@type":"ListItem","position":i,"name":name,"item":item_url})
    schema_blocks = [json.dumps({"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":bc_items}, ensure_ascii=False)]
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
<meta property="og:site_name" content="Digital Theory" />
<meta property="og:title" content="{full_title}" />
<meta property="og:description" content="{desc}" />
<meta property="og:url" content="{canonical}" />
<meta property="og:image" content="{og_image}" />
<meta name="twitter:card" content="summary_large_image" />
<meta name="twitter:title" content="{full_title}" />
<meta name="twitter:description" content="{desc}" />
<meta name="twitter:image" content="{og_image}" />
<meta name="theme-color" content="#000000" />
<link rel="icon" href="assets/favicon.svg" type="image/svg+xml" />
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link href="https://fonts.googleapis.com/css2?family=Archivo:wght@400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet" />
<link rel="stylesheet" href="assets/styles.css" />
<script>window.DT_BASE = ''; window.DT_PAGE = '{active}';</script>
{schema_html}
</head>
<body>
<div class="page">
<div id="dt-nav"></div>
{body}
<div id="dt-footer"></div>
</div>
<script src="assets/shared.js"></script>
</body>
</html>
"""

def render_faq(items, section_title="Frequently asked questions", eyebrow="FAQ"):
    import re as _re
    def to_text(s): return _re.sub(r'\s+',' ',_re.sub(r'<[^>]+>','',s)).strip()
    faq_items = "\n".join(f'<details><summary>{q}</summary><div class="faq__answer">{a}</div></details>' for q,a in items)
    html = f'''
<section class="section" style="background:var(--surface-section);border-top:1px solid var(--line)" id="faq">
  <div class="container">
    <div class="sec-head" style="justify-content:center;text-align:center">
      <div style="margin:0 auto"><span class="eyebrow" style="justify-content:center">{eyebrow}</span><h2 style="margin-top:12px">{section_title}</h2></div>
    </div>
    <div class="faq">{faq_items}</div>
  </div>
</section>'''
    schema = {"@context":"https://schema.org","@type":"FAQPage",
              "mainEntity":[{"@type":"Question","name":to_text(q),"acceptedAnswer":{"@type":"Answer","text":to_text(a)}} for q,a in items]}
    return html, schema

CTA = '''
<section class="section cta-final">
  <div class="container container--narrow">
    <span class="eyebrow">Start here</span>
    <h2>Two hours will tell you more than <span class="accent">a quarter of pilots.</span></h2>
    <p class="lead">Bring the people who own revenue, operations and data. Leave with a written baseline and three costed agents, ranked by payback — whatever you decide next.</p>
    <div class="cta-final__row">
      <a href="audit.html" class="btn btn--primary btn--lg">Book the 2-hour Growth Audit <span class="btn__arrow">→</span></a>
      <a href="pricing.html" class="btn btn--secondary btn--lg">See how we charge</a>
    </div>
    <p class="geo-strip" style="text-align:center">₹75,000 · credited in full against any engagement signed within 30 days</p>
  </div>
</section>'''

SERVICES_META = {
    "revenue-services": ("Revenue Services","AI growth agents deployed into your revenue engine — demand, GEO, lifecycle, service and RevOps — priced on the number they move."),
    "strategy": ("Strategy & Intelligence","Growth strategy, AI transformation roadmaps and Market Research as a Service — decision-grade insight in five business days."),
    "brand": ("Brand & Influence","Brand strategy, AI influencer marketing, social, founder branding, content and entity engineering — instrumented and priced on citation share."),
    "implementation": ("Implementation & Systems","AI agent implementation plus SAP Business One, Odoo, Salesforce and SFMC — fixed fee, with fee at risk."),
    "engineering": ("Product & Platform Engineering","Web, mobile and AI-native product builds with a publicly auditable Core Web Vitals SLA and conversion-linked pricing."),
}
RELATED = {
    "revenue-services": ["strategy","brand","implementation"],
    "strategy": ["revenue-services","implementation","brand"],
    "brand": ["revenue-services","strategy","engineering"],
    "implementation": ["revenue-services","engineering","strategy"],
    "engineering": ["implementation","revenue-services","brand"],
}
def related_html(slug):
    cards = "".join(
        f'<a class="service" href="{r}.html"><span class="service__index">→</span><h3 class="service__title">{SERVICES_META[r][0]}</h3><p class="service__body">{SERVICES_META[r][1]}</p></a>'
        for r in RELATED[slug])
    return f'''
<section class="section" style="background:var(--surface-section);border-top:1px solid var(--line)">
  <div class="container">
    <div class="sec-head"><div><span class="eyebrow">Related services</span><h2>Pairs well with</h2></div><p class="lead">Most engagements combine two or three of these into one operating system.</p></div>
    <div class="services-grid">{cards}</div>
  </div>
</section>'''

def svc_schema(name, desc, path):
    return {"@context":"https://schema.org","@type":"Service","name":name,"description":desc,
            "provider":{"@type":"Organization","name":"Digital Theory","url":SITE_URL+"/"},
            "areaServed":[{"@type":"Country","name":"India"},{"@type":"Country","name":"United States"},{"@type":"Country","name":"United Arab Emirates"}],
            "serviceType":name,"url":f"{SITE_URL}/{path}"}

def offering_card(tag, title, desc, note=None):
    n = f'<div class="src">{note}</div>' if note else ''
    return f'<div class="svc-rich__card" style="cursor:default"><div class="svc-rich__body" style="padding-top:28px"><span class="svc-rich__num">{tag}</span><h3 class="svc-rich__title">{title}</h3><p class="svc-rich__desc">{desc}</p>{n}</div></div>'

def deliverables_html(items):
    return '<div class="solution__deliverables">' + "".join(f'<div class="deliverable"><h3>{n}</h3><p>{d}</p></div>' for n,d in items) + '</div>'

def service_hero(eyebrow, h1, lead):
    return f'''
<section class="page-hero">
  <div class="container page-hero__inner">
    <span class="eyebrow">{eyebrow}</span>
    <h1>{h1}</h1>
    <p class="lead page-hero__lead">{lead}</p>
    <div class="page-hero__cta">
      <a href="audit.html" class="btn btn--primary btn--lg">Book the 2-hour Growth Audit <span class="btn__arrow">→</span></a>
      <a href="pricing.html" class="btn btn--secondary btn--lg">How we charge</a>
    </div>
  </div>
</section>'''

def what_we_do(h2, intro, scope, panel_title, panel_items):
    scope_html = "".join(f"<li>{s}</li>" for s in scope)
    panel_html = "".join(f'<li style="padding-left:24px;position:relative;color:var(--fg);font-size:14.5px;line-height:1.55;list-style:none"><span style="position:absolute;left:0;color:var(--lime-400);font-weight:700">→</span> {p}</li>' for p in panel_items)
    return f'''
<section class="section">
  <div class="container">
    <div class="solution__intro">
      <div class="solution__what">
        <span class="eyebrow">What we do</span>
        <h2 style="margin-top:12px;max-width:20ch">{h2}</h2>
        <p class="lead" style="margin-top:16px">{intro}</p>
        <ul>{scope_html}</ul>
      </div>
      <div>
        <div class="case-detail__panel">
          <h3>{panel_title}</h3>
          <ul style="border:0;padding:0;margin:0;display:flex;flex-direction:column;gap:12px">{panel_html}</ul>
        </div>
      </div>
    </div>
  </div>
</section>'''

def write(path, content):
    with open(os.path.join(ROOT, path),"w") as f: f.write(content)
    print("wrote", path)

# ================================================================ REVENUE SERVICES
def build_revenue():
    offerings = "".join([
        offering_card("Demand","Pipeline agents","ICP scoring against your closed-won data, signal-triggered outbound, meeting qualification and routing — writing to your CRM, not a spreadsheet.","Priced per qualified meeting held"),
        offering_card("Search","AI SEO &amp; GEO","Getting your brand cited by ChatGPT, Perplexity, Gemini and Google AI Overviews — schema, entity work, citation-optimised content and earned-media placement.","Guarantee: citation share moves by month four, or month four is free"),
        offering_card("Creators","Creator-led acquisition","Influencer run as an acquisition channel — creators matched on conversion history, fraud-screened before signing, priced per customer produced.","Run with the Brand &amp; Influence practice"),
        offering_card("Lifecycle","Retention agents","Churn prediction on behaviour, next-best-action per segment, triggered against your billing and support systems across email, WhatsApp, push and in-app.","Priced against retained revenue"),
        offering_card("Service","Resolution agents","Support deflection grounded in your knowledge base and order system. Escalation is free; you only pay for a clean resolution.","₹95–₹190 per resolution vs ₹500–₹1,100 human-handled"),
        offering_card("RevOps","Operating agents","Quote-to-cash, collections follow-up, margin-leakage detection and forecast hygiene — the back-office work where ROI is highest and nobody looks.","Priced per recovered rupee or fixed + kicker"),
    ])
    delivs = deliverables_html([
        ("Value Baseline Memo","Your current-state numbers — agreed, signed and locked before anything is built. Every outcome fee is measured against it."),
        ("Growth Engine Blueprint","Which agents, reading which systems, producing which measurable outcome, in what order — with the commercial terms attached to each."),
        ("Agents in production","Built inside your stack — ERP, CRM, warehouse, ticketing — with a named owner and binary success criteria. First agent live in 30 days."),
        ("Eval suite you own","An OpenTelemetry-instrumented evaluation suite that lives in your stack and stays with you whether or not we do."),
        ("The Growth Graph","Your org-level context layer — every outcome, correction and edge case written back, so agents get cheaper per outcome each quarter."),
        ("Quarterly certification","A shared dashboard, holdout-based measurement and finance sign-off before any outcome invoice is raised."),
    ])
    steps = '''
    <div class="bc-method">
      <div class="bc-step"><div class="bc-step__num">01</div><div style="font-family:var(--font-mono);font-size:12px;letter-spacing:.1em;color:var(--lime-400);margin-bottom:10px">2 HOURS</div><h3>Audit</h3><p>Your leadership in the room. We trace the revenue path end to end and agree the baseline.</p></div>
      <div class="bc-step"><div class="bc-step__num">02</div><div style="font-family:var(--font-mono);font-size:12px;letter-spacing:.1em;color:var(--lime-400);margin-bottom:10px">5 DAYS</div><h3>Blueprint</h3><p>Agent architecture, integration map, eval criteria and the costed outcome contract.</p></div>
      <div class="bc-step"><div class="bc-step__num">03</div><div style="font-family:var(--font-mono);font-size:12px;letter-spacing:.1em;color:var(--lime-400);margin-bottom:10px">30 DAYS</div><h3>Deploy</h3><p>Forward-deployed engineers build inside your stack. One workflow, binary success criteria, a named owner.</p></div>
      <div class="bc-step"><div class="bc-step__num">04</div><div style="font-family:var(--font-mono);font-size:12px;letter-spacing:.1em;color:var(--lime-400);margin-bottom:10px">∞ ONGOING</div><h3>Compound</h3><p>Every result feeds the Growth Graph. Cost per outcome falls quarter over quarter; our fee tracks the curve.</p></div>
    </div>'''
    faq_html, faq_schema = render_faq([
        ("What kinds of agents do you deploy?","<p>Six lines: pipeline agents (demand), AI SEO/GEO, creator-led acquisition, lifecycle and retention agents, support resolution agents, and RevOps operating agents — each reading and writing to your actual systems, not a spreadsheet.</p>"),
        ("How are Revenue Services priced?","<p>On outcomes. Depending on the line: per qualified meeting held, per clean resolution, per recovered rupee, or a base fee with a quarterly kicker against the agreed KPI — always with a floor, a cap and a baseline locked at signature. The five contract tiers are published on our pricing page.</p>"),
        ("How fast is the first agent live?","<p>Thirty days from blueprint sign-off. Deploy is deliberately narrow — one workflow, binary success criteria, a named owner on your side — because scope, not model capability, is what kills these projects.</p>"),
        ("Which systems do the agents connect to?","<p>SAP Business One, Odoo, Salesforce and SFMC natively — plus your warehouse, ticketing, billing and analytics stack through APIs. Systems-of-record access is the difference between an agent and a chatbot.</p>"),
        ("What do we keep if we stop working with you?","<p>Everything: the agents, the eval suite, the Growth Graph and the documentation. Built in your cloud, governed under your policy, portable if you leave.</p>"),
    ], section_title="Questions about Revenue Services")
    body = service_hero("Services · Revenue Services",
        'AI growth agents, <span class="accent">priced on the number they move.</span>',
        "We build and run AI agents inside your revenue engine — demand generation, AI SEO/GEO, creator-led acquisition, lifecycle, service and RevOps — reading your CRM and margin data, with our fee tied to outcomes.")
    body += what_we_do("A complete revenue-agent stack, under one roof.",
        "Six agent lines, deployed in the order your payback ranks them — each one reading and writing to your systems of record.",
        ["Demand generation &amp; pipeline agents","AI SEO &amp; GEO (generative engine optimisation)","Creator-led acquisition","Lifecycle &amp; retention agents","Support resolution agents","RevOps &amp; operating agents"],
        "How it&rsquo;s priced",
        ["Outcome contracts with a locked baseline, floor and cap","Per meeting, per resolution, per recovered rupee — or base + kicker","Randomised 10% holdout, never last-touch attribution","Quarterly certification with your finance team&rsquo;s sign-off"])
    body += f'''
<section class="section" style="background:var(--surface-section);border-block:1px solid var(--line)">
  <div class="container">
    <div class="sec-head"><div><span class="eyebrow">The offerings</span><h2 style="max-width:22ch">Agents that touch revenue, not slideware.</h2></div></div>
    <div class="svc-rich">{offerings}</div>
  </div>
</section>
<section class="section">
  <div class="container">
    <div class="sec-head"><div><span class="eyebrow">Deliverables</span><h2>What you walk away with</h2></div><p class="lead">Working systems and signed baselines — not decks.</p></div>
    {delivs}
  </div>
</section>
<section class="section" style="background:var(--surface-section);border-block:1px solid var(--line)">
  <div class="container">
    <div class="sec-head"><div><span class="eyebrow">How it runs</span><h2>Audit. Blueprint. Deploy. Compound.</h2></div><p class="lead">A clock on every stage — 2 hours, 5 days, 30 days, then compounding.</p></div>
    {steps}
  </div>
</section>
{related_html("revenue-services")}
{faq_html}
{CTA}'''
    schema = svc_schema("Revenue Services", SERVICES_META["revenue-services"][1], "revenue-services.html")
    return page("Revenue Services",
        "AI growth agents deployed into your revenue engine — demand gen, AI SEO/GEO, creator-led acquisition, lifecycle, service and RevOps — priced on outcomes.",
        body, active="practices", path="revenue-services.html",
        seo_title="Revenue Services — Outcome-Priced AI Agents | Digital Theory",
        extra_schema=[schema, faq_schema])

# ================================================================ STRATEGY
def build_strategy():
    offerings = "".join([
        offering_card("01","AI &amp; Growth Strategy","Where AI actually changes your P&amp;L, sequenced by payback rather than by fashion. Which functions, which agents, which order, and what each is worth — against your own baseline.","From ₹2.5L"),
        offering_card("02","Market Research as a Service","Category sizing, buyer research, pricing studies, concept tests, win/loss and competitive intelligence — AI-moderated at scale, human-validated on a stratified subsample.","Subscription or per study · 5-day turnaround"),
        offering_card("03","India Mid-Market Benchmark Index","Longitudinal norms for mid-market operating metrics. &ldquo;Your repeat-purchase rate is 0.6× the median for your category&rdquo; is a sentence that starts a project.","Proprietary"),
        offering_card("04","Transformation Roadmap","The operating model, the org design, the data foundations and the sequencing — with 25% of the fee contingent on the recommendation being live within two quarters.","6–8 weeks"),
    ])
    delivs = deliverables_html([
        ("Strategy memo &amp; model","A short, sharp memo with the decisions and the reasoning — plus a working financial model that is yours to keep and edit."),
        ("Research report with error bands","Every synthetic finding validated against a stratified human subsample, with the observed error band disclosed in the deliverable — contractually."),
        ("Prioritised agent roadmap","Use cases ranked by payback, each with the data it needs and the number it should move."),
        ("Quarterly operating rhythm","Reviews tied to the model, so decisions update with reality instead of lagging it."),
    ])
    faq_html, faq_schema = render_faq([
        ("What does Strategy &amp; Intelligence cover?","<p>Four offerings: AI &amp; growth strategy, Market Research as a Service, the India Mid-Market Benchmark Index, and full transformation roadmaps — all delivered against your own baseline rather than a benchmark deck.</p>"),
        ("How fast is Market Research as a Service?","<p>Decision-grade insight in five business days, or the fee is waived — written into the engagement letter. Interviews are AI-moderated at scale in 50+ languages, then human-validated on a stratified subsample.</p>"),
        ("How is consulting priced?","<p>AI &amp; growth strategy starts at ₹2.5L. Research runs on subscription or per study. On roadmaps, 25% of the fee is tied to the recommendation actually being live within two quarters.</p>"),
        ("How do you handle synthetic research accuracy?","<p>We publish where the method breaks: safe for ranking and prioritisation, unsafe for magnitude, significance and segment variance. Every synthetic finding is human-validated and the error band is disclosed in the report.</p>"),
        ("What makes this different from a big consultancy?","<p>Cost structure, not IQ. We have no $700-an-hour blended rate or associate pyramid to protect — so the same rigour lands in days, at a fraction of the price, with fee tied to the outcome.</p>"),
    ], section_title="Questions about Strategy &amp; Intelligence")
    body = service_hero("Services · Strategy &amp; Intelligence",
        'Decision-grade answers in <span class="accent">five business days.</span>',
        "Growth strategy, AI transformation roadmaps and Market Research as a Service — the rigour of a tier-one firm at a fraction of the clock, with part of the fee tied to the recommendation landing.")
    body += what_we_do("Strategy that ships, research that answers.",
        "Four offerings, all measured, all fast — built for leadership teams that need an answer this quarter, not next year.",
        ["AI &amp; growth strategy","Market Research as a Service","Pricing &amp; unit-economics studies","Win/loss &amp; competitive intelligence","India Mid-Market Benchmark Index","Transformation roadmaps"],
        "Standards we work to",
        ["5-day decision-grade turnaround, or the fee is waived","25% of roadmap fees tied to the recommendation landing","Synthetic findings human-validated, error bands disclosed","Delivered against your baseline, not a benchmark deck"])
    body += f'''
<section class="section" style="background:var(--surface-section);border-block:1px solid var(--line)">
  <div class="container">
    <div class="sec-head"><div><span class="eyebrow">The offerings</span><h2>Four ways in.</h2></div></div>
    <div class="svc-rich" style="grid-template-columns:repeat(2,1fr)">{offerings}</div>
  </div>
</section>
<section class="section">
  <div class="container">
    <div class="sec-head"><div><span class="eyebrow">Market Research as a Service</span><h2 style="max-width:22ch">Traditional timelines, collapsed.</h2></div></div>
    <div class="dt-table-wrap"><table class="dt-table">
      <tr><th>Method</th><th>Traditional cost</th><th>Traditional timeline</th><th>With us</th></tr>
      <tr><td>20 in-depth interviews</td><td>$15,000 – $30,000</td><td>4–8 weeks</td><td><strong>Days, at a fraction of the cost</strong></td></tr>
      <tr><td>4–6 focus groups</td><td>$24,000 – $90,000</td><td>4–8 weeks</td><td><strong>Under a week</strong></td></tr>
      <tr><td>Five-market study</td><td>$75,000 – $225,000</td><td>8–12 weeks</td><td><strong>50+ languages, one cost base</strong></td></tr>
      <tr><td>Analysis phase alone</td><td>Included</td><td>~4 weeks</td><td><strong>Hours</strong></td></tr>
    </table></div>
  </div>
</section>
<section class="section" style="background:var(--surface-section);border-block:1px solid var(--line)">
  <div class="container">
    <div class="sec-head"><div><span class="eyebrow">Deliverables</span><h2>What you walk away with</h2></div></div>
    {delivs}
  </div>
</section>
{related_html("strategy")}
{faq_html}
{CTA}'''
    schema = svc_schema("Strategy & Intelligence", SERVICES_META["strategy"][1], "strategy.html")
    return page("Strategy & Intelligence",
        "Growth strategy, AI roadmaps and Market Research as a Service — decision-grade insight in 5 business days, with 25% of the fee tied to the outcome.",
        body, active="practices", path="strategy.html",
        seo_title="Strategy & Intelligence — Research in 5 Days | Digital Theory",
        extra_schema=[schema, faq_schema])

# ================================================================ BRAND
def build_brand():
    offerings = "".join([
        offering_card("01","Brand strategy &amp; positioning","The category you intend to own, the buyer you intend to move, and the words that do it — written to be repeated by a salesperson, a journalist and a language model."),
        offering_card("02","AI Influencer Marketing","Creator matching on conversion history rather than follower count, fraud screening before you sign, and ASCI-compliant disclosure generated into every brief — indemnified in writing."),
        offering_card("03","Social media marketing","Always-on social run by agents against a brief you approve — planning, production, community response and reporting — with a human editor on every post that carries a claim."),
        offering_card("04","Personal &amp; founder-led branding","A governed voice model built from your own writing — never a generic ghostwriter — with you signing off on everything. Point of view, cadence, platform strategy, podcast and press placement."),
        offering_card("05","Content strategy &amp; editorial","Built to be cited, not just read — written to a scored standard derived from peer-reviewed research on what earns AI citations: sources, statistics, quotations."),
        offering_card("06","Entity &amp; mention engineering","Schema, knowledge panels, review profiles and consistent naming — making every machine that reads about you resolve it to the same entity. Feeds the GEO work in Revenue Services."),
    ])
    delivs = deliverables_html([
        ("Positioning &amp; messaging house","Category narrative, messaging pillars and tone of voice — usable by sales, PR and content from day one."),
        ("Citation baseline &amp; tracking","Your share of citation in your category across ChatGPT, Perplexity, Gemini and Google AI Overviews — measured before we start, tracked monthly."),
        ("Creator program with compliance","Matched creators, fraud-screened, with ASCI dual-disclosure compliance generated into every brief and indemnified."),
        ("Founder voice model","Trained on your actual writing, governed by your sign-off — with a publishing cadence across LinkedIn, newsletter and press."),
        ("Content standard &amp; calendar","A scored editorial standard plus the monthly calendar that ships against it."),
        ("Entity layer","Schema, profiles and naming consistency across the surfaces machines actually read."),
    ])
    faq_html, faq_schema = render_faq([
        ("What does Brand &amp; Influence include?","<p>Six services run as one system: brand strategy and positioning, AI influencer marketing, social media marketing, personal and founder-led branding, content strategy and editorial, and entity and mention engineering.</p>"),
        ("How can brand work be priced on outcomes?","<p>Because citation share is countable. We measure your share of citation in your category across ChatGPT, Perplexity, Gemini and Google AI Overviews against a baseline agreed before we start — with a guarantee that it moves by month four, or month four is free.</p>"),
        ("How does the influencer offering work?","<p>Creators are matched on conversion history rather than reach, fraud-screened before contract, and every brief ships with ASCI-compliant dual disclosure that we indemnify. Work is priced per qualified customer, with a monthly floor and cap.</p>"),
        ("Do you replace our in-house social team?","<p>No. Two-thirds of brands run social in-house and are right to. We provide the system, the standard and the measurement layer — your team keeps the wheel wherever that works better.</p>"),
        ("Is a founder&rsquo;s content ghostwritten?","<p>It is written from a governed voice model built on your own writing — never a generic ghostwriter — and nothing publishes without your sign-off.</p>"),
    ], section_title="Questions about Brand &amp; Influence")
    body = service_hero("Services · Brand &amp; Influence",
        'Brand, influence and content — <span class="accent">run as one instrumented system.</span>',
        "Brand strategy, AI influencer marketing, social, founder-led branding, content and entity engineering — measured on citation share, the number machines now read when they decide who gets recommended.")
    body += what_we_do("Six services, one system.",
        "Everything a brand team buys — strategy, creators, social, founder content, editorial and entity work — wired together and measured where it now counts.",
        ["Brand strategy &amp; positioning","AI influencer marketing","Social media marketing","Personal &amp; founder-led branding","Content strategy &amp; editorial","Entity &amp; mention engineering"],
        "How it&rsquo;s priced",
        ["Citation share as the outcome, baseline agreed up front","Guarantee: citation share moves by month four, or month four is free","Influencer priced per qualified customer, with floor and cap","Verifiable with tools you can buy yourself — never just our word"])
    body += f'''
<section class="section" style="background:var(--surface-section);border-block:1px solid var(--line)">
  <div class="container">
    <div class="sec-head"><div><span class="eyebrow">The offerings</span><h2>What&rsquo;s in the system.</h2></div></div>
    <div class="svc-rich">{offerings}</div>
  </div>
</section>
<section class="section">
  <div class="container">
    <div class="sec-head"><div><span class="eyebrow">Deliverables</span><h2>What you walk away with</h2></div></div>
    {delivs}
  </div>
</section>
<section class="section" style="background:var(--surface-section);border-block:1px solid var(--line)">
  <div class="container">
    <div class="sec-head"><div><span class="eyebrow">Fit</span><h2 style="max-width:24ch">Where we&rsquo;ll recommend against ourselves.</h2></div></div>
    <div class="fact-rows" style="grid-template-columns:repeat(3,1fr)">
      <div class="fact"><h3>AI influencers</h3><p>Right for gaming, electronics and fashion-forward. Wrong for health, financial services and anything where trust is the product — human creators outperform virtual by up to 2.7× in authenticity-driven categories.</p></div>
      <div class="fact"><h3>In-house social</h3><p>If your team runs social well, keep it in-house. We supply the system, standard and measurement layer rather than taking the job.</p></div>
      <div class="fact"><h3>Timeframes</h3><p>Citation share moves in months, not weeks. We show leading indicators monthly and will not pretend a quarter is a verdict.</p></div>
    </div>
  </div>
</section>
{related_html("brand")}
{faq_html}
{CTA}'''
    schema = svc_schema("Brand & Influence", SERVICES_META["brand"][1], "brand.html")
    return page("Brand & Influence",
        "Brand strategy, AI influencer marketing, social, founder branding, content and entity engineering — one instrumented system, priced on citation share.",
        body, active="practices", path="brand.html",
        seo_title="Brand & Influence — Brand, Priced on Outcomes | Digital Theory",
        extra_schema=[schema, faq_schema])

# ================================================================ IMPLEMENTATION
def build_implementation():
    offerings = "".join([
        offering_card("Agents","AI agent implementation","Custom agents built into your workflows — order-to-cash, support triage, finance ops — from a countable, versioned, evaluated library, each with a published eval suite."),
        offering_card("ERP","SAP Business One &amp; Odoo","Implementation, migration, localisation and AMC — plus the agent layer on top. Configured to how you actually run, phased by module so value lands early."),
        offering_card("CRM","Salesforce &amp; SFMC","Implementation, migration and consolidation, with agents wired into the objects that matter rather than a chatbot on the homepage."),
        offering_card("Data","Warehouse &amp; integration","Pipelines, identity resolution and the semantic model that makes agent answers correct instead of plausible."),
        offering_card("Governance","Evals, observability &amp; DPDP","Traces, token accounting, failure clustering, audit logs, RBAC and consent-compatible processing — designed for May 2027 enforcement, built now."),
        offering_card("Rescue","Project rescue","A stalled or failing implementation audited, stabilised and brought to an adopted state — with the same contracted delivery standards as a fresh build."),
    ])
    delivs = deliverables_html([
        ("Pre-Mortem Scorecard","Before we quote, a scored diagnostic on the things that sink these projects — sponsorship, data readiness, change capacity, measurable value. Below threshold, we tell you what to fix first."),
        ("Implementation blueprint","Architecture, integration map, migration plan and a phased sequence with binary success criteria per phase."),
        ("Working systems","ERP, CRM or agents live in production — one workflow at a time, each with a named owner on your side."),
        ("Eval harness you own","OpenTelemetry-instrumented evaluations living in your stack — offline pre-deploy, online in production, every failure converted to a regression test."),
        ("Training &amp; SOPs","Role-based training and written procedures so adoption sticks after we leave."),
        ("Hyper-care &amp; AMC","Post-go-live support, upgrades and continuous improvement against your operating KPIs."),
    ])
    faq_html, faq_schema = render_faq([
        ("What do you implement?","<p>Custom AI agents, SAP Business One, Odoo, Salesforce and SFMC — plus the data and governance layer underneath: warehouse, integration, evals, observability and DPDP-ready processing.</p>"),
        ("How is implementation priced?","<p>Fixed fee, with a defined portion at risk against binary success criteria. Fixed scope is the direct countermeasure to the cost-and-scope failure modes that kill most agentic projects.</p>"),
        ("What is the Pre-Mortem Scorecard?","<p>A paid diagnostic that scores your project on executive sponsorship, data readiness, change capacity and measurable value before we quote. Below threshold, we decline the project and tell you what to fix first.</p>"),
        ("What are the three contracted delivery standards?","<p>A named agent owner on your side, automated evaluations on every change, and one workflow with binary success criteria — written into the statement of work as standards you can hold us to.</p>"),
        ("Do you take over projects other vendors started?","<p>Yes — project rescue is a standing offering. We audit the current build, identify what is salvageable, fix configuration and data issues, and bring the implementation to a stable, adopted state.</p>"),
    ], section_title="Questions about Implementation &amp; Systems")
    body = service_hero("Services · Implementation &amp; Systems",
        'Agents and systems of record, <span class="accent">delivered by one team.</span>',
        "AI agent implementation plus SAP Business One, Odoo, Salesforce and SFMC — scored before we quote, contracted to delivery standards, fixed fee with fee at risk.")
    body += what_we_do("From ERP to agents, one accountable team.",
        "The systems of record and the intelligence on top — because an agent that cannot see inventory, margin, credit or service history is guessing.",
        ["AI agent implementation","SAP Business One — implementation, migration, AMC","Odoo — implementation, customisation, integration","Salesforce &amp; SFMC — implementation and consolidation","Data warehouse &amp; systems integration","Evals, observability &amp; governance (DPDP-ready)"],
        "How we deliver",
        ["Pre-Mortem Scorecard before any quote","Fixed fee, with a defined portion at risk on miss","Three delivery standards written into the SOW","Forward-deployed engineers inside your systems"])
    body += f'''
<section class="section" style="background:var(--surface-section);border-block:1px solid var(--line)">
  <div class="container">
    <div class="sec-head"><div><span class="eyebrow">The offerings</span><h2>What we implement.</h2></div></div>
    <div class="svc-rich">{offerings}</div>
  </div>
</section>
<section class="section">
  <div class="container">
    <div class="sec-head"><div><span class="eyebrow">Deliverables</span><h2>What you walk away with</h2></div></div>
    {delivs}
  </div>
</section>
{related_html("implementation")}
{faq_html}
{CTA}'''
    schema = svc_schema("Implementation & Systems", SERVICES_META["implementation"][1], "implementation.html")
    return page("Implementation & Systems",
        "AI agents, SAP B1, Odoo, Salesforce & SFMC — a Pre-Mortem diagnostic, contracted delivery standards, an eval harness you keep, fixed fee with fee at risk.",
        body, active="practices", path="implementation.html",
        seo_title="Implementation & Systems — Agents + ERP/CRM | Digital Theory",
        extra_schema=[schema, faq_schema])

# ================================================================ ENGINEERING
def build_engineering():
    offerings = "".join([
        offering_card("Web","D2C storefronts &amp; web platforms","Shopify, Shopify Plus, Next.js headless and marketing sites — engineered around your AOV, attach-rate and repeat-rate goals, shipping fast by default."),
        offering_card("Mobile","Mobile app development","Native iOS/Android and React Native consumer apps — with ASO, in-app analytics and event-driven CRM designed in from day one."),
        offering_card("AI-native","AI-native product builds","Products with agents, retrieval and evals in the architecture from the start — not an AI feature bolted onto a CRUD app."),
        offering_card("CRO","Landing systems &amp; CRO","Reusable landing-page modules your marketing team can spin up per campaign in hours, plus a hypothesis-driven A/B testing cadence with documented uplift."),
        offering_card("Analytics","Analytics &amp; tracking","GA4, server-side events, CAPI and product analytics — wired so every channel sees the same number."),
        offering_card("Access","Accessibility &amp; compliance","WCAG conformance as a deliverable, not a preference — a legal requirement under the European Accessibility Act, and the one thing that cannot be vibe-coded."),
    ])
    delivs = deliverables_html([
        ("A site that passes, provably","All three Core Web Vitals at p75 on launch, or we fix it free — auditable by you on public Chrome UX Report data."),
        ("Citation-ready structure","Schema, entity markup, strict heading hierarchy and citation-optimised content structure ship by default. Built to be cited, not just ranked."),
        ("Reviewed, gated code","Human review and a static-analysis gate on every line of AI-generated code before it ships."),
        ("Analytics wired end-to-end","One measurement layer across web, ads and CRM, so conversion lift is measurable — and priceable."),
        ("Landing-page system","Reusable modules with a testing cadence, not one-off pages."),
        ("Documentation &amp; handover","Your repo, your cloud, your documentation — portable from day one."),
    ])
    faq_html, faq_schema = render_faq([
        ("What do you build?","<p>D2C storefronts and web platforms (Shopify, Next.js headless), native and cross-platform mobile apps, AI-native products, landing-page systems with CRO, and the analytics layer underneath.</p>"),
        ("What is the Core Web Vitals SLA?","<p>Every site we ship passes all three Core Web Vitals at p75 on launch, or we fix it free. The Chrome UX Report is public data, so you can verify the claim without trusting us.</p>"),
        ("How is engineering priced?","<p>A base build fee plus a share of measured conversion lift where the analytics support it — underwritten by published elasticities, not optimism. Fixed-fee builds are available where a lift share doesn&rsquo;t fit.</p>"),
        ("Do you use AI to write code?","<p>Yes, where it is faster — with human review and a static-analysis security gate on every line before it ships, because the published research on AI-generated code quality is not reassuring.</p>"),
        ("Do you handle small brochure sites?","<p>Honestly, no. That tier is collapsing to $20-a-month website builders, and we will tell you to use one. Our work starts where measured conversion and performance matter to revenue.</p>"),
    ], section_title="Questions about Product &amp; Platform Engineering")
    body = service_hero("Services · Product &amp; Platform Engineering",
        'Web, mobile and AI-native builds — <span class="accent">with a performance SLA you can audit.</span>',
        "D2C storefronts, mobile apps, AI-native products and landing systems. Every site ships passing all three Core Web Vitals at p75 or we fix it free — verifiable on public data.")
    body += what_we_do("Everything above the boilerplate line.",
        "Builds where speed, conversion and measurement are the point — engineered, instrumented and priced against the lift they produce.",
        ["D2C storefronts &amp; web platforms","Mobile app development (iOS, Android, React Native)","AI-native product builds","Landing-page systems &amp; CRO","Analytics &amp; tracking (GA4, server-side, CAPI)","Accessibility &amp; WCAG conformance"],
        "What we put in the contract",
        ["Core Web Vitals SLA at p75 — or we fix it free","Base fee + share of measured conversion lift","Human review + SAST gate on all AI-generated code","Citation-ready structure ships by default"])
    body += f'''
<section class="section" style="background:var(--surface-section);border-block:1px solid var(--line)">
  <div class="container">
    <div class="sec-head"><div><span class="eyebrow">The offerings</span><h2>What we build.</h2></div></div>
    <div class="svc-rich">{offerings}</div>
  </div>
</section>
<section class="section">
  <div class="container">
    <div class="sec-head"><div><span class="eyebrow">Deliverables</span><h2>What you walk away with</h2></div></div>
    {delivs}
  </div>
</section>
{related_html("engineering")}
{faq_html}
{CTA}'''
    schema = svc_schema("Product & Platform Engineering", SERVICES_META["engineering"][1], "engineering.html")
    return page("Product & Platform Engineering",
        "Web, mobile and AI-native builds with a Core Web Vitals SLA verifiable on public CrUX data, and pricing linked to measured conversion lift.",
        body, active="practices", path="engineering.html",
        seo_title="Product & Platform Engineering | Digital Theory",
        extra_schema=[schema, faq_schema])

# ================================================================ LABS
def build_labs():
    products = [
        ("Private beta","AI Influencer Marketing","Creator matching on conversion history rather than follower count, fraud screening before you sign, and ASCI-compliant disclosure generated into every brief.",
         ["66.3% of brands run influencer in-house — the gap is measurement, not execution","Fake followers are 56.5% of reported brand fraud concerns","Brands carry the ASCI liability; penalties reach ₹50 lakh"]),
        ("In build","AI SEO","Citation share across ChatGPT, Perplexity, Gemini and Google AI Overviews — plus the work that actually moves it. Tools measure. This one is built to change the number.",
         ["AI Overview citation overlap with the top 10 fell from 76% to 17–38%","Earned media produces 82% of all AI citations; owned and paid, 6%","ChatGPT and Perplexity overlap on only 11% of cited domains"]),
        ("In design","AI OS · Full Stack","The operating layer underneath everything else we ship — the Growth Graph, the agent runtime, the eval harness and the governance controls, packaged for a mid-market company to run itself.",
         ["OpenTelemetry-native, so your traces stay portable","Consent-compatible and auditable ahead of DPDP enforcement","Self-hostable, because data residency is a real constraint"]),
    ]
    prods_html = "".join(
        f'''<div class="tier"><span class="tier__label">{status}</span><div class="tier__price">{t}</div><p class="tier__desc">{d}</p>
        <ul style="list-style:none;margin:0;padding:0;display:flex;flex-direction:column;gap:10px">{"".join(f'<li style="padding-left:20px;position:relative;color:var(--fg-muted);font-size:13.5px;line-height:1.5"><span style="position:absolute;left:0;color:var(--lime-400)">→</span>{b}</li>' for b in bullets)}</ul></div>'''
        for status,t,d,bullets in products)
    body = f'''
<section class="page-hero">
  <div class="container page-hero__inner">
    <span class="eyebrow">Digital Theory Labs</span>
    <h1>We don&rsquo;t only deliver AI. <span class="accent">We build it.</span></h1>
    <p class="lead page-hero__lead">A productised AI portfolio for B2B and B2C. Every product in Labs started as a system we built for a client, proved on their P&amp;L, and then generalised. Nothing here is a concept deck.</p>
    <div class="page-hero__cta">
      <a href="audit.html" class="btn btn--primary btn--lg">Request early access <span class="btn__arrow">→</span></a>
      <a href="revenue-services.html" class="btn btn--secondary btn--lg">See the services side</a>
    </div>
  </div>
</section>
<section class="section">
  <div class="container">
    <div class="sec-head"><div><span class="eyebrow">The portfolio</span><h2>Three products in build.</h2></div></div>
    <div class="fact-rows" style="grid-template-columns:repeat(3,1fr)">{prods_html}</div>
  </div>
</section>
<section class="section" style="background:var(--surface-section);border-block:1px solid var(--line)">
  <div class="container">
    <div class="sec-head">
      <div><span class="eyebrow">Why a services firm builds products</span><h2 style="max-width:22ch">The services business is the research lab.</h2></div>
      <p class="lead">Most AI products are built by people guessing at a workflow. Ours are built by people who have already run that workflow inside a real business, under a contract where getting it wrong cost us money.</p>
    </div>
    <div class="fact-rows" style="grid-template-columns:repeat(3,1fr)">
      <div class="fact"><h3>Rule one</h3><p>Nothing enters Labs until it has produced a measured outcome on a client engagement.</p></div>
      <div class="fact"><h3>Rule two</h3><p>Every product ships with the eval suite it was built against. If we can&rsquo;t measure it, we can&rsquo;t sell it.</p></div>
      <div class="fact"><h3>Rule three</h3><p>Clients who helped prove a product get it at cost for the life of their engagement.</p></div>
    </div>
  </div>
</section>
{CTA}'''
    return page("Digital Theory Labs",
        "A productised AI portfolio — AI Influencer Marketing, AI SEO and AI OS Full-Stack. Every product proved on a client P&L before it ships.",
        body, active="labs", path="labs.html",
        seo_title="Digital Theory Labs — Productised AI | Digital Theory")

# ================================================================ PRICING
def build_pricing():
    cmp1_rows = [
        ("Reaches your systems","Reads and writes to SAP Business One, Odoo, Salesforce, your warehouse and your ticketing system.","No access to ERP, CRM, warehouse or ticketing. Every answer is ungrounded in what is true today."),
        ("Memory","Persistent, governed, org-level memory — the Growth Graph.","Session-scoped, per-user, non-transferable. Nothing the organisation learns is retained."),
        ("Accuracy on business tasks","Grounded retrieval cuts hallucination 30–70%; under 2% on grounded summarisation.","Legal-query hallucination measured at 58–88% (Stanford RegLab)."),
        ("Evaluation","Offline evals pre-deploy, online LLM-as-judge in production, every failure converted into a regression test.","None. No ground truth, no regression tests, no quality gate."),
        ("Observability","OpenTelemetry gen_ai.* spans — model calls, tokens, agent steps, tool executions.","No traces, no token accounting, no audit trail."),
        ("Governance","Policy, role-based access, audit log, human-in-the-loop and a model allow-list from day one.","52% of organisations have no formal policy on external AI tools."),
        ("Data exposure","Data stays inside the governed boundary — DLP, redaction and retention controls.","27% of employees have entered confidential company data into public AI tools."),
        ("DPDP readiness","Purpose-limited, consent-manager compatible, auditable — ahead of May 2027 enforcement, penalties to ₹250 Cr.","Consumer accounts sit outside consent management, retention limits and audit obligations."),
        ("Payback","Agreed in the blueprint before we build, then measured against the locked baseline every quarter.","Unmeasured — that is rather the point. There is no instrumentation to measure it with."),
    ]
    cmp1 = "".join(f'<div class="compare-row" data-row><div class="compare-cell compare-cell--param">{p}</div><div class="compare-cell compare-cell--us">{us}</div><div class="compare-cell compare-cell--other">{o}</div></div>' for p,us,o in cmp1_rows)
    cmp2_rows = [
        ("What you buy","A growth system that runs inside your business.","Hours, headcount, decks and campaigns."),
        ("Pricing","Outcome contracts with a locked baseline, a floor and a cap. Minimum retainer — or none.","A monthly retainer regardless of result."),
        ("Time to first value","2-hour audit · 5-day blueprint · 30-day deployment.","6–12 months to deployment, against an 8-month expectation."),
        ("What gets measured","The number in your P&amp;L, against a randomised holdout.","Impressions, ROAS, deliverables shipped."),
        ("Where the work lives","In your ERP, CRM and warehouse — with an eval suite you own.","In the agency&rsquo;s tools and the agency&rsquo;s heads."),
        ("What you own at the end","Agents, evals and a Growth Graph that appreciate.","A body of work you have to re-buy every year."),
        ("Accountability","Fees at risk, in writing, with a clawback clause.","&ldquo;Market conditions changed.&rdquo;"),
        ("When you stop paying","The agents keep running.","Everything stops."),
    ]
    cmp2 = "".join(f'<div class="compare-row" data-row><div class="compare-cell compare-cell--param">{p}</div><div class="compare-cell compare-cell--us">{us}</div><div class="compare-cell compare-cell--other">{o}</div></div>' for p,us,o in cmp2_rows)
    body = f'''
<section class="page-hero">
  <div class="container page-hero__inner">
    <span class="eyebrow">Outcome Contracts</span>
    <h1>Five ways to buy. <span class="accent">All of them published.</span></h1>
    <p class="lead page-hero__lead">Every tier has a floor so we can staff you properly, a cap so your CFO can budget, and a baseline locked at signature so nobody argues about attribution six months in. All figures exclude GST.</p>
    <div class="page-hero__cta"><a href="audit.html" class="btn btn--primary btn--lg">Start at Tier 0 <span class="btn__arrow">→</span></a></div>
  </div>
</section>
<section class="section">
  <div class="container" style="display:flex;flex-direction:column;gap:24px">
    <div class="tier tier--hero">
      <span class="tier__label">Tier 0 · Growth Audit — the front door</span>
      <div class="tier__price">₹75,000 ≈ $790 · 2 hours · 100% credited</div>
      <p class="tier__desc">Two hours with your leadership, and a written baseline at the end of it. Credited in full against any engagement signed within 30 days.</p>
      <div class="tier__rows">
        <div class="tier__row"><span>Value Baseline Memo — your current-state numbers, agreed and signed</span><span>Included</span></div>
        <div class="tier__row"><span>Three costed use cases, ranked by payback</span><span>Included</span></div>
        <div class="tier__row"><span>Fixed price, paid upfront, no scoping call required</span><span>—</span></div>
      </div>
      <p class="tier__note">Extended version — two weeks, five stakeholder interviews, prioritised roadmap: ₹2,50,000 (≈$2,630). We price the audit because free diagnostics select for people who will never buy.</p>
      <div><a href="audit.html" class="btn btn--primary">Book the audit <span class="btn__arrow">→</span></a></div>
    </div>
    <div class="fact-rows">
      <div class="tier">
        <span class="tier__label">Tier 1 · Sprint + Kicker — default first engagement</span>
        <div class="tier__price">₹8L – ₹15L build · then ₹1.5L – ₹3L / month</div>
        <p class="tier__desc">A fixed build, a monthly run fee, and an upside kicker when the agreed KPI lands. No downside for you.</p>
        <div class="tier__rows">
          <div class="tier__row"><span>Build &amp; deploy sprint (6–8 weeks)</span><span>₹8L – ₹15L</span></div>
          <div class="tier__row"><span>Monthly run fee</span><span>₹1.5L – ₹3L</span></div>
          <div class="tier__row"><span>Outcome kicker, paid quarterly</span><span>10–15% of base</span></div>
          <div class="tier__row"><span>Kicker cap</span><span>50% of base</span></div>
        </div>
      </div>
      <div class="tier">
        <span class="tier__label">Tier 2 · Baseline + Bonus — fee genuinely at risk</span>
        <div class="tier__price">₹1.89L – ₹3.15L / month</div>
        <p class="tier__desc">For clients with clean data and a number somebody owns. We take a lower base and put part of it at risk against the target.</p>
        <div class="tier__rows">
          <div class="tier__row"><span>Base fee (70% of the fixed equivalent)</span><span>₹2,10,000</span></div>
          <div class="tier__row"><span>At risk if KPI &lt; 50% of target</span><span>−10% of base</span></div>
          <div class="tier__row"><span>Bonus, 100–120% of target</span><span>+25% of base</span></div>
          <div class="tier__row"><span>Bonus, above 120% of target</span><span>+50% of base</span></div>
        </div>
      </div>
      <div class="tier">
        <span class="tier__label">Tier 3 · Pure per-outcome</span>
        <div class="tier__price">Per unit · floor ₹1.5L / month · cap ₹6L / month</div>
        <p class="tier__desc">Only where the unit is countable and your system already emits it. You pay for the outcome, not the attempt.</p>
        <div class="tier__rows">
          <div class="tier__row"><span>Resolved support ticket</span><span>₹95 – ₹190</span></div>
          <div class="tier__row"><span>Qualified meeting held</span><span>₹15,000 – ₹30,000</span></div>
          <div class="tier__row"><span>Qualified lead</span><span>₹4,500 – ₹15,000</span></div>
          <div class="tier__row"><span>Recovered rupee (dues, disputes)</span><span>20–25%</span></div>
        </div>
        <p class="tier__note">Benchmark: a human-handled ticket costs ₹500–₹1,100. An in-house SDR meeting costs roughly ₹78,000–₹1,09,000 fully loaded.</p>
      </div>
      <div class="tier">
        <span class="tier__label">Tier 4 · Gain-share — ₹1 Cr+ opportunities only</span>
        <div class="tier__price">₹3L / month floor + 20–30% of verified value · cap ₹1.5 Cr / yr</div>
        <p class="tier__desc">The top of the ladder, and the one we are most careful about. A non-refundable floor covers our cost base; above that we take a tiered share of value your finance team has certified.</p>
        <div class="tier__rows">
          <div class="tier__row"><span>Of the first ₹1 Cr of verified value</span><span>20%</span></div>
          <div class="tier__row"><span>From ₹1 Cr to ₹3 Cr</span><span>25%</span></div>
          <div class="tier__row"><span>Above ₹3 Cr (to the annual cap)</span><span>30%</span></div>
          <div class="tier__row"><span>Maximum measurement window per cohort</span><span>2 quarters</span></div>
        </div>
      </div>
    </div>
  </div>
</section>
<section class="section" style="background:var(--surface-section);border-block:1px solid var(--line)">
  <div class="container">
    <div class="sec-head"><div><span class="eyebrow">The machinery</span><h2 style="max-width:26ch">What makes an outcome contract survive contact with reality.</h2></div></div>
    <div class="fact-rows">
      <div class="fact"><h3>Baseline</h3><p>Trailing twelve months of your data, normalised for seasonality, volume and mix. Locked at signature, changed only by formal change control. Exogenous factors named in a schedule so neither side can argue them later.</p></div>
      <div class="fact"><h3>Attribution</h3><p>A randomised 10% holdout wherever you can give us one. Where you can&rsquo;t, a pre-agreed proxy metric decided upfront. Never last-touch.</p></div>
      <div class="fact"><h3>Verification</h3><p>Quarterly certification by a joint steering committee, with your finance team&rsquo;s sign-off required before we raise an invoice. Shared dashboard, buyer audit rights, fifteen-day dispute window.</p></div>
      <div class="fact"><h3>Clawback</h3><p>If the verified value reverses in the following quarter, we repay pro-rata — capped at 100% of that quarter&rsquo;s outcome fee. We have not met anyone else who will write this down.</p></div>
    </div>
    <p class="src" style="margin-top:20px;max-width:90ch">All fees are professional services fees under SAC 9983, quoted exclusive of GST, and invoiced against a defined quarterly certification date. Not tax advice; your finance team should review the contract.</p>
  </div>
</section>
<section class="section">
  <div class="container">
    <div class="sec-head"><div><span class="eyebrow">Choosing</span><h2>Where most clients start.</h2></div></div>
    <div class="dt-table-wrap"><table class="dt-table">
      <tr><th>Where you are</th><th>Start here</th><th>Why</th></tr>
      <tr><td>Never bought AI services; no clean baseline</td><td><strong>Tier 0 → Tier 1</strong></td><td>Build the baseline first, then take upside only. No downside while you learn how we work.</td></tr>
      <tr><td>You have data and a number somebody owns</td><td><strong>Tier 2</strong></td><td>Lower base, real fee at risk. The cheapest way to buy accountability.</td></tr>
      <tr><td>A countable unit your system already emits</td><td><strong>Tier 3</strong></td><td>Tickets, meetings, recoveries. Nothing to argue about — the system counts it.</td></tr>
      <tr><td>₹1 Cr+ P&amp;L line, CFO-sponsored, holdout available</td><td><strong>Tier 4</strong></td><td>The largest upside for both of us, and the only tier where we underwrite the whole number.</td></tr>
    </table></div>
  </div>
</section>
<section class="section" id="compare" style="background:var(--surface-section);border-block:1px solid var(--line)">
  <div class="container">
    <div class="sec-head">
      <div><span class="eyebrow">Comparison one</span><h2 style="max-width:26ch">A chat window is where your team thinks. This is where your business runs.</h2></div>
      <p class="lead">Generic AI is not worthless — your team uses it every day and it is making them faster. But it is ungoverned, unmeasured and un-auditable. All three are fixable, and the fix is what you are paying for.</p>
    </div>
    <div class="compare-table" id="compareTable">
      <div class="compare-row compare-row--header">
        <div class="compare-cell compare-cell--header compare-cell--param"></div>
        <div class="compare-cell compare-cell--header compare-cell--us-header">A Digital Theory agent system</div>
        <div class="compare-cell compare-cell--header">Generic AI chat in a browser</div>
      </div>
      {cmp1}
    </div>
    <p class="src" style="margin-top:16px;max-width:90ch">Sources: MIT NANDA The GenAI Divide (2025, preprint) · Chroma Context Rot · Stanford RegLab · Gartner (June 2025) · IBM · Cyberhaven · India DPDP compliance timeline.</p>
  </div>
</section>
<section class="section">
  <div class="container">
    <div class="sec-head">
      <div><span class="eyebrow">Comparison two</span><h2>A typical agency versus us.</h2></div>
      <p class="lead">Eighty-five percent of agencies prefer retainers. There is nothing wrong with a retainer — but you should know what you are buying and who carries the risk.</p>
    </div>
    <div class="compare-table">
      <div class="compare-row compare-row--header">
        <div class="compare-cell compare-cell--header compare-cell--param"></div>
        <div class="compare-cell compare-cell--header compare-cell--us-header">Digital Theory</div>
        <div class="compare-cell compare-cell--header">A typical agency or consultancy</div>
      </div>
      {cmp2}
    </div>
  </div>
</section>
{CTA}'''
    return page("Outcome Contracts — Pricing",
        "Five published Outcome Contract tiers — from the credited Growth Audit to gain-share on verified value. Floors, caps, locked baselines and clawbacks, in public.",
        body, active="pricing", path="pricing.html",
        seo_title="Pricing — Published Outcome Contracts | Digital Theory")

# ================================================================ COMPANY
def build_company():
    body = f'''
<section class="page-hero">
  <div class="container page-hero__inner">
    <span class="eyebrow">Company</span>
    <h1>Ten years of growth work. Rebuilt around <span class="accent">agents and outcomes.</span></h1>
    <p class="lead page-hero__lead">We were a data-first growth marketing company. We managed ₹100 Cr+ of spend, lifted ROAS by an average of 45%, and acquired more than five lakh users. Then AI changed what a services firm is for — so we changed what we are.</p>
  </div>
</section>
<section class="section" style="padding-top:0">
  <div class="container">
    <div class="hero__proof" style="margin-top:0">
      <div class="stat"><div class="stat__num">50<span class="unit">+</span></div><div class="stat__label">Brands scaled</div></div>
      <div class="stat"><div class="stat__num">₹100<span class="unit">Cr+</span></div><div class="stat__label">Ad spend managed</div></div>
      <div class="stat"><div class="stat__num">45<span class="unit">%</span></div><div class="stat__label">Average ROAS lift</div></div>
      <div class="stat"><div class="stat__num">2</div><div class="stat__label">Offices · Bengaluru, Mumbai</div></div>
    </div>
  </div>
</section>
<section class="section" style="background:var(--surface-section);border-block:1px solid var(--line)">
  <div class="container">
    <div class="sec-head">
      <div><span class="eyebrow">Why we changed</span><h2 style="max-width:26ch">Most firms added AI to a menu. We rebuilt the business around it.</h2></div>
      <p class="lead">The uncomfortable truth about our old model is that we were paid for effort. A retainer is a bet that activity produces outcomes, and the client carries that bet alone. We had the outcome data to know when it worked and when it didn&rsquo;t — so we stopped pretending the risk should sit only on one side of the table.</p>
    </div>
    <div class="bc-principles">
      <div class="bc-principle"><h3>Numbers before adjectives</h3><p>Never &ldquo;significant growth.&rdquo; Always a number, a period, and the method used to measure it. If we can&rsquo;t state it that way, we don&rsquo;t claim it.</p></div>
      <div class="bc-principle"><h3>Say what doesn&rsquo;t work</h3><p>We publish where our own methods break — where synthetic research is unsafe, why llms.txt does nothing, where AI code is more dangerous than human code. Contrarian honesty is the cheapest trust available.</p></div>
      <div class="bc-principle"><h3>Risk belongs on both sides</h3><p>If we design it, build it and run it, we should carry part of the consequence. Otherwise we are selling you optimism at a fixed monthly price.</p></div>
    </div>
  </div>
</section>
<section class="section">
  <div class="container">
    <div class="sec-head"><div><span class="eyebrow">Who we work with</span><h2 style="max-width:22ch">Mid-market companies with a number to move.</h2></div></div>
    <div class="fact-rows" style="grid-template-columns:repeat(3,1fr)">
      <div class="fact"><h3>Size</h3><p>₹100 Cr – ₹1,000 Cr in India. $50M – $1B in the US and GCC. Big enough to have systems worth connecting, small enough that a decision doesn&rsquo;t take three quarters.</p></div>
      <div class="fact"><h3>Sectors</h3><p>D2C and retail, BFSI and fintech, healthcare, education, SaaS, travel, and manufacturing with a distribution motion.</p></div>
      <div class="fact"><h3>Who signs</h3><p>The CEO who owns growth, the COO who owns cost, the CMO or CRO who owns pipeline. Usually all three in the room for the audit — that is rather the point of it.</p></div>
    </div>
    <p style="margin-top:24px;color:var(--fg-muted);font-size:15px;max-width:80ch;line-height:1.65"><strong style="color:var(--lime-400)">Who we are not for.</strong> If you need a forty-country rollout, hire a global consultancy — we will refer you and stay friends. If you want a ₹80,000 brochure site, use a website builder; that tier is collapsing and we are not going to pretend otherwise. And if your data can&rsquo;t support a baseline, we will tell you that in the audit rather than sell you an outcome contract that will end in an argument.</p>
  </div>
</section>
<section class="section" style="background:var(--surface-section);border-block:1px solid var(--line)">
  <div class="container">
    <div class="sec-head"><div><span class="eyebrow">How we work</span><h2>Four things that are always true.</h2></div></div>
    <div class="fact-rows">
      <div class="fact"><h3>01 · Forward-deployed</h3><p>Our engineers work inside your systems and your standups. Not a ticket queue, not a weekly status call.</p></div>
      <div class="fact"><h3>02 · One workflow at a time</h3><p>Binary success criteria and a named owner on your side. Scope creep — not model capability — is what produces negative ROI.</p></div>
      <div class="fact"><h3>03 · Instrumented from hour one</h3><p>If it isn&rsquo;t measured it isn&rsquo;t deployed, because an unmeasured agent can&rsquo;t be priced on outcomes.</p></div>
      <div class="fact"><h3>04 · You keep everything</h3><p>The agents, the evals, the Growth Graph, the documentation. Built in your cloud, portable if you leave.</p></div>
    </div>
  </div>
</section>
{CTA}'''
    return page("Company",
        "Ten years of growth work — ₹100 Cr+ spend managed, 45% average ROAS lift — rebuilt around AI agents and outcome contracts. Bengaluru and Mumbai.",
        body, active="company", path="company.html",
        seo_title="Company — We Engineer Growth | Digital Theory")

# ================================================================ AUDIT
def build_audit():
    faq_html, faq_schema = render_faq([
        ("What exactly happens in the two hours?","<p>A working session, not a pitch: minutes 0–30 we map your revenue path end to end; 30–70 we find where money leaks and which decisions wait on a human; 70–100 we size three candidate agents ranked by payback; 100–120 we write the baseline down and both sides sign it.</p>"),
        ("Who should be in the room?","<p>Whoever owns revenue, whoever owns operations, and whoever owns the data. Usually the CEO, COO and CMO or CRO. The audit works because the people who can say yes are all looking at the same numbers.</p>"),
        ("Why is the audit priced instead of free?","<p>Because free diagnostics select for people who will never buy. A priced audit that is credited in full costs a serious buyer nothing and screens out everyone else. It also means we send our best people, not a junior with a template.</p>"),
        ("What do I keep if we never work together?","<p>The Value Baseline Memo, the three costed use cases, and an honest read on whether your data can support an outcome contract at all. The memo is yours regardless of what you decide next.</p>"),
        ("Can the audit say no?","<p>Yes. If your baseline can&rsquo;t be measured or your systems can&rsquo;t be reached, we will say so in the room. It costs us a sale and saves you a bad year.</p>"),
        ("How is the ₹75,000 credited?","<p>If you sign any engagement within thirty days, the full ₹75,000 comes straight off the first invoice. The extended two-week version (five stakeholder interviews, prioritised roadmap) is ₹2,50,000 and credited the same way.</p>"),
    ], section_title="Questions we get about the audit")
    body = f'''
<section class="page-hero">
  <div class="container page-hero__inner">
    <span class="eyebrow">The 2-hour Growth Audit</span>
    <h1>Two hours. One baseline. <span class="accent">Then you decide.</span></h1>
    <p class="lead page-hero__lead">₹75,000, credited in full against any engagement you sign within thirty days. You leave with a written Value Baseline Memo — your own numbers, agreed — whether or not you ever work with us.</p>
  </div>
</section>
<section class="section">
  <div class="container">
    <div class="sec-head">
      <div><span class="eyebrow">What happens</span><h2>It is a working session, not a pitch.</h2></div>
      <p class="lead">Bring whoever owns revenue, whoever owns operations, and whoever owns the data. Two hours, one room, no deck from us at the start.</p>
    </div>
    <div class="bc-method">
      <div class="bc-step"><div class="bc-step__num">0–30</div><h3>Map</h3><p>We trace the revenue path end to end — how demand arrives, how it converts, where it stalls, and what each stage costs you today.</p></div>
      <div class="bc-step"><div class="bc-step__num">30–70</div><h3>Find</h3><p>Where money leaks, which decisions are waiting on a human being, and what your systems already emit that nobody is currently reading.</p></div>
      <div class="bc-step"><div class="bc-step__num">70–100</div><h3>Size</h3><p>Three candidate agents, each with an estimated payback period and the data it would need. Ranked by time-to-value, not by how interesting they are.</p></div>
      <div class="bc-step"><div class="bc-step__num">100–120</div><h3>Agree</h3><p>We write the baseline down and both sides sign it. That memo is what every future outcome fee would be measured against — and it is yours regardless.</p></div>
    </div>
  </div>
</section>
<section class="section" style="background:var(--surface-section);border-block:1px solid var(--line)">
  <div class="container">
    <div class="sec-head">
      <div><span class="eyebrow">Why it isn&rsquo;t free</span><h2 style="max-width:26ch">Because free diagnostics select for people who never buy.</h2></div>
      <p class="lead">A priced audit that is credited in full costs a serious buyer nothing and screens out everyone else. It also means we send our best people rather than a junior with a template.</p>
    </div>
    <div class="fact-rows">
      <div class="fact"><h3>You get, regardless</h3><p>The Value Baseline Memo, the three costed use cases, and an honest read on whether your data can support an outcome contract at all.</p></div>
      <div class="fact"><h3>We might say no</h3><p>If your baseline can&rsquo;t be measured or your systems can&rsquo;t be reached, we will say so in the room. It costs us a sale and saves you a bad year.</p></div>
    </div>
  </div>
</section>
<section class="section" id="book">
  <div class="container">
    <div class="contact-grid">
      <form class="form" onsubmit="event.preventDefault(); this.querySelector('button').textContent='Thanks — we will come back within one business day.';">
        <div><label>Company</label><input type="text" required placeholder="Company Pvt Ltd" /></div>
        <div><label>Work email</label><input type="email" required placeholder="you@company.com" /></div>
        <div><label>The number you want to move</label><textarea placeholder="One line is enough — e.g. 'CAC is up 40% YoY and the board wants it back down.'"></textarea></div>
        <button type="submit" class="btn btn--primary btn--lg" style="margin-top:8px">Request the audit <span class="btn__arrow">→</span></button>
        <p class="tier__note" style="margin-top:4px">₹75,000 · credited in full against any engagement signed within 30 days</p>
      </form>
      <div class="contact-info">
        <div class="contact-info__row">
          <div class="contact-info__label">What happens next</div>
          <div class="contact-info__value" style="font-size:1rem;font-weight:500;color:var(--fg-muted);line-height:1.6">We come back within one business day with two times and the names of the people who would be in the room.</div>
        </div>
        <div class="contact-info__row">
          <div class="contact-info__label">Email</div>
          <div class="contact-info__value"><a href="mailto:hello@digitaltheory.co.in">hello@digitaltheory.co.in</a></div>
        </div>
        <div class="contact-info__row">
          <div class="contact-info__label">Offices</div>
          <div class="contact-info__value">Bengaluru · Mumbai</div>
        </div>
        <div class="contact-info__row">
          <div class="contact-info__label">Serving</div>
          <div class="contact-info__value">Mid-market across India, US and GCC</div>
        </div>
      </div>
    </div>
  </div>
</section>
{faq_html}'''
    return page("Book the 2-hour Growth Audit",
        "₹75,000, credited in full against any engagement signed within 30 days. Leave with a signed Value Baseline Memo and three costed agents ranked by payback.",
        body, active="", path="audit.html",
        seo_title="Book the 2-hour Growth Audit — ₹75,000, Credited | Digital Theory",
        extra_schema=[faq_schema])

# ================================================================ WRITE + SITEMAP + REDIRECTS
write("revenue-services.html", build_revenue())
write("strategy.html", build_strategy())
write("brand.html", build_brand())
write("implementation.html", build_implementation())
write("engineering.html", build_engineering())
write("labs.html", build_labs())
write("pricing.html", build_pricing())
write("company.html", build_company())
write("audit.html", build_audit())

keep = ["", "revenue-services.html","strategy.html","brand.html","implementation.html","engineering.html",
        "labs.html","pricing.html","company.html","audit.html",
        "case-studies.html","our-work.html","blog.html","careers.html"]
for d in ("case-studies","blog"):
    full = os.path.join(ROOT,d)
    if os.path.isdir(full):
        keep += [f"{d}/{f}" for f in sorted(os.listdir(full)) if f.endswith(".html")]
today = "2026-08-30"
entries = []
for u in keep:
    loc = f"{SITE_URL}/" if u=="" else f"{SITE_URL}/{u}"
    pr = "1.0" if u=="" else ("0.9" if u in ("revenue-services.html","pricing.html","audit.html") else "0.7")
    entries.append(f"  <url>\n    <loc>{loc}</loc>\n    <lastmod>{today}</lastmod>\n    <changefreq>monthly</changefreq>\n    <priority>{pr}</priority>\n  </url>")
write("sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "\n".join(entries) + "\n</urlset>\n")
write("robots.txt", f"User-agent: *\nAllow: /\n\nSitemap: {SITE_URL}/sitemap.xml\n")

redir = []
svc_map = {
    "performance-marketing":"revenue-services.html","seo":"revenue-services.html","crm-retention":"revenue-services.html",
    "branding":"brand.html","social-media-marketing":"brand.html","personal-branding":"brand.html",
    "business-consulting":"strategy.html",
    "sap-b1-implementation":"implementation.html","sfmc-implementation":"implementation.html",
    "odoo-implementation":"implementation.html","ai-automations":"implementation.html",
    "web-development":"engineering.html","app-development":"engineering.html",
}
for slug,dest in svc_map.items():
    redir.append({"source":f"/services/{slug}.html","destination":f"/{dest}","permanent":True})
redir.append({"source":"/services.html","destination":"/","permanent":True})
redir.append({"source":"/services/:slug*","destination":"/","permanent":True})
redir.append({"source":"/industries.html","destination":"/company.html","permanent":True})
redir.append({"source":"/industries/:slug*","destination":"/company.html","permanent":True})
redir.append({"source":"/about.html","destination":"/company.html","permanent":True})
redir.append({"source":"/contact.html","destination":"/audit.html","permanent":True})
with open(os.path.join(ROOT,"vercel.json"),"w") as f:
    json.dump({"redirects":redir}, f, indent=2)
print("wrote vercel.json")
print("\nDone — V2 catalog-format pages built.")
