# Agate south entry and ordinary Ricardo fight — source proposal

Source-only, not executed. Installed19.5.43 declarations/maps take precedence over the [BigJRA raid route](https://bigjra.github.io/reborn/#the-raid-on-agate-city), which explicitly recommends Vanhanen Labyrinth → Agate's south entry. Root retains ownership of actual public controls/checkpoints. No active battle data or AI predictions used.

## Travel, keeping Tranquill

Current intended condition is391=51,988/989=True. Keep the conscious Fly carrier until after Ricardo. The normal Vanhanen Labyrinth/Vanhanen Castle Fly point is **292[16,16]**, region0 cursor[12,9].

Reviewed ordinary queue (existing helpers; root executes only after public guards):

```sh
python3 scripts/fly_to.py 292
python3 scripts/connected_walk.py 292 291 48 0
python3 scripts/connected_walk.py 291 297 25 13
python3 scripts/eventq.py 297 1
python3 scripts/q.py 298,8,2
python3 scripts/eventq.py 298 8
```

Static route proof: `work/agate-south-travel-proposal.json`, full installed map extracts `work/agate-south-travel-static.json`. The chosen boundary geometry is292[33,0]UP→291[47,49],291[48,0]UP→297[24,22],297E1[25,12]→298[8,13],298E8p2/988True[8,1]→763[36,85]. Reviewed walking totals121+54+10+11 keys. Maze292 only touches E27/E3 (switch96 off; E3 may run ordinary dismount common32); no dialogue or battle. Route291 remainsx46–48, outside active trainer26[37,19]DOWN6. Ordinary Repel can cover grass; an unexpected wild battle/dialogue ends the current walking batch and must be resolved before resume.

Both alternatives are blocked *before* any trainer at39151: Fly763[46,70] is an allied NPC enclosure; Circus west arrival763[13,54] is enclosed by BishopE41[22,72]/AllyssaE42[22,73], the only passable eastern boundary openings. Their dialogue lists are empty; their blank pages require391>=52. Therefore no optional Christopher fight is necessary for this southern route.

## Ricardo approach and story guard

From south763[36,85], the reviewed26-key prefix to[32,63] is:

`left up up up left up up up up left up up up left up up up up up up up up up up up up`

Proof `work/ricardo-safe-route-36.json`. Stop there to prepare lead, HP and weather. One **UP** reaches[32,62], normal stage52 setterE84 and RicardoE48's left-facing Trainer(3) sightline. This is an ordinary street fight, **not** the two-battle Agate chain. Do not blindly queue further keys. On public victory, Ricardo selfA=True; verify39152 outside battle. At52 the allied barricades disappear; normal Agate PC752 can now exchange Tranquill for Cryogonal/borrow Sash, arrange/heal the fixed final six. Do not cross763x43–48,y52 until whole-chain preparation and archive entry are ready (that commits39153 and the warmup→Solaris chain).

## Ricardo actual team and weather

Installed trainertext10312: Ricardo/MeteorAceM1; defaults Hardy,10IV/85EV each, no held items or trainer medicines. NoField; map763 Outdoor/MapPosition[0,13,6] selects **Carnelia weather region4**. Game_Screen.rb318/349 chooses regional weather on outdoor entry; leaving a PC does not force clear weather. Field.rb1122 maps outdoor Snow/Blizzard to permanent Hail. Swamp hail chip18; Cofa chip15. Use the fresh outside-battle checkpoint `weather` export plus public fight weather before selecting the plan.

| Foe | Level | Ability | HP / Def / SpD / Speed | Moves |
|---|---:|---|---|---|
| Slurpuff |86|Unburden|263 /179 /160 /155|PlayRough, Wish, StickyWeb, Surf|
| Minior, full-HP Meteor7 |86|ShieldsDown|225 /203 /203 /134|CosmicPower, RockSlide, ConfuseRay, Bulldoze|
| Scolipede |87|SpeedBoost|228 /186 /152 /226|Megahorn, RockSlide, SwordsDance, PoisonJab|
| Aggron |88|RockHead|248 /349 /137 /120|IronHead, HeadSmash, Earthquake, Curse|
| Blaziken |88|SpeedBoost|266 /155 /155 /173|HighJumpKick, FlareBlitz, BraveBird, RockSlide|

Battler.rb1489/2355 makes full-HP Minior Meteor7 on activation; its declared YellowCore5 is restored at<=halfHP (coreSpeed238). Battle.rb6127 requires turncount>0 for SpeedBoost, so a fresh Scolipede/Blaziken replacement has no entry boost.

**Clear/rain/sand:** lead full295HP Swamp/WaveIncense. Use selfXSpeed, then selfXAttack, inspect public stages, then Waterfall all five while staying active. Speed290 beats initial Scoli226/Blaz173. At actual Attack>=+2, Waterfall floors277/487/266/286/638 against the five HP totals. Two maximum rainy Surf crits144 each leave7HP; clear PlayRough crit133 twice leaves29. Ground typing prevents sand chip. **Any public Attackfell changes this proof:** heal/restore Attack>=+2 before attack, without inferring hidden enemy intentions. One-XAttack-only is not recommended: later faster Scoli/Blaziken crits can overwhelm the remaining HP. Do not use this same damage plan in sun (water weakened) or hail (setup chip can kill).

**Hail/sun:** take PowerLens off Cofa normally before entering Ricardo; otherwise its battleSpeed is halved. Require the completed normal Timid build252HP/333Def/210SpA/218SpD/68Spe and Hex present. Use three selfXSPECIAL and three selfXSPEED, with public HP guards between every action. At+6/+6, SpA840/Speed272. Slurp has no damaging status move; PlayRough Attack drops do not affect this special plan. Wish and StickyWeb do not prevent a sweep while Cofa stays active. Hail worst Slurp crit PlayRough77 +15chip=92: **>=93HP before every setup item**; Ultra200 safely restores enough even from1HP. Sun has no chip; conservative same93 guard is fine. Before first Hex, **>=76HP** covers five hail ticks75. Unstatus Hex floors333/263/351/388/343, guaranteeing every foe's KO before it acts. Do not switch or waste turns after starting this sweep. Rain Cofa fallback uses>=123HP because rainy Surf crit122; prefer the short Swamp plan there. Sand raises rock SpD, so the stated Cofa Minior KO does not apply; use Swamp.

Heal/reset party normally after this ordinary victory, take the required Agate PC exchange, then freeze the real final six/stock before opening the curated Solaris126 shared-chain attempt.
