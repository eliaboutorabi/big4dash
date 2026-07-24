# FirmScope

An evidence-first interactive dashboard comparing Deloitte, PwC, EY and KPMG across scale, growth, business mix, geography and workforce.

The interface is designed as a research product rather than a static report. Every headline, chart point and composition segment can open the underlying observation, source excerpt, reporting period, locator, quality flag and comparability score.

## Highlights

- Revenue mosaic, reporting-calendar comparison and fifteen-year indexed growth race
- Historical within-four revenue-share ribbon with an interactive year scrubber
- Transparent scenario studio for five-year CAGR, latest-pace and custom assumptions
- Switchable revenue, workforce and local-currency trend views with point-level evidence
- Service-line composition in proportional and reported-dollar modes
- Revenue-versus-workforce productivity frontier with directional iso-productivity bands
- Pairwise workbench for comparing any two firms across five decision-useful measures
- Disclosure-coverage matrix that makes taxonomy and comparability gaps visible
- Original-to-revised disclosure lineage for restatements and later comparatives
- Searchable evidence ledger containing 651 observations from 71 sources
- Keyboard command palette spanning chapters, firms, metrics and source records
- Bookmarkable evidence notebook with CSV and Markdown exports
- Shareable URL state and progressive-disclosure drawers
- Two-dimensional office atlas with an optional, deferred 3D globe
- Responsive light and dark themes, keyboard-aware dialogs and opt-in guided tour

## Run locally

```sh
npm install
npm run dev
```

The development and production commands rebuild the frontend data artifact from the canonical CSV package automatically.

## Quality checks

```sh
npm run check
npm run build
npm run lint
npm run data:validate
npm run test:e2e
```

Run the complete release gate with `npm run quality`. The gate rebuilds the derived artifact,
checks Svelte and TypeScript, verifies formatting and lint rules, validates the research data
contract, builds the static application and exercises the primary dashboard interactions in
Chromium.

## Data flow

Canonical research files live in `data/`. `scripts/build-dashboard-data.mjs` validates and
composes them into the typed dashboard artifact at `src/lib/data/dashboard-data.json`. The
original observation and source identifiers remain intact so the UI can trace every comparison
back to its evidence. Contract tests protect counts, identities, source lineage, office
coordinates, market-share reconciliation and CAGR calculations from silent regressions.

## Stack

Svelte 5, SvelteKit, TypeScript, Driver.js, Lucide and static-site deployment via `@sveltejs/adapter-static`.
