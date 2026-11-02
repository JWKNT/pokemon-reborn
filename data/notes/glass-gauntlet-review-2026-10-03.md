# Glass gauntlet strategy and archive review — 2026-10-03

This is a static, read-only prebattle review. No game input, save alteration,
live battle log, AI choice or RNG inspection was used. The baseline is
`Glass-10AM-paused-status.json`; later normal preparation/checkpoints take
precedence. Installed Reborn19.5.43 takes precedence over the walkthrough.

**Critical correction after source/UI review:** Xitems affect only the Pokémon
whose action opens the bag. Arcanine cannot use an Xitem on Klinklang.
`Battle_Scene.pbItemMenu`3359 sets `retindex=index` for battleitems;
`Battle.pbRegisterItem`1998 registers that actor's item action. Ordinary Xitems
do not skip the allied partner's action: the skip is only for items having the
separate `UseInBattle` handler, such as balls. Potions/Full Heal/Revive have the
party target menu, so the partner can heal an ally. All plans below use legal
self-Xitems. The earlier proposed allied-Xitem openers are superseded.

## Entry and fixed six

Installed734E12 page0 calls Shelly version3 plus Cain version6, **six Pokémon
each**, in a12v6 doubles battle. Those numbers are trainer versions, not party
sizes. Page1 then calls QMARK0 (Luna, singles), `pbPartialHeal`, and QMARK1 plus
QMARK2 (Radomus/Serra,12v6 doubles). Win all three consecutively without saving,
reloading or changing the roster between rounds.

The six owned Lv90 Pokémon remain suitable: Arcanine, Klinklang, Excadrill,
Swampert, Cofagrigus and Mienshao. Lead **Arcanine/Klinklang**, obtained through
normal party menus before the entry checkpoint. The paused save has Excadrill
fainted, Arcanine200/294 with only6 Flamethrower PP, and Mienshao176/228 with
2 High Jump Kick PP. **Use the normal healing machine before entry.** Full HP
alone is insufficient: verify PP recovery as well.

Keep Charcoal on Arcanine, Wide Lens on Klinklang, Protective Pads on Mienshao,
and Spell Tag on Cofagrigus. Giving owned Wave Incense to Swampert instead of
Exp.Share is an optional legal improvement; record the actual entry build if
changed. Mienshao's fourth move is **Brick Break**, not U-turn. Excadrill has
Earthquake/Rock Smash/Rock Slide/Swords Dance.

After round1, event code314 invokes `pbHealAll`: full HP, status, PP and revival
with Nuzlocke off. After round2, `pbPartialHeal` restores **living Pokémon's HP
and status only**; fainted members remain down and PP is not restored. Prefer
no allied faints in round2. The single owned Revive can recover an emergency
faint through normal controls, but the current conservative archive proof
will then require additional real carryover evidence rather than accepting a
blanket no-faints assumption.

## Exact Factory mechanics

Installed `fieldtext.rb`971–1023 gives Gear Grind2× damage and Electric1.5×.
Fire has no general Factory bonus. `Battle_MoveEffects.rb`1643 gives Shift Gear
**+2Attack/+2Speed** on Factory. X Defend/X Sp.Def/X Sp.Atk/X Speed each give
two stages in this build (`ItemEffects.rb`3279 onward).

Avoid unnecessary Earthquake/Discharge: they change Factory into Short Circuit.
Short Circuit gives Gear Grind1.5× and changes it to Electric, so Ground types
can become immune; its Synthetic Seed also differs. A Factory Synthetic Seed
gives+1Sp.Atk and Laser Focus. Vivillon, Mismagius and Jynx can therefore land
dangerous critical hits if allowed a damaging turn.

Wide Lens does **not** make Gear Grind certain: the installed accuracy formula
floors85×1.1 to **93%**. Gear Grind makes one accuracy check for the two-hit
move, not one for each hit. Twelve uses at93% have only~42% probability of no
misses. Reserve the two owned X Accuracy for Klinklang in rounds1 and3.
X Accuracy's+2 accuracy stages exceeds100% even after Snow Cloak's0.8 hail
modifier, unless additional unreviewed evasion effects intervene.

Cofagrigus's Trick Room lasts **five turns on Factory** with Spell Tag. Eight
turns require the installed Psychic Terrain/Chess/New World condition or an
Amplifield Rock. Do not combine Trick Room casually with a fast boosted
Klinklang; reserve it for a slower backup plan if the sweep collapses.

