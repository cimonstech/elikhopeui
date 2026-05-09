"""
Patch EliKhope static HTML: branding, shared logo, sidebars, headers, footers, links.
Run: python scripts/elikhope_patch.py   (from repo root)
"""
from __future__ import annotations

import hashlib
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

MARK = "/elikhope_farms_marketing_pages"
AUTH = "/Authentication_Pages"
CUST = "/Customer_Dashboard_Pages"
ADMIN = "/Admin_Dashboard_Pages"
SHOP = "/E-Commerce_Shop_UI%20Pages"
ASSET_LOGO = "/assets/elilogo.png"
_AP = "/assets"
_PD = f"{_AP}/products"
# Shop catalogue: use only files in /assets/products/
PD_BEEF = f"{_PD}/beef.jpg"
PD_CHICKEN = f"{_PD}/fresh-chicken-meat.jpg"
PD_GOAT = f"{_PD}/fresh-goat.jpg"
PD_RIBS = f"{_PD}/ribs.jpg"
PD_SPECIAL = f"{_PD}/special-cuts.jpg"
PD_TBONE = f"{_PD}/t-bone.jpg"

# Editorial / hero / non-grid imagery (under /assets).
ASSET_MEAT_COLD_ROOM = f"{_AP}/meat-in-cold-room.jpg"
ASSET_MEAT_SMILING = PD_BEEF
ASSET_MEAT_COLD_STORAGE = f"{_AP}/Butcher-in-Cold-Storage-Room.jpg"
ASSET_MEAT_WEIGHING = f"{_AP}/butcher-weighing-meat.jpg"
ASSET_MEAT_BUTCHERY = f"{_AP}/butchers-in-butchery.jpg"
ASSET_GOAT = PD_GOAT
ASSET_CHICKEN = PD_CHICKEN
ASSET_SPECIAL_CUTS = PD_SPECIAL
ASSET_PERSON = f"{_AP}/person.jpg"
ASSET_PERSON_BUTCHER = ASSET_PERSON
ASSET_PERSON_CUTTING = f"{_AP}/african-male-cutting-meat.jpg"

AUTH_CUSTOMER_AUTH_HERO_IMG = f"{_AP}/butcher-smiling-with-beef.jpg"
AUTH_ADMIN_AUTH_HERO_IMG = ASSET_MEAT_COLD_STORAGE

_IMG_REMOTE_SRC_RE = re.compile(
    r'<img(\s[^>]*?)\bsrc="(https://(?:lh3\.googleusercontent\.com|images\.unsplash\.com)[^"]+)"([^>]*?)>',
    re.IGNORECASE | re.DOTALL,
)
_PEOPLE_CONTEXT_RE = re.compile(
    r"\b(butcher|chef|farmer|team|staff|worker|portrait|headshot|master\s+butcher)\b",
    re.IGNORECASE,
)


def _skip_remote_img_replace(inner: str) -> bool:
    """Leave map / location previews alone (not a product photo)."""
    low = inner.lower()
    if "data-location=" in low:
        return True
    if "map view" in low or "geographic sales map" in low:
        return True
    if "map visualization" in low or "digital map" in low:
        return True
    if re.search(r'data-alt="[^"]*?\bmap\b', low) and "profile" not in low:
        return True
    if re.search(r'alt="[^"]*?\bmap\b', low) and "profile" not in low:
        return True
    if "delivery route" in low and "map" in low:
        return True
    return False


def _img_context_is_people(inner: str) -> bool:
    low = inner.lower()
    # "butcher block" / paper are product-styling props, not portraits.
    if "butcher block" in low or "butcher paper" in low:
        return False
    if _PEOPLE_CONTEXT_RE.search(low):
        return True
    if "headshot" in low or "portrait" in low:
        return True
    if "profile" in low and "map" not in low:
        return True
    if "rounded-full" in low and (
        "h-10 w-10" in low or "h-8 w-8" in low or "w-8 h-8" in low or "w-10 h-10" in low
    ):
        return True
    return False


def _food_asset_from_alt_class(inner: str) -> str | None:
    """Pick a meat/poultry asset from editorial alt text when obvious."""
    low = inner.lower()
    if "chicken" in low or "poultry" in low or "drumstick" in low or "thighs" in low:
        return ASSET_CHICKEN
    if "goat" in low or "chevon" in low:
        return ASSET_GOAT
    if "lamb" in low or "crown roast" in low or "tomahawk" in low or "porterhouse" in low:
        return ASSET_SPECIAL_CUTS
    if "wagyu" in low:
        return PD_TBONE
    if "beef" in low or "steak" in low or "ribeye" in low or "brisket" in low or "fillet" in low or "tenderloin" in low:
        return PD_BEEF
    return None


def patch_remote_cdn_images_to_local(html: str) -> str:
    """Swap unreliable Google/Unsplash CDN <img> sources to /assets for public pages."""
    meat_pool = (
        PD_BEEF,
        PD_TBONE,
        PD_RIBS,
        PD_GOAT,
        PD_CHICKEN,
        PD_SPECIAL,
        ASSET_MEAT_COLD_ROOM,
        ASSET_MEAT_BUTCHERY,
    )
    people_pool = (
        ASSET_PERSON,
        ASSET_PERSON_CUTTING,
        ASSET_MEAT_BUTCHERY,
    )

    def repl(m: re.Match[str]) -> str:
        before, url, after = m.group(1), m.group(2), m.group(3)
        inner = before + after
        if _skip_remote_img_replace(inner):
            return m.group(0)
        food = _food_asset_from_alt_class(inner)
        if food is not None:
            pick = food
        elif _img_context_is_people(inner):
            idx = int(hashlib.md5(url.encode(), usedforsecurity=False).hexdigest(), 16) % len(people_pool)
            pick = people_pool[idx]
        else:
            idx = int(hashlib.md5(url.encode(), usedforsecurity=False).hexdigest(), 16) % len(meat_pool)
            pick = meat_pool[idx]
        return f'<img{before}src="{pick}"{after}>'

    return _IMG_REMOTE_SRC_RE.sub(repl, html)

U = {
    "home": f"{MARK}/elikhope_farms_home_page/code.html",
    "about": f"{MARK}/elikhope_farms_about_us/code.html",
    "categories": f"{MARK}/elikhope_farms_shop_all_meat/code.html",
    "quality": f"{MARK}/elikhope_farms_quality_standards/code.html",
    "gallery": f"{MARK}/elikhope_farms_visual_gallery/code.html",
    "blog": f"{MARK}/elikhope_farms_meat_preparation_farm_news/code.html",
    "help": f"{MARK}/elikhope_farms_help_center/code.html",
    "contact": f"{MARK}/elikhope_farms_contact_us/code.html",
    "login": f"{AUTH}/login_elikhope_farms/code.html",
    "register": f"{AUTH}/create_account_elikhope_farms/code.html",
    "forgot": f"{AUTH}/forgot_password_elikhope_farms/code.html",
    "otp": f"{AUTH}/email_verification_elikhope_farms/code.html",
    "verified": f"{AUTH}/success_elikhope_farms/code.html",
    "admin_login": f"{AUTH}/admin_login_elikhope_farms/code.html",
    "shop_home": f"{SHOP}/elikhope_farms_browse_products/code.html",
    "plp": f"{SHOP}/elikhope_farms_browse_products/code.html",
    "categories_hub": f"{MARK}/elikhope_farms_all_categories/code.html",
    "cat_beef": f"{SHOP}/category_beef_elikhope_farms/code.html",
    "cat_goat": f"{SHOP}/category_goat_elikhope_farms/code.html",
    "cat_chicken": f"{SHOP}/category_chicken_elikhope_farms/code.html",
    "cat_special": f"{SHOP}/category_special_elikhope_farms/code.html",
    "search": f"{SHOP}/elikhope_farms_search_results/code.html",
    "pdp": f"{SHOP}/elikhope_farms_product_detail/code.html",
    "cart": f"{SHOP}/elikhope_farms_shopping_cart/code.html",
    "checkout_delivery": f"{SHOP}/checkout_delivery_information_elikhope_farms/code.html",
    "checkout_pay": f"{SHOP}/checkout_payment_elikhope_farms/code.html",
    "checkout_review": f"{SHOP}/checkout_order_review_elikhope_farms/code.html",
    "order_success": f"{SHOP}/elikhope_farms_order_success/code.html",
    "track_guest": f"{SHOP}/elikhope_farms_track_order/code.html",
    "dash": f"{CUST}/dashboard_overview_elikhope_farms/code.html",
    "orders": f"{CUST}/my_orders_elikhope_farms/code.html",
    "track_dash": f"{CUST}/track_your_delivery_elikhope_farms/code.html",
    "wishlist": f"{CUST}/my_wishlist_elikhope_farms/code.html",
    "addresses": f"{CUST}/manage_addresses_elikhope_farms/code.html",
    "notif": f"{CUST}/notifications_elikhope_farms/code.html",
    "recent": f"{CUST}/recent_purchases_elikhope_farms/code.html",
    "settings_c": f"{CUST}/account_settings_elikhope_farms/code.html",
    "adm_dash": f"{ADMIN}/admin_dashboard_overview_elikhope_farms/code.html",
    "adm_orders": f"{ADMIN}/orders_management_elikhope_farms_admin/code.html",
    "adm_products": f"{ADMIN}/product_management_elikhope_farms_admin/code.html",
    "adm_inv": f"{ADMIN}/inventory_management_elikhope_farms_admin/code.html",
    "adm_deliver": f"{ADMIN}/delivery_management_elikhope_farms_admin/code.html",
    "adm_cust": f"{ADMIN}/customer_management_elikhope_farms_admin/code.html",
    "adm_promo": f"{ADMIN}/promotions_campaigns_elikhope_farms_admin/code.html",
    "adm_cms": f"{ADMIN}/content_management_elikhope_farms_admin/code.html",
    "adm_hero": f"{ADMIN}/homepage_hero_management_admin_cms/code.html",
    "adm_analytics": f"{ADMIN}/analytics_business_intelligence_elikhope_farms_admin/code.html",
    "adm_support": f"{ADMIN}/customer_support_elikhope_farms_admin/code.html",
    "adm_settings": f"{ADMIN}/admin_settings_elikhope_farms_admin/code.html",
    "adm_pay": f"{ADMIN}/payment_settings_elikhope_farms_admin/code.html",
    "adm_zones": f"{ADMIN}/delivery_zones_elikhope_farms_admin/code.html",
    "adm_staff": f"{ADMIN}/staff_permissions_elikhope_farms_admin/code.html",
}

ADMIN_SIDEBAR_RE = re.compile(
    r"(?:<!--[^\n]*-->\s*)?<(?:aside|nav)(?=[^>]*\bw-64\b)(?=[^>]*\bfixed\b)(?=[^>]*\bleft-0\b)[^>]*>[\s\S]*?</(?:aside|nav)>",
    re.IGNORECASE,
)

CUSTOMER_SIDEBAR_RE = re.compile(
    r"<!-- SideNavBar[^-][^\n]*-->[\s\S]*?</aside>",
    re.IGNORECASE,
)

CUSTOMER_SIDEBAR_ALT_RE = re.compile(
    r"<!--[^\n]*Sidebar[^\n]*-->\s*<aside[^>]*\bw-64\b[^>]*\bfixed\b[^>]*\bleft-0[\s\S]*?</aside>",
    re.IGNORECASE,
)

CUST_HEADER_RE = re.compile(
    r'(?:<!-- TopNavBar[^\n]*-->\s*)?<header class="fixed top-0 right-0[^"]*(?:w-\[calc\(100%-16rem\)\]|md:w-\[calc\(100%-16rem\)\])[\s\S]*?</header>',
    re.IGNORECASE,
)

CUSTOMER_HEADER_ALT_RE = re.compile(
    r"(?:<!-- TopNavBar[^\n]*-->\s*)?<header[^>]*\bsticky\b[\s\S]*?</header>",
    re.IGNORECASE,
)

BRAND_SUBSTS = [
    ("Artisanal Butcher | Enterprise Admin", "EliKhope Farms | Enterprise Admin"),
    ("Customer Support Management | Artisanal Butcher", "Customer Support | EliKhope Farms Admin"),
    ("Customer CRM | Artisanal Butcher", "Customer CRM | EliKhope Farms Admin"),
    ("Promotions Management | Artisanal Butcher", "Promotions | EliKhope Farms Admin"),
    ("Inventory Management | Artisanal Butcher", "Inventory | EliKhope Farms Admin"),
    ("Artisanal Butcher</title>", "EliKhope Farms</title>"),
    (" | Artisanal Butcher</title>", " | EliKhope Farms Admin</title>"),
    ("Artisanal Butcher</h1>", "EliKhope Farms</h1>"),
    ('class="text-h4 font-h4 text-primary-fixed dark:text-primary">Artisanal Butcher</h1>',
     'class="text-h4 font-h4 text-primary-fixed dark:text-primary">EliKhope Farms</h1>'),
    ('font-h4 text-h4 text-primary-fixed dark:text-primary">Artisanal Butcher</h1>',
     'font-h4 text-h4 text-primary-fixed dark:text-primary">EliKhope Farms</h1>'),
    ("Premium Butcheries", "Farm-to-consumer delivery"),
    ("The Butcher's Table", "Chef's table bundle"),
    ("Artisanal Sausages (Pack of 12)", "Mixed sausage pack (12 pcs)"),
    ("Artisanal Lamb Chops", "Premium lamb chops"),
    ("Artisanal Heritage Lamb Chops", "Heritage lamb chops"),
    ("Artisanal Sea Salt Rub", "House spice rub"),
    ("Premium Butcher Experience", "EliKhope premium delivery"),
    ("The Artisanal Promise", "The EliKhope promise"),
    ("Notify Butchery Manager", "Notify operations manager"),
    ("Butcher Chat Active", "Support chat active"),
    ("Talk to our Master Butcher", "Talk to customer care"),
    ("John D. Butcher", "John D. Mensah"),
    ("Kenyan pastures", "Ghana partner farms"),
    ("Artisanal Cured Meats Box", "Premium cured meats box"),
    ("Artisanal Cut", "Chef's choice cut"),
    ("Artisanal Butchery", "On-site butchery"),
    ("join our community of artisanal meat enthusiasts",
     "join EliKhope Farms for premium, hygienic meat delivery"),
    # Ghana localization (locations, phones, names, placeholders)
    ("Highlands Estate, NY 10522", "Akuse, Eastern Region, Ghana"),
    ("42 Verdant Valley Way,<br/>Highlands Estate, NY 10522", "Akuse, Eastern Region, Ghana"),
    ("42 Verdant Valley Way,", "Akuse, Eastern Region, Ghana"),
    ("NY 10522", "Eastern Region, Ghana"),
    ("+1 (888) 555-FARMS", "+233 (0) 30 555 0123"),
    ("+1 (888) 555-0123", "+233 (0) 20 555 0123"),
    ("+1 (888) 999-FAST", "+233 (0) 55 999 0123"),
    ("+1 (555) 000-0000", "+233 (0) 24 000 0000"),
    ("+1 (555) 000-0000", "+233 (0) 24 000 0000"),
    ("(555) 000-0000", "(0) 24 000 0000"),
    ("name@example.com", "batista@elikhopefarms.com"),
    ("john@example.com", "batista@elikhopefarms.com"),
    ("John Doe", "Batista Cimons"),
    ("James Wilson", "Kelvin Yao"),
    ("Marcus Thorne", "Kwame Mensah"),
    ("Alex Lawson", "Batista Cimons"),
    ("/assets/elikhope-logo.svg", "/assets/elilogo.png"),
]


def apply_brand(html: str) -> str:
    for old, new in BRAND_SUBSTS:
        html = html.replace(old, new)
    # Normalize any remaining non-Ghana phone formats.
    html = re.sub(r"\+1\s*\(\d{3}\)\s*\d{3}-\d{4}", "+233 (0) 24 000 0000", html)
    html = re.sub(r"\+27\s*", "+233 ", html)
    html = re.sub(
        r"<title>([^<]*)\|\s*Artisanal Butcher</title>",
        r"<title>\1 | EliKhope Farms Admin</title>",
        html,
        flags=re.IGNORECASE,
    )
    return html


def apply_currency_ghs(html: str) -> str:
    # Convert displayed USD-style prices to Ghana cedi across the static prototype.
    # Only replace "$" when it is clearly used as a currency prefix (e.g. $45, $ 45.00).
    html = re.sub(r"(?<![A-Za-z0-9])\$\s*(?=\d)", "GHS ", html)
    html = re.sub(r"\bUSD\b", "GHS", html, flags=re.IGNORECASE)
    html = re.sub(r"\bUS\$\b", "GHS", html, flags=re.IGNORECASE)
    return html


FONTS_LINK = (
    'https://fonts.googleapis.com/css2?'
    'family=Plus+Jakarta+Sans:wght@400;600;700;800&'
    'family=Inter:wght@400;500;600;700&display=swap'
)

FONTS_STYLE = """<style id="elikhope-fonts">
  body, button, input, textarea, select { font-family: 'Inter', ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, Arial, sans-serif; }
  h1, h2, h3, h4, h5, h6 { font-family: 'Plus Jakarta Sans', ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, Arial, sans-serif; }
  .font-h1,.font-h2,.font-h3,.font-h4,.font-price-lg { font-family: 'Plus Jakarta Sans', ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, Arial, sans-serif !important; }
  .font-body-sm,.font-body-md,.font-body-lg,.font-label-caps { font-family: 'Inter', ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, Arial, sans-serif !important; }
</style>"""

RESPONSIVE_STYLE_ALL = """<style id="elikhope-responsive-v2">
/* EliKhope Farms — comprehensive mobile responsiveness pass */
/* Product listing cards: ~30% smaller than global price-lg (70% scale) */
.ek-product-card .ek-product-price,
.ek-product-card .font-price-lg.text-price-lg.text-primary {
  font-size: 19.6px !important;
  line-height: 1.15 !important;
  white-space: nowrap !important;
}
/* PDP hero price: same ~70% scale as cards (vs default 28px price-lg) */
.ek-pdp-hero-price {
  font-size: 19.6px !important;
  line-height: 1.15 !important;
}
@media (max-width: 1023px) {
  /* Generic tightened horizontal margin where Tailwind used the desktop token */
  .px-margin-desktop { padding-left: 16px !important; padding-right: 16px !important; }
  .pl-margin-desktop { padding-left: 16px !important; }
  .pr-margin-desktop { padding-right: 16px !important; }
  .mx-margin-desktop { margin-left: 16px !important; margin-right: 16px !important; }
}
@media (max-width: 640px) {
  /* ---------- Typography ---------- */
  h1, .text-h1, .font-h1 { font-size: 30px !important; line-height: 1.15 !important; letter-spacing: -0.02em !important; }
  h2, .text-h2, .font-h2 { font-size: 24px !important; line-height: 1.2 !important; }
  h3, .text-h3, .font-h3 { font-size: 20px !important; line-height: 1.25 !important; }
  h4, .text-h4, .font-h4 { font-size: 17px !important; line-height: 1.3 !important; }
  .text-body-lg, .font-body-lg { font-size: 15px !important; line-height: 1.55 !important; }
  .text-body-md, .font-body-md { font-size: 14.5px !important; line-height: 1.55 !important; }
  .text-price-lg, .font-price-lg { font-size: 22px !important; }
  .ek-product-card .ek-product-price,
  .ek-product-card .font-price-lg.text-price-lg.text-primary {
    font-size: 15.4px !important;
  }
  .ek-pdp-hero-price {
    font-size: 15.4px !important;
  }
  /* Some Stitch designs use raw Tailwind sizes; soften the very largest */
  .text-5xl, .text-6xl { font-size: 28px !important; line-height: 1.15 !important; }
  .text-4xl { font-size: 24px !important; line-height: 1.2 !important; }
  .text-3xl { font-size: 20px !important; }
  .text-2xl { font-size: 18px !important; }
  .text-xl { font-size: 16px !important; }
  /* Cap absurd arbitrary icon sizes */
  [class*="text-[120px]"] { font-size: 72px !important; }
  [class*="text-[96px]"] { font-size: 56px !important; }

  /* ---------- Section spacing ---------- */
  .py-stack-lg { padding-top: 32px !important; padding-bottom: 32px !important; }
  .pt-stack-lg { padding-top: 32px !important; }
  .pb-stack-lg { padding-bottom: 32px !important; }
  .my-stack-lg { margin-top: 24px !important; margin-bottom: 24px !important; }
  .mt-stack-lg { margin-top: 24px !important; }
  .mb-stack-lg { margin-bottom: 24px !important; }
  .py-stack-md { padding-top: 20px !important; padding-bottom: 20px !important; }
  .my-stack-md { margin-top: 16px !important; margin-bottom: 16px !important; }
  .mb-stack-md { margin-bottom: 16px !important; }
  .gap-gutter { gap: 16px !important; }
  .gap-stack-lg { gap: 20px !important; }
  .gap-stack-md { gap: 16px !important; }

  /* ---------- Card / container paddings ---------- */
  .p-stack-lg { padding: 20px !important; }
  .p-stack-md { padding: 14px !important; }
  .p-8 { padding: 16px !important; }
  .p-6 { padding: 14px !important; }
  .px-8 { padding-left: 16px !important; padding-right: 16px !important; }
  .px-10 { padding-left: 18px !important; padding-right: 18px !important; }
  .px-12 { padding-left: 18px !important; padding-right: 18px !important; }
  .py-12 { padding-top: 28px !important; padding-bottom: 28px !important; }
  .py-16 { padding-top: 32px !important; padding-bottom: 32px !important; }
  .py-20, .py-24 { padding-top: 36px !important; padding-bottom: 36px !important; }

  /* Rounded big banners shouldn't have huge corners on mobile */
  .rounded-3xl { border-radius: 18px !important; }
  .rounded-2xl { border-radius: 14px !important; }

  /* ---------- Heroes / banners ---------- */
  [class*="h-[870px]"], [class*="h-[800px]"], [class*="h-[720px]"], [class*="h-[700px]"], [class*="h-[680px]"], [class*="h-[640px]"], [class*="h-[600px]"], [class*="h-[560px]"] {
    height: auto !important;
    min-height: 460px !important;
  }
  [class*="min-h-[870px]"], [class*="min-h-[800px]"], [class*="min-h-[720px]"], [class*="min-h-[700px]"], [class*="min-h-[680px]"], [class*="min-h-[640px]"], [class*="min-h-[600px]"] {
    min-height: 460px !important;
  }
  /* Wide editorial heroes (21/9, 16/9, 3/1, 2/1) become a portrait card on phones.
     Tailwind escapes the bracketed value so we target it both ways. */
  [class*="aspect-[21/9]"], [class*="aspect-[16/9]"], [class*="aspect-[3/1]"], [class*="aspect-[2/1]"],
  .aspect-\\[21\\/9\\], .aspect-\\[16\\/9\\], .aspect-\\[3\\/1\\], .aspect-\\[2\\/1\\] {
    aspect-ratio: 4 / 5 !important;
  }

  /* ---------- Image / card heights ---------- */
  .h-96 { height: 14rem !important; }    /* 224px */
  .h-80 { height: 13rem !important; }    /* 208px */
  .h-72 { height: 12rem !important; }
  .h-64 { height: 11rem !important; }    /* 176px */
  .h-60 { height: 10.5rem !important; }
  .h-56 { height: 10rem !important; }

  /* Product / blog card image headers become square at narrow widths */
  .rounded-2xl > .relative.h-64,
  .rounded-2xl > .relative.h-60,
  .rounded-2xl > .relative.h-72,
  .rounded-2xl > .relative.h-56 {
    height: auto !important;
    aspect-ratio: 1 / 1;
  }
  /* Standalone tile-style image cards (e.g. Curated Categories on home) */
  .group.relative.h-80,
  .group.relative.h-64 {
    height: auto !important;
    aspect-ratio: 1 / 1;
  }

  /* CTA promo banner orb container */
  .w-64.h-64, .w-80.h-80 { width: 11rem !important; height: 11rem !important; }

  /* ---------- Top nav / header ---------- */
  nav.fixed.top-0 .h-20 { height: 64px !important; }
  nav.fixed.top-0 [class*="h-20"] { height: 64px !important; }
  main.pt-20, main[class*="pt-20"] { padding-top: 64px !important; }
  main.pt-24, main[class*="pt-24"] { padding-top: 72px !important; }

  /* Reduce logo wordmark size beside the logo image in nav/footer */
  nav.fixed.top-0 .text-h4.font-h4 { font-size: 17px !important; }
  footer .text-h3.font-h3 { font-size: 18px !important; }

  /* ---------- Newsletter / inline forms ---------- */
  form input[type="email"], form input[type="text"] { padding: 12px 14px !important; font-size: 14.5px !important; }
  form button[type="submit"] { padding-top: 12px !important; padding-bottom: 12px !important; }

  /* ---------- Footer columns ---------- */
  footer .grid.grid-cols-1.md\\:grid-cols-4 { row-gap: 24px !important; }
  footer .grid.grid-cols-2.md\\:grid-cols-4 { row-gap: 22px !important; align-items: start !important; }
  footer .grid h5 { margin-bottom: 6px !important; }

  /* ---------- Margins / spacing utilities used heavily ---------- */
  .mb-8 { margin-bottom: 18px !important; }
  .mb-6 { margin-bottom: 14px !important; }
  .mt-8 { margin-top: 18px !important; }
  .mt-6 { margin-top: 14px !important; }
  .gap-8 { gap: 16px !important; }
  .gap-6 { gap: 14px !important; }

  /* ---------- Buttons ---------- */
  button { font-size: 14px !important; }
  a[class*="bg-"], a[class*="border"] { font-size: 14px !important; }
  button,
  input[type="submit"],
  a.inline-block,
  a.inline-flex,
  a.rounded-lg,
  a.rounded-xl,
  a.rounded-full {
    line-height: 1.1 !important;
    white-space: nowrap !important;
  }
  /* Keep horizontally-scrollable chip rows intact (don't shrink chips) */
  .overflow-x-auto { flex-wrap: nowrap !important; }
  .overflow-x-auto > button,
  .overflow-x-auto > a,
  .overflow-x-auto > * {
    flex: 0 0 auto !important;
    flex-shrink: 0 !important;
    min-width: max-content !important;
    width: auto !important;
    max-width: none !important;
  }
  a.px-8.py-4, button.px-8.py-4,
  a.px-6.py-3, button.px-6.py-3,
  a.px-4.py-3, button.px-4.py-3,
  a.px-10.py-4, button.px-10.py-4 {
    padding: 11px 16px !important;
  }
  button.rounded-full, a.rounded-full { padding-top: 8px !important; padding-bottom: 8px !important; }

  /* ---------- Inverse promo CTA banner: stack neatly ---------- */
  section .flex.flex-col.md\\:flex-row.items-center.justify-between { gap: 18px !important; }

  /* ---------- Process / step lists ---------- */
  .lg\\:pl-stack-lg { padding-left: 0 !important; }
  .pl-stack-lg { padding-left: 0 !important; }

  /* Prevent overflow from absolute decoration cards */
  [class*="-bottom-6"][class*="-right-6"].absolute { display: none !important; }

  /* ---------- Admin dashboard mobile cleanups ---------- */
  /* Make page-action toolbars wrap nicely instead of overflowing.
     Scoped to `gap-3` to avoid wrapping numbered-step rows (which use `flex gap-4`
     with a fixed-size circle next to text). */
  main .flex.justify-between.items-center.flex-wrap,
  main .flex.justify-between.items-center { flex-wrap: wrap !important; gap: 8px !important; }
  main .flex.items-center.gap-4,
  main .flex.gap-3 { flex-wrap: wrap !important; gap: 8px !important; }
  main .flex.gap-3 > * { min-width: 0; }
  /* Hide the admin header text user-info block; keep avatar */
  main > header .text-right,
  main > header .h-8.w-\\[1px\\] { display: none !important; }
  /* Allow sticky admin header to still wrap content if it overflows */
  main > header.sticky { gap: 8px !important; }
  main > header.sticky .max-w-md { max-width: 100% !important; }
  /* Push admin sticky header right of the floating hamburger on mobile */
  main > header.sticky { padding-left: 56px !important; }
  /* Promotion CTA banner: tame extreme decorative orbs */
  [class*="blur-3xl"] { filter: blur(40px) !important; }

  /* Final safety: prevent horizontal scroll bleed */
  html, body { overflow-x: hidden !important; }
}
@media (max-width: 380px) {
  h1, .text-h1, .font-h1 { font-size: 26px !important; }
  h2, .text-h2, .font-h2 { font-size: 22px !important; }
  .px-margin-desktop { padding-left: 14px !important; padding-right: 14px !important; }
}
</style>"""

