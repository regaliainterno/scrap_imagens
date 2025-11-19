# UI/UX Modernization Guide

This document outlines the design principles and potential enhancements for the Anunnakis Roteiros application.

## Current State

The application uses PySide6 with a custom dark theme. While functional, further modernization can improve user experience.

## Design Recommendations

### 1. **Modern Color Palette (Tailwind-inspired)**
- **Background**: `#0f172a` (slate-950)
- **Surface**: `#1e293b` (slate-800)
- **Primary Accent**: `#0ea5e9` (sky-500)
- **Text**: `#e2e8f0` (slate-100)
- **Borders**: `#334155` (slate-700)

### 2. **Typography**
- **Font Stack**: `-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif`
- **Sizes**:
  - Headers: 14pt, 600 weight
  - Body: 10pt, 400 weight
  - Labels: 10pt, 400 weight

### 3. **Spacing & Layout**
- **Base Unit**: 8px
- **Padding**: 8px, 12px, 16px, 20px
- **Margins**: 10px-16px for major sections
- **Border Radius**: 6px for input fields, buttons; 4px for secondary elements

### 4. **Interactive Elements**
- **Buttons**: Solid background with hover darkening (20% darker on hover)
- **Input Fields**: Subtle borders, glow on focus (2px sky-500 border)
- **Tabs**: Bottom-border indicator, color-coded states
- **Transitions**: 150-200ms ease-in-out for hover/focus effects

### 5. **Potential Enhancements (Future)**

#### A. Add custom CSS-like stylesheet file
Create `anunnakis_roteiros/src/styles.py` with centralized theme definitions:
```python
THEME_COLORS = {
    'bg_primary': '#0f172a',
    'bg_secondary': '#1e293b',
    'accent_primary': '#0ea5e9',
    'text_primary': '#e2e8f0',
    'border_color': '#334155',
}
```

#### B. Implement smooth transitions
Use `QPropertyAnimation` for:
- Hover scaling (buttons: 1.0 → 1.05)
- Color fades on state changes
- Slide animations for tab content

#### C. Create reusable widget components
- `ModernButton` with built-in animations
- `ModernLineEdit` with focus effects
- `ModernComboBox` with styled dropdown

#### D. Add icon system
Use a monochromatic icon set (e.g., Feather Icons, Tabler Icons) scaled at 20x20, 24x24, 32x32px.

#### E. Implement accessibility
- Keyboard navigation (Tab order, shortcuts)
- Focus indicators (visible outline on all interactive elements)
- Color contrast compliance (WCAG AA minimum)
- Font size adjustments for readability

### 6. **Modern Layout Patterns**

#### Recommended Container Structure:
```
[Header Section - 60px]
    ├─ Logo + Title
    └─ Quick Settings

[Tabs Container]
    ├─ Tab 1 (Gerador)
    ├─ Tab 2 (Biblioteca)
    └─ Tab 3 (Scraper)

[Content Area - Scrollable]
    └─ Tab-specific content with padding/spacing

[Status Bar - 30px]
    └─ Progress, status messages, help text
```

#### Grid-based spacing:
- Container padding: 16px
- Element gaps: 12px
- Section dividers: 8px + 1px border + 8px

### 7. **Dark Mode Advantages (Current)**
- Reduces eye strain in low-light environments
- Better for desktop applications
- Modern aesthetic
- Lower power consumption on OLED screens (future)

### 8. **Optional Light Mode**
If implementing light mode, use:
- **Background**: `#f8fafc` (slate-50)
- **Surface**: `#ffffff`
- **Text**: `#1e293b` (slate-900)
- **Primary**: `#0284c7` (sky-600) — darker for light mode

### 9. **Animation Best Practices**
- Duration: 150-200ms for interactive elements
- Easing: `QEasingCurve.InOutQuad` or `InOutCubic`
- Avoid: animations longer than 300ms (feels sluggish)
- Use: consistent animation timing across app

### 10. **Testing & Validation**
- Test on Windows 10/11 at different DPI scales (100%, 125%, 150%)
- Verify performance (no jank on animations)
- A/B test with users if possible

## Implementation Priority

1. **High Impact, Low Effort**:
   - Consolidate colors into a central palette
   - Update spacing/padding in layouts

2. **Medium Impact, Medium Effort**:
   - Add hover/focus effects with QPropertyAnimation
   - Create custom widget base classes

3. **Low Priority** (Consider for v2.0):
   - Implement light mode toggle
   - Add icon system
   - Accessibility audit & fixes

## File Locations

- **Main UI**: `anunnakis_roteiros/src/main.py`
- **Custom Styles** (if created): `anunnakis_roteiros/src/styles.py`
- **Themes** (if created): `anunnakis_roteiros/src/themes.py`

## References

- [Tailwind CSS Color Palette](https://tailwindcss.com/docs/customizing-colors)
- [PySide6 Styling Guide](https://doc.qt.io/qtforpython-6/overviews/stylesheet-syntax.html)
- [Apple Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines/)
- [Material Design 3](https://m3.material.io/)

---

**Current Status**: Functional design with modern dark theme.  
**Next Steps**: Consider enhancements from section 5 (A-E) based on user feedback and available dev time.
