# Civil Engineering Estimation Tool - Design Guidelines

## Design Approach
**System-Based Design**: Drawing from Carbon Design System (enterprise data applications) and Linear (clean productivity tools) to create a professional, data-focused estimation platform for government PWD/ZP projects.

**Core Principles:**
- Clarity and precision in data presentation
- Efficient data entry workflows
- Excel-familiar interaction patterns
- Professional government-standard aesthetics

---

## Typography System

### Font Families
- **Primary**: Inter (via Google Fonts CDN) - for UI elements, labels, data entry
- **Monospace**: JetBrains Mono - for numerical data, calculations, measurements

### Type Scale
- **Page Headers**: text-2xl font-semibold (Project titles, sheet names)
- **Section Headers**: text-lg font-medium (Abstract sections, component categories)
- **Table Headers**: text-sm font-semibold uppercase tracking-wide
- **Body/Data**: text-sm font-normal (Form inputs, table cells)
- **Labels**: text-xs font-medium uppercase tracking-wider
- **Calculations/Numbers**: text-sm font-mono (Quantities, rates, amounts)
- **Small Print**: text-xs (Units, helper text)

---

## Layout System

### Spacing Primitives
Use Tailwind units: **2, 4, 6, 8, 12, 16**
- Tight spacing: p-2, gap-2 (within form groups)
- Standard spacing: p-4, gap-4 (between form fields, table cells)
- Section spacing: p-6, gap-6 (between major sections)
- Page spacing: p-8 (main content areas)
- Large breaks: mb-12, mt-16 (between major components)

### Grid Structure
- **Main Application**: Sidebar navigation (w-64) + Content area (flex-1)
- **Content Width**: max-w-7xl mx-auto (standard content container)
- **Form Layouts**: Two-column grid on desktop (grid-cols-2 gap-4), single column mobile
- **Table Layouts**: Full-width with horizontal scroll on mobile (overflow-x-auto)

---

## Component Library

### Navigation Structure
**Sidebar Navigation (Left, Fixed)**
- Project selector dropdown at top
- Expandable/collapsible sections for:
  - Dashboard (overview)
  - Measurement Sheets (collapsible submenu: Civil Work, Sanitary Work, Landscape Work, Electrical Work, etc.)
  - Abstracts (General Abstract, SSR-Based Abstract, Abstract of Cost)
  - SSR Database
  - Reports & Export
- Active state: subtle left border accent, background tint
- Icon library: Heroicons (outline style)

**Top Bar**
- Project name/title (left)
- Quick actions: Save, Export, Print (right)
- User profile/settings (far right)

### Data Entry Forms

**Measurement Entry Form**
- Card-based layout (rounded corners, subtle border)
- Form grid: 6 columns for measurement data
  - Item No. (col-span-1)
  - Description (col-span-2)
  - Quantity (col-span-1)
  - Length, Breadth, Height (col-span-1 each)
  - Unit dropdown (col-span-1)
  - Total (col-span-1, auto-calculated, read-only with distinct background)
- Add Row button (with plus icon) below form
- Save Changes button (primary action) at bottom right

**Input Field Specifications**
- Standard height: h-10
- Border: border rounded
- Focus state: ring-2 ring-offset-0
- Disabled/calculated fields: distinct muted background
- Number inputs: right-aligned text for easy scanning

### Tables

**Measurement Sheet Tables**
- Sticky header row (position-sticky top-0)
- Alternating row backgrounds for readability
- Bordered cells (border-collapse)
- Column widths optimized:
  - Item No: w-16
  - Description: flex-1 (min-width-200)
  - Numeric columns: w-24 each
  - Unit: w-20
  - Actions: w-16
- Row hover state: subtle background change
- Editable cells: cursor-text, click to edit
- Totals row: bold, distinct background at table bottom

**Abstract Tables**
- Similar structure to measurement tables
- Additional columns: Rate (from SSR), Amount (auto-calculated)
- Summary section below table showing:
  - Sub-total
  - Add: (various government additions)
  - Grand Total
