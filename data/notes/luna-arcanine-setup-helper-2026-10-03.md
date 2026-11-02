# Luna round-2 guarded setup queue

`scripts/luna_arcanine_setup.py` queues only the reviewed Arcanine setup. Run
once at the **first command menu**, with **Lv90 Arcanine versus Lv83 Weavile**,
before any manually used X items. Recording must already be healthy, and the
root controller must be the only game-input owner.

```sh
python3 scripts/luna_arcanine_setup.py --journal notes/luna-arcanine-setup-attempt-N.json
```

Replace `N` with the actual new whole-gauntlet attempt. Do not reuse a journal
or restart the eight-item queue in the middle of an already prepared battle.
The helper deliberately refuses an existing journal. If actual visible maximum
HP changed after round 1 EV gain, pass that observed number with
`--expected-max-hp 295` (default 294). This option does not read native saves.

One narrowly bounded exception is `--resume-initial-guard`: it can reuse an
existing journal **only** when no initial state was accepted, no item action
was recorded, no item is pending and the run is not complete. It preserves
the earlier stop reason/time in `initial_guard_stop_history`. This retries
the same untouched first command after an OCR correction, without claiming
a new attempt. It refuses any possibly advanced battle. The level parser
normalizes diacritics and o/q→0 only inside an explicit Lv/Lu numeric token;
it accepts the observed `Lụ9o` as Lv90 and still rejects other levels.

The fixed setup is X Defend → X Speed → X Defend → two X Sp.Def → three X
Sp.Atk. All X items target the active Arcanine through `--active`; potions and
Full Heal use the ordinary party target selector. Before each action the
helper requires two stable rendered-UI checks of the command prompt, both HUD
names and exact levels, numeric current/maximum HP, the visible HP gauge and
the status badge. It inserts an Ultra Potion when HP is below 180, then a Full
Heal for poison only once HP is at least 180. Paralysis, sleep, burn, frozen
status, an unreadable badge, an unfamiliar actor/foe or ambiguous HP stops the
queue before another item. Immediate re-poisoning after a cure also stops it.

The status check uses the **installed static graphic assets**, compared with
the rendered HUD, rather than treating missing PSN OCR as healthy. Source
geometry is `PBScene.rb` and `PokemonDataBox.refresh/update` in
`Battle_Scene.rb`: player badge at (326,228), HP gauge at (404,232), with the
selected HUD's legitimate two-pixel vertical bob considered. **Native screenshot
pixels differ from ScreenCaptureKit points.** Inspection of the existing
`work/state-native.png` (no new capture) calibrated its 2272×1816 shadowed retina
image to game canvas **`112,132,2048,1536`**. Its window starts at y76, the
title bar is 56 pixels high, and the game starts at y132. This is the automatic
preset for that exact image size; 1024×796 unshadowed captures use
`0,28,1024,768`. Any other size stops before input and requires a verified
`--canvas left,top,width,height` rather than loosening HP/status guards.

Each action is written as `pending` **before** input. Successful setup steps
require the **rendered boost panel** to match the exact expected stage sprites
before and after the item. `statdis1.png`/`statdis2.png` are composed in the
installed draw order at game coordinates246,188, considering both legal bob
positions. The expected value must beat every alternate legal−6…+6 value for
each of the seven stats, so a small unchanged icon cannot pass a loose overall
image threshold. Initial zero stages are also required. Visible stat-rise
messages from `recordings/screens.jsonl` are recorded when available; battle
turbo may legitimately complete them before the next screenshot.

For Ultra Potion, either the actual visible restored-HP message or a stable
numeric/bar-proved HP increase is required. There is no passive HP recovery
for this Charcoal Arcanine against Weavile's four damaging moves. If a critical
hit makes post-potion HP no higher than before and the effect text was missed,
the helper leaves that item pending for manual review. For Full Heal, either
effect text or a template-proved poison→healthy badge transition is required.
All of this is public rendered-UI evidence, not a battle log, live AI, runtime,
RNG or save inspection. A timeout or other uncertainty also leaves the pending
entry; never replay it blindly. The script has no resume facility because a
partially executed item cannot safely be assumed unused.

Defaults allow at most 22 total item actions, eight Ultra Potions and six Full
Heals. After the eight proved setup actions it restores the same HP/status
safety floor if needed, then stops at the command menu **before attacking**.
The journal reports the proved intended stages: Defense +4, Speed +2,
Sp.Def +4, Sp.Atk +6. It never imports legacy top-level battle scripts; only
`play.py` is imported and the reviewed, bounded item/readiness helpers are
invoked as subprocesses. All game input still goes through the recording and
session-limit guards in `play.act` and `scripts/key`.

Validation performed: Python syntax compilation only. **No helper execution,
game input, live screenshot capture or native save modification was performed
during development.** The first live invocation can stop conservatively on
OCR, template or geometry differences and should be supervised by the root
controller. No attacking helper is referenced or called.
