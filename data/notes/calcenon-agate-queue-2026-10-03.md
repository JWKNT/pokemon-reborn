# Calcenon prep queue after Hypno

Source-only development; no game/recorder input, live native/runtime read or save edit was executed. New helper: `scripts/calcenon_agate_queue.py`, dry-run by default. Installed events were exported to `work/calcenon-agate-prep-source.json`; default validation re-reads only those installed event assets, not native state. Python syntax, exact transfers and page-selection fixtures passed.

Independent source-only sibling review found no blocking route/control guard issue. It caught a title-normalization typo in both first-dialogue anchors: the lowercased screen now removes lowercased `pokemon reborn`, allowing short Hardy lines to match despite the window title. Recompiled without controls.

## Approved sequence and boundaries

1. At the actually observed post-recovery Calcenon413[77,26], completed planning39149: Shelly413E46 page0 is optional for the quest (sets1023 only), but included by default for the story. `--skip-shelly` omits it. Eve413E93 **page0 only** sets39150. Do not replay Eve: page1 is the four-way PULSE information menu. Then413E67 enters417[11,28] and immediately starts417E29p0 when878false, orE30p1 when878true. The queue requires a visible installed house line before advancing the autorun. Both branches have no choice/battle and finish39151,988/989true. Exit417E6→413[28,32]. Planning effects are reflected only after observed completion, apart from the house entrance503 effect which is reflected after its installed house dialogue is positively seen.
2. Center413E68→415[10,10], nurse415E4/common1: choose **Yes** by visible labels, then normal healing. PC415E7 opens afresh, requires **Box1**; exchange Box1slot12 **Tranquill** for party index1 **Klinklang**. Source `Storage.rb:1942` resets the fresh box cursor to0. Existing `pc_exchange_named.py` verifies both incoming and outgoing names; the new wrapper then verifies all six party cards at their expected positions, opens Tranquill's ordinary menu and verifies its Fly option. No HM/moves are taught. Exit415E8→413[45,28].
3. Ordinary approach413E21→418[17,7]→418E2→412[12,18]. Use one owned SuperRepel normally; existing route helpers renew only on visible expiry. Climbs:412E1→710[23,49];710E2→711[20,58];711E3→713[17,24]; **layer_walk713→48,36 using observed410**;713E5→714[17,10];714E3→715[65,17]. Every transfer is checked at its exact observed endpoint. Stop there. This repeats the successful resupply climb prefix; it calls none of the obsolete Glass story sections, and never visits already-collected710E64.

The runner conservatively rejects any still-active automatic trainer/boss page on each approach map, before movement. A remote unbeaten trainer can therefore stop a safe-looking queue: inspect/review a narrower route manually, rather than suppressing the guard. Unexpected battles, choices, dialogue, ambiguous party cards, missing Fly, coordinate disagreement or helper failures stop without further queued actions.

## Commands for root (not executed during development)

Print the installed-source proposal:

```sh
python3 scripts/calcenon_agate_queue.py
```

Once root has verified that its frozen post-Hypno party evidence is still unchanged (six members, Arcanine90 lead, Klinklang party1, Swampert Surf/RockClimb, at least3 owned SuperRepels), execute the whole queue while recording:

```sh
python3 scripts/calcenon_agate_queue.py --execute --party-status notes/ACTUAL-FROZEN-POST-HYPNO-status.json --journal work/calcenon-agate-queue-run1.json
```

The frozen party file may predate the recovery cutscenes: it supplies unchanged party/bag evidence, not a claim that Calcenon coordinates were saved there. Each movement phase independently reads the rendered overworld/coordinates and completed planning391. Root must not reuse that old party file after changing party, moves or spending its prerequisite Repels. The helper inserts **no save/checkpoint**; take one meaningful native checkpoint after the completed briefing/prep if useful.

Separate phase runs use `--phase briefing`, `--phase carrier` or `--phase approach`. `--stop-phase briefing`/`carrier` ends an automatic chain there. Standalone `approach` requires freshly verified carrier party evidence (Tranquill1 knows Fly, healthy full-HP90 lead, Swampert Surf/RockClimb,3Repels). The optional `--climb-index N` starts at the source map of climbN (0=412,1=710,2=711,3=713,4=714); it sends no initial Repel and is appropriate only after root reviews the interrupted route and confirms active Repel. Any run requires a **new journal**, while preserving the previous failure/pending receipt. No automatic journal replay/resume is permitted.

For the new Scale, follow `notes/heartscale-normal-route-2026-10-03.md`:715dry layer→50,23; normal Surf boarding→50,24; Down→50,25 proves410true; surface route→57,21; faceUP for715E64. This helper intentionally stops before those actions.

After the Scale is actually collected and a fresh normal checkpoint proves Tranquill1/Fly, HeartScale≥1 and **dry715[57,21]**, the optional separate leg is:

```sh
python3 scripts/calcenon_agate_queue.py --phase fly-circus --execute --party-status notes/ACTUAL-POST-SCALE-status.json --journal work/calcenon-circus-fly-run1.json
```

That leg calls existing `fly_to355`, which checks actual outdoor map metadata, owned carrier menu, already visited Fly destination and exact Circus arrival. It cannot Fly from the indoor center, the brief recovery autorun or the water dock. Root's Circus purchases/build/training remain in the separate reviewed Agate prep phase script. No Agate fight is started here.
