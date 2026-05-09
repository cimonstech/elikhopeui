import re, os

# ============================================================
# DRAWER JS SNIPPET
# ============================================================
DRAWER_JS = '''<script id="ek-toggle-init">
(() => {
  const openDrawer = (root) => {
    root.classList.remove('hidden');
    const panel = root.querySelector('[data-ek-drawer-panel]');
    if (panel) requestAnimationFrame(() => {
      panel.classList.remove('translate-x-full');
      panel.classList.remove('-translate-x-full');
    });
  };
  const closeDrawer = (root) => {
    const panel = root.querySelector('[data-ek-drawer-panel]');
    if (panel) {
      const dir = root.getAttribute('data-ek-drawer');
      if (dir === 'left') panel.classList.add('-translate-x-full');
      else panel.classList.add('translate-x-full');
    }
    window.setTimeout(() => root.classList.add('hidden'), 220);
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
    if (isOpen) closeDrawer(root);
    else openDrawer(root);
  });
})();
</script>'''

# ============================================================
# RESPONSIVE CSS BLOCKS
# ============================================================

AUTH_RESPONSIVE = '''<style id="elikhope-responsive">
@media (max-width: 640px) {
  h1, .text-h1, .font-h1 { font-size: 28px !important; line-height: 1.15 !important; letter-spacing: -0.02em !important; }
  h2, .text-h2, .font-h2 { font-size: 24px !important; line-height: 1.2 !important; }
  button { font-size: 14px !important; }
  a[class*="bg-"], a[class*="border"] { font-size: 14px !important; }
  .auth-split-layout { grid-template-columns: 1fr !important; }
  .auth-visual-side { display: none !important; }
  footer { padding-left: 1rem !important; padding-right: 1rem !important; }
}
</style>'''

MARKETING_RESPONSIVE = '''<style id="elikhope-responsive">
@media (max-width: 640px) {
  h1, .text-h1, .font-h1 { font-size: 30px !important; line-height: 1.15 !important; letter-spacing: -0.02em !important; }
  h2, .text-h2, .font-h2 { font-size: 24px !important; line-height: 1.2 !important; }
  h3, .text-h3, .font-h3 { font-size: 20px !important; }
  button { font-size: 14px !important; }
  a[class*="bg-"], a[class*="border"] { font-size: 14px !important; }
  nav .max-w-container-max { padding-left: 1rem !important; padding-right: 1rem !important; }
  section { padding-left: 1rem !important; padding-right: 1rem !important; }
  footer { padding-left: 1rem !important; padding-right: 1rem !important; }
}
@media (max-width: 767px) {
  section[style*="height"], section[class*="h-["] { height: auto !important; min-height: 280px !important; padding-top: 3rem !important; padding-bottom: 3rem !important; }
  .grid { grid-template-columns: repeat(2, 1fr) !important; gap: 1rem !important; }
  footer .grid { grid-template-columns: repeat(2, 1fr) !important; }
}
@media (max-width: 480px) {
  footer .grid { grid-template-columns: 1fr !important; }
  .grid[class*="cols-4"] { grid-template-columns: 1fr 1fr !important; }
}
</style>'''

ECOMMERCE_RESPONSIVE = '''<style id="elikhope-responsive">
@media (max-width: 640px) {
  h1, .text-h1, .font-h1 { font-size: 26px !important; line-height: 1.15 !important; letter-spacing: -0.02em !important; }
  h2, .text-h2, .font-h2 { font-size: 22px !important; line-height: 1.2 !important; }
  h3, .text-h3, .font-h3 { font-size: 18px !important; }
  button { font-size: 14px !important; }
  a[class*="bg-"], a[class*="border"] { font-size: 14px !important; }
  nav .max-w-container-max { padding-left: 1rem !important; padding-right: 1rem !important; }
  section { padding-left: 1rem !important; padding-right: 1rem !important; }
  footer { padding-left: 1rem !important; padding-right: 1rem !important; }
  table { display: block !important; overflow-x: auto !important; width: 100% !important; -webkit-overflow-scrolling: touch; }
}
@media (max-width: 767px) {
  section[class*="h-["] { height: auto !important; min-height: 220px !important; padding-top: 3rem !important; padding-bottom: 3rem !important; }
  aside[class*="w-80"], aside[class*="w-96"] { width: 100% !important; min-width: 0 !important; }
  footer .grid { grid-template-columns: repeat(2, 1fr) !important; gap: 1.5rem !important; }
}
@media (max-width: 480px) {
  footer .grid { grid-template-columns: 1fr !important; }
}
</style>'''

