# Digitaltheory — Website

A data-first growth marketing company website. Static HTML/CSS/JS — no build step required.

## Structure

```
index.html                 # Home
services.html              # All services hub
case-studies.html          # All case studies hub
about.html                 # About / vision / values
careers.html               # Open roles
contact.html               # Contact form + offices

case-studies/              # 6 detailed case study pages
  celio.html · nutriglow.html · codingal.html
  laundrokart.html · pocket52.html · thulasi.html

services/                  # 9 detailed service pages
  performance-marketing.html · branding.html · web-development.html
  app-development.html · business-consulting.html · video-production.html
  seo.html · digital-transformation.html · crm-retention.html

assets/
  styles.css               # Design system (dark + lime accent)
  shared.js                # Nav + footer injection, mobile menu

build_pages.py             # Regenerator for inner pages
```

## Design system

- **Palette:** true-black canvas, graphite surfaces, near-white ink, single muted apple-green accent (`#8CC63F`)
- **Type:** Archivo (display + body), JetBrains Mono (labels, eyebrows)
- **Components:** pill buttons, hairline-bordered cards, radial-void hero, lime "platform" band

## Deploying to Vercel

Static site — point Vercel at the repo root, no build command, output directory `./`.

## Editing inner pages

Edit `build_pages.py` and re-run:

```bash
python3 build_pages.py
```

All inner pages (services, case studies, about, careers, contact) regenerate from data in the script.
