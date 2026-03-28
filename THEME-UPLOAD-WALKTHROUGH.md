# PRM HerboVilla Theme - Upload & Setup Walkthrough

Complete step-by-step guide to upload your theme to Shopify and get your store live.

---

## Part 1: Upload the Theme

### Step 1: Access Shopify Admin
1. Open your browser and go to: `https://prm-herbovilla.myshopify.com/admin`
2. Log in with your Shopify credentials

### Step 2: Navigate to Themes
1. In the left sidebar, click **Online Store**
2. Click **Themes**
3. You'll see your current theme (usually Dawn or a default theme)

### Step 3: Upload the Theme ZIP
1. Scroll down to **Theme library** section
2. Click the **Add theme** button
3. Select **Upload ZIP file**
4. Click **Choose file** and select: `prm-herbovilla-theme.zip`
5. Wait for the upload to complete (usually 1-2 minutes)
6. The theme will appear in your Theme library as "PRM HerboVilla Theme"

### Step 4: Preview Before Publishing
1. Click **Actions** next to the uploaded theme
2. Select **Preview**
3. Browse through your store to check:
   - Homepage sections display correctly
   - Products show with images
   - Navigation works
   - Mobile view looks good (resize browser or use mobile device)

### Step 5: Publish the Theme
1. If preview looks good, click **Actions** again
2. Select **Publish**
3. Confirm by clicking **Publish** in the popup
4. Your new theme is now LIVE!

---

## Part 2: Upload Your Logo

### Step 1: Access Theme Customizer
1. Click **Customize** next to your published theme
2. This opens the Theme Editor

### Step 2: Upload Logo
1. Click the **gear icon** (Theme settings) in the left sidebar
2. Click **Logo**
3. Click **Select image**
4. Upload your logo file: `Prm Logo.jpg`
5. Set recommended size: 200-300px width
6. Click **Save** in the top right corner

### Step 3: Set Favicon (Optional)
1. Still in Theme settings, scroll to **Favicon**
2. Upload a square version of your logo (recommended: 32x32 or 64x64 pixels)
3. Click **Save**

---

## Part 3: Create Pages in Shopify

Your theme includes templates for these pages. Create them in Shopify admin:

### Required Pages to Create

#### About Us Page
1. Go to **Online Store → Pages**
2. Click **Add page**
3. **Title**: About Us
4. **Content**: Leave empty (the template handles it)
5. **Theme template**: Select `page.about`
6. Click **Save**

#### FAQ Page
1. Click **Add page**
2. **Title**: FAQ
3. **Theme template**: Select `page.faq`
4. Click **Save**

#### Contact Page
1. Click **Add page**
2. **Title**: Contact Us
3. **Theme template**: Select `page.contact`
4. Click **Save**

#### Shipping Policy Page
1. Click **Add page**
2. **Title**: Shipping Policy
3. **Theme template**: Select `page.shipping-policy`
4. Click **Save**

#### Refund Policy Page
1. Click **Add page**
2. **Title**: Refund Policy
3. **Theme template**: Select `page.refund-policy`
4. Click **Save**

#### Privacy Policy Page
1. Click **Add page**
2. **Title**: Privacy Policy
3. **Theme template**: Select `page.privacy-policy`
4. Click **Save**

#### Terms of Service Page
1. Click **Add page**
2. **Title**: Terms of Service
3. **Theme template**: Select `page.terms-of-service`
4. Click **Save**

---

## Part 4: Set Up Navigation Menus

### Main Menu (Header)
1. Go to **Online Store → Navigation**
2. Click **Main menu**
3. Set up these links:
   ```
   Home → /
   Shop → /collections/all
     ├── All Products → /collections/all
     ├── Best Sellers → /collections/best-sellers
     ├── Immunity → /collections/immunity-boosters
     ├── Digestive Health → /collections/digestive-health
     ├── Hair & Skin → /collections/hair-skin-care
     └── Joint Care → /collections/joint-pain-relief
   About → /pages/about-us
   Blog → /blogs/news
   Contact → /pages/contact-us
   ```