FA_CSS_LINK = "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.2/css/all.min.css"

def apply_fontawesome(html: str) -> str:
    if "font-awesome" in html or "cdnjs.cloudflare.com/ajax/libs/font-awesome" in html:
        return html
    return re.sub(
        r"(?is)</head>",
        f'<link rel="stylesheet" href="{FA_CSS_LINK}"/>\n</head>',
        html,
        count=1,
    )


def apply_fonts(html: str) -> str:
    # Ensure Inter + Plus Jakarta Sans are loaded everywhere.
    if "fonts.googleapis.com" not in html or ("Plus+Jakarta+Sans" not in html or "family=Inter" not in html):
        html = re.sub(
            r"(?is)</head>",
            f'<link href="{FONTS_LINK}" rel="stylesheet"/>\n</head>',
            html,
            count=1,
        )
    # Ensure our global font mapping exists exactly once.
    if 'id="elikhope-fonts"' not in html:
        html = re.sub(r"(?is)</head>", FONTS_STYLE + "\n</head>", html, count=1)
    return html


def apply_responsive_type(html: str) -> str:
    # Strip any previously injected versions so re-runs always get the latest CSS.
    html = re.sub(
        r'(?is)<style id="elikhope-responsive(?:-v\d+)?">[\s\S]*?</style>',
        "",
        html,
    )
    return re.sub(r"(?is)</head>", RESPONSIVE_STYLE_ALL + "\n</head>", html, count=1)


def apply_responsive_helpers(html: str) -> str:
    if "data-ek-toggle" not in html:
        return html
    # Remove any previously injected helper so re-runs always ship the latest JS.
    html = re.sub(
        r'(?is)<script id="ek-toggle-init">[\s\S]*?</script>',
        "",
        html,
    )
    js = """<script id="ek-toggle-init">
(() => {
  const closedClass = (root) => (root.getAttribute('data-ek-drawer') === 'left') ? '-translate-x-full' : 'translate-x-full';
  const openDrawer = (root) => {
    root.classList.remove('hidden');
    const panel = root.querySelector('[data-ek-drawer-panel]');
    if (panel) requestAnimationFrame(() => panel.classList.remove(closedClass(root)));
    document.documentElement.classList.add('overflow-hidden');
  };
  const closeDrawer = (root) => {
    const panel = root.querySelector('[data-ek-drawer-panel]');
    if (panel) panel.classList.add(closedClass(root));
    window.setTimeout(() => {
      root.classList.add('hidden');
      document.documentElement.classList.remove('overflow-hidden');
    }, 220);
  };
  document.addEventListener('click', (e) => {
    const btn = e.target.closest('[data-ek-toggle]');
    if (!btn) return;
    const id = btn.getAttribute('data-ek-toggle');
    const root = document.getElementById(id);
    if (!root) return;
    const isDrawer = root.hasAttribute('data-ek-drawer');
    if (!isDrawer) { root.classList.toggle('hidden'); return; }
    const isOpen = !root.classList.contains('hidden');
    if (isOpen) closeDrawer(root); else openDrawer(root);
  });
  document.addEventListener('keydown', (e) => {
    if (e.key !== 'Escape') return;
    document.querySelectorAll('[data-ek-drawer]:not(.hidden)').forEach(closeDrawer);
  });
})();
</script>"""
    return re.sub(r"(?is)</body>", js + "\n</body>", html, count=1)


def logo_brand_link(href_home: str, subtitle: str, dark_sidebar: bool) -> str:
    sub_cls = (
        "font-body-sm text-body-sm text-surface-variant dark:text-outline opacity-70"
        if dark_sidebar
        else "text-on-surface-variant font-body-sm"
    )
    title_cls = (
        "text-h4 font-h4 text-primary-fixed dark:text-primary tracking-tight"
        if dark_sidebar
        else "font-h3 text-h3 font-bold text-primary dark:text-primary-fixed-dim"
    )
    return f"""<a href="{href_home}" class="flex items-center gap-3 group">
<img src="{ASSET_LOGO}" alt="" class="h-10 w-10 shrink-0 rounded-lg" width="40" height="40"/>
<div class="leading-tight">
<h1 class="{title_cls}">EliKhope Farms</h1>
<p class="{sub_cls}">{subtitle}</p>
</div>
</a>"""


def admin_nav_link(active: str, key: str, icon: str, label: str, href: str) -> str:
    is_on = active == key or (active == "settings" and key == "settings")
    if is_on:
        return f"""<a class="flex items-center gap-3 px-4 py-3 rounded-lg text-primary-fixed-dim font-bold border-l-4 border-primary-fixed-dim bg-on-surface-variant/10 transition-opacity" href="{href}">
<span class="material-symbols-outlined">{icon}</span>
<span class="font-body-md text-body-md">{label}</span>
</a>"""
    return f"""<a class="flex items-center gap-3 px-4 py-3 rounded-lg text-surface-variant dark:text-outline hover:text-surface-bright hover:bg-on-surface-variant/5 transition-colors" href="{href}">
<span class="material-symbols-outlined">{icon}</span>
<span class="font-body-md text-body-md">{label}</span>
</a>"""


def render_admin_sidebar(active: str) -> str:
    if active in ("payment", "zones", "staff"):
        active = "settings"
    items = [
        ("dashboard", "dashboard", "Dashboard", U["adm_dash"]),
        ("orders", "shopping_cart", "Orders", U["adm_orders"]),
        ("products", "inventory_2", "Products", U["adm_products"]),
        ("inventory", "warehouse", "Inventory", U["adm_inv"]),
        ("deliveries", "local_shipping", "Deliveries", U["adm_deliver"]),
        ("customers", "groups", "Customers", U["adm_cust"]),
        ("promotions", "campaign", "Promotions", U["adm_promo"]),
        ("cms", "dvr", "CMS", U["adm_cms"]),
        ("hero", "view_quilt", "Homepage hero", U["adm_hero"]),
        ("analytics", "analytics", "Analytics", U["adm_analytics"]),
        ("support", "support_agent", "Support", U["adm_support"]),
    ]
    nav_inner = "\n".join(admin_nav_link(active, k, ic, lb, h) for k, ic, lb, h in items)
    settings_cls = (
        "flex items-center gap-3 px-4 py-2 rounded-lg text-primary-fixed-dim font-bold border-l-4 border-primary-fixed-dim bg-on-surface-variant/10"
        if active == "settings"
        else "flex items-center gap-3 px-4 py-2 rounded-lg text-surface-variant dark:text-outline hover:text-surface-bright hover:bg-on-surface-variant/5 transition-colors"
    )
    desktop = f"""<aside class="hidden md:flex flex-col h-screen fixed left-0 top-0 bg-inverse-surface dark:bg-surface-container-lowest shadow-md docked left-0 h-full w-64 z-50">
<div class="p-6">
{logo_brand_link(U["adm_dash"], "Admin terminal", True)}
</div>
<nav class="flex-1 px-4 space-y-1 overflow-y-auto">
{nav_inner}
</nav>
<div class="p-4 border-t border-on-surface-variant/10" data-ek-admin-footer="1">
<a class="w-full bg-primary-container text-on-primary font-bold py-3 px-4 rounded-lg hover:opacity-90 transition-opacity flex items-center justify-center gap-2" href="{U["adm_support"]}">
<span class="material-symbols-outlined">support_agent</span>
Contact support
</a>
<a class="{settings_cls} mt-3 block" href="{U["adm_settings"]}">
<span class="material-symbols-outlined align-middle mr-2">settings</span>
Settings
</a>
<a class="flex items-center gap-3 px-4 py-2 mt-1 rounded-lg text-surface-variant dark:text-outline hover:text-surface-bright" href="{U["admin_login"]}">
<span class="material-symbols-outlined">logout</span>
Log out
</a>
</div>
</aside>"""
    mobile = f"""
<button class="md:hidden fixed top-3 left-3 z-[60] p-3 rounded-xl bg-surface shadow-md border border-outline-variant/40" type="button" aria-label="Open admin menu" data-ek-toggle="ek-admin-drawer">
  <i class="fa-solid fa-bars text-on-surface-variant"></i>
</button>
<div id="ek-admin-drawer" class="md:hidden hidden fixed inset-0 z-[70]" data-ek-drawer="left">
  <div class="absolute inset-0 bg-black/40" data-ek-toggle="ek-admin-drawer" aria-label="Close menu"></div>
  <aside data-ek-drawer-panel class="absolute left-0 top-0 h-full w-80 max-w-[85vw] bg-inverse-surface dark:bg-surface-container-lowest shadow-xl border-r border-on-surface-variant/10 flex flex-col -translate-x-full transition-transform duration-200 ease-out">
    <div class="p-6 flex items-start justify-between gap-4">
      <div class="flex-1">
        {logo_brand_link(U["adm_dash"], "Admin terminal", True)}
      </div>
      <button class="p-2 rounded-lg hover:bg-on-surface-variant/10" type="button" aria-label="Close menu" data-ek-toggle="ek-admin-drawer">
        <i class="fa-solid fa-xmark text-surface-variant"></i>
      </button>
    </div>
    <nav class="flex-1 px-4 space-y-1 overflow-auto pb-4">
      {nav_inner}
    </nav>
    <div class="p-4 border-t border-on-surface-variant/10" data-ek-admin-footer="1">
      <a class="w-full bg-primary-container text-on-primary font-bold py-3 px-4 rounded-lg hover:opacity-90 transition-opacity flex items-center justify-center gap-2" href="{U["adm_support"]}">
        <span class="material-symbols-outlined">support_agent</span>
        Contact support
      </a>
      <a class="{settings_cls} mt-3 block" href="{U["adm_settings"]}">
        <span class="material-symbols-outlined align-middle mr-2">settings</span>
        Settings
      </a>
      <a class="flex items-center gap-3 px-4 py-2 mt-1 rounded-lg text-surface-variant dark:text-outline hover:text-surface-bright" href="{U["admin_login"]}">
        <i class="fa-solid fa-arrow-right-from-bracket"></i>
        Log out
      </a>
    </div>
  </aside>
</div>"""
    return desktop + mobile


def render_admin_settings_tabs(active: str) -> str:
    def tab(key: str, icon: str, label: str, href: str) -> str:
        cls_active = "pb-4 text-primary font-bold border-b-2 border-primary flex items-center gap-2 px-1 whitespace-nowrap"
        cls_inact = "pb-4 text-on-surface-variant hover:text-primary transition-colors flex items-center gap-2 px-1 whitespace-nowrap"
        cls = cls_active if active == key else cls_inact
        fill = " style=\"font-variation-settings: 'FILL' 1;\"" if active == key else ""
        return f"""<a class="{cls}" href="{href}"><span class="material-symbols-outlined"{fill}>{icon}</span>{label}</a>"""

    return "\n".join(
        [
            '<div class="flex items-center gap-8 border-b border-surface-variant mb-10 overflow-x-auto pb-px">',
            tab("general", "settings", "General", U["adm_settings"]),
            tab("payments", "payments", "Payments", U["adm_pay"]),
            tab("zones", "map", "Delivery Zones", U["adm_zones"]),
            tab("staff", "admin_panel_settings", "Staff Permissions", U["adm_staff"]),
            "</div>",
        ]
    )


ADMIN_FOLDER_ACTIVE = {
    "admin_dashboard_overview_elikhope_farms": "dashboard",
    "orders_management_elikhope_farms_admin": "orders",
    "product_management_elikhope_farms_admin": "products",
    "inventory_management_elikhope_farms_admin": "inventory",
    "delivery_management_elikhope_farms_admin": "deliveries",
    "customer_management_elikhope_farms_admin": "customers",
    "promotions_campaigns_elikhope_farms_admin": "promotions",
    "content_management_elikhope_farms_admin": "cms",
    "homepage_hero_management_admin_cms": "hero",
    "analytics_business_intelligence_elikhope_farms_admin": "analytics",
    "customer_support_elikhope_farms_admin": "support",
    "admin_settings_elikhope_farms_admin": "settings",
    "payment_settings_elikhope_farms_admin": "settings",
    "delivery_zones_elikhope_farms_admin": "settings",
    "staff_permissions_elikhope_farms_admin": "settings",
}


def cust_nav(active: str, key: str, icon: str, label: str, href: str) -> str:
    act = (
        "flex items-center gap-3 px-4 py-3 rounded-lg bg-secondary-container text-on-secondary-container "
        "dark:bg-primary-container dark:text-on-primary-container font-semibold transition-transform duration-150"
    )
    inact = (
        "flex items-center gap-3 px-4 py-3 rounded-lg text-on-surface-variant "
        "hover:bg-surface-container-high dark:hover:bg-surface-container-highest transition-colors duration-150"
    )
    cls = act if active == key else inact
    return f"""<a class="{cls}" href="{href}">
<span class="material-symbols-outlined" data-icon="{icon}">{icon}</span>
<span>{label}</span>
</a>"""


def render_customer_sidebar(active: str) -> str:
    rows = [
        ("overview", "dashboard", "Overview", U["dash"]),
        ("orders", "shopping_bag", "Orders", U["orders"]),
        ("track", "local_shipping", "Tracking", U["track_dash"]),
        ("wishlist", "favorite", "Wishlist", U["wishlist"]),
        ("addresses", "location_on", "Addresses", U["addresses"]),
        ("notifications", "notifications", "Notifications", U["notif"]),
        ("recent", "history", "Recent purchases", U["recent"]),
        ("settings", "settings", "Settings", U["settings_c"]),
    ]
    nav = "\n".join(cust_nav(active, k, i, lb, h) for k, i, lb, h in rows)
    desktop = f"""<!-- SideNavBar Shell -->
<aside class="hidden md:flex h-screen w-64 fixed left-0 top-0 flex-col h-full border-r border-outline-variant dark:border-outline bg-surface dark:bg-surface-container-lowest shadow-sm z-50">
<div class="p-6">
{logo_brand_link(U["dash"], "Your account", False)}
</div>
<nav class="flex-1 px-4 space-y-2">
{nav}
</nav>
<div class="p-4 mt-auto border-t border-outline-variant/40">
<a class="block text-center text-sm text-primary font-semibold hover:underline" href="{U["shop_home"]}">Continue shopping</a>
<a class="block text-center text-xs text-on-surface-variant mt-2 hover:text-primary" href="{U["home"]}">Back to website</a>
<a class="mt-4 inline-flex w-full items-center justify-center gap-2 rounded-lg border border-outline-variant/60 px-4 py-2 text-sm font-semibold text-on-surface-variant hover:bg-surface-container-high transition-colors" href="{U["login"]}">
<span class="material-symbols-outlined text-[18px]">logout</span>
Log out
</a>
</div>
</aside>"""
    mobile = f"""
<div id="ek-cust-drawer" class="md:hidden hidden fixed inset-0 z-[70]" data-ek-drawer="left">
  <div class="absolute inset-0 bg-black/40" data-ek-toggle="ek-cust-drawer" aria-label="Close menu"></div>
  <aside data-ek-drawer-panel class="absolute left-0 top-0 h-full w-80 max-w-[85vw] bg-surface shadow-xl border-r border-outline-variant flex flex-col -translate-x-full transition-transform duration-200 ease-out">
    <div class="p-6 flex items-start justify-between gap-4">
      <div class="flex-1">
        {logo_brand_link(U["dash"], "Your account", False)}
      </div>
      <button class="p-2 rounded-lg hover:bg-surface-container" type="button" aria-label="Close menu" data-ek-toggle="ek-cust-drawer">
        <i class="fa-solid fa-xmark text-on-surface-variant"></i>
      </button>
    </div>
    <nav class="flex-1 px-4 space-y-2 overflow-auto pb-4">
      {nav}
    </nav>
    <div class="p-4 mt-auto border-t border-outline-variant/40">
      <a class="block text-center text-sm text-primary font-semibold hover:underline" href="{U["shop_home"]}">Continue shopping</a>
      <a class="block text-center text-xs text-on-surface-variant mt-2 hover:text-primary" href="{U["home"]}">Back to website</a>
      <a class="mt-4 inline-flex w-full items-center justify-center gap-2 rounded-lg border border-outline-variant/60 px-4 py-2 text-sm font-semibold text-on-surface-variant hover:bg-surface-container-high transition-colors" href="{U["login"]}">
        <i class="fa-solid fa-arrow-right-from-bracket text-[16px]"></i>
        Log out
      </a>
    </div>
  </aside>
</div>"""
    return desktop + mobile


CUST_FOLDER_ACTIVE = {
    "dashboard_overview_elikhope_farms": "overview",
    "my_orders_elikhope_farms": "orders",
    "track_your_delivery_elikhope_farms": "track",
    "my_wishlist_elikhope_farms": "wishlist",
    "manage_addresses_elikhope_farms": "addresses",
    "notifications_elikhope_farms": "notifications",
    "recent_purchases_elikhope_farms": "recent",
    "account_settings_elikhope_farms": "settings",
}


def customer_top_header() -> str:
    return f"""<!-- TopNavBar Shell -->
<header data-ek-cust-header class="fixed top-0 right-0 md:w-[calc(100%-16rem)] w-full h-16 bg-surface/80 dark:bg-surface-container/80 backdrop-blur-md shadow-sm flex justify-between items-center px-margin-mobile md:px-margin-desktop z-40 gap-3">
<div class="flex items-center gap-2 flex-1 min-w-0">
<button class="md:hidden inline-flex items-center justify-center p-2 rounded-lg hover:bg-surface-container transition-colors shrink-0" type="button" aria-label="Open menu" data-ek-toggle="ek-cust-drawer">
  <i class="fa-solid fa-bars text-on-surface-variant"></i>
</button>
<div class="relative max-w-md w-full group min-w-0">
<a href="{U["search"]}" class="absolute left-3 top-1/2 -translate-y-1/2 text-on-surface-variant"><span class="material-symbols-outlined">search</span></a>
<input class="w-full bg-surface-container-low border-none rounded-lg py-2 pl-10 pr-3 text-body-sm focus:ring-2 focus:ring-primary/20 focus:bg-surface transition-all" placeholder="Search products..." type="text"/>
</div>
</div>
<div class="flex items-center gap-2 sm:gap-4 md:gap-6 shrink-0">
<a class="hidden md:flex text-on-surface-variant hover:text-primary transition-colors items-center gap-1 font-body-sm" href="{U["help"]}"><span class="material-symbols-outlined" data-icon="help">help</span>Support</a>
<a class="relative inline-flex text-on-surface-variant hover:text-primary p-2" href="{U["notif"]}"><span class="material-symbols-outlined" data-icon="notifications">notifications</span><span class="absolute top-1 right-1 w-2 h-2 bg-error rounded-full"></span></a>
<a class="inline-flex p-2 text-on-surface-variant hover:text-primary" href="{U["cart"]}"><span class="material-symbols-outlined" data-icon="shopping_cart">shopping_cart</span></a>
<div class="hidden md:block h-8 w-[1px] bg-outline-variant"></div>
<a href="{U["settings_c"]}" class="hidden sm:flex items-center gap-3">
<img alt="" class="w-8 h-8 rounded-full object-cover border border-outline-variant" src="{ASSET_PERSON_BUTCHER}"/>
</a>
</div>
</header>"""