## Round1: Arcanine supports Klinklang

Suggested opening, adapting if an actual critical hit/target change alters HP:

1. **Arcanine self-XSpeed; Klinklang self-XDefend.** Both items occur before
   attacks, and each partner still has its own action. Arcanine's entry
   Intimidate reduces Marowak's ordinary physical damage.
2. Arcanine now352Speed uses Flamethrower on Ribombee before its310Speed action;
   Klinklang uses Shift Gear. Flame still KOs through Light Screen226–265 vs214HP.
   If Arcanine is at121HP or less after turn1, use Klinklang's action to Ultra
   Potion **Arcanine**, delaying Shift Gear: Marowak Shadow Bone can do120.
3. Arcanine's fast Flamethrower eliminates Vivillon through Light Screen
   (295–347 vs243HP), preventing Sleep Powder/seed critical Hurricane. Klinklang
   heals itself if at102HP or less; otherwise it can self-XAccuracy, or take
   the delayed Shift Gear when actually safe. Do not force a nonheal action
   while another ordinary Marowak Fire Punch can KO it.
4. Heal as needed from Arcanine's action; boosted Klinklang removes Marowak.
   Finish Klinklang's self-XAccuracy at a safe opportunity if not already used.

This order intentionally keeps Marowak alive while the two first Shelly Pokémon
are removed; therefore Meowstic cannot yet enter with Rain Dance. It also lets
fast Arcanine eliminate Vivillon itself, freeing Klinklang's action for healing
or setup. Exact HP and any unexpected switch still take precedence.

Klinklang's+2Speed is374. Ribombee is310, Meowstic264, Vivillon222 and Nidoking224.
Arcanine starts176; its own X Speed produces352, but Sticky Web can alter that
round1 stage calculation. Clear Body protects Klinklang from Web/Icy Wind stat
loss. Scolipede262 becomes393 after one Speed Boost; target it promptly or give
Klinklang another X Speed/Shift Gear before it gains too much momentum.

The primary risk is Marowak's **critical Fire Punch**: it ignores Intimidate
and positive Defense and does~383–450 to Klinklang275HP. A round1 Klinklang faint
does not invalidate the full chain because the scripted full heal revives it.
Healthy Swampert's Waterfall and Excadrill's Rock Slide are the recovery tools;
Mienshao's Wide Guard protects spread attacks. Use Earthquake only if its
immediate benefit outweighs abandoning Factory.

For ordinary hits, Ribombee's Pollen Puff can do62 to Klinklang, exceeding its
spread Dazzling Gleam42. With Marowak Fire Punch102, Klinklang can be as low
as111 after turn1 and9 after turn2; the turn3 self-heal is essential in that
case. Arcanine can be109 after turn1 from Shadow Bone120 plus Pollen Puff65;
the conditional turn2 allied potion above prevents a second Bone knockout.
These bounds do not protect against critical hits or an unexpected move effect.

Meowstic can use Rain Dance/Reflect. Do not assume Arcanine still one-shots
Ribombee through **rain plus Light Screen**, and avoid re-entering Intimidate
against Competitive Meowstic without accounting for the special-attack boost.
Prioritize dangerous Fire/Ground users and Sleep Powder with Klinklang; use
Arcanine's spare turns for healing/buffs. Primarina's Water Hyper Voice, Nidoking's
Earth Power and Volcarona's Heat Wave demand actual HP/target review.

## Round2: safe special Arcanine setup

Weavile has Icicle Crash/Poison Jab/Brick Break/Night Slash, no Low Kick or
Superpower. Use it as the setup opportunity, preserving the other five.

Recommended order: X Defend, **X Speed early**, second X Defend, two X Sp.Def,
then three X Sp.Atk, inserting healing/status cures when needed. Do not boost
Attack: Gothitelle and Umbreon have Foul Play. One X Speed makes Arcanine352,
above Weavile319, Mismagius286 and Mega Absol308. Before that speed boost,
Weavile moves before Morning Sun; use a priority bag heal if HP is threatened.

Keep Arcanine roughly180HP or higher before a nonhealing setup action. Night
Slash's critical hit can do126–149 even after Defense boosts; Poison Jab can
add poison chip. Ultra Potion restores **200HP**, not a full heal. After the
speed boost, Morning Sun normally restores147HP before Weavile attacks. A
status cure alone can still leave Arcanine in range of the next attack; handle
HP before poison if necessary.

