# Void route after Glass — installed 19.5.43

Read-only extraction, 2026-10-03. No gameplay, save, runtime, or navigation data was changed. This plans the mandatory route from Glass's victory transfer **754[31,12]** to PULSE Hypno **758[28,105]**. Coordinates/step counts below are static proposals; refresh observed/native state after every dialogue or touch cutscene before executing another movement queue. [BigJRA's Void section](https://bigjra.github.io/reborn/#inside-the-void) supplies narrative context; installed events take precedence.

## Preparation and route boundaries

1. Let arrival autorun **754E8** finish. It faces the player left and sets the Pokémon Center return point; it does **not** heal or move the player off31,12.
2. **Use the ordinary Light Shard754E5[17,12].** Approach16,12, face RIGHT and bump it. Event314 fully heals the six, including PP/fainted members; self-A then consumes the shard. This is the normal game event, not a scripted heal.
3. The fixed Glass six continue through the Void. No normal PC/roster replacement was found in754–759. Bag operations remain available outside conversations/battles. Teach owned **TM20 Safeguard to Arcanine**, replacing ExtremeSpeed after Glass; retain Crunch, MorningSun and Flamethrower. Refresh remaining UltraPotion/FullHeal/XSpeed/XSpDef/XAttack counts after the chain.
4. The last safe planned square is **758[28,106]**. One UP enters the boss player-touch event at28,105. Check party order/HP/moves/items and save normally before that step. The boss victory branch does **not** heal everyone; event314 is in its loss branch.

## Mandatory map/event chain

“Face” is the proposed player tile immediately beside an action NPC. Touch events activate by walking onto the listed tile. Dialogue controls must stop and resolve before resuming the route.

| Map | Target / player face | Required interaction and result | Proposed movement from previous endpoint |
|---|---|---|---:|
|754|LightShard E5[17,12] / **16,12 RIGHT**|Bump to fully heal.|31 steps from31,12|
|754|Conductor E2[14,79] / **14,78 DOWN**|Talk; no choice. Self-A removes this physical gate.|68|
|754|Ame E3, **touch58,80**|Along the route, stop for intro touchE6[16,80]. Ame cutscene transfers to**755[60,81]**.|46|
|755|Mudkip E24[62,65] / **62,64 DOWN**|ArrivalAme E5 resolves first. Mandatory route touches Victoria E11[99,94] (sets391=25). Talk to **Mudkip**, choose **Yes**. Our starter variable26=13 selects this event. Transfer to756 preserves the player's current coordinates, normally**62,64**.|179|
|756|Cain E3[100,69] / **99,69 RIGHT**|Talk; no choice. Gate disappears.|84|
|756|Julia E2[119,43] / **119,44 UP**|Talk; no choice. Gate disappears.|45|
|756|Fern E4[102,19] / **102,20 UP**|Talk; no choice. Sets391=26 and transfers to**757[102,20]**.|41|
|757|Florinia E2[132,15] / **132,16 UP**|Talk; no choice. Self-A removes gate.|74|
|757|Anna E14[163,188] / **164,188 LEFT**|Follow the long loop, resolving all touch scenes listed below. Talk to Anna; gate disappears.|342|
|757|Cain E16[139,157] / **138,157 RIGHT**|Talk; no choice. Gate disappears.|73|
|757|Kiki E17[132,107] / **132,108 UP**|Talk; no choice. Gate disappears.|57|
|757|Lin E24[121,82] / **121,81 DOWN**|On the way resolve Kiki touchE65[132,104] and Cain sceneE76[156,23]. Talk to Lin; her runtime move route sets through, fades and removes her sprite. There is no blank replacement page to infer this from.|270|
|757|Radomus E26[107,146] / **107,145 DOWN**|Talk; no choice. Long animation removes both Radomus and LunaE147[107,150], then sets switch973. Wait for completion.|78|
|757|Zina E27[120,159] / **120,158 DOWN**|Talk; no choice. Story transfers to**758[120,158]**, sets return point; no heal.|26|
|758|Pre-Hypno safe tile **28,106**|Route touches baby-voice E17[28,134]; resolve it. Stop at28,106 to prepare/save. **Do not queue the last UP automatically.**|210|

The Florinia→Anna loop crosses these meaningful automatic scenes, in order: **Corey E29[172,10]** (391→27; E3[172,9] is its alternate trigger), **Cal/Shelly E6[187,77] then E34[187,80]** (parallel animation, autorun391→28), **Blake/Cal E54[157,135] then E55[157,138]** (parallel animation, autorun391→29), and **Heather/Sigmund E13[182,169], E56[188,175], E57[178,179]** (the last has a parallel follow-up). These pauses are story activity, not a pathfinding failure. Give each its normal dialogue/animation completion and re-read coordinates. Cain touchE76 later sets391→30 and clears his associated scene actorE77; E84[156,20] is an alternate trigger.

Optional conversational branches do not block this extraction. Aya757E20 and lucidCain757E21 are beside the later loop; if speaking to lucidCain, **Yes or No both continue and both give the same286+1 affinity point** (increment occurs after the choice block). There is no mandatory choice there. The only progression choice in the extracted route is **Mudkip Yes**. The subsequent758 history branches need not all be visited to reach Hypno; the source passability route reaches the boss via the baby-voice scene.

## Hypno: scarce supplies and proposed shortcuts

Exact trainer **HYPNO/Hypno/0**, level100 PULSEPsychic/Dark/NoGuard/BigRoot; Hypnosis, DreamEater, DarkPulse, CalmMind. Starlight boosts Dark/Psychic power1.5 and makes Dark attacks also receive Fairy effectiveness. Hypno is196Speed; Arc is176 before an XSpeed,352 afterward. Safeguard prevents Hypnosis even with NoGuard (`Battle_Effects.rb` sleep/status gate).

Arc remains the practical existing-team answer: XSpeed, maintain five-turn Safeguard while awake, boost SpDef/heal as required, and use **physical Crunch**. Approximate unboosted damage76–90 means at most6 ordinary hits; oneXAttack gives150–177/3hits, two give224–264/2hits. XAttack0 before Glass is not a hard block: the six-hit plan is longer and consumes more healing/guard renewals. ThreeXSpDef gives+6; against Hypno+6SpA, ordinary DarkPulse is about109–128 into Arc+6SpDef. Observe CalmMind, critical hits and guard expiration instead of issuing blind multi-turn attack queues. A FullHeal can wake Arc before a previously selected DreamEater resolves, but the AI is not guaranteed to choose that move. All Xitems target their **own acting Pokémon**, never its ally.

- **Excadrill HornDrill is not a NoGuard shortcut:** installed OHKO accuracy code rejects a higher-level target **before** testing NoGuard (`Battle_MoveEffects.rb:3284`).90<100, so it fails.
- **PerishSong would work in principle** against this NoGuard, non-Soundproof opponent; it is not an accuracy trick. None of the fixed Glass six knows it. Boxed Kricketune50 does know it, but cannot be withdrawn inside this route. Do not assume a new team.
- **Current Cofa DestinyBond is legal but unreliable as a shortcut.** Cofa62Speed is slower than Hypno196, and unboosted Starlight DarkPulse can already KO its270HP/239SpDef before it acts. DestinyBond has ordinary priority; consecutive use alternates success/failure outside Haunted. Safeguard on Arc then switching does not guarantee a safe Cofa turn. A confirmed FocusSash could permit a different setup, but no such held-item availability is assumed. Cofa would need threeXSpeed to outrun Hypno (+4 only186; +6 is248), making its setup more costly and exposed than Arc's. Do not replace the safe Arc plan with a hoped-for Hypnosis/CalmMind turn.

## Source-only route artifacts

- `scripts/void_source_extract.rb` reads installed map files754–759 only and outputs every event page/command to`work/void-source-event-index.json`.
- `scripts/void_static_paths.py` reads already extracted`work/void-map-754.json`…`758.json` only. It has no UI/game-driver imports and no native/save/navigation access. Its main function modifies only RAM copies to represent source-confirmed gates disappearing, then prints proposed directional runs to`work/void-static-paths.json`.
- These snapshots use hypothetical future story flags and reset actor positions; they are **not fresh observed state**. Long runs are planning aids. The controlling agent should split them at`touch_stops`, allow native story scripts to resolve, then use current observed coordinates/event pages for the next queue.

## Guarded normal-control batch helper

`scripts/void_batch_route.py` now implements all15 mandatory phases, using current observed coordinates and active installed event pages rather than replaying the static runs. **Syntax/source boundaries checked only; it has not been run against the UI.** It defaults to56-tile chunks, ends each chunk at the first meaningful touch, resolves only approved installed scenes, and refuses an unknown touch/choice/battle/capture failure. The boss tile28,105 is always blocked in its planning model. Existing `play.act` capture and session-limit guards remain in force.

For a cautious first live segment, run `python3 scripts/void_batch_route.py --stop-phase ame`; it consumes the ordinary shard, verifies the normal heal with one native checkpoint, teaches Arc Safeguard over its verified ExtremeSpeed slot, then stops on755. Running without a stop flag continues to758[28,106], verifies/saves the safe approach, and leaves Hypno unstarted. It does **not** save-quit or start archive entries; those remain the controlling agent's responsibility.

Actual14:03 frozen Hypno readiness has Safeguard **8/25 PP, PP-Up0**: normal machine teaching preserves `min(old currentPP,new totalPP)`, so the previously healed ExtremeSpeed8 becomes Safeguard8. Every other move is fullPP. The final-only readiness verifier now allows exactly this source-backed Arc90 slot/order while retaining strict LightShard/fullPP checks; it records the partial8/25 honestly. Eight casts suffice for the short reviewed Hypno plan. See `notes/hypno-tm-pp-carryover-2026-10-03.md`; do not replay the route or spend recovery items just to satisfy the old blanket fullPP assertion.

Resume supports `--from-phase` names: `shard`, `conductor`, `ame`, `mudkip`, `cain-first`, `julia`, `fern`, `florinia`, `anna`, `cain-second`, `kiki`, `lin`, `radomus`, `zina`, `hypno-approach`. Without that flag it chooses the first phase on the observed current map and skips source-confirmed completed gates. Noninitial-map/position resume takes one normal checkpoint to refresh true event conditions first. It refuses to skip the mandatory shard if its consumed self-switch is absent. Lin's end-of-scene self-A governs the planner-only removal of her runtime-faded sprite, including removing a stale override after an earlier save was restored. Resume requires an actual **overworld**, with pending dialogue/menus resolved first; it never guesses its way through a partially completed cutscene.

Completion receipts go to`work/void-batch-progress.json`; only completed, source-confirmed scene effects are mirrored into navigation notes. No receipt is treated as game-state proof. If a chunk stops early, inspect the actual screen and resume from the appropriate phase after settling its known scene; do not assume all queued inputs completed.

An optional source754E14 prompt, “Skip cutscenes on this file?”, can be unlocked by another file through global`voidskip`. The helper does not activate that event. If the exact prompt is already open at startup, it chooses **No** using verified labels so the full story stays recorded. Other unexpected choices stop the run. Source-anchored BGM changes are logged through the existing dialogue helper where those events contain music commands.

After victory, continue the story normally: Luna758E35[40,176] transfers to759[40,176], and759E5[43,191] exits to735[18,18]. Hypno is the next eligible major archive entry after the three Glass rounds; no Void conversation belongs in the major-fights compilation.