CUSTOMER_RESPONSIVE = '''<style id="elikhope-responsive">
@media (max-width: 640px) {
  h1, .text-h1, .font-h1 { font-size: 24px !important; line-height: 1.15 !important; }
  h2, .text-h2, .font-h2 { font-size: 20px !important; line-height: 1.2 !important; }
  h3, .text-h3, .font-h3 { font-size: 18px !important; }
  button { font-size: 14px !important; }
  a[class*="bg-"], a[class*="border"] { font-size: 14px !important; }
  table { display: block !important; overflow-x: auto !important; width: 100% !important; -webkit-overflow-scrolling: touch; }
  section[class*="h-["] { height: 200px !important; }
}
@media (max-width: 767px) {
  main { margin-left: 0 !important; }
  header[class*="md:w-[calc"] { width: 100% !important; right: 0 !important; left: 0 !important; }
}
@media (max-width: 480px) {
  .grid[class*="md:grid-cols-2"], .grid[class*="sm:grid-cols-2"] { grid-template-columns: 1fr !important; }
  input, select, textarea { width: 100% !important; min-width: 0 !important; }
}
</style>'''

SITE_DRAWER_HTML = '''<div id="ek-site-drawer" class="lg:hidden hidden fixed inset-0 z-[70]" data-ek-drawer="right">
  <div class="absolute inset-0 bg-black/40" data-ek-toggle="ek-site-drawer" aria-label="Close menu"></div>
  <aside data-ek-drawer-panel class="absolute right-0 top-0 h-full w-80 max-w-[85vw] bg-surface shadow-xl border-l border-outline-variant translate-x-full transition-transform duration-200 ease-out flex flex-col">
    <div class="p-6 flex items-start justify-between gap-4 border-b border-outline-variant/40">
      <div class="flex-1">
        <a href="/elikhope_farms_marketing_pages/elikhope_farms_home_page/code.html" class="flex items-center gap-3">
          <img src="/assets/elilogo.png" alt="" class="h-10 w-10 rounded-lg" width="40" height="40"/>
          <span class="text-h4 font-h4 font-bold text-primary">EliKhope Farms</span>
        </a>
        <p class="text-xs text-on-surface-variant mt-2">Menu</p>
      </div>
      <button class="p-2 rounded-lg hover:bg-surface-container" type="button" aria-label="Close menu" data-ek-toggle="ek-site-drawer">
        <i class="fa-solid fa-xmark text-on-surface-variant"></i>
      </button>
    </div>
    <nav class="flex-1 p-6 pt-4 flex flex-col gap-2 overflow-auto">
      <a class="py-2 font-body-md text-on-surface hover:text-primary" href="/elikhope_farms_marketing_pages/elikhope_farms_home_page/code.html">Home</a>
      <a class="py-2 font-body-md text-on-surface hover:text-primary" href="/E-Commerce_Shop_UI%20Pages/elikhope_farms_browse_products/code.html">Shop</a>
      <a class="py-2 font-body-md text-on-surface hover:text-primary" href="/elikhope_farms_marketing_pages/elikhope_farms_about_us/code.html">About</a>
      <a class="py-2 font-body-md text-on-surface hover:text-primary" href="/elikhope_farms_marketing_pages/elikhope_farms_quality_standards/code.html">Quality Control</a>
      <a class="py-2 font-body-md text-on-surface hover:text-primary" href="/elikhope_farms_marketing_pages/elikhope_farms_visual_gallery/code.html">Gallery</a>
      <a class="py-2 font-body-md text-on-surface hover:text-primary" href="/elikhope_farms_marketing_pages/elikhope_farms_meat_preparation_farm_news/code.html">Blog</a>
      <a class="py-2 font-body-md text-on-surface hover:text-primary" href="/elikhope_farms_marketing_pages/elikhope_farms_contact_us/code.html">Contact</a>
    </nav>
    <div class="p-6 border-t border-outline-variant/40 space-y-3">
      <a class="w-full inline-flex items-center justify-center px-4 py-3 rounded-xl border border-outline-variant text-on-surface font-semibold" href="/Authentication_Pages/login_elikhope_farms/code.html">Login</a>
      <a class="w-full inline-flex items-center justify-center px-4 py-3 rounded-xl bg-primary text-on-primary font-bold" href="/Authentication_Pages/create_account_elikhope_farms/code.html">Create account</a>
    </div>
  </aside>
</div>'''