At+6Sp.Atk, Charcoal Flamethrower KOs every unboosted target. Weavile's Focus
Sash needs a second hit; Extreme Speed can finish1HP without allowing another
ordinary attack. Mismagius must be outsped and KOed before its seed-focused
critical hit. Umbreon's damage margin is narrow: **344–405 vs340HP**, so verify
Charcoal has not been lost and do not casually lower the special setup.
Protect consumes PP but24 starting Flamethrower PP affords room for the entire
round and a useful round3 reserve. All enemy trainer bags in the reviewed
three rounds are null.

## Round3: rebuild Klinklang, retain living party and PP

Stat stages reset between battles. Luna's Arcanine boosts do not carry into
round3. The opponents lead Clefable and Alolan Ninetales; Ninetales starts hail.

Suggested first turn: **Arcanine self-XSpeed; Klinklang self-XSp.Def.** Clefable's
Fire Blast is special: X Defend is the wrong opener protection. Without a
boost it does163–192 to Klinklang; X Sp.Def reduces that to83–98.

Turn2: fast Arcanine Flamethrower Ninetales; Klinklang Shift Gear. If Nine used
Veil on turn1, Flame does180–212 and leaves10–42HP, but Nine caused no turn1
damage. If Nine attacked on turn1, no Veil and fast Flame KOs before its next
attack. Under those ordinary-hit branches, Klinklang survives two turns with
at least20HP. On turn3, Arcanine uses Ultra Potion on Klinklang while Klinklang
Gear Grind removes a surviving Ninetales, or Clefable if Ninetales is already
gone. If actual paralysis interrupts the setup, cure it with the partner's
Full Heal before continuing. Do not let theoretical turn numbers override the
screen.

Once Sandslash is present, Arcanine's352Speed narrowly exceeds Slush Rush350;
Flamethrower is4× effective and can eliminate it while Klinklang attacks the
other lead. After the leads are cleared, Klinklang can **self-XDefend** for the
physical replacements, then **self-XAccuracy**. Arcanine spends those setup
turns healing it or removing an urgent threat. Keep a potion reserve; both
buffs consume Klinklang's own action and cannot accompany its Gear Grind.

Then eliminate Clefable before repeated Fire Blast/Thunder Wave. Cofagrigus
cannot stop Thunder Wave aimed at Klinklang; Full Heal is an ordinary emergency
option. Brick Break removes Aurora Veil when Mienshao can enter safely. Wide
Guard blocks Blizzard/Dazzling Gleam/Rock Slide/Hyper Voice, but not Psychic,
Fire Blast, Freeze-Dry, Thunderbolt or a Z-move's full residual damage.

Boosted Gear Grind handles most foes even through Veil. Bronzong, Bisharp and
Metagross resist Steel; use Arcanine's Flamethrower and/or a second Shift Gear.
Arcanine is slower than Slush Rush Sandslash350 without its own speed help;
Klinklang374 outruns it after one Shift Gear. A second Shift Gear produces
Klinklang561Speed and+4Attack on Factory. Do not re-enter Arcanine casually
against **Defiant Bisharp**: Intimidate triggers its boost. Save a healthy
Cofagrigus/Swampert/Excadrill recovery option if the main pair loses momentum.

Alakazam can replace Factory with Psychic Terrain; stop assuming Factory
damage after that occurs. Jynx's Synthetic Seed is dangerous if Factory is
still active. Froslass has Destiny Bond; boosted faster Klinklang can normally
KO it before the initial Bond, but observe whether a previous Bond is active
before attacking. After a Bond, let it expire through a safe nondamaging turn
or accept the final-round trade only with enough surviving teammates.

## Numerical evidence

`scripts/glass_damage_review.py` is a standalone read-only planner. It uses
the exact installed trainer EV/IV/nature/form tables in `work/glass-*-teams.json`,
the selected static species metadata in `work/glass-species-stats.json`, and
the native baseline numeric stats. It reproduces the installed final damage
formula for **explicitly supplied modifiers**; it does not simulate AI choices,
RNG, all field interactions or every move. Output: `work/glass-damage-review.json`.

