"""
Patch EliKhope static HTML: branding, shared logo, sidebars, headers, footers, links.
Run: python scripts/elikhope_patch.py   (from repo root)
"""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

MARK = "/elikhope_farms_marketing_pages"
AUTH = "/Authentication_Pages"
CUST = "/Customer_Dashboard_Pages"
ADMIN = "/Admin_Dashboard_Pages"
SHOP = "/E-Commerce_Shop_UI%20Pages"
ASSET_LOGO = "/assets/elikhope-logo.svg"

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


def apply_responsive_helpers(html: str) -> str:
    if "data-ek-toggle" not in html:
        return html
    if "ek-toggle-init" in html:
        return html
    js = """<script id="ek-toggle-init">
(() => {
  const openDrawer = (root) => {
    root.classList.remove('hidden');
    const panel = root.querySelector('[data-ek-drawer-panel]');
    if (panel) requestAnimationFrame(() => panel.classList.remove('translate-x-full'));
  };
  const closeDrawer = (root) => {
    const panel = root.querySelector('[data-ek-drawer-panel]');
    if (panel) panel.classList.add('translate-x-full');
    window.setTimeout(() => root.classList.add('hidden'), 220);
  };
  document.addEventListener('click', (e) => {
    const btn = e.target.closest('[data-ek-toggle]');
    if (!btn) return;
    const id = btn.getAttribute('data-ek-toggle');
    const root = document.getElementById(id);
    if (!root) return;

    const isDrawer = root.hasAttribute('data-ek-drawer');
    if (!isDrawer) {
      root.classList.toggle('hidden');
      return;
    }

    const isOpen = !root.classList.contains('hidden');
    if (isOpen) closeDrawer(root);
    else openDrawer(root);
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
<button class="md:hidden fixed top-4 left-4 z-[60] p-3 rounded-xl bg-surface shadow-md border border-outline-variant/40" type="button" aria-label="Open admin menu" data-ek-toggle="ek-admin-drawer">
  <i class="fa-solid fa-bars text-on-surface-variant"></i>
</button>
<div id="ek-admin-drawer" class="md:hidden hidden fixed inset-0 z-[70]" data-ek-drawer="left">
  <div class="absolute inset-0 bg-black/40" data-ek-toggle="ek-admin-drawer" aria-label="Close menu"></div>
  <aside data-ek-drawer-panel class="absolute left-0 top-0 h-full w-80 max-w-[85vw] bg-inverse-surface dark:bg-surface-container-lowest shadow-xl border-r border-on-surface-variant/10 flex flex-col translate-x-full transition-transform duration-200 ease-out">
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
  <aside data-ek-drawer-panel class="absolute left-0 top-0 h-full w-80 max-w-[85vw] bg-surface shadow-xl border-r border-outline-variant flex flex-col translate-x-full transition-transform duration-200 ease-out">
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
<header class="fixed top-0 right-0 md:w-[calc(100%-16rem)] w-full h-16 bg-surface/80 dark:bg-surface-container/80 backdrop-blur-md shadow-sm flex justify-between items-center px-margin-desktop z-40">
<div class="flex items-center gap-3 flex-1 min-w-0">
<button class="md:hidden inline-flex items-center justify-center p-2 rounded-lg hover:bg-surface-container transition-colors" type="button" aria-label="Open menu" data-ek-toggle="ek-cust-drawer">
  <i class="fa-solid fa-bars text-on-surface-variant"></i>
</button>
<div class="relative max-w-md w-full group min-w-0">
<a href="{U["search"]}" class="absolute left-3 top-1/2 -translate-y-1/2 text-on-surface-variant"><span class="material-symbols-outlined">search</span></a>
<input class="w-full bg-surface-container-low border-none rounded-lg py-2 pl-10 pr-4 text-body-sm focus:ring-2 focus:ring-primary/20 focus:bg-surface transition-all" placeholder="Search products..." type="text"/>
</div>
</div>
<div class="flex items-center gap-6">
<a class="text-on-surface-variant hover:text-primary transition-colors flex items-center gap-1 font-body-sm" href="{U["help"]}"><span class="material-symbols-outlined" data-icon="help">help</span>Support</a>
<div class="flex items-center gap-4">
<a class="relative inline-flex text-on-surface-variant hover:text-primary p-2" href="{U["notif"]}"><span class="material-symbols-outlined" data-icon="notifications">notifications</span><span class="absolute top-1 right-1 w-2 h-2 bg-error rounded-full"></span></a>
<a class="inline-flex p-2 text-on-surface-variant hover:text-primary" href="{U["cart"]}"><span class="material-symbols-outlined" data-icon="shopping_cart">shopping_cart</span></a>
</div>
<div class="h-8 w-[1px] bg-outline-variant"></div>
<a href="{U["settings_c"]}" class="flex items-center gap-3">
<img alt="" class="w-8 h-8 rounded-full object-cover border border-outline-variant" src="https://lh3.googleusercontent.com/aida-public/AB6AXuBjNjqeidHh9QfPQmvz4Hz2qHZxzNsgstnVknWK4dixp5768ZYZ9YaJnj1N_hQPLAJtBR6VQcKBPcEhd0ozBYwugZATVCI0BglE22H0z3GK4dw1l8_-5gK5eVRcMPuMORgUhmYmVI2o_lboqGA70_WCVIkiZIw4V0IiN5npzwgYxKPyFbNsSSRZO1kiwXieeuaM31x1CfXyFzi46mzKbxFQiR6FxhbCHnUQsbA3Ft0Ux4wZNWn7Eo_vX86MAUffJ_T_Ya96rU3tWLs"/>
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
<div class="max-w-container-max mx-auto flex justify-between items-center px-margin-desktop h-20">
<a href="{U["home"]}" class="flex items-center gap-3 shrink-0">
<img src="{ASSET_LOGO}" alt="" class="h-10 w-10 rounded-lg" width="40" height="40"/>
<span class="text-h4 font-h4 font-bold text-primary dark:text-primary-fixed">EliKhope Farms</span>
</a>
<div class="hidden lg:flex items-center gap-6 flex-wrap justify-center">
{MARKETING_NAV_INNER}
</div>
<div class="flex items-center gap-stack-sm">
<a class="hidden sm:inline font-body-sm font-semibold text-primary hover:underline" href="{U["login"]}">Login</a>
<a class="hidden sm:inline-flex px-4 py-2 rounded-lg bg-primary text-white font-bold text-sm hover:opacity-90" href="{U["register"]}">Sign up</a>
<a class="p-2 rounded-full hover:bg-surface-container transition-colors" href="{U["cart"]}" title="Cart"><span class="material-symbols-outlined text-on-surface-variant">shopping_cart</span></a>
<a class="p-2 rounded-full hover:bg-surface-container transition-colors" href="{U["dash"]}" title="Account"><span class="material-symbols-outlined text-on-surface-variant">account_circle</span></a>
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
<div class="py-stack-lg px-margin-desktop grid grid-cols-1 md:grid-cols-4 gap-gutter max-w-container-max mx-auto">
<div class="flex flex-col gap-4">
<a href="{U["home"]}" class="flex items-center gap-3">
<img src="{ASSET_LOGO}" alt="" class="h-9 w-9 rounded-lg" width="36" height="36"/>
<span class="text-h3 font-h3 font-bold text-primary dark:text-primary-fixed">EliKhope Farms</span>
</a>
<p class="font-body-sm text-body-sm text-on-surface-variant dark:text-surface-variant">© 2026 EliKhope Farms. Premium farm-to-consumer meat.</p>
<p class="text-xs text-on-surface-variant"><a href="{U["admin_login"]}" class="underline hover:text-primary">Staff login</a></p>
</div>
<div class="flex flex-col gap-2">
<h5 class="font-bold mb-2">Shop</h5>
<a class="font-body-sm text-on-surface-variant hover:text-primary underline" href="{U["shop_home"]}">Shop home</a>
<a class="font-body-sm text-on-surface-variant hover:text-primary underline" href="{U["shop_home"]}">Shop</a>
<a class="font-body-sm text-on-surface-variant hover:text-primary underline" href="{U["plp"]}">Browse cuts</a>
</div>
<div class="flex flex-col gap-2">
<h5 class="font-bold mb-2">Trust</h5>
<a class="font-body-sm text-on-surface-variant hover:text-primary underline" href="{U["quality"]}">Quality standards</a>
<a class="font-body-sm text-on-surface-variant hover:text-primary underline" href="{U["help"]}">Help center</a>
<a class="font-body-sm text-on-surface-variant hover:text-primary underline" href="{U["contact"]}">Contact us</a>
</div>
<div class="flex flex-col gap-2">
<h5 class="font-bold mb-2">Account</h5>
<a class="font-body-sm text-on-surface-variant hover:text-primary underline" href="{U["login"]}">Login</a>
<a class="font-body-sm text-on-surface-variant hover:text-primary underline" href="{U["register"]}">Create account</a>
<a class="font-body-sm text-on-surface-variant hover:text-primary underline" href="{U["dash"]}">Customer dashboard</a>
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


AUTH_FOOTER = f"""<footer class="w-full py-8 px-margin-desktop border-t border-outline-variant bg-surface-container-low">
<div class="max-w-container-max mx-auto flex flex-col sm:flex-row gap-4 justify-between items-center text-sm text-on-surface-variant">
<a href="{U["home"]}" class="flex items-center gap-2 font-semibold text-primary"><img src="{ASSET_LOGO}" alt="" class="h-8 w-8 rounded-lg" width="32" height="32"/>EliKhope Farms</a>
<div class="flex gap-4 flex-wrap justify-center">
<a href="{U["help"]}" class="hover:text-primary underline">Help</a>
<a href="{U["contact"]}" class="hover:text-primary underline">Contact</a>
<a href="{U["admin_login"]}" class="hover:text-primary underline">Staff login</a>
</div>
</div>
</footer>"""


def replace_or_append_footer(html: str, footer_html: str) -> str:
    if re.search(r"(?is)<footer[^>]*>", html):
        return re.sub(r"(?is)<footer[^>]*>.*?</footer>", footer_html, html, count=1)
    return html.replace("</body>", footer_html + "\n</body>")


def patch_marketing_page(html: str, current_url: str | None = None) -> str:
    # Replace inconsistent exported top bars with our canonical marketing nav.
    html = re.sub(
        r"(?is)<!--\s*Top(NavBar|AppBar)\s*-->\s*<(header|nav)[^>]*fixed top-0[^>]*>[\s\S]*?</\2>",
        marketing_top_nav() + mobile_site_drawer(),
        html,
        count=1,
    )
    # Fallback if the comment differs or is missing.
    html = re.sub(
        r"(?is)<(header|nav)[^>]*class=\"[^\"]*fixed top-0[^\"]*w-full[^\"]*z-50[^\"]*\"[^>]*>[\s\S]*?</\1>",
        marketing_top_nav() + mobile_site_drawer(),
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
        f'<a href="{U["categories"]}" class="inline-block text-center px-8 py-4 border-2 border-white text-white font-bold rounded-lg hover:bg-white hover:text-primary transition-colors">View all cuts</a>',
        1,
    )
    return html


def patch_shop_page(html: str, current_url: str | None = None) -> str:
    # Shop pages should use the same marketing header/nav as Home/About/etc.
    # (Requested to keep nav consistent across the public site.)
    html = re.sub(
        r"(?is)<!--\s*Top(NavBar|AppBar)\s*-->\s*<(header|nav)[^>]*fixed top-0[^>]*>[\s\S]*?</\2>",
        marketing_top_nav() + mobile_site_drawer(),
        html,
        count=1,
    )
    html = re.sub(
        r"(?is)<(header|nav)[^>]*class=\"[^\"]*fixed top-0[^\"]*w-full[^\"]*z-50[^\"]*\"[^>]*>[\s\S]*?</\1>",
        marketing_top_nav() + mobile_site_drawer(),
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
  <aside data-ek-drawer-panel class="absolute left-0 top-0 h-full w-80 max-w-[85vw] bg-surface shadow-xl border-r border-outline-variant translate-x-full transition-transform duration-200 ease-out flex flex-col">
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
        r'(?is)<button class="md:hidden fixed top-4 left-4[^"]*"[^>]*data-ek-toggle="ek-admin-drawer"[^>]*>[\s\S]*?</button>',
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
        r'(?is)<button class="md:hidden fixed top-4 left-4[^"]*"[^>]*data-ek-toggle="ek-cust-drawer"[^>]*>[\s\S]*?</button>',
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
    html = re.sub(
        r'(<main class="[^"]*)\bml-64\b([^"]*")',
        r"\1md:ml-64 ml-0\2",
        html,
    )
    # Many customer pages use a desktop-only padding token; make it responsive.
    html = html.replace("p-margin-desktop", "p-margin-mobile md:p-margin-desktop")

    # Fix customer dashboard footers that were still using desktop offset on mobile.
    html = re.sub(
        r'(?is)<footer class="ml-64([^"]*)w-\[calc\(100%-16rem\)\]([^"]*)">',
        r'<footer class="md:ml-64 ml-0\1w-full\2 px-margin-mobile md:px-margin-desktop">',
        html,
        count=1,
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
        r'(?is)<img[^>]+alt="Google"[^>]*>\s*<span class="text-on-surface">Google</span>',
        '<i class="fa-brands fa-google text-[18px] text-on-surface"></i><span class="text-on-surface">Google</span>',
        html,
    )
    html = re.sub(
        r'(?is)<img[^>]+alt="Apple"[^>]*>\s*<span class="text-on-surface">Apple</span>',
        '<i class="fa-brands fa-apple text-[18px] text-on-surface"></i><span class="text-on-surface">Apple</span>',
        html,
    )
    return html


def process_file(path: Path) -> None:
    html = path.read_text(encoding="utf-8")
    html = apply_brand(html)
    html = apply_currency_ghs(html)
    html = apply_fonts(html)
    html = apply_fontawesome(html)
    html = apply_responsive_helpers(html)
    rel = path.relative_to(ROOT).as_posix()
    parent = path.parent.name

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
    elif rel.startswith("Authentication_Pages/"):
        html = patch_auth_top(html)
        html = replace_or_append_footer(html, AUTH_FOOTER)
        if parent == "login_elikhope_farms":
            html = patch_login(html)
        elif parent == "create_account_elikhope_farms":
            html = patch_register(html)
        elif parent == "forgot_password_elikhope_farms":
            html = patch_forgot(html)
        elif parent == "email_verification_elikhope_farms":
            html = patch_otp(html)
        elif parent == "success_elikhope_farms":
            html = patch_verified(html)
        elif parent == "admin_login_elikhope_farms":
            html = patch_admin_login(html)

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


def main() -> None:
    ensure_admin_login()
    for html_path in sorted(ROOT.rglob("code.html")):
        if "prime" in html_path.parts:
            continue
        process_file(html_path)
    print("OK: patched code.html files (excluding prime).")


if __name__ == "__main__":
    main()
