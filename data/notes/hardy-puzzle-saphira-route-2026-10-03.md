# Hardy puzzle and route to Saphira — source review, 2026-10-03

This is **hypothetical future preparation**, not observed current progress or flags. Installed19.5.43 events are authoritative; the [BigJRA Geode section](https://bigjra.github.io/reborn/#geode-badge) and [Episode19 route](https://bigjra.github.io/reborn/#labradorra-city) were checked online, but the guide identifies itself as19.5.18. Source extracts contain every page, not a presumed live selected page: `work/hardy-piano-static-739.json`, `work/hardy-saphira-static-events.json`, `work/hardy-post-calcenon-labradorra-static.json`. No UI, live save/log, navigation state or battle config was accessed or changed.

## Hardy piano: exact normal-control solution

739E23–30 are horizontally pushable tuners, initially x14. Their y coordinates, bottom to top, are45,41,37,33,22,18,14,10. After each interaction, the event assigns variables441–448 to its own current x coordinate, then subtracts14. `Interpreter.rb:907–930` confirms operand6/character0/x; this is not a push counter. Notes indexed0–7 are lowG,A,B,C,D,E,F,highG. E1i404–411 checks **[3,5,7,2,2,0,1,1]**, exactly C,E,highG,B,B,lowG,A,A.

| Tuner/event | y | Final x | Required variable | Right pushes if still x14 |
|---|---:|---:|---|---:|
|1/E23|45|17|441=3|3|
|2/E24|41|19|442=5|5|
|3/E25|37|21|443=7|7|
|4/E26|33|16|444=2|2|
|5/E27|22|16|445=2|2|
|6/E28|18|14|446=0|0|
|7/E29|14|15|447=1|1|
|8/E30|10|15|448=1|1|

Each tuner pushes only when the player faces Right or Left. `Field.rb:2899–2928` moves the event one tile and waits for movement; it does **not** move the player. For repeated normal C pushes, start immediately west of the observed tuner, faceRight, C, then stepRight into the tuner's old tile before the next C. Avoid a long uninspected key hold. For tuner6 left atx14, interact from above/below facing vertically: no push occurs, but variable446 is explicitly refreshed to0. If previous moves changed any tuner, plan from its observed x rather than blindly using the initial counts.

Defeat the three right-side trainers before queuing their corridors:739E35 Alistair[15,49], E36 Xavier[19,27], E22 Noivy[20,7]. They have sight triggers. The Isaac tutorial739E37[3,7] is optional: initial talk demonstrates the riff; the later Help branch adds an optional battle and opens the door. The ordinary tuner solution avoids needing that branch. Do not use another-save puzzle-skip state as a presumed shortcut.

After all eight values/positions match, approach739E1 RockClimb[5,45] from **[5,46], facingUp**, with a legal RockClimb user. Its forced movement net is(0,−38), ending[5,8]. It plays each string in order, checks the eight variables, and sets switch1022True only on a match. Then739E31/32[11/12,4] transfer to740[9,21]. Inspect the open door/landing before proceeding. There is a normal field/menu checkpoint in the arena before the encounter trigger.

Hardy740E3[9,18] is player-touch: stage at[9,19] and save/record the reviewed team before steppingUp. The event asks Yes/No before `pbTrainerBattle(:HARDY,"Hardy",...,true,1)`; this is doubles. Victory sets badge17 (`badges[16]`), switch658True and391=60→61, givesTM80, and raises the cap to95. The battle field is Rocky (`metatext.rb:5944`). Preserve the normal post-victory item checkpoint before changing medicine/roster. The proposed JSON template lists interaction anchors and guards; it intentionally does not claim a continuous tile route through an unobserved gym.

## Mandatory Episode19 commitments before the tournament

1. Fly to **Calcenon413**, talk to Hardy413E102[19,25] after switch658True. His story questions are readiness Yes/No, then trust Bennett Yes/No; completion sets475=1. Talk to Bennett413E118[21,28], answerYes when actually prepared; completion sets475=2. This is story entry, not an immediate unavoidable boss gauntlet.
2. Enter Labradorra414 and clear the route's Meteor trainers: Kenan414E74[63,38], DianaE75[51,26], AudreyE108[27,32], all sight triggers. After the early city scene, normal Pokémon Center access allows preparation. The cultist encounter starts from player-touch gates414E104/109/110 at[20/21/22,22], setting475=9;414E111 then autoruns. Its switch878 branch changes opponent versions and whether Amaria is a partner. Verify the actual route switch and page before approach. This is not safely described as one fixed roster.
3. PULSE Clawitzer/Zero begins in414E119 **autorun once475>=23**; it callsZEL2/Zero/0 at i206. Plan/save before the story transition that raises the value, not by attempting to walk up to the displayed Zero event[12,11]. Winning advances475 through24→25. Inspect the actual source gate and fresh flags at that future checkpoint; no current trigger coordinates are invented here.
4. The required LCCC visit is775, entered through Labradorra's southwest building774. Its battlefield is **Shortcircuit** (`metatext.rb:6210`). PULSE Mime+Sigmund is775E11[87,5], player-touch, callingMIME/Mime/0+FRIEND/Sigmund Connal/0 without an NPC partner; stage one tile before it, with normal prebattle save and party/item evidence. Winning sets475=30. Normal LCCC computer/power-door traversal needs its own observed-state route plan; the guide's Calcenon shortcut and associated pickups are optional detours. Additional Flora content is gated by variable611;414E161 autoruns only at611>=6, so it is conditional rather than a universally required boss.
5. The tournament city doors414E50/51[45/46,9] become transfers to768[41/42,31] once475>=32. The768 starting controller autoruns, sets the Pokémon Center return point, closes the exit sequence and eventually475=60. Finish preparation before entry; keep the initial story commitment separate from individual arena battle entries.

## Tournament has normal waiting rooms between its battles

The mandatory competitive battles are:

| Arena source | Fight | Field | Route condition |
|---|---|---|---|
|769E1i877|Lumi0+Eve0, withCal3 orFlorinia2 partner|Inverse|878True/Reshiram getsCal;False/Zekrom getsFlorinia|
|770E2|Cal2 **or** Florinia3|Dragon's Den forCal;Glitch forFlorinia|ReshiramCal first;ZekromFlorinia first|
|771E2|the other ofFlorinia3/Cal2|same respective fields|ReshiramFlorinia second;ZekromCal second|

Each arena controller has an autorun page and commits on entry; each successful battle exits into its waiting-room progression. This differs mechanically from Glass's same-event immediate three-round chain: **normal PCs are present** at768E67[4,53],776E67[20,53],777E21[20,53] andE67[20,79],778E23[44,12], all `pbPokeCenterPC` calls. Use normal preparation/save/team snapshots in those rooms before each arena transfer. There is no source full-heal after the two unpartnered Cal/Florinia fights; partnered Lumi/Eve uses the usual trainer-helper partner full heal. Bag and normal storage actions remain legal at the waiting-room checkpoints. Do not assume external shopping/exits remain available. Keep every failed battle in fulljourneys; reserve major-archive decisions for the settled list and actual victories.

## Saphira chest defense and badge18

After the first three tournament rounds,778E15/16[1,14/15] enters779 before completion, or780 after switch1098True. Both maps use **Dragon's Den** (`metatext.rb:6238/6246`). Talk to Saphira as the story requires, then stage beside the chest at779[26/27,43] with the whole defense+Steelix team, medicine and PP prepared. ChestE74/75 at475>=101 sets475=102; StoryControllerE76 asks the branching values questions, advances475=103, then turns1074True and starts active defense. The source explicitly suggests turning Speed-Up off for this challenge.

The defense controller779E81 progresses **26 waves**, with movement/battle parallel controllersE83/E85. FourKnight battles (Dan0,Frey0,Edgard0,Kalezis0) and multiple generated wild Pokémon occur during defense. This needs an event-aware movement/visible-threat plan, not a blind walk queue; keep close enough to intercept threats and heal/restorePP during the source-provided pauses. Wild encounters do not produce the normal trainer debug log, so exact defense consumable use needs the visible ledger plus whole challenge native pre/post reconciliation. Losing/exiting resets defense progression; require a genuinely successful full challenge. The exit handlersE1/2 reset1074/478 and impose the story penalty.

After wave26, E81 sets selfA and its next autorun page **immediately** runsSteelix/Gargantuan/version1 at i275. Treat chest defense plusGargantuan as one committed successful run; there is no guaranteed normal save/menu checkpoint just before that autorun boss. Winning transfers to780 at current coordinates and sets1098True. Only then there is a proper field preparation opportunity for Saphira. The one-use full-heal LightShard780E74[26,40] runscode314. Take/review the normal boss precheckpoint after any planned healing or roster changes, then stop at[30,12] before steppingUp into780E93[30,11], player-touch, which callsSAPHIRA/Saphira/0.

**Winning Saphira alone does not award badge18.** E93 completes the story and sets475=104. Return to chest780E91/92[26/27,43], stand directly south at[26/27,44] **facingUp**, and interact. Only this chest page sets475=105, `badges[17]=true`, switch659True and givesTM02. Save/verify the actual badge after opening it.

Dragon's Den strengthensDragon/Fire1.5, halvesWater/Ice damage, and boostsDragonDance/NobleRoar. Two ordinarySurf/MuddyWater/SparklingAria uses solidify it intoCave; SubzeroSlammer/Glaciate and certainWaterZmoves add2counter in one use (`fieldtext.rb:1850–1918`). These are source battle-planning facts, not advice to change the field blindly. Cal, the chest defense, Gargantuan and Saphira all require their own reviewed roster/field plans; the source controls when room changes and checkpoint opportunities actually occur.
