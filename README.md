# Pokémon Reborn

The public record of Astra's HARDCAP playthrough of Pokémon Reborn 19.5.43, published at
[jehlp.net/pokemon-reborn](https://jehlp.net/pokemon-reborn/). It uses the shared
[site theme](https://jehlp.net/site-theme/) and its `pokemon-reborn` mark.

| Page | Contents |
| --- | --- |
| `reasoning/` | One page for each of the 31 gameplay tasks. Each page shows Astra's REASONING messages with their EDT times. |
| `notes/` | 195 planning notes, one page each. The index opens a note in place. |
| `scripts/` | 1,197 gameplay scripts. The index opens a highlighted script in place. |

## Selection

The source is the private `reborn` checkout. `data/selection.json` lists every published note and script.

- Notes: plans, preplans, preparation, proposals, strategy and tactical reviews, route plans and play policy.
  Status, navigation and map snapshots, team and battle records, progress logs and handoffs are not published.
  Copied walkthrough text is not published.
- Scripts: gameplay automation and handoff tooling.
  Video, audio, recording, idle-cut, panel, export and archive scripts are not published.
- Reasoning: only the REASONING messages from `CODEX_LOG.md`. Prompts, steers and tool lines stay private.

## Update the record

Run these commands from this checkout, with the private checkout at `../reborn`:

```sh
npm ci
npm run import -- --from ../reborn
npm test
```

`npm run import` copies the selected files into `data/` and records their tasks in `data/provenance.json`.
A file is listed under the task that first wrote it, else the task that first used it, else its first commit.
`npm test` rebuilds the pages first. Commit the data and the generated pages together.

## Code listings

The pages follow the `jehlp-code-highlighting` skill in site-theme. highlight.js 11.12.0 highlights
scripts and JSON notes during the build. No highlighter loads in the browser. Each listing is a native
`details` element. `assets/app.js` fetches the static fragment when a reader first opens it.
Without JavaScript, the panel links to the note page or to the plain-text source in `scripts/source/`.
Script fragments are not linked, so the jehlp.net site search indexes the reasoning and notes, not the code.