MARKETING_NAV_INNER = f"""
<a class="font-body-md text-body-md text-on-surface hover:text-primary transition-colors" href="{U["home"]}">Home</a>
<a class="font-body-md text-body-md text-on-surface hover:text-primary transition-colors" href="{U["shop_home"]}">Shop</a>
<a class="font-body-md text-body-md text-on-surface hover:text-primary transition-colors" href="{U["about"]}">About</a>
<a class="font-body-md text-body-md text-on-surface hover:text-primary transition-colors" href="{U["quality"]}">Quality Control</a>
<a class="font-body-md text-body-md text-on-surface hover:text-primary transition-colors" href="{U["gallery"]}">Gallery</a>
<a class="font-body-md text-body-md text-on-surface hover:text-primary transition-colors" href="{U["blog"]}">Blog</a>
<a class="font-body-md text-body-md text-on-surface hover:text-primary transition-colors" href="{U["contact"]}">Contact</a>
"""


def marketing_top_nav() -> str:
    return f"""<!-- TopNavBar -->
<nav class="fixed top-0 w-full z-50 bg-surface dark:bg-inverse-surface shadow-sm">
<div class="max-w-container-max mx-auto flex justify-between items-center px-margin-mobile md:px-margin-desktop h-16 md:h-20 gap-2">
<a href="{U["home"]}" class="flex items-center gap-2 sm:gap-3 shrink-0 min-w-0">
<img src="{ASSET_LOGO}" alt="" class="h-9 w-9 sm:h-10 sm:w-10 rounded-lg shrink-0" width="40" height="40"/>
<span class="text-h4 font-h4 font-bold text-primary dark:text-primary-fixed truncate">EliKhope Farms</span>
</a>
<div class="hidden lg:flex items-center gap-6 flex-wrap justify-center">
{MARKETING_NAV_INNER}
</div>
<div class="flex items-center gap-1 sm:gap-stack-sm shrink-0">
<a class="hidden sm:inline font-body-sm font-semibold text-primary hover:underline" href="{U["login"]}">Login</a>
<a class="hidden sm:inline-flex px-4 py-2 rounded-lg bg-primary text-white font-bold text-sm hover:opacity-90" href="{U["register"]}">Sign up</a>
<a class="p-2 rounded-full hover:bg-surface-container transition-colors" href="{U["cart"]}" title="Cart"><span class="material-symbols-outlined text-on-surface-variant">shopping_cart</span></a>
<a class="hidden sm:inline-flex p-2 rounded-full hover:bg-surface-container transition-colors" href="{U["dash"]}" title="Account"><span class="material-symbols-outlined text-on-surface-variant">account_circle</span></a>
<button class="lg:hidden p-2 rounded-full hover:bg-surface-container transition-colors" type="button" aria-label="Open menu" data-ek-toggle="ek-site-drawer">
  <i class="fa-solid fa-bars text-on-surface-variant"></i>
</button>
</div>
</div>
</nav>"""


def mobile_site_drawer() -> str:
    return f"""
<div id="ek-site-drawer" class="lg:hidden hidden fixed inset-0 z-[70]" data-ek-drawer="right">
  <div class="absolute inset-0 bg-black/40" data-ek-toggle="ek-site-drawer" aria-label="Close menu"></div>
  <aside data-ek-drawer-panel class="absolute right-0 top-0 h-full w-80 max-w-[85vw] bg-surface shadow-xl border-l border-outline-variant translate-x-full transition-transform duration-200 ease-out flex flex-col">
    <div class="p-6 flex items-start justify-between gap-4 border-b border-outline-variant/40">
      <div class="flex-1">
        <a href="{U["home"]}" class="flex items-center gap-3">
          <img src="{ASSET_LOGO}" alt="" class="h-10 w-10 rounded-lg" width="40" height="40"/>
          <span class="text-h4 font-h4 font-bold text-primary">EliKhope Farms</span>
        </a>
        <p class="text-xs text-on-surface-variant mt-2">Menu</p>
      </div>
      <button class="p-2 rounded-lg hover:bg-surface-container" type="button" aria-label="Close menu" data-ek-toggle="ek-site-drawer">
        <i class="fa-solid fa-xmark text-on-surface-variant"></i>
      </button>
    </div>
    <nav class="flex-1 p-6 pt-4 flex flex-col gap-2 overflow-auto">
      <a class="py-2 font-body-md text-on-surface hover:text-primary" href="{U["home"]}">Home</a>
      <a class="py-2 font-body-md text-on-surface hover:text-primary" href="{U["shop_home"]}">Shop</a>
      <a class="py-2 font-body-md text-on-surface hover:text-primary" href="{U["about"]}">About</a>
      <a class="py-2 font-body-md text-on-surface hover:text-primary" href="{U["quality"]}">Quality Control</a>
      <a class="py-2 font-body-md text-on-surface hover:text-primary" href="{U["gallery"]}">Gallery</a>
      <a class="py-2 font-body-md text-on-surface hover:text-primary" href="{U["blog"]}">Blog</a>
      <a class="py-2 font-body-md text-on-surface hover:text-primary" href="{U["contact"]}">Contact</a>
    </nav>
    <div class="p-6 border-t border-outline-variant/40 space-y-3">
      <a class="w-full inline-flex items-center justify-center px-4 py-3 rounded-xl border border-outline-variant text-on-surface font-semibold" href="{U["login"]}">Login</a>
      <a class="w-full inline-flex items-center justify-center px-4 py-3 rounded-xl bg-primary text-on-primary font-bold" href="{U["register"]}">Create account</a>
    </div>
  </aside>
</div>
"""


MARKETING_FOOTER = f"""<footer class="w-full bg-surface-container-highest dark:bg-inverse-surface border-t border-outline-variant">
<div class="py-stack-lg px-margin-mobile md:px-margin-desktop max-w-container-max mx-auto">
<div class="grid grid-cols-2 md:grid-cols-4 gap-x-6 gap-y-8 lg:gap-gutter">
<div class="col-span-2 md:col-span-4 lg:col-span-1 lg:col-auto flex flex-col gap-3 md:max-w-sm">
<a href="{U["home"]}" class="flex items-center gap-3">
<img src="{ASSET_LOGO}" alt="" class="h-9 w-9 rounded-lg" width="36" height="36"/>
<span class="text-h3 font-h3 font-bold text-primary dark:text-primary-fixed">EliKhope Farms</span>
</a>
<p class="font-body-sm text-body-sm text-on-surface-variant dark:text-surface-variant">© 2026 EliKhope Farms. Premium farm-to-consumer meat.</p>
</div>
<div class="flex flex-col gap-2 min-w-0">
<h5 class="font-bold text-on-surface mb-1">Shop</h5>
<a class="font-body-sm text-on-surface-variant hover:text-primary underline block" href="{U["shop_home"]}">Shop</a>
<a class="font-body-sm text-on-surface-variant hover:text-primary underline block" href="{U["categories_hub"]}">Categories</a>
</div>
<div class="flex flex-col gap-2 min-w-0">
<h5 class="font-bold text-on-surface mb-1">Trust</h5>
<a class="font-body-sm text-on-surface-variant hover:text-primary underline block" href="{U["quality"]}">Quality Control</a>
<a class="font-body-sm text-on-surface-variant hover:text-primary underline block" href="{U["help"]}">Help center</a>
<a class="font-body-sm text-on-surface-variant hover:text-primary underline block" href="{U["contact"]}">Contact us</a>
</div>
<div class="flex flex-col gap-2 min-w-0">
<h5 class="font-bold text-on-surface mb-1">Account</h5>
<a class="font-body-sm text-on-surface-variant hover:text-primary underline block" href="{U["login"]}">Login</a>
<a class="font-body-sm text-on-surface-variant hover:text-primary underline block" href="{U["register"]}">Create account</a>
<a class="font-body-sm text-on-surface-variant hover:text-primary underline block" href="{U["dash"]}">Account</a>
</div>
</div>
</div>
</footer>"""


SHOP_TOP_NAV = f"""<header class="fixed top-0 w-full z-50 flex justify-between items-center px-margin-desktop h-20 max-w-container-max mx-auto bg-surface dark:bg-inverse-surface shadow-sm">
<a href="{U["home"]}" class="flex items-center gap-3 shrink-0">
<img src="{ASSET_LOGO}" alt="" class="h-10 w-10 rounded-lg" width="40" height="40"/>
<span class="text-h4 font-h4 font-bold text-primary dark:text-primary-fixed">EliKhope Farms</span>
</a>
<nav class="hidden md:flex items-center gap-stack-md">
<a class="text-body-sm text-primary font-semibold border-b-2 border-primary pb-1" href="{U["shop_home"]}">Shop</a>
<a class="text-body-sm text-on-surface-variant hover:text-primary font-medium" href="{U["shop_home"]}">Beef</a>
<a class="text-body-sm text-on-surface-variant hover:text-primary font-medium" href="{U["shop_home"]}">Goat</a>
<a class="text-body-sm text-on-surface-variant hover:text-primary font-medium" href="{U["shop_home"]}">Chicken</a>
<a class="text-body-sm text-on-surface-variant hover:text-primary font-medium" href="{U["shop_home"]}">Special cuts</a>
</nav>
<div class="flex items-center gap-base">
<a href="{U["search"]}" class="hidden lg:inline-flex items-center rounded-lg bg-surface-container-low px-3 py-2 text-body-sm text-on-surface-variant hover:bg-surface-container">
<span class="material-symbols-outlined text-base mr-1">search</span>Search</a>
<a class="p-2 hover:bg-surface-container rounded-full" href="{U["cart"]}" title="Cart"><span class="material-symbols-outlined text-primary">shopping_cart</span></a>
<a class="p-2 hover:bg-surface-container rounded-full" href="{U["login"]}" title="Account"><span class="material-symbols-outlined text-primary">account_circle</span></a>
</div>
</header>"""


AUTH_TOP_RE = re.compile(
    r"<!-- TopNavBar[^>]*-->\s*<header[^>]*fixed top-0[\s\S]*?</header>",
    re.IGNORECASE,
)


def patch_auth_top(html: str) -> str:
    if AUTH_TOP_RE.search(html):
        return AUTH_TOP_RE.sub(marketing_top_nav(), html, count=1)
    return html


# Mobile branding block injected at the top of every auth form so the logo
# always appears above the form, regardless of the original export.
AUTH_BRAND_BLOCK = (
    '<div class="mb-stack-lg flex flex-col items-center text-center" data-ek-auth-brand>'
    f'<img src="{ASSET_LOGO}" alt="EliKhope Farms" class="h-12 w-12 rounded-lg shadow-sm" width="48" height="48"/>'
    '<h2 class="font-h3 text-h3 text-primary mt-base">EliKhope Farms</h2>'
    '</div>'
)


def strip_auth_visual_side(html: str) -> str:
    """Remove the green left/top visual section on auth pages.

    Targets two known patterns:
    - login / admin_login: <section class="auth-visual-side ...">...</section>
    - create_account: <section class="hidden lg:flex lg:w-1/2 ... bg-primary-container ...">...</section>
    Also collapses the parent <main class="auth-split-layout"> into a single-column flex layout
    and centers the form column.
    """
    # 1) login / admin_login style.
    html = re.sub(
        r'(?is)<section class="auth-visual-side[^"]*"[^>]*>[\s\S]*?</section>',
        "",
        html,
    )
    # 2) create_account style.
    html = re.sub(
        r'(?is)<!--\s*Left Side[\s\S]*?-->\s*<section class="hidden lg:flex lg:w-1/2[^"]*"[^>]*>[\s\S]*?</section>',
        "",
        html,
    )
    html = re.sub(
        r'(?is)<section class="hidden lg:flex lg:w-1/2[^"]*"[^>]*>[\s\S]*?</section>',
        "",
        html,
    )
    # 3) Drop the now-unused split-grid CSS rules so the form fills full width.
    html = re.sub(
        r"(?is)\.auth-split-layout\s*\{[^}]*\}",
        ".auth-split-layout { display: flex; align-items: stretch; justify-content: center; min-height: 100vh; }",
        html,
        count=1,
    )
    html = re.sub(
        r"(?is)@media\s*\(max-width:\s*768px\)\s*\{[^}]*\.auth-split-layout[^}]*\}[^}]*\.auth-visual-side[^}]*\}\s*\}",
        "",
        html,
    )
    # 4) Collapse main wrappers to a single centered column.
    html = re.sub(
        r'(<main class="auth-split-layout)"',
        r'\1 justify-center"',
        html,
        count=1,
    )
    html = re.sub(
        r'(<main class=")flex min-h-screen w-full"',
        r'\1flex min-h-screen w-full justify-center"',
        html,
        count=1,
    )
    # 5) Make the form section take a comfortable max width on desktop, full width on mobile.
    # Normalise a prior buggy pass that closed class="" too early.
    html = html.replace(
        'class="flex items-center justify-center p-margin-mobile md:p-margin-desktop bg-surface" w-full max-w-2xl mx-auto>',
        'class="flex items-center justify-center p-margin-mobile md:p-margin-desktop bg-surface w-full max-w-2xl mx-auto">',
    )
    html = re.sub(
        r'(<section class="(?:flex items-center justify-center|w-full lg:w-1/2 flex items-center justify-center)[^"]*)(")(\s*>)',
        r"\1 w-full max-w-2xl mx-auto\2\3",
        html,
    )
    # 6) Replace the `agriculture` (tractor) icon block with the actual logo.
    html = re.sub(
        r'(?is)<div class="md:hidden mb-stack-lg flex flex-col items-center">\s*'
        r'<span class="material-symbols-outlined text-primary text-\[48px\]">agriculture</span>\s*'
        r'<h1 class="font-h3 text-h3 text-primary mt-base">EliKhope Farms</h1>\s*</div>',
        AUTH_BRAND_BLOCK,
        html,
    )
    # 7) For pages that lacked a mobile branding block (create_account, etc.),
    #    inject our brand block at the top of the form column. Skip if already injected.
    if "data-ek-auth-brand" not in html:
        html = re.sub(
            r'(?is)(<section class="(?:[^"]*?)(?:flex items-center justify-center|w-full lg:w-1/2)[^"]*"[^>]*>\s*<div class="w-full max-w-(?:md|lg|xl|2xl)[^"]*">)',
            r"\1\n" + AUTH_BRAND_BLOCK,
            html,
            count=1,
        )
    return html


AUTH_FOOTER = f"""<footer class="w-full py-6 px-margin-mobile md:px-margin-desktop border-t border-outline-variant bg-surface-container-low">
<div class="max-w-container-max mx-auto flex flex-col sm:flex-row gap-3 justify-between items-center text-sm text-on-surface-variant">
<a href="{U["home"]}" class="font-semibold text-primary hover:underline">EliKhope Farms</a>
<div class="flex gap-4 flex-wrap justify-center">
<a href="{U["help"]}" class="hover:text-primary underline">Help</a>
<a href="{U["contact"]}" class="hover:text-primary underline">Contact</a>
</div>
</div>
</footer>"""


def replace_or_append_footer(html: str, footer_html: str) -> str:
    if re.search(r"(?is)<footer[^>]*>", html):
        return re.sub(r"(?is)<footer[^>]*>.*?</footer>", footer_html, html, count=1)
    return html.replace("</body>", footer_html + "\n</body>")


def sync_auth_hero_image(html: str, hero_src: str) -> str:
    """Keep <img src> inside data-ek-auth-hero aligned with the page (customer vs admin)."""
    return re.sub(
        r'(?is)(<section[^>]*\bdata-ek-auth-hero\b[^>]*>\s*<img\s+src=")([^"]+)(")',
        rf"\1{hero_src}\3",
        html,
        count=1,
    )


def auth_login_hero_section(hero_img: str) -> str:
    return f"""<!-- Auth desktop hero (image left) -->
<section class="hidden lg:flex lg:w-1/2 relative min-h-[280px] lg:min-h-screen overflow-hidden bg-black" data-ek-auth-hero>
  <img src="{hero_img}" alt="" class="absolute inset-0 w-full h-full object-cover" width="1200" height="1600"/>
  <div class="absolute inset-0 bg-gradient-to-tr from-black/90 via-black/55 to-black/40"></div>
  <div class="relative z-10 flex flex-col justify-end p-margin-desktop max-w-xl mt-auto">
    <p class="font-label-caps text-white/70 tracking-widest mb-2">FARM · AKUSE · EASTERN REGION</p>
    <h2 class="font-h2 text-h2 text-white mb-3">Premium cuts from our pastures to your kitchen.</h2>
    <p class="font-body-md text-white/80 max-w-md">Ethically raised in Ghana, cold-chain delivery, and the hygiene standards you expect from EliKhope Farms.</p>
  </div>
</section>"""


def apply_auth_login_desktop_split(html: str, parent: str) -> str:
    """Desktop: hero image left, form right (login + staff login). Mobile: form only."""
    if parent not in {"login_elikhope_farms", "admin_login_elikhope_farms"}:
        return html
    hero_img = AUTH_ADMIN_AUTH_HERO_IMG if parent == "admin_login_elikhope_farms" else AUTH_CUSTOMER_AUTH_HERO_IMG
    if "auth-split-layout" not in html:
        return html
    html = re.sub(
        r"\.auth-split-layout\s*\{[^}]+\}",
        ".auth-split-layout { display: flex; flex-direction: column; min-height: 100vh; width: 100%; }\n"
        "        @media (min-width: 1024px) {\n"
        "            .auth-split-layout { flex-direction: row; }\n"
        "        }",
        html,
        count=1,
    )
    html = html.replace('<main class="auth-split-layout justify-center">', '<main class="auth-split-layout">', 1)
    if "data-ek-auth-hero" not in html:
        html = re.sub(
            r'(<main class="auth-split-layout[^"]*">)\s*(?:<!-- Auth desktop hero[^>]*-->\s*\n\s*)?',
            r"\1\n" + auth_login_hero_section(hero_img) + "\n",
            html,
            count=1,
        )
    html = re.sub(
        r'<section class="flex items-center justify-center p-margin-mobile md:p-margin-desktop bg-surface(?:\s+[^"]*)?"[^>]*>',
        '<section class="w-full lg:w-1/2 flex flex-1 items-center justify-center p-margin-mobile md:p-margin-desktop bg-surface">',
        html,
        count=1,
    )
    html = html.replace(
        '<div class="mb-stack-lg flex flex-col items-center text-center" data-ek-auth-brand>',
        '<div class="mb-stack-lg flex flex-col items-center text-center lg:hidden" data-ek-auth-brand>',
        1,
    )
    return sync_auth_hero_image(html, hero_img)


def apply_register_desktop_split(html: str, parent: str) -> str:
    """Mirror login layout: refrigerated-hero left, register form right (lg+)."""
    if parent != "create_account_elikhope_farms":
        return html
    if "data-ek-auth-hero" in html:
        return sync_auth_hero_image(html, AUTH_CUSTOMER_AUTH_HERO_IMG)
    if ".auth-split-layout {" not in html:
        html = html.replace(
            "</style>",
            """
        .auth-split-layout { display: flex; flex-direction: column; min-height: 100vh; width: 100%; }
        @media (min-width: 1024px) {
            .auth-split-layout { flex-direction: row; }
        }
</style>""",
            1,
        )
    # Export may already use auth-split + empty hero placeholder (no <section>).
    html_new, n = re.subn(
        r'<main class="auth-split-layout justify-center">\s*<!-- Auth desktop hero \(image left\) -->[\s\n]*(?=<!-- Right Side:)',
        '<main class="auth-split-layout">\n' + auth_login_hero_section(AUTH_CUSTOMER_AUTH_HERO_IMG) + "\n",
        html,
        count=1,
    )
    if n:
        html = html_new
    else:
        html = html.replace(
            '<main class="flex min-h-screen w-full justify-center">',
            '<main class="auth-split-layout">',
            1,
        )
        html = html.replace(
            '<main class="auth-split-layout">',
            '<main class="auth-split-layout">\n' + auth_login_hero_section(AUTH_CUSTOMER_AUTH_HERO_IMG) + "\n",
            1,
        )
    html = html.replace(
        '<section class="w-full lg:w-1/2 flex items-center justify-center p-margin-mobile md:p-margin-desktop bg-surface" w-full max-w-2xl mx-auto>',
        '<section class="w-full lg:w-1/2 flex flex-1 items-center justify-center p-margin-mobile md:p-margin-desktop bg-surface">',
        1,
    )
    html = html.replace(
        '<div class="mb-stack-lg flex flex-col items-center text-center" data-ek-auth-brand>',
        '<div class="mb-stack-lg flex flex-col items-center text-center lg:hidden" data-ek-auth-brand>',
        1,
    )
    return sync_auth_hero_image(html, AUTH_CUSTOMER_AUTH_HERO_IMG)


def patch_shop_ghana_plp_filters(html: str) -> str:
    """Ghana-market wording for sidebar cut + freshness filters (PLP templates)."""
    if "data-ek-ghana-filters" in html:
        return html
    if '<h3 class="text-h4 font-h4 mb-stack-sm text-on-surface">Cut Type</h3>' not in html:
        return html
    html = html.replace(
        '<span class="text-body-md text-on-surface-variant group-hover:text-primary transition-colors">Ribeye Steak</span>',
        '<span class="text-body-md text-on-surface-variant group-hover:text-primary transition-colors">Stew beef (bone-in chunks)</span>',
        1,
    )
    html = html.replace(
        '<span class="text-body-md text-primary font-bold">Sirloin Fillet</span>',
        '<span class="text-body-md text-primary font-bold">Minced beef (khebab mix)</span>',
        1,
    )
    html = html.replace(
        '<span class="text-body-md text-on-surface-variant group-hover:text-primary transition-colors">Ground Beef</span>',
        '<span class="text-body-md text-on-surface-variant group-hover:text-primary transition-colors">Cow leg / knee (wele-style)</span>',
        1,
    )
    html = html.replace(
        '<span class="text-body-md text-on-surface-variant group-hover:text-primary transition-colors">Brisket</span>',
        '<span class="text-body-md text-on-surface-variant group-hover:text-primary transition-colors">Bone-in short ribs</span>',
        1,
    )
    html = html.replace(
        '<button class="px-4 py-2 rounded-full border border-primary bg-primary-container text-on-primary-container text-label-caps">Same Day</button>\n'
        '<button class="px-4 py-2 rounded-full border border-outline-variant text-on-surface-variant text-label-caps hover:border-primary transition-colors">Chilled</button>\n'
        '<button class="px-4 py-2 rounded-full border border-outline-variant text-on-surface-variant text-label-caps hover:border-primary transition-colors">Frozen</button>',
        '<button class="px-4 py-2 rounded-full border border-primary bg-primary-container text-on-primary-container text-label-caps">Today&apos;s kill</button>\n'
        '<button class="px-4 py-2 rounded-full border border-outline-variant text-on-surface-variant text-label-caps hover:border-primary transition-colors">Cold room</button>\n'
        '<button class="px-4 py-2 rounded-full border border-outline-variant text-on-surface-variant text-label-caps hover:border-primary transition-colors">Frozen</button>',
        1,
    )
    html = html.replace(
        "<p class=\"text-body-sm text-on-secondary-container opacity-90\">100% Grass-fed, ethically raised beef from local Ghana partner farms.</p>",
        "<p class=\"text-body-sm text-on-secondary-container opacity-90\">Sourced with local partner farms across Ghana — traceable beef with cold-chain handling.</p>",
        1,
    )
    html = html.replace(
        'id="ek-filters-panel" class="hidden lg:block w-full lg:w-64 flex-shrink-0 space-y-stack-lg"',
        'id="ek-filters-panel" data-ek-ghana-filters class="hidden lg:block w-full lg:w-64 flex-shrink-0 space-y-stack-lg"',
        1,
    )
    return html


