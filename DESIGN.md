# FirmScope design system

## Direction

FirmScope should feel like a serious research instrument with the confidence of an independent editorial object. The visual language is subtle neo-brutalism: cool graph-paper structure, deep ink outlines, compact hard shadows, assertive yellow signals, and firm colors only where they carry comparative meaning. The result should feel authored and memorable without compromising analytical credibility.

## Typography

- Manrope Variable for navigation, interface copy and editorial headings
- JetBrains Mono Variable for reported values, dates, scores and ranks
- Large headings use tight tracking and compact line-height; supporting copy is comfortably readable at 12–16px and never treated as decorative microtype

## Color roles

- Pure white for primary analysis surfaces
- Cool low-chroma gray for the application canvas and dividers
- Deep blue-black for navigation, evidence cards and decisive actions
- Honey for focus, methodology and guided-learning cues
- Deloitte green, PwC orange, EY yellow and KPMG blue only for firm identity and comparison marks
- Service-line and geography palettes use separate semantic scales to avoid confusing categories with firms

All implementation colors are defined in OKLCH in `src/routes/layout.css`.

## Interaction principles

1. Make the comparison visible before asking for interaction.
2. Keep evidence one action away from every analytical mark.
3. Use progressive disclosure for definitions, caveats and reporting hierarchies.
4. Preserve a stable visual frame when users change the metric or firm selection.
5. Keep motion brief and state-based; never delay analytical reading.
6. Keep hover information in stable readout regions outside dense plots so a popover can never occlude the mark that opened it.
7. Distinguish complete source directories from representative samples through mark shape, copy, and persistent methodology notes.

## Component language

Primary surfaces use square or near-square corners, 1.5–2px ink rules, and 3–7px hard offset shadows. Softer dividers remain inside dense tables and charts. Cards are reserved for independent analytical objects; related values use bands, rows, editorial rails, and direct grouping instead of nested containers. Icons come from Lucide and never replace a necessary label.

## Motion language

- Trend lines draw into place and data points enter with short scale fades.
- Composition bars grow from their shared baseline.
- The office atlas uses a low-contrast scan sweep while all analytical marks remain static and immediately readable.
- Section content rises gently on first entry where view-timeline animation is supported.
- Reduced-motion preferences collapse all animation to an immediate final state.
