# Week 3 Native-Mobile Production Contract V1
**Primary surface:** typical iPhone/Apple mobile PDF viewer. **Master orientation:** portrait ~9:16.

## Master
- Working master: 1080 × 1920 px equivalent (9:16) or vector/PDF dimensions preserving exactly that ratio.
- No page may be generated at arbitrary ratio and destructively cropped/stretch-fit later.
- Locked page masters are immutable during PDF assembly.
- Maintain protected edge-safe zones of at least 5% of width and 4% of height for critical text/faces/data.
- Bleed/background art may extend to edge; critical content may not.

## Typography/readability
- Body copy must be tested at actual phone-view scale; use the largest practical size consistent with page purpose.
- Avoid dense multi-column body copy on phone.
- Headline, deck, body, caption and deterministic data modules must have visibly distinct hierarchy.
- Long literary pages may carry 300–700 words only when actual-scale readability passes; otherwise split the page.
- Exact score/standings modules require deterministic typography.

## Composition zones
- Protect focal faces/identity features from trim, fold-equivalent edges and data overlays.
- Reserve deterministic text-safe regions in the Page Brief before art.
- Score modules should occupy a stable high-contrast zone, but not force every page into the same template.
- Footer/page numbering remains subordinate to story image/copy.

## Mobile QA
Render the page at final ratio; inspect at 100% phone-equivalent scale; verify no clipped glyphs, unreadable body text, edge collisions, distorted art, accidental landscape ratio, or focal character under UI/data overlays. Any failure = PATCH or REGENERATE before PAGE_LOCK.
