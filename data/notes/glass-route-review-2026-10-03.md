# Glass route review — 2026-10-03

Read-only research of installed 19.5 map events, native `Glass-10AM-paused` evidence, and [BigJRA’s Glass walkthrough](https://bigjra.github.io/reborn/#glass-workstation). No game input or save/game/runtime edits were made by this reviewer. Live observations and subsequent native checkpoints supersede this planning document.

## Rescue and carry Espeon

Native pause: player732[37,28],410=True; Espeon36,19,965=True,947=False; Glaceon27,33,964=False,946=False. E65 requires **410=False when965=True**;965=False instead requires410=True. Approach Espeon from35,19False and faceRight/C. Successful rejoin zeros406/407 and sets947=True.

The layered route from37,28True is Left twice, then Up nine times to35,19False. This ladder ascent is harmless while neither companion follows. **Do not take this ladder down after rejoining Espeon:**73219[35,20] and73221[35,22] explicitly remove the following dependency and set947/946False. The generic eleven-step route to37,28 (Down9,Right2) crosses both events and causes the former false pallet-success report.

Carry Espeon Left29 from35,19False to6,19False; enter73270[6,18] to733[3,43]. SelectB2F at73366[1,39], then exit73367[3,44] to732[6,24]410True. The lift updates965=False **only if947True**, preserving a waiting companion’s layer. Use live route guards for timing/drift.

## Reopen the northern corridor and retain access to Glaceon

The pivotal geometric correction is **GB1 DOWN (core97)→408=1**. Native408=0 has its top blockers at21/22,28–30, preventing a carry route from6,24 to the safe left face of GB10. A read-only hypothetical408=1 opens a55-step route from6,24True to37,28True, without the companion-dropping ladder. The old assumption that GB1 should remainUP throughout was wrong.

Glaceon27,33 becomes isolated on the south side when GB1 isDOWN. Prefer moving Glaceon to the western corridor **before** this push: leave Espeon near17,31 using its actualWait menu; fetchGlaceon27,33; bring it back near the waiting Espeon, then swap back toEspeon so Glaceon waits on a clear western tile, such as18,31. Confirm actual follower placement in footage/native save.18,31 is outside the common-event forbidden box ranges. With4081,4172,4191 andGlaceon18,31, read-only routes from37,28 reach its adjacent17,31 in23steps and the upper-left lava’s lower stair35,15 in24steps. These routes still require live confirmation.

Then push **GB10 RIGHT (147 or146)→417=2**, provided416=1. Safe observed target is37,28, facingRight toward150[38,28]. Espeon must actually be following; stationary player coordinates alone prove nothing. The repaired helper checks the expected pallet variable after a normal native quicksave.

Push **GB12 RIGHT (157)→419=1** while418=0. A short route from37,28 after4172 reaches41,26, facingUp to core157[41,25]. This opens the upper-left path.

## Upper puzzle, with corrected directions

FetchGlaceon from the accessible western placement; take it to35,15 and trigger73284[35,14] forFrostBreath→402=60.73283[35,13] is the counterpart from the upper side. The5XL item is73295[36,12]; sourceLightShard73262[34,12] is nearby. Use the normal native healing effect if encountered, but still verify full party HP/status/PP before the gauntlet.

LeaveGlaceon **41,22**, as in the first guide image, and bringEspeon to41,23 beneath it. Important installed-source sequence:

1. **GB12 LEFT**,4191→0. From41,23, one stepRight to42,23 and faceDown toward160[42,24] is a safe left-push face; other equally safe faces exist.
2. **GB11 DOWN**,4180→1. This is **DOWN, notUP**. From43,23 faceRight toward154[44,23]. Source blocks thisDown motion while419=1, so step1 must precede it. UP only restores4181→0.
3. **GB12 RIGHT**,4190→2 while418=1. Source selects4192 rather than4191 when4181. A safe northern face is161[41,24], from41,23 facingDown. Verify actual geometry after each operation.

TakeEspeon around the cleared eastern side and leave it **43,15**, immediately right of the lower staircase42,15. This follows the second guide image: old42,14 was a mistaken sprite-coordinate reading and lies on unfrozen lava. A possible way to place it is walk43,15 then43,16, faceUp/C andWait when the follower is visually at43,15. Do not repeat a long held turn that exchanges player/follower positions.

Fetch Glaceon41,22; approach the upper-right lava from42,15, faceUp to73285[42,14]→403=60.73286[42,13] is the upper counterpart. **Do not leave Blue at42,16 or43,16:** either placement blocks the only southern exit, making the eventual scanner return impossible until Blue is moved.

Prefer parking Blue in the upper alcove **43,11** before rejoining Espeon43,15. After freezing from42,15, carry Blue Up4 to42,11, Right to43,11, then Left to42,11. FaceRight/C and choose its actual Wait menu when Blue is43,11. This tile is outside the forbidden Wait rectangles, and it does not obstruct the main bridge at42,12. Return Down4 to42,15 and faceRight/C to join waiting Espeon43,15. Verify actual coordinates after the Wait operation; hypothetical geometry cannot prove live follower placement.

At the upper pallets, the accessible order from the right bridge is **GB14 RIGHT (170)→421=1 first**, then **GB13 LEFT (165)→420=1**. With4200/4210, the installed model has no accessible legal GB13Left face, while GB14Right is accessible from42,11 facingUp toward171[42,10]. Moving GB14 exposes the GB13 interaction. Reach732174[40,8] andC: native MeteorCard possession leads to **958=True**. The scanner itself does not start the gauntlet.

## Proven hypothetical scanner return

With Blue43,11, following Espeon, frozen402/403=60, and4201/4211:

1. From scanner stand40,9, reach43,23 in21 route actions; faceDown toward163[43,24] and push **GB12 LEFT→4190**.
2. Down2 to43,25, faceRight toward155[44,25], and push **GB11 UP→4180**.
3. Up2, Left to42,23, faceDown toward163[42,24], and push **GB12 RIGHT→4191**. This restores access to the left bridge.
4. The model now reaches35,10 in24 actions via the frozen left bridge; faceRight toward167[36,10], and push **GB13 RIGHT→4202**.4211 is required for this branch. A right push from the eastern side facingLeft is explicitly blocked.
5. From35,10, Right, Up, Right2 reaches safe door standby38,9. Both38,8 and39,8 remain forbidden in the helper, so this route cannot enter the gauntlet.

All segments above were checked against the installed map/controller using explicit hypothetical state, not executed by this reviewer. Recompute after each native observation. If402 is actually0, the western return route is absent; a new freeze is needed. Installed map732 source contains only the freeze writes402/403=60, with no local countdown found, so60 should not be described as a confirmed expiring timer.

## Standalone planner

`scripts/glass_upper_route_plan.py` accepts an explicit snapshot, start coordinate/layer, optional stage and waiting-companion overrides, and returns layered route steps to safe interaction faces. It never sends input, quicksaves, extracts native state, or writes shared navigation. It reads installed map data and native saved progress, with explicit snapshot keys taking precedence. The generic navigation lookup is redirected to a temporary planning-only JSON that is deleted on completion.

Example query:

```sh
python3 scripts/glass_upper_route_plan.py \
  --state notes/Glass-10AM-paused-navigation.json --stage scanner-return \
  --from 40 9 true --following espeon --glaceon 43 11 --query GB12Left
```

Use `--stage current` with a current observed snapshot for live planning. Stage presets are hypotheses, not success claims. `--var 419=0 --var 418=0` supplies a proposed pallet state without writing it anywhere. `--goal 38 9 true` plans standby; a gauntlet-door goal returns null. Seven read-only regression probes passed: layer rescue, follower-drop avoidance, western Blue access, upper pallet order, scanner return, GB13 west-face access, and safe door standby.

## Authoritative branch table

|Core|Current state|Direction|Result and gate|
|---|---:|---|---|
|97GB1|4080|Down|4081; opens northern corridor|
|97GB1|4081|Up|4080|
|140GB9|4161|Up|4160, unless4172|
|146/147GB10|4171|Right|4172 if4161; otherwise4170|
|153GB11|4180|Down|4181 unless4191|
|153GB11|4181|Up|4180|
|157GB12|4190|Right|4192 if4181; otherwise4191|
|157GB12|4191/2|Left|4190|
|165GB13|4200/2|Left|4201|
|165GB13|4200/1|Right|4202 if4211; otherwise4200|
|170GB14|4210|Right|4211|
|170GB14|4211|Left|4210|

For any desired push, the player must not face opposite that direction:Right forbids facingLeft;Left forbidsRight;Down forbidsUp;Up forbidsDown. C opens the purple directional prompt only if947True. The arrow is a puzzle selection, not ordinary walking.

## Door boundary

73274/75[38/39,8] transfer directly to734[18,24] and remove companions.73412 has an unconditional initial autorun; its391>=46 page is the **post-gauntlet** inactive page.39123 is valid before entering. **Do not step into eitherdoor before healing, selecting the fixedsix and leading pair, taking battle-entry metadata, and committing to all three consecutive fights.**958 should beTrue and1040False at first entry.

Guide images inspected: `work/guide-glass-glaceon.jpg` and `work/guide-glass-espeon.png`. Current source: `work/story-map-732-events.json`, `work/story-map-733-events.json`, `work/story-map-734-events.json`; native pause notes: `notes/Glass-10AM-paused-status.json` and companion navigation snapshot. Read-only geometry experiments used hypothetical planning objects only and were never copied into game/save state.
