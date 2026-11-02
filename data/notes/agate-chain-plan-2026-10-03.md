# Agate fixed-six chain: reviewed preparation, installed 19.5.43

Source-only planning, not a completed fight or an executable battle script. No UI, current battle logs, game data, or save data was changed. Calculation output: `work/agate-chain-calculation.json`; pure calculator: `scripts/agate_chain_calculation.py`. It uses extracted trainer data, construction defaults and the installed final damage formula, not enemy decisions or future rolls.

## Commitment and full-heal boundary

The final trigger is **Map763 x43–48, y52**, touch events110/113–117. Entering the strip forces movement and sets391=53, after which E44 autoruns wherever the player stands. **[45,53] with391=52 is a source-proven passable, event-free preparation checkpoint. There is no confirmation prompt.** `work/agate-commit-source.json` and `work/agate-prep-source-narrow.json` preserve the event proof.

E44 registers Hardy0, starts Howaya1 + Christina0, deregisters Hardy after victory, then starts Solaris2 in the same event. No intervening menu, PC, party reorder or save. Installed `Trainers.rb:230` fully heals the player's HP/status/PP, including fainted party members, after the partnered warmup. Battle boosts and battle weather/terrain reset. **Consumed held items do not return:** `Battler.rb:3915` clears itemInitial on consumption, and Battle6697 restores the resulting initial item. Do not spend the backup FocusSash in the warmup.

Both battles start **No Field**: map763's backdrop FieldEve has no compiled field match. Each battle independently copies current overworld weather. Native-check weather before committing; initial rain changes Ludicolo153→306 Speed. The proposed Cofa lead does not rely on outspeeding it. Warmup RainDance/ElectricTerrain does not carry into Solaris.

Street defenders do not commit the chain: Ricardo1 E48[33,62], Antoine1 E49[37,63], Lyla1 E45[42,60], Ezra1 E46[42,55]. Lyla/Ezra sightlines overlap on x42,y56–59 and can merge into doubles. Side defenders Christopher0[30,54] and Ama0[68,44] remain ordinary. Rebuild native passability/event guards after each fight, and block the y52 strip until all prep is complete.

## Recommended same six and normal preparation

**Lead Cofagrigus for both fights. Replace Klinklang with owned Hexan/Cryogonal90.** Klinklang loses its Factory benefits here and has poor coverage into Ground/Fire/Fighting attacks. Excadrill retains MoldBreaker utility in the warmup; Arcanine, Swampert and Mienshao retain concrete singles counters.

| Slot | Level / ability / held item | Moves for this commitment |
|---|---|---|
|Cofagrigus|90 / Mummy / **no item**|TrickRoom, **Hex**, WillOWisp, **DarkPulse**|
|Arcanine|90 / Intimidate / Charcoal|Safeguard, Flamethrower, Crunch, MorningSun|
|Swampert|90 / Torrent / WaveIncense|Waterfall, Earthquake, Surf, RockClimb|
|Mienshao|90 / Reckless / ProtectivePads|HighJumpKick, WideGuard, FakeOut, BrickBreak|
|Excadrill|90 / MoldBreaker / no item|Earthquake, RockSmash, RockSlide, SwordsDance|
|Cryogonal|90 / Levitate / **borrowed FocusSash**|LightScreen, IceBeam, Recover, FreezeDry|

Normal changes before the checkpoint: owned **TM97 teaches Cofa DarkPulse over DestinyBond** (installed-compatible); remove SpellTag; use owned **TimidMint on Cofa**. Then **4 Pomeg berries remove80HP EV;3 ordinary KOs holding PowerLens add32+32+16 SpA EV**, preserving Defense EV252. Remove Lens and fully heal. Result: **252HP /93Atk /333Def /210SpA /218SpD /68Speed**, EV[172,4,252,80,0,2]. Pomeg costs500 at Store2F; PowerLens15000 at Store4F **Map183E1[13,5]** (our saved sticker count91=3 grants access), or Circus355E83[36,14] while715 is false. Current saved715 is nil/false, so that shop page is available; check it again when approaching. Do not assume Lens owned. The training changes require ordinary gameplay, not file edits.