def patch_about_us_page(html: str, current_url: str | None) -> str:
    """About: dark hero, Our Team + Ghanaian names, shared portrait asset."""
    if not current_url or "elikhope_farms_about_us" not in current_url:
        return html
    html = html.replace(
        '<section class="relative h-[716px] flex items-center justify-center overflow-hidden bg-primary-container">',
        '<section class="relative h-[716px] flex items-center justify-center overflow-hidden bg-neutral-900">',
        1,
    )
    html = html.replace(
        '<img class="absolute inset-0 w-full h-full object-cover opacity-60 mix-blend-overlay"',
        '<img class="absolute inset-0 w-full h-full object-cover"',
        1,
    )
    if 'data-ek-about-hero-scrim' not in html:
        html = re.sub(
            r'(?is)(<img class="absolute inset-0 w-full h-full object-cover" data-alt="[^"]*" src="[^"]+"/>)\s*(<div class="relative z-10 text-center)',
            r'\1\n<div class="absolute inset-0 bg-black/60" data-ek-about-hero-scrim aria-hidden="true"></div>\n\2',
            html,
            count=1,
        )
    html = html.replace(
        'text-label-caps font-label-caps text-on-primary-container uppercase mb-stack-sm block tracking-widest">Our Heritage</span>',
        'text-label-caps font-label-caps text-white/80 uppercase mb-stack-sm block tracking-widest">Our Heritage</span>',
        1,
    )
    html = html.replace(
        'text-h1 font-h1 text-on-primary mb-stack-md">Redefining Freshness</h1>',
        'text-h1 font-h1 text-white mb-stack-md">Redefining Freshness</h1>',
        1,
    )
    html = html.replace(
        "text-body-lg font-body-lg text-on-primary-container max-w-2xl mx-auto opacity-90",
        "text-body-lg font-body-lg text-white max-w-2xl mx-auto opacity-90",
        1,
    )
    html = html.replace('The Artisans', 'Our Team', 1)
    html = html.replace("Sarah Thompson", "Akosua Mensah", 1)
    html = html.replace("James Miller", "Kofi Owusu", 1)
    html = html.replace("Elena Rossi", "Abena Serwaa", 1)
    html = re.sub(
        r'(<img class="w-48 h-48 rounded-full object-cover mx-auto mb-stack-md border-4 border-primary/10"[^>]*?src=")([^"]+)(")',
        r"\1" + ASSET_PERSON + r"\3",
        html,
        count=4,
    )
    return html


def _shop_product_card(
    badge_classes: str,
    badge: str,
    title: str,
    category: str,
    subtitle: str,
    price: str,
    rating: str,
    img_alt: str,
    img_src: str,
) -> str:
    return f"""<a href="{U["pdp"]}" class="bg-white dark:bg-surface-container-lowest rounded-2xl overflow-hidden shadow-sm hover:shadow-md transition-shadow group ek-product-card border border-outline-variant/20 block text-inherit no-underline hover:no-underline">
<div class="relative aspect-[4/5] md:aspect-auto md:h-64 overflow-hidden">
<img alt="{title}" class="w-full h-full object-cover transition-transform duration-500 group-hover:scale-105" src="{img_src}" data-alt="{img_alt}" loading="lazy"/>
<div class="absolute top-4 left-4 {badge_classes} font-label-caps px-3 py-1 rounded-full uppercase">{badge}</div>
<span class="absolute bottom-4 right-4 bg-white/90 p-2 rounded-full text-primary shadow-sm" aria-hidden="true">
<span class="material-symbols-outlined" data-icon="add_shopping_cart">add_shopping_cart</span>
</span>
</div>
<div class="p-stack-md">
<h4 class="font-h4 text-h4 mb-1">{title}</h4>
<p class="text-label-caps text-primary font-semibold tracking-wide text-[11px] mb-1">{category}</p>
<p class="text-sm text-on-surface-variant mb-3 line-clamp-2">{subtitle}</p>
<div class="flex justify-between items-center gap-2 min-w-0">
<span class="font-price-lg text-price-lg text-primary ek-product-price shrink-0">{price}</span>
<div class="flex items-center gap-1 shrink-0">
<span class="material-symbols-outlined text-secondary text-sm" data-icon="star" data-weight="fill">star</span>
<span class="text-sm font-bold">{rating}</span>
</div>
</div>
</div>
</a>"""


PLP_SPECS_MAIN = [
    (
        "bg-tertiary-fixed text-on-tertiary-fixed",
        "Same Day",
        "Beef Chunks (Stew Cut)",
        "Beef",
        "1kg · bone-in · ready for light soup",
        "GHS 42.00",
        "4.9",
        "Stew beef",
        PD_BEEF,
    ),
    (
        "bg-secondary-fixed text-on-secondary-fixed",
        "Chilled",
        "Tenderloin Portion",
        "Beef",
        "450g · trimmed steak cut",
        "GHS 38.50",
        "4.8",
        "Fillet cut",
        PD_TBONE,
    ),
    (
        "bg-tertiary-fixed text-on-tertiary-fixed",
        "Same Day",
        "Minced Beef (Khebab Mix)",
        "Beef",
        "1kg · chilled grind",
        "GHS 12.00",
        "5.0",
        "Minced beef",
        PD_BEEF,
    ),
    (
        "bg-tertiary-fixed text-on-tertiary-fixed",
        "Same Day",
        "T-Bone (Local Cut)",
        "Beef",
        "950g · bone-in",
        "GHS 52.00",
        "4.7",
        "T-bone",
        PD_TBONE,
    ),
    (
        "bg-secondary-fixed text-on-secondary-fixed",
        "Chilled",
        "Bone-In Short Ribs",
        "Beef",
        "1.2kg · braising cut",
        "GHS 29.00",
        "4.8",
        "Short ribs",
        PD_RIBS,
    ),
    (
        "bg-outline text-surface-container-lowest",
        "Frozen",
        "Brisket & Plate",
        "Beef",
        "4.5kg · slow-cook cut",
        "GHS 85.00",
        "4.9",
        "Brisket",
        PD_RIBS,
    ),
]

PLP_SPECS_GOAT = [
    (
        "bg-secondary-fixed text-on-secondary-fixed",
        "Chilled",
        "Tender Goat Stew Cuts",
        "Goat",
        "1kg · bone-in · pasture-raised",
        "GHS 18.99",
        "5.0",
        "Goat stew",
        ASSET_GOAT,
    ),
    (
        "bg-tertiary-fixed text-on-tertiary-fixed",
        "Same Day",
        "Goat Shoulder Roast",
        "Goat",
        "1.5kg · bone-in",
        "GHS 24.50",
        "4.8",
        "Goat shoulder",
        ASSET_GOAT,
    ),
    (
        "bg-primary-fixed text-on-primary-fixed",
        "New",
        "Goat Ribs Rack",
        "Goat",
        "800g · frenched rack",
        "GHS 32.00",
        "4.7",
        "Goat ribs",
        PD_GOAT,
    ),
]

PLP_SPECS_CHICKEN = [
    (
        "bg-secondary-fixed text-on-secondary-fixed",
        "Organic",
        "Free-Range Chicken Thighs",
        "Chicken",
        "1kg · skin-on",
        "GHS 12.50",
        "4.8",
        "Chicken thighs",
        ASSET_CHICKEN,
    ),
    (
        "bg-tertiary-fixed text-on-tertiary-fixed",
        "Same Day",
        "Whole Free-Range Chicken",
        "Chicken",
        "1.4kg · cleaned",
        "GHS 22.00",
        "4.9",
        "Whole chicken",
        ASSET_CHICKEN,
    ),
    (
        "bg-secondary-fixed text-on-secondary-fixed",
        "Chilled",
        "Chicken Drumsticks Pack",
        "Chicken",
        "900g · 6 pieces",
        "GHS 9.50",
        "4.6",
        "Drumsticks",
        ASSET_CHICKEN,
    ),
]

PLP_SPECS_SPECIAL = [
    (
        "bg-primary-fixed text-on-primary-fixed",
        "New arrival",
        "Crown Roast of Lamb",
        "Special cuts",
        "2.5kg · seasonal",
        "GHS 65.00",
        "4.7",
        "Lamb crown",
        ASSET_SPECIAL_CUTS,
    ),
    (
        "bg-tertiary-fixed text-on-tertiary-fixed",
        "Aged",
        "Bone-In Marbled Steak",
        "Special cuts",
        "450g · rich marbling",
        "GHS 89.00",
        "4.9",
        "Marbled steak",
        PD_TBONE,
    ),
    (
        "bg-secondary-fixed text-on-secondary-fixed",
        "Limited",
        "Tomahawk Steak",
        "Special cuts",
        "1.1kg · long bone",
        "GHS 95.00",
        "5.0",
        "Tomahawk",
        PD_TBONE,
    ),
    (
        "bg-outline text-surface-container-lowest",
        "Reserve",
        "Dry-Aged Porterhouse",
        "Special cuts",
        "800g · 28-day age",
        "GHS 72.00",
        "4.8",
        "Porterhouse",
        PD_BEEF,
    ),
]

CATEGORY_PLP_SPECS: dict[str, list[tuple]] = {
    "category_beef_elikhope_farms": PLP_SPECS_MAIN,
    "category_goat_elikhope_farms": PLP_SPECS_GOAT,
    "category_chicken_elikhope_farms": PLP_SPECS_CHICKEN,
    "category_special_elikhope_farms": PLP_SPECS_SPECIAL,
}

CATEGORY_PLP_HEADLINE = {
    "category_beef_elikhope_farms": "Beef · All products",
    "category_goat_elikhope_farms": "Goat · All products",
    "category_chicken_elikhope_farms": "Chicken · All products",
    "category_special_elikhope_farms": "Special cuts · All products",
}


def patch_shop_browse_product_grid(html: str, parent: str = "elikhope_farms_browse_products") -> str:
    """Unify PLP cards; optional category-specific grids for category_* folder clones."""
    specs = CATEGORY_PLP_SPECS.get(parent, PLP_SPECS_MAIN)
    body = "\n".join(_shop_product_card(*s) for s in specs)
    grid_tag = '<div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-gutter" data-ek-product-grid>'
    pag_tail = r'(</div>\s*<!-- Pagination -->)'
    if "data-ek-product-grid" in html:
        html = re.sub(
            r'(?is)(<div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-gutter" data-ek-product-grid>)[\s\S]*?'
            + pag_tail,
            r"\1\n" + body + r"\n\2",
            html,
            count=1,
        )
    else:
        html = re.sub(
            r'(?is)(<div class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-gutter">)\s*<!-- Product Card 1 -->[\s\S]*?'
            + pag_tail,
            grid_tag + "\n" + body + r"\n\2",
            html,
            count=1,
        )
        if "data-ek-product-grid" not in html:
            html = re.sub(
                r'(?is)(<div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-gutter">)[\s\S]*?'
                + pag_tail,
                grid_tag + "\n" + body + r"\n\2",
                html,
                count=1,
            )
    headline = CATEGORY_PLP_HEADLINE.get(parent)
    if headline:
        html = html.replace("Premium Beef Selection", headline, 1)
    return html


def patch_home_bestseller_cards(html: str, current_url: str | None) -> str:
    if not current_url or "elikhope_farms_home_page" not in current_url:
        return html
    html = html.replace(
        '<h4 class="font-h4 text-h4 mb-1">Premium Angus Ribeye</h4>',
        '<h4 class="font-h4 text-h4 mb-1">Local Beef Chunks (Stew)</h4>',
        1,
    )
    html = html.replace(
        '<div class="bg-white rounded-2xl overflow-hidden shadow-sm hover:shadow-md transition-shadow group">',
        f'<a href="{U["pdp"]}" class="bg-white rounded-2xl overflow-hidden shadow-sm hover:shadow-md transition-shadow group ek-product-card border border-outline-variant/20 block text-inherit no-underline hover:no-underline">',
        4,
    )
    html = html.replace(
        '<div class="relative h-64 overflow-hidden">',
        '<div class="relative aspect-[4/5] md:aspect-auto md:h-64 overflow-hidden">',
        4,
    )
    html = html.replace(
        '<span class="font-price-lg text-price-lg text-primary">',
        '<span class="font-price-lg text-price-lg text-primary ek-product-price">',
        4,
    )
    html = html.replace(
        '<button class="absolute bottom-4 right-4 bg-white/90 p-2 rounded-full text-primary hover:bg-primary hover:text-white transition-colors">',
        '<span class="absolute bottom-4 right-4 bg-white/90 p-2 rounded-full text-primary shadow-sm" aria-hidden="true">',
        4,
    )
    html = html.replace(
        '<span class="material-symbols-outlined" data-icon="add_shopping_cart">add_shopping_cart</span>\n</button>',
        '<span class="material-symbols-outlined" data-icon="add_shopping_cart">add_shopping_cart</span>\n</span>',
        4,
    )
    html = html.replace(
        '<div class="flex justify-between items-center">',
        '<div class="flex justify-between items-center gap-2 min-w-0">',
        4,
    )
    html = html.replace("</div>\n</div>\n</div>\n<!-- Product 2 -->", "</div>\n</div>\n</a>\n<!-- Product 2 -->", 1)
    html = html.replace("</div>\n</div>\n</div>\n<!-- Product 3 -->", "</div>\n</div>\n</a>\n<!-- Product 3 -->", 1)
    html = html.replace("</div>\n</div>\n</div>\n<!-- Product 4 -->", "</div>\n</div>\n</a>\n<!-- Product 4 -->", 1)
    html = html.replace(
        "</div>\n</div>\n</div>\n</div>\n</div>\n</section>\n<!-- Section 5:",
        "</div>\n</div>\n</a>\n</div>\n</div>\n</section>\n<!-- Section 5:",
        1,
    )
    cat_line = 'text-label-caps text-primary font-semibold tracking-wide text-[11px] mb-1'
    for title, cat in (
        ("Local Beef Chunks (Stew)", "Beef"),
        ("Free-Range Chicken Thighs", "Chicken"),
        ("Tender Goat Stew Cuts", "Goat"),
        ("Crown Roast of Lamb", "Special cuts"),
    ):
        h = f'<h4 class="font-h4 text-h4 mb-1">{title}</h4>'
        tagged = f'{h}\n<p class="{cat_line}">{cat}</p>'
        if h in html and tagged not in html:
            html = html.replace(h, tagged, 1)
    for cat in ("Beef", "Chicken", "Goat", "Special cuts"):
        html = re.sub(
            r'(?:<p class="text-label-caps text-primary font-semibold tracking-wide text-\[11px\] mb-1">'
            + re.escape(cat)
            + r"</p>\n){2,}",
            f'<p class="{cat_line}">{cat}</p>\n',
            html,
        )
    html = patch_home_bestseller_product_images(html, current_url)
    return html


def patch_home_bestseller_product_images(html: str, current_url: str | None) -> str:
    """Force correct /assets shots for each weekly bestseller card (idempotent)."""
    if not current_url or "elikhope_farms_home_page" not in current_url:
        return html
    fixes = (
        (1, PD_BEEF),
        (2, PD_CHICKEN),
        (3, PD_GOAT),
        (4, PD_SPECIAL),
    )
    for n, src in fixes:
        html = re.sub(
            r"(?s)(<!-- Product "
            + str(n)
            + r" -->[\s\S]*?<img[^>]*src=\")([^\"]+)(\")",
            r"\1" + src + r"\3",
            html,
            count=1,
        )
    return html


def patch_marketing_editorial_image_fixes(html: str) -> str:
    """Pin flagship marketing shots to audience-appropriate /assets files (idempotent)."""
    html = re.sub(
        r'(?is)(<img[^>]*data-alt="[^"]*\bmaster butcher\b[^"]*"[^>]*src=")([^"]+)(")',
        r"\1" + ASSET_PERSON_CUTTING + r"\3",
        html,
        count=1,
    )
    html = re.sub(
        r'(?is)(<img[^>]*data-alt="[^"]*\bmarbled raw ribeye\b[^"]*"[^>]*src=")([^"]+)(")',
        r"\1" + PD_BEEF + r"\3",
        html,
        count=1,
    )
    return html


def patch_home_category_tiles(html: str, current_url: str | None) -> str:
    if not current_url or "elikhope_farms_home_page" not in current_url:
        return html
    bf = ASSET_MEAT_SMILING
    gf = ASSET_GOAT
    cf = ASSET_CHICKEN
    sf = ASSET_SPECIAL_CUTS
    sec = f"""<!-- Section 3: Category Grid -->
<section class="py-stack-lg px-margin-desktop max-w-container-max mx-auto" data-ek-category-tiles>
<div class="flex justify-between items-end mb-stack-md flex-col sm:flex-row gap-4 sm:gap-0 sm:items-end">
<div>
<h2 class="font-h2 text-h2 text-on-surface">Curated Categories</h2>
<p class="font-body-md text-on-surface-variant mt-2">Explore our premium selection of ethically sourced cuts.</p>
</div>
<a class="text-primary font-bold hover:underline shrink-0" href="{U["categories_hub"]}">View all categories →</a>
</div>
<div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-gutter">
<a href="{U["cat_beef"]}" class="group relative h-80 rounded-2xl overflow-hidden cursor-pointer shadow-sm block no-underline text-inherit hover:no-underline">
<img class="absolute inset-0 w-full h-full object-cover transition-transform duration-500 group-hover:scale-110" alt="" src="{bf}"/>
<div class="absolute inset-0 bg-gradient-to-t from-black/70 to-transparent"></div>
<div class="absolute bottom-6 left-6 text-white">
<h3 class="font-h3 text-h3 mb-1">Beef</h3>
<p class="text-sm opacity-80">Prime Steaks &amp; Roasts</p>
</div>
</a>
<a href="{U["cat_goat"]}" class="group relative h-80 rounded-2xl overflow-hidden cursor-pointer shadow-sm block no-underline text-inherit hover:no-underline">
<img class="absolute inset-0 w-full h-full object-cover transition-transform duration-500 group-hover:scale-110" alt="" src="{gf}"/>
<div class="absolute inset-0 bg-gradient-to-t from-black/70 to-transparent"></div>
<div class="absolute bottom-6 left-6 text-white">
<h3 class="font-h3 text-h3 mb-1">Goat</h3>
<p class="text-sm opacity-80">Tender Highland Cuts</p>
</div>
</a>
<a href="{U["cat_chicken"]}" class="group relative h-80 rounded-2xl overflow-hidden cursor-pointer shadow-sm block no-underline text-inherit hover:no-underline">
<img class="absolute inset-0 w-full h-full object-cover transition-transform duration-500 group-hover:scale-110" alt="" src="{cf}"/>
<div class="absolute inset-0 bg-gradient-to-t from-black/70 to-transparent"></div>
<div class="absolute bottom-6 left-6 text-white">
<h3 class="font-h3 text-h3 mb-1">Chicken</h3>
<p class="text-sm opacity-80">Free-range &amp; Organic</p>
</div>
</a>
<a href="{U["cat_special"]}" class="group relative h-80 rounded-2xl overflow-hidden cursor-pointer shadow-sm block no-underline text-inherit hover:no-underline">
<img class="absolute inset-0 w-full h-full object-cover transition-transform duration-500 group-hover:scale-110" alt="" src="{sf}"/>
<div class="absolute inset-0 bg-gradient-to-t from-black/70 to-transparent"></div>
<div class="absolute bottom-6 left-6 text-white">
<h3 class="font-h3 text-h3 mb-1">Special Cuts</h3>
<p class="text-sm opacity-80">Wagyu &amp; Aged Selections</p>
</div>
</a>
</div>
</section>"""
    html = re.sub(
        r"(?is)<!-- Section 3: Category Grid -->[\s\S]*?</section>\s*(?=<!-- Section 4)",
        sec + "\n",
        html,
        count=1,
    )
    return html


def patch_all_categories_hub_page(html: str) -> str:
    """Single-purpose hub: hero + four category cards (idempotent)."""
    block = f"""
<section class="py-stack-lg px-margin-mobile md:px-margin-desktop max-w-container-max mx-auto" data-ek-all-categories>
<div class="max-w-container-max mx-auto mb-stack-lg">
<h1 class="font-h1 text-h1 text-on-surface">All categories</h1>
<p class="font-body-md text-on-surface-variant mt-2 max-w-2xl">Browse by animal or special cuts — each category shows every product we list online.</p>
<p class="mt-4"><a href="{U["shop_home"]}" class="text-primary font-bold hover:underline">← Back to full shop</a></p>
</div>
<div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-gutter">
<a href="{U["cat_beef"]}" class="group relative h-72 sm:h-80 rounded-2xl overflow-hidden cursor-pointer shadow-sm block no-underline text-inherit">
<img alt="" class="absolute inset-0 w-full h-full object-cover transition-transform duration-500 group-hover:scale-110" src="{ASSET_MEAT_SMILING}"/>
<div class="absolute inset-0 bg-gradient-to-t from-black/70 to-transparent"></div>
<div class="absolute bottom-6 left-6 text-white">
<h2 class="font-h3 text-h3 mb-1">Beef</h2>
<p class="text-sm opacity-80">Prime steaks &amp; roasts</p>
</div>
</a>
<a href="{U["cat_goat"]}" class="group relative h-72 sm:h-80 rounded-2xl overflow-hidden cursor-pointer shadow-sm block no-underline text-inherit">
<img alt="" class="absolute inset-0 w-full h-full object-cover transition-transform duration-500 group-hover:scale-110" src="{ASSET_GOAT}"/>
<div class="absolute inset-0 bg-gradient-to-t from-black/70 to-transparent"></div>
<div class="absolute bottom-6 left-6 text-white">
<h2 class="font-h3 text-h3 mb-1">Goat</h2>
<p class="text-sm opacity-80">Tender highland cuts</p>
</div>
</a>
<a href="{U["cat_chicken"]}" class="group relative h-72 sm:h-80 rounded-2xl overflow-hidden cursor-pointer shadow-sm block no-underline text-inherit">
<img alt="" class="absolute inset-0 w-full h-full object-cover transition-transform duration-500 group-hover:scale-110" src="{ASSET_CHICKEN}"/>
<div class="absolute inset-0 bg-gradient-to-t from-black/70 to-transparent"></div>
<div class="absolute bottom-6 left-6 text-white">
<h2 class="font-h3 text-h3 mb-1">Chicken</h2>
<p class="text-sm opacity-80">Free-range &amp; organic</p>
</div>
</a>
<a href="{U["cat_special"]}" class="group relative h-72 sm:h-80 rounded-2xl overflow-hidden cursor-pointer shadow-sm block no-underline text-inherit">
<img alt="" class="absolute inset-0 w-full h-full object-cover transition-transform duration-500 group-hover:scale-110" src="{ASSET_SPECIAL_CUTS}"/>
<div class="absolute inset-0 bg-gradient-to-t from-black/70 to-transparent"></div>
<div class="absolute bottom-6 left-6 text-white">
<h2 class="font-h3 text-h3 mb-1">Special cuts</h2>
<p class="text-sm opacity-80">Wagyu-style &amp; aged</p>
</div>
</a>
</div>
</section>"""
    block_stripped = block.strip()
    if "data-ek-all-categories" in html:
        html = re.sub(
            r'(?is)<section[^>]*data-ek-all-categories[^>]*>[\s\S]*?</section>',
            block_stripped,
            html,
            count=1,
        )
    else:
        html = re.sub(
            r"(?is)<main class=\"pt-20\">[\s\S]*?</main>",
            f'<main class="pt-20">\n{block}\n</main>',
            html,
            count=1,
        )
    if re.search(r"<title>All categories \| EliKhope Farms</title>", html) is None:
        html = re.sub(
            r"<title>[^<]*</title>",
            "<title>All categories | EliKhope Farms</title>",
            html,
            count=1,
        )
    return html


