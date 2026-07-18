# FirmScope

An evidence-first interactive dashboard comparing Deloitte, PwC, EY and KPMG across scale, growth, business mix, geography and workforce.

The interface is designed as a research product rather than a static report. Every headline, chart point and composition segment can open the underlying observation, source excerpt, reporting period, locator, quality flag and comparability score.

## Highlights

- Fifteen-year revenue comparison with switchable workforce and local-currency growth views
- FY2025 service-line and regional composition comparisons
- Revenue-versus-workforce field and directional revenue-per-person proxy
- Searchable evidence ledger containing 651 observations from 71 sources
- Firm profiles and source-level evidence drawers for progressive disclosure
- Eight-step Driver.js product tour with custom presentation and smooth section transitions
- Responsive desktop and mobile research navigation
- Local variable fonts, Lucide iconography and an OKLCH design-token system

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
```

## Data flow

Canonical research files live in `data/`. `scripts/build-dashboard-data.mjs` validates and composes them into the typed dashboard artifact at `src/lib/data/dashboard-data.json`. The original observation and source identifiers remain intact so the UI can trace every comparison back to its evidence.

## Stack

Svelte 5, SvelteKit, TypeScript, Driver.js, Lucide and static-site deployment via `@sveltejs/adapter-static`.