Relearn **Hex (natural level17) over ShadowBall**, costing one HeartScale at Circus355E35. At research time bagHeartScale0 and CF's permanent reminder unlock is false. Source-proven uncollected scales in the latest saved self-switches: **Route4 Map715E64[57,20]** and **TourmalineDesert Map704E87[34,53]**. The source locations/conditions are in `work/agate-heartscale-candidates.json`; plan a normal guarded approach rather than assuming a straight line. All prep including berries/Lens costs17000 plus the scale trip. Cofa remains slower than every Hardy17 opponent for that gym's TrickRoom plan; moves can be normally retaught afterward. Borrow FocusSash from boxed Kricketune50; keep Cryo out of the warmup unless actually needed.

The extra SpA is deliberate: Hex130 into a burned Mega must clear391HP **without a held item**, because Scizor can remove SpellTag with KnockOff. Mint alone with existing192SpA does not meet that guaranteed KO. A limited quicker variant retains ShadowBall and270HP, but its two-hit Mega plan still risks a burned+2Atk sand EQ critical308; do not call that variant critical-proof.

The mint matters: Cofa with three XSpeed reaches **272**, above Staraptor266, Gyarados258 and MegaGarchomp263. Installed Battle4325 recalculates turn order **after Mega evolution**, so Garchomp's pre-Mega282 does not break the first-turn comparison. SandRush Excadrill496 is the one exception. Never retain TrickRoom during the fast-Cofa plan except the short Excadrill branch.

Budget after refreshing the post-Glass/Hypno native bag: **at least6 XSpecial, 3 XSpeed, 2 XSpDef, 2 XDefend, 1 XAccuracy, roughly15 UltraPotions**, FullHeals and a few Revives. The restocked pre-Glass snapshot had10/8/16/10/5/43 respectively, but Glass spent some; buy a useful margin before Agate. Warmup uses up to3 XSpecial, Solaris uses3; their boosts do not carry. X items target the **acting Pokémon only**. An UltraPotion heals200; include sand16HP/turn in health guards. One or two MaxPotions are useful for restoring a critical-hit health margin quickly if stocked normally.

## Warmup: own damage, no assumed Hardy targeting

Howaya: Ludicolo87 / Lapras87 / Magneton88 / Lanturn89 / PorygonZ89. Christina: Beheeyem87 / Eelektross87 / Cryogonal88 / Seismitoad89 / Clefable89. Their unspecified nature/IV/EV defaults are **Hardy /10 /85 in every stat**, not zero EVs. Full moves and exact stats are in the calculation and `work/postglass-howaya-installed.json`, `work/postglass-christina-installed.json`. Hardy0's six are92/90/91/91/92/97; do not require his RockSlides, flinches or weather to make our moves work.

Open **Cofa self-XSpDef**, then a second self-XSpDef when health permits. At+2SpD the initial ordinary pair's worst clear-weather damage is106 total; with rain it is117. At+4SpD, rainy Surf34 + Beheeyem DarkPulse/ShadowBall46 is **80 maximum**. Heal before another action whenever the current observed pair can KO; do not blindly queue a fixed seven-turn opener. DarkPulse can flinch and interrupt TrickRoom, so verify room actually starts.

Build Cofa to **+4 or preferably+6SpAtk**, use TrickRoom after healing and attack Beheeyem first. Cofa68 is slower than all opposing unboosted warmup Pokémon, so acts first under room. +2SpAtk **unstatus Hex273–321** already KOs unshielded Beheeyem254HP; +4 remains a guaranteed KO behind doubles LightScreen. Burning doubles Hex65→130 and controls physical foes, but do not spend a burn turn when an unstatus attack already guarantees a KO. Renew room only after it expires, heal before the dangerous pair, and burn a dancing Lapras or physical Eelektross rather than allowing endless setup.

