#!/usr/bin/env python3
"""page.src.html + assets/*.webp -> two outputs:

- index.html            full standalone document for hosting (SEO head + JSON-LD)
- geumjung-motors.html  fragment for claude.ai Artifact preview (wrapped by the host)
"""
import base64, pathlib

SITE_URL = "https://geumjung.netlify.app/"

root = pathlib.Path(__file__).parent
src = (root / "page.src.html").read_text()

PHOTOS = ["master", "tire", "engine", "oil", "brake"]
marker = '<style id="photoCss"></style>'
assert marker in src, "photoCss marker not found"

# artifact fragment: external requests are blocked, so photos go in as base64
b64_rules = []
for name in PHOTOS:
    b64 = base64.b64encode((root / "assets" / f"{name}.webp").read_bytes()).decode()
    b64_rules.append(f".ph-{name}{{background-image:url(data:image/webp;base64,{b64})}}")
fragment = src.replace(marker, '<style id="photoCss">' + "\n".join(b64_rules) + "</style>")
(root / "geumjung-motors.html").write_text(fragment)

# hosted build: reference the asset files so they load in parallel and cache
url_rules = [f".ph-{name}{{background-image:url(assets/{name}.webp)}}" for name in PHOTOS]
hosted = src.replace(marker, '<style id="photoCss">' + "\n".join(url_rules) + "</style>")

# ── standalone document for hosting ──
seo_head = f"""<meta charset="utf-8">
<meta name="naver-site-verification" content="25ee0f2c84a943156451fdd41188ace1bc9b630e">
<meta name="keywords" content="남양주 카센터, 화도읍 카센터, 화도읍 카센타, 금남리 카센터, 마석 카센터, 남양주 공업사, 화도읍 공업사, 자동차 고장, 자동차 수리, 남양주 자동차 정비, 타이어 교체, 엔진오일 교환, 브레이크 정비, 금중자동차공업사, 카포스">
<meta name="robots" content="index, follow">
<link rel="canonical" href="{SITE_URL}">
<meta property="og:type" content="website">
<meta property="og:locale" content="ko_KR">
<meta property="og:site_name" content="카포스 금중자동차공업사">
<meta property="og:title" content="금중자동차공업사 | 남양주 화도읍 카센터·자동차 정비">
<meta property="og:description" content="1996년부터 남양주 화도읍에서. 마석·금남리 인근 자동차 고장 수리, 타이어·엔진·오일·브레이크 정비 전문 카센터. ☎ 010-2370-0303">
<meta property="og:url" content="{SITE_URL}">
<meta property="og:image" content="{SITE_URL}assets/og.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="geo.region" content="KR-41">
<meta name="geo.placename" content="경기도 남양주시 화도읍">
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "AutoRepair",
  "name": "카포스 금중자동차공업사",
  "alternateName": ["금중자동차공업사", "금중카센터", "화도읍 금중자동차"],
  "description": "남양주 화도읍 카센터. 1996년부터 자동차 고장 수리, 타이어 교체, 엔진 수리, 엔진오일·소모품 교환, 브레이크 정비 전문.",
  "url": "{SITE_URL}",
  "image": "{SITE_URL}assets/og.jpg",
  "telephone": "+82-10-2370-0303",
  "foundingDate": "1996",
  "priceRange": "₩₩",
  "address": {{
    "@type": "PostalAddress",
    "streetAddress": "화도읍 북한강로 1505",
    "addressLocality": "남양주시",
    "addressRegion": "경기도",
    "addressCountry": "KR"
  }},
  "areaServed": ["남양주시", "화도읍", "금남리", "마석", "묵현리"],
  "employee": {{ "@type": "Person", "name": "김주림", "jobTitle": "대표" }},
  "openingHoursSpecification": [
    {{
      "@type": "OpeningHoursSpecification",
      "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
      "opens": "08:30", "closes": "19:00"
    }},
    {{
      "@type": "OpeningHoursSpecification",
      "dayOfWeek": "Saturday",
      "opens": "08:30", "closes": "12:00"
    }}
  ],
  "makesOffer": [
    {{ "@type": "Offer", "itemOffered": {{ "@type": "Service", "name": "타이어 교체·휠 밸런스" }} }},
    {{ "@type": "Offer", "itemOffered": {{ "@type": "Service", "name": "엔진 수리·경고등 진단" }} }},
    {{ "@type": "Offer", "itemOffered": {{ "@type": "Service", "name": "엔진오일·소모품 교환" }} }},
    {{ "@type": "Offer", "itemOffered": {{ "@type": "Service", "name": "브레이크 패드·디스크 정비" }} }}
  ]
}}
</script>"""

# the hosted build is head-content (title/meta/styles) followed by body markup;
# the first body element is the top M stripe
split_at = '<div class="m-stripe top-stripe"'
head_part, body_part = hosted.split(split_at, 1)
body_part = split_at + body_part

standalone = f"""<!doctype html>
<html lang="ko">
<head>
{seo_head}
{head_part}</head>
<body>
{body_part}</body>
</html>"""

(root / "index.html").write_text(standalone)
print(f"built index.html ({len(standalone)//1024} KB standalone) + geumjung-motors.html ({len(fragment)//1024} KB fragment)")
