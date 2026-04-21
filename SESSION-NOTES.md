# PRM HerboVilla Theme - Session Notes

## Store Details
- **Store URL:** prm-herbovilla.myshopify.com
- **Theme ID:** 150645178542
- **Push command:** `shopify theme push --theme 150645178542 --store prm-herbovilla.myshopify.com --allow-live`
- **Push single file:** append `--only "sections/filename.liquid"`

---

## What Was Done (Sessions up to April 19, 2026)

### 1. About Us Page (`sections/page-template.liquid`)
- Made hero title text white (`color: #fff` on `.about-auto-hero__title`)
- Title: "25 Years of Healing. Rooted in Bhavnagar."

### 2. Featured Product Section (`sections/vedacold-featured.liquid`)
This section was heavily modified. Current state:

- **Images:** Replaced product catalog image with 4 direct asset images:
  - `assets/vedacold-box-front.png` (box front)
  - `assets/vedacold-strip-back.png` (strip back)
  - `assets/vedacold-box-back.png` (box back)
  - `assets/vedacold-strip-3d.png` (strip 3D view)
- **Thumbnail switcher:** 4 clickable thumbnails (62px) with JS at bottom of file
- **Removed:** "100% Ayurvedic" badge (both HTML and CSS deleted)
- **Herbs:** Shows all 22 herbs as compact pills in a card with leaf icon header and divider
- **Current sizing (final reverted state):**
  - Container: max-width 1100px, gap 50px
  - Padding: 60px 20px
  - Product image: max-width 400px
  - Title: 34px (Playfair Display)
  - Tagline: 15.5px
  - Description: 14.5px, line-height 1.65
  - Benefits gap: 8px, margin-bottom 20px
  - Benefit text: 14px
  - Price: 30px
  - Buttons: 14px, padding 12px 24px (add to cart) / 12px 20px (view details)

### 3. Hero Section (`sections/hero.liquid`)
- Fully responsive rewrite with modern CSS
- min-height: 68vh / 68dvh
- Uses `clamp()` throughout for fluid sizing
- 7 breakpoints: 375px, 576px, 768px landscape, 992px, 992px landscape, 1440px, 1920px
- `prefers-reduced-motion` support for accessibility

### 4. Collection Cards (`snippets/collection-card.liquid`)
- Icon + text box style cards with SVG icons
- Auto-assigns icon/color based on collection handle keywords
- 15 icon variants (shield, stomach, lungs, bone, sparkle, heart, strength, droplet, star, zap, baby, smile, plus-circle, droplets, leaf)

### 5. Shop by Goal Section (`sections/shop-by-goal.liquid`)
- Collections grid with configurable blocks
- Uses `collection-card` snippet for rendering

---

## Key Files
| File | Purpose |
|------|---------|
| `sections/vedacold-featured.liquid` | Featured product (VedaCold-CV 675) - most modified |
| `sections/hero.liquid` | Homepage hero banner - responsive rewrite |
| `sections/page-template.liquid` | About Us and other pages |
| `sections/shop-by-goal.liquid` | Shop by Health Goal grid |
| `snippets/collection-card.liquid` | Reusable collection card with SVG icons |
| `templates/index.json` | Homepage section order |
| `assets/vedacold-*.png` | 4 product images for featured section |

---

## Theme Colors & Fonts
- **Primary green:** #2D6A4F
- **Accent brown:** #8B5E3C
- **Cream background:** #FDF8F0
- **Headings:** Playfair Display (serif)
- **Body:** Inter (sans-serif)
- **Currency:** INR (₹)

---

## Notes
- All changes are pushed live to the store
- The featured product section went through multiple sizing iterations - current state is the "just right" version before any reduction
- Hero section is fully responsive across all device sizes and orientations
- Product handle for VedaCold: `vedacold-cv-675`

---

## Session: 2026-04-19 (mobile responsive pass)

### Primary fix
- **Hero mobile ordering**: on phones the right-column feature cards
  (Pure Herbal / Clinically Tested / No Side Effects / Expert
  Formulated) were landing ABOVE the hero headline because of
  `.hero__right { order: -1 }`. Flipped to content-first, cards-after.

### Responsive polish (15 commits pushed to GitHub one-by-one)
- `.gitignore` + initial assets (collection SVGs, vedacold PNGs)
- Hero: mobile ordering fix, tiny-screen + landscape + reduced-motion
- Social-proof: tighter mobile grid + <=360px fallback
- Shop by Goal cards: compact padding, smaller icons on phones
- VedaCold featured: full-width CTAs, tiny-screen scaling
- Footer: single column under 480px
- Newsletter: 48px tap targets
- Testimonials: viewport-edge bleed on mobile
- Announcement bar: xs font on narrow phones
- Product card: always-visible actions for touch
- Header: compacted icons for iPhone SE class
- Base: responsive section padding + container gutter

