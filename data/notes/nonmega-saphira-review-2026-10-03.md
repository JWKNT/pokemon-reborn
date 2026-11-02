# Future non-Mega Saphira fallback — installed-source review

**Proposal only; nothing trained, obtained or executed.** Reads installed source/extracts and historical Glass-post-gauntlet Swampert IVs only. No controls, runtime, live save/logs, opponent AI/PP or active recordings were read. Calculator: `scripts/nonmega_saphira_review.py`; full tables: `work/nonmega-saphira-damage-review.json`. Five pure mechanic fixtures and syntax checks pass. Existing Mega/route notes remain unchanged.

## Better practical primary: Impish AV Swampert

Independent follow-up validates **Impish95 EV[252,0,100,0,52,104] → 363HP/242Atk/232Def/155SpA/197SpDef/160Speed**, effective AV SpDef295.5. Outgoing attacks and speed are unchanged from the Careful tables below. This is the preferred AV build if choosing the normal non-Mega branch: it trades some Noivern comfort for survival against the two **unboosted** Sash dragons' criticals.

|Incoming move|Ordinary at +0SpDef|Ordinary at +2SpDef|Ordinary at +6SpDef|Critical despite +6SpDef|
|---|---:|---:|---:|---:|
|Seeded Noivern DragonPulse|186–218|94–110|48–56|278–327|
|Seeded Noivern Boomburst|136–160|69–81|35–41|204–240|
|Seeded+FlashFire Flamethrower|98–116|50–59|26–30|147–173|

Use **HP>330** for Noivern while its DragonPulse remains; after ten public uses, **HP>245** covers remaining criticals. Heal fully before the first exposed setup. One XSpDef first still helps; ordinary+2SpDef DragonPulse can leave253, so the larger325/330 critical guard generally calls for more healing than Careful. No premature setup queue is certified.

On first Sash strike, require enemy Attack/Speed still+0 and **HP>337 for Salamence / HP>355 for Haxorus** (small margins over source base critical ceilings334/351). If that strike leaves1HP and the foe used DD, +6Speed640 is still faster than one field DD: **kill next command without an extra heal**. If it attacked unboosted, the guarded HP survives its source critical and the next command also kills. Neither dragon has priority. Actual enemy FullRestore uses its own turn; Sash remains consumed. This establishes those individual two-command branches, not a blanket whole-fight guarantee.

Do not silently assume the HP guard at the next dragon: the preceding opponent may have damaged Swamp, and **healing on a new Haxorus turn can let it DD before our first strike**. Then boosted criticals are no longer covered (Hax +2Atk DragonClaw594–699 into this build). Garchomp lacks DD and its base maximum critical DragonClaw324 / EQ270 can be survived at fullHP while healing, but the post-heal damage does not restore a guaranteed Haxorus opening guard. The practical plan must inspect that exact transition and accept a reviewed contingency/critical risk if the clean guard is absent. Free-entry priority and normal Revive are backups; no guaranteed unbroken solo sweep is claimed.

For all medical/physical tables not explicitly marked Impish below, the original **Careful** calculation is retained as a comparison, not the recommended physical build. Source report now contains both named builds. Ring+Mega is still a valid normal alternate preparation; the AV branch avoids assuming a Ring, but does not erase every critical/setup risk.

## Careful comparison and common prerequisites

**Careful Swampert95 with Assault Vest is a practical normal-control fallback**, but not a certified solo sweep. EV `[252,0,0,0,152,104]`, historical IV `[9,30,12,7,10,18]` gives **363HP / 242Atk / 187Def / 155SpA / 243SpDef / 160Speed**. Vest contributes **364.5 effective SpDef**, including on critical hits; it is not rounded to364 before the installed final calculation. +6Speed is640, narrowly above one Dragon's Den DD Charizard-X638, Salamence630, Haxorus610; above ScarfGarchomp480 and Noivern360. Fresh measured stats, nature, EVs, full HP/PP, Vest and actual medicine stock govern execution.

Replace Protect with an ordinary attack: **Earthquake / RockSlide / Surf / Waterfall** is sufficient. AV prevents status **moves**, not normal self-target X items or Bag healing (`Battle.rb:1271`; `ItemEffects.rb:3230–3479`). Surf is utility; **do not use it twice** while preserving Dragon's Den. No automatic offensive action should silently change the field.