def patch_visual_gallery_page(html: str) -> str:
    """Gallery hero + Signature Cuts tile imagery."""
    html = re.sub(
        r'(?s)(<!-- Hero Banner -->\s*<section class="relative h-\[[^\]]+\][^>]*>)\s*<img class="absolute inset-0 w-full h-full object-cover"[^>]*src="[^"]*"',
        rf'\1\n<img class="absolute inset-0 w-full h-full object-cover" data-alt="" src="{ASSET_MEAT_BUTCHERY}"',
        html,
        count=1,
    )
    html = re.sub(
        r'(?is)(<img class="w-full h-full object-cover transition-transform duration-500 group-hover:scale-110"[^>]*src=")([^"]+)("/>\s*<div class="absolute inset-0 bg-black/20 opacity-0 group-hover:opacity-100 transition-opacity flex items-end p-stack-md">\s*<span class="text-on-primary font-h4 text-h4">Signature Cuts</span>)',
        rf"\1{PD_SPECIAL}\3",
        html,
        count=1,
    )
    return html


def patch_product_detail_page(html: str) -> str:
    """Ensure PDP has a title, traceability, related strip, review modal; drop bundle upsell."""
    if re.search(r"(?is)<title>[^<]+</title>", html) is None:
        html = re.sub(
            r"(?is)(<meta content=\"width=device-width[^>]*/>)",
            r'\1\n<title>EliKhope Farms | Beef cut detail</title>',
            html,
            count=1,
        )
    if 'class="text-price-lg font-price-lg text-primary ek-pdp-hero-price"' not in html:
        html = html.replace(
            '<div class="text-price-lg font-price-lg text-primary">',
            '<div class="text-price-lg font-price-lg text-primary ek-pdp-hero-price">',
            1,
        )
    html = html.replace(
        '<nav class="flex text-label-caps text-on-surface-variant gap-2">\n<a href="#">Beef</a>',
        f'<nav class="flex text-label-caps text-on-surface-variant gap-2">\n<a class="hover:text-primary" href="{U["plp"]}">Beef</a>',
        1,
    )
    html = html.replace(
        '<a class="text-primary" href="#">Prime Selection</a>',
        f'<a class="text-primary hover:underline" href="{U["categories"]}">Prime cuts</a>',
        1,
    )
    html = re.sub(
        r"(?is)<!-- Frequently Bought Together -->[\s\S]*?</section>\s*(?=<!-- Customer Reviews -->)",
        "",
        html,
        count=1,
    )
    html = html.replace(
        '<button class="bg-secondary-container text-on-secondary-container px-6 py-3 rounded-lg font-semibold hover:opacity-90 transition-all">Write a Review</button>',
        '<button type="button" class="bg-secondary-container text-on-secondary-container px-6 py-3 rounded-lg font-semibold hover:opacity-90 transition-all" data-ek-toggle="ek-review-modal">Write a review</button>',
        1,
    )
    if 'id="ek-review-modal"' not in html:
        review_modal = """
<div id="ek-review-modal" class="hidden fixed inset-0 z-[80] flex items-center justify-center p-4">
<div class="absolute inset-0 bg-black/50" data-ek-toggle="ek-review-modal" aria-label="Close review form"></div>
<div class="relative bg-surface max-w-lg w-full rounded-2xl p-stack-lg shadow-xl border border-outline-variant/40">
<h3 class="font-h3 text-h3 text-on-surface mb-2">Write a review</h3>
<p class="text-body-sm text-on-surface-variant mb-stack-md">Share your experience with this cut. This is a prototype — your note is not submitted anywhere.</p>
<label class="font-label-caps text-on-surface-variant text-xs uppercase block mb-1">Rating</label>
<div class="flex gap-1 mb-4 text-primary" aria-hidden="true">
<span class="material-symbols-outlined">star</span><span class="material-symbols-outlined">star</span><span class="material-symbols-outlined">star</span><span class="material-symbols-outlined">star</span><span class="material-symbols-outlined">star</span>
</div>
<label class="font-label-caps text-on-surface-variant text-xs uppercase block mb-1" for="ek-review-text">Your review</label>
<textarea id="ek-review-text" class="w-full min-h-[120px] rounded-xl border border-outline-variant bg-surface-container-low p-3 text-body-md" placeholder="How was the quality, packaging, and delivery?"></textarea>
<div class="flex justify-end gap-3 mt-stack-md">
<button type="button" class="px-4 py-2 rounded-lg border border-outline-variant font-semibold text-on-surface" data-ek-toggle="ek-review-modal">Cancel</button>
<button type="button" class="px-4 py-2 rounded-lg bg-primary text-on-primary font-semibold" data-ek-toggle="ek-review-modal">Submit</button>
</div>
</div>
</div>"""
        html = html.replace("</body>", review_modal + "\n</body>", 1)
    rib = PD_BEEF
    fillet = PD_TBONE
    goat = PD_GOAT
    related = f"""
<section class="px-margin-mobile md:px-margin-desktop max-w-container-max mx-auto pb-stack-lg" data-ek-pdp-related>
<div class="max-w-container-max mx-auto pt-stack-lg mt-stack-lg border-t border-outline-variant/40">
<h2 class="font-h2 text-h2 text-on-surface mb-stack-md">You may also like</h2>
<div class="grid grid-cols-1 sm:grid-cols-3 gap-gutter">
{_shop_product_card("bg-secondary-fixed text-on-secondary-fixed", "Chilled", "Tenderloin Portion", "Beef", "450g · trimmed cut", "GHS 38.50", "4.8", "", fillet)}
{_shop_product_card("bg-tertiary-fixed text-on-tertiary-fixed", "Bestseller", "Tender Goat Stew", "Goat", "1kg · Bone-in", "GHS 18.99", "5.0", "", goat)}
{_shop_product_card("bg-tertiary-fixed text-on-tertiary-fixed", "Fresh Today", "Local Beef Chunks (Stew)", "Beef", "1kg · Grass-fed", "GHS 24.99", "4.9", "", rib)}
</div>
<p class="text-center mt-stack-md"><a class="text-primary font-bold text-body-sm hover:underline" href="{U["plp"]}">Browse all cuts</a></p>
</div>
</section>"""
    related_stripped = related.strip()
    if "data-ek-pdp-related" in html:
        html = re.sub(
            r'(?is)<section[^>]*data-ek-pdp-related[^>]*>[\s\S]*?</section>',
            related_stripped,
            html,
            count=1,
        )
    else:
        html = html.replace("</main>\n<!-- Footer -->", related + "\n</main>\n<!-- Footer -->", 1)
    html = re.sub(
        r"<title>EliKhope Farms \| [^<]+</title>",
        "<title>EliKhope Farms | Premium beef</title>",
        html,
        count=1,
    )
    html = html.replace(
        ">Premium Ribeye Cut</h1>",
        ">Premium beef</h1>",
        1,
    )
    html = html.replace('alt="Premium Ribeye Cut"', 'alt="Premium beef"', 1)
    html = re.sub(
        r'(<img alt="Premium beef" class="w-full h-full object-cover transition-transform duration-500 ease-out" data-alt=")([^"]*)(" src=")([^"]+)(")',
        rf'\1Premium beef cuts from EliKhope Farms.\3{PD_BEEF}\5',
        html,
        count=1,
    )
    html = re.sub(
        r'(\bdata-alt="Close up thumbnail of a raw ribeye steak[^"]*" src=")([^"]+)(")',
        rf"\1{PD_BEEF}\3",
        html,
        count=1,
    )
    html = re.sub(
        r'(\bdata-alt="Side view of a thick cut ribeye steak[^"]*" src=")([^"]+)(")',
        rf"\1{PD_TBONE}\3",
        html,
        count=1,
    )
    html = re.sub(
        r'(\bdata-alt="A cooked version of the ribeye steak[^"]*" src=")([^"]+)(")',
        rf"\1{PD_RIBS}\3",
        html,
        count=1,
    )
    html = html.replace(
        "Our signature Ribeye is hand-selected for superior marbling and aged for 21 days. Sourced from grass-fed cattle raised on our sustainable valley pastures.",
        "Our premium beef is hand-selected for consistent quality. Sourced from cattle raised on partner farms across Ghana with the hygiene and cold-chain standards you expect from EliKhope Farms.",
        1,
    )
    html = html.replace(
        '"Best Ribeye I\'ve had in years. The marbling is consistent throughout, and you can really taste the grass-fed quality. Excellent delivery and packaging."',
        '"Best beef I\'ve had in years. The texture is consistent, and you can really taste the quality. Excellent delivery and packaging."',
        1,
    )
    html = re.sub(
        r'(\bdata-alt="A panoramic wide-angle shot of a lush, rolling green valley[^"]*" src=")([^"]+)(")',
        rf"\1{PD_BEEF}\3",
        html,
        count=1,
    )
    html = html.replace(
        "Temperature controlled dry-aging for 21 days.",
        "Temperature-controlled processing under HACCP standards.",
        1,
    )
    html = html.replace(
        '"Best cooked medium-rare to let the marbling melt and baste the meat from within."',
        '"Best cooked medium-rare so the juices stay in the cut."',
        1,
    )
    return html


def patch_home_hero_slider(html: str, current_url: str | None) -> str:
    """Home only: 3-image hero carousel; remove Est. line from hero copy."""
    if not current_url or "elikhope_farms_home_page" not in current_url:
        return html
    s1 = ASSET_MEAT_BUTCHERY
    s2 = ASSET_MEAT_COLD_ROOM
    s3 = AUTH_CUSTOMER_AUTH_HERO_IMG
    hero = f"""<!-- Section 1: Hero -->
<section class="relative w-full h-[870px] flex items-center overflow-hidden bg-black min-h-[460px]" data-ek-home-hero-slider>
<div class="absolute inset-0 z-0" aria-hidden="true">
<div class="absolute inset-0 transition-opacity duration-1000 ease-out opacity-100" data-ek-hero-slide>
<img class="absolute inset-0 w-full h-full object-cover" alt="" src="{s1}" width="1600" height="900"/>
<div class="absolute inset-0 bg-gradient-to-r from-black/65 via-black/45 to-transparent"></div>
</div>
<div class="absolute inset-0 transition-opacity duration-1000 ease-out opacity-0" data-ek-hero-slide>
<img class="absolute inset-0 w-full h-full object-cover" alt="" src="{s2}" width="1600" height="900"/>
<div class="absolute inset-0 bg-gradient-to-r from-black/65 via-black/45 to-transparent"></div>
</div>
<div class="absolute inset-0 transition-opacity duration-1000 ease-out opacity-0" data-ek-hero-slide>
<img class="absolute inset-0 w-full h-full object-cover" alt="" src="{s3}" width="1600" height="900"/>
<div class="absolute inset-0 bg-gradient-to-r from-black/65 via-black/45 to-transparent"></div>
</div>
</div>
<button type="button" class="absolute left-2 sm:left-4 top-1/2 -translate-y-1/2 z-20 w-10 h-10 sm:w-12 sm:h-12 rounded-full bg-black/35 hover:bg-black/50 text-white flex items-center justify-center border border-white/30 backdrop-blur-sm transition-colors" data-ek-hero-prev aria-label="Previous slide">
<span class="material-symbols-outlined text-2xl">chevron_left</span>
</button>
<button type="button" class="absolute right-2 sm:right-4 top-1/2 -translate-y-1/2 z-20 w-10 h-10 sm:w-12 sm:h-12 rounded-full bg-black/35 hover:bg-black/50 text-white flex items-center justify-center border border-white/30 backdrop-blur-sm transition-colors" data-ek-hero-next aria-label="Next slide">
<span class="material-symbols-outlined text-2xl">chevron_right</span>
</button>
<div class="absolute bottom-6 left-1/2 -translate-x-1/2 z-20 flex gap-2" role="tablist" aria-label="Hero slides">
<button type="button" class="w-2.5 h-2.5 rounded-full bg-white transition-all" data-ek-hero-dot="0" aria-label="Slide 1" aria-current="true"></button>
<button type="button" class="w-2.5 h-2.5 rounded-full bg-white/40 hover:bg-white/70 transition-all" data-ek-hero-dot="1" aria-label="Slide 2"></button>
<button type="button" class="w-2.5 h-2.5 rounded-full bg-white/40 hover:bg-white/70 transition-all" data-ek-hero-dot="2" aria-label="Slide 3"></button>
</div>
<div class="relative z-10 px-margin-desktop max-w-container-max mx-auto w-full">
<div class="max-w-2xl text-white">
<h1 class="font-h1 text-h1 mb-6">Premium Farm-to-Table Meat Quality</h1>
<p class="font-body-lg text-body-lg mb-base opacity-90">Experience the difference of ethically raised, fresh daily butchery delivered directly to your doorstep with unmatched hygiene standards.</p>
<div class="flex gap-stack-sm mt-8">
<a href="{U["shop_home"]}" class="inline-block text-center px-8 py-4 bg-primary text-white font-bold rounded-lg hover:scale-105 transition-transform">Shop Now</a>
</div>
</div>
</div>
</section>"""
    html = re.sub(
        r"(?is)<!-- Section 1: Hero -->[\s\S]*?(?=<!-- Section 2: Quality Highlights -->)",
        hero.strip() + "\n",
        html,
        count=1,
    )
    script = r"""<script id="ek-hero-slider-script">
(function(){
  var root=document.querySelector("[data-ek-home-hero-slider]");
  if(!root||root.getAttribute("data-ek-slider-ready"))return;
  root.setAttribute("data-ek-slider-ready","1");
  var slides=[].slice.call(root.querySelectorAll("[data-ek-hero-slide]"));
  var dots=[].slice.call(root.querySelectorAll("[data-ek-hero-dot]"));
  var prev=root.querySelector("[data-ek-hero-prev]");
  var next=root.querySelector("[data-ek-hero-next]");
  var idx=0,timer;
  function show(n){
    n=(n+slides.length)%slides.length;
    idx=n;
    slides.forEach(function(el,i){
      el.classList.toggle("opacity-100",i===n);
      el.classList.toggle("opacity-0",i!==n);
    });
    dots.forEach(function(d,i){
      var on=i===n;
      d.classList.toggle("bg-white",on);
      d.classList.toggle("bg-white/40",!on);
      if(on)d.setAttribute("aria-current","true");else d.removeAttribute("aria-current");
    });
  }
  function advance(){show(idx+1);}
  if(prev)prev.addEventListener("click",function(){show(idx-1);});
  if(next)next.addEventListener("click",advance);
  dots.forEach(function(d,i){d.addEventListener("click",function(){show(i);});});
  function arm(){clearInterval(timer);timer=setInterval(advance,6500);}
  arm();
  root.addEventListener("mouseenter",function(){clearInterval(timer);});
  root.addEventListener("mouseleave",arm);
})();
</script>"""
    if 'id="ek-hero-slider-script"' not in html:
        html = html.replace("</body>", script + "\n</body>", 1)
    return html


def patch_marketing_page(html: str, current_url: str | None = None) -> str:
    # Strip any previously injected mobile site drawer to keep idempotent.
    html = re.sub(r'(?is)<div id="ek-site-drawer"[^>]*>[\s\S]*?</aside>\s*</div>', "", html)
    # Strip leftover empty <!-- TopNavBar --> comment runs from prior passes.
    html = re.sub(r"(?is)(?:<!--\s*TopNavBar\s*-->\s*){2,}", "<!-- TopNavBar -->\n", html)
    # Replace inconsistent exported top bars with our canonical marketing nav.
    new_html, n = re.subn(
        r"(?is)<!--\s*Top(NavBar|AppBar)\s*-->\s*<(header|nav)[^>]*fixed top-0[^>]*>[\s\S]*?</\2>",
        marketing_top_nav(),
        html,
        count=1,
    )
    if n == 0:
        new_html, n = re.subn(
            r"(?is)<(header|nav)[^>]*class=\"[^\"]*fixed top-0[^\"]*w-full[^\"]*z-50[^\"]*\"[^>]*>[\s\S]*?</\1>",
            marketing_top_nav(),
            html,
            count=1,
        )
    html = new_html
    # Inject the mobile drawer exactly once, right after the new nav.
    html = re.sub(
        r"(?is)(<!--\s*TopNavBar\s*-->\s*<nav[^>]*fixed top-0[\s\S]*?</nav>)",
        r"\1\n" + mobile_site_drawer(),
        html,
        count=1,
    )
    if current_url:
        active_href = current_url
        if f'href="{active_href}"' not in html:
            # Map pages that don't have a 1:1 menu item.
            if "shop" in active_href:
                active_href = U["shop_home"]
        # Set active nav state by matching href= active_href
        html = re.sub(
            r'(<a class=")([^"]*)(" href="' + re.escape(active_href) + r'">)',
            r'\1font-body-md text-body-md text-primary font-semibold border-b-2 border-primary pb-1\3',
            html,
            count=1,
        )
    html = replace_or_append_footer(html, MARKETING_FOOTER)
    html = html.replace(
        '<button class="px-8 py-4 bg-primary text-white font-bold rounded-lg hover:scale-105 transition-transform">Shop Now</button>',
        f'<a href="{U["shop_home"]}" class="inline-block text-center px-8 py-4 bg-primary text-white font-bold rounded-lg hover:scale-105 transition-transform">Shop Now</a>',
        1,
    )
    html = html.replace(
        '<button class="px-8 py-4 border-2 border-white text-white font-bold rounded-lg hover:bg-white hover:text-primary transition-colors">View All Cuts</button>',
        "",
        1,
    )
    # If it already exists as a link (from a previous run), remove it too.
    html = html.replace(
        f'<a href="{U["categories"]}" class="inline-block text-center px-8 py-4 border-2 border-white text-white font-bold rounded-lg hover:bg-white hover:text-primary transition-colors">View all cuts</a>',
        "",
        1,
    )
    # Process / Journey section: hide the master-butcher image on mobile so the
    # numbered steps stand on their own, matching the requested mobile layout.
    html = re.sub(
        r'(?is)<div class="relative">(\s*<img class="rounded-2xl shadow-xl")',
        r'<div class="relative hidden lg:block">\1',
        html,
        count=1,
    )
    html = patch_home_bestseller_cards(html, current_url)
    html = patch_home_category_tiles(html, current_url)
    if current_url and "elikhope_farms_home_page" in current_url:
        html = patch_home_hero_slider(html, current_url)
    if current_url and "elikhope_farms_all_categories" in current_url:
        html = patch_all_categories_hub_page(html)
    if current_url and "elikhope_farms_visual_gallery" in current_url:
        html = patch_visual_gallery_page(html)
    html = patch_marketing_editorial_image_fixes(html)
    html = patch_about_us_page(html, current_url)
    return html


def patch_shop_page(html: str, current_url: str | None = None) -> str:
    # Shop pages should use the same marketing header/nav as Home/About/etc.
    # (Requested to keep nav consistent across the public site.)
    # Strip any previously injected mobile site drawer to keep idempotent.
    html = re.sub(r'(?is)<div id="ek-site-drawer"[^>]*>[\s\S]*?</aside>\s*</div>', "", html)
    html = re.sub(r"(?is)(?:<!--\s*TopNavBar\s*-->\s*){2,}", "<!-- TopNavBar -->\n", html)
    new_html, n = re.subn(
        r"(?is)<!--\s*Top(NavBar|AppBar)\s*-->\s*<(header|nav)[^>]*fixed top-0[^>]*>[\s\S]*?</\2>",
        marketing_top_nav(),
        html,
        count=1,
    )
    if n == 0:
        new_html, n = re.subn(
            r"(?is)<(header|nav)[^>]*class=\"[^\"]*fixed top-0[^\"]*w-full[^\"]*z-50[^\"]*\"[^>]*>[\s\S]*?</\1>",
            marketing_top_nav(),
            html,
            count=1,
        )
    html = new_html
    html = re.sub(
        r"(?is)(<!--\s*TopNavBar\s*-->\s*<nav[^>]*fixed top-0[\s\S]*?</nav>)",
        r"\1\n" + mobile_site_drawer(),
        html,
        count=1,
    )
    # Some shop exports use a non-fixed "docked" header.
    html = re.sub(
        r'(?is)<!--\s*TopAppBar\s*-->\s*<header[^>]*\btop-0\b[^>]*\bz-50\b[^>]*>[\s\S]*?</header>',
        marketing_top_nav() + mobile_site_drawer(),
        html,
        count=1,
    )
    # Ensure Shop appears active on browsing pages, but NOT on checkout pages.
    if current_url and "checkout" not in current_url:
        active_href = U["shop_home"]
        html = re.sub(
            r'(<a class=")([^"]*)(" href="' + re.escape(active_href) + r'">)',
            r'\1font-body-md text-body-md text-primary font-semibold border-b-2 border-primary pb-1\3',
            html,
            count=1,
        )

    # Mobile-only: make PLP filters open from left drawer.
    if "<!-- Sidebar Filters -->" in html:
        m = re.search(r"(?is)(<!--\s*Sidebar Filters\s*-->\\s*)(<aside\\b[\\s\\S]*?</aside>)", html)
        if m:
            aside_html = m.group(2)
            # Desktop sidebar: hide on mobile, show on lg+
            if 'class="' in aside_html:
                desktop_aside = re.sub(r'(?is)<aside\\s+class="', '<aside class="hidden lg:block ', aside_html, count=1)
            else:
                desktop_aside = re.sub(r"(?is)<aside\\b", '<aside class="hidden lg:block"', aside_html, count=1)

            inner_m = re.search(r"(?is)<aside\\b[^>]*>([\\s\\S]*?)</aside>", aside_html)
            inner = inner_m.group(1) if inner_m else ""
            mobile_drawer = f"""
<div id="ek-shop-filters" class="lg:hidden hidden fixed inset-0 z-[70]" data-ek-drawer="left">
  <div class="absolute inset-0 bg-black/40" data-ek-toggle="ek-shop-filters" aria-label="Close filters"></div>
  <aside data-ek-drawer-panel class="absolute left-0 top-0 h-full w-80 max-w-[85vw] bg-surface shadow-xl border-r border-outline-variant -translate-x-full transition-transform duration-200 ease-out flex flex-col">
    <div class="p-6 flex items-start justify-between gap-4 border-b border-outline-variant/40">
      <div class="flex-1">
        <p class="text-h4 font-h4 text-on-surface">Filters</p>
        <p class="text-xs text-on-surface-variant mt-1">Refine your selection</p>
      </div>
      <button class="p-2 rounded-lg hover:bg-surface-container" type="button" aria-label="Close filters" data-ek-toggle="ek-shop-filters">
        <i class="fa-solid fa-xmark text-on-surface-variant"></i>
      </button>
    </div>
    <div class="flex-1 overflow-auto p-6 pt-4 space-y-stack-lg">
      {inner}
    </div>
  </aside>
</div>
"""
            html = html.replace(m.group(0), m.group(1) + desktop_aside + mobile_drawer, 1)

            # Insert the mobile filters button just after breadcrumbs nav.
            html = re.sub(
                r"(?is)(<!--\\s*Breadcrumbs\\s*-->\\s*<nav\\b[\\s\\S]*?</nav>)",
                r'\\1\n<div class="lg:hidden flex items-center justify-between mb-stack-md">\n  <button class="inline-flex items-center gap-2 px-4 py-2 rounded-xl border border-outline-variant/50 bg-surface hover:bg-surface-container transition-colors" type="button" data-ek-toggle="ek-shop-filters" aria-label="Open filters">\n    <i class="fa-solid fa-bars"></i>\n    <span class="font-body-sm font-semibold">Filters</span>\n  </button>\n</div>',
                html,
                count=1,
            )

    html = patch_shop_ghana_plp_filters(html)
    html = replace_or_append_footer(html, MARKETING_FOOTER)
    return html


