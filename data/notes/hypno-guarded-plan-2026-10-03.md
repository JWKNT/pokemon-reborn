# PULSE Hypno: short Arcanine plan and visible-turn guard

Static review of installed Reborn19.5.43, 2026-10-03. This is a proposed future battle, not a victory or current battle-state claim. No live controls, save edits, active battle logs, AI data, or RNG were used. Frozen build/stock evidence is `Glass-post-gauntlet-attempt-1-status.json`; fresh normal healing, TM teaching and lead ordering must happen before entry.

## Recommended practical sequence

Keep the Glass six. Heal at754E5 LightShard; teach ownedTM20 Safeguard to Arcanine over ExtremeSpeed normally; put Arc first; take the planned outside-battle checkpoint. Approach758[28,106] and inspect before stepping north onto Hypno's758E122[28,105]. Frozen Arc is90,294HP,228Atk,171SpD,176Spe, Intimidate, Charcoal; Hypno is100,381HP,479Def,603SpD,287SpA,196Spe, NoGuard, BigRoot, Psychic/Dark, Starlight. Hypnosis/DreamEater/DarkPulse/CalmMind only. Charcoal is immaterial to Crunch.

1. **T1 XSpeed**, a priority bag action. Arc reaches352Spe. Hypno can still use Hypnosis after the item; do not begin with a slow Safeguard.
2. If asleep, **FullHeal immediately**. An item happens before Hypno's move. Observe actual cure, opposing action and HP, then count that completed turn. Do not attempt Safeguard while asleep or assume sleep wears off.
3. While awake and faster, **Safeguard when inactive**. If current HP falls below the reviewed survival margin, heal first and observe the new turn; the extra turn can permit a new Hypnosis and must be counted.
4. **Two XAttack** give+4 Attack. Add **one XSpDef only when observed DarkPulse damage/CalmMind makes ordinary survival require it**. Do not automatically spend three defensive turns. Heal before the current attack can KO, and keep critical exposure explicit.
5. **Crunch promptly**. At+4 it does224–264 ordinary, so two successful ordinary hits defeat381HP. A confirmed first+4 Crunch gives a conservative remaining-HP upper bound157; a faster awake second Crunch finishes before an enemy attack, even if Safeguard expired at the preceding turn's end. Do not add unnecessary boosts or renewal ahead of that finishing hit.

The actual turn numbers shift with sleep, healing, failed actions and defensive response. This is a practical plan with nonzero critical risk, not a deterministic win. If Hypno reaches+2SpA, no positive ArcSpDef stage protects against its critical DarkPulse at full294HP. Finish quickly, use a reviewed fallback, or treat the exposure as an explicit tactical risk. Repeating cures/heals blindly increases exposure.

Static normal trainer selection supports the early sleep-cure opening: player item selection registers a command, without curing yet; enemy selection follows (`Battle.rb:4104–4122`). `Battle_AI.rb:3427–3429` scores a sleep-only move0 when the target cannot be put to sleep, and `:516–522` chooses only moves within95% of the top score. Thus a currently sleeping Arc with usable alternative enemy moves should not draw another Hypnosis on the FullHeal turn. DreamEater chosen against the sleeping target then fails after the priority cure. This is installed source reasoning; always record what actually happened, and do not read live enemy choices/scores.

## Exact Safeguard ledger

`Battle_MoveEffects.rb:899–915` fails Safeguard if its existing counter is positive. A successful cast sets5. `Battle.rb:5867–5873` decrements at every completed round, including the cast round, and announces “Your team is no longer protected by Safeguard!” at0.

| Command point after a T2 cast | Counter before next command | Action |
|---|---:|---|
| EndT2 / commandT3 |4| Protection remains; do not renew |
| EndT3 / commandT4 |3| Count any item/failed action as a turn |
| EndT4 / commandT5 |2| Protection remains |
| EndT5 / commandT6 |1| Still protects the enemy'sT6 Hypnosis |
| EndT6 / commandT7 |0| Observe expiry, then faster awake renewal if needed |

The cast and next four enemy turns are protected. Renewal one turn early fails and still costs a turn. NoGuard bypasses accuracy (`Battle_Move.rb:1204`), but not the Safeguard status gate (`Battle_Effects.rb:20/36`); Hypno is not Infiltrator. Safeguard does not cure an existing status. A button receipt, helper return, move-selection receipt, or animation pause is not proof of a completed turn. If an expiry/message/turn was missed, inspect footage before queuing another action.

## Survival and healing limits

These ranges use installed final rounding through `glass_damage_review.damage`, exact frozen stats, no weather, Starlight Dark power1.5 and Dark+Fairy effectiveness0.5 into Fire, DarkSTAB1.5. Critical multiplier1.5; ordinary crit rate1/24 (`Battle_Move.rb:1390`). Crit ignores positive targetSpDef (`:1947`) and retains positive attackingSpA. All ranges are static ordinary conditions, not live damage observations.

| Hypno SpA stage | DarkPulse crit at any positive ArcSpDef | Normal atArc+0SpDef | Normal atArc+2SpDef | Normal atArc+6SpDef |
|---:|---:|---:|---:|---:|
|0|164–192|109–128|55–65|29–34|
|1|244–287|163–191|82–97|42–50|
|2|326–383|217–255|109–128|55–65|
|3|406–478|271–318|136–160|69–81|
|4|488–574|325–383|164–192|82–97|
|5|568–668|379–446|190–224|96–113|
|6|650–764|433–510|217–255|109–128|

