# Session Context — HerboVilla Shopify Theme

**Last worked:** 2026-08-07
**Project:** PRM HerboVilla Shopify theme
**Path:** `C:\Users\sonik\Desktop\New\last prm update\HerboVilla Shopify\prm-herbovilla-theme`
**Live theme:** `151479124142` on `prm-herbovilla.myshopify.com` / `prmherbovilla.com`
**Push command:** `shopify theme push --theme 151479124142 --allow-live --force --only <path>`
**GitHub:** `https://github.com/krish2248/PRM-SHOPIFY.git` (branch `main`)

---

## ⚠️ READ FIRST — OPEN PRICING ISSUES

> Krish's standing instruction (2026-08-07): **report this section first, before anything else**,
> at the start of every session. Pricing errors cost money on every order.

### 1. NEW MRP rollout is NOT applied to the live store yet
`price-mapping.json` + `update-prices.py` are ready and validated (25 rows, 0 unresolved), but
**blocked on a Shopify Admin API token**. Nothing has been written to product prices.

To unblock: Shopify admin → Settings → Apps and sales channels → Develop apps → create app,
scopes `read_products` + `write_products` → install → copy `shpat_...` token, then:
```powershell
$env:SHOPIFY_ADMIN_TOKEN="shpat_xxxxxxxxxx"
cd "C:\Users\sonik\Desktop\New\last prm update\HerboVilla Shopify"
python update-prices.py            # dry run — writes nothing
python update-prices.py --apply    # applies, after writing a rollback backup
```
22 prices go up (e.g. ICEE 224→240, Vedacold 220→240, soaps 144→162, Pynil Ointment 168→200),
1 goes down (Dermo Neem 144→120, confirmed correct by Krish).

### 2. ~11 COMBO listings will be UNDERPRICED once the rollout runs
They're priced off their components and are **not** in the MRP sheet. Krish still owes numbers:

| Combo listing | Current |
|---|---|
| Platigen Syrup & Tablets COMBO | ₹570 |
| Cofula & Vedacold COMBO | ₹293 |
| Pynil Ointment & Capsules COMBO | ₹252 |
| Harry Syrup & Tablets COMBO | ₹280 |
| ZymoVilla Syrup & Tablets COMBO | ₹280 |
| Dermovilla Syrup & Tablets | ₹280 |
| Prolax Tablets & Syrup COMBO | ₹160 |
| Saheli Soap & Cream COMBO | ₹156 |
| Hair Marshal & Prolice Oil COMBO | ₹140 |
| ArthoVilla Oil & Syrup COMBO | ₹0 ⚠️ |
| Rome Oil & Capsules COMBO | ₹0 ⚠️ |

### 3. Products priced ₹0 on the live store (sellable for free)
- `ArthoVilla Oil & Syrup COMBO` — ₹0
- `Rome Oil & Capsules COMBO` — ₹0
- `PRM Ayurvedic Nasal Inhaler (pack of 4)` — ₹0
- `PRM Platigem Tablets` — ₹0
- `Stenovilla Herbal Tablets for Kidney Stones (Pack of 2)` — ₹0