- Each summary line: right-aligned amounts, bold totals

### Cards & Panels

**Dashboard Summary Cards**
- Grid layout: grid-cols-1 md:grid-cols-2 lg:grid-cols-4
- Card structure:
  - Icon (top-left, in subtle background circle)
  - Label (text-sm)
  - Value (text-2xl font-semibold)
  - Change indicator if applicable (text-xs)
- Border, rounded-lg, p-6

**Component Section Cards**
- Collapsible card design
- Header with expand/collapse icon
- Content padding: p-6
- Border between sections

### Buttons & Actions

**Primary Actions**: Solid background, medium weight font, h-10 px-4 rounded
**Secondary Actions**: Border only (outline), same dimensions
**Tertiary Actions**: Text only with hover underline
**Icon Buttons**: Square (h-10 w-10), centered icon, rounded
**Save/Submit**: Prominent placement, bottom-right of forms

### SSR Database Interface

**Search & Filter Bar**
- Search input with icon (w-full max-w-md)
- Category filter dropdowns (inline, gap-4)
- Results count indicator

**SSR Items Display**
- Table format with columns: Code, Description, Unit, Rate, Effective Date
- Quick-select action for applying to measurements
- Pagination at bottom

### Reports & Export

**Preview Panel**
- Print-optimized layout preview
- A4 format simulation (max-w-4xl)
- Government standard formatting:
  - Official headers
  - Table formatting
  - Signature blocks
  - Date/reference numbers

**Export Options**
- Button group for: Excel, PDF, Print
- Each with appropriate icon from Heroicons

---

## Animations & Interactions

**Minimal, Purposeful Motion**
- Sidebar expand/collapse: transition-all duration-200
- Dropdown menus: fade-in with slight slide (duration-150)
- Form validation feedback: subtle shake on error
- Table row hover: transition-colors duration-100
- No auto-scrolling animations
- No decorative animations

**Loading States**
- Spinner for calculations (when processing large datasets)
- Skeleton loading for tables when fetching data
- Progress bar for export operations

---

## Page-Specific Layouts

### Dashboard (Home)
- Summary cards grid at top (4 cards: Total Projects, Active Sheets, Pending Abstracts, Recent Activity)
- Recent Projects table below
- Quick access shortcuts to create new measurement sheet

### Measurement Sheet View
- Breadcrumb navigation (Project > Component Type > Sheet Name)
- Sheet header with title and metadata (created date, last modified)
- Data entry form (sticky at top or in modal)
- Measurement table (main content, full width)
- Totals summary panel (right sidebar or below table)
- Action buttons: Add Row, Delete Selected, Import from Excel

### Abstract View
- Two-panel layout option: Measurement source (left) + Abstract (right)
- Or single scrollable view with linked highlighting
- SSR rate selector integrated inline or as modal
- Auto-calculation indicators showing formula source
- Export/Print preview button prominent

### SSR Database View
- Full-width table with advanced filtering
- Side panel for SSR item details when selected
- Add to Project quick action

---

## Responsive Behavior

**Desktop (lg and above)**: Full sidebar, multi-column forms, wide tables
**Tablet (md)**: Collapsible sidebar (hamburger menu), two-column forms, horizontal scroll tables
**Mobile**: Hidden sidebar (hamburger), single-column forms, stacked table view with essential columns only, floating action button for primary actions

---

## Data Visualization

**Calculation Flows**
- Visual indicators showing measurement → quantity → rate → amount relationships
- Subtle connecting lines or grouped sections
- Auto-updated values with brief highlight animation on change

**Formulas Display**
- Show formula on hover for calculated cells
- Formula bar option (Excel-like) for advanced users

---

## Professional Trust Elements

- Government-compliant header with official formatting options
- Audit trail indicators (created by, modified by, timestamps)
- Version history access
- Approval workflow status badges
- Official seal/logo placement options
- Disclaimer text in footers for official documents

This design creates a professional, efficient, data-centric application that civil engineers will find familiar and powerful for government estimation work.