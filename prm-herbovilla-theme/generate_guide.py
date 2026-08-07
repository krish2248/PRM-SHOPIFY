"""Generate Krish's instruction guide PDF for HerboVilla Shopify setup."""
from fpdf import FPDF
from datetime import date


GREEN = (45, 106, 79)        # #2D6A4F
DARK_GREEN = (27, 67, 50)    # #1B4332
BROWN = (139, 90, 43)        # warm brown
TEXT = (40, 40, 40)
MUTED = (110, 110, 110)
LIGHT_BG = (245, 245, 240)
CODE_BG = (240, 240, 235)
ACCENT = (180, 90, 40)


class GuidePDF(FPDF):
    def __init__(self):
        super().__init__(orientation="P", unit="mm", format="A4")
        self.set_auto_page_break(auto=True, margin=18)
        self.set_margins(left=18, top=18, right=18)
        self.alias_nb_pages()

    def header(self):
        if self.page_no() == 1:
            return
        self.set_font("Helvetica", "B", 9)
        self.set_text_color(*GREEN)
        self.cell(0, 8, "Krish's Instruction Guide  -  HerboVilla Shopify Setup",
                  border=0, align="L")
        self.set_text_color(*MUTED)
        self.set_font("Helvetica", "", 8)
        self.cell(0, 8, f"Page {self.page_no()} of {{nb}}", align="R")
        self.ln(10)
        self.set_draw_color(*GREEN)
        self.set_line_width(0.3)
        self.line(18, 22, 192, 22)
        self.ln(4)

    def footer(self):
        self.set_y(-14)
        self.set_font("Helvetica", "I", 7)
        self.set_text_color(*MUTED)
        self.cell(0, 5, "PRM HerboVilla  |  prm-herbovilla.myshopify.com", align="C")

    # ---------- helpers ----------
    def cover(self):
        self.add_page()
        self.set_fill_color(*DARK_GREEN)
        self.rect(0, 0, 210, 297, "F")

        # Decorative top band
        self.set_fill_color(*GREEN)
        self.rect(0, 90, 210, 80, "F")

        # Title block
        self.set_text_color(255, 255, 255)
        self.set_xy(0, 100)
        self.set_font("Helvetica", "B", 30)
        self.cell(210, 14, "KRISH'S", align="C")
        self.set_xy(0, 116)
        self.set_font("Helvetica", "B", 30)
        self.cell(210, 14, "INSTRUCTION GUIDE", align="C")

        self.set_xy(0, 138)
        self.set_font("Helvetica", "", 13)
        self.cell(210, 8, "HerboVilla Shopify - Step-by-Step Setup", align="C")

        # Subtitle / scope
        self.set_xy(0, 195)
        self.set_text_color(255, 255, 255)
        self.set_font("Helvetica", "B", 13)
        self.cell(210, 8, "Inside this guide:", align="C")
        self.ln(10)
        self.set_font("Helvetica", "", 12)
        items = [
            "1.  Razorpay Payment Gateway Setup",
            "2.  Nimbus Post Shipping Integration",
            "3.  Populating All Collections With Products",
        ]
        for item in items:
            self.set_x(0)
            self.cell(210, 8, item, align="C")
            self.ln(7)

        # Footer of cover
        self.set_xy(0, 270)
        self.set_font("Helvetica", "", 10)
        self.cell(210, 6, "PRM HerboVilla  -  Bhavnagar, Gujarat", align="C")
        self.ln(6)
        self.set_font("Helvetica", "I", 9)
        self.cell(210, 6, f"Prepared: {date.today().strftime('%B %Y')}", align="C")

    def chapter_title(self, num, title):
        self.add_page()
        # Header band
        self.set_fill_color(*GREEN)
        self.rect(0, 30, 210, 22, "F")

        self.set_xy(18, 33)
        self.set_text_color(255, 255, 255)
        self.set_font("Helvetica", "B", 11)
        self.cell(0, 6, f"PART {num}")

        self.set_xy(18, 40)
        self.set_font("Helvetica", "B", 18)
        self.cell(0, 8, title)

        self.ln(28)
        self.set_text_color(*TEXT)

    def h2(self, text):
        if self.get_y() > 250:
            self.add_page()
        self.ln(2)
        self.set_text_color(*DARK_GREEN)
        self.set_font("Helvetica", "B", 13)
        self.cell(0, 8, text, ln=1)
        self.set_draw_color(*GREEN)
        self.set_line_width(0.4)
        x = self.get_x()
        y = self.get_y()
        self.line(x, y, x + 30, y)
        self.ln(3)
        self.set_text_color(*TEXT)

    def h3(self, text):
        if self.get_y() > 255:
            self.add_page()
        self.ln(1)
        self.set_text_color(*BROWN)
        self.set_font("Helvetica", "B", 11)
        self.cell(0, 6, text, ln=1)
        self.set_text_color(*TEXT)
        self.ln(1)

    def body(self, text):
        self.set_font("Helvetica", "", 10.5)
        self.set_text_color(*TEXT)
        self.multi_cell(0, 5.6, text)
        self.ln(1)

    def bullet_list(self, items):
        self.set_font("Helvetica", "", 10.5)
        self.set_text_color(*TEXT)
        for item in items:
            if self.get_y() > 260:
                self.add_page()
            self.set_x(self.l_margin)
            self.cell(5, 5.6, "-", new_x="RIGHT", new_y="TOP")
            text_w = self.w - self.r_margin - self.get_x()
            self.multi_cell(text_w, 5.6, item)
        self.ln(1)

    def numbered_steps(self, steps):
        self.set_font("Helvetica", "", 10.5)
        self.set_text_color(*TEXT)
        for i, step in enumerate(steps, 1):
            if self.get_y() > 258:
                self.add_page()
            self.set_x(self.l_margin)
            self.set_font("Helvetica", "B", 10.5)
            self.set_text_color(*GREEN)
            self.cell(7, 5.6, f"{i}.", new_x="RIGHT", new_y="TOP")
            self.set_font("Helvetica", "", 10.5)
            self.set_text_color(*TEXT)
            text_w = self.w - self.r_margin - self.get_x()
            self.multi_cell(text_w, 5.6, step)
            self.ln(1)
        self.ln(1)

    def callout(self, label, text, color=None):
        if color is None:
            color = (255, 247, 230)
        if self.get_y() > 245:
            self.add_page()
        self.set_fill_color(*color)
        self.set_draw_color(*ACCENT)
        x = self.get_x()
        y = self.get_y()
        # Pre-calculate wrapped height
        self.set_font("Helvetica", "", 10)
        # Estimate
        text_lines = max(1, int(len(text) / 90) + text.count("\n") + 1)
        height = 8 + text_lines * 5
        self.set_line_width(0.3)
        self.rect(x, y, 174, height, "DF")
        # Label
        self.set_xy(x + 3, y + 2)
        self.set_text_color(*ACCENT)
        self.set_font("Helvetica", "B", 9)
        self.cell(50, 5, label.upper())
        # Body
        self.set_xy(x + 3, y + 7)
        self.set_text_color(*TEXT)
        self.set_font("Helvetica", "", 10)
        self.multi_cell(168, 5, text)
        self.set_y(y + height + 2)

    def code_block(self, text):
        if self.get_y() > 255:
            self.add_page()
        self.set_fill_color(*CODE_BG)
        self.set_draw_color(200, 200, 195)
        x = self.get_x()
        y = self.get_y()
        lines = text.split("\n")
        height = 4 + len(lines) * 4.5
        self.set_line_width(0.2)
        self.rect(x, y, 174, height, "DF")
        self.set_xy(x + 3, y + 2)
        self.set_font("Courier", "", 9)
        self.set_text_color(60, 60, 60)
        for line in lines:
            self.set_x(x + 3)
            self.cell(168, 4.5, line, ln=1)
        self.set_y(y + height + 2)
        self.set_text_color(*TEXT)


