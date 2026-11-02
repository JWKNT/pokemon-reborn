# Hardy17: reviewed numeric plan, installed19.5.43

Static future plan; **no live fight/state was read and no current party was changed**. This assumes the normal Timid/Hex/80SpA-EV Cofagrigus preparation in [agate-chain-plan-2026-10-03.md](agate-chain-plan-2026-10-03.md) has actually been completed. Its proposed Cofagrigus stats below are hypothetical until a normal post-preparation checkpoint proves them. Other stats come from the archived Glass-restocked party and the ownedLv90 Ludicolo. Recalculate if the actual team changes or levels beyond90.

The [BigJRA Geode walkthrough](https://bigjra.github.io/reborn/#geode-badge) was checked online; its Hardy roster currently agrees with the installed extraction. Exact sources and local calculations take precedence. The source-only calculator is `scripts/hardy_battle_calculation.py`, output `work/hardy-battle-calculation.json`; it imports no gameplay/native/UI helper. All calculations retain normal enemy abilities/item boosts, do not depend on a predicted AI target/move, and do not assume that Mummy or Defeatist has activated.

## Six and legal preparation

Recommended six: **Cofagrigus, Swampert, Mienshao, Klinklang, Excadrill, Ludicolo**, lead **Cofa+Swamp**. Bench Arcanine for this Rock fight; Cryogonal adds little here. Ludicolo supplies an accurate special attack reserve after the dangerous flyers are removed, rather than duplicating another physical attacker. It is **not** a safe blind early switch.

| Pokémon90 | HP / Atk / Def / SpA / SpD / Spe | Ability; item | Reviewed moves |
|---|---|---|---|
|Cofa, proposed Timid build|252 /93 /333 /210 /218 /68|Mummy; none|TrickRoom, WillOWisp, Hex, DarkPulse|
|Swamp|295 /264 /190 /199 /183 /145|Torrent; WaveIncense|Waterfall, Earthquake, Surf, RockClimb|
|Mien|228 /251 /130 /195 /145 /217|Reckless; ProtectivePads|HighJumpKick, WideGuard, FakeOut, BrickBreak|
|KG|275 /267 /228 /149 /176 /187|ClearBody; WideLens|GearGrind, MirrorShot, Discharge, ShiftGear|
|Exc|379 /312 /144 /93 /122 /182|MoldBreaker; none|Earthquake, RockSmash, RockSlide, SwordsDance|
|Ludi|285 /140 /153 /194 /208 /142|verify actual owned ability; WiseGlasses|**Scald** over Uproar; MegaDrain, ZenHeadbutt, KnockOff|

TM55Scald is already owned and Ludicolo-compatible; teach through the normal bag before entry. Scald's100accuracy and no ally damage are useful. Avoid Surf/Earthquake as the default doubles attack. Swampert **cannot learn WideGuard** in the installed moveset/compatibility; Mienshao is the carrier. Do not substitute a nonexistent SwampWideGuard branch.

No AmplifieldRock was found in the archived bag or read-only saved boxed held items. Leave Cofa unheld unless a subsequently verified legal item is deliberately chosen. Rocky **TrickRoom lasts5turns**, including the casting turn: only **four following turns**. Do not reuse Glass's field duration. Before entry, aim for at least3XDefend,2XAttack,1XAccuracy,8UltraPotion and someRevives; these are reserve goals, not a prediction of item use. Additional XDefend/XSPECIAL enable reserve setups. Check actual stock after Solaris and its warmup; those consumables remain spent.

## Installed Hardy1, doubles, Rocky

| Enemy | HP / Atk / Def / SpA / SpD / Spe | Item, ability, moves |
|---|---|---|
|Gigalith90|337 /365 /266 /126 /177 /77|ChoiceBand, SandStream; StompingTantrum, RockSlide, RockSmash, ThroatChop|
|MegaAerodactyl92|278 /372 /189 /145 /208 /367|Aerodactylite, ToughClaws; AquaTail, RockSlide, AerialAce, RockSmash|
|MiddayLycanroc92|269 /333 /153 /120 /153 /297|ChoiceBand, SandRush(**594sand**); RockSlide, DrillRun, BrickBreak, ZenHeadbutt|
|Archeops91|265 /345 /152 /213 /151 /319|FlyingGem, Defeatist; RockSlide, AquaTail, Endeavor, Acrobatics|
|Rampardos91|306 /429 /142 /135 /124 /196|ChoiceScarf(**294**), SheerForce; RockSlide, IronHead, FirePunch, RockSmash|
|DuskLycanroc97|283 /323 /161 /126 /161 /339|TelluricSeed(**+1Def→241**), ToughClaws; RockSlide, Accelerock, BrickBreak, DrillRun|

Hardy has2FullRestores. Opening sand is5turns; Gigalith holds no SmoothRock. Cofa68 is slower than Gigalith77 under TrickRoom. Swamp145 is faster than Gigalith in ordinary order, so **Gigalith still acts before Swamp under TrickRoom**; every other enemy is faster than Swamp, so Swamp acts before them within normal priority. Accelerock remains +1priority even in room.

Rocky boosts Rock damage1.5 and RockSmash power2. Its most useful defensive rule: **any positive Defense stage prevents both flinching and the extra quarter-HP rock collision**. Cofa's own XDefend is therefore both bulk and a dependable ordinary RockSlide→TrickRoom defense. RockSmash can lower Swamp's Defense; inspect its actual stage rather than remembering the original boost. Cofa is immune to RockSmash and Endeavor. KG's ClearBody prevents ordinary opposing RockSmash Defense drops.

## Guarded opener and sweep

**Xitems always boost their own acting Pokémon.** Swamp cannot select XDefend for Cofa. Ordinary medicine can target the active ally, and both actors retain their own registered action.

1. **T1 Cofa selfXDefend; Swamp selfXDefend.** Both actions occur before attacks. Cofa's +2Def remains positive despite Fighting-immune RockSmash; don't rely on RockSlide flinch luck.
2. **T2 Cofa TrickRoom; Swamp UltraPotion on Cofa**, ordinarily restoring its252HP before attacks. This establishes room even if Swamp subsequently faints. A faster optional T2SwampXAttack is permissible only after the first-turn checkpoint proves CofaHP≥174 and Swamp's own HP/Defense can survive the next pair; it is not the default queue.
3. **T3 normally Cofa heals itself; Swamp selfXAttack** for+2Atk. Guard Swamp's Defense/HP first. If RockSmash drops left Defense0 or insufficient HP, restore/heal instead of issuing the attack boost blindly. An extra recovery turn shortens this room; record its exact remaining turns. Cofa can heal Swamp while Swamp uses its own XDefend when Cofa itself has enough HP for the incoming turn. Arbitrarily repeated two-target Defense drops are not guaranteed survivable by a fixed queue.
4. **T4 Swamp Waterfall MegaAero**, then prioritize Archeops if it replaces Aero. Otherwise remove Gigalith next, because it acts before Swamp in room and ThroatChop threatens Cofa. Cofa heals the relevant teammate, uses XAccuracy before planned WillOWisp, or burns a surviving physical attacker only from a safeHP checkpoint. Do not spend a non-healing setup turn on Cofa at low HP.
5. Continue single-target Waterfall KOs while Cofa preserves itself/Swamp. At room expiration, renew **only when room=0**; selecting TrickRoom while active cancels it. A renewal turn faces ordinary speed order before Cofa's −7priority move: positive Defense and adequate HP matter. Gear/Scald reserves also need an observed room counter, not a presumed eight-turn window.

The normal lead-turn bounds at Cofa+2Def are GigalithThroatChop87–102, MegaAeroRockSlide47–56 and sand15: **173maximum**, so require **174HP** before an unhealed setup turn with both leads alive. TwoRockSlides give at most81+56+15=152. At Swamp+2Def, most focused lead pairs remain below180; if AeroRockSmash drops Defense to+1 before GigalithRockSmash, the pair can reach79+118=197. Further stage drops change those bounds; rows forDef+1/0 are in the calculation output.

These bounds are **ordinary damage, not a critical-hit guarantee**. Gigalith's criticalThroatChop258–303 ignores positive Defense and KOs hypothetical252HP Cofa; two other critical hits can also defeat either lead. The plan minimizes extra setup and checks the resulting turn instead of assuming its HP estimate remains valid after a crit. Source-proven Mummy/choice locks may improve a *subsequent observed* branch, but no opener depends on them.

## Damage and reserves

| Target | Swamp+2Atk Waterfall | KG+2Atk GearGrind, both hits | Ludi+4SpA Scald, sand |
|---|---:|---:|---:|
|Giga337HP|372–438|398–468|377–444|
|MegaAero278|523–615|556–654|321–378|
|MidLyc269|645–759|684–804|436–513|
|Arch265|650–765|688–810|441–519|
|Ramp306|696–819|734–864|538–633|
|Dusk283, seedDefense|411–483|438–516|413–486|

Every listed range guarantees an ordinary full-health KO when it hits. Unboosted Swamp already KOs MidLyc/Arch/Ramp, but not guaranteed Giga/Mega/Dusk; one XAttack covers all. Waterfall100accuracy is the main reason to favor Swamp. KG's WideLens GearGrind still has a miss chance; selfXAccuracy removes that ordinary accuracy risk. ShiftGear on Rocky is only+1Atk/+2Speed and makes it less slow in room, so selfXAttack is the efficient reserve damage boost.

Ludi needs **two own XSPECIAL (+4SpA)** for guaranteed sand KOs of every target. Its setup is conditional: MegaAeroAerialAce189–222 and first-gem ArcheopsAcrobatics316–372 even into Ludi+2Def make it unsafe before the flyers are removed. Two focused RockSlides can also exceed its285HP at+2Def. Bring it against a safely weakened/burned pair or a single remaining enemy, heal/support through setup, and don't label it an unconditional tank. KG likewise needs a guarded setup against Fighting/Ground attacks; its Steel typing is helpful against Rock, but not a universal resistance.

**WideGuard branch:** Mienshao can repeatedly guard enemy spreadRockSlides while its partner heals/boosts. It does not block targeted attacks. MegaAeroAerialAce219–258 into Mien even at+2Def can OHKO its228HP; ArcheopsAcrobatics and MidLycanrocZenHeadbutt are also dangerous. Use Mien chiefly after the flyers are gone and after observing the relevant ChoiceBand lock, or knowingly as a one-turn emergency guard that may faint after acting. Leading Cofa+Mien is less dependable than Cofa+Swamp: T1MienWideGuard+CofaXDef; if Mien faints, freeSwamp entry can heal Cofa on its room turn. Do not call the sacrifice guaranteed safe against every selected attack.

Exc is a reserve, not the default sweeper. Rocky Earthquake gains Rock effectiveness in addition to Ground: into pureRock the2×Ground and0.5×Rock cancel; Flying targets remain immune. Calculated unboosted spreadEQGiga258–304 fails to KO337, Aero/Arch0. It also hits a grounded ally. Waterfall/Scald avoid those problems.

## Commitments and subsequent route

Use [hardy-puzzle-saphira-route-2026-10-03.md](hardy-puzzle-saphira-route-2026-10-03.md) and `work/hardy-piano-proposed-template.json` for source-verified tuner geometry and guarded interaction anchors. Eight targetx values are17,19,21,16,16,14,15,15. RockClimb from739[5,46] facingUp ends[5,8]; switch1022 opens the arena door. Clear its three sight trainers first. Stage at **740[9,19]** before the player-touch Hardy trigger at[9,18], then the normalYes response starts doubles. After victory verify badge17/cap95 and the normal item ledger.

Beyond Hardy, prepare independent boss teams for Zero/PULSEClawitzer, LCCC Mime+Sigmund onShortcircuit, then the route-dependent tournament. **Tournament waiting rooms have normal PCs and menu checkpoints**; its arena transfers each commit to their own autorun fight, so it is not one Glass-style fixed-six continuous script. The later chest challenge **does** commit to26defense waves then immediateGargantuanSteelix, requiring a whole-run team/PP plan. Only after that win is there a normal Saphira preparation point and780E74LightShard fullheal. Saphira victory alone is not badge18: interact with the chest at780[26/27,43] facingUp afterward and verify the badge. These later battles still require their own numeric review.

No actual major IDs or active configs were allocated. Hardy is an eligible gym major; ordinary gym/raid trainers stay only in full journey recordings. Preserve failed attempts in the full recording and count only the successful battle footage in the major compilation, with actual attempts/items/team metadata.

Sources: installed `trainers.dat` Hardy/version1; `metatext.rb` map740 Rocky; `fieldtext.rb` Rocky; `Battle_Scene.rb:3361` self-only Xitem; `Battler.rb:4745–4765` positiveDefense/flinch; `Battle_MoveEffects.rb:8177` TrickRoom5/8 condition and WideGuard implementation; `Battle_Move.rb` mixed field typing/ToughClaws/Acrobatics; `montext.rb` Swampert compatibility. Calculator syntaxchecked and run independently; no live input execution.
