# Fiore attempt 1 review — 2026-10-01

This is completed observation, not future AI/RNG inspection. Session089 major113 ended as a normal reset at the time cutoff. No victory; no major-video addition. Full journey retains all turns, mistakes, items, switch decisions and reset; decision-only menu idle time is removed. Saved party/supplies were restored by loading the verified outside checkpoint.

Before the next attempt, rebuild the plan. The previous plan cannot be treated as validated: enemy EVs were omitted from several speed/damage estimates. Gyarados is faster than our 155-Speed Cryogonal; switching or half-reviving Cryogonal into it is unsafe because Stone Edge can kill before Freeze-Dry. Ground Krookodile can arrive before Ampharos's queued Discharge. Arcanine's actual ability is Flash Fire, so it offers no Intimidate support.

The largest operator error was selecting Cryogonal's Recover(slot2) instead of Ice Beam(slot1) during Trick Room. It died to Haxorus before contributing. New battle_named_move.py resolves the exact saved actor/move ID; use it for variable actions. Do not assume slots across party members. Check a fresh command/target before queuing a new foe.

A second mistake was planning revives as full healing. Installed19.5.43 ItemEffects.rb confirms Cotton Candy and Funnel Cake restore HALF HP. Herbal Tea copies MAXREVIVE/full healing. Hyper Potion restores120; Ultra Potion200. Account for enemy attacks in the item-use turn and heal bench revives before switching when necessary. Do not repeat an automatic heal policy with an ineffective move on an asleep target or a .9 threshold that burns potions unnecessarily.

Round1 Diana/Kenan was won with Florinia, followed by automatic full engine healing. Round2 eliminated Walrein, Mamoswine, Haxorus, Krookodile, Roserade, Gyarados, Starmie and Scizor, but Florinia's six members and most of ours were lost. It ended with injured Cofagrigus facing Weavile/Rhyperior; Destiny Bond failed because Rock Slide flinched it. The reset was for the time cutoff, not a disguised recorded victory/loss.

Recorded defeated mons do not imply the remaining team was beaten. Blake still had Weavile/Alolan Sandslash; Fern still had Rhyperior/Decidueye. Round3 Solaris/John was never entered. Actual saved BeatSolaris183=true selects Julia for round3, not the alternative partner. All trainer-column sprites/builds must remain in any eventual successful major113/114 segment.

Potential revisions to evaluate before play: optimize Mienshao's attack/speed EVs and held item (Exp.Share provides no battle protection); give Cryogonal a verified speed plan or choose a safer Electric counter for Gyarados; use Ground-immune/speed control support without abandoning the overall three-round roster. Read installed EVs, natures, abilities, fields and source move damage. Confirm availability/cost before committing to new members/items. Neither Ciel nor the earlier Fiore proposal is validated by this attempt.

Current location is safe outside map359[50,55], allLv75 healthy. Existing route helpers return to Circus for normal training/supply/PC access; wtc_waterfall_exit now accounts for the observed direct arrival on map359, avoiding an obsolete second ascent. F12 is a reload, never the final OS quit. Shutdown verification confirms the actual game process is gone.