def build():
    pdf = GuidePDF()
    pdf.cover()

    # ---- TABLE OF CONTENTS ----
    pdf.add_page()
    pdf.set_text_color(*DARK_GREEN)
    pdf.set_font("Helvetica", "B", 22)
    pdf.cell(0, 12, "Table of Contents", ln=1)
    pdf.set_draw_color(*GREEN)
    pdf.set_line_width(0.5)
    pdf.line(18, pdf.get_y(), 80, pdf.get_y())
    pdf.ln(8)

    pdf.set_text_color(*TEXT)
    toc_items = [
        ("Part 1", "Razorpay Payment Gateway Setup", "3"),
        ("",       "  1.1  Create your Razorpay account",  ""),
        ("",       "  1.2  Complete KYC verification",     ""),
        ("",       "  1.3  Activate Razorpay in Shopify",  ""),
        ("",       "  1.4  Get API keys & test a payment", ""),
        ("",       "  1.5  Troubleshooting",               ""),
        ("Part 2", "Nimbus Post Shipping Integration",     ""),
        ("",       "  2.1  Create your Nimbus Post account", ""),
        ("",       "  2.2  KYC and wallet recharge",        ""),
        ("",       "  2.3  Install Nimbus Post for Shopify", ""),
        ("",       "  2.4  Configure shipping & pickup",    ""),
        ("",       "  2.5  Process your first order",       ""),
        ("Part 3", "Populating Collections with Products",  ""),
        ("",       "  3.1  Open the project folder",        ""),
        ("",       "  3.2  Generate a Shopify Admin API token", ""),
        ("",       "  3.3  Run the populate-collections.py script", ""),
        ("",       "  3.4  Verify in Shopify admin",        ""),
        ("",       "  3.5  Maintenance & re-runs",          ""),
    ]
    pdf.set_font("Helvetica", "", 11)
    for left, mid, _ in toc_items:
        if left:
            pdf.set_font("Helvetica", "B", 11)
            pdf.set_text_color(*GREEN)
            pdf.cell(20, 7, left)
        else:
            pdf.cell(20, 7, "")
        pdf.set_font("Helvetica", "", 11)
        pdf.set_text_color(*TEXT)
        pdf.cell(0, 7, mid, ln=1)

    # ---- PART 1: RAZORPAY ----
    pdf.chapter_title(1, "Razorpay Payment Gateway")

    pdf.body(
        "Razorpay is the payment gateway that will collect online payments on your "
        "HerboVilla store - UPI, credit/debit cards, net banking, wallets and EMI. "
        "It is a PCI-DSS Level 1 certified service, which is the highest security "
        "standard for handling card data. You do not need to manage any card details "
        "yourself - Razorpay handles all of that."
    )

    pdf.callout(
        "Before you begin",
        "Keep these documents ready:  PAN card (business or personal), Aadhaar card, "
        "cancelled cheque or bank passbook front page, GSTIN (if available), and your "
        "business registration / shop license."
    )

    pdf.h2("1.1  Create your Razorpay account")
    pdf.numbered_steps([
        "Open https://razorpay.com in your web browser.",
        "Click the 'Sign Up' button at the top right of the page.",
        "Enter your business email address and create a strong password.",
        "Verify the email - Razorpay will send you a confirmation link. Click it.",
        "When asked 'What kind of business?' choose 'Private Limited' or "
        "'Proprietorship' depending on how PRM HerboVilla is registered.",
        "Choose 'E-commerce / D2C' as your industry category.",
        "You are now in the Razorpay dashboard, but in TEST MODE. Real payments "
        "won't work yet until KYC is approved.",
    ])

    pdf.h2("1.2  Complete KYC verification")
    pdf.body(
        "KYC (Know Your Customer) is the verification step Razorpay needs before "
        "it can settle real money to your bank account."
    )
    pdf.numbered_steps([
        "From the Razorpay dashboard, click 'Account & Settings' on the left "
        "sidebar, then click 'Activate Account'.",
        "Fill in business details: legal name, brand name (HerboVilla), business "
        "type, registered address (Plot No.343, 1-A, Chitra GIDC, Bhavnagar 364004).",
        "Upload PAN card photo (clear, all corners visible).",
        "Upload Aadhaar (front and back) for the authorised signatory.",
        "Enter bank account details where you want settlements deposited. Upload a "
        "cancelled cheque or bank statement that shows the same account number.",
        "If you have a GSTIN, enter it here. If not, you can skip this for now and "
        "add it later.",
        "Click 'Submit for Activation'.",
    ])
    pdf.callout(
        "How long does it take?",
        "Razorpay usually approves KYC within 1-3 business days. You will receive an "
        "email when the account is live. Until then you can keep testing in test mode."
    )

    pdf.h2("1.3  Activate Razorpay in Shopify")
    pdf.body(
        "Shopify already has a built-in connector for Razorpay - you do not need to "
        "install any app."
    )
    pdf.numbered_steps([
        "Log in to your Shopify admin at https://prm-herbovilla.myshopify.com/admin",
        "From the left menu click 'Settings' (gear icon at the bottom).",
        "Click 'Payments'.",
        "Under 'Additional payment methods' click 'Choose alternative payment'.",
        "Type 'Razorpay' in the search box, then click 'Razorpay Secure (UPI, "
        "Cards, Wallets, NetBanking)'.",
        "Click 'Activate'.",
    ])

    pdf.h2("1.4  Get API keys & test a payment")
    pdf.numbered_steps([
        "Go back to the Razorpay dashboard (https://dashboard.razorpay.com).",
        "Click 'Account & Settings' on the left sidebar.",
        "Click 'API Keys'.",
        "Click 'Generate Key' (or 'Regenerate' if one already exists).",
        "Razorpay will show you a Key ID (starts with 'rzp_live_...') and a Key "
        "Secret. Copy BOTH - the Key Secret is shown only once.",
        "Switch back to Shopify's Razorpay activation screen.",
        "Paste the Key ID into the 'Key ID' field and the Key Secret into the "
        "'Key Secret' field.",
        "Click 'Activate Razorpay'.",
        "Place a small test order on your storefront (Rs. 1) using a real card or "
        "UPI to confirm everything works end to end.",
    ])

    pdf.h2("1.5  Troubleshooting")
    pdf.bullet_list([
        "If 'Activate' is greyed out in Shopify, your KYC is not yet approved by "
        "Razorpay - wait for the approval email and try again.",
        "If a test payment fails with 'Payment processing not enabled', check that "
        "you used the LIVE keys (rzp_live_...) and not the TEST keys (rzp_test_...).",
        "If settlements are not arriving in your bank, check Razorpay -> "
        "Settlements - cycle is usually T+2 (two business days after the order).",
        "Razorpay support: https://razorpay.com/support  |  support@razorpay.com",
    ])

    # ---- PART 2: NIMBUS POST ----
    pdf.chapter_title(2, "Nimbus Post Shipping Integration")

    pdf.body(
        "Nimbus Post is a shipping aggregator that connects you with multiple courier "
        "partners (Delhivery, Bluedart, DTDC, Ekart, XpressBees) through a single "
        "dashboard. You print one shipping label, and Nimbus picks the cheapest "
        "courier that serves the customer's pincode. They cover 27,000+ pincodes "
        "across India."
    )

    pdf.callout(
        "Before you begin",
        "Keep these documents ready:  GSTIN (recommended, not mandatory), PAN card, "
        "cancelled cheque, signature on a blank A4 page (for the rate contract), "
        "and a working email + phone number."
    )

    pdf.h2("2.1  Create your Nimbus Post account")
    pdf.numbered_steps([
        "Open https://nimbuspost.com in your web browser.",
        "Click 'Sign Up' at the top right.",
        "Enter your business name (PRM HerboVilla), email, mobile number and "
        "create a password.",
        "Verify your email and mobile via the OTP / link sent to you.",
        "When the welcome screen asks for your monthly shipment volume, give an "
        "honest estimate (this affects which rate slab you get).",
    ])

    pdf.h2("2.2  KYC and wallet recharge")
    pdf.body(
        "Unlike Razorpay (which collects from customers), Nimbus Post is prepaid - "
        "you load a wallet, and shipping charges get deducted as you book orders."
    )
    pdf.numbered_steps([
        "From the Nimbus dashboard, click 'Settings' -> 'KYC'.",
        "Upload PAN card, GSTIN certificate (if you have one) and a cancelled "
        "cheque.",
        "Add your business address (this becomes the default pickup address).",
        "Click 'Submit'. KYC approval is usually same-day.",
        "Now click 'Wallet' on the dashboard.",
        "Click 'Add Money' and recharge with at least Rs. 1,000 to start. UPI / "
        "card / netbanking are accepted.",
    ])
    pdf.callout(
        "Cost guideline",
        "A typical 500g shipment within India costs around Rs. 45-80 depending on "
        "zone. Cash-on-Delivery orders also have a 1.5% COD fee. Top up the wallet "
        "every few weeks based on your order volume."
    )

    pdf.h2("2.3  Install Nimbus Post for Shopify")
    pdf.numbered_steps([
        "From your Nimbus Post dashboard, click 'Channels' on the left menu.",
        "Click 'Add Channel' and choose 'Shopify' from the list of platforms.",
        "Enter your Shopify store URL: prm-herbovilla.myshopify.com",
        "Click 'Connect' - this will redirect you to Shopify to approve the app.",
        "On the Shopify approval screen, click 'Install app'.",
        "You'll be redirected back to Nimbus Post. The channel should now show "
        "as 'Connected' in green.",
    ])

    pdf.h2("2.4  Configure shipping & pickup")
    pdf.numbered_steps([
        "In Nimbus dashboard, go to 'Settings' -> 'Pickup Address'.",
        "Add your warehouse address (Plot No.343, 1-A, Chitra GIDC, Bhavnagar "
        "364004) and mark it as default.",
        "Go to 'Settings' -> 'Order Sync' and enable 'Auto-sync new orders from "
        "Shopify'. This means new orders appear in Nimbus automatically.",
        "Decide your preference: 'Lowest Cost' courier or 'Fastest Delivery' "
        "courier - set this in 'Settings' -> 'Courier Priority'.",
        "Optional: in Shopify admin go to Settings -> Shipping and Delivery and "
        "create a 'Free shipping above Rs. 400' rule that matches your storefront "
        "promise.",
    ])

    pdf.h2("2.5  Process your first order")
    pdf.numbered_steps([
        "When a customer places an order, it appears in Nimbus dashboard under "
        "'Orders' -> 'New' (within 1-2 minutes).",
        "Open the order, verify the address, and click 'Ship Now'.",
        "Nimbus will show you available couriers with their rates - pick one (or "
        "let auto-select based on your priority setting).",
        "Click 'Generate Label'. A PDF shipping label downloads.",
        "Print the label, paste it on the parcel.",
        "Click 'Schedule Pickup' - the courier will collect from your address.",
        "Tracking automatically syncs back to Shopify, and the customer receives "
        "tracking emails.",
    ])
    pdf.callout(
        "Need help?",
        "Nimbus support is responsive on chat from the dashboard, or email "
        "support@nimbuspost.com  |  Phone: +91-9220-413-148"
    )

    # ---- PART 3: COLLECTIONS ----
    pdf.chapter_title(3, "Populating Collections with Products")

    pdf.body(
        "Your Shopify store has empty collection pages (e.g. 'Diabetic Care', 'Joint "
        "Care', 'Immunity Boosters'). Each product needs to be assigned to one or "
        "more collections so it shows up on those pages. The script "
        "populate-collections.py automates this - it reads a JSON file with "
        "product-to-collection mappings and tags everything in one go."
    )

    pdf.callout(
        "What you'll need",
        "Python 3 installed on this computer (already present), the project folder "
        "open in a terminal, and a Shopify Admin API token (we'll create one in step 3.2)."
    )

    pdf.h2("3.1  Open the project folder")
    pdf.numbered_steps([
        "Press the Windows key, type 'cmd', and press Enter to open Command Prompt.",
        "Navigate to the project folder:",
    ])
    pdf.code_block(
        'cd "C:\\Users\\sonik\\Desktop\\last prm update\\HerboVilla Shopify\\prm-herbovilla-theme"'
    )
    pdf.body(
        "Confirm you're in the right place by typing 'dir populate-collections.py'. "
        "If you see the file listed, you're set."
    )

    pdf.h2("3.2  Generate a Shopify Admin API token")
    pdf.numbered_steps([
        "Log in to Shopify admin: https://prm-herbovilla.myshopify.com/admin",
        "Click 'Settings' (gear icon, bottom-left).",
        "Click 'Apps and sales channels'.",
        "Click 'Develop apps' (top right).",
        "If asked, click 'Allow custom app development' and confirm.",
        "Click 'Create an app'.",
        "App name: 'Collection Populator'. Click 'Create app'.",
        "On the new app page, click 'Configure Admin API scopes'.",
        "Tick these permissions:  read_products, write_products, read_collections, "
        "write_collections.",
        "Click 'Save'.",
        "Click the 'API credentials' tab.",
        "Click 'Install app' and confirm the install.",
        "Under 'Admin API access token', click 'Reveal token once'. Copy the token "
        "(starts with 'shpat_...'). Save it somewhere safe - you cannot see it again.",
    ])
    pdf.callout(
        "Keep it secret",
        "The shpat_... token gives full read/write access to your store's products. "
        "Do NOT paste it into chats, public docs, screenshots, or commit it to git."
    )

    pdf.h2("3.3  Run the populate-collections.py script")
    pdf.numbered_steps([
        "Open the file collection-product-mapping.json in a text editor (Notepad "
        "is fine) and verify the product-to-collection mapping looks correct.",
        "Back in the Command Prompt, set the token as an environment variable:",
    ])
    pdf.code_block("set SHOPIFY_ADMIN_TOKEN=shpat_your_token_here")
    pdf.numbered_steps([
        "Now run the script:",
    ])
    pdf.code_block("python populate-collections.py")
    pdf.body(
        "The script will print progress as it works:  for each product it will say "
        "'Adding <product> to <collection>... OK' or 'SKIPPED (already in)'. "
        "Expect it to take 1-3 minutes depending on how many products you have."
    )

    pdf.h2("3.4  Verify in Shopify admin")
    pdf.numbered_steps([
        "Open Shopify admin -> 'Products' -> 'Collections'.",
        "Click any collection (e.g. 'Diabetic Care').",
        "Scroll down to the 'Products' section - you should see the products that "
        "the script just added.",
        "Visit the storefront page (e.g. /collections/diabetic-care) and confirm "
        "products appear there too.",
    ])

    pdf.h2("3.5  Maintenance & re-runs")
    pdf.bullet_list([
        "When you add a new product to the store, also add it to "
        "collection-product-mapping.json and re-run the script.",
        "The script is safe to re-run - it skips products that are already in a "
        "collection, so you won't get duplicates.",
        "If you change a collection name or handle in Shopify, update the same name "
        "in the JSON file before re-running.",
        "If the token ever leaks, delete the custom app in Shopify admin and "
        "create a new one - this invalidates the old token immediately.",
    ])

    pdf.callout(
        "All done",
        "Once Razorpay is live, Nimbus Post is connected, and collections are "
        "populated, your HerboVilla store is fully operational. Place a real Rs. 1 "
        "test order yourself to confirm the entire flow:  add to cart -> checkout -> "
        "Razorpay payment -> Nimbus label generated -> tracking syncs back."
    )

    # ---- BACK PAGE ----
    pdf.add_page()
    pdf.set_text_color(*DARK_GREEN)
    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(0, 10, "Quick Reference", ln=1)
    pdf.set_draw_color(*GREEN)
    pdf.line(18, pdf.get_y(), 70, pdf.get_y())
    pdf.ln(6)

    pdf.set_text_color(*TEXT)
    pdf.set_font("Helvetica", "B", 11)
    pdf.cell(0, 7, "Important URLs", ln=1)
    pdf.set_font("Helvetica", "", 10.5)
    refs = [
        ("Shopify admin",        "https://prm-herbovilla.myshopify.com/admin"),
        ("Storefront",           "https://prm-herbovilla.myshopify.com"),
        ("Razorpay dashboard",   "https://dashboard.razorpay.com"),
        ("Razorpay support",     "https://razorpay.com/support"),
        ("Nimbus Post dashboard","https://app.nimbuspost.com"),
        ("Nimbus Post site",     "https://nimbuspost.com"),
    ]
    for label, url in refs:
        pdf.set_x(pdf.l_margin)
        pdf.set_font("Helvetica", "B", 10.5)
        pdf.cell(45, 6, label + ":", new_x="RIGHT", new_y="TOP")
        pdf.set_font("Helvetica", "", 10.5)
        pdf.cell(0, 6, url, new_x="LMARGIN", new_y="NEXT")

    pdf.ln(4)
    pdf.set_font("Helvetica", "B", 11)
    pdf.cell(0, 7, "Business Details (for forms)", ln=1)
    pdf.set_font("Helvetica", "", 10.5)
    biz = [
        ("Business name",  "PRM Pharmaceuticals (HerboVilla division)"),
        ("Address",        "Plot No.343, 1-A, Chitra GIDC, Bhavnagar, Gujarat 364004"),
        ("Email",          "contact@prmpharmaceuticals.com"),
        ("Phone",          "+91-9227928075"),
    ]
    for label, val in biz:
        pdf.set_x(pdf.l_margin)
        pdf.set_font("Helvetica", "B", 10.5)
        pdf.cell(35, 6, label + ":", new_x="RIGHT", new_y="TOP")
        pdf.set_font("Helvetica", "", 10.5)
        text_w = pdf.w - pdf.r_margin - pdf.get_x()
        pdf.multi_cell(text_w, 6, val)

    pdf.ln(4)
    pdf.set_font("Helvetica", "B", 11)
    pdf.cell(0, 7, "Order to follow", ln=1)
    pdf.set_font("Helvetica", "", 10.5)
    pdf.multi_cell(
        0, 5.6,
        "Do them in this order so each step is testable on its own:\n"
        "  1.  Razorpay first (so you can take payments).\n"
        "  2.  Nimbus Post next (so payments-in have a fulfillment path).\n"
        "  3.  Collections last (cosmetic merchandising - the store works without it)."
    )

    pdf.ln(8)
    pdf.set_text_color(*MUTED)
    pdf.set_font("Helvetica", "I", 9)
    pdf.cell(0, 5, "End of guide.", ln=1)

    output = "Krish's instruction guide.pdf"
    pdf.output(output)
    print(f"Wrote {output}")


if __name__ == "__main__":
    build()
