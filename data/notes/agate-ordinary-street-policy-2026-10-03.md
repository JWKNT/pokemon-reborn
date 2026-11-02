# Ordinary Agate street fights — installed 19.5.43

Source-only plan. These are ordinary fights, not curated major-video additions.
Parent-reported/frozen Lv90 stats are used; current HP/status/PP/item stock must
come from ordinary public screens. No AI, future random outcome or live state is
assumed. Calculation: `scripts/agate_street_review.py`; static teams/species are
`work/agate-{antoine,lyla,ezra}1-static-roster.json` and
`work/agate-street-species-static.json`. Default source trainer nature Hardy,
IV10/EV85 each, no held items and no trainer medicines.

## Antoine1 — 763 E49, single, No Field + regional weather

Mamoswine86 / Lurantis86 / Liepard87 / Mightyena88 / Tyranitar88. CF
252/93/333/210/218/68, Mummy/no item, TR0/Hex1/Wisp2/DP3.

Mamo Earthquake normal73–86, crit109–128; at +2Def ordinary37–44, crit unchanged.
Hail CF15: preburn min144 for one incoming hit and residual. XDef pilot, XAccuracy
(+2), Wisp then root-selected setup. SnowCloak Hail multiplies accuracy .8;
+2 accuracy makes85%-Wisp floor113%, so no accuracy miss under unchanged source
conditions. Burned EQ crit55–64: min80 including Hail. Three XSpecial (+6) and
three XSpeed (+6 =>272Spe) permit the intended sweep; use guarded finite queue
with public status/weather/foe changes stopping it. Never replay pending input.

+6 Hex: Mamo397–467 vs311, Lurantis287–338 vs243. Kill Lurantis immediately:
Contrary LeafStorm raises its SpA by2; a boosted crit becomes331, lethal to CF.
Liepard Hex225–265 vs235: while Hail continues, any≤10 remaining dies to14chip.
Prankster Swagger precedes CF, adds confusion and +2Atk. Its FoulPlay critical
max95/180/266/351 at CFAtk stages0/+2/+4/+6 respectively; FullHeal clears
confusion but preserves Attack boosts. Stop/review actual Swagger/Substitute/
confusion; do not automatically add a Wisp turn. FakeOut cannot hurt Ghost CF.
Mightyena burn-Hex387–455 vs248, guaranteed KO. Tyranitar SandStream changes
weather and supplies1.5SpDef: burn-Hex171–201 vs301 requires2 hits. Wisp first
while CF remains faster; do not reuse unburned low-HP thresholds. Burn damage
does not reduce Liepard's Prankster status priority.

## Lyla1 + Ezra1 — E45/E46, double

Lyla: Noivern/Whimsicott/Wigglytuff/Haxorus87. Ezra: Ditto/Bellossom/Mantine/
Kommo-o87. Trigger overlap42,56..59 combines them normally (Trainers.rb255+).
Exact event geometry belongs to the route agent; do not advance through another
trainer or the Agate true-chain story trigger blindly.

**Prefer Cryo first, Mien second, full HP, then heal afterward.** Installed
Imposter (Battle.rb3240) copies opposite battler via index^3 (Battler.rb1247),
so enemy Ditto3 copies owned Cryo0. Actual frozen south-ready130 Cryo moves are
LightScreen/IceBeam/Recover/FreezeDry (not the older Haze build). Transform copies
nonHP stats/moves/stages/ability, each move5PP; keeps Ditto's207HP and name
(`Battle_Effects.rb903`).
Do not lead CF first: Noivern Hurricane crit167 + copiedCF Hex crit212 +Hail15
can defeat full252CF even after XSpDef, since crits ignore positive defense.

T1 Mien FakeOut **Ditto**, Cryo IceBeam **Noivern**. Ditto copiedCryo does not
have FakeOut. Noivern245 acts before Cryo207; its Hurricane crit119–140 or
spread HeatWave crit103–122 cannot defeat full320Cryo. IceBeam428–504 defeats
271HP Noivern. Hurricane confusion/Swagger may still interrupt the attack;
public observation governs any retry. A hit can break full-HP Sash protection
but does not consume the held Sash unless it actually prevents lethal damage.
Mien may faint to Noivern Hurricane after its FakeOut action; choose a free
replacement from actual visible results, not an assumed T2 pair.

If healthy, unstatused Mien remains: T2 BrickBreak Ditto281–330 vs207HP,
Mien217 > copiedCryoDitto207. Whimsicott233 acts before Mien; its spread Dazzle
crit192–226 means **full228** Mien lives to BrickBreak, possibly faints toHail
afterward. Any lower HP or paralysis needs a different branch. Cryo self
XSpecial T2 is useful: +2 IceBeam Whim446–525, even LightScreen297–350 vs228.
Unboosted IceBeam224–264 can miss by4. Ditto can use LightScreen or Recover if not
defeated; confirm its KO before relying on a short sweep. Whim can StunSpore/
LightScreen/LeechSeed; ordinary FullHeal/partner medicines are legal but root
must choose them based on public evidence.

Then use actual foe pairs. +2 IceBeam: Bellossom352–414 vs254, Haxorus472–555
vs256, Kommo-o339–399 vs254; under LightScreen Kommo226–266 is no longer a
guaranteed OHKO. FreezeDry Mantine413–486 at+2 vs271 (4x, unlike IceBeam).
Wigglytuff +2 IceBeam305–359 vs367 is2 hits; its normal HyperVoice cannot hit
CF. Mien WideGuard protects the party from Noivern Boomburst/HeatWave,
Whim/Wiggly Dazzle, Wiggly HyperVoice/IcyWind, Haxorus EQ and Kommo-o
ClangingScales, but not Hurricane/Outrage/CloseCombat/PoisonJab/Scald/AirSlash.
BrickBreak can remove LightScreen; do not HJK Fairy Whim or assume Wiggly is
Fighting-weak (Normal weakness and Fairy resistance cancel to neutral).

## Guarded wrapper support

`agate_public_action.py --mode antoine` defaults Mamoswine single.
`--mode lylaezra` defaults Noivern,Ditto double and uses the unchanged OWN Q
numeric-HP proof before/after. Actor remains CF only; Cryo/Mien ordinary actions
use existing move/item helpers under root control. Both new modes are accepted
by `agate_finite_items.py`. Fresh actor, exact foe sets, requested numeric HP,
target geometry, capture-health, pending journals and no-replay guards remain.
21 wrapper/finite synthetic tests and3 tactical numeric tests passed; no UI run.