def render_checkout_payment_main() -> str:
    return f"""<main class="pt-24 pb-stack-lg max-w-container-max mx-auto px-margin-desktop">
<div class="grid grid-cols-1 lg:grid-cols-[1fr,360px] gap-gutter items-start">
  <section class="space-y-stack-lg min-w-0">
    <div class="bg-surface-container-lowest border border-outline-variant/30 rounded-2xl p-stack-md shadow-ambient">
      <div class="flex items-center justify-between gap-4">
        <div class="flex items-center gap-3 opacity-90">
          <span class="w-8 h-8 rounded-full bg-primary text-on-primary flex items-center justify-center">
            <span class="material-symbols-outlined text-[18px]" style="font-variation-settings: 'FILL' 1;">check</span>
          </span>
          <span class="text-body-sm font-semibold text-on-surface">Delivery</span>
        </div>
        <div class="h-[2px] flex-1 bg-outline-variant/60"></div>
        <div class="flex items-center gap-3">
          <span class="w-8 h-8 rounded-full bg-primary-container text-on-primary flex items-center justify-center ring-4 ring-primary-fixed-dim/20 font-bold">2</span>
          <span class="text-body-sm font-semibold text-primary">Payment</span>
        </div>
        <div class="h-[2px] flex-1 bg-outline-variant/60"></div>
        <div class="flex items-center gap-3 opacity-70">
          <span class="w-8 h-8 rounded-full bg-surface-container-high text-on-surface-variant flex items-center justify-center font-bold">3</span>
          <span class="text-body-sm font-semibold text-on-surface-variant">Review</span>
        </div>
      </div>
    </div>

    <div class="flex items-center justify-between gap-4">
      <div>
        <h1 class="font-h2 text-h2 text-on-surface">Payment</h1>
        <p class="font-body-sm text-on-surface-variant mt-1">Secure checkout powered by <span class="font-semibold text-on-surface">Paystack</span>.</p>
      </div>
      <span class="inline-flex items-center rounded-full bg-surface-container px-3 py-1 text-[11px] font-semibold text-on-surface-variant border border-outline-variant/40">Paystack</span>
    </div>

    <div class="bg-surface-container-lowest border border-outline-variant/30 rounded-2xl p-stack-md shadow-ambient">
      <h2 class="font-h4 text-h4 mb-stack-sm">Select payment method</h2>
      <div class="grid grid-cols-2 sm:grid-cols-4 gap-base">
        <button class="p-stack-sm rounded-xl bg-surface border border-primary/30 hover:border-primary shadow-sm flex flex-col items-center gap-2 transition-all active:scale-95">
          <span class="material-symbols-outlined text-primary text-3xl">credit_card</span>
          <span class="font-body-sm font-semibold">Card</span>
        </button>
        <button class="p-stack-sm rounded-xl bg-surface border border-outline-variant/40 hover:border-outline shadow-sm flex flex-col items-center gap-2 transition-all active:scale-95">
          <span class="material-symbols-outlined text-on-surface-variant text-3xl">smartphone</span>
          <span class="font-body-sm">Mobile Money</span>
        </button>
        <button class="p-stack-sm rounded-xl bg-surface border border-outline-variant/40 hover:border-outline shadow-sm flex flex-col items-center gap-2 transition-all active:scale-95">
          <span class="material-symbols-outlined text-on-surface-variant text-3xl">account_balance</span>
          <span class="font-body-sm">Bank</span>
        </button>
        <button class="p-stack-sm rounded-xl bg-surface border border-outline-variant/40 hover:border-outline shadow-sm flex flex-col items-center gap-2 transition-all active:scale-95">
          <span class="material-symbols-outlined text-on-surface-variant text-3xl">payments</span>
          <span class="font-body-sm">Cash</span>
        </button>
      </div>
    </div>

    <div class="bg-surface-container-lowest border border-outline-variant/30 rounded-2xl p-stack-md shadow-ambient">
      <div class="flex items-center justify-between mb-stack-md">
        <h2 class="font-h4 text-h4">Card details</h2>
        <span class="inline-flex items-center rounded-full bg-surface-container px-3 py-1 text-[11px] font-semibold text-on-surface-variant border border-outline-variant/40">Paystack</span>
      </div>
      <form class="space-y-stack-md">
        <div class="space-y-2">
          <label class="font-label-caps text-on-surface-variant">Cardholder Name</label>
          <input class="w-full p-4 rounded-lg bg-surface-container-low border border-outline-variant focus:border-primary focus:ring-1 focus:ring-primary outline-none transition-all font-body-md" placeholder="Full name on card" type="text"/>
        </div>
        <div class="space-y-2">
          <label class="font-label-caps text-on-surface-variant">Card Number</label>
          <div class="relative">
            <input class="w-full p-4 rounded-lg bg-surface-container-low border border-outline-variant focus:border-primary focus:ring-1 focus:ring-primary outline-none transition-all font-body-md pl-12" placeholder="0000 0000 0000 0000" type="text"/>
            <span class="material-symbols-outlined absolute left-4 top-1/2 -translate-y-1/2 text-on-surface-variant">lock</span>
          </div>
        </div>
        <div class="grid grid-cols-2 gap-gutter">
          <div class="space-y-2">
            <label class="font-label-caps text-on-surface-variant">Expiry Date</label>
            <input class="w-full p-4 rounded-lg bg-surface-container-low border border-outline-variant focus:border-primary focus:ring-1 focus:ring-primary outline-none transition-all font-body-md" placeholder="MM/YY" type="text"/>
          </div>
          <div class="space-y-2">
            <label class="font-label-caps text-on-surface-variant">CVV</label>
            <div class="relative">
              <input class="w-full p-4 rounded-lg bg-surface-container-low border border-outline-variant focus:border-primary focus:ring-1 focus:ring-primary outline-none transition-all font-body-md" placeholder="***" type="password"/>
              <span class="material-symbols-outlined absolute right-4 top-1/2 -translate-y-1/2 text-on-surface-variant text-sm cursor-help">help</span>
            </div>
          </div>
        </div>
        <label class="flex items-center gap-3 py-2">
          <input checked="" class="w-5 h-5 rounded border-outline-variant text-primary focus:ring-primary" type="checkbox"/>
          <span class="font-body-sm text-on-surface-variant">Save this card for faster checkout next time.</span>
        </label>
      </form>
      <div class="flex items-center justify-between pt-stack-md mt-stack-md border-t border-outline-variant/30">
        <a class="flex items-center gap-2 text-primary font-body-md hover:translate-x-[-4px] transition-transform" href="{U["checkout_delivery"]}">
          <span class="material-symbols-outlined">arrow_back</span>
          <span>Back to delivery</span>
        </a>
        <a href="{U["checkout_review"]}" class="px-6 py-3 bg-primary text-on-primary rounded-xl font-bold shadow-sm hover:bg-primary-container transition-all active:scale-95 inline-flex items-center gap-2">
          Continue to review
          <span class="material-symbols-outlined text-[20px]">arrow_forward</span>
        </a>
      </div>
    </div>
  </section>

  <aside class="sticky top-24 bg-surface-container-lowest border border-outline-variant/30 rounded-2xl p-stack-md shadow-ambient">
    <div class="flex items-center justify-between mb-stack-md">
      <div>
        <h3 class="font-h4 text-h4 text-on-surface">Order summary</h3>
        <p class="text-body-sm text-on-surface-variant">Premium selection</p>
      </div>
      <span class="material-symbols-outlined text-primary">receipt_long</span>
    </div>

    <div class="space-y-3 border-y border-outline-variant/30 py-stack-md">
      <div class="flex justify-between items-center text-on-surface-variant">
        <span class="font-body-sm">Grass-fed Ribeye (1kg)</span>
        <span class="font-body-sm font-semibold">GHS 48.00</span>
      </div>
      <div class="flex justify-between items-center text-on-surface-variant">
        <span class="font-body-sm">Premium lamb chops (500g)</span>
        <span class="font-body-sm font-semibold">GHS 32.00</span>
      </div>
      <div class="flex justify-between items-center text-on-surface-variant">
        <span class="font-body-sm">Delivery fee</span>
        <span class="font-body-sm font-semibold">GHS 5.00</span>
      </div>
    </div>

    <div class="pt-stack-sm">
      <div class="flex justify-between items-end">
        <span class="font-label-caps text-on-surface-variant">Total</span>
        <span class="font-price-lg text-price-lg text-primary">GHS 85.00</span>
      </div>
      <p class="text-[11px] text-on-surface-variant mt-2">Payments are processed securely via Paystack. This is a static prototype.</p>
    </div>
  </aside>
</div>
</main>"""


def render_checkout_delivery_main() -> str:
    return f"""<main class="pt-24 pb-stack-lg max-w-container-max mx-auto px-margin-desktop">
<div class="grid grid-cols-1 lg:grid-cols-[1fr,360px] gap-gutter items-start">
  <section class="space-y-stack-lg min-w-0">
    <div class="bg-surface-container-lowest border border-outline-variant/30 rounded-2xl p-stack-md shadow-ambient">
      <div class="flex items-center justify-between gap-4">
        <div class="flex items-center gap-3">
          <span class="w-8 h-8 rounded-full bg-primary-container text-on-primary flex items-center justify-center ring-4 ring-primary-fixed-dim/20 font-bold">1</span>
          <span class="text-body-sm font-semibold text-primary">Delivery</span>
        </div>
        <div class="h-[2px] flex-1 bg-outline-variant/60"></div>
        <div class="flex items-center gap-3 opacity-70">
          <span class="w-8 h-8 rounded-full bg-surface-container-high text-on-surface-variant flex items-center justify-center font-bold">2</span>
          <span class="text-body-sm font-semibold text-on-surface-variant">Payment</span>
        </div>
        <div class="h-[2px] flex-1 bg-outline-variant/60"></div>
        <div class="flex items-center gap-3 opacity-70">
          <span class="w-8 h-8 rounded-full bg-surface-container-high text-on-surface-variant flex items-center justify-center font-bold">3</span>
          <span class="text-body-sm font-semibold text-on-surface-variant">Review</span>
        </div>
      </div>
    </div>

    <div>
      <h1 class="font-h2 text-h2 text-on-surface">Delivery details</h1>
      <p class="font-body-sm text-on-surface-variant mt-1">Choose an address, delivery method, and a preferred time slot for Accra.</p>
    </div>

    <div class="bg-surface-container-lowest border border-outline-variant/30 rounded-2xl p-stack-md shadow-ambient">
      <div class="flex items-center justify-between gap-4 mb-stack-md">
        <div class="flex items-center gap-2">
          <span class="material-symbols-outlined text-primary" style="font-variation-settings: 'FILL' 1;">person_pin_circle</span>
          <h2 class="font-h4 text-h4">Delivery address</h2>
        </div>
        <a class="text-primary font-semibold text-body-sm hover:underline" href="{U["addresses"]}">Manage addresses</a>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 gap-gutter mb-stack-lg">
        <button type="button" class="text-left relative p-stack-md border-2 border-primary-container bg-primary/5 rounded-2xl">
          <div class="flex justify-between items-start mb-base">
            <span class="material-symbols-outlined text-primary-container">home</span>
            <span class="material-symbols-outlined text-primary-container" style="font-variation-settings: 'FILL' 1;">check_circle</span>
          </div>
          <p class="font-bold text-on-surface">Home</p>
          <p class="text-body-sm text-on-surface-variant">42 Farmview Lane, East Legon, Accra</p>
          <p class="text-xs text-on-surface-variant mt-2">+233 24 123 4567</p>
        </button>
        <button type="button" class="text-left p-stack-md border border-outline-variant/40 rounded-2xl hover:border-outline transition-colors">
          <div class="flex justify-between items-start mb-base">
            <span class="material-symbols-outlined text-on-surface-variant">add_location_alt</span>
          </div>
          <p class="font-bold text-on-surface">Add new address</p>
          <p class="text-body-sm text-on-surface-variant">Set up a new delivery location for your orders.</p>
        </button>
      </div>

      <form class="grid grid-cols-1 md:grid-cols-2 gap-gutter">
        <div class="flex flex-col gap-base">
          <label class="font-label-caps text-on-surface-variant">Full name</label>
          <input class="w-full p-stack-sm rounded-lg bg-surface-container-low border border-outline-variant focus:border-primary-container focus:ring-1 focus:ring-primary-container transition-all" placeholder="Jonathan Mensah" type="text"/>
        </div>
        <div class="flex flex-col gap-base">
          <label class="font-label-caps text-on-surface-variant">Phone number</label>
          <input class="w-full p-stack-sm rounded-lg bg-surface-container-low border border-outline-variant focus:border-primary-container focus:ring-1 focus:ring-primary-container transition-all" placeholder="+233 24 123 4567" type="tel"/>
        </div>
        <div class="md:col-span-2 flex flex-col gap-base">
          <label class="font-label-caps text-on-surface-variant">Delivery address</label>
          <input class="w-full p-stack-sm rounded-lg bg-surface-container-low border border-outline-variant focus:border-primary-container focus:ring-1 focus:ring-primary-container transition-all" placeholder="Street name and number" type="text"/>
        </div>
        <div class="flex flex-col gap-base">
          <label class="font-label-caps text-on-surface-variant">City / region</label>
          <input class="w-full p-stack-sm rounded-lg bg-surface-container-low border border-outline-variant focus:border-primary-container focus:ring-1 focus:ring-primary-container transition-all" placeholder="Greater Accra" type="text"/>
        </div>
        <div class="flex flex-col gap-base">
          <label class="font-label-caps text-on-surface-variant">Apartment / building (optional)</label>
          <input class="w-full p-stack-sm rounded-lg bg-surface-container-low border border-outline-variant focus:border-primary-container focus:ring-1 focus:ring-primary-container transition-all" placeholder="Suite 4B" type="text"/>
        </div>
        <div class="md:col-span-2 flex flex-col gap-base">
          <label class="font-label-caps text-on-surface-variant">Delivery instructions</label>
          <textarea class="w-full p-stack-sm rounded-lg bg-surface-container-low border border-outline-variant focus:border-primary-container focus:ring-1 focus:ring-primary-container transition-all" placeholder="Drop at the gate, call upon arrival..." rows="3"></textarea>
        </div>
      </form>

      <div class="mt-stack-lg">
        <p class="font-label-caps text-on-surface-variant mb-base">Location preview</p>
        <div class="w-full h-52 rounded-2xl overflow-hidden bg-surface-container shadow-inner border border-outline-variant/30 relative">
          <img alt="Map View" class="w-full h-full object-cover grayscale-[20%]" data-location="Accra" src="https://lh3.googleusercontent.com/aida-public/AB6AXuAHzEp9FOw43r_SVR8odhoWJPHwly9jhC2PIFuXxxdSyCkt4KoY691-tyutSAUTnRbO_h3gTd4aMDBoTsJ9_msc-Vvj_TvG9bz6T4fffwq57UL52fz9Hsy2EgT5qERhQ-YharrET2drl1rrvDm7Ah5DGDKCtjHDaCtnVMQErEJ1TdNM-miZk37wBK7L157sZjtgt3VOIlxpUbV7sI1-NpFzJMjjLGMEINU4EGjVhlt8pyfU90ncbkYvAx3XGLxylHeQUjd_d-97xUI"/>
          <div class="absolute inset-0 flex items-center justify-center pointer-events-none">
            <span class="material-symbols-outlined text-primary text-4xl" style="font-variation-settings: 'FILL' 1;">location_on</span>
          </div>
        </div>
      </div>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-2 gap-gutter">
      <div class="bg-surface-container-lowest border border-outline-variant/30 rounded-2xl p-stack-md shadow-ambient">
        <div class="flex items-center gap-2 mb-stack-md">
          <span class="material-symbols-outlined text-primary">local_shipping</span>
          <h3 class="font-h4 text-h4">Shipping method</h3>
        </div>
        <div class="space-y-base">
          <label class="flex items-center justify-between p-stack-sm border border-primary-container bg-primary/5 rounded-xl cursor-pointer">
            <div class="flex items-center gap-base">
              <input checked="" class="text-primary-container focus:ring-primary-container" name="shipping" type="radio"/>
              <div>
                <p class="font-bold text-on-surface">Standard delivery</p>
                <p class="text-body-sm text-on-surface-variant">2–3 business days</p>
              </div>
            </div>
            <span class="font-bold text-primary-container">FREE</span>
          </label>
          <label class="flex items-center justify-between p-stack-sm border border-outline-variant/40 hover:border-outline transition-colors rounded-xl cursor-pointer">
            <div class="flex items-center gap-base">
              <input class="text-primary-container focus:ring-primary-container" name="shipping" type="radio"/>
              <div>
                <p class="font-bold text-on-surface">Express delivery</p>
                <p class="text-body-sm text-on-surface-variant">Same day (order before 11am)</p>
              </div>
            </div>
            <span class="font-bold text-on-surface">GHS 12.50</span>
          </label>
        </div>
      </div>

      <div class="bg-surface-container-lowest border border-outline-variant/30 rounded-2xl p-stack-md shadow-ambient">
        <div class="flex items-center gap-2 mb-stack-md">
          <span class="material-symbols-outlined text-primary">schedule</span>
          <h3 class="font-h4 text-h4">Select time slot</h3>
        </div>
        <div class="grid grid-cols-2 gap-base">
          <button type="button" class="p-stack-sm rounded-xl border border-primary-container bg-primary/5 text-left">
            <p class="text-xs font-semibold text-on-surface-variant">Tomorrow</p>
            <p class="font-bold text-on-surface">08:00 – 13:00</p>
          </button>
          <button type="button" class="p-stack-sm rounded-xl border border-outline-variant/40 hover:border-outline transition-colors text-left">
            <p class="text-xs font-semibold text-on-surface-variant">Tomorrow</p>
            <p class="font-bold text-on-surface">12:00 – 17:00</p>
          </button>
          <button type="button" class="p-stack-sm rounded-xl border border-outline-variant/40 hover:border-outline transition-colors text-left">
            <p class="text-xs font-semibold text-on-surface-variant">Wed</p>
            <p class="font-bold text-on-surface">08:00 – 13:00</p>
          </button>
          <button type="button" class="p-stack-sm rounded-xl border border-outline-variant/40 hover:border-outline transition-colors text-left">
            <p class="text-xs font-semibold text-on-surface-variant">Wed</p>
            <p class="font-bold text-on-surface">12:00 – 17:00</p>
          </button>
        </div>
      </div>
    </div>

    <div class="bg-surface-container-lowest border border-outline-variant/30 rounded-2xl p-stack-md shadow-ambient">
      <div class="grid grid-cols-1 sm:grid-cols-3 gap-gutter">
        <div class="flex items-center gap-3">
          <span class="material-symbols-outlined text-primary" style="font-variation-settings: 'FILL' 1;">verified_user</span>
          <div>
            <p class="font-body-sm font-bold">Secure delivery</p>
            <p class="text-[10px] text-on-surface-variant leading-tight">Cold-chain packaging</p>
          </div>
        </div>
        <div class="flex items-center gap-3">
          <span class="material-symbols-outlined text-primary" style="font-variation-settings: 'FILL' 1;">grocery</span>
          <div>
            <p class="font-body-sm font-bold">Freshness guarantee</p>
            <p class="text-[10px] text-on-surface-variant leading-tight">Handled with care</p>
          </div>
        </div>
        <div class="flex items-center gap-3">
          <span class="material-symbols-outlined text-primary" style="font-variation-settings: 'FILL' 1;">inventory_2</span>
          <div>
            <p class="font-body-sm font-bold">Hygienic packaging</p>
            <p class="text-[10px] text-on-surface-variant leading-tight">Sealed & labeled</p>
          </div>
        </div>
      </div>
    </div>

    <div class="flex items-center justify-between">
      <a class="flex items-center gap-2 text-primary font-body-md hover:translate-x-[-4px] transition-transform" href="{U["cart"]}">
        <span class="material-symbols-outlined">arrow_back</span>
        <span>Return to cart</span>
      </a>
      <a href="{U["checkout_pay"]}" class="px-6 py-3 bg-primary text-on-primary rounded-xl font-bold shadow-sm hover:bg-primary-container transition-all active:scale-95 inline-flex items-center gap-2">
        Continue to payment
        <span class="material-symbols-outlined text-[20px]">arrow_forward</span>
      </a>
    </div>
  </section>

  <aside class="sticky top-24 bg-surface-container-lowest border border-outline-variant/30 rounded-2xl p-stack-md shadow-ambient">
    <div class="flex items-center justify-between mb-stack-md">
      <div>
        <h3 class="font-h4 text-h4 text-on-surface">Order summary</h3>
        <p class="text-body-sm text-on-surface-variant">Premium selection</p>
      </div>
      <span class="material-symbols-outlined text-primary">receipt_long</span>
    </div>

    <div class="space-y-3 border-y border-outline-variant/30 py-stack-md">
      <div class="flex justify-between items-center text-on-surface-variant">
        <span class="font-body-sm">Premium Ribeye Steak</span>
        <span class="font-body-sm font-semibold">GHS 84.00</span>
      </div>
      <div class="flex justify-between items-center text-on-surface-variant">
        <span class="font-body-sm">Organic Chicken Breast</span>
        <span class="font-body-sm font-semibold">GHS 24.50</span>
      </div>
      <div class="flex justify-between items-center text-on-surface-variant">
        <span class="font-body-sm">Delivery fee</span>
        <span class="font-body-sm font-semibold">FREE</span>
      </div>
    </div>

    <div class="pt-stack-sm">
      <div class="flex justify-between items-end">
        <span class="font-label-caps text-on-surface-variant">Total</span>
        <span class="font-price-lg text-price-lg text-primary">GHS 124.78</span>
      </div>
      <p class="text-[11px] text-on-surface-variant mt-2">You can confirm your delivery details before payment.</p>
    </div>
  </aside>
</div>
</main>"""


