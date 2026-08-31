#!/usr/bin/env python3
"""Digital Theory V2 — repositioning site generator.
Generates the 9 inner pages of the new architecture + sitemap + vercel.json redirects.
Design system unchanged (assets/styles.css, dark + lime). Nav/footer injected by assets/shared.js.
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
              "mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":to_text(a)}} for q,a in items]}
    return html, schema

def ev(num, unit, claim, src):
    u = f'<span class="unit">{unit}</span>' if unit else ''
    return f'<div class="ev"><div class="stat__num">{num}{u}</div><p class="ev__claim">{claim}</p><div class="src">{src}</div></div>'

def step(n, clock, title, body, out):
    return f'<div class="bc-step"><div class="bc-step__num">{n}</div><div style="font-family:var(--font-mono);font-size:12px;letter-spacing:.1em;color:var(--lime-400);margin-bottom:10px">{clock}</div><h3>{title}</h3><p>{body}</p><p style="margin-top:12px;color:var(--fg);font-size:13.5px"><strong style="color:var(--lime-400)">You get:</strong> {out}</p></div>'

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

ENGINE = f'''
<section class="section" id="engine">
  <div class="container">
    <div class="sec-head">
      <div><span class="eyebrow">The Growth Engine</span><h2 style="max-width:24ch">Two hours to a baseline. Thirty days to production.</h2></div>
      <p class="lead">A four-stage operating loop, with a clock on every stage. The first three get an agent live. The fourth is why month twelve costs us less and returns you more.</p>
    </div>
    <div class="bc-method">
      {step("01","2 HOURS","Audit","A working session across revenue, operations and data. We map where money leaks, which decisions are waiting on a human, and what your systems already emit.","a Value Baseline Memo — the agreed numbers every future outcome is measured against.")}
      {step("02","5 DAYS","Blueprint","Agent architecture, integration map, evaluation criteria, a costed sequence — and the commercial model with baseline, floor and cap written down before anyone builds.","a Growth Engine Blueprint and a signed outcome contract.")}
      {step("03","30 DAYS","Deploy","Forward-deployed engineers build inside your stack — ERP, CRM, warehouse, ticketing. One workflow, binary success criteria, a named owner. First agent live in production.","agents in production and an OpenTelemetry-instrumented eval suite in your stack.")}
      {step("04","∞ EVERY DAY AFTER","Compound","Every outcome, correction and edge case is written back to your Growth Graph. Agents get more accurate, cheaper per outcome, and broader in scope.","a growth system that appreciates instead of one you re-buy annually.")}
    </div>
    <p style="margin-top:28px;color:var(--fg-muted);font-size:14.5px;max-width:72ch;line-height:1.6">Deploy is deliberately narrow: one workflow, binary success criteria, a named owner on your side, automated evaluations on every change — written into the statement of work as delivery standards rather than good intentions. <strong style="color:var(--fg)">Scope, not model capability, is what kills these projects.</strong></p>
  </div>
</section>'''

def svc_schema(name, desc, path):
    return {"@context":"https://schema.org","@type":"Service","name":name,"description":desc,
            "provider":{"@type":"Organization","name":"Digital Theory","url":SITE_URL+"/"},
            "areaServed":[{"@type":"Country","name":"India"},{"@type":"Country","name":"United States"},{"@type":"Country","name":"United Arab Emirates"}],
            "serviceType":name,"url":f"{SITE_URL}/{path}"}

def write(path, content):
    full = os.path.join(ROOT, path)
    with open(full,"w") as f: f.write(content)
    print("wrote", path)

# ================================================================ REVENUE SERVICES
def build_revenue():
    agents = [
        ("Demand","Pipeline agents","ICP scoring against your closed-won data, signal-triggered outbound, meeting qualification and routing — writing to your CRM, not a spreadsheet.","Priced per qualified meeting held. McKinsey documented a US homebuilder tripling its conversion-to-appointment rate with AI sales agents."),
        ("Search","AI SEO &amp; GEO agents","Getting your brand cited by ChatGPT, Perplexity, Gemini and Google AI Overviews — a different discipline from ranking, with different mechanics.","Five of six AI citations come from pages not in the top 10. ChatGPT referrals convert at 15.9% vs 1.76% for organic."),
        ("Creators","Creator-led acquisition","Influencer run as an acquisition channel rather than an awareness one — matched on conversion history, priced per customer. Built with Brand &amp; Influence.","65.9% of brands now expect payback within one month. Fake followers are 56.5% of reported fraud concerns."),
        ("Lifecycle","Retention agents","Churn prediction on behaviour, not RFM alone. Next-best-action per segment, triggered against your billing and support systems.","Personalisation lifts revenue 5–15% (McKinsey). One airline cut high-value churn 59%."),
        ("Service","Resolution agents","Support deflection grounded in your knowledge base and order system. Escalation is free; you only pay for a clean resolution.","₹95–₹190 per resolution vs ₹500–₹1,100 human-handled. 40–60% resolution at launch, 60%+ within a year."),
        ("RevOps","Operating agents","Quote-to-cash, collections follow-up, margin-leakage detection and forecast hygiene — the back-office work where ROI is highest and nobody looks.","50%+ of AI budgets go to front-office despite better back-office ROI."),
    ]
    agents_html = "".join(
        f'<div class="svc-rich__card" style="cursor:default"><div class="svc-rich__body" style="padding-top:28px"><span class="svc-rich__num">{tag}</span><h3 class="svc-rich__title">{t}</h3><p class="svc-rich__desc">{d}</p><div class="src">{src}</div></div></div>'
        for tag,t,d,src in agents)

    mech = [
        ("1 · Baseline","Trailing 12 months of your data, normalised for seasonality, volume and mix. Locked at signature. Exogenous factors named in a schedule so neither side can argue them later."),
        ("2 · Holdout","A randomised 10% holdout wherever you can give us one. Where you can&rsquo;t, a pre-agreed proxy metric. Never last-touch attribution — it is how these deals die."),
        ("3 · Floor &amp; cap","A minimum so we can staff you properly. A ceiling so your CFO can put a number in the plan. Both in the contract on day one."),
        ("4 · Clawback","If the verified value reverses in the following quarter, we repay pro-rata — capped at 100% of that quarter&rsquo;s outcome fee."),
    ]
    mech_html = "".join(f'<div class="fact"><h3>{t}</h3><p>{d}</p></div>' for t,d in mech)

    cmp1_rows = [
        ("Reaches your systems","Reads and writes to SAP Business One, Odoo, Salesforce, your warehouse and your ticketing system.","No access to ERP, CRM, warehouse or ticketing. Every answer is ungrounded in what is true today."),
        ("Memory","Persistent, governed, org-level memory — the Growth Graph.","Session-scoped, per-user, non-transferable. Nothing the organisation learns is retained."),
        ("Accuracy on business tasks","Grounded retrieval cuts hallucination 30–70%; under 2% on grounded summarisation.","Legal-query hallucination measured at 58–88% (Stanford RegLab)."),
        ("Evaluation","Offline evals pre-deploy, online LLM-as-judge in production, every failure converted into a regression test.","None. No ground truth, no regression tests, no quality gate."),
        ("Observability","OpenTelemetry gen_ai.* spans — model calls, tokens, agent steps, tool executions.","No traces, no token accounting, no audit trail."),
        ("Ownership","A named agent owner, evals on every change, one workflow with binary success criteria — contracted.","Nobody owns it. MIT: 60% of firms evaluated custom AI; only 20% reached pilot."),
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
        ("Role of AI","The operating system of the engagement.","A tool the team uses to make deliverables faster."),
        ("Accountability","Fees at risk, in writing, with a clawback clause.","&ldquo;Market conditions changed.&rdquo;"),
        ("Who does the work","Forward-deployed engineers inside your systems.","A pyramid, with juniors on your account."),
        ("When you stop paying","The agents keep running.","Everything stops."),
    ]
    cmp2 = "".join(f'<div class="compare-row" data-row><div class="compare-cell compare-cell--param">{p}</div><div class="compare-cell compare-cell--us">{us}</div><div class="compare-cell compare-cell--other">{o}</div></div>' for p,us,o in cmp2_rows)

    body = f'''
<section class="page-hero">
  <div class="container page-hero__inner">
    <span class="eyebrow">Revenue Services · The flagship</span>
    <h1>We engineer your growth by building AI agents <span class="accent">customised for your business.</span></h1>
    <p class="lead page-hero__lead">Not a chatbot. Not a workflow tool. A growth system that reads your margin data, decides what to do next, executes it, and learns from what happened — with our fee tied to the number it moves.</p>
    <div class="page-hero__cta">
      <a href="audit.html" class="btn btn--primary btn--lg">Start with the 2-hour Audit <span class="btn__arrow">→</span></a>
      <a href="#pricing" class="btn btn--secondary btn--lg">How outcome pricing works</a>
    </div>
  </div>
</section>
{ENGINE}
<section class="section" style="background:var(--surface-section);border-block:1px solid var(--line)">
  <div class="container">
    <div class="sec-head"><div><span class="eyebrow">What we deploy</span><h2 style="max-width:22ch">Agents that touch revenue, not slideware.</h2></div></div>
    <div class="svc-rich">{agents_html}</div>
  </div>
</section>
<section class="section" id="pricing">
  <div class="container">
    <div class="sec-head">
      <div><span class="eyebrow">Outcome-based pricing</span><h2 style="max-width:24ch">No retainer. Or a very small one. If you grow, we grow.</h2></div>
      <p class="lead">Outcome pricing collapsed in advertising once because attribution fights killed it. It works when the machinery is built before the contract is signed — so we build the machinery first, in the 2-hour audit.</p>
    </div>
    <div class="fact-rows">{mech_html}</div>
    <div style="margin-top:28px"><a href="pricing.html" class="btn btn--secondary btn--lg">See the five contract tiers and the numbers <span class="btn__arrow">→</span></a></div>
  </div>
</section>
<section class="section" style="background:var(--surface-section);border-block:1px solid var(--line)">
  <div class="container">
    <div class="sec-head">
      <div><span class="eyebrow">Comparison one</span><h2 style="max-width:26ch">A chat window is where your team thinks. This is where your business runs.</h2></div>
      <p class="lead">We are not going to tell you generic AI is worthless — your team uses it every day and it is making them faster. The problem is that it is ungoverned, unmeasured and un-auditable. All three are fixable.</p>
    </div>
    <div class="compare-table" id="compareTable">
      <div class="compare-row compare-row--header">
        <div class="compare-cell compare-cell--header compare-cell--param"></div>
        <div class="compare-cell compare-cell--header compare-cell--us-header">A Digital Theory agent system</div>
        <div class="compare-cell compare-cell--header">Generic AI chat in a browser</div>
      </div>
      {cmp1}
    </div>
    <p class="src" style="margin-top:16px;max-width:90ch">Sources: MIT NANDA The GenAI Divide (2025, preprint) · Chroma Context Rot · Stanford RegLab · Gartner (June 2025) · IBM · Cyberhaven · India DPDP compliance timeline. A note on the &ldquo;95%&rdquo; figure we quote elsewhere: it describes organisations getting zero return, not projects that failed outright, and it comes from a non-peer-reviewed preprint. We will explain that distinction before you have to ask.</p>
  </div>
</section>
<section class="section">
  <div class="container">
    <div class="sec-head">
      <div><span class="eyebrow">Comparison two</span><h2>A typical agency versus us.</h2></div>
      <p class="lead">Eighty-five percent of agencies prefer retainers, and that preference went up last year. There is nothing wrong with a retainer — but you should know what you are buying and who carries the risk.</p>
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
    schema = svc_schema("Revenue Services","AI agents deployed into the revenue engine — demand generation, AI SEO/GEO, lifecycle, service and RevOps — priced against the number they move.","revenue-services.html")
    return page("Revenue Services",
        "AI growth agents deployed into your revenue engine — demand gen, AI SEO/GEO, lifecycle, service and RevOps — priced on outcomes with a locked baseline, floor and cap.",
        body, active="practices", path="revenue-services.html",
        seo_title="Revenue Services — Outcome-Priced AI Agents | Digital Theory",
        extra_schema=[schema])

# ================================================================ STRATEGY
def build_strategy():
    offers = [
        ("AI &amp; Growth Strategy","From ₹2.5L","Where AI actually changes your P&amp;L, sequenced by payback rather than by fashion. Which functions, which agents, which order, and what each is worth — delivered against your own baseline, not a benchmark deck."),
        ("Market Research as a Service","Subscription or per study","Category sizing, buyer research, pricing studies, concept tests, win/loss and competitive intelligence — AI-moderated at scale, human-validated on a stratified subsample, with the error band published in the report."),
        ("India Mid-Market Benchmark Index","Proprietary","Longitudinal norms for mid-market operating metrics that no tool vendor owns — because tools own respondents and nobody owns the norms. &ldquo;Your repeat-purchase rate is 0.6× the median for your category&rdquo; is a sentence that starts a project."),
        ("Transformation Roadmap","6–8 weeks","The operating model, the org design, the data foundations and the sequencing — with 25% of the fee contingent on the recommendation being live within two quarters."),
    ]
    offers_html = "".join(f'<div class="tier"><span class="tier__label">{p}</span><div class="tier__price">{t}</div><p class="tier__desc">{d}</p></div>' for t,p,d in offers)
    body = f'''
<section class="page-hero">
  <div class="container page-hero__inner">
    <span class="eyebrow">Strategy &amp; Intelligence</span>
    <h1>Decision-grade answers in <span class="accent">five business days.</span></h1>
    <p class="lead page-hero__lead">Growth strategy, AI transformation roadmaps, and Market Research as a Service. Same rigour as a tier-one firm, at a fraction of the clock — because we never had a billable-hour model to protect.</p>
    <div class="page-hero__cta"><a href="audit.html" class="btn btn--primary btn--lg">Book the 2-hour Audit <span class="btn__arrow">→</span></a></div>
  </div>
</section>
<section class="section">
  <div class="container">
    <div class="sec-head">
      <div><span class="eyebrow">The opening</span><h2 style="max-width:24ch">The incumbents already conceded the argument.</h2></div>
      <p class="lead">Strategy advice is now under 20% of McKinsey&rsquo;s work, and roughly 25% of its global fees are tied to outcomes rather than hours. They are right — and they are trapped, because they have a $700-an-hour blended rate and an associate pyramid to protect. We don&rsquo;t. That is a claim about cost structure, and cost structure is checkable.</p>
    </div>
    <div class="ev-grid" style="grid-template-columns:repeat(3,1fr)">
      {ev("5","days","Decision-grade insight, or the fee is waived. Written into the engagement letter.","Digital Theory delivery standard")}
      {ev("25","%","Of our consulting fee tied to the recommendation actually landing — matching McKinsey&rsquo;s outcome share at a fraction of the price.","McKinsey outcome-share benchmark, 2026")}
      {ev("~$25","","All-in cost of an AI-moderated interview, against $500–$1,500 for a traditional in-depth interview.","Published AI-research platform pricing, 2026")}
    </div>
  </div>
</section>
<section class="section" style="background:var(--surface-section);border-block:1px solid var(--line)">
  <div class="container">
    <div class="sec-head"><div><span class="eyebrow">Market Research as a Service</span><h2 style="max-width:24ch">The softest target in professional services.</h2></div></div>
    <div class="dt-table-wrap"><table class="dt-table">
      <tr><th>Method</th><th>Traditional cost</th><th>Traditional timeline</th><th>With us</th></tr>
      <tr><td>20 in-depth interviews</td><td>$15,000 – $30,000</td><td>4–8 weeks</td><td><strong>Days, at a fraction of the cost</strong></td></tr>
      <tr><td>4–6 focus groups</td><td>$24,000 – $90,000</td><td>4–8 weeks</td><td><strong>Under a week</strong></td></tr>
      <tr><td>Five-market study</td><td>$75,000 – $225,000</td><td>8–12 weeks</td><td><strong>50+ languages, one cost base</strong></td></tr>
      <tr><td>Analysis phase alone</td><td>Included</td><td>~4 weeks</td><td><strong>Hours</strong></td></tr>
    </table></div>
    <p class="src" style="margin-top:16px;max-width:90ch">Traditional market research grows 4.8% a year while research software grows 11.5%; in India, analytics grows 14% against syndicated research at 6% (ESOMAR 2025 · MRSI 2026). Microsoft cut research timelines from 4–6 weeks to hours and ran 100+ interviews at one-third of traditional cost.</p>
  </div>
</section>
<section class="section">
  <div class="container">
    <div class="sec-head">
      <div><span class="eyebrow">Our unfair advantage</span><h2 style="max-width:22ch">We publish where our own method breaks.</h2></div>
      <p class="lead">Synthetic respondents fail in specific, characterisable ways the peer-reviewed literature has documented. Every firm selling AI research knows this. We are the ones who put it in writing.</p>
    </div>
    <div class="fact-rows">
      <div class="fact"><h3>Where it is safe</h3><p>Ranking and prioritisation. One reproduction of a 3,600-person survey achieved a median Spearman ρ of 0.90 across 53 matched questions.</p></div>
      <div class="fact"><h3>Where it breaks</h3><p>Magnitude. Models systematically overestimate effect sizes (<em>Nature</em>, 2026), and one study measured a 14.5 percentage-point mean absolute error — worst on exactly the consumer and market questions you would commission.</p></div>
      <div class="fact"><h3>Where it breaks badly</h3><p>Significance and segment variance. Across 156 experiments, when the human study found no significant effect, models produced one in 68–83% of cases (<em>Nature Computational Science</em>, 2025).</p></div>
      <div class="fact"><h3>The protocol</h3><p>Every synthetic finding is validated against a stratified human subsample, and the observed error band is disclosed in the deliverable — contractually. No tool vendor will do this; it costs them sales.</p></div>
    </div>
  </div>
</section>
<section class="section" style="background:var(--surface-section);border-block:1px solid var(--line)">
  <div class="container">
    <div class="sec-head"><div><span class="eyebrow">What you can buy</span><h2>Four ways in.</h2></div></div>
    <div class="fact-rows">{offers_html}</div>
  </div>
</section>
{CTA}'''
    schema = svc_schema("Strategy & Intelligence","Growth strategy, AI transformation roadmaps, and Market Research as a Service — decision-grade insight in five business days.","strategy.html")
    return page("Strategy & Intelligence",
        "Growth strategy, AI roadmaps and Market Research as a Service — decision-grade insight in 5 business days, with 25% of the fee tied to the outcome.",
        body, active="practices", path="strategy.html",
        seo_title="Strategy & Intelligence — Research in 5 Days | Digital Theory",
        extra_schema=[schema])

# ================================================================ BRAND
def build_brand():
    six = [
        ("01","Brand strategy &amp; positioning","The category you intend to own, the buyer you intend to move, and the words that do it. Written to be repeated by a salesperson, a journalist and a language model — three audiences that used to be one."),
        ("02","AI Influencer Marketing","Creator matching on conversion history rather than follower count, fraud screening before you sign, and disclosure compliance generated into every brief. The gap in this market is measurement, not execution."),
        ("03","Social media marketing","Always-on social run by agents against a brief you approve — planning, production, community response and reporting — with a human editor on every post that carries a claim."),
        ("04","Personal &amp; founder-led branding","Founders are the highest-trust distribution most mid-market companies own, and the most under-used. A governed voice model built from your own writing — never a generic ghostwriter — with you signing off on everything."),
        ("05","Content strategy &amp; editorial","Built to be cited, not just read. Source citations lift AI visibility ~115%, statistics +41%, direct quotations +28% — and adding words alone does nothing at all. We write to that as a scored standard."),
        ("06","Entity &amp; mention engineering","The connective layer: schema, knowledge panels, review profiles and consistent naming — making every machine that reads about you resolve it to the same entity. Feeds directly into the GEO work in Revenue Services."),
    ]
    six_html = "".join(f'<div class="svc-rich__card" style="cursor:default"><div class="svc-rich__body" style="padding-top:28px"><span class="svc-rich__num">{n}</span><h3 class="svc-rich__title">{t}</h3><p class="svc-rich__desc">{d}</p></div></div>' for n,t,d in six)
    mechs = [
        ("We make brand measurable — then price it on outcomes","Share of citation in your category, tracked across ChatGPT, Perplexity, Gemini and Google AI Overviews, against a baseline agreed before we start. Brand has never been outcome-priced because it has never been countable. Now it is."),
        ("The earned-media citation map","We maintain, per vertical, the list of publications and creators each generative engine actually cites — the 98% of the problem that pitch lists miss. Proprietary, empirical, and it compounds every month we run it."),
        ("Creator selection on outcome data, not reach","Every platform sells follower counts. Nobody has which creator, in which category, in which format, actually produced a customer — at what cost. After a few campaigns, we do, and that data is not for sale anywhere."),
        ("Compliance we indemnify","ASCI&rsquo;s 2026 guidelines impose a dual disclosure mandate on AI influencers, with the brand treated as the advertiser and penalties to ₹50 lakh. We take that on in writing."),
        ("Owned brand IP instead of rented audience","Everything else in influencer marketing is rent. A brand character you own is an appreciating asset — the market&rsquo;s best-known example earns around $34,000 a post — and the audience never renegotiates."),
    ]
    mechs_html = "".join(f'<div class="bc-principle"><h3>{t}</h3><p>{d}</p></div>' for t,d in mechs)
    body = f'''
<section class="page-hero">
  <div class="container page-hero__inner">
    <span class="eyebrow">Brand &amp; Influence</span>
    <h1>Being known is now <span class="accent">a ranking factor.</span></h1>
    <p class="lead page-hero__lead">Brand used to be the line item nobody could measure and everybody cut first. That changed the moment machines started deciding who gets recommended — because what they read is your brand mentions. We build brand, influence and content as an instrumented system, and measure it where it now counts.</p>
    <div class="page-hero__cta">
      <a href="audit.html" class="btn btn--primary btn--lg">Book the 2-hour Audit <span class="btn__arrow">→</span></a>
      <a href="revenue-services.html" class="btn btn--secondary btn--lg">See how it connects to revenue</a>
    </div>
  </div>
</section>
<section class="section">
  <div class="container">
    <div class="sec-head">
      <div><span class="eyebrow">The reframe</span><h2>Your brand is training data now.</h2></div>
      <p class="lead">When a buyer asks ChatGPT or Perplexity who they should use, the model isn&rsquo;t reading your website. It is reading what the rest of the internet says about you — press, reviews, podcasts, creator posts, forum threads. The soft spend became the hard input, and almost nobody has noticed yet.</p>
    </div>
    <div class="ev-grid">
      {ev("r=0.66","","Correlation between brand mentions and AI visibility — against 0.22 for backlinks. Roughly 3× stronger.","Ahrefs, 75,000-brand study, 2025")}
      {ev("82","%","of AI citations come from earned media. Owned and paid together account for 6%.","Muck Rack, 1M+ citations, Dec 2025")}
      {ev("2","%","overlap between the journalists PR teams pitch and the journalists AI actually cites.","Muck Rack, Dec 2025")}
      {ev("₹5,000","Cr","Projected size of India&rsquo;s influencer market by 2027, from ₹3,000–3,500 Cr in 2025.","Kofluence, 2026")}
    </div>
    <p style="margin-top:24px;color:var(--fg-muted);font-size:15px;max-width:76ch;line-height:1.65"><strong style="color:var(--lime-400)">Read the 2% carefully — it is the whole opportunity.</strong> Almost every PR and content programme in the country is pitching a list of publications that generative engines do not cite. The work isn&rsquo;t harder than what agencies already do. It is aimed at the wrong targets, and nobody is checking.</p>
  </div>
</section>
<section class="section" style="background:var(--surface-section);border-block:1px solid var(--line)">
  <div class="container">
    <div class="sec-head"><div><span class="eyebrow">What we do</span><h2>Six things, run as one system.</h2></div></div>
    <div class="svc-rich">{six_html}</div>
  </div>
</section>
<section class="section">
  <div class="container">
    <div class="sec-head"><div><span class="eyebrow">How we build advantage</span><h2 style="max-width:26ch">Five things a creative agency structurally cannot do.</h2></div></div>
    <div class="bc-principles" style="grid-template-columns:1fr;gap:16px">{mechs_html}</div>
  </div>
</section>
<section class="section" style="background:var(--surface-section);border-block:1px solid var(--line)">
  <div class="container">
    <div class="sec-head">
      <div><span class="eyebrow">What we will tell you not to do</span><h2 style="max-width:26ch">AI influencers are wrong for most of your categories.</h2></div>
      <p class="lead">Virtual influencers average roughly 5.67% engagement against 1.89% for human creators. But in authenticity-driven categories, humans outperform virtual by up to 2.7×, and 43.8% of consumers hold active ethical concerns. We recommend virtual for gaming, electronics and fashion-forward work — and against it for health, financial services and anything where trust is the product.</p>
    </div>
    <div class="fact-rows" style="grid-template-columns:repeat(3,1fr)">
      <div class="fact"><h3>Reach is not the metric</h3><p>65.9% of brands now expect payback from influencer spend within a month. If your programme cannot attribute, it cannot survive that expectation — and attribution is the part we build first.</p></div>
      <div class="fact"><h3>Keep social in-house if it works</h3><p>Two-thirds of brands already run influencer in-house, and they are right to. We are not here to take the team&rsquo;s job — we give them a system, a standard and a measurement layer.</p></div>
      <div class="fact"><h3>Brand is slower than performance</h3><p>Citation share moves in months, not weeks. We will show you the leading indicators, and we will not pretend a quarter is a verdict.</p></div>
    </div>
  </div>
</section>
<section class="section">
  <div class="container">
    <div class="sec-head">
      <div><span class="eyebrow">How this is priced</span><h2>Brand, on an outcome contract.</h2></div>
      <p class="lead">Because citation share is countable, brand work can sit on the same commercial terms as everything else we do. That is new — and as far as we know, nobody else in this market offers it.</p>
    </div>
    <div class="fact-rows" style="grid-template-columns:repeat(3,1fr)">
      <div class="fact"><h3>The outcome</h3><p>Share of citation in your category across the engines your buyers actually use — measured with tools you can buy yourself for a few hundred dollars a month, so you never have to take our word for the number.</p></div>
      <div class="fact"><h3>The guarantee</h3><p>Category citation share moving by month four, or month four is free.</p></div>
      <div class="fact"><h3>Influencer work</h3><p>Priced per qualified outcome — a customer, not a post — with a monthly floor so we can staff the programme and a cap so you can budget it.</p></div>
    </div>
    <div style="margin-top:28px"><a href="pricing.html" class="btn btn--secondary btn--lg">See the contract tiers <span class="btn__arrow">→</span></a></div>
  </div>
</section>
{CTA}'''
    schema = svc_schema("Brand & Influence","Brand strategy, AI influencer marketing, social, founder-led branding, content and entity engineering — instrumented and priced on citation share.","brand.html")
    return page("Brand & Influence",
        "Brand mentions predict AI visibility 3× better than backlinks. We build brand, influencer, social and content as an instrumented system — priced on citation share.",
        body, active="practices", path="brand.html",
        seo_title="Brand & Influence — Brand, Priced on Outcomes | Digital Theory",
        extra_schema=[schema])

# ================================================================ IMPLEMENTATION
def build_implementation():
    mech = [
        ("01","The Pre-Mortem Scorecard","Before we quote, we score you on the things that actually sink these projects — executive sponsorship, data readiness, change capacity, and whether the value is defined well enough to measure. Below threshold, we tell you what to fix first and decline the project. Refusing work is the most credible thing a services firm can do."),
        ("02","The eval harness is a deliverable","An OpenTelemetry-instrumented evaluation suite that lives in your stack — offline evals pre-deploy, online judging in production, and every real-world failure converted into a regression test. You keep it whether or not you keep us."),
        ("03","Three standards, contracted","A named agent owner on your side. Automated evaluations on every change. One workflow with binary success criteria. Most firms treat these as good practice. We write all three into the statement of work as delivery standards you can hold us to."),
        ("04","A countable agent library","Not &ldquo;hundreds of pre-built agents.&rdquo; A specific, versioned, evaluated set across order-to-cash, support triage and finance operations, each with a published eval suite and a coverage score you can inspect."),
        ("05","Forward-deployed engineers","Our engineers sit inside your systems and your standups, not behind a ticket queue. There are roughly 2,000 genuinely elite forward-deployed engineers in the world and demand is rising faster than supply. We are building that bench in India."),
        ("06","Fixed fee, with fee at risk","A fixed price with a defined portion clawed back on miss. Gartner names escalating cost and unclear value as the top reasons agentic projects get cancelled — both are scope problems. Fixed scope with binary criteria is the countermeasure, and putting our fee behind it is how you know we mean it."),
    ]
    mech_html = "".join(f'<div class="svc-rich__card" style="cursor:default"><div class="svc-rich__body" style="padding-top:28px"><span class="svc-rich__num">{n}</span><h3 class="svc-rich__title">{t}</h3><p class="svc-rich__desc">{d}</p></div></div>' for n,t,d in mech)
    systems = [
        ("ERP","SAP Business One · Odoo","Implementation, migration, localisation and AMC — plus the agent layer on top. In mid-market ERP, systems-integration fees are 40–60% of the total. Services are the product."),
        ("CRM &amp; marketing","Salesforce · SFMC","Implementation, migration and consolidation, with agents wired into the objects that matter rather than a chatbot on the homepage."),
        ("Data","Warehouse &amp; integration","The unglamorous layer: pipelines, identity resolution, and the semantic model that makes agent answers correct instead of plausible."),
        ("Governance","Evals, observability, DPDP","Traces, token accounting, failure clustering, audit logs, RBAC and consent-compatible processing — designed for enforcement in May 2027, built now."),
    ]
    systems_html = "".join(f'<div class="fact"><span class="tier__label">{tag}</span><h3 style="margin-top:8px">{t}</h3><p>{d}</p></div>' for tag,t,d in systems)
    body = f'''
<section class="page-hero">
  <div class="container page-hero__inner">
    <span class="eyebrow">Implementation &amp; Systems</span>
    <h1>Gartner expects 40% of agentic projects to be cancelled. <span class="accent">Almost none of it will be the technology.</span></h1>
    <p class="lead page-hero__lead">AI agents, SAP Business One, Odoo, Salesforce and SFMC — delivered against the failure modes that actually kill these projects: unclear value, weak change management, bad data, and scope that grows. We score you against them before we quote, and we walk away from projects that won&rsquo;t work.</p>
    <div class="page-hero__cta"><a href="audit.html" class="btn btn--primary btn--lg">Book the 2-hour Audit <span class="btn__arrow">→</span></a></div>
  </div>
</section>
<section class="section">
  <div class="container">
    <div class="sec-head"><div><span class="eyebrow">The evidence</span><h2>The failure rate is the business case.</h2></div></div>
    <div class="ev-grid">
      {ev("40","%+","of agentic AI projects forecast to be cancelled by end-2027.","Gartner prediction, June 2025")}
      {ev("5","%","of integrated GenAI pilots are extracting real value; the rest show no measurable P&amp;L impact.","MIT NANDA, 2025 · preprint")}
      {ev("40–60","%","of mid-market ERP implementation cost is systems-integration fees. Services are the product.","ERP Research, 2026")}
      {ev("2","×","Pilots built through a strategic partnership reached full deployment twice as often as internal builds.","MIT NANDA, 2025")}
    </div>
    <p style="margin-top:24px;color:var(--fg-muted);font-size:15px;max-width:76ch;line-height:1.65">Read Gartner&rsquo;s reasons carefully: escalating costs, unclear business value, inadequate risk controls. <strong style="color:var(--fg)">Not model quality.</strong> Every one is a delivery-method failure — which means every one is preventable by method. Method is the thing we sell.</p>
  </div>
</section>
<section class="section" style="background:var(--surface-section);border-block:1px solid var(--line)">
  <div class="container">
    <div class="sec-head"><div><span class="eyebrow">How we deliver</span><h2 style="max-width:24ch">Six things we do that almost nobody does.</h2></div></div>
    <div class="svc-rich">{mech_html}</div>
  </div>
</section>
<section class="section">
  <div class="container">
    <div class="sec-head">
      <div><span class="eyebrow">The systems we know</span><h2 style="max-width:24ch">Agents without the system of record are toys.</h2></div>
      <p class="lead">This is the part of our business that looks least glamorous and matters most. An agent that cannot see inventory, margin, credit terms or service history is guessing. We have implemented these platforms for years — which is why our agents can read them.</p>
    </div>
    <div class="fact-rows">{systems_html}</div>
  </div>
</section>
{CTA}'''
    schema = svc_schema("Implementation & Systems","Agent implementation plus SAP Business One, Odoo, Salesforce and SFMC — fixed fee with fee at risk, delivered against the failure modes that kill agentic projects.","implementation.html")
    return page("Implementation & Systems",
        "AI agents, SAP B1, Odoo, Salesforce & SFMC — delivered with a Pre-Mortem Scorecard, contracted delivery standards, an eval harness you keep, and fee at risk.",
        body, active="practices", path="implementation.html",
        seo_title="Implementation & Systems — Agents + ERP/CRM | Digital Theory",
        extra_schema=[schema])

# ================================================================ ENGINEERING
def build_engineering():
    receipts = [
        ("Vodafone","31% LCP improvement","+8% sales"),
        ("Redbus","Core Web Vitals optimisation","+80–100% mobile conversion rate"),
        ("T-Mobile","Core Web Vitals focus","+60% visit-to-order, −20% in-site issues"),
        ("Swappie","23% load-time reduction","+42% mobile revenue"),
        ("Renault","1-second LCP improvement","+13% conversion, −14% bounce"),
        ("Nykaa","40% LCP improvement","+28% organic traffic from Tier 2/3 cities"),
    ]
    receipts_html = "".join(f'<tr><td>{c}</td><td>{w}</td><td><strong>{r}</strong></td></tr>' for c,w,r in receipts)
    commitments = [
        ("SLA","Passing all three Core Web Vitals at p75 on launch, or we fix it free. Fewer than half of sites pass on mobile, and the top 1,000 barely do better. The Chrome UX Report is public data — you can audit our claim without trusting us, which is the strongest form of proof there is."),
        ("Pricing","A base build fee plus a share of measured conversion lift — underwritten by a published elasticity, not by optimism."),
        ("Search","Built to be cited, not just ranked. Schema, entity markup, strict heading hierarchy and citation-optimised structure ship by default — because roughly five of every six AI Overview citations come from pages outside the top 10."),
        ("Code","Human review and a static-analysis gate on every line of AI-generated code. The published research on AI-generated code quality is not reassuring, and a vulnerability that ships is cheaper to catch here than in production."),
        ("Access","WCAG conformance as a deliverable, not a preference. Under the European Accessibility Act it is a legal requirement — and it is the one thing that cannot be vibe-coded."),
    ]
    commitments_html = "".join(f'<div class="bc-principle"><h3>{t}</h3><p>{d}</p></div>' for t,d in commitments)
    body = f'''
<section class="page-hero">
  <div class="container page-hero__inner">
    <span class="eyebrow">Product &amp; Platform Engineering</span>
    <h1>We don&rsquo;t sell websites. We sell <span class="accent">measured conversion lift</span> — and publish the numbers.</h1>
    <p class="lead page-hero__lead">Web, mobile and AI-native product builds. Every site we ship passes all three Core Web Vitals at p75, or we fix it free — and you can verify that on public data without taking our word for anything.</p>
    <div class="page-hero__cta"><a href="audit.html" class="btn btn--primary btn--lg">Book the 2-hour Audit <span class="btn__arrow">→</span></a></div>
  </div>
</section>
<section class="section">
  <div class="container">
    <div class="sec-head">
      <div><span class="eyebrow">The honest read</span><h2 style="max-width:26ch">AI made boilerplate cheap and everything above it harder.</h2></div>
      <p class="lead">A randomised trial found experienced developers 19% slower with AI tools while believing they were 20% faster. McKinsey measured 46% time savings on routine tasks and under 10% on complex work. Brochure sites are genuinely collapsing to $20-a-month tools. Let them. Everything above that line now commands more, not less.</p>
    </div>
    <div class="ev-grid">
      {ev("48","%","of origins pass all three Core Web Vitals on mobile — 56% on desktop.","HTTP Archive Web Almanac 2025, on CrUX data")}
      {ev("51","%","of the top 1,000 origins pass on mobile. Scale does not fix this.","Web Almanac 2025")}
      {ev("19","%","slower — experienced developers using AI tools, while believing they were 20% faster.","METR randomised trial, 2025")}
      {ev("+8.4","%","Retail conversion associated with a 0.1-second improvement, with AOV up 9.2%.","Deloitte &amp; Google · data 2019, published 2020")}
    </div>
  </div>
</section>
<section class="section" style="background:var(--surface-section);border-block:1px solid var(--line)">
  <div class="container">
    <div class="sec-head"><div><span class="eyebrow">The receipts</span><h2 style="max-width:26ch">Speed is not a technical metric. It is a revenue metric.</h2></div></div>
    <div class="dt-table-wrap"><table class="dt-table">
      <tr><th>Company</th><th>What changed</th><th>What happened to the business</th></tr>
      {receipts_html}
    </table></div>
    <p class="src" style="margin-top:16px;max-width:90ch">Published case studies from Google&rsquo;s web.dev library. We cite them because you can check them. These are observational correlations rather than controlled experiments — worth knowing before you build a business case on any single one.</p>
  </div>
</section>
<section class="section">
  <div class="container">
    <div class="sec-head"><div><span class="eyebrow">What we put in the contract</span><h2>Five commitments, all of them checkable.</h2></div></div>
    <div class="bc-principles" style="grid-template-columns:1fr;gap:16px">{commitments_html}</div>
  </div>
</section>
{CTA}'''
    schema = svc_schema("Product & Platform Engineering","Web, mobile and AI-native product builds sold on measured conversion lift, with a publicly auditable Core Web Vitals SLA.","engineering.html")
    return page("Product & Platform Engineering",
        "Web, mobile and AI-native builds sold on measured conversion lift. Every site passes all three Core Web Vitals at p75 or we fix it free — verifiable on public CrUX data.",
        body, active="practices", path="engineering.html",
        seo_title="Product & Platform Engineering | Digital Theory",
        extra_schema=[schema])

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
      <div class="fact"><h3>Baseline</h3><p>Trailing twelve months of your data, normalised for seasonality, volume and mix. Locked at signature, changed only by formal change control. Exogenous factors — macro shifts, regulatory change, your own pricing moves — named in a schedule so neither side can argue them later.</p></div>
      <div class="fact"><h3>Attribution</h3><p>A randomised 10% holdout wherever you can give us one. Where you can&rsquo;t, a pre-agreed proxy metric decided upfront. Never last-touch. Performance pricing died in advertising once because of attribution fights, and we are not repeating that.</p></div>
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
      <p class="lead">The uncomfortable truth about our old model is that we were paid for effort. A retainer is a bet that activity produces outcomes, and the client carries that bet alone. We had the outcome data to know when it worked and when it didn&rsquo;t — so we stopped pretending the risk should sit only on one side of the table. Everything on this site follows from that one decision.</p>
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

# Sitemap: enumerate actual html files we keep
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

# vercel.json 301 redirects for retired URLs
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
print("\nDone — V2 pages built.")