4. Click **Save menu**

### Footer Menu
1. Click **Add menu**
2. Name: Footer menu
3. Add these links:
   ```
   About Us → /pages/about-us
   FAQ → /pages/faq
   Contact → /pages/contact-us
   Shipping Policy → /pages/shipping-policy
   Refund Policy → /pages/refund-policy
   Privacy Policy → /pages/privacy-policy
   Terms of Service → /pages/terms-of-service
   ```
4. Click **Save menu**

---

## Part 5: Configure Theme Settings

### Access Theme Customizer
1. Go to **Online Store → Themes**
2. Click **Customize** on your published theme

### Configure Header
1. Click on the **Header** section
2. Select your logo
3. Enable sticky header (recommended)
4. Set announcement bar text
5. Click **Save**

### Configure Homepage Sections
1. **Hero Section**: Upload a hero image, set headline and button text
2. **Social Proof**: Customize trust badges and numbers
3. **Shop by Goal**: Select your collections
4. **Featured Products**: Select a collection to display
5. **Testimonials**: Add customer reviews
6. **Newsletter**: Customize signup text

### Configure Footer
1. Click on **Footer** section
2. Enter contact information
3. Add social media links (Facebook, Instagram, LinkedIn)
4. Select footer menu
5. Add payment icons

### Save All Changes
1. Click **Save** in the top right corner
2. Click **Exit** to return to admin

---

## Part 6: Create Collections

Refer to the `COLLECTION-SETUP-GUIDE.md` file for detailed instructions on:
- Creating collections
- Organizing your 44 products
- Adding collection images
- Setting up automated collections

Quick Summary:
1. Go to **Products → Collections**
2. Click **Create collection**
3. Create these collections:
   - Immunity Boosters
   - Digestive Health
   - Hair & Skin Care
   - Joint & Pain Relief
   - Women's Health
   - Men's Health
   - Best Sellers
   - New Arrivals
   - All Products

---

## Part 7: Final Checklist

Before going live, verify:

### Design & Branding
- [ ] Logo uploaded and displays correctly
- [ ] Favicon set
- [ ] Brand colors appear correctly
- [ ] Fonts load properly

### Navigation
- [ ] Main menu links work
- [ ] Footer menu links work
- [ ] Mobile menu opens and closes
- [ ] All pages are accessible

### Products
- [ ] Products display with images
- [ ] Prices show in ₹ (INR)
- [ ] Add to cart works
- [ ] Product pages load correctly

### Pages
- [ ] Homepage sections load
- [ ] About page displays
- [ ] Contact page shows form
- [ ] Policy pages are accessible

### Checkout
- [ ] Cart page works
- [ ] Checkout process completes
- [ ] Payment methods configured

### Mobile
- [ ] Site is responsive on mobile
- [ ] Touch interactions work
- [ ] Images load properly
- [ ] Text is readable

---

## Troubleshooting

### Theme doesn't appear after upload
- Clear browser cache and refresh
- Try a different browser
- Re-upload the ZIP file

### Images not showing
- Ensure products have images uploaded
- Check image file sizes (keep under 20MB)
- Verify image formats (JPG, PNG, WebP)

### Sections not displaying
- Go to Theme Customizer
- Ensure sections are added to the page
- Check section settings are configured

### Mobile menu not working
- Clear browser cache
- Check for JavaScript errors (browser console)
- Ensure theme.js is loaded

### Need more help?
- Email: contact@prmpharmaceuticals.com
- Phone: +91-9227928075

---

## Quick Links

- Shopify Admin: https://prm-herbovilla.myshopify.com/admin
- Theme Customizer: https://prm-herbovilla.myshopify.com/admin/themes/current/editor
- Products: https://prm-herbovilla.myshopify.com/admin/products
- Collections: https://prm-herbovilla.myshopify.com/admin/collections
- Pages: https://prm-herbovilla.myshopify.com/admin/pages
- Navigation: https://prm-herbovilla.myshopify.com/admin/menus

---

**Congratulations!** Your PRM HerboVilla theme is now set up and ready to serve customers!
