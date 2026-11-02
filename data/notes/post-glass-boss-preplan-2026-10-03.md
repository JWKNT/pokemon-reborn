# After Glass: Hypno, Agate, Hardy — installed 19.5.43

Read-only research, 2026-10-03. This is preparation, not proof of a completed fight. Fresh native checkpoints and observed footage override every estimate. Source trainer/event extracts are `work/postglass-*-installed.json` and `work/postglass-*-event.{json,txt}`. No game/save/runtime data was changed.

Exact mandatory Void gates, dialogue choices and source-only proposed routes are in [void-route-plan-2026-10-03.md](void-route-plan-2026-10-03.md). It stops one tile before the Hypno trigger and includes the OHKO/PerishSong/DestinyBond limitations for the existing six.

## Sequence and commitment boundaries

- Complete **all three Glass rounds consecutively**, unchanged six: Cain6+Shelly3 → QMARK0/Luna → QMARK1+2/Radomus+Serra. Installed734E12 heals everyone fully after round1; after round2 `pbPartialHeal` heals living HP/status only, without PP or reviving fainted Pokémon. Archive122/123/124 are already reserved; all display “Glass Gauntlet” and one shared whole-chain attempt total. Source transfers final victory to754[31,12].
- Void story maps754→755→756→757→758→759→735. **Use754E5 LightShard[17,12] after the gauntlet:** code314 fully heals, then selfA consumes it. No PC/roster replacement opportunity was found in these story maps: prepare Hypno with the same Glass six, then use the bag normally after the gauntlet. An independently verified in-game PC/exit would supersede this restriction. The starter table's **Mudkip event755E24[62,65]**, Yes, transfers to756 preserving current XY via variables47/48; our starter is Mudkip. Do not interpret these table interactions as gaining another starter.
- Hypno is **758E122[28,105], player-touch**. Prepare/save before stepping north into it. Winning sets1874True. The event's code314/full-heal is in the **loss branch**, not its victory branch; do not assume post-victory healing. Luna758E35[40,176] transfers759, and759E5[43,191] exits to735[18,18].
- [BigJRA's Void and Agate sequence](https://bigjra.github.io/reborn/#inside-the-void): finish the story, accept travel to Calcenon, talk to Shelly and Eve, then return to the story building. Eve's briefing is useful before the raid. Enter Agate from Vanhanen Labyrinth and clear the ordinary defenders.
- **Agate two-fight commitment:**763E44 page1 is autorun once391>=53. Hardy0 joins against Howaya1+Christina0, then deregisters and Solaris2 starts in the same event. No menu/save/reload between them. `Trainers.rb:230` automatically `pbHealAll` after the partnered fight, restoring HP/PP and fainted allies before Solaris. Prepare the fixed six before the final approach; finish both consecutively. The warmup remains in the full journey and is **excluded from the major compilation by the settled editorial list**. Count chain attempts honestly even though only Solaris is shown.
- Hardy arena740E3[9,18] asks Yes/No and explicitly selects **HARDY/Hardy/version1, doubles**. Victory awards badge17, raises the cap to95, sets391=60 then61 and givesTM80. [Gym puzzle](https://bigjra.github.io/reborn/#geode-badge): bottom-to-top C, E, highG, B, B, lowG, A, A; actual installed block states must be checked before writing a queue.739E31/32[11/12,4] transfer740[9,21].

## PULSE Hypno: existing roster, physical Arcanine

Exact HYPNO/Hypno/0: female100, form1 Psychic/Dark, BigRoot, NoGuard, Calm,31IVs,252Def/4SpA/252SpD. Hypnosis / DreamEater / DarkPulse / CalmMind. Stats **381HP,479Def,603SpD,287SpA,196Spe**. Starlight comes from map758 metadata. Dark/Psychic power1.5; Fairy1.3; Dark attacks also receive Fairy effectiveness. Weather suspends field boosts, so do not introduce weather casually.

Use ownedTM20 **Safeguard on Arcanine**, replacing ExtremeSpeed after the Glass chain. Arc is installed-compatible; no new Pokémon or move reminder required. CalmMind raises Hypno's special bulk, making physical **Crunch** preferable to prolonged Flamethrower setup. Starlight Crunch is Dark+Fairy, net2× into Psychic/Dark, plus1.5field power. Based on current Arc228Atk/171SpD/176Spe/294HP:

| Arc Attack boost | Approximate Crunch | Maximum ordinary hits needed |
|---|---|---|
| none |76–90|6|
|+2, oneXAttack|150–177|3|
|+4, twoXAttack|224–264|2|

These are ordinary damage estimates, not live tests. No Attack increase is mandatory. One/two XAttacks reduce exposure and consumable use; native pre-resume bag has **zero**, so buying them requires a legitimate supply run before committing to Glass. Current stock23Ultra/11FullHeal/6XSpDef/8XSpeed/10XSpAtk may change during the gauntlet; refresh the count before Hypno.

Practical plan: XSpeed makes Arc352Spe, comfortably above196. Establish and maintain **five-turn Safeguard**, reach+6SpDef with threeXSpDef if needed, attack physically and heal before lethal damage. Against Hypno+6SpA, Arc+6SpDef receives roughly109–128 per ordinary DarkPulse; Ultra heals200, MorningSun normally147. Count each CalmMind and each Safeguard end-turn tick. Renew Safeguard while awake before Hypnosis can land; never simply hold Crunch for six turns. If initial speed setup causes sleep, FullHeal resolves before Hypno's move: a previously selected DreamEater can fail after waking, allowing faster Safeguard next turn. **Do not assume the AI always chooses DreamEater**; observe and adapt. Critical hits ignore defensive boosts, so shorter plans reduce risk.

KG is an inferior setup alternative here: Starlight **ShiftGear gives+1Atk/+2Spe per use**. Three uses give+3Atk, unlike Factory's doubled Attack gain. ArcSafeguard→switchKG consumes a turn and does not provide a clean six-boost window. No Phantom Factory bonuses.

Owned alternatives are useful only if included before the Glass commitment: Drapion70(KeeneEye) is Psychic-immune and Dark/Fairy DarkPulse net0.5, but needs training and suitable attacks; Kricketune50 already holdsFocusSash and knowsPerishSong/XScissor/StickyWeb/RockSmash. Neither can be silently withdrawn inside the Void. Do not sacrifice a well-prepared Glass sixth merely to simplify Hypno when Arc already has a legal answer.

## Solaris: fully physical opponent and Mega ace

The deeper whole-chain preparation is now in [agate-chain-plan-2026-10-03.md](agate-chain-plan-2026-10-03.md): exact y52 commitment guard, shared Cofa lead, normal Timid/Hex/SpA training, damage/speed proof and the mandatory partner full-heal boundary. Use that reviewed plan rather than treating the preliminary unboosted Cryo discussion below as a guaranteed ace counter. No proposed roster changes have been executed by this research agent.

No Field; oneFullRestore. Exact Solaris/Solaris/2:

| Pokémon | Level / item / ability | Four moves |
|---|---|---|
|Staraptor|89 / Leftovers / Intimidate|Return, CloseCombat, Uturn, BraveBird|
|Scizor|88 / LifeOrb / Technician|BulletPunch, Uturn, Superpower, KnockOff|
|Gyarados|90 / WacanBerry / Moxie|DragonDance, Earthquake, Waterfall, Outrage|
|Tyranitar|89 / SmoothRock / SandStream|StoneEdge, Earthquake, Crunch, FirePunch|
|Excadrill|90 / FocusSash / SandRush|Earthquake, RockSlide, SwordsDance, IronHead|
|Garchomp|93 / Garchompite / RoughSkin→SandForce|SwordsDance, Earthquake, DragonClaw, StoneEdge|

The Garchomp has **252EVs in all six stats**, independently of HARDCAP-only settings. Sand boosts its Mega attacks and enemyExc speed. Do not calculate its bulk like an ordinary510EV Pokémon.

Keep Arc for Intimidate/ScizorFlame, Cofa for physical burn/TrickRoom/DestinyBond, Swamp for Ttar/Exc and Mienshao for priorityFakeOut in the warmup and Fighting damage in singles. A practical roster change is **already-owned Hexan/Cryogonal90 replacing the least useful sixth**: IceBeam gives4× coverage intoGarchomp and FreezeDry4× intoGyarados, with Recover/LightScreen. Native Hexan is Brave207Spe,205SpA,320HP/132Def; it does **not** naturally outrun Staraptor266, Gyarados258 or MegaGarchomp. A TimidMint is owned, but alone does not imply enough Speed; verify stats and use XSpeed/TrickRoom deliberately. IceBeam is not a proven unboosted OHKO against the fully invested Mega. Keep it away from physical rock hits until it can act safely. Borrowing the ownedKricketuneFocusSash is legal, but sand chip can break it.

Optional Ampharos85→90 provides a sturdier direct Electric attacker, ThunderWave and LightScreen. Gyarados's WacanBerry halves the first Electric hit, not FreezeDry. The preceding 12v10 warmup contains Ludicolo/Lapras/Magneton/Lanturn/PorygonZ and Beheeyem/Eelektross/Cryogonal/Seismitoad/Clefable. Do not spam Discharge into LanturnVoltAbsorb or use Surf into LaprasWaterAbsorb. Exact warmup and partner rosters are extracted beside the boss files.

## Hardy: WideGuard, TrickRoom, defensive field interaction

Rocky Field; twoFullRestores. Exact Hardy1 lead order:

| Pokémon | Level / item / ability | Four moves |
|---|---|---|
|Gigalith|90 / ChoiceBand / SandStream|StompingTantrum, RockSlide, RockSmash, ThroatChop|
|Aerodactyl|92 / Aerodactylite / Pressure→ToughClaws|AquaTail, RockSlide, AerialAce, RockSmash|
|Lycanroc midday|92 / ChoiceBand / SandRush|RockSlide, DrillRun, BrickBreak, ZenHeadbutt|
|Archeops|91 / FlyingGem / Defeatist|RockSlide, AquaTail, Endeavor, Acrobatics|
|Rampardos|91 / ChoiceScarf / SheerForce|RockSlide, IronHead, FirePunch, RockSmash|
|Lycanroc dusk form2|97 / TelluricSeed / ToughClaws|RockSlide, Accelerock, BrickBreak, DrillRun|

Field: Rock power1.5, RockSmash power2, Earthquake gains Rock effectiveness and1.5power, so **do not assume ordinary Ground2× against pureRock** (Ground2××Rock0.5 becomes neutral). Missing a contact attack causes1/8HP recoil. Most dangerously, flinching without protection causes **1/4HP rock recoil**. Installed`Battler.rb:4761` additionally says a positive Defense stage prevents flinching and its recoil. An XDefend can be used before incoming attacks, guaranteeing that particular flinch gate is cleared; this is more reliable than hoping twoRockSlides do not interruptTrickRoom.

Keep Cofa and MienshaoWideGuard. **Correction from installedBattleScene3359:** Xitems forcibly target the Pokémon spending that action. Swamp cannot use XDefend on Cofa. Cofa must use XDefend itself on an earlier turn, then use TrickRoom on the following turn, supported by WideGuard/Intimidate and normal healing as needed. Do not publish the previous one-turn proposal as a valid opener. Swamp resists Rock and is healthier than most candidates into the lead coverage; Cofa's+2Def prevents flinching once established. Track both targeted attacks/HP, then burnGigalith and removeAerodactyl before exposingMienshao toAerialAce. WideGuard stops spreads, **not AerialAce, ZenHeadbutt, Acrobatics orAccelerock**. Cofa62Spe is slower thanGigalith77, so acts first underTrickRoom; all enemy fast rocks then favor our slower attacks. Renew room only after it expires, and do not assume KG/Exc can freely set up into boostedRockSmash/Fighting coverage. Any actual opener needs current damage calculations and live observation.

No capture is required. Existing Ludicolo90 can replaceArc for this Rock gym; teach ownedScald/Surf before assuming its current MegaDrain/ZenHeadbutt/KnockOff/Uproar build is ready. Its142Spe fitsTrickRoom; sand raises opposingRockSpDef. ExistingSwamp/Exc/KG provide real Rock resistance. **Optional new reserve:** LevitateBronzong is legitimately catchable onRoute3/map361 (17%morning,5%day/night;55–62 or72), learns/accepts ownedTM92TrickRoom, and combines Rock resistance with Ground immunity and GyroBall. It still fears ThroatChop and RampardosFirePunch. OptionalStormDrainGastrodon is obtainable viaSurf in ChrysoliaSpring1F/map238 (15%,60–80), adding recovery and Water immunity forAeroAquaTail; only train it if Swamp's coverage actually proves insufficient. Catch/train through normal controls, never alter ability/EV/save data.

## Archive choices and exact source anchors

Settled planned entries future012–014=Glass, future015=Hypno, future016=Solaris, future017=Hardy. After existing122–124, **candidate IDs125/126/127** must be confirmed unused at actual entry; these notes do not allocate them. Only these boss victories belong in the major compilation. OrdinaryGlass trainers, Void dialogue, Agate defenders, Howaya/Christina and gym trainers stay in fulljourneys. Solaris's editorial warmup exclusion survives the requirement to play its true chain consecutively. Show exact player bag consumable totals from each displayed completed log, not opponentFullRestores; record every failed chain in the full journey. Actual doubles ownership/left-right order must come from footage.

Installed anchors: trainers.dat; Map734E12,754E5/14,755E24,758E122,759E5,763E44,739E31/32,740E3; `Trainers.rb:136–240`; `metatext.rb` maps740/758/763; `fieldtext.rb` ROCKY805 / STARLIGHT2200; `Battle_Move.rb:1118` mixed effectiveness; `Battler.rb:4740–4765`; `montext.rb` Hypno6963/7035, Arc4217, Kricketune27016, Drapion30162; `enctext.rb` maps238/361. Static source and actual current snapshots take precedence over guide version19.5.18. CurrentBigJRA Gym roster happens to match the extracted Hardy1 list; historic wording that the live online guide still differs is stale.
