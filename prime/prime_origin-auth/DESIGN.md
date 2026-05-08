---
name: Prime Origin
colors:
  surface: '#fcf9f8'
  surface-dim: '#dcd9d9'
  surface-bright: '#fcf9f8'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#f6f3f2'
  surface-container: '#f0eded'
  surface-container-high: '#eae7e7'
  surface-container-highest: '#e5e2e1'
  on-surface: '#1c1b1b'
  on-surface-variant: '#404a3c'
  inverse-surface: '#313030'
  inverse-on-surface: '#f3f0ef'
  outline: '#707a6a'
  outline-variant: '#bfcab8'
  surface-tint: '#0b6e10'
  primary: '#004e05'
  on-primary: '#ffffff'
  primary-container: '#01690a'
  on-primary-container: '#8be77b'
  inverse-primary: '#80db71'
  secondary: '#396a25'
  on-secondary: '#ffffff'
  secondary-container: '#b9f29c'
  on-secondary-container: '#3f702a'
  tertiary: '#314900'
  on-tertiary: '#ffffff'
  tertiary-container: '#436300'
  on-tertiary-container: '#a4e524'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#9bf98b'
  primary-fixed-dim: '#80db71'
  on-primary-fixed: '#002201'
  on-primary-fixed-variant: '#005306'
  secondary-fixed: '#b9f29c'
  secondary-fixed-dim: '#9ed583'
  on-secondary-fixed: '#062100'
  on-secondary-fixed-variant: '#21510d'
  tertiary-fixed: '#b5f739'
  tertiary-fixed-dim: '#9ad912'
  on-tertiary-fixed: '#131f00'
  on-tertiary-fixed-variant: '#354e00'
  background: '#fcf9f8'
  on-background: '#1c1b1b'
  surface-variant: '#e5e2e1'
typography:
  h1:
    fontFamily: plusJakartaSans
    fontSize: 48px
    fontWeight: '700'
    lineHeight: '1.2'
    letterSpacing: -0.02em
  h2:
    fontFamily: plusJakartaSans
    fontSize: 36px
    fontWeight: '700'
    lineHeight: '1.2'
    letterSpacing: -0.01em
  h3:
    fontFamily: plusJakartaSans
    fontSize: 24px
    fontWeight: '600'
    lineHeight: '1.3'
  h4:
    fontFamily: plusJakartaSans
    fontSize: 20px
    fontWeight: '600'
    lineHeight: '1.4'
  body-lg:
    fontFamily: inter
    fontSize: 18px
    fontWeight: '400'
    lineHeight: '1.6'
  body-md:
    fontFamily: inter
    fontSize: 16px
    fontWeight: '400'
    lineHeight: '1.6'
  body-sm:
    fontFamily: inter
    fontSize: 14px
    fontWeight: '400'
    lineHeight: '1.5'
  label-caps:
    fontFamily: inter
    fontSize: 12px
    fontWeight: '600'
    lineHeight: '1'
    letterSpacing: 0.05em
  price-lg:
    fontFamily: plusJakartaSans
    fontSize: 28px
    fontWeight: '700'
    lineHeight: '1'
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  base: 8px
  container-max: 1280px
  gutter: 24px
  margin-mobile: 16px
  margin-desktop: 48px
  stack-sm: 12px
  stack-md: 24px
  stack-lg: 48px
---

## Brand & Style

This design system establishes a visual language that bridges the gap between traditional artisanal butchery and high-end digital commerce. The brand personality is grounded, transparent, and sophisticated, evoking the feeling of a premium boutique market rather than a generic supermarket. 

The chosen style is **Minimalism with Corporate Modern influences**, prioritizing high-density whitespace and structural clarity to communicate hygiene and professionalism. The interface relies on "editorial-grade" product photography—macro shots of marbled textures and fresh garnishes—to serve as the primary visual driver. The UI remains understated and functional, allowing the quality of the product to occupy the center stage.

## Colors

The palette is rooted in a spectrum of greens that signify life, growth, and rigorous quality standards. 

