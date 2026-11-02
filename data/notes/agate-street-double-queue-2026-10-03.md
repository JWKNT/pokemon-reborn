# Bounded ordinary Lyla/Ezra helper

`scripts/agate_street_double_queue.py` defaults to a pure source proposal. Only explicit `--execute --reviewed-midbattle` enables public screen reads and normal controls. Root separately owns the opener, actual Ditto transformation and choosing safe HP thresholds. Five pure/source fixtures pass; no game controls were sent during development.

An explicit JSON list has1–16 selections (at most8 double turns), with actor, min_hp, two exact foes, and either move_slot or item. Targeted attacks also name physical enemy target1/3 and target_foe. Actor/move/totalHP come from an explicitly supplied frozen outside-battle six-party status; currentHP comes only from normal current-actor own Q inspection. Every action checks fresh exact current prompt/actor/foes/menu, actual numericHP, capturePID/restart stability. A new status/field/weather/TrickRoom, faint, transformation, foe change, unexpected next actor, capture gap/restart, ambiguity or no-effect stops the queue with pending journal preserved. No native/battle logs, foe inspection, RNG, auto-switch or inferred stages/consumption. Owned child process groups terminate on timeout/cancellation; no replay.

Example currently requested one WideGuard selection is `work/agate-street-mien-wideguard-proposal.json`. Its min_hp1 only proves living actor; root must choose a tactical threshold from the observed situation. Provide the actual frozen outside roster and a NEW output folder. The helper stops after a knockout rather than guessing replacement foes. A stopped helper may leave a normal own-inspection/menu open; inspect/cancel normally before another worker.

General root-selected policy: IceBeam for most targets, FreezeDry for Mantine; Recover if observed CryoHP and incoming damage make that turn safe. At most one additional XSpAtk per plan, only after both Noivern/Ditto are absent. Mienshao FakeOut is excluded because it belongs to the separate turn1 opener; use root-reviewed WideGuard against spreads or explicit BrickBreak into copiedCryo/screens and appropriate HJK only with actual risk reviewed. Arcanine's Flamethrower handles copiedCryo/Grass/Fairy; do not presume Crunch is its best Mantine coverage. Swamp/Exc switches and reviving reserves remain manual. Earthquake/Surf/RockSlide require explicit reviewed_spread=true because partner safety is not inferred. Moves are always root-selected, not automated policy.

```sh
python3 scripts/agate_street_double_queue.py --plan work/agate-street-mien-wideguard-proposal.json --roster notes/Agate-final-six-south-ready130-status.json
# Root only, after actual opener/menu/HP review; replace roster with the real latest frozen staging snapshot and choose a fresh folder:
python3 scripts/agate_street_double_queue.py --plan work/agate-street-mien-wideguard-proposal.json --roster notes/Agate-final-six-south-ready130-status.json --output work/agate-street-NEW --reviewed-midbattle --execute
```