def patch_admin_page(path: Path, html: str) -> str:
    folder = path.parent.name
    active = ADMIN_FOLDER_ACTIVE.get(folder, "dashboard")
    # Remove any previously injected admin sidebar/drawer/button blocks (they can duplicate).
    html = re.sub(
        r'(?is)<button class="md:hidden fixed top-\d+ left-\d+[^"]*"[^>]*data-ek-toggle="ek-admin-drawer"[^>]*>[\s\S]*?</button>',
        "",
        html,
    )
    html = re.sub(r'(?is)<div id="ek-admin-drawer"[^>]*>[\s\S]*?</div>', "", html)
    # Remove any stray mobile drawer panels.
    html = re.sub(r'(?is)<aside[^>]*\bdata-ek-drawer-panel\b[^>]*>[\s\S]*?</aside>', "", html)
    html = re.sub(
        r'(?is)<aside[^>]*class="absolute left-0 top-0 h-full w-80[^"]*"[^>]*>[\s\S]*?</aside>',
        "",
        html,
    )
    html = re.sub(
        r"(?is)<aside(?=[^>]*\bw-64\b)(?=[^>]*\bfixed\b)(?=[^>]*\bleft-0\b)[^>]*>[\s\S]*?</aside>",
        "",
        html,
    )
    m = ADMIN_SIDEBAR_RE.search(html)
    if m:
        html = html[: m.start()] + render_admin_sidebar(active) + html[m.end() :]
    else:
        # If sidebar couldn't be detected (after cleanup), inject after <body>.
        html = re.sub(r"(?is)<body([^>]*)>", r"<body\1>\n" + render_admin_sidebar(active), html, count=1)

    # Remove orphaned duplicated "sidebar footer" blocks that show up as repeated green bars.
    html = re.sub(
        r'(?is)<div class="p-4 border-t border-on-surface-variant/10"(?![^>]*data-ek-admin-footer)[^>]*>[\s\S]*?Contact support[\s\S]*?</div>\s*</aside>',
        "",
        html,
    )
    # Some exports contain duplicate sidebar remnants after replacement.
    # Strip any stray sidebar/footer blocks that appear after the first sidebar
    # and before the main content.
    # First, if there are multiple sidebars, keep only the first one.
    html = re.sub(
        r"(?is)^([\s\S]*?</aside>)(?:\s*<aside\b[\s\S]*?</aside>)+",
        r"\1",
        html,
        count=1,
    )
    # Then remove any stray blocks between the sidebar and the top header/main content.
    html = re.sub(
        r"(?is)(</aside>)\s*(?:"
        r"(?:<div[^>]*>[\s\S]*?</div>\s*)|"
        r"(?:</aside>\s*)"
        r")*(?=\s*(?:<!--\s*Top|<!--\s*Main Content|<header\b|<main\b))",
        r"\1\n",
        html,
        count=1,
    )

    # Settings pages: add cross-page tabs.
    if folder in (
        "admin_settings_elikhope_farms_admin",
        "payment_settings_elikhope_farms_admin",
        "delivery_zones_elikhope_farms_admin",
        "staff_permissions_elikhope_farms_admin",
    ):
        tab_active = {
            "admin_settings_elikhope_farms_admin": "general",
            "payment_settings_elikhope_farms_admin": "payments",
            "delivery_zones_elikhope_farms_admin": "zones",
            "staff_permissions_elikhope_farms_admin": "staff",
        }[folder]
        tabs_html = render_admin_settings_tabs(tab_active)

        # Replace existing tab bar on General page if present.
        html = re.sub(
            r'(?is)<div class="flex items-center gap-8 border-b border-surface-variant[^"]*"[^>]*>[\s\S]*?</div>',
            tabs_html,
            html,
            count=1,
        )
        # Otherwise, insert tabs right after the page header block.
        if tabs_html not in html:
            html = re.sub(
                r"(?is)(<h[12] class=\"font-h2 text-h2 text-on-surface\">[\s\S]*?</p>\s*</div>\s*(?:<div class=\"flex[^>]*>[\s\S]*?</div>\s*)?</(?:section|div)>)",
                r"\1\n" + tabs_html,
                html,
                count=1,
            )

        if folder == "delivery_zones_elikhope_farms_admin":
            html = html.replace('data-location="Johannesburg"', 'data-location="Accra"')

    # Payment settings: localize Mobile Money providers (Ghana).
    if folder == "payment_settings_elikhope_farms_admin":
        # Remove payout UI: EliKhope Farms isn't paying out third parties in this model.
        html = re.sub(
            r'(?is)<div class="md:col-span-2 p-6 bg-primary text-on-primary rounded-xl shadow-lg relative overflow-hidden">[\s\S]*?Review Payout Detail</button>[\s\S]*?</div>\s*',
            "",
            html,
            count=1,
        )
        # Remove any leftover decorative icon block from the removed payout card.
        html = re.sub(
            r'(?is)<div class="absolute right-\[-20px\] bottom-\[-20px\] opacity-10">[\s\S]*?</div>\s*</div>',
            "</div>",
            html,
            count=1,
        )
        html = re.sub(
            r'(?is)<div class="absolute right-\[-20px\] bottom-\[-20px\] opacity-10">[\s\S]*?</div>',
            "",
            html,
            count=1,
        )
        # Remove payout wording elsewhere on the page.
        html = html.replace("Instant Payouts", "Instant Settlements")
        html = html.replace("M-Pesa, MTN, Airtel", "MTN, Telecel, AirtelTigo")
        html = html.replace(">M-Pesa<", ">Telecel<")

    # Mobile fix: remove sidebar offset on small screens so admin pages
    # don't horizontally overflow when the desktop sidebar is hidden.
    # Idempotent guards: don't re-match a prefixed `md:ml-64` and don't add
    # `ml-0` if it's already present.
    html = re.sub(
        r'(<main class="(?![^"]*\bml-0\b)[^"]*?)(?<!:)\bml-64\b([^"]*")',
        r"\1md:ml-64 ml-0\2",
        html,
    )
    # Some admin pages use desktop-only horizontal padding inside main; soften it.
    html = re.sub(
        r"(?<!:)(?<!-)\bp-margin-desktop\b",
        "p-margin-mobile md:p-margin-desktop",
        html,
    )
    html = re.sub(
        r"(?<!:)(?<!-)\bpx-margin-desktop\b",
        "px-margin-mobile md:px-margin-desktop",
        html,
    )
    html = re.sub(r"\b(?:p-margin-mobile\s+){2,}", "p-margin-mobile ", html)
    html = re.sub(r"\b(?:px-margin-mobile\s+){2,}", "px-margin-mobile ", html)
    # Reserve space at the top of admin main on mobile so the floating
    # hamburger doesn't overlap the sticky header. Skip if already added.
    html = re.sub(
        r'(<main class="(?![^"]*\bpt-12\b)[^"]*\bml-0\b[^"]*)(min-h-screen[^"]*")',
        r'\1pt-12 md:pt-0 \2',
        html,
        count=1,
    )
    return html


def patch_customer_page(path: Path, html: str) -> str:
    folder = path.parent.name
    active = CUST_FOLDER_ACTIVE.get(folder, "overview")
    # Remove any previously injected customer drawer blocks before re-inserting sidebar.
    html = re.sub(r'(?is)<div id="ek-cust-drawer"[^>]*>[\s\S]*?</div>', "", html)
    html = re.sub(r'(?is)<aside[^>]*\bdata-ek-drawer-panel\b[^>]*>[\s\S]*?</aside>', "", html)
    m = CUSTOMER_SIDEBAR_RE.search(html)
    if not m:
        m = CUSTOMER_SIDEBAR_ALT_RE.search(html)
    if m:
        html = html[: m.start()] + render_customer_sidebar(active) + html[m.end() :]

    # Some exports contain duplicated sidebar blocks; keep only the first injected shell.
    html = re.sub(
        r'(?is)(<!--\s*SideNavBar Shell\s*-->[\s\S]*?id="ek-cust-drawer"[\s\S]*?</div>)(?:\s*<!--\s*SideNavBar Shell\s*-->[\s\S]*?)+(?=\s*(?:<!--\s*TopNavBar Shell\s*-->|<header\b))',
        r"\1",
        html,
    )
    html = re.sub(
        r'(?is)(<aside class="hidden md:flex[\s\S]*?</aside>)(?:\s*<aside class="hidden md:flex[\s\S]*?</aside>)+',
        r"\1",
        html,
    )
    # Remove stray duplicated mobile drawer asides (without data-ek-drawer-panel).
    html = re.sub(
        r'(?is)<aside(?![^>]*\bdata-ek-drawer-panel\b)[^>]*class="absolute left-0 top-0 h-full w-80[\s\S]*?</aside>',
        "",
        html,
    )

    html = CUST_HEADER_RE.sub(customer_top_header(), html, count=1)
    html = CUSTOMER_HEADER_ALT_RE.sub(customer_top_header(), html, count=1)
    # If a page export still has no customer top header, inject ours right
    # before <main>. This ensures pages like recent_purchases get the same
    # header bar as dashboard_overview.
    if "data-ek-cust-header" not in html:
        html = re.sub(
            r"(?is)(<!--\s*Main (?:Canvas|Content)[^>]*-->\s*)?(<main\b)",
            customer_top_header() + r"\n\1\2",
            html,
            count=1,
        )

    # Notifications export sometimes wraps sidebar in an in-flow min-h-screen container,
    # which creates a full-viewport blank spacer above <main> (because sidebar is fixed).
    # Rebuild the block between </header> and the main content marker to contain only
    # the fixed sidebar/drawer shell.
    if folder == "notifications_elikhope_farms":
        html = re.sub(
            r"(?is)(</header>)\s*[\s\S]*?(<!--\s*Main Content Area\s*-->)",
            r"\1\n" + render_customer_sidebar(active) + r"\n\2",
            html,
            count=1,
        )

    # Tracking export uses an in-flow <div class="flex min-h-screen"> wrapper,
    # which creates a blank spacer above <main> (sidebar is fixed).
    if folder == "track_your_delivery_elikhope_farms":
        html = re.sub(
            r"(?is)(</header>)\s*[\s\S]*?(<!--\s*Main Content\s*-->)",
            r"\1\n" + render_customer_sidebar(active) + r"\n\2",
            html,
            count=1,
        )

    # Orders list export often places content below an extra top margin.
    if folder == "my_orders_elikhope_farms":
        html = re.sub(
            r'(<main class="[^"]*)\bmt-16\b([^"]*")',
            r"\1\2",
            html,
        )

    # Remove any previously injected floating hamburger buttons (now in top header).
    html = re.sub(
        r'(?is)<button class="md:hidden fixed top-\d+ left-\d+[^"]*"[^>]*data-ek-toggle="ek-cust-drawer"[^>]*>[\s\S]*?</button>',
        "",
        html,
    )

    # Normalize main canvas spacing for pages that were not exported
    # with the standard `ml-64 pt-16` dashboard shell.
    html = re.sub(
        r'<main class="flex-1 [^"]*">',
        '<main class="ml-64 pt-16 min-h-screen">',
        html,
        count=1,
    )

    # Mobile fix: remove sidebar offset + desktop padding on small screens.
    # Idempotent: only rewrite a bare `ml-64` (not already prefixed with `md:`)
    # and only when `ml-0` isn't already present in the same class list.
    html = re.sub(
        r'(<main class="(?![^"]*\bml-0\b)[^"]*?)(?<!:)\bml-64\b([^"]*")',
        r"\1md:ml-64 ml-0\2",
        html,
    )
    # Ensure every customer dashboard <main> reserves space for the fixed
    # top header (h-16). Skip pages that already include a pt-16/pt-20 token.
    html = re.sub(
        r'(<main class="(?:(?!pt-(?:16|20|24)\b)[^"])*?\bml-0\b)([^"]*")',
        r"\1 pt-16\2",
        html,
        count=1,
    )
    # Many customer pages use a desktop-only padding token; make it responsive.
    # Guard: don't re-prefix tokens that are already part of `md:p-margin-desktop`
    # or that already sit next to `p-margin-mobile`.
    html = re.sub(
        r"(?<!:)(?<!-)\bp-margin-desktop\b",
        "p-margin-mobile md:p-margin-desktop",
        html,
    )
    # Collapse any accidental double-prefix that may have leaked from earlier runs.
    html = re.sub(r"\b(?:p-margin-mobile\s+){2,}", "p-margin-mobile ", html)

    # Fix customer dashboard footers that were still using desktop offset on mobile.
    html = re.sub(
        r'(?is)<footer class="ml-64([^"]*)w-\[calc\(100%-16rem\)\]([^"]*)">',
        r'<footer class="md:ml-64 ml-0\1w-full\2 px-margin-mobile md:px-margin-desktop">',
        html,
        count=1,
    )

    # Remove any floating mobile bottom navigation that appears on top of dashboard pages.
    # These were exported on a few pages (wishlist, addresses) and conflict with the
    # standardized sidebar drawer.
    html = re.sub(
        r'(?is)<!--\s*Mobile Bottom Navigation[\s\S]*?-->\s*',
        "",
        html,
    )
    html = re.sub(
        r'(?is)<nav class="md:hidden fixed bottom-0[^"]*"[^>]*>[\s\S]*?</nav>',
        "",
        html,
    )
    html = re.sub(
        r'(?is)<div class="md:hidden fixed bottom-0[^"]*"[^>]*>[\s\S]*?</div>',
        "",
        html,
    )

    # Some customer dashboard pages should have no footer at all (per design).
    if folder in {
        "track_your_delivery_elikhope_farms",
        "recent_purchases_elikhope_farms",
        "my_orders_elikhope_farms",
        "manage_addresses_elikhope_farms",
        "notifications_elikhope_farms",
    }:
        html = re.sub(
            r"(?is)<footer\b[^>]*>[\s\S]*?</footer>",
            "",
            html,
        )

    # Reduce the order-total price size on mobile so it stays on a single line
    # in the right column of order cards. Add the responsive size override
    # only once.
    if folder in {"my_orders_elikhope_farms", "recent_purchases_elikhope_farms"}:
        html = html.replace(
            'class="text-price-lg font-price-lg text-on-surface">GHS',
            'class="text-h4 font-h4 text-on-surface whitespace-nowrap">GHS',
        )
        # Switch order-status filter pills from wrapping to a single horizontal
        # scrollable row so all four chips remain on one line on mobile.
        html = html.replace(
            '<div class="flex flex-wrap gap-2">\n<button class="px-6 py-2 rounded-full bg-secondary-container text-on-secondary-container font-semibold text-body-sm shadow-sm">All Orders</button>',
            '<div class="flex flex-nowrap gap-2 overflow-x-auto -mx-1 px-1 pb-1">\n<button class="px-6 py-2 rounded-full bg-secondary-container text-on-secondary-container font-semibold text-body-sm shadow-sm whitespace-nowrap">All Orders</button>',
        )
        html = re.sub(
            r'(<button class="px-6 py-2 rounded-full hover:bg-surface-container-high text-on-surface-variant font-medium text-body-sm transition-colors)(">(?:Active|Delivered|Cancelled)</button>)',
            r'\1 whitespace-nowrap\2',
            html,
        )
        # Drop the order-card bottom thumbnail/delivery strip so every card has
        # the same compact layout. The active state is still communicated by
        # the green "Active" pill in the card header.
        html = re.sub(
            r'(?is)<div class="px-6 py-4 bg-surface-container-low/30 flex items-center gap-4 overflow-x-auto no-scrollbar">[\s\S]*?</div>\s*</div>\s*<!-- Order Card 2 -->',
            "</div>\n<!-- Order Card 2 -->",
            html,
        )
        # Stack the right-side block (Order Total + buttons) under the order
        # info on mobile, side-by-side on >= sm.
        html = html.replace(
            '<div class="flex items-center gap-8">',
            '<div class="flex flex-col sm:flex-row sm:items-center gap-stack-sm sm:gap-6 w-full sm:w-auto">',
        )
        html = re.sub(
            r'<div class="flex gap-2">\s*<button class="px-5 py-2\.5 rounded-lg border-1\.5 border-primary text-primary font-semibold text-body-sm hover:bg-primary/5 transition-colors border-\[1\.5px\]">View Details</button>',
            '<div class="flex gap-2 flex-wrap"><button class="flex-1 sm:flex-none px-4 sm:px-5 py-2.5 rounded-lg border-1.5 border-primary text-primary font-semibold text-body-sm hover:bg-primary/5 transition-colors border-[1.5px]">View Details</button>',
            html,
        )

    # Recent purchases / Order history page: make layout stack on mobile.
    if folder == "recent_purchases_elikhope_farms":
        html = re.sub(
            r'(<main class="[^"]*)\bmax-w-container-max\b([^"]*")',
            r"\1w-full max-w-container-max mx-auto\2",
            html,
        )
        html = html.replace(
            '<header class="mb-stack-lg flex justify-between items-end">',
            '<header class="mb-stack-lg flex flex-col md:flex-row md:justify-between md:items-end gap-4">',
        )
        html = re.sub(
            r'(<div class="flex gap-stack-sm")>',
            r'\1 flex-col sm:flex-row w-full sm:w-auto">',
            html,
            count=1,
        )
        html = re.sub(
            r'(?is)<button class="([^"]*)px-4 py-2([^"]*)">\\s*<span class="material-symbols-outlined">filter_list</span>',
            r'<button class="\1px-4 py-3 sm:py-2\2 w-full sm:w-auto justify-center"> <span class="material-symbols-outlined">filter_list</span>',
            html,
            count=1,
        )
        html = re.sub(
            r'(?is)<button class="([^"]*)px-4 py-2([^"]*)bg-primary([^"]*)">\\s*<span class="material-symbols-outlined">download</span>',
            r'<button class="\1px-4 py-3 sm:py-2\2bg-primary\3 w-full sm:w-auto justify-center"> <span class="material-symbols-outlined">download</span>',
            html,
            count=1,
        )
        html = html.replace(
            '<section class="grid grid-cols-12 gap-gutter mb-stack-lg">',
            '<section class="grid grid-cols-1 md:grid-cols-12 gap-gutter mb-stack-lg">',
        )
        html = html.replace('class="col-span-8 ', 'class="col-span-1 md:col-span-8 ')
        html = html.replace('class="col-span-4 ', 'class="col-span-1 md:col-span-4 ')
        html = html.replace(
            '<div class="grid grid-cols-3 gap-stack-md">',
            '<div class="grid grid-cols-1 sm:grid-cols-3 gap-stack-md">',
        )
        html = re.sub(
            r'(<input class=")([^"]*)w-64([^"]*)" placeholder="Search order ID or product\.\.\."',
            r'\1\2w-full sm:w-64\3" placeholder="Search order ID or product..."',
            html,
            count=1,
        )

    # Notifications page: reduce extra top whitespace (pt-16 + p-margin-*)
    if folder == "notifications_elikhope_farms":
        html = re.sub(
            r'(?is)<div class="max-w-\[1280px\] mx-auto [^"]*space-y-stack-lg">',
            '<div class="max-w-[1280px] mx-auto px-margin-mobile md:px-margin-desktop pt-stack-md pb-stack-lg space-y-stack-lg">',
            html,
            count=1,
        )

    # Dashboard overview: wire CTAs + add simple details modal.
    if path.parent.name == "dashboard_overview_elikhope_farms":
        html = html.replace("Welcome back, Alex.", "Welcome back, Batista.")
        html = html.replace(
            '<a class="text-primary font-bold text-body-sm hover:underline" href="#">View All History</a>',
            f'<a class="text-primary font-bold text-body-sm hover:underline" href="{U["orders"]}">View All History</a>',
        )
        html = html.replace(
            '<button class="flex-1 bg-primary text-on-primary font-bold py-3 rounded-lg text-body-sm hover:opacity-90 transition-opacity">Track Delivery</button>',
            f'<a class="flex-1 bg-primary text-on-primary font-bold py-3 rounded-lg text-body-sm hover:opacity-90 transition-opacity text-center" href="{U["track_dash"]}">Track Delivery</a>',
        )
        html = html.replace(
            '<button class="flex-1 border-1.5 border-primary text-primary font-bold py-3 rounded-lg text-body-sm hover:bg-primary/5 transition-colors border-[1.5px]">View Details</button>',
            '<button class="flex-1 border-1.5 border-primary text-primary font-bold py-3 rounded-lg text-body-sm hover:bg-primary/5 transition-colors border-[1.5px]" type="button" data-open-modal="order-details">View Details</button>',
        )

        if "data-open-modal=\"order-details\"" in html and "id=\"order-details-modal\"" not in html:
            modal = f"""
<!-- Order Details Modal -->
<div id="order-details-modal" class="fixed inset-0 z-[100] hidden" aria-hidden="true">
  <div class="absolute inset-0 bg-black/40 backdrop-blur-sm"></div>
  <div class="relative w-full h-full flex items-center justify-center p-margin-mobile">
    <div class="w-full max-w-2xl bg-surface-container-lowest rounded-2xl shadow-2xl border border-outline-variant/30 overflow-hidden">
      <div class="flex items-center justify-between px-6 py-4 border-b border-outline-variant/30">
        <div>
          <p class="text-xs text-on-surface-variant font-semibold uppercase tracking-wider">Order details</p>
          <h4 class="font-h4 text-h4 text-on-surface">Order #EF-90234</h4>
        </div>
        <button type="button" class="p-2 rounded-lg hover:bg-surface-container-high transition-colors" data-close-modal="order-details" aria-label="Close">
          <span class="material-symbols-outlined text-on-surface-variant">close</span>
        </button>
      </div>
      <div class="p-6 grid grid-cols-1 md:grid-cols-2 gap-gutter">
        <div class="space-y-3">
          <div class="flex justify-between text-body-sm text-on-surface-variant"><span>Status</span><span class="font-semibold text-on-surface">Out for delivery</span></div>
          <div class="flex justify-between text-body-sm text-on-surface-variant"><span>Items</span><span class="font-semibold text-on-surface">3</span></div>
          <div class="flex justify-between text-body-sm text-on-surface-variant"><span>Total</span><span class="font-semibold text-on-surface">GHS 124.78</span></div>
          <div class="flex justify-between text-body-sm text-on-surface-variant"><span>Delivery</span><span class="font-semibold text-on-surface">Tomorrow, 10:00</span></div>
        </div>
        <div class="bg-surface-container-low rounded-xl p-4 border border-outline-variant/20">
          <p class="text-xs text-on-surface-variant font-semibold uppercase tracking-wider mb-2">Quick actions</p>
          <div class="grid grid-cols-1 gap-3">
            <a href="{U["track_dash"]}" class="w-full bg-primary text-on-primary py-3 rounded-lg font-bold text-body-sm hover:opacity-90 transition-opacity text-center">Track delivery</a>
            <a href="{U["orders"]}" class="w-full border border-outline-variant py-3 rounded-lg font-semibold text-body-sm hover:bg-surface-container-high transition-colors text-center">Go to orders</a>
          </div>
        </div>
      </div>
      <div class="px-6 py-4 border-t border-outline-variant/30 flex justify-end gap-3">
        <button type="button" class="px-5 py-3 rounded-xl border border-outline-variant font-semibold text-body-sm hover:bg-surface-container-high transition-colors" data-close-modal="order-details">Close</button>
      </div>
    </div>
  </div>
</div>
<script>
(() => {{
  const modal = document.getElementById('order-details-modal');
  if (!modal) return;
  const openers = document.querySelectorAll('[data-open-modal="order-details"]');
  const closers = modal.querySelectorAll('[data-close-modal="order-details"]');
  const open = () => {{ modal.classList.remove('hidden'); modal.setAttribute('aria-hidden','false'); }};
  const close = () => {{ modal.classList.add('hidden'); modal.setAttribute('aria-hidden','true'); }};
  openers.forEach(b => b.addEventListener('click', open));
  closers.forEach(b => b.addEventListener('click', close));
  modal.addEventListener('click', (e) => {{ if (e.target === modal.firstElementChild) close(); }});
  document.addEventListener('keydown', (e) => {{ if (e.key === 'Escape') close(); }});
}})();
</script>
"""
            html = html.replace("</body>", modal + "\n</body>")
    return html


def patch_login(html: str) -> str:
    html = html.replace(
        '<a class="font-body-sm text-primary font-semibold hover:underline" href="#">Forgot password?</a>',
        f'<a class="font-body-sm text-primary font-semibold hover:underline" href="{U["forgot"]}">Forgot password?</a>',
    )
    html = html.replace(
        '<a class="text-primary font-bold hover:underline" href="#">Create an account</a>',
        f'<a class="text-primary font-bold hover:underline" href="{U["register"]}">Create an account</a>',
    )
    html = html.replace(
        """<button class="w-full py-4 bg-primary-container text-on-primary font-h4 rounded-lg shadow-lg hover:brightness-110 active:scale-[0.98] transition-all flex items-center justify-center gap-base" type="submit">
                        Sign In
                        <span class="material-symbols-outlined">arrow_forward</span>
</button>""",
        f"""<a href="{U["dash"]}" class="w-full py-4 bg-primary-container text-on-primary font-h4 rounded-lg shadow-lg hover:brightness-110 active:scale-[0.98] transition-all flex items-center justify-center gap-base">
                        Sign In
                        <span class="material-symbols-outlined">arrow_forward</span>
</a>""",
    )
    # Ensure social buttons use actual Google + Apple logos.
    html = re.sub(
        r'(?is)<img[^>]+alt="Google"[^>]*>\s*<span class="text-on-surface">Google</span>',
        '<i class="fa-brands fa-google text-[18px] text-on-surface"></i><span class="text-on-surface">Google</span>',
        html,
        count=1,
    )
    html = re.sub(
        r'(?is)<button([^>]*)>\s*(?:<img[^>]+alt="Apple"[^>]*>\s*)<span class="text-on-surface">Apple</span>\s*</button>',
        r'<button\1><i class="fa-brands fa-apple text-[18px] text-on-surface"></i><span class="text-on-surface">Apple</span></button>',
        html,
        count=1,
    )
    html = re.sub(
        r'(?is)<button([^>]*)>\s*<span class="material-symbols-outlined[^"]*"\s*data-weight="fill">\s*ios\s*</span>\s*<span class="text-on-surface">Apple</span>\s*</button>',
        r'<button\1><i class="fa-brands fa-apple text-[18px] text-on-surface"></i><span class="text-on-surface">Apple</span></button>',
        html,
        count=1,
    )
    return html