Important branches: **PorygonZ is Normal and immune to Hex; use DarkPulse.** LightScreen can appear later; multiply special damage by the installed doubles factor0.66 until it expires. Preserve10 Hex PP: use DarkPulse for lowHP finishes, and use the normally healed backup counters rather than presuming Cofa has unlimited attacks. Magneton has Sturdy; enemy Cryogonal's FreezeDry is4× into Swampert. Lanturn absorbs Electric attacks and Lapras absorbs Water attacks. Surf/Earthquake hit our NPC partner; use Exc's MoldBreaker Earthquake into Magneton/Eelektross only with an airborne Hardy partner or a deliberate, reviewed trade. Mienshao WideGuard blocks spreads, not Beheeyem's targeted Psychic. CF/Arc/Cryo give clean attacks while preserving the reserve Sash.

Faints in a **winning** warmup are healed before Solaris, but if Cofa faints it cannot finish warmup setup and the plan needs a normal backup. Rare stacked criticals bypass positive SpD; this opening is not a promise against every double critical. Inspect health and stop an input batch on a faint, replacement, new screen or unexpected room result.

## Solaris: fast Cofa, all attacks physically bounded

The opponent is entirely physical, with one FullRestore. Staraptor89 Leftovers; Scizor88 LifeOrb; Gyarados90 WacanBerry; Tyranitar89 SmoothRock; Excadrill90 FocusSash; Garchomp93 Garchompite. Exact HP/Atk/Def/SpA/SpD/Speed:

| Pokémon | Stats |
|---|---|
|Staraptor|312 /294 /157 /108 /139 /266|
|Scizor|303 /347 /209 /116 /173 /146|
|Gyarados|299 /314 /175 /126 /212 /258|
|Tyranitar|360 /359 /229 /180 /210 /141|
|Excadrill|326 /365 /140 /109 /149 /248; SandRush496|
|MegaGarchomp|391 /448 /306 /283 /269 /263|

Garchomp has252 EVs **in all six stats**. Its sand-boosted Earthquake is lethal to slow unburned Cofa on a critical (264–311); prevent that race rather than treating ordinary bulk as sufficient.

Against the starting Staraptor, Cofa uses **self-XDefend, self-XAccuracy, WillOWisp**, with UltraPotions inserted before an unsafe turn. Then reach **+6Speed with3 XSpeed and +6SpAtk with3 XSpecial**. Cofa's Return/CloseCombat immunity, Uturn resistance and Defense333 make this a useful setup target independent of which ordinary move it selects. Pre-burn BraveBird critical maximum180 means keep **at least181HP** before an exposed action; after burning its critical maximum90 means at least91, plus any weather chip. Ordinary+2Def BraveBird is51–60; burned damage halves again. XAccuracy gives+2 accuracy, making85%-accurate WillOWisp reliable with no enemy evasion/field modifiers.

**Uturn changes the current opponent:** stop and branch immediately, do not finish the Staraptor setup macro into Garchomp or Tyranitar. Until all three speed items are applied, the first-entry Garchomp critical risk remains real. Arc's Intimidate, a normally healed reserve, and a correctly timed room/switch remain emergency options; do not call the whole fight guaranteed from turn1.

With full setup, preserve Cofa's boosts and use these independent damage bounds (no SpellTag, drops, recoil or Mummy assumed):

| Target | Attack / damage / ordinary hits |
|---|---|
|Staraptor|**DarkPulse314–369**, guaranteed1; Hex does0|
|Scizor|unstatusHex307–362 already guaranteed1; burnedHex613–722|
|Gyarados|burnedHex501–590, guaranteed1; unstatus251–296, at most2|
|Tyranitar in sand|burnedHex169–199, at most3; unstatus85–100|
|Excadrill|unstatusHex357–420 or burned711–837; at most2 with intact Sash|
|MegaGarchomp|**burnedHex395–465, guaranteed1**; unstatus199–234, guaranteed2|

