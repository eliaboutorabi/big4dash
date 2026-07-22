# FirmScope design system

## Direction

FirmScope should feel like a serious research instrument with the confidence of an independent editorial object. The visual language is subtle neo-brutalism: graph-paper structure, disciplined framing, compact hard shadows, assertive yellow signals, and firm colors only where they carry comparative meaning. The dark theme uses low-chroma graphite surfaces, near-neutral cool type, quiet gray borders, and shorter shadows; warmth is reserved for small honey signals. The result should feel authored and memorable without compromising analytical credibility.

## Typography

- Manrope Variable for navigation, controls, explanatory copy and analytical labels
- Newsreader Variable for the large editorial statements that open the overview and each research chapter
- JetBrains Mono Variable for reported values, dates, scores and ranks
- Display type is reserved for narrative headings; supporting copy is comfortably readable at 12–16px and never treated as decorative microtype

## Color roles

- Pure white for primary analysis surfaces
- Cool low-chroma gray for the application canvas and dividers
- Deep blue-black for navigation, evidence cards and decisive actions
- Honey for focus, methodology and guided-learning cues
- Deloitte green, PwC orange, EY yellow and KPMG blue only for firm identity and comparison marks
- Service-line and geography palettes use separate semantic scales to avoid confusing categories with firms

All implementation colors are defined in OKLCH in `src/routes/layout.css`.

The light and dark themes share the same semantic token names. Text, frames, inverse surfaces, and shadow colors have distinct roles so the dark theme never produces white structural rules or accidental light panels. It remaps those roles rather than applying a global inversion, preserving firm and chart semantics in both modes.

Dark-mode elevation follows four explicit levels: the canvas is darkest, flat structural bands use the default surface and a border, raised analytical objects use a lighter elevated surface with a 4px zero-blur offset shadow, and overlays use the lightest surface with an 8px hard shadow or a directional hard drawer edge. Small highlighted controls use a 2px offset; focal calls to action may use the honey shadow. Shadow geometry never changes arbitrarily between themes, and soft atmospheric shadows are not part of the neo-brutalist vocabulary.

The FirmScope mark is a contiguous two-by-two field with one firm color anchored in each corner and an upright numeral 4 centered over their shared intersection. The colors touch as one market; the numeral names the category without becoming a fifth, unrelated brand color.

## Interaction principles

1. Make the comparison visible before asking for interaction.
2. Keep evidence one action away from every analytical mark.
3. Use progressive disclosure for definitions, caveats and reporting hierarchies.
4. Preserve a stable visual frame when users change the metric or firm selection.
5. Keep motion brief and state-based; never delay analytical reading.
6. Anchor chart tooltips just above the active mark, clamp them inside the plot, and flip them below only when the upper edge would collide.
7. Distinguish source coordinates from city-centroid joins through explicit provenance copy and persistent methodology notes.

## Spatial visualization

- The 2D atlas and 3D globe use the same 2,206 mapped records and the same firm-color mapping. Deloitte contributes 699 unique plotted locations from an 867-entry official directory snapshot; KPMG contributes 327 locations normalized from 76 official country-directory pages.
- Office marks are translucent filled points in every coverage tier. Markers that would collide separate into a compact petal group with one firm-colored point per network; the readout reports the underlying firm and mapped-record counts. This preserves the shared geography while ensuring no firm is hidden beneath another.
- Deloitte, EY, and PwC use source-linked or structured directory coordinates. KPMG office-city labels are joined to GeoNames city centroids and are identified as such in the readout.
- The globe uses a textured world-atlas sphere, drag/zoom controls, restrained auto-rotation, a taller uncropped stage, and a projection transition that preserves the map’s spatial context. Co-located globe markers receive small tangent-plane offsets so all represented networks remain visible without implying a different city.
- Firm filters and the selected-office readout remain shared between projection modes.

## Component language

Primary surfaces use square or near-square corners, 1.5px structural rules, and tokenized 2px, 4px, 6px, or 8px zero-blur offset shadows. Shadows indicate actual elevation: bands, rows, and grouped values remain flat; independent analytical objects are raised; dialogs, drawers, tooltips, and the guided tour occupy the overlay level. Buttons within one action group share the same border, shadow, hover, and pressed mechanics; hierarchy comes from fill and contrast rather than a different silhouette. Softer dividers remain inside dense tables and charts. Cards are reserved for independent analytical objects; related values use bands, rows, editorial rails, and direct grouping instead of nested containers. Icons come from Lucide and never replace a necessary label.

## Motion language

- Trend series rise from the chart baseline as one analytical state change whenever the metric or selected-firm set changes. Smooth monotone curves, translucent strokes, and soft same-color points reduce collisions without adding halos.
- Composition and market-share bars stretch as complete stacks from their shared baseline; individual color segments never fill independently.
- The office atlas keeps analytical marks static and immediately readable; only the globe’s restrained orbit and the projection transition provide ambient motion.
- Section content rises gently on first entry where view-timeline animation is supported.
- Reduced-motion preferences collapse all animation to an immediate final state.
