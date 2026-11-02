# Conditional Sylveon opening for Saphira

**Source-only future proposal, not executed.** A normally acquired and trained Sylveon is a useful Noivern counter without Mega Ring or Assault Vest. It does not establish a safe solo sweep or pass setup boosts to the next team member. All figures below use installed19.5.43 source and the named frozen source extracts; no live UI, save, AI, RNG, battle log or active recording was inspected.

## Normal gift and preparation

774E122 code **3862** unlocks1064; gift774E128[36,18] requires standing[36,19], facingUp,1064True/1066False and Yes. It gives **female Sylveon75, Wish/MistyTerrain/HealBell/Moonblast, RibbonCollar**. The gift has **zero EVs, random0–31 IVs, random nature and CuteCharm/Pixilate**. No perfect-IV or Calm guarantee exists. RibbonCollar is a quest clue with no battle protection; take it off normally. CuteCharm is sufficient: Moonblast is already Fairy, so no AbilityCapsule is needed for this role.

Recommend **Calm95, HP252/SpDef252/4Speed** after the actual17th badge makes HARDCAP95. Even all-zero IVs give **345HP/115Atk/128Def/214SpA/342SpDef/119Speed**. Mixed actual IVs must be measured after acquisition; the all-zero build conservatively bounds bulk and special offense. The role prioritizes one protected Fairy attack rather than racing Noivern360Speed.

Normal Calm methods: uncollected **CalmMint289E109[49,11]**; the one-use favorite-nature reward57E40[9,51] whenvar107≥8; or **SevenStreet psychologist326E3[13,7], active page1, two HeartScales**, Calm menuindex20. Do not assume any is currently accessible/uncollected. The2190 GrandHall mint package is not an authorized extra password reward.

Fresh zero EVs need **8 successful PowerWeight KOs +8 PowerBand KOs**, with normal held-item swap and actual EV verification between blocks. Installed power items replace the species yield with32 in only the named stat and cap252; a4EV SpeedWing completes508. Participant/actualExpShare EV rules matter; ExpAll alone gives no EVs to a nonparticipant. Vitamins also give32, wings4, with252/stat and510total limits. Candy itself adds no EVs: MediumFast75→95 needs435500EXP, normally15XL before existing EXP/modifiers. Train under the current90 cap first if acquired before Hardy; do not cross95 before badge17.

**Historical ownership only:** frozen `Void-Hypno-won-128-status.json` had PowerWeight1, PowerBand0, CalmMint0, HeartScale0, XL15, MaxPotion0, FullRestore0 and74180money. Later spending/training changes this. Circus **355E83[36,14] page0** sells PowerBand for**15000**; higher job-application page overrides when715True (frozen128715False). Check the actual merchant page and fresh money before purchasing. No normal CalmMint shop was found in the installed event scan. At17 badges normal default marts sell **MaxPotion**, but **FullRestore and Revive enter only at18** (`Mart.rb:735–741`). Buy MaxPotions plus status cures before tournament commitment; a200HP UltraPotion is not automatically a full heal for345+HP.

## Noivern numbers and a practical short opening

Installed Noivern95 is **296HP/278SpA/360Speed**, ElementalSeed/Infiltrator, with **Boomburst/DragonPulse/Flamethrower/Defog — no Roost**. Seed gives+1SpA and persistent FlashFire×1.5 Fire power. Sylveon is **immune to DragonPulse**. Noivern's Infiltrator bypasses LightScreen; criticals also bypass positive XSpDef stages.

Source-derived ranges against the conservative Calm build:

|Action|Dragon’s Den|Misty|
|---|---:|---:|
|Noivern seeded Flamethrower, critical|254–299|113–134|
|Noivern seeded Boomburst, critical|176–207|119–140|
|Flamethrower ordinary after one XSpDef|85–101|38–45|
|Sylveon unboosted Moonblast|176–207|339–399|
|Moonblast after one XSpAtk(+2)|347–408|673–792|

Misty removes Den's Fire×1.5, gives Fairy targets×1.5 special defense even against criticals, and gives Moonblast×1.5 base power. Den instead gives Noivern×1.3 Dragon defense. A normal unboosted Misty Moonblast comfortably exceeds296HP without needing Pixilate or an offense item.

