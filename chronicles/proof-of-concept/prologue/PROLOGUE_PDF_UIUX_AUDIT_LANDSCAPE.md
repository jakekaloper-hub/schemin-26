# PROLOGUE PDF UI/UX AUDIT — LANDSCAPE REBUILD

**Status:** CORRECTIVE ACTION ACTIVE

## Bullpen finding

The PDF container must behave like the approved P1–P2 spread, not like a conventional portrait book or a gallery/contact sheet.

Binding output rules:
- one **facing-page pair** per PDF page;
- fixed landscape **3:2 spread canvas**, matching the approved P1–P2 source ratio;
- full bleed artwork with zero artificial margin;
- no fit-to-portrait behavior;
- no letterboxing introduced by PDF composition;
- every subsequent spread occupies the same physical canvas;
- spread order remains P1–P2, P3–P4 ... P31–P32;
- PDF navigation/bookmarks identify spread pairs;
- final PDF must be rendered back to PNG and visually compared before lock.

## Important content finding

Container/layout correction does **not** certify the later spread artwork itself. Several generated spreads contain UI/UX and typography problems (including generated pseudo-text and weaker visual grammar than P1–P2). Those remain Chronicle-content QA issues and must not be hidden by a better PDF wrapper.

This pass fixes the **PDF presentation system** first:
**P1–P2 template ratio → every spread → fixed landscape full bleed.**

Then content spreads can be corrected without changing the delivery geometry again.
