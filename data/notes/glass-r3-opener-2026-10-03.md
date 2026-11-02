# Glass round 3 opener — short plans and rendered-UI preflight

The existing `glass_turn.py` can run the three short JSON plans in `work/`.
`glass_r3_preflight.py` **does not send any keys**: it captures/reads the ordinary
rendered menu, checks the named actor, exact allied Lv90 HUDs and both initial
opposing Lv81 slots, checks healthy status templates and stable HP-bar intervals,
then prints the appropriate plan path. Development validation was syntax only;
neither script/plan was executed against the game.

Run the preflight before each turn, then execute only that one plan through the
existing recorded controls. There is no three-turn blind queue:

```sh
python3 scripts/glass_r3_preflight.py --phase t1
python3 scripts/glass_turn.py work/glass-r3-opener-t1.json
```

Turn 1 requires full HP: Arc self-XSpeed, KG self-XSp.Def. Turn 2 requires Arc
at least140HP and KG at least130HP by the conservative gauge interval: Arc
Flamethrower Ninetales slot3, KG Shift Gear. Turn 3's supplied plan is specifically
the **Ninetales still alive** branch: Arc Ultra Potion KG, KG Gear Grind Nine3.
The preflight refuses the turn if Nine already fainted/replaced. It always stops
for poison/paralysis/other status, a KO, an unfamiliar actor/foe, an uncalibrated
canvas or animating HP. Doubles show no numeric HP by default, so the report
gives intervals from the installed96-pixel gauge, assuming Arc294/KG275 maxima.
If actual maxima changed, supply the observed `--arc-max-hp`/`--kg-max-hp`.

The HP safety thresholds follow the reviewed ordinary branches: Nine using
Veil on turn1 leaves KG enough HP for a second attacking turn; Nine attacking
on turn1 instead leaves KG around135 minimum and gets KOed by fast Flame on
turn2 without Veil. Both reviewed branches leave KG at least20 after turn2.
Clef's critical Fire Blast bypasses positive Sp.Def and can KO KG; a source
damage bound is not permission to continue after an actual knockout/status.
The preflight verifies pixels rather than relying on a stage sprite proof:
the Luna initial stage template had a semitransparent zero-stage backing and
the parent switched to normal manual setup. This R3 helper does not use it.

If Nine is replaced by **Alolan Sandslash**, review the actual pair before turn3.
Arc+2Speed352 beats Slush Rush350; fast Flame is4× effective. If KG is in immediate
danger, Arc's Ultra Potion can rescue it before KG attacks Clef, but evaluate
whether leaving Sand alive risks Knock Off/flinch/spread Rock Slide. No supplied
plan blindly accepts that replacement. Healthy status and boosted speed remain
prerequisites; paralysis invalidates the speed comparison.

After the leads, KG self-XDefend and self-XAccuracy consume its own action;
Arc handles healing/urgent Fire targets. Wide Lens Gear Grind remains93% until
accuracy is boosted. Prioritize Sand, Clef's Fire Blast/Thunder Wave, seed-focused
Jynx and threats entering before a safe setup window. Use Flame for Bisharp,
Bronzong and Metagross; avoid re-entering Intimidate against Defiant Bisharp.
Alakazam's Psychic Terrain removes Factory assumptions, and Froslass Destiny
Bond requires observation before an attack. Stop the short opener plans at
the first replacement and handle those branches using the existing battle tools.

The JSON plans have no HP/status/stage checks internally beyond `glass_turn`'s
actor/foe/menu guards. The separate preflight and actual visible turn result
are required. All X items use self targets; ordinary potions use the legal
named party target. No changes to live input helpers, game source or saves
were made by this subagent.