1. **Start fully healed; use MistyTerrain.** Noivern acts first. At345HP/342SpDef this survives its strongest seeded critical299 plus a possible21HP burn tick. The general first-turn guard is actualHP greater than the Den critical ceiling +status residual +2 rounding margin. At345HP, a measured SpDef≥320 suffices for that single guarded setup turn; recommended342 provides more room.
2. At the next real command, inspect **actual field, HP, status and timer**. If Misty remains and SylveonHP>142 with no residual status, **Moonblast** can survive the reviewed140 critical ceiling before acting and OHKO. With burn add actualHP/16 residual (or cure it): do not reuse the clean-status threshold.
3. If HP is below that guard, normally **MaxPotion** first, then inspect again. A damaging attack while Misty remains leaves at least205HP from a345HP full heal, enough for the next guarded Moonblast if no unexpected condition intervenes. HealBell/FullHeal costs another enemy turn and one terrain turn; choose it only with a current HP guard. FullRestore is useful only if legitimately already owned.
4. **Stop the planned sequence on Defog, field expiry, foe change, a new status or ambiguous HP.** A Noivern Defog consumes its attacking turn, but may remove the Misty Moonblast boost before Sylveon attacks. Moonblast then only chips in Den; assess the new foeHP and the Den critical guard before another command. Re-establish Misty only from a state that can survive the pre-Misty enemy attack. A priority full heal can itself end at lowHP after a critical; it is not a guarantee that a following setup move is safe.

Misty lasts**5turns**, or8 only with an actually acquired/given AmplifieldRock. It **cannot refresh while already Misty**. `setField(:MISTY,temp)` preserves the current backing field, and Defog's Indoor change runs `breakField`, popping the top layer. Thus temporary Misty normally restores **backed-up Den**, not permanent Indoor; an actual Indoor backup would instead return Indoor. This install's baseDen table has no Defog field-change entry, and the Defog handler has no unconditional Indoor conversion, so first-turn Defog on baseDen does not itself establish an Indoor backup. Always use the observed field after any change.

Saphira has3FullRestores; that healing replaces her attack for the turn. The full-health Misty OHKO remains sufficient, but do not invent when she uses them. Moonblast can visibly drop SpA30%: recalculate if it happens rather than assuming it. Avoid a blind XSpDef→XSpAtk setup on Den: ordinary damage decreases, but the299 critical ceiling does not. A shorter terrain opening is preferable when its visible field/HP guards hold.

## Handoff and support limits

If an actual ordinary **Shift-style “about to send in” prompt** appears after Noivern faints, using that prompt changes our Pokémon without spending a separate attack turn (`Battle.rb:1766–1775`). Do not presume the configured style. An ordinary command-menu switch gives the next enemy an attack/setup turn; it passes **neither X boosts nor HP**. A genuine faint followed by replacement offers a fresh entry, but sacrificing Sylveon may also give a DragonDance/Moxie opportunity. Review the named incoming foe, public stages, field and remaining timer before either kind of handoff.

Misty reduces DragonDance to its ordinary+1/+1 and removes the Den Fire boost while active. It does not protect this special-bulk Sylveon against physical coverage: unboosted Garchomp IronHead critical444–522, Haxorus PoisonJab479–564, MegaCharX FlareBlitz652–767 **even on Misty**, versus345HP. No Fairy solo-sweep or casual physical hot-switch is certified. The existing Swamp/Cofa/other-owned-member plan still needs independent setup/entry guards after Noivern. A free entry does not transfer Sylveon's special-defense boosts to Swamp.

Wish heals the recipient's position next end-turn for**75% of Sylveon's maxHP when cast on Misty** (259 at345HP), otherwisehalf. It may support a real safe switch, but the recipient must survive the entry hit and the next turn until Wish resolves; it is not emergency priority healing or a protected handoff. HealBell retains general team-status utility. Keep these gift moves until a measured role justifies a normal reminder/TM change.

## Proof and validation

Gift/default anchors:774E122/E128; `Pokemon.rb:66–118,272,516`; `Reborn/montext.rb:45997`; `ItemEffects.rb:1704–1752,1898`; `Battle.rb:2558,2707`; `Items.rb:393`; `work/sylveon-normal-nature-source.json`. Field/damage anchors: `Reborn/fieldtext.rb:171–235,1850–1913`; `Battle_Field.rb:265–289,356–402,500–518,953–964`; `Battle_MoveEffects.rb:2136–2256,6089–6110,8389–8400`; `Battle_Move.rb:1877,1929–1947,2078,2110,2212–2215`; burn `Battle.rb:5532–5543`. Static rosters/species are `work/saphira-installed-team.json` and `work/saphira-capture-options-source.json`.

Pure calculator `scripts/sylveon_saphira_review.py` writes no state. Five bounded tests verify legal EVs, first-turn critical+burn survival, Misty OHKO versus Den failure, XSpDef critical bypass and actual backup popping/noRoost. Output is `work/sylveon-saphira-damage-review.json`. No new future battle config, save data, input queue or archive metadata was changed.
