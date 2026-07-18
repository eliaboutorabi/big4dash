# FirmScope design system

## Direction

FirmScope should feel like a serious research instrument with the polish of a modern strategy product. The interface uses a light, quiet work surface; a deep ink navigation rail; honey-colored interaction cues; and firm colors only where they carry comparative meaning.

## Typography

- Manrope Variable for navigation, interface copy and editorial headings
- JetBrains Mono Variable for reported values, dates, scores and ranks
- Large headings use tight tracking and compact line-height; supporting copy remains small and deliberately calm

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

## Component language

Surfaces use restrained 8–16px radii, hairline dividers and minimal shadow. Cards are reserved for independent analytical objects; related values use bands, rows and direct grouping instead of nested containers. Icons come from Lucide and never replace a necessary label.