AV ownership is **not assumed** (another agent reports frozen post-Hypno bag0). Normal installed pickup: **Underground Railnet602 E17[17,7]**, `Kernel.pbItemBall(:ASSAULTVEST)`, then self-switchA hides it. Restored Railnet519 E215–219 at[59,13..9], page1 requires **switch652**, transfers right-facing player to602[1,15..11]. Return602 E1–5 left edge[0,11..15]→519[58,9..13]. Item-page and entry extracts are `work/nonmega-saphira-assaultvest-events.json` and `work/nonmega-saphira-av-route-source.json`. Verify uncollected self-switch and route normally; this is source availability, not proof it is currently reachable/uncollected. The other Vest rewards are782 Victory Road PC and827 Nightclub, so do not assume those solve pre-Saphira stock.

**Current funding prerequisite:** the sibling's explicitly frozen post-Hypno128 navigation has652false, so this pickup is currently locked. Its complete installed entrance scan found only the restored519 entries. Normal pre-Saphira unlock is GrandHall38 E37 **Railnet Reconstruction**, base100,000 funding; the source counter for a partly funded project's remaining amount must be proved in its ordinary UI, not interpreted as zero/free. Frozen money74,180 would be25,820 short if the project is wholly unfunded. See `work/mega-ring-railnet-funding-source.json`. The later postgame Lumi setter does not establish a present route. AV setup therefore includes normal funding/earnings as well as pickup and training.

Stock true full healing (MaxPotion/FullRestore), normal status cures, Revives and each planned X item before tournament commitment. UltraPotion200 cannot always restore the HP guard after a critical. A practical budget is approximately20–25 full heals, including contingency rather than a claimed exact consumption count. None is assumed currently owned.

## Noivern opening: substantially safer than bare Swampert

Installed Noivern95:296HP/278SpA/360Speed; ElementalSeed gives **+1SpA (417)** plus FlashFire. Infiltrator bypasses screens. Dragon's Den boosts Dragon/Fire1.5; FlashFire independently adds1.5 to Fire attack. AV remains active when criticals ignore positive SpDef stages.

|Attack|Ordinary, +0SpDef|Ordinary, +2SpDef|Ordinary, +6SpDef|Critical, even +6SpDef|
|---|---:|---:|---:|---:|
|DragonPulse|151–178|77–90|40–47|227–267|
|Boomburst|111–130|56–66|29–34|166–195|
|Flamethrower|80–94|40–47|20–24|120–141|

Lead full-HP Swamp. **Use one XSpDef first**, then inspect actual damage before each next command. While DragonPulse remains usable, require **HP>270** before an exposed setup/attack; priority full-heal otherwise. It survives the source maximum critical from that guarded HP. Ordinary unboosted hit could leave185, so heal before trying the second setup action. At +2SpDef, full363→worst ordinary90→273 leaves room for one further guarded action; after another ordinary hit inspect/heal. Do not chain setup after an unobserved critical.

Build the necessary **three XSpeed, three XAttack, three XDefense, one XAccuracy** on Noivern, raising SpDef farther only if healing budget/observed damage calls for it. Each standard X item gives two stages. Visible Defog reduces our evasion, not accuracy stages. Noivern offers no recovery, recoil or status move; it will not be damaged while setting up. Guard Struggle/visible PP exhaustion; avoid unnecessarily extending setup to exhaustion. Counting ten public DragonPulses permits the lower **HP>200** critical guard afterward, but PP must be counted from visible move messages, never queried at runtime. Burn from Flamethrower requires an ordinary status cure/full restore before physical finishing; cure costs a turn and needs the HP guard.

## Finishing sequence and the real limits

These are source core/modifier ranges at +6Atk, unchanged Dragon's Den:

|Opponent|Attack / damage|HP|Branch|
|---|---:|---:|---|
|Noivern|RockSlide411–484|296|One landed hit; require +2accuracy first.|
|Salamence|RockSlide406–478|319|Full-HP Sash leaves1HP; second landed hit needed.|
|Garchomp|EQ352–414|344|Guaranteed minimum exceeds HP by only8; actual attack≥242 and no reduction required.|
|Haxorus|EQ372–438|279|Full-HP Sash leaves1HP; second EQ needed.|
|MegaCharizardX|EQ612–720|289|One hit; prove Mega form/grounded Dragon-Fire typing before assuming Ground connects.|
|Dragonite|RockSlide169–199 at fullHP;338–398 after Multiscale breaks|386|Iapapa and three team FullRestores prevent a promised two-hit finish; Curse insurance preferred.|

**Heal before the initial Sash hit; minimize extra turns afterward.** At +6Def, Salamence/Haxorus ordinary DragonClaw is≤72/74 unboosted, ≤140/146 after one DD; full363 survives one ordinary exposed turn. +6Speed remains faster after **one** field DD, so the next attack can finish the visible1HP survivor. Source Haxorus uses **PoisonJab**, not GunkShot.