### Important: git vs live store divergence
- Remote `main` had an OLDER vedacold-featured.liquid (SVG placeholder,
  no thumbnail switcher) than what was running on the Shopify store.
- The newer thumbnail-switcher version from earlier sessions was never
  committed — so my git-side changes are against the older base.
- **Don't** blindly `shopify theme push` from this working tree —
  doing so would overwrite the newer in-store version with the older
  one-plus-my-mobile-polish. Push individual files instead, e.g.:
  `shopify theme push --only "sections/hero.liquid" --only "assets/theme.css"`.

---

## Session: 2026-04-22 (production-ready overhaul)

- **New theme ID**: `151479124142` (replaces older `150645178542`)
- **Push command**: `shopify theme push --store=prm-herbovilla.myshopify.com --theme=151479124142 --allow-live --nodelete`
- **Status as of this session end**: all code changes saved locally and
  committed to git; **NOT yet pushed to Shopify** — CLI auth token expired.
  Push blocked pending fresh device-code auth (tomorrow morning).

### Homepage (`templates/index.json`)
- New section order: hero → shop-by-goal → certifications → featured-collection
  → vedacold-featured → new-arrivals → herbs-uses → how-it-works →
  testimonials (renamed "Doctor's Reviews") → newsletter
- Removed: brand-mission, wellness/blog-posts, why-us, collection-list,
  hero stats bar
- `featured-collection` → 8 products, `show_secondary_image: true`
- `new-arrivals` → 8 products
- All 6 shop-by-goal blocks now reference real collection handles
- Added 6 `herbs-uses` category blocks with inline herb lists
- Replaced all 8 testimonials with Ayurvedic practitioner voices

### Vedacold Featured (`sections/vedacold-featured.liquid`)
- 4-image carousel (front / back / strip 3D / strip back) driven by JS
  thumb-click toggle with `is-active` class
- Removed "Coming Soon to Store" text + "100% Ayurvedic" badge
- CTA changed to "Order Now" → `/products/vedacold-cv-675`
- All 22 herbs shown inline in compact pill grid

### New sections & files
- **`sections/herbs-uses.liquid`** — new section, 6 category cards with
  SVG icons (immunity / digestive / respiratory / joint / skin / women),
  responsive grid (minmax 280px), hover lift effect
- **`prm-herbovilla-theme/layout/password.liquid`** — custom password-
  page layout (previously missing)

### Footer (`sections/footer.liquid`)
- Removed Quick Links column entirely + `link_col1`/`col1_title` schema
- Added hardcoded `contact@prmpharmaceuticals.com` + `0278 244 8087`
- 3-column structure: Brand (logo+desc+social+certs) /
  Customer Service (hardcoded contact + dynamic links) /
  Visit & Connect (address + Mon-Sat hours + email)

### About page (`sections/about-page.liquid` + `templates/page.about.json`)
- Major expansion: hero with 3 badges, stats bar
  (1999/2013/3,00,000+/85+/250+/28+), parent-brand comparison card,
  mission, values (4), 6-milestone timeline (**2013 highlighted**),
  leadership (Hemang + Dhyey Soni), Bhavnagar G.I.D.C. Plot 343
  manufacturing, 6-cert grid, CTA
- Value blocks: Purity First / Pharmaceutical-Grade / Classical & Clinical
  / Trusted by Professionals
- 8 feature blocks: WHO-GMP, ISO 9001:2015, AYUSH, FSSAI, State FDA,
  Heavy-Metal Tested, Contract-Farmed Herbs, Batch-Wise QC

### Product page (`sections/product-template.liquid`)
- **Image fix**: `.product-main-image` → `display:flex; padding:30px;
  border; bg #FDF8F0`; `img` → `object-fit: contain` (no more zoom)
- Thumbnails → 78px with padding + cream bg + contain fit
- **How to Use tab** — default 5-step fallback when no `usage_step` blocks
- **Shipping tab** — 4-card grid (Free Shipping / Delivery Timeline /
  COD / Returns) + tracking & quality notes + contact info

### Blog (`sections/blog-template.liquid`)
- 10 curated expert articles fall back when no admin articles exist
  (Johns Hopkins, Healthline, WHO)
- Categories: Ayurveda 101, Herbal Science, Superfoods, Digestion,
  Immunity, Research, Skin Care, Respiratory, Adaptogens, Skin & Detox
- Styled meta chips + source attribution badges

### New images copied to assets/
- `vedacold-cv-675-box-front.png` / `-box-back.png` / `-strip-3d.png` /
  `-strip-back.png` (also kept shorter-named duplicates referenced by
  vedacold-featured.liquid)

### Responsive breakpoints touched
All sections responsive at 992px (grid collapse), 768px (stack),
576px (single column + reduced padding), 480px (tiny-screen scale).