def replace_responsive_style(content, new_style_block):
    pattern = r'<style id="elikhope-responsive">.*?</style>'
    if re.search(pattern, content, re.DOTALL):
        return re.sub(pattern, new_style_block, content, flags=re.DOTALL)
    return content.replace('</head>', new_style_block + '\n</head>', 1)


def dedup_site_drawers(content):
    """Remove duplicate ek-site-drawer divs, keep only first."""
    marker = 'id="ek-site-drawer"'
    if content.count(marker) <= 1:
        return content

    # Split into parts by drawer boundary
    parts = re.split(r'(?=<div id="ek-site-drawer")', content)
    if len(parts) <= 1:
        return content

    before = parts[0]
    result_parts = [before]

    first = True
    for chunk in parts[1:]:
        if first:
            # Keep this entire drawer chunk as-is
            result_parts.append(chunk)
            first = False
        else:
            # Strip the drawer div, keep anything after it
            end_match = re.search(r'</aside>\s*\n</div>\s*\n?', chunk)
            if end_match:
                result_parts.append(chunk[end_match.end():])
            else:
                # fallback: just skip
                pass

    return ''.join(result_parts)


def fix_customer_main_class(content):
    # Fix repeated md: prefix on ml-64
    content = re.sub(
        r'class="(?:md:){2,}ml-64(?:\s+ml-0)+',
        'class="md:ml-64',
        content
    )
    # Fix repeated md:p-margin-mobile ... md:p-margin-desktop
    content = re.sub(
        r'p-margin-mobile(?:\s+md:p-margin-mobile)+\s+md:p-margin-desktop',
        'p-margin-mobile md:p-margin-desktop',
        content
    )
    return content


def ensure_drawer_js(content):
    if 'ek-toggle-init' in content:
        return content
    return content.replace('</body>', DRAWER_JS + '\n</body>', 1)


def add_mobile_nav_to_checkout_order_review(content):
    if 'ek-site-drawer' in content:
        return content
    # Add font awesome if missing
    if 'font-awesome' not in content:
        content = content.replace('</head>', '<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.2/css/all.min.css"/>\n</head>', 1)
    # Add hamburger to header - find closing of header actions div
    # The header has: <div class="ml-auto hidden md:flex ...">...</div>  </div></header>
    # We add a button after the hidden desktop nav
    content = re.sub(
        r'(</div>\s*</div>\s*</header>)',
        '''  <button class="md:hidden p-2 rounded-full hover:bg-surface-container ml-auto" type="button" aria-label="Open menu" data-ek-toggle="ek-site-drawer"><i class="fa-solid fa-bars text-on-surface-variant"></i></button>
\\1''',
        content,
        count=1
    )
    # Add drawer before <main
    content = content.replace('<main ', SITE_DRAWER_HTML + '\n<main ', 1)
    return content


# ============================================================
# PROCESS FILES
# ============================================================

files_auth = [
    'Authentication_Pages/admin_login_elikhope_farms/code.html',
    'Authentication_Pages/create_account_elikhope_farms/code.html',
    'Authentication_Pages/email_verification_elikhope_farms/code.html',
    'Authentication_Pages/forgot_password_elikhope_farms/code.html',
    'Authentication_Pages/login_elikhope_farms/code.html',
    'Authentication_Pages/success_elikhope_farms/code.html',
]

files_customer = [
    'Customer_Dashboard_Pages/account_settings_elikhope_farms/code.html',
    'Customer_Dashboard_Pages/dashboard_overview_elikhope_farms/code.html',
    'Customer_Dashboard_Pages/manage_addresses_elikhope_farms/code.html',
    'Customer_Dashboard_Pages/my_orders_elikhope_farms/code.html',
    'Customer_Dashboard_Pages/my_wishlist_elikhope_farms/code.html',
    'Customer_Dashboard_Pages/notifications_elikhope_farms/code.html',
    'Customer_Dashboard_Pages/recent_purchases_elikhope_farms/code.html',
    'Customer_Dashboard_Pages/track_your_delivery_elikhope_farms/code.html',
]