**Burn each healthy physical foe first when needed, then finish promptly.** Scizor's priority BulletPunch can precede fast Cofa: unburned critical maximum140, burned70. No held item reduces Scizor KnockOff critical300→203; burn further reduces it. Tyranitar's burned Crunch critical maximum147, plus sand16. At272 Cofa burns before Tyranitar attacks. FirePunch can inflict player burn, adding chip; cure an actual status or include it in the health guard. Physical player burn does not reduce Cofa's special attacks.

Gyarados may raise Speed beyond272 with DragonDance, but burned+2Atk Waterfall critical maximum131; one burned Hex kills it. If a FullRestore clears burn before Hex, the first unstatus hit leaves at most48HP and another Hex finishes; include its actual Attack stage in the health guard if it now acts first. MegaGarchomp receives burn **before** its first move at272, then burned Hex KOs before it can attack after SwordsDance. If the single FullRestore removes burn before Hex, it takes the foe's action and the unstatus hit leaves at most192HP, below the next unstatus minimum199: **finish immediately** before Mega's move. Reapply burn on targets needing further turns, especially Tyranitar; do not waste a guaranteed finishing turn on status.

**Sand Excadrill branch:** restore a useful HP margin before facing it, then set TrickRoom while it has at most+0Atk. Its unburned+0Atk EQ critical maximum191 +sand16 requires208HP to cover that particular turn. Under room, fast Cofa272 is slower than SandExc496, so burn before its next move, then Hex removes it. Burn chip usually breaks its Sash before the attack; retain a second-hit contingency if FullRestore heals it. Burned+2Atk EQ critical maximum189; +4 is dangerous282, so do not extend the sequence unnecessarily. RockSlide/IronHead flinch can interrupt room: verify it, heal and adapt. Contact Mummy can remove SandRush, but **do not count on it**; observed ability/weather decides speed order. When sand ends, Exc is248 and Cofa272 is naturally faster, so room is unnecessary and can become counterproductive.

Use10 Hex PP carefully: the conservative route consumes8 with the Sash contingency, and Tyranitar's single FullRestore can add about2. Burn chip usually lowers the actual count, but do not depend on that arithmetic blindly. DarkPulse can finish lowHP neutral foes or preserve Hex PP. Full-heal between fights restores these PP first. If switching Cofa to a counter, its boosts are lost; native-check remaining items before trying to rebuild.

Backups are real rather than unboosted “ice OHKO” assumptions: **Cryo205SpA IceBeam Mega=275–324, not a KO391; +2SpAtk=541–636. FreezeDry Gyarados=270–318, not guaranteed299; +2=530–624.** A fresh Sash plus an active room with sufficient remaining turns can allow Cryo one XSpecial followed by the guaranteed Ice attack. Sand chip can break Sash, and stock207Speed is slow outside room. Burned Tyranitar permits Swamp a self-XAttack then Waterfall434–510, while Mien's Reckless HJK668–786 has its normal90% accuracy risk. Do not advertise BrickBreak as a guaranteed unboosted Ttar KO326–384 into360HP.

## Scope and handoff

Owned Ludicolo90 needs normal Surf/Scald teaching and lacks immediate Ice coverage; it does not improve this proposed singles plan enough to displace the established counters. Ampharos85→90 adds Electric/LightScreen but faces widespread Ground attacks and Gyarados's WacanBerry. Neither is needed for this chain. Cryo remains a useful reserve and future specialist.

If preferring a fast Cryo build later: Timid alone gives253. Three Pomeg berries remove60HP EV (installed berries remove20 each), and two normal KOs with PowerAnklet add32+28 Speed EV, moving142→202 for267Speed/307HP. The berries cost1500 total at Store2F; Anklet15000 at Circus355E83 avoids sticker locks. This alternative consumes the one mint and is **not** part of the Cofa-mint recommendation.

Archive rule remains settled: record the entire route and both fights, including failures, in the full journey. **Only Solaris belongs in the major compilation; Howaya/Christina and street defenders are excluded.** Count attempts of the complete commitment honestly. Do not alter existing major configs122–124. After victory, normal save/native checkpoint before continuing Hardy prep.
