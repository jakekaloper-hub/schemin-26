# VISUAL WORLD PACKET SCHEMA V2

A visual packet is a read-only production compilation. It does not create canon.

## Required sections

### WORLD
- location_id
- physical_zone
- route context
- water context
- world_state
- history/memory
- institutions
- ordinary inhabitants

### ATLAS
- division presence
- owner domain
- arrival routes
- water relationship
- elevation relationship
- camera direction
- foreground terrain
- midground route/settlement
- background topography
- visible landmarks
- forbidden landmarks
- weather state

### DOMAIN
- architecture/materials
- economy/resources
- division culture
- civilization context

### CHARACTER
- current visual authority
- ontology
- body locks
- negative locks
- explicit reference status

### MEMORY
- prior events
- active scars
- temporary state
- prohibited literalization

### TYPOGRAPHY
- exact approved names
- deterministic label list
- generated text forbidden by default

## Renderer permissions

Renderer may change:
- style;
- lens/perspective;
- lighting;
- composition.

Renderer may not change:
- topology;
- physical region;
- route;
- hydrology;
- owner domain;
- location identity;
- persistent world state;
- principal body canon.

## Existing Location Control Plane

`world/location-control-plane/` remains the existing production packet compiler/adapters. V1.2 must extend or consume it rather than create a parallel location-card authority. Universe/Atlas V2 files provide additional world context; location IDs remain shared.

**GATE 11 DESIGN: READY**