The Sash turns remain real critical risk: criticals retain enemy positive Attack while discarding our defensive stages. At full363, Salamence unboosted DragonClaw critical353–415 can KO; Haxorus370–435 always KOs. After one field DD (+2Atk), corresponding criticals700–824 /737–867; EQ critical456/482 can also KO. **No HP threshold makes those boosted criticals safe with this build.** Do not describe XDefense as protection against them. A second DD gives speed945/915 and invalidates the planned speed edge. Healing/other extra turns can allow that extra DD; observe stages/messages rather than assuming one. Enemy FullRestore at1HP uses its turn; the consumed Sash stays consumed, so another full-HP lethal hit can finish if our attack still meets the table.

Garchomp has no DD: avoid spending an exposed turn on it; immediate EQ is the safer action. Its unboosted DragonClaw critical341–402 can KO full363; EQ critical285–335 is survivable at fullHP. CharX unboosted contact DragonClaw critical448–527 (ToughClaws1.3) already KOs; immediate EQ before it moves is preferable to trying to heal against it. The640 versus638 speed edge is only two points and does not survive a speed drop or second DD.

If Swamp actually falls leaving a visible1HP Sash opponent, a **free replacement** with normally taught priority (Arc ExtremeSpeed or Mien FakeOut) can clean up; inspect remaining HP, priority, source move legality, and enemy FullRestore inventory. An enemy full heal before priority may prevent that cleanup. Do not promise a hot switch preserves Swamp's boosts. Regular Revive/rebuild is a contingency, not the original sweep continuing unchanged.

For Dragonite, preserve a **full-HP Cofa/intact normal FocusSash** with Ghost Curse and a living reserve. Its free entry after a real Swamp faint can apply Curse through a single hit; ExtremeSpeed is immune, and the half-HP Curse cost may sacrifice Cofa after applying it. A hot switch consuming Sash before the next turn is not equivalent. Require visible Curse effect, then stall ticks with legitimate heals/revives while tracking berry/FullRestore healing. Sash ownership is another explicit prerequisite (frozen post-Hypno bag0 is not an available Sash); optional ordinary Scarborough/penthouse purchase requires its own completed normal quest. Alternate Perish backup likewise needs actual surviving singer/PP and a living bench. Do not start the locked chest/Steelix/Saphira preparation on assumed items.

## Sylveon/Misty/Cryogonal alternative

Misty changes the entire field for5 turns or8 with a real AmplifieldRock (`MoveEffects.rb:8389`); it cannot refresh while already active. Defog may remove it to Indoor, and timer expiry restores the backup. Never queue actions against a presumed refreshed field. Fairy immunity to Dragon is useful, but a HP+Defense Sylveon has an unsafe Den opening: even a worst-IV Bold95 HP252/Def252 build's345HP can be exceeded by seeded FlashFire critical Flamethrower (~404). Special bulk or an independently proved opening guard is necessary. Calm95 HP252/SpDef252 has guaranteed minimum345HP/342SpDef even IV0, and its source maximum seeded Den Flamethrower critical is below300; this is a possible normal bulky lead, not a trained roster claim.

Cryo's IceBeam gains value after Misty/Indoor/Cave removes Den penalties, but the original six's exact future95 Cryo stats were not supplied here; no numerical solo sweep is certified. Opponent Steel/Poison coverage, finite terrain turns and setup crits remain. **Two Surf field conversion to Cave introduces the second-EQ ceiling-collapse trap**; do not use a generic EQ sweep after conversion.

An attractive theoretical fresh-Misty BatonPass into Swamp would preserve boosts while covering the two Sashes. **The guaranteed Sylveon gift cannot currently be assumed to do this:** installed Sylveon natural/relearner list has no BatonPass; compatiblemoves alone is not a tutor. Reborn's ordinary reminder does not add Eevee's pre-evolution natural list. A separately acquired Eevee can normally learn BatonPass before evolution, but that is an extra unreviewed acquisition/training branch, so it is not the recommendation here.

Primary proof anchors: `Reborn/fieldtext.rb:1850–1913` (Den/seed), `Battle_Field.rb:953–964` (Dragon defense), `Battle_Move.rb:1785/1879/1947/1987/2078/2110/2212–2215` (stages/FlashFire/AV/crit/type/final rounding), `Battle.rb:1271` (AV status move gate), `MoveRelearner.rb:1–36` / `Pokemon.rb:324` (legal reminder), fixed `work/saphira-installed-team.json`.