def patch_register(html: str) -> str:
    html = html.replace(
        """<button class="w-full py-4 bg-primary text-white font-h4 text-h4 rounded-lg shadow-lg hover:bg-primary-container active:scale-[0.98] transition-all duration-200 mt-stack-md flex items-center justify-center gap-2" type="submit">
                        Create Account
                        <span class="material-symbols-outlined">arrow_forward</span>
</button>""",
        f"""<a href="{U["otp"]}" class="w-full py-4 bg-primary text-white font-h4 text-h4 rounded-lg shadow-lg hover:bg-primary-container active:scale-[0.98] transition-all duration-200 mt-stack-md flex items-center justify-center gap-2">
                        Create Account
                        <span class="material-symbols-outlined">arrow_forward</span>
</a>""",
    )
    html = html.replace(
        '<a class="text-primary font-bold hover:underline" href="#">Log in here</a>',
        f'<a class="text-primary font-bold hover:underline" href="{U["login"]}">Log in here</a>',
    )
    # Swap social button images for Font Awesome icons.
    html = re.sub(
        r'(?is)<img[^>]+alt="Google"[^>]*>\s*Google',
        '<i class="fa-brands fa-google text-[18px] text-on-surface"></i> Google',
        html,
    )
    html = re.sub(
        r'(?is)<img[^>]+alt="Apple"[^>]*>\s*Apple',
        '<i class="fa-brands fa-apple text-[18px] text-on-surface"></i> Apple',
        html,
    )
    return html


def patch_forgot(html: str) -> str:
    html = html.replace(
        """<button class="w-full bg-primary-container text-on-primary py-4 rounded-lg font-h4 text-body-md font-bold shadow-md hover:opacity-90 active:scale-[0.98] transition-all" type="submit">
                        Send Reset Link
                    </button>""",
        f"""<a href="{U["login"]}" class="w-full bg-primary-container text-on-primary py-4 rounded-lg font-h4 text-body-md font-bold shadow-md hover:opacity-90 active:scale-[0.98] transition-all inline-flex justify-center items-center">
                        Send reset link
                    </a>""",
    )
    html = html.replace(
        '<a class="text-primary font-body-sm font-semibold flex items-center justify-center gap-1 hover:underline" href="#">',
        f'<a class="text-primary font-body-sm font-semibold flex items-center justify-center gap-1 hover:underline" href="{U["login"]}">',
        1,
    )
    return html


def patch_otp(html: str) -> str:
    html = html.replace(
        """<button class="w-full bg-primary text-on-primary py-4 rounded-lg font-h4 text-body-md font-bold shadow-md hover:opacity-90 active:scale-[0.98] transition-all" type="submit">
                        Verify Code
                    </button>""",
        f"""<a href="{U["verified"]}" class="w-full bg-primary text-on-primary py-4 rounded-lg font-h4 text-body-md font-bold shadow-md hover:opacity-90 active:scale-[0.98] transition-all inline-flex justify-center items-center">
                        Verify code
                    </a>""",
    )
    html = html.replace(
        '<a class="text-primary font-body-sm font-semibold flex items-center justify-center gap-1 hover:underline" href="#">',
        f'<a class="text-primary font-body-sm font-semibold flex items-center justify-center gap-1 hover:underline" href="{U["login"]}">',
        1,
    )
    return html


def patch_verified(html: str) -> str:
    html = html.replace(
        """<button class="w-full bg-primary-container text-on-primary font-h4 text-h4 py-4 rounded-lg shadow-sm hover:opacity-90 active:scale-[0.98] transition-all duration-200">
                    Continue to Shop
                </button>""",
        f"""<a href="{U["shop_home"]}" class="w-full bg-primary-container text-on-primary font-h4 text-h4 py-4 rounded-lg shadow-sm hover:opacity-90 active:scale-[0.98] transition-all duration-200 inline-flex justify-center items-center">
                    Continue to shop
                </a>""",
    )
    html = html.replace(
        """<button class="w-full border-1.5 border-primary-container text-primary-container font-h4 text-h4 py-4 rounded-lg border-2 hover:bg-primary-container/5 active:scale-[0.98] transition-all duration-200">
                    Go to Dashboard
                </button>""",
        f"""<a href="{U["dash"]}" class="w-full border-1.5 border-primary-container text-primary-container font-h4 text-h4 py-4 rounded-lg border-2 hover:bg-primary-container/5 active:scale-[0.98] transition-all duration-200 inline-flex justify-center items-center">
                    Go to dashboard
                </a>""",
    )
    return html


def patch_admin_login(html: str) -> str:
    html = html.replace(
        """<button class="w-full py-4 bg-primary-container text-on-primary font-h4 rounded-lg shadow-lg hover:brightness-110 active:scale-[0.98] transition-all flex items-center justify-center gap-base" type="submit">
                        Sign In
                        <span class="material-symbols-outlined">arrow_forward</span>
</button>""",
        f"""<a href="{U["adm_dash"]}" class="w-full py-4 bg-primary-container text-on-primary font-h4 rounded-lg shadow-lg hover:brightness-110 active:scale-[0.98] transition-all flex items-center justify-center gap-base">
                        Sign in to admin
                        <span class="material-symbols-outlined">arrow_forward</span>
</a>""",
    )
    html = html.replace(
        '<a class="text-primary font-bold hover:underline" href="#">Create an account</a>',
        f'<a class="text-primary font-bold hover:underline" href="{U["login"]}">Customer login</a>',
    )
    html = re.sub(
        r'(?is)</form>\s*<div class="mt-stack-lg">\s*<div class="relative flex items-center justify-center mb-stack-md">[\s\S]*?</div>\s*<div class="grid grid-cols-2 gap-gutter">[\s\S]*?</div>\s*</div>\s*(?=<div class="mt-stack-lg pt-stack-md border-t)',
        "</form>\n",
        html,
        count=1,
    )
    return html


_CLASS_ATTR_RE = re.compile(r'class="([^"]*)"')


_REPEATED_PREFIX_RE = re.compile(r"\b((?:md|lg|sm|xl|2xl|hover|focus|active|dark):)(?:\1)+")


def dedupe_classes(html: str) -> str:
    """Collapse duplicated tokens inside every class="..." attribute.

    Several patch passes use plain string-replace or regex substitutions that
    are not idempotent (e.g. `p-margin-desktop` -> `p-margin-mobile md:p-margin-desktop`),
    which causes class attributes to grow with every script run. This post-pass
    splits each class list, collapses repeated responsive/state prefixes
    (e.g. `md:md:md:ml-64` -> `md:ml-64`), removes duplicate tokens while
    preserving order, and rewrites the attribute.
    """
    def _normalize(match: "re.Match[str]") -> str:
        raw = match.group(1)
        if not raw.strip():
            return 'class=""'
        # Collapse stuttering responsive/state prefixes inside any single token.
        raw = _REPEATED_PREFIX_RE.sub(r"\1", raw)
        # Split, dedupe.
        seen = set()
        out: list[str] = []
        for tok in raw.split():
            if tok and tok not in seen:
                out.append(tok)
                seen.add(tok)
        return f'class="{" ".join(out)}"'
    return _CLASS_ATTR_RE.sub(_normalize, html)


def normalize_legacy_product_image_paths(html: str) -> str:
    """Fix 404s: chicken/special-cuts only exist under /assets/products/."""
    html = html.replace('src="/assets/fresh-chicken-meat.jpg"', f'src="{PD_CHICKEN}"')
    html = html.replace('src="/assets/special-cuts.jpg"', f'src="{PD_SPECIAL}"')
    return html


def patch_shopping_cart_line_images(html: str) -> str:
    """Cart PLP row thumbs: beef portrait → product; herbs pairing → non-meat asset."""
    html = re.sub(
        r'(<img class="w-full h-full object-cover" data-alt="A professional studio macro shot of premium grass-fed ribeye beef steak[^"]*" )\s*src="[^"]+"',
        rf'\1src="{PD_BEEF}"',
        html,
        count=1,
    )
    html = re.sub(
        r'(\bdata-alt="A macro detail shot of vibrant green fresh rosemary sprigs[^"]*" )\s*src="[^"]+"',
        rf'\1src="{ASSET_MEAT_COLD_ROOM}"',
        html,
        count=1,
    )
    return html


def patch_checkout_order_review_line_images(html: str) -> str:
    """Review order: ribeye row uses chicken per prototype; lamb → goat from products folder."""
    html = re.sub(
        r'(\balt="Prime Grass-fed Ribeye Steak" class="w-full h-full object-cover" data-alt="[^"]*" src=")([^"]+)(")',
        rf"\1{PD_CHICKEN}\3",
        html,
        count=1,
    )
    html = re.sub(
        r'(\balt="Premium lamb chops" class="w-full h-full object-cover" data-alt="[^"]*" src=")([^"]+)(")',
        rf"\1{PD_GOAT}\3",
        html,
        count=1,
    )
    return html


def patch_track_order_line_images(html: str) -> str:
    """Guest track list: chicken + lamb thumbnails from /assets/products/."""
    html = re.sub(
        r'(\balt="Chicken Item" class="w-full h-full object-cover" data-alt="[^"]*" src=")([^"]+)(")',
        rf"\1{PD_CHICKEN}\3",
        html,
        count=1,
    )
    html = re.sub(
        r'(\balt="Lamb Item" class="w-full h-full object-cover" data-alt="[^"]*" src=")([^"]+)(")',
        rf"\1{PD_GOAT}\3",
        html,
        count=1,
    )
    return html


def process_file(path: Path) -> None:
    html = path.read_text(encoding="utf-8")
    html = apply_brand(html)
    html = apply_currency_ghs(html)
    html = apply_fonts(html)
    html = apply_fontawesome(html)
    html = apply_responsive_helpers(html)
    # Responsive mobile tweaks across all pages.
    rel = path.relative_to(ROOT).as_posix()
    html = apply_responsive_type(html)
    parent = path.parent.name
    html = normalize_legacy_product_image_paths(html)

    if rel.startswith("Admin_Dashboard_Pages/"):
        html = patch_admin_page(path, html)
    elif rel.startswith("Customer_Dashboard_Pages/"):
        html = patch_customer_page(path, html)
        if parent == "manage_addresses_elikhope_farms":
            # Some exports use a public-style sticky nav + settings sidebar.
            # Replace the sticky top nav with the dashboard top header.
            html = re.sub(
                r"<nav class=\"flex justify-between items-center [^\"]*sticky top-0[\\s\\S]*?</nav>",
                customer_top_header(),
                html,
                count=1,
            )
            # Replace the sticky settings sidebar with the standard dashboard sidebar.
            html = re.sub(
                r"<aside class=\"hidden md:flex[\\s\\S]*?</aside>",
                render_customer_sidebar("addresses"),
                html,
                count=1,
            )
            # Ensure the main canvas uses the standard offsets.
            html = re.sub(
                r"<main class=\"flex-1 [^\"]*\">",
                "<main class=\"ml-64 pt-16 min-h-screen\">",
                html,
                count=1,
            )
            html = html.replace(
                'href="#">Shop</a>',
                f'href="{U["shop_home"]}">Shop</a>',
            )
            html = html.replace(
                'href="#">Traceability</a>',
                f'href="{U["quality"]}">Traceability</a>',
            )
            html = html.replace(
                'href="#">About Us</a>',
                f'href="{U["about"]}">About Us</a>',
            )
            html = html.replace(
                '<a class="flex items-center gap-3 px-4 py-3 text-on-surface-variant hover:bg-surface-variant rounded-lg transition-colors active:scale-95" href="#">\n<span class="material-symbols-outlined" data-icon="dashboard">dashboard</span>',
                f'<a class="flex items-center gap-3 px-4 py-3 text-on-surface-variant hover:bg-surface-variant rounded-lg transition-colors active:scale-95" href="{U["dash"]}">\n<span class="material-symbols-outlined" data-icon="dashboard">dashboard</span>',
                1,
            )
            html = html.replace(
                '<a class="flex items-center gap-3 px-4 py-3 text-on-surface-variant hover:bg-surface-variant rounded-lg transition-colors active:scale-95" href="#">\n<span class="material-symbols-outlined" data-icon="package_2">package_2</span>',
                f'<a class="flex items-center gap-3 px-4 py-3 text-on-surface-variant hover:bg-surface-variant rounded-lg transition-colors active:scale-95" href="{U["orders"]}">\n<span class="material-symbols-outlined" data-icon="package_2">package_2</span>',
                1,
            )
        if parent == "track_your_delivery_elikhope_farms":
            html = html.replace(
                'href="#">Explore</a>',
                f'href="{U["shop_home"]}">Explore</a>',
            )
            html = html.replace(
                'href="#">My Orders</a>',
                f'href="{U["orders"]}">My orders</a>',
            )
            html = html.replace(
                'href="#">Farm Stories</a>',
                f'href="{U["blog"]}">Farm stories</a>',
            )
            html = html.replace(
                '<span class="font-h3 text-h3 font-bold text-primary">EliKhope Farms</span>',
                f'<a href="{U["home"]}" class="font-h3 text-h3 font-bold text-primary">EliKhope Farms</a>',
                1,
            )
    elif rel.startswith("elikhope_farms_marketing_pages/"):
        # current_url for active nav state
        current_url = "/" + rel.replace(" ", "%20")
        html = patch_marketing_page(html, current_url=current_url)
    elif rel.startswith("E-Commerce_Shop_UI Pages/"):
        current_url = "/" + rel.replace(" ", "%20")
        html = patch_shop_page(html, current_url=current_url)
        if parent == "elikhope_farms_browse_products" or parent in CATEGORY_PLP_SPECS:
            html = patch_shop_browse_product_grid(html, parent)
        if parent == "elikhope_farms_product_detail":
            html = patch_product_detail_page(html)
        if parent == "elikhope_farms_product_detail":
            html = html.replace(
                """<button class="flex-1 bg-primary text-on-primary py-4 rounded-lg font-bold flex items-center justify-center gap-2 shadow-lg hover:opacity-90 active:scale-95 transition-all">
<span class="material-symbols-outlined">shopping_bag</span> Add to Cart
                    </button>""",
                f"""<a href="{U["cart"]}" class="flex-1 bg-primary text-on-primary py-4 rounded-lg font-bold flex items-center justify-center gap-2 shadow-lg hover:opacity-90 active:scale-95 transition-all">
<span class="material-symbols-outlined">shopping_bag</span> Add to cart
                    </a>""",
            )
        if parent == "elikhope_farms_shopping_cart":
            html = html.replace(
                """<button class="w-full bg-primary-container text-on-primary-container py-4 rounded-xl font-bold text-body-lg shadow-lg hover:opacity-90 transition-all flex items-center justify-center gap-2">
<span class="material-symbols-outlined" style="font-variation-settings: 'FILL' 1;">lock</span>
                        Secure Checkout
                    </button>""",
                f"""<a href="{U["checkout_delivery"]}" class="w-full bg-primary-container text-on-primary-container py-4 rounded-xl font-bold text-body-lg shadow-lg hover:opacity-90 transition-all flex items-center justify-center gap-2">
<span class="material-symbols-outlined" style="font-variation-settings: 'FILL' 1;">lock</span>
                        Secure checkout
                    </a>""",
            )
            html = patch_shopping_cart_line_images(html)
        if parent == "checkout_delivery_information_elikhope_farms":
            # Rebuild the delivery page with a clean, wide structure.
            html = re.sub(
                r"(?is)<main[^>]*>[\s\S]*?</main>",
                render_checkout_delivery_main(),
                html,
                count=1,
            )
            # Localize placeholders for Ghana (fallback for any remaining content).
            html = html.replace("Johannesburg", "Accra")
            html = html.replace("+27", "+233")
            html = html.replace("Gauteng", "Greater Accra")
            html = re.sub(
                r'<button([^>]*bg-primary-container[^>]*)>[\s\S]*?Continue to Payment[\s\S]*?</button>',
                r'<a href="' + U["checkout_pay"] + r'"\1>Continue to payment</a>',
                html,
                count=1,
            )
        if parent == "checkout_payment_elikhope_farms":
            # Rebuild the payment page with a clean structure.
            html = re.sub(
                r"(?is)<main[^>]*>[\s\S]*?</main>",
                render_checkout_payment_main(),
                html,
                count=1,
            )
            # Remove the Google/logo image blocks from the payment UI and reference Paystack.
            html = re.sub(
                r'(?is)<img[^>]+alt="Payment Network"[^>]*>',
                '<span class="inline-flex items-center rounded-full bg-surface-container px-3 py-1 text-[11px] font-semibold text-on-surface-variant border border-outline-variant/40">Paystack</span>',
                html,
                count=1,
            )
            html = html.replace(
                '<span class="font-label-caps text-on-surface-variant">Paystack</span>',
                '<span class="inline-flex items-center rounded-full bg-surface-container px-3 py-1 text-[11px] font-semibold text-on-surface-variant border border-outline-variant/40">Paystack</span>',
            )
            html = re.sub(
                r'(?is)<img[^>]+alt="EliKhope Farms Logo"[^>]*>',
                '',
                html,
            )
            html = html.replace("Select Payment Method", "Select payment method (Paystack)")
            # The original container for the network logo is too small and clips text.
            html = html.replace(
                '<div class="h-6 w-10 bg-surface-container rounded flex items-center justify-center overflow-hidden">',
                '<div class="flex items-center justify-end">',
                1,
            )
            html = html.replace(
                """<button class="w-full py-4 px-6 bg-primary text-on-primary rounded-lg font-h4 shadow-md hover:bg-primary-container transition-all active:scale-95 mt-auto">
                    Complete Purchase
                </button>""",
                f"""<a href="{U["checkout_review"]}" class="w-full py-4 px-6 bg-primary text-on-primary rounded-lg font-h4 shadow-md hover:bg-primary-container transition-all active:scale-95 mt-auto inline-flex justify-center items-center">
                    Continue to review
                </a>""",
            )
        if parent == "checkout_order_review_elikhope_farms":
            html = patch_checkout_order_review_line_images(html)
            html = html.replace(
                """<button class="w-full bg-primary-container text-on-primary py-4 rounded-lg font-h4 text-h4 shadow-md hover:opacity-90 active:scale-95 transition-all flex items-center justify-center gap-2">
                            Place Order
                            <span class="material-symbols-outlined">arrow_forward</span>
</button>""",
                f"""<a href="{U["order_success"]}" class="w-full bg-primary-container text-on-primary py-4 rounded-lg font-h4 text-h4 shadow-md hover:opacity-90 active:scale-95 transition-all flex items-center justify-center gap-2">
                            Place order
                            <span class="material-symbols-outlined">arrow_forward</span>
</a>""",
            )
        if parent == "elikhope_farms_order_success":
            html = html.replace(
                """<button class="bg-primary text-on-primary font-body-md px-10 py-4 rounded-lg shadow-md hover:opacity-90 transition-all active:scale-95 flex items-center justify-center gap-2">
<span class="material-symbols-outlined" data-icon="local_shipping">local_shipping</span>
                        Track My Order
                    </button>""",
                f"""<a href="{U["track_guest"]}" class="bg-primary text-on-primary font-body-md px-10 py-4 rounded-lg shadow-md hover:opacity-90 transition-all active:scale-95 flex items-center justify-center gap-2">
<span class="material-symbols-outlined" data-icon="local_shipping">local_shipping</span>
                        Track my order
                    </a>""",
            )
            html = html.replace(
                """<button class="border-[1.5px] border-primary text-primary font-body-md px-10 py-4 rounded-lg hover:bg-primary-fixed/20 transition-all active:scale-95 flex items-center justify-center gap-2">
<span class="material-symbols-outlined" data-icon="shopping_basket">shopping_basket</span>
                        Continue Shopping
                    </button>""",
                f"""<a href="{U["shop_home"]}" class="border-[1.5px] border-primary text-primary font-body-md px-10 py-4 rounded-lg hover:bg-primary-fixed/20 transition-all active:scale-95 flex items-center justify-center gap-2">
<span class="material-symbols-outlined" data-icon="shopping_basket">shopping_basket</span>
                        Continue shopping
                    </a>""",
            )
        if parent == "elikhope_farms_track_order":
            html = patch_track_order_line_images(html)
    elif rel.startswith("Authentication_Pages/"):
        html = patch_auth_top(html)
        html = strip_auth_visual_side(html)
        if parent in {"login_elikhope_farms", "admin_login_elikhope_farms"}:
            html = apply_auth_login_desktop_split(html, parent)
        html = replace_or_append_footer(html, AUTH_FOOTER)
        if parent == "login_elikhope_farms":
            html = patch_login(html)
        elif parent == "create_account_elikhope_farms":
            html = patch_register(html)
            html = apply_register_desktop_split(html, parent)
        elif parent == "forgot_password_elikhope_farms":
            html = patch_forgot(html)
        elif parent == "email_verification_elikhope_farms":
            html = patch_otp(html)
        elif parent == "success_elikhope_farms":
            html = patch_verified(html)
        elif parent == "admin_login_elikhope_farms":
            html = patch_admin_login(html)

    if rel.startswith(
        (
            "elikhope_farms_marketing_pages/",
            "E-Commerce_Shop_UI Pages/",
            "Customer_Dashboard_Pages/",
            "Authentication_Pages/",
        )
    ):
        html = patch_remote_cdn_images_to_local(html)

    html = dedupe_classes(html)
    path.write_text(html, encoding="utf-8")


def ensure_admin_login() -> None:
    dest = ROOT / "Authentication_Pages" / "admin_login_elikhope_farms" / "code.html"
    src = ROOT / "Authentication_Pages" / "login_elikhope_farms" / "code.html"
    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.exists():
        return
    text = src.read_text(encoding="utf-8")
    text = re.sub(
        r"<title>[^<]*</title>",
        "<title>Staff admin login | EliKhope Farms</title>",
        text,
        count=1,
    )
    text = text.replace(
        '<h1 class="font-h2 text-h2 text-on-surface mb-base">Welcome Back</h1>',
        '<h1 class="font-h2 text-h2 text-on-surface mb-base">Admin sign in</h1>',
    )
    text = text.replace(
        "Access your premium meat selection dashboard.",
        "Operations portal for EliKhope Farms staff.",
    )
    dest.write_text(text, encoding="utf-8")


def ensure_category_pages() -> None:
    """Clone shop PLP template for per-category listing pages; seed categories hub from home."""
    shop = ROOT / "E-Commerce_Shop_UI Pages"
    template = shop / "elikhope_farms_browse_products" / "code.html"
    if not template.exists():
        return
    for folder in CATEGORY_PLP_SPECS:
        dest = shop / folder / "code.html"
        if not dest.exists():
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_text(template.read_text(encoding="utf-8"), encoding="utf-8")
    hub = ROOT / "elikhope_farms_marketing_pages" / "elikhope_farms_all_categories" / "code.html"
    if not hub.exists():
        hub.parent.mkdir(parents=True, exist_ok=True)
        home = ROOT / "elikhope_farms_marketing_pages" / "elikhope_farms_home_page" / "code.html"
        if home.exists():
            hub.write_text(home.read_text(encoding="utf-8"), encoding="utf-8")


def main() -> None:
    ensure_admin_login()
    ensure_category_pages()
    for html_path in sorted(ROOT.rglob("code.html")):
        if "prime" in html_path.parts:
            continue
        process_file(html_path)
    print("OK: patched code.html files (excluding prime).")


if __name__ == "__main__":
    main()
