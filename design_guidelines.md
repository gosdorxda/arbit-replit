# Design Guidelines: Multi-Exchange Crypto Data Aggregator

## Design Approach

**Selected Framework:** Material Design principles adapted for financial data applications, with inspiration from trading platforms like Binance and data-heavy tools like Linear.

**Rationale:** This is a utility-focused, information-dense application where data clarity, scannability, and functional efficiency are paramount. The design prioritizes quick data comparison over aesthetic flourishes.

## Layout System

**Container Structure:**
- Maximum width: `max-w-7xl` centered with `mx-auto`
- Horizontal padding: `px-4 sm:px-6 lg:px-8`
- Vertical section spacing: `py-8` for compact sections, `py-12` for major divisions

**Spacing Primitives:**
Use Tailwind units: **2, 3, 4, 6, 8, 12** for consistent rhythm
- Micro spacing (within components): `gap-2`, `p-3`
- Component spacing: `gap-4`, `mb-6`
- Section spacing: `space-y-8`, `mt-12`

## Typography Hierarchy

**Font Stack:**
- Primary: Inter (via Google Fonts CDN) - excellent for data-heavy interfaces
- Monospace: JetBrains Mono - for numerical data, prices, timestamps

**Type Scale:**
- Page Title: `text-3xl font-bold` 
- Section Headers: `text-xl font-semibold`
- Data Table Headers: `text-sm font-medium uppercase tracking-wide`
- Body/Data: `text-base` for descriptive text, `text-sm` for table cells
- Small metadata (timestamps): `text-xs`
- Numbers/Prices: `font-mono text-base` for consistency

## Core Components

### 1. Header Section
- Simple top banner with application title and brief description
- Layout: Single row, left-aligned title, optional right-aligned metadata
- Padding: `py-6 border-b`

### 2. Control Panel (Action Zone)
**Layout:** Horizontal flex layout with responsive stacking
- Two prominent fetch buttons (LBANK, HashKey) side by side on desktop (`flex gap-4`)
- Button styling: Large size (`px-6 py-3`), rounded (`rounded-lg`), with icons from Heroicons
- Status indicators below buttons: Small badges showing last fetch time and status
- Filter/Sort controls in separate row below: Dropdowns and search input aligned horizontally

### 3. Data Table (Primary Component)
**Structure:**
- Full-width responsive table with horizontal scroll on mobile
- Sticky header row for scrolling contexts
- Column widths: Exchange (15%), Symbol (20%), Price (15%), Volume (15%), High/Low (12% each), Change (11%)
- Row height: Comfortable `h-12` minimum for readability
- Alternating row treatment for scannability

**Table Headers:**
- Uppercase, small font size, medium weight
- Sortable columns indicated with icon (Heroicons arrow-up/down)
- Alignment: Left for text (Exchange, Symbol), Right for numbers (Price, Volume, etc.)

**Table Cells:**
- Numbers use monospace font for alignment
- Right-aligned for numerical data
- Padding: `px-4 py-3`
- Change % includes directional indicator (arrow icon)

### 4. Empty/Loading States
- Centered message in table area when no data
- Loading spinner (Heroicons refresh icon with spin animation) during fetch
- Gentle skeleton loader for table rows (optional enhancement)

### 5. Status Indicators
- Small badges/pills showing fetch status
- Timestamp display in small text beneath action buttons
- Format: "Last updated: [time]" with relative time (e.g., "2 minutes ago")

## Component Specifications

### Buttons
- Primary action buttons: Large size, rounded corners (`rounded-lg`)
- Icon + text combination using Heroicons (database or refresh icons)
- States: Default, hover (subtle lift via shadow), active (slight scale), disabled (reduced opacity)
- Loading state: Replace text with spinner icon

### Filters & Inputs
- Dropdown selects: Styled with custom appearance, consistent height (`h-10`)
- Search input: Icon prefix (Heroicons magnifying glass), placeholder text, rounded
- Layout: Horizontal arrangement with labels or compact label-inside-input pattern

### Badges/Pills
- Small, rounded containers for status indicators
- Padding: `px-2 py-1 text-xs rounded-full`
- Used for: Exchange name labels, status (success/error), change direction

## Responsive Behavior

**Desktop (lg and up):**
- Table displays all columns
- Buttons arranged horizontally
- Filters in single row

**Tablet (md):**
- Table maintains structure but may require horizontal scroll
- Buttons remain horizontal
- Filters stack if needed

**Mobile (base):**
- Buttons stack vertically (`flex-col`)
- Table converts to card-based layout OR horizontal scroll with pinned first column
- Filters stack vertically with full width

## Accessibility Implementation

- All interactive elements keyboard navigable
- Focus states clearly visible with outline
- Table headers use semantic `<th>` with `scope` attributes
- Color-independent indicators for change direction (icons + numerical sign)
- ARIA labels for icon-only buttons
- Sufficient contrast for all text (verified against WCAG AA)

## Animation Strategy

**Minimal, Purposeful Animations:**
- Fetch button: Spinner icon rotation during loading (2s linear infinite)
- Table rows: Fade-in on data load (`transition-opacity duration-300`)
- Avoid: Elaborate transitions, scroll effects, decorative animations

## Data Visualization Enhancements

**Change Percentage:**
- Positive: Upward arrow icon prefix
- Negative: Downward arrow icon prefix
- Zero: Dash or equals symbol

**Volume Formatting:**
- Abbreviated notation (e.g., "1.2M", "543.5K") with tooltip for full value
- Consistent decimal places (2 for prices, 1 for volume abbreviations)

---

**Design Philosophy:** Professional, data-first interface optimized for quick scanning and comparison. Every element serves a functional purpose. Clarity over creativity, efficiency over embellishment.