| Reviewed move and state | Damage range | Target HP |
|---|---:|---:|
| Intimidated Marowak Fire Punch into Klinklang+2Def |87–102|275|
| Marowak critical Fire Punch into Klinklang |383–450|275|
| Klinklang+2Atk Factory Gear Grind, two hits, Marowak |262–310|254|
| Charcoal Flamethrower, Ribombee with Light Screen |226–265|214|
| Same attack with Rain too |113–133|214|
| Charcoal Flamethrower, Vivillon with Light Screen |295–347|243|
| Factory-seeded Vivillon critical Hurricane into Arcanine |312–367|294|
| Weavile critical Night Slash into Arcanine |126–149|294|
| Arcanine+6Sp.Atk Flamethrower, Umbreon |344–405|340|
| Clefable Fire Blast into unboosted Klinklang |163–192|275|
| Arcanine unboosted Flamethrower, Ninetales with Veil |180–212|222|

## Archive readiness and implemented corrections

Reserved major IDs122/123/124 retain the title **Glass Gauntlet**, round1/3,
2/3,3/3 labels and one shared whole-gauntlet attempt total. Full journeys retain
every attempt; only the final consecutive winning chain enters the major video.
Every round's item totals remain exact `[Player used ...]` counts from that
round's **completed** native log, excluding menu selections, held effects and
enemy usage (`count_battle_items.py`). No active battle log was inspected.

Fixed actual pre-entry archive blockers:

- `glass_continuity.py` and `complete_glass_archive_chain.py` formerly indexed
  `row['id']` across historical rows. Sessions061/062 have valid old rows without
  that field; both scripts would raise KeyError. They now use `.get('id')`.
- `major-122.json` uses `intro_name: Cain`, avoiding the brittle combined
  `Cain & Shelly` string when the actual introduction puts Shelly first.
- All three configs now reference the existing **Gym17 progress journey**;
  a finalGym17 file does not exist until Hardy. If the journey is promoted
  before these rounds are staged, update the source path deliberately.
- `glass_continuity.py` admits nonconsumable Wave Incense. It nulls round3's
  derived PP fields rather than falsely claiming Luna's used PP was restored.
  Numeric stats remain explicitly labelled pre-chain; panels use unchanged
  species/form/level/ability/item/four moves. These are archive-only records,
  never game/save writes.
- The completed-chain gate now verifies all three battle-entry party panels
  are identical fixed Lv90 sixes, all round1 attempts have actual observed
  intros, no duplicate opener timestamps, and no F12 within the winning chain.
- Installed `Pokemon.setGender` forces female Meowstic to form1. The trainer
  export and pending opponent roster122 now show **Female**, with the correct
  sprite row, rather than the omitted-form default Male. Historical published
  panels were not silently changed.

The existing renderer supports these12v6 rounds with **three trainer columns**
(one player trainer controls both allied battlers). Its source-order reversal
should give **Our team | Cain | Shelly** and **Our team | Serra | Radomus**.
Verify ownership against the recorded visible left/right sprites; save any
explicit `roster_screen_order` if the actual footage differs. Preserve sprites,
types and full builds. There is no NPC partner in this gauntlet.

`major_enter`/`major_attempt` continuity criteria match the reviewed normal
chain when the pre-chain native checkpoint is unchanged and fresh. Round2
permits prior faints after proven full revival; round3 currently requires no
Luna faints. A normal Revive after a Luna faint makes the actual game playable
but will be refused by this conservative zero-faint proof until reviewed.
Do not bypass the check or invent an HP/build snapshot. Creation ages remain
<120s at each inter-round entry; use the **fresh healed entry baseline**, not
the10AM snapshot. Intro/outro work must finish before falsely anchoring the
next round's audio/attempt to the previous victory screen.

Validation: Python compile for changed archive scripts and calculator; Ruby
syntax check for the exporter; valid JSON/current source existence checks.
A temporary metadata-only fixture exercised five cases: valid three-win
chain with one earlier opener loss plus an idless legacy row (shared2attempts),
and rejection of an intervening reset, changed round3 build, failed round3,
or missing opener-intro evidence. All five passed. Fixture files were removed.
No live Glass chain has yet validated these helpers; preserve pending source
footage with `--keep-sources` until **all three** clips plus the full journey
have been published, decoded and visually checked.

Primary mechanical sources are the installed `734E12` event and
`Scripts/{Trainers.rb,Pokemon.rb,Utilities.rb,ItemEffects.rb,Battle_Move.rb,
Battle_MoveEffects.rb,Battler.rb,Reborn/fieldtext.rb}`.
The [BigJRA Glass walkthrough](https://bigjra.github.io/reborn/#glass-workstation)
supports planning all three rounds and maintaining doubles momentum; exact
local mechanics and team data above control this run.
