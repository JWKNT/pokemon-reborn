# Post-Hypno normal exit, recovery and Calcenon

Installed19.5.43 source review only. **Freeze the normal post-Hypno native save/status/bag and reconcile major125 before any medicine, held-item, PC or training flows.** Hypno victory sets1874True, does not heal the party, and does not advance391 to47.

`scripts/post_hypno_exit.py` implements the post-Hypno758 loop in bounded normal movement, then the recovery autoruns to Calcenon. Development/source validation and pure tests sent no inputs. It reuses ordinary capture/session guards and stops for unknown touch events, choices, battles, dialogue mismatch, coordinate/timing disagreement or capture failure. Planner flags change only after an observed approved scene has settled; these notes are never game-state writes. The two actor removals used by its route model are explicit installed animation endings: Amy25 after90A, Cal26 after92 advances39133.

```sh
python3 scripts/post_hypno_exit.py
python3 scripts/post_hypno_exit.py --execute --post-status notes/EXACT-HYPNO-POST-status.json --item-report work/EXACT-HYPNO-ITEM-REPORT.json --stop-phase zel
python3 scripts/post_hypno_exit.py --execute --post-status notes/EXACT-HYPNO-POST-status.json --item-report work/EXACT-HYPNO-ITEM-REPORT.json --from-phase shade
```

The placeholders must be replaced by the actual frozen files. The gate requires a frozen status on758, a verified one-Hypno125 item report with native inventory proof, and an exact hash binding to the supplied post-status. `status_full.rb` omits1874 from its small switch subset; a normal post-Hypno checkpoint must separately have synced1874True into the full navigation notes, and the helper checks that before UI inputs. No inventory, money, party, game save, or archive configuration is altered by this helper. It does not save or save-quit.

Expected Hypno's forced movements leave the player near **758[28,102]**; observed coordinates govern the path. The source loop crosses heartbeatE36[29,90], Terra memoryE62/63[83,18/19]→39131, E89[54,18]→39132 plus Titania90 autorun, E91[53,50] (826-dependent Taka animation/dialogue), E92[37,57]→39133, Cal/Blake touches28[34,40],99[34,33],100[34,28], E30/101[31,16/9]→39134 plus104, E102/103[17,16/9]→39135 plus105, and E107/108[19/18,63]→39136 plus Victoria31's parallel transitions through40. Every meaningful touch truncates the current movement batch; followers settle before planning the next segment.

Mandatory finishing action gates: **ZEL758E33[12,146], face from11,146 RIGHT**, then **Shade758E34[17,181], face from17,180 DOWN**. Both have animation-only source sequences and set their own self-A. Then touch **Luna758E35[40,176]**, which transfers759[40,176]. On759 the whitelisted touches at43,177/178/180/182/184/186/188/189 only change tint; E5[43,191] transfers735[18,18]. The loop's exact walk length varies with already consumed pages and actor movements; static routes are proposals, not observed receipts.

Resume phases: `zel`, `shade`, `luna`, `void-exit`, `recovery`. On a normal758/759 overworld, absent `--from-phase` selects the first applicable phase and skips source-confirmed consumed33/34. A partially completed touch/dialogue must first be inspected and settled; automatic coordinate resume does not operate inside dialogue. For a known recovery dialogue on735,715 or734, use explicit `--from-phase recovery`; it uses public installed-text/choice guards and sends no coordinate hotkey mid-scene. Stopping after `void-exit` leaves a sent transfer touch plus pending recovery, explicitly **unverified**; the later full Calcenon coordinate check is the chain completion proof.

The installed recovery is an uninterrupted chain of autoruns, **with no controllable HeartScale window on715**:

| Source | Condition and resulting transfer |
|---|---|
|735E4 page0|Initial Void return with391<47; completes39145→715[39,20].|
|715E85 page0 Radomus|Trigger3 autorun at39145; completes39146→734[18,14], facingRIGHT.|
|734E16 page0 Radomus|Trigger3 autorun at39146; completes39147→735[18,14].|
|735E7 page0|Trigger3 autorun at39147; completes39148.|
|735E4 page2|Trigger3 autorun at39148; Anna asks “you're coming too, right?” Choose **Yes** normally; completes39149→413[77,26].|

All earlier scenes have no battles or choices. The helper stops at the one reviewed Anna Yes/No, selects Yes by visible labels, resolves its tail, then verifies Calcenon coordinates. It does not guess inter-scene flags or credit a key receipt as a transfer. Installed BGM changes during the uninterrupted recovery are journaled only when their following public dialogue anchor is actually observed; no coordinate hotkey interrupts those scenes.

From Calcenon, root can use the existing ordinary helpers: optionally413E46 Shelly[61,32] (sets1023), **413E93 Eve[43,30] first page** (sets39150), then413E67[28,31]→417[11,28]. House briefing autorun is417E29 unless878True, in which case417E30; either finishes39151. Exit417E6[11,29]→413[28,32]. Do not interact with Eve again blindly: her39150 page is a four-option PULSE information menu.

Normal Pokémon Center:413E68[45,27]→415[10,10]; nurse415E4[10,4] calls the ordinary healing common event; PC415E7[14,3] runs `pbPokeCenterPC`; exit415E8[10,11]→413[45,28]. From the reviewed Arc/KG/Swamp/Mien/Cofa/Exc order, temporary Box1 slot12 **Tranquill** replaces party index1 **Klinklang** using visibly verified `pc_exchange_named.py 12 1 Tranquill Klinklang`. Keep the carrier until reaching Agate's PC752. Ordinary `fly_to.py 355` checks visited status, carrier Fly menu and destination label, and arrives at **Circus355[30,13]**. This remaining PC/Fly segment is root-owned, not included in this helper.

Static supporting event dumps: `work/posthypno-source-735-4.json`, `...715-85.json`, `...734-16.json`, `...735-7.json`, `...758-35.json`, `...759-5.json`. `python3 scripts/post_hypno_exit.py` validated all approved installed pages; syntax and three pure guard regressions passed. Source checks never loaded a native save or ongoing battle log.

`scripts/post_hypno_static_route.py` additionally replays the route model using **hypothetical**39130/1874True/17A at758[28,102], updating only RAM copies after source-approved touch effects. Both826False and `--taka`/826True branches passed:17 bounded84-tile chunks,668 total steps, then ZEL/Shade source gates and Luna. The generated `work/post-hypno-static-route-proposal*.json` files are proposals with explicit `no_observed_completion`; real runtime actor movement/coordinates remain authoritative.
