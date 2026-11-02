# Mega Ring prerequisite and normal quest plan

Source-only plan. No game controls or save writes. Installed19.5.43 map/script declarations take precedence over [BigJRA's quest outline](https://bigjra.github.io/reborn/#mega-z-ring-quest). Static export: `work/mega-ring-installed-source.json`; exact mandatory teams: `work/mega-ring-mandatory-teams-source.json`; frozen cost report: `work/mega-ring-frozen-preplan.json`. These use explicitly frozen `Void-Hypno-won-128-{status,navigation}.json`, not current runtime or battle information.

**The Mega-Z Ring is optional, not an automatic main-story gift.** Its quest can first be completed on the restored-city return after Ciel, and is available again after Titania if that opportunity was missed. Current frozen evidence has sixteen badges, restoration switch479=true and MEGARING=0. Swampertite alone cannot enable MegaSwampert: `Battle.rb:901–910` requires an owned Ring/Bracelet/Cuff/Charm. Do not start the earlier MegaSwamp Saphira plan until normal bag/form proof establishes the ring. The GrandHall38E69 gift requires extra password switch2166; it is excluded under this run's HARDCAP-only rule.

## Purchases: no Squirtle or wild replacement required

The source requires buying all nine SeventhStreet cage Pokémon, then returning **five**, not four. Earlier Ditto rescue switch426 lowers the threshold to eight purchases. Frozen426=false, and no cage16–24 purchase self-switch is recorded in the planning mirror. An absent mirror flag is not proof that a Pokémon was never bought: inspect actual cage pages and normal PC before paying or searching for replacements. Frozen160=0 is an observed planner value, not a newly read save claim.

|324 event; position|Pokémon/original owner|Shard cost|Returned for Ring?|
|---|---|---|---|
|16;29,42|Vanillite35 / Eustace|3Purple|Yes|
|17;30,42|Loudred35 / Lillin|5Blue|Yes|
|18;35,39|Cyndaquil10 / Sanford|9Red|No|
|19;33,42|Lickitung35 / Myles|7Blue|No|
|20;31,39|Makuhita40 / Felicia|3Green|Yes|
|21;34,39|Jigglypuff30 / Santiago|5Green|Yes|
|22;35,45|Abra15 / Arzelle|8Purple|No|
|23;32,45|Roggenrola24 / Mr. McKrezzy|3Red|Yes|
|24;35,42|Ditto5 / Sanford|8Green|No; earlier426 skips this purchase|

All-nine totals are **12Red/12Blue/16Green/11Purple =51 shards**, with no direct money payment. Frozen stock is6Red/4Blue/8Green/7Purple; if all nine cages are still unbought, the additional requirement is **6Red/8Blue/8Green/4Purple =26 shards**. Existing purchases reduce this. The probe did not find a verified normal shard mart, so the item's1000 base price does not prove buyability. Uncollected ordinary pickups/mining are valid; do not silently use the developer mart or grant shards. SevenStreet tutor purchases, such as future KnockOff/GigaDrain, compete for this stock.

The current19.5 save uses `belongsTo(poke,name)`, which checks `trainerID == KNOWN_TRAINERS[name]` (`Utilities.rb:2948–2950`), not a species-only match. Original shop Pokémon must be returned; evolution preserves provenance, while catching another Jigglypuff does not qualify. The five returns remove the chosen Pokémon and return any held item to the bag. This quest's Jigglypuff is therefore separate from a future permanent PerishSong reserve. Squirtle and the starter-egg quest are unrelated.

## Source order and bounded ordinary queues

Each successful cage purchase increments160 by1 and sets its own324,event,A. After nine purchases, talk to **324E26p2** (or p4 if Arc is absent during Devon): it sets160=12; the early-Ditto path is p3/p5 at eight+426. Enter restored NorthObsidia **527E87[36,22]→826[10,11]** and talk to Arc **826E8[12,5]p0**, requiring479/160>=12, to set160=20. His list identifies five owners. During the Devon story Arc can be temporarily absent; the current after-Titania branch is reopened. Reward is p4 at160>=25, sets160=26 and givesMEGARING. Do not change these story values in planning to manufacture access.

An efficient normal order, with visible first-line/page/quest proof after every interaction:

1. Carry original Loudred and Jigglypuff. **Jasper523E3[19,31]→534[10,11]**; Lillin **534E4[12,9]** needs first refusal p0 then p1 return Loudred, sets1724 and160+1.
2. NorthPeridot **522→532**, entrance at522[103,36], Santiago **532E8[8,9]p0**: stand below him facingUP (he checks player direction8), win his required singles, sets709. Talk again if the old NorthPeridot-Alley mirror does not reflect the battle flag. This fight has a normal field checkpoint afterward.
3. Return Jigglypuff to Lillin p2 with709: she keeps it temporarily and sets710; this does **not yet** count a completed fifth-owner return.
4. Felicia **23E16[1,17]** in Apophyll's middle west dormitory. Restored outside **564E4[5,19]→23[4,17]**. First talk sets708. Arc826E8p2 gives ARCAUTOGRAPH and selfA; return to Felicia p1 to give autograph/selfA, then p2 return original Makuhita (1721,160+1,selfB). With710, **talk once more on p4** to request McKrezzy's autograph, setting711. This request must precede the autograph pickup.
5. Spinel **242E58[4,20]**: first talk p0 setsA; p1 returns original Roggenrola (1722,160+1,selfB); p3 with711 gives MCKREZZYAUTOGRAPH and selfC. **Stop here: p4 offers an optional battle.** The installed quest does not require fighting McKrezzy; this saves a six-Pokémon battle compared with following the guide's suggested sequence literally.
6. Felicia p5 exchanges autograph for HEADPHONES/selfC. Lillin p3 exchanges headphones, finishes Santiago's return (1725,160+1,712); either Yes/No in the harmless hearing demonstration advances the same dialogue. Require actual headphones/reward text.
7. Lapis **524E48[26,29]→612[4,10]**, mother **612E6[3,6]p1** sets2154. Santiago first needs p1 with712 to setselfA, then p2 with2154/selfA to set713. He reveals the Onyx rooftop. Return here with a healed fixed combat six and normal medicine; do not carry low-level quest passengers into the chain.
8. **573E30[17,10]p0**, switch713: mandatory Colin0+Matthew0 doubles followed immediately by Eustace0 singles. There is dialogue but **no source heal, PC, party menu or bag window between battles**. Prepare all six/PP/items before triggering the first battle. One chain attempt must win both consecutively; if Eustace loses, do not publish the first battle as a successful chain. Normal victory sets714; do not mirror it before observing the actual result.
9. Lapis upstairs **612E7[22,8]** with714: first talk p0 sets its selfA, then a second talk p1 returns original Vanillite (1723,160+1,selfB). After all five increments,160=25. Arc826E8p4 gives the ring. Verify its actual bag quantity and later a normal successful Mega form change; then save at an ordinary checkpoint.

Dialogue batches should stop before every Pokémon selector, choice that has not been reviewed, battle, and transition. A queue may combine verified outdoor Fly hops and static transfer endpoints, but it must refresh actual map/page proof after each transfer. Never run old g9 scripts wholesale: they overwrite obsolete navigation stages. No new queue was executed or future config allocated here.

## Mandatory battle scope and preparation

|Battle|Installed roster|Preparation implication|
|---|---|---|
|Santiago0 singles|Azumarill79/HugePower; Sylveon80/Pixilate; Lopunny82/Limber/Sitrus|Do not leave BellyDrum Azumarill free while setting up. Klinklang Steel damage against the Fairies and Cofagrigus physical control are useful; plan moves from the fresh actual party rather than assuming the current Hypno build persists.|
|Colin0 doubles|Weezing73/Levitate/DestinyBond; Mudsdale74/Stamina/AV; Zangoose76/ToxicBoost/ToxicOrb|Avoid unobserved DestinyBond trades. Ground misses Weezing; physical repeated hits grow Mudsdale's defense.|
|Matthew0 doubles|AlolanMuk73/PowerOfAlchemy/Minimize; Tsareena74/QueenlyMajesty/LifeOrb; Lickilicky76|No priority reliance into Tsareena. Accuracy setup or guaranteed-hit choices address Muk; WideGuard protects spread moves but does not make the whole turn safe.|
|Eustace0 singles, same entry six|Manectric81/Specs; Sceptile81/Unburden/Sitrus; Sharpedo82/SpeedBoost/LifeOrb; Scizor83/Technician; Alakazam84/LifeOrb|Fresh Swamp against Electric, Arc for Grass/Steel, Mien for Sharpedo, Cofa's bulk/DarkPulse or other confirmed coverage for Psychic. Preserve these during doubles; stage boosts do not carry into the second battle.|

All mandatory teams are lower than the current90 cap, and fields have no special field boost in the quest outline; there is no fixed promise of a sweep or damage guarantee. Exact installed moves/items/IVs are in the team JSON. None of these quest fights is added to the settled major-battles roadmap; retain all attempts in the full journey.

## Budget decision and Saphira fallback

This is available before Gym18 and has lasting Mega/Z value for the EliteFour, but is a meaningful detour: up to nine purchases, five original-owner retrievals, many Fly/PC visits, three mandatory battles (the last two consecutive), and possibly26 extra shards. No measured time estimate exists; allow an additional session if shard collection or provenance inspection is needed. The normal Ring route is preferable long term when budget permits, but **not a requirement for beating Saphira now**.

Without the Ring, the earlier proposed Careful95 spread [252,4,0,0,212,40] gives ordinary Swamp **363HP/243Atk/187Def/155SpAtk/258SpDef/145Speed**. Seeded Noivern's critical DragonPulse reaches about374, and+6Speed580 loses to a single field-DD Salamence630/Charizard638. Thus simply removing the Mega button is unsafe. MaximumHP/SpDef [252,0,0,0,252,4] narrowly limits that crit to360 but only548 boostedSpeed, so it is not the same sweeping plan either.

The independent calculation now prefers **ordinary Impish AssaultVest Swamp95**, EV[252,0,100,0,52,104], giving363HP/242Atk/232Def/155SpAtk/197SpDef/160Speed. AV gives295.5 effectiveSpDef; seeded Noivern critical DragonPulse278–327 fits the full-HP build, and+6Speed640 beats one-DD Salamence630/Haxorus610/CharX638. Unboosted Salamence/Haxorus critical DragonClaw ceilings334/351 allow individually guarded Sash branches: actualHP>337/>355, no previousDD, first strike, then kill next command without adding a healing turn. **The whole-chain handoff remains conditional:** healing Noivern/Garchomp does not promise fullHP afterward, and healing the newly entered dragon can grantDD and invalidate the unboosted ceiling. See `nonmega-saphira-review-2026-10-03.md` and its pure calculator before choosing the actual build.

**AV is also locked behind an optional prerequisite in the named frozen state.** The normal pickup is602 UndergroundRailnetE17[17,7]. Every installed602 entrance comes from restored519E215–219 and requires652; no Dive is required in those actual event declarations. Frozen652=false. Pre-Saphira, the normal unlock is GrandHall38E37[14,7], RailnetReconstruction, base **100,000**, with variable335 tracking remaining donations. Frozen337=0 has no observed completed project, and74,180 money is25,820 below the full untouched price. Source initializes335 on the first funding conversation, so frozen default335=0 is **not** proof that restoration is free; inspect normal UI for the real remaining amount before payment. The later postgame Lumi setter is irrelevant. Full funding must be observed before mirroring652 or routing into602. Source proof is `work/mega-ring-railnet-funding-source.json`; actual uncollected pickup status also needs normal verification.

X items are allowed while wearing AV; status moves such as Protect are not. The AV route avoids the Ring quest but can consume up to100k before medicine/nature/EV training. The Ring requires shards and three fights instead and remains valuable for EliteFour/Z options. Neither upgrade is assumed immediately available. Sylveon/Misty and Cryogonal alternatives are conditional; the gift Sylveon's natural reminder list lacks BatonPass, so a BatonPass chain needs a separate legal Eevee acquisition/evolution. This review did not execute game controls or allocate future battle configs.

Validation: `mega_ring_source_probe.rb` syntax check and static extraction pass; `mega_ring_preplan.py` verifies all nine exact source costs/owners and creates the hash-bound frozen cost report. No live gameplay benchmark or new save inspection was made. One mistakenly invoked legacy `map_brief.py` refreshed only the derived `notes/map-state.json` cache from the current save; root was informed, confirmed no navigation/save repair was needed, and further research used static exporters only.
