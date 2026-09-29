# ATLAS V1 — SCHEMIN WORLD ENGINE

**Status:** RELEASE CANDIDATE / DATA-DRIVEN ATLAS  
**Coordinate space:** Schemin-local-v1, abstract and non-metric

## Purpose

Atlas V1 is not one overloaded fantasy poster. It is a family of views over the same world data.

## Layer products

1. **Physical Atlas** — seven causal physical zones.
2. **Division Atlas** — Burgers / Wings / Pizza overlay.
3. **Owner Domain Atlas** — twelve owner relationships to place.
4. **Roads & Travel Atlas** — routes and travel classes.
5. **World-State Atlas** — scars, weather, contamination, repairs and historical events.
6. **Weather Atlas** — regional propagation.
7. **Horizon/Visibility Atlas** — composition continuity.

## Division macro-placement

### Burgers
North-central highlands, upper valleys, market roads and selected stormward escarpments.

### Wings
Western frontier through southern wetland/delta country.

### Pizza
Eastern mountain-to-coast arc and inner-sea mercantile corridor.

The divisions are connected territories with porous march zones. They are not sovereign food kingdoms.

## Published location placement

World Engine V1 places the principal recurring sites into the seven-zone model:
- Trade Jedi Mountain Base — upper eastern valleys / Pizza.
- Mud Dogs Swamp — southern wetlands / Wings.
- Country Club of Jackson — raised southern wetlands / Wings.
- Arsenal Barbershop — upper valleys / Burgers.
- Red Leopard Ruins — stormward eastern escarpment / Burgers.
- TDS Waterfall Temple — southern wet escarpment / Wings.
- Chili Stable — western tablelands / Wings.
- LLC Boardroom — inner-sea littoral / Pizza.
- Belt Keeper Rune Keep — northeast storm cliffs / Pizza.
- League Chamber / Pittsy's Book — central basin neutral network.

Week 3 event sites remain explicitly provisional where the published story proves the scene but not permanent civic status.

## Rendering doctrine

Rendering reads world data and cannot mutate it.

A production renderer may:
- stylize;
- label;
- hide/show layers;
- alter scale;
- choose camera framing.

It may not:
- move a location to a different zone;
- rewrite a division;
- add permanent roads;
- erase state consequences;
- convert generated scenery into canon.

## Prototype

`world/atlas/render_atlas_svg.py` creates a deterministic schematic SVG from the machine records. It is a QA/prototyping renderer, not final illustrated art direction.

**PHASE 11 DATA/RENDER ARCHITECTURE: READY FOR CI**