At+1SpA, full294HP survives the current critical maximum287 with7HP margin. Current HP must be **greater than** the appropriate maximum to guarantee that hit's survival. At+2SpA, healing/defense alone cannot give a critical guarantee. Once awake and faster, a conservative finishing Crunch gives the enemy no attacking turn; this has higher priority than defensive maintenance.

UltraPotion restores200; use only while damaged. MorningSun normally restores147 at this294HP build (`Battle_MoveEffects.rb:6114–6148`). Starlight's3/4 recovery applies **Moonlight**, not MorningSun. Prefer the stronger priority item for an urgent heal; MorningSun is reasonable only with awake/faster confirmation, positive PP and enough recoveredHP for the current damage, and costs a Safeguard tick. FullHeal cures status without HP; FullRestore cures/restores but frozen stock is0. Asleep+potentially lethal DarkPulse with no FullRestore is a separate HP/status dilemma, not an automatically safe cure loop. DreamEater unboosted into sleepingArc is272–320 before a critical and heals BigRootHypno: never intentionally leave Arc asleep for it.

## Pure proposal helper

`scripts/hypno_guarded_plan.py` accepts an explicitly supplied JSON and returns **one action proposal**, ordinary helper argv and damage/turn warnings. It never invokes those argv, imports gameplay helpers, reads native saves/logs, or changes data. The caller must perform fresh visible confirmation before and after every action. `scripts/battle_batch.py` is unsuitable as an unattended Safeguard controller: its heal branch does not increment its turn counter, and generic helper returns do not prove turn completion.

Input contract:

- `build`: fresh outside-battle frozen Arc species/level/totalhp/attack/spdef/speed/item/ability and four move IDs, matching the reviewed build. A changed build stops for new review.
- `stock`: frozen prebattle quantities forXSPEED/XATTACK/XSPDEF/FULLHEAL/ULTRAPOTION/FULLRESTORE. Successful consumed items subtract; capped/refunded items cannot be silently counted as boosts.
- `observation`: fresh confirmed command menu, turn, actorArcanine/foeHypno, fieldSTARLIGHT/weatherNONE, visible numeric HP/status and fresh confirmed movePP.
- `ledger_complete:true`, and contiguous `turns`: turnnumber, confirmed/completedtrue, playeraction/result, itemconsumedboolean, observed enemy move/result, and `safeguard_expired:true/false`. Include failed/asleep/flinched player turns. Optional `observed_hp_damage` is the difference of visible HP numbers for a confirmed DarkPulse; omit when obscured.
- `accept_critical_risk:false` by default: heal above the current critical maximum if possible; otherwise return review. Settingtrue records a reviewed tactical acceptance and still guards ordinary lethal damage. It does not make the action safe from a critical.

Run `python3 scripts/hypno_guarded_plan.py work/hypno-visible-ledger-PROPOSAL.json`. Returncode2 means review/no action. The fixture template represents **unplayed turn1**, not current game state. Append only public observed turns, refresh HP/status/PP, then invoke again. Never blindly execute its future proposals as a fixed multi-turn queue.12 meaningful fixtures verify sleep-cure priority, exact Safeguard ticking/expiry, failed renewal, missed turns/messages, the finishing-hit exception, critical bypass, stock/refund disagreement and changed builds.

## Other existing-roster options and route review

Frozen postGlass bag:4XAttack,5XSpeed,12XSpDef,31UltraPotion,17FullHeal,0FullRestore,0Lum/ChestoBerry,1TM20,0TM12Taunt,0TM95Snarl. Cryogonal is not a legal Safeguard supporter in installed `montext.rb:40553–40619`; it learns Mist, a different move. Mienshao217 is faster than Hypno196 but also lacks Safeguard compatibility (`:40858–40922`). It accepts Taunt, but TM12 is not currently owned and its DarkPulse matchup is worse; do not invent teaching it. Neither reserve withdrawal nor a new berry was found inside the Void.

Cofagrigus's DestinyBond is legal against this normal trainer Hypno form1, with no opponent-level gate (`Battle_MoveEffects.rb:6490–6506`, `Battler.rb:5139–5155`). The custom `isbossmon` DB shield does not apply to this trainer form. However CF62Spe needs **three XSpeed** (+6→248; +4→186 still slower), can sleep/faint during setup and cannot cast while asleep; it is an observed-opportunity fallback, not a faster reliable opening. Existing Klinklang physicalGearGrind / Excadrill physicalEarthquake and one ordinary Revive can be used if necessary, with independent actor/build/HP/status review. This Arc-only proposal stops if the actor changes; do not carry Arc's Speed/Attack/SpDef boosts to a replacement.

`void_batch_route.py` correctly ends at758[28,106], forbids the boss tile, bounds movement chunks and guards meaningful touch events/dialogue/map transitions. Its shard and approach checkpoints validate normal healing/PP and legally taught Safeguard. It does **not** set Arcanine's lead position; do that normally before final entry. Final readiness currently requires Safeguard/Crunch/MorningSun but does not independently enforce every numerical build/held item/Flamethrower guard above; use the fresh frozen build check. No root-owned route or live navigation file was changed by this review.

After victory, stop bag/held-item/teaching/training flows, take the ordinary postbattle checkpoint and exact native item reconciliation first. Only then begin the planned Cofagrigus Timid/Hex and Cryogonal preparation for Agate. Keep the failed attempts in the full recording; only the successful Hypno victory belongs in the major compilation.