files_ecommerce = [
    'E-Commerce_Shop_UI Pages/checkout_delivery_information_elikhope_farms/code.html',
    'E-Commerce_Shop_UI Pages/checkout_order_review_elikhope_farms/code.html',
    'E-Commerce_Shop_UI Pages/checkout_payment_elikhope_farms/code.html',
    'E-Commerce_Shop_UI Pages/elikhope_farms_browse_products/code.html',
    'E-Commerce_Shop_UI Pages/elikhope_farms_checkout/code.html',
    'E-Commerce_Shop_UI Pages/elikhope_farms_order_success/code.html',
    'E-Commerce_Shop_UI Pages/elikhope_farms_product_detail/code.html',
    'E-Commerce_Shop_UI Pages/elikhope_farms_search_results/code.html',
    'E-Commerce_Shop_UI Pages/elikhope_farms_shopping_cart/code.html',
    'E-Commerce_Shop_UI Pages/elikhope_farms_track_order/code.html',
]

files_marketing = [
    'elikhope_farms_marketing_pages/elikhope_farms_about_us/code.html',
    'elikhope_farms_marketing_pages/elikhope_farms_contact_us/code.html',
    'elikhope_farms_marketing_pages/elikhope_farms_help_center/code.html',
    'elikhope_farms_marketing_pages/elikhope_farms_home_page/code.html',
    'elikhope_farms_marketing_pages/elikhope_farms_meat_preparation_farm_news/code.html',
    'elikhope_farms_marketing_pages/elikhope_farms_quality_standards/code.html',
    'elikhope_farms_marketing_pages/elikhope_farms_shop_all_meat/code.html',
    'elikhope_farms_marketing_pages/elikhope_farms_visual_gallery/code.html',
]

processed = 0
errors = []

for f in files_auth:
    try:
        content = open(f, encoding='utf-8').read()
        content = replace_responsive_style(content, AUTH_RESPONSIVE)
        with open(f, 'w', encoding='utf-8') as fh:
            fh.write(content)
        processed += 1
        print('OK: ' + f)
    except Exception as e:
        errors.append('ERROR ' + f + ': ' + str(e))
        print('ERROR ' + f + ': ' + str(e))

for f in files_customer:
    try:
        content = open(f, encoding='utf-8').read()
        content = replace_responsive_style(content, CUSTOMER_RESPONSIVE)
        content = fix_customer_main_class(content)
        with open(f, 'w', encoding='utf-8') as fh:
            fh.write(content)
        processed += 1
        print('OK: ' + f)
    except Exception as e:
        errors.append('ERROR ' + f + ': ' + str(e))
        print('ERROR ' + f + ': ' + str(e))

for f in files_ecommerce:
    try:
        content = open(f, encoding='utf-8').read()
        n_before = content.count('id="ek-site-drawer"')
        if n_before > 1:
            content = dedup_site_drawers(content)
        n_after = content.count('id="ek-site-drawer"')

        if f == 'E-Commerce_Shop_UI Pages/checkout_order_review_elikhope_farms/code.html':
            content = add_mobile_nav_to_checkout_order_review(content)
            content = ensure_drawer_js(content)

        content = replace_responsive_style(content, ECOMMERCE_RESPONSIVE)

        with open(f, 'w', encoding='utf-8') as fh:
            fh.write(content)
        processed += 1
        print('OK (drawers ' + str(n_before) + '->' + str(n_after) + '): ' + f)
    except Exception as e:
        errors.append('ERROR ' + f + ': ' + str(e))
        print('ERROR ' + f + ': ' + str(e))

for f in files_marketing:
    try:
        content = open(f, encoding='utf-8').read()
        n_before = content.count('id="ek-site-drawer"')
        if n_before > 1:
            content = dedup_site_drawers(content)
        n_after = content.count('id="ek-site-drawer"')

        content = replace_responsive_style(content, MARKETING_RESPONSIVE)

        with open(f, 'w', encoding='utf-8') as fh:
            fh.write(content)
        processed += 1
        print('OK (drawers ' + str(n_before) + '->' + str(n_after) + '): ' + f)
    except Exception as e:
        errors.append('ERROR ' + f + ': ' + str(e))
        print('ERROR ' + f + ': ' + str(e))

print('')
print('Done: ' + str(processed) + '/32 processed')
if errors:
    print('ERRORS:')
    for e in errors:
        print(e)