### 4. Skipped / unresolved from the MRP sheet
- **PYNIL CAPSULES 30cap** — sheet says ₹210 (pack of 2 = ₹420) but the listing sits at ₹168
  (the *ointment's* price) and its live title reads "Pynil Piles Care Combo", not capsules.
  Krish chose to skip until the listing itself is fixed.
- **PREGONE CAPSULE** (12cap, ₹140) and **SUMAN MEGA CAPSULE** (6cap, ₹210) — in the sheet,
  no matching product among the 66 live listings. Need creating in admin.
- **Duplicate ArthoVilla oil listing** — "Arthovilla Ayurvedic Joint & Muscle Relief Oil" (₹336)
  looks like a second copy of the 100ml pack-of-2. Left untouched; either reprice to ₹360 or
  delete the duplicate.

### 5. Store data hygiene (handle/title swaps — not pricing, but confusing)
- handle `prm-prince-mouth-gel-...` → title says "Prince Mouth **Liquid**" (pack of 4)
- handle `prm-prince-mouth-liquid-...` → title says "Prince Mouth **Gel**" (pack of 3)
- handle `prm-steno-villa-...-syrup-...` → title says "Stenovilla Herbal **Tablets**"
- handle `prm-steno-villa-...-tablet-...` → title says "Stenovilla Kidney Care **Syrup**"
- handle `prm-dermo-villa-herbal-syrup-200ml-...` → title says "Dermovilla Herbal **Soap**"
- handle `prm-prolax-...-syrup-170ml-...` → title is raw copy: "Chronic Constipation Poor bowel movement…"
- Saheli Syrup listing carries SKU `PRM HARRY-1 SYRUP`

---

## Session 2026-08-07 — NEW MRP pricing rollout (prepared, not applied) + auto-calculating combo packs

Krish supplied `NEW MRP (2).xls` (26 rows) and asked to update product pricing only.

### 1. Key finding — prices are admin data, not theme code
Product prices live in Shopify admin. The theme contains **no** product prices except the
`combo_pack` block defaults. So this was not a code edit — it needs the Admin REST API.

### 2. Pricing rule derived from the sheet
The sheet gives **per-unit MRP** plus Pack of 2/3/4/5 columns that are **exact multiples**
(zero pack discount). The store sells almost everything as multipacks, so:

> **new listing price = per-unit MRP × pack count in the product title/handle**

This matches how it was priced before (e.g. ICEE ₹224 = old MRP ₹112 × 2), confirming the rule.

### 3. Files created (in repo root, next to `populate-collections.py`)
- **`price-mapping.json`** — full Excel→store mapping: 23 `confident`, 1 `needs_decision`
  (Pynil Capsules, skipped), 2 `not_on_store`, plus a `knock_on_effects` section.
- **`update-prices.py`** — dry-run by default; `--apply` writes; timestamped backup written
  before every apply; `--rollback <backup.json>` restores. `--include-decisions` opts into
  the needs_decision rows.

Validated offline against live `products.json`: all 25 rows resolve, every handle + variant
matches, every recorded "current price" matches live. **0 unresolved.**

### 4. Krish's decisions this session
- **Dermo Neem Soap** → apply ₹120 (the only downward move; it's intentionally the cheap soap at MRP ₹60 vs ₹81)
- **Pynil Capsules** → skip (listing looks mispriced/mislabelled today)
- **Combo pack selector** → auto-calculate from product price
- **COMBO listings** → leave alone, flag only; Krish will send numbers later

### 5. Theme change — combo pack selector now auto-calculates (`sections/product-template.liquid`)
- Pack of N price is now `product.price × N`, rendered via the `money` filter
  (was hardcoded ₹500 / ₹750 applied globally to all 66 products)
- MRP + "% off" lines only render when a real `compare_at_price` exists — with the new
  zero-discount sheet they stay hidden instead of showing a fake "0% off"
- Block settings `price` / `mrp` are now **optional overrides** — blank = auto. Schema labels
  and `info` text updated to say so.
- `templates/product.json` — cleared the ₹500/₹750/₹600/₹1000 hardcodes to `""`, and turned
  **off** `best_value` on Pack of 5 (with no discount it claimed a saving that doesn't exist)

`shopify theme check`: product-template.liquid is clean (only pre-existing ImgWidthAndHeight
errors at rows 951/1033 and two HardcodedRoutes warnings). The 54 repo-wide errors are
pre-existing and live in other files — `product-pdf-url.liquid` and friends have malformed
`elsif X or (Y and Z)` conditionals that Liquid silently truncates. Worth a cleanup pass.

### 6. NOT pushed to Shopify
The theme change is local + committed only. Plan is to push it together with the price
rollout once the Admin token exists, so the storefront changes once, not twice.

### Carry-forward
See the **READ FIRST — OPEN PRICING ISSUES** block at the top of this file. That is the
first thing to report next session.

---

## Session 2026-05-27 — Product page major expansion, employee cleanup, description overhaul

Big session: restored theme after employee broke it via admin editor, then added major new product page sections.

### 1. Employee admin editor cleanup — full theme restore
- Employee had added a "product description section" on the homepage and extra sections below reviews on product page via Shopify admin theme editor
- Pushed all 32 local files back to live theme to overwrite: all templates, sections, snippets, config, layout, theme.css, theme.js

### 2. Combo Pack Selector (near Add to Cart) — `sections/product-template.liquid`
- **Radio-style cards**: Single (default, product price) / Pack of 3 / Pack of 5
- Each shows: combo price, M.R.P crossed out, % off badge
- "Best Value" green tag on the best deal
- Selecting a combo updates main price display + quantity automatically
- Schema block type `combo_pack` with settings: label, quantity, price, mrp, best_value
- Defaults in `product.json`: Pack of 3 (₹500, MRP ₹600) and Pack of 5 (₹750, MRP ₹1000, Best Value)

### 3. Video Testimonials section — "Real Users, Real Results"
- 4 vertical reel-style video cards (9:16 aspect ratio, Instagram-like) + 1 optional YouTube product video
- Videos autoplay muted via YouTube embed; clicking opens original URL (opens app on mobile)
- Cream background card with green dashed border placeholders when no URL set
- Grid auto-adapts columns to match number of cards
- Schema: `video_testimonial` blocks (video_url + click_url) + section settings (youtube_product_url + youtube_click_url)
- Placed right after Description section, before Research-Backed Ingredients
- Currently shows 4 placeholder cards (no URLs filled yet — Krish needs to paste YouTube/Shorts URLs)

### 4. Research-Backed Ingredients section
- 4 detailed ingredient cards with: image placeholder, name, scientific name (italic), description, green research badge
- Defaults: Papaya Extract (Clinically Studied), Giloy (Ayurvedic Gold Standard), Tulsi (Traditional Medicine), Ashwagandha (Evidence-Based)
- Schema block type `research_ingredient` with image_picker, name, scientific_name, description, badge
- Admin can upload ingredient images and customize per product

### 5. Product Comparison table
- "Feature | Our Product | Others" green-header table
- Rows: Natural Ingredients, GMP Certified, Side Effects, Clinically Tested, State FDA Approved
- Green checkmarks for "Our Product", red crosses for "Others"
- Hardcoded brand-wide claims (same for all products)

### 6. Description section — complete visual overhaul
- **Cream background** (#FDF8F0) with rounded corners, padding — no more dead white space
- **JS auto-structuring**: detects h2/h3/h4 headings in product description HTML, wraps each heading+content group into white `.desc-block` cards with green borders
- **Two-column layout**: when exactly 2 heading groups exist (e.g., "Key Skin Benefits" + "Herbal Ingredients"), they're placed side-by-side
- **Ingredient lists**: lists with 4+ items auto-become 3-column pill grids
- **Styled RTE elements**: list items get green check icons + card backgrounds, tables get green headers + alternating rows, bold text highlighted, images get rounded corners
- **Product specs table**: white card with green heading accent
- **Benefits grid**: cleaner card styling

### 7. Sections removed (per Krish's request)
- Removed "Premium Ayurvedic Wellness" two-column showcase section
- Removed "Key Benefits" 4 circular icons section
- Removed "Key Ingredients" 3-card section (ingredient blocks still in schema for future use)

### 8. Schema additions to product-template
- New block types: `combo_pack`, `research_ingredient`, `video_testimonial`
- `ingredient` block got `image_picker` field added
- New section settings: `showcase_heading`, `showcase_text`, `youtube_product_url`, `youtube_click_url`

### 9. Krish's completed homework (confirmed this session)
- Razorpay: done
- Nimbus Post: done
- Collections: done
- 3lakh+ happy customers: done

### Files pushed this session
```
sections/product-template.liquid  (massive — combo packs, video testimonials, research ingredients, comparison table, description overhaul, all CSS/JS)
templates/product.json            (added combo_pack, research_ingredient, video_testimonial blocks)
templates/index.json              (restored from employee mess)
+ 30 other files restored in the initial cleanup push
```

### Product page section order (current)
1. Breadcrumbs
2. Main product grid (gallery + info + combo packs + add to cart + buy now + share + trust badges)
3. Description section (cream bg, auto-structured cards, specs table)
4. Video Testimonials ("Real Users, Real Results" — 4 reel placeholders)
5. Research-Backed Ingredients (4 cards)
6. Product Comparison table
7. You May Also Like (horizontal scroll)
8. Customer Reviews (admin blocks + localStorage + form)

### Carry-forward notes for next session
- **Video testimonials**: 4 placeholder cards visible — Krish needs to paste YouTube/Shorts URLs in theme editor (Product page → Video Testimonial blocks)
- **YouTube product video**: setting exists but empty — fill in theme editor → Product Template → settings → "YouTube Product Video URL"
- **Combo pack pricing**: currently set to generic ₹500/₹750 defaults — Krish should update per-product via theme editor (or create product-specific templates)
- **Research ingredient images**: all 4 cards show placeholder icons — upload images in theme editor blocks
- **Ingredient card images**: `image_picker` field added to ingredient block schema but no images uploaded yet
- **Description auto-structuring** depends on product descriptions having proper headings (h2/h3/h4) in the Shopify rich text editor — descriptions without headings will render as plain text in a cream card

---

## Session 2026-05-25 — Major product page rewrite, content corrections, cart fix

Massive session covering product page overhaul, About Us content corrections, AYUSH removal, and multiple homepage/navbar updates.

### 1. Doctor's Reviews — replaced fake with real testimonials (`templates/index.json`)
- Removed all 8 fake doctor testimonials
- Added 3 real PRM testimonials:
  - **Dr. Devang Patel** (Deesa, Gujarat) — Harry Capsules, Saheli Syrup, Prince Mouth Gel
  - **Vaidh Dr. B.L. Parik** (Jodhpur, Rajasthan) — Harry group, Liver Tonic, Rome group
  - **Vaidh Pankaj Kavre** (Amravati, Maharashtra) — Harry Capsules, Pynil Capsules, Cofula
- Fixed testimonial card CSS for equal-height cards (`assets/theme.css`)

### 2. Product Page — complete rewrite (`sections/product-template.liquid`)
- **Layout modelled after Vasu Store** (vasustore.com) structure
- Two-column grid: sticky image gallery + product info
- Feature pills: GMP Certified, Clinically Tested, No Side Effects, State FDA Approved
- Key Benefits box (2-column grid from section blocks)
- Quantity + Add to Cart + Buy Now + Download Presentation buttons
- Share buttons: WhatsApp, Facebook, Copy Link
- 4 trust badges: Free Shipping, Authentic, Secure Checkout, COD
- **Description section** (no tabs — clean single section with benefits grid + product specs table)
- **"You May Also Like"** horizontal scrollable carousel with left/right arrows (pulls from same collection, up to 8 products, each with Add to Cart)
- **Customer Reviews section**: rating summary bars, admin-controlled review blocks (only removable via Shopify admin), customer review form with image upload (up to 5 photos with preview), localStorage persistence
- White background (`#fff`) for entire product page
- White image borders (removed cream/pastel `#FDF8F0` tint)

### 3. AYUSH Certificate — removed from entire store
Replaced every "AYUSH" reference with "State FDA Approved" or removed entirely:
- Homepage certifications (index.json)
- Product page feature pills
- Hero qualification strip chips (removed AYUSH chip, replaced with "25+ Years / Trusted legacy")
- Footer cert badge
- Customer login trust badges
- Expert section, brand mission, certifications section defaults
- About Us templates (page.about-us.json, page.about.json, page.json)
- Qualifications strip preset

### 4. WHO-GMP — changed from "Facility" to "Products"
- "WHO-GMP Certified Facility" → "WHO-GMP Certified Products" everywhere
- Hero chip: "Certified facility" → "Certified Products"
- About Us achievement card, parent brand card, all template presets
- Qualifications strip preset

### 5. Business Hours — updated to 10:00 AM - 7:00 PM
Changed across: footer, contact page (display + schema default), page template, refund policy

### 6. About Us Page — major content batch
- **Hero text**: "serving 3 Lakh+ customers across 22+ states"
- **Hero card**: "3Lakh+ Customers" (was Healthcare Pros)
- **At a Glance subtitle**: "the people, the goal, and the efforts behind every HerboVilla bottle"
- **Removed "Production"** from caption → "QC · R&D · Field Force"
- **150+ Employees** → "150+ Team Members"
- **QC lab caption** → "QC & Formulation Research"
- **Herbs caption** → "Organic & A-Grade Herbs · 40+ Botanicals"
- **Parent brand paragraph**: "one of the largest player", removed "1 international market" suffix, updated HerboVilla paragraph ("manufactured at top GMP certified facilities ensuring pharmaceutical standards")
- **Removed Dhyey Soni/IIT-Delhi paragraph** entirely
- **Parent brand card**: "marketing / distribution", HerboVilla "marketed & distributed"
- **Why Choose section**: updated GMP text ("GMP-certified production plant sharing qualities goals as per pharmaceutical standards")
- **WHO-GMP achievement**: "WHO-GMP Certified Products / Since 2018 · Renewed continuously / Our products are being manufactured under..."
- **ISO 9001:2015**: "Certified 2023" added back
- **Removed "Nutraceuticals since 2018"** from FSSAI
- **Gujarat MSME**: "exporters" → "company"
- **Removed entire "3 Lakh+ Customers Served" milestone card**
- **Removed entire "In the Community" media section** (trade press, 25+ Years, Top-10, #1, 300+ stats)
- **Achievements grid**: changed from 4-column to 3-column (3x3 layout)
- **Removed "FDA / Regulatory approved" chip** from hero qualification strip

### 7. Homepage Changes
- **Hero "Pure Herbal" box**: "High Quality organic herbs" (removed "sourced from Himalayas")
- **Bestsellers section**: collection changed from `all` → `best-sellers`, limited to 8 products
- **New Arrivals section**: collection set to `new-arrivals`, button links to `/collections/new-arrivals`

### 8. Navbar — added Bestsellers & New Arrivals
- Desktop nav: Home · All Products · **Bestsellers** · **New Arrivals** · About Us · Blog · Contact · Cart
- Mobile menu: same additions
- Links: `/collections/best-sellers` and `/collections/new-arrivals`

### 9. Contact Page — background color matched to homepage (`#FDF8F0`)

### 10. Herbs & Uses — first herb font weight
- Removed bold (`font-weight: 600`) from the first herb in each category card
- All herbs now display at normal weight (`font-weight: 400`)

### 11. Cart Drawer — checkout button fix (`assets/theme.js`)
- **Bug**: when cart was empty on page load, the checkout footer HTML wasn't server-rendered. Adding a product via AJAX showed items but no Checkout button.
- **Fix**: JS `render()` now dynamically creates the footer (Subtotal + Checkout + tax note) if it doesn't exist in the DOM
- Cart drawer title now updates item count live ("Your Cart (N)")

### Files pushed this session
```
sections/product-template.liquid  (complete rewrite — multiple pushes)
sections/about-page.liquid        (major content batch — multiple pushes)
sections/hero.liquid               (AYUSH/FDA/WHO-GMP chip changes)
sections/header.liquid             (Bestsellers + New Arrivals nav links)
sections/footer.liquid             (hours + AYUSH removal)
sections/contact-page.liquid       (hours + background color)
sections/page-template.liquid      (hours)
sections/refund-policy.liquid      (hours)
sections/certifications.liquid     (AYUSH → State FDA)
sections/qualifications-strip.liquid (AYUSH → State FDA)
sections/customer-login.liquid     (AYUSH removal)
sections/expert-section.liquid     (AYUSH removal)
sections/brand-mission.liquid      (AYUSH removal)
sections/herbs-uses.liquid         (first herb font weight fix)
sections/testimonials.liquid       (no changes — CSS fix was in theme.css)
snippets/cart-drawer.liquid        (no changes — fix was in theme.js)
templates/index.json               (testimonials + bestsellers + new arrivals)
templates/page.about-us.json      (hero text + AYUSH removal)
templates/page.about.json         (hero text + AYUSH removal)
templates/page.json                (hero text + AYUSH removal)
assets/theme.css                   (testimonial card flex fix)
assets/theme.js                    (cart drawer checkout button fix)
```

### Carry-forward notes for next session
- **Bestsellers collection**: handle is `best-sellers` in theme code. If products don't show, verify the exact handle in Shopify Admin > Products > Collections > Best Sellers (check URL at bottom of page).
- **New Arrivals collection**: handle is `new-arrivals`. Same verification needed.
- **Policy pages** (Terms of Service, Shipping Policy, Refund Policy): already have full content with proper standard clauses — no changes needed this session.
- **Customer reviews**: stored in localStorage per product handle + admin blocks in theme editor. Admin reviews are permanent; customer-submitted reviews persist in browser only.
- **`social-proof-bar.liquid`** still has default "10,000+ Happy Customers" — hasn't been flagged yet.

---

## Session 2026-05-14 — Navbar cleanup, About Us overhaul, favicon

Big content + structural batch. All edits pushed live (push reported success each time).

### 1. Navbar — removed 3 collection links (`sections/header.liquid`)
- Removed `Child-Care`, `Skin-Care`, `Supplements` from both desktop nav and mobile menu
- Desktop nav is now: `Home · All Products · About Us · Blog · Contact · Cart`
- **Note for Krish:** the collection URLs (`/collections/child-care` etc.) still resolve because the collections still exist in Shopify admin. To fully remove them, go to Shopify admin → Products → Collections → delete (or unpublish) each one. Theme code cannot delete admin records.

### 2. Tata 1mg marketplace link
- `config/settings_data.json` + `config/settings_schema.json` default for `marketplace_tata1mg` → `https://www.1mg.com/marketer/prm-85731` (was search URL)
- Used in footer marketplace chip + contact-page marketplace chip via `settings.marketplace_tata1mg`

### 3. Favicon (`layout/theme.liquid`)
- Added fallback: if `settings.favicon` is blank, the site now uses `assets/herbovilla-transparent.png` for `<link rel="icon">`, `shortcut icon`, and `apple-touch-icon`
- Browser tab will show HerboVilla logo after hard-reload (Ctrl+Shift+R)
- **Optional follow-up:** the full logo gets blurry when browsers downscale to 16×16/32×32. For sharper rendering, upload a square cropped favicon (just the tree mark, no text) in Shopify admin → Online Store → Themes → Customize → Theme settings → Favicon. That overrides the fallback automatically.

### 4. About Us page — major content batch (`sections/about-page.liquid`)

**Hero & showcase stat cards**
- Hero card "250+ Formulations" → **84+ Formulations**
- Showcase tile placeholder "250+ Formulations · 85+ Brands" → **"84+ Formulations · 55+ Products"**
- Figcaption "250+ Formulations" → **84+ Formulations**

**Parent-brand block (body paragraph + card list)**
- Body: "85+ brands, 250+ formulations" → **"55+ products, 84+ formulations"**
- Card list: "85+ Brands across therapy areas" → **"55+ Products across therapy areas"**; "250+ Formulations" → **"84+ Formulations"**
- 35,000+ customers / 22+ states / 1 international market left alone (Krish didn't ask)

**Achievement cards — major rework**
- WHO-GMP: "Awarded 2010 · Renewed continuously" → **"Awarded 2018 · Renewed continuously"**; body rewritten to *"Our product manufacturing under the World Health Organisation's Good Manufacturing Practices — the global gold standard for pharmaceutical production quality."*
- ISO 9001:2015: "Certified 2012" → **"Certified 2023"**
- **AYUSH Ministry Licence card REPLACED** with **Saurashtra Chamber of Commerce & Industry** (title + body rewritten, year line says "Member Certificate")
- State FDA card: title "State FDA Approved **Plant**" → **"State FDA Approved Product"**; removed "Continuously inspected" year line; body kept
- **Removed entire "Schedule T & Schedule M / Compliant since launch" card**
- 35,000+ Customers Served body: "250+ SKU portfolio" → **"84+ SKU portfolio"** (kept "35,000+" since Krish didn't explicitly say to change it — note the trust strip on homepage says "3lakh+" so this is inconsistent; flag if Krish notices)

**Entire "Meet the PRM · HerboVilla Team" section REMOVED** (final step of session)
- Whole `<section class="about-team">` block deleted — section header, 5 team-stat cards, culture block, and Zero/100%/10+yrs/90days list. About Us page now ends after the achievement cards.
- Mid-session Krish had me update individual team stats (QC 10+, R&D 6+, Field Sales Team Members 43+, BAMS 4+, Production Operators 60+, removed 150+ Team Members) and rewrite the culture text. Then he scrapped the whole section. So all that team-stat code is gone — if Krish wants any of it back, restore from git history or rewrite.

### Files pushed this session
```
sections/header.liquid
sections/about-page.liquid   (pushed 3 times across the session)
config/settings_data.json
config/settings_schema.json
layout/theme.liquid
```

### Carry-forward notes for next session
- `sections/social-proof-bar.liquid` still has default `10,000+ Happy Customers` — Krish hasn't pointed at it yet, but flag if he mentions the standalone counter.
- The 35,000+ on the achievement card may be inconsistent with the homepage's "3lakh+" trust line — wait for Krish to call it out before changing.
- Krish still has manual homework: Razorpay KYC, Nimbus Post setup, collection populate (see `Krish's instruction guide.pdf` + section below).
- The `/collections/child-care`, `/collections/skin-care`, `/collections/supplements` collection records still need to be deleted/unpublished in Shopify admin — only the navbar links were removed from theme code.

---

## Session 2026-05-11 — Content/copy corrections pushed to live

Krish gave a batch of content-only corrections to apply across the entire site. All edits made locally + pushed live (push reported success).

### Changes applied
1. **Amazon marketplace URL** → `https://www.amazon.in/l/27943762031?ie=UTF8&marketplaceID=A21TJRUUN4KGV&product=B0CS2Z3JWZ&me=ASQS5905XC63T` (this is Krish's actual Amazon storefront page, not a search). Set in `config/settings_data.json` + `config/settings_schema.json` default. Used everywhere via `settings.marketplace_amazon` — footer chip, contact page chip, about page connect grid.
2. **Meesho marketplace URL** → `https://www.meesho.com/PRMCOMPANY?ms=2` (PRM's actual Meesho store). Same locations.
3. **Business hours** → `Monday - Saturday: 10:00 AM – 6:30 PM` (was a mix of `9:00 AM – 6:00 PM` and `9:30 AM – 6:30 PM`). Updated in: `sections/footer.liquid`, `sections/contact-page.liquid` (display + schema default), `sections/page-template.liquid`, `sections/refund-policy.liquid`.
4. **Trust line** → "Trusted by over **3lakh+** customers across India" (was `10,000+`). Updated in `sections/certifications.liquid` schema default + `templates/index.json` `trust_text` setting. Krish wrote it literally as "3lakh+" so we kept that exact form (not "3 Lakh+" or "3,00,000+") — matches what's stored in the certifications strip on the homepage.
5. **Distribution figures** → site now consistently says **"22+ states & 1 country of active distribution"**. Updated everywhere in `sections/about-page.liquid` + about page templates:
   - Hero stat card: `28+` → `22+` Indian States
   - Showcase stat: `20+` → `22+` States Across India
   - Parent-brand list: `28+ States, 3 Countries` → `22+ States & 1 Country of active distribution`
   - Body paragraphs: `28+ Indian states` → `22+ Indian states`, `3 international markets` / `3 Countries` → `1 international market` / `1 Country`
   - Hero text default (schema + `templates/page.about-us.json` + `templates/page.about.json`): `across 28 states` → `across 22+ states`

### Files pushed
```
config/settings_data.json
config/settings_schema.json
sections/contact-page.liquid
sections/page-template.liquid
sections/footer.liquid
sections/refund-policy.liquid
sections/certifications.liquid
sections/about-page.liquid
templates/index.json
templates/page.about-us.json
templates/page.about.json
```

### Notes for next session
- Krish said "do these rest i tell later on" — more content corrections are queued, scope TBD.
- The `sections/social-proof-bar.liquid` block still has a default of `10,000+ Happy Customers`. We did NOT change it this session because Krish specifically named the "Trusted by over 10,000+..." phrase, not the standalone counter. If he points at it next session, flip to `3lakh+` there too.
- `sections/customer-login.liquid` already says `Trusted by 3,00,000+ Ayurvedic households` — left alone (already aligned with the new figure).

---

## Session 2026-05-02 — Restored hero + shop-by-goal on live (paused, resuming tonight)

Krish reported the homepage hero section was missing and the "Shop by Health Goal" section's sizing/structure looked wrong on live. Diagnosis: local files were intact (untouched since the 2026-04-25 mobile pass) — the live theme had been edited via the Shopify admin theme editor, so live diverged from local.

**Fix applied:** pushed local copies back to live theme `151479124142` to overwrite the editor changes:
- `templates/index.json` — restores hero at top of `order` + 6 shop-by-goal collection blocks (immunity-boosters, hair-skin-care, digestive-health, respiratory-care, joint-pain-relief, womens-health)
- `sections/hero.liquid` — full two-column hero + 6-chip qualifications strip at hero bottom
- `sections/shop-by-goal.liquid` — section structure
- `snippets/collection-card.liquid` — icon-card design (white SVG on `#2D6A4F` green background, icon picked by collection handle)
- `assets/theme.css` — included for safety

Push command used:
```
shopify theme push --theme 151479124142 --allow-live --force \
  --only templates/index.json \
  --only sections/hero.liquid \
  --only sections/shop-by-goal.liquid \
  --only snippets/collection-card.liquid \
  --only assets/theme.css
```

Theme push reported success. Krish has not yet confirmed visual result — verify at `https://prm-herbovilla.myshopify.com` (hard reload) when resuming.

**Krish's next-session intent:** "we will work later on night" — minor changes pending, scope TBD when he returns.

### Lesson learned (carry forward)
If Krish reports something "missing" or "changed" on the homepage, first check whether local files were modified (look at file mtimes vs the last session date in this file). If local is untouched, the divergence is almost certainly the Shopify admin theme editor — re-pushing local overwrites it.

---

## Session 2026-04-25 — Mobile optimization pass

Krish reported the mobile view was unstructured: product page title cut off, hero cramped, trust badges stacked, qualification chips cluttering the hero. Desktop was fine and must stay untouched. All changes are gated behind mobile/tablet media queries.

### Product page (`sections/product-template.liquid`)
- `product-grid` now uses `minmax(0, 1fr)` so child columns cannot overflow their track
- `.product-info` given `min-width: 0` + `max-width: 100%`
- `.product-title` gets `word-wrap / overflow-wrap: break-word / hyphens: auto` so long product titles wrap instead of cutting off
- Description blocks (`.product-description-short`, `.desc-benefits li`, `.product-highlights li`, etc.) get `overflow-wrap: anywhere`
- Added ≤768px breakpoint: title 1.55rem, price 1.45rem, main image padding reduced, thumbnails 64×64
- Added ≤576px breakpoint: title 1.35rem, tightened buttons/quantity selector, breadcrumbs truncate
- **Trust badges now horizontal 3-up on mobile** (`grid-template-columns: repeat(3, 1fr)` at ≤576px) — previously stacked 1fr
- ≤380px breakpoint for tiny phones — further font reductions

### Home hero (`sections/hero.liquid`)
- ≤992px: `.hero__features` **hidden entirely** (the "100% Natural · GMP Certified · Free Shipping Above ₹400" checklist) — Krish wanted it gone on mobile/tablet/iPad
- ≤992px: `.hero__quali-strip` **hidden entirely** (the 6 WHO-GMP / ISO / FSSAI / AYUSH / FDA / Global GMP chips) — home page already has a dedicated Certifications section below the hero
- ≤992px: hero padding tightened to 40px 0 32px, grid to 1 column, feature cards 2-up
- ≤640px: label/title/description/buttons sized down, buttons stack full-width, feature cards 1-up
- ≤380px breakpoint for tiny phones
- Floating badges already hidden on mobile (pre-existing)

### Herbs & Uses (`sections/herbs-uses.liquid`)
- Each category card now **shows only the first half** of the herb list on ≤1024px (mobile/tablet/iPad)
- Liquid loop builds a cleaned herbs array, calculates `half_herbs = ceil(total / 2)`, adds `.herb-card__list-extra` class to items past that index
- CSS hides `.herb-card__list-extra { display: none; }` at `@media (max-width: 1024px)`
- Desktop (>1024px) still shows the full list unchanged

### Featured products grid (`sections/featured-collection.liquid`)
- All `repeat(N, 1fr)` → `repeat(N, minmax(0, 1fr))` so cards can't overflow
- ≤768px: gap 14px, font sizes tightened (vendor 10px, title 13px, price 15px), card radius 12px
- ≤480px: gap 10px, even smaller fonts, compact badges

### Global safeguards (`assets/theme.css`)
- Added "MOBILE OPTIMIZATION — GLOBAL SAFEGUARDS" block at the end of the file
- `html, body { max-width: 100%; overflow-x: hidden }`
- All headings/paragraphs get `overflow-wrap: break-word`
- At ≤768px: all top-level sections clipped to viewport, all grid cells/children get `min-width: 0`
- Featured products forced to 2-up on phones (never 1-up), with tightened card typography
- ≤640px: why-us grid 2-up compact, certifications grid 2-up compact
- ≤420px: tightened products grid, why-us, certifications, section headers, announcement bar

### Files touched this session
- `sections/product-template.liquid`
- `sections/hero.liquid`
- `sections/herbs-uses.liquid`
- `sections/featured-collection.liquid`
- `assets/theme.css`
- `SESSION-CONTEXT.md` (this file)

---

## Still pending from earlier sessions (Krish's homework)

External/manual steps — see `Krish's instruction guide.pdf` for full instructions:

1. **Razorpay** — sign up, complete KYC (1–3 business days), activate in Shopify admin, paste API keys, run a ₹1 test order
2. **Nimbus Post** — sign up, complete KYC (same-day), top up wallet, install Nimbus Shopify channel, configure pickup address
3. **Collections** — generate Shopify Admin API token (custom app), run `python populate-collections.py` from the project folder

---

## Session 2026-04-24 (previous)

### About Us page hero (`sections/about-page.liquid`)
- Hero `min-height: 100vh` so it fills viewport on first paint
- Two-column grid `minmax(0, 1fr) minmax(0, 1fr)` with `width: 100%` on right column
- Logo on white rounded card (radius 22px, padding 36px 40px, soft shadow)
- 4 stat cards (Years of Excellence / Healthcare Pros / Indian States / Formulations)
- CTAs: "Shop Our Products" + "Talk to Us" with SVG icons
- Decorative radial gradients (`.about-hero__decor`)

### About Us page sections
- **"At a Glance" header** — pastel mint card (`#F0FAF4 → #E6F4EA` gradient, `#D4ECDD` border)
- **Showcase tiles** — 165px row height, gap 10px, all 6 tiles dark pastel green palette
- **Achievement cards** — all 8 cards now use WHO-GMP green gradient

### Header (`sections/header.liquid` + `layout/theme.liquid`)
- Replaced "PRM HerboVilla" text with `herbovilla-transparent.png`
- Logo wrapped in white rounded box
- Box dimensions: padding 6px 28px, radius 12px, image height 48px desktop / 40px mobile menu / 42px tablet / 36px small mobile
- `--header-height` = 72px

### PDF guide
- `Krish's instruction guide.pdf` in project root
- Step-by-step beginner instructions for Razorpay, Nimbus Post, Collections population
- Generator script `generate_guide.py` kept for regen

---

## Open design choices we may revisit

- About Us hero `min-height: 100vh` may feel too tall on very short laptop screens — could switch to `min-height: max(640px, 90vh)` if Krish reports this
- Achievement cards are uniformly green (per Krish's request) — previous varied palette in git history if he changes his mind
- Showcase tile placeholders only show when `section.settings.showcase_image_*` is blank

---

## How to resume next session

1. Open this folder in Claude Code: `C:\Users\sonik\Desktop\last prm update\HerboVilla Shopify\prm-herbovilla-theme`
2. Read this file for full context
3. If Krish has more mobile tweaks, the pattern is: edit the relevant `sections/*.liquid` or `assets/theme.css`, then push with `shopify theme push --theme 151479124142 --allow-live --force --only <path>`
4. Desktop (>992px) must stay untouched — gate every change behind `@media (max-width: 992px)` or smaller