- **Primary Green (#01690A):** Used for primary actions, brand identifiers, and trust signals.
- **Deep Green (#2E5E1A):** Reserved for complex navigational elements and secondary backgrounds to provide a sense of established professionalism.
- **Accent Green (#95D405):** A high-vibrancy "Freshness" indicator used sparingly for badges (e.g., "New Arrival," "In Stock") and subtle highlights to draw the eye without overwhelming the premium aesthetic.
- **Neutrals:** A pure white (#FFFFFF) is the foundation for cleanliness, while the soft neutral (#F5F5F5) is used for layout grouping to prevent eye fatigue. The "Premium Depth" neutral (#1A1A1A) is used for high-contrast typography and footer sections.

## Typography

This design system utilizes a dual-font strategy to balance character with utility. **Plus Jakarta Sans** provides a modern, slightly rounded, and friendly geometric structure for headlines, echoing the premium and welcoming nature of the brand. **Inter** is utilized for all functional text, descriptions, and UI controls to ensure maximum readability at small sizes and high-density information displays (like weight specs and nutritional data).

Tighten letter spacing on large H1 and H2 headlines to create a "locked-in," editorial look. Use the `label-caps` style for small metadata like "Weight" or "Origin" to create a distinct hierarchy against body copy.

## Layout & Spacing

The layout philosophy follows a **Fixed Grid** approach for desktop to maintain a curated, premium feel, centering the content within a 1280px container. A 12-column grid provides flexibility for product listings (4 columns per item) and featured sections (split 6/6 or 8/4).

The spacing rhythm is built on an 8px baseline. Generous "Stack" units (48px+) are used between major sections to prevent the interface from feeling cluttered, reinforcing the "clean and hygienic" brand pillar. Product grids should utilize the 24px gutter to provide breathing room for high-quality imagery.

## Elevation & Depth

Visual hierarchy is conveyed through **Ambient Shadows** and tonal layering. Rather than harsh borders, this design system uses soft, diffused shadows with a slight tint of the Primary Green (#01690A) at very low opacity (2-4%). This creates a "lifted" effect for cards that feels natural and light.

- **Level 1 (Subtle):** Used for persistent cards and product items in a grid.
- **Level 2 (Active):** Used for hover states and cart drawers.
- **Level 3 (System):** Reserved for modals and critical pop-overs.

Surface-on-surface depth is achieved by placing white (#FFFFFF) cards atop the soft neutral (#F5F5F5) background, minimizing the need for heavy drop shadows.

## Shapes

The design system utilizes **Rounded** geometry (Level 2). A base radius of 0.5rem (8px) is applied to buttons and standard input fields, while larger containers like product cards and hero banners utilize 1rem (16px) or 1.5rem (24px) to create a softer, more approachable aesthetic. This choice balances the "sharpness" of a butcher’s knife with the "softness" of high-quality service and organic products.

## Components

### Buttons
- **Primary:** Solid #01690A background with white text. High-contrast, bold, 8px radius.
- **Secondary:** Outlined with #01690A, 1.5px stroke width.
- **Tertiary:** Text-only with an icon, used for low-priority actions.

### Cards
Product cards are the core component. They must feature a white background, Level 1 ambient shadow, and a 16px corner radius. The image container should have a subtle 1px inner border (#E5E5E5) to separate the product shot from the card background if the photo has a white backdrop.

### Inputs & Selection
- **Fields:** 8px radius, #F5F5F5 background with a subtle gray border that turns Primary Green on focus.
- **Chips:** Used for meat categories (e.g., "Grass-fed," "Wagyu"). 100px radius (pill-shaped), using the Accent Green (#95D405) for high-visibility attributes.

### Trust Indicators
Dedicated components for "Farm-to-Table Traceability" certificates and "Hygienic Packaging" badges should use the Deep Green (#2E5E1A) and clear iconography to reinforce the brand's commitment to quality.

### Imagery
All product imagery must be shot on neutral or natural wooden backgrounds with consistent lighting. Use a 4:5 or 1:1 aspect ratio for all product listings to maintain grid harmony.