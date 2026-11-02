# Proposed normal Agate preparation queue

Source-only review for installed Reborn 19.5.43. This is a future route/build proposal, not evidence that any preparation was performed. No UI input, active game state, current battle log, AI or RNG was inspected. Explicit historical reference: `Glass-post-gauntlet-attempt-1-status.json` and its named backup. Root owns all fresh state checks and normal controls.

## First finish and freeze Hypno

After a Hypno victory, make the native post-battle save/checkpoint and reconcile its exact consumed items **before** spending a mint, berries, Scale or changing held items/PC membership. The Void exit arrives at735[18,18], then the native recovery autoruns must complete:735E4 page0→715[39,20]/39145;715E85→734[18,14]/39146;734E16→735[18,14]/39147;735E7→39148. The brief715 arrival is **not** a controllable Scale window: RadomusE85 is an autorun.735E4 page2 then presents Anna's choice; Yes transfers to413[77,26] and sets391=49; No stays local and sets391=49. The post-Hypno exit helper/review owns those exact source boundaries. From the Calcenon arrival, source-backed interactions are413E46 Shelly[61,32], then413E93 Eve[43,30], then413E67[28,31] into417[11,28]. The house autorun is417E29, or417E30 when878 is true. Both finish at391=51. Inspect the actual branch and take one meaningful checkpoint after it; do not invent unsaved planner flags.

## Temporary Fly carrier and exact later PC

Calcenon413E68[45,27] enters415[10,10]; PC415E7[14,3], nurseE4[10,4], exitE8[10,11] returns413[45,28]. The historical Box1 has Tranquill24 at slot12, Cryogonal/Hexan90 at slot6, and Kricketune50 holding FocusSash at slot11. Verify those slots and the outgoing party index visibly before using `pc_exchange_named.py`. A practical temporary swap is Tranquill for Klinklang, retaining the carrier throughout shopping, scale collection and training.

Keep Tranquill until Agate arrival. City763E79[46,69] unconditionally enters **Agate Pokémon Center752[10,10]**, south of the commitment strip. PC752E7[14,3], nurseE4[10,4], exitE8[10,11]→763[46,70]. There, use fresh inspected Box1 exchanges to bring in Kricketune, take its Sash normally, then exchange Kricketune for Hexan and give Hexan the Sash. This solves the Fly-carrier problem without assuming access to a PC between the Agate fights. If the Agate Fly point is not yet registered, Fly to Vanhanen Castle292[16,16] and use the ordinary route into the city; that approach still needs a fresh guarded route.

## Shops, new Scale and build

Circus355E136[46,36] sells Pomeg Berry for500; buy4. Circus355E83[36,14] sells PowerLens for15000 while switch715 is false. Total17000, skipping supplies already owned. E136 is unconditional. Refresh bag/money/vendor page outside battle before shopping. The helper's `shops` phase verifies the exact budget and refuses a needed Lens purchase after715.

The new HeartScale target is **Route4 Map715E64[57,20]**. The old `route4_scale_and_rockslide.py` targets710E64, which is already collected, and must not be reused for this pickup. Installed event transfers for the proposed climb are413E21→418[17,7],418E2→412[12,18],412E1→710,710E2→711,711E3→713,713E5→714, then714E3[15,25]→715[65,17]. Use the previously reviewed normal layer approach on713 before its E5; do not assume straight-line movement.

**Resolved source geometry:** E64 is on the central island and requires Surf. Basic walking/layer-only planning failed because it omitted that mode. Existing `surface_plan.py` also falsely treats ordinary hop-rock landings as Surf, so do not start `surface_event71564` from the climb arrival. Use the explicit dry-to-Surf recipe in `notes/heartscale-normal-route-2026-10-03.md`: layer-walk to715[50,23]/410False, board Surf downward to50,24, then one normal DOWN to50,25, whose E97 establishes410True. From that verified Surf anchor, the existing surface helper safely plans the short crossing to57,21. `agate_prep_phase.py scale` is the final island pickup only. The uncollected704E87[34,53] remains a backup needing its own ordinary approach review. The old failure artifact `work/agate-scale715-source-routes.json` describes only walking/layer models, not a complete surface route.

At Circus355, the `build` phase performs only normal menus:

1. Take Cofa's SpellTag, put Cofa first, use the owned Timid Mint.
2. Give4 Pomeg berries: HP EV252→172.
3. Teach owned TM97 DarkPulse over slot3 DestinyBond.
4. Relearn Hex over slot1 ShadowBall at355E35[50,35], spending1 HeartScale.
5. Give PowerLens, heal at355E118, then checkpoint `Agate-Cofa-training-ready`.

The reminder selection is **index2**, because native firstmoves prepend unknown Curse/OminousWind/Hex. It is not the level-up-list index. Native `MoveRelearner.rb:12–38` establishes this order; the named historical backup establishes Cofa's firstmoves. Shared `learning.py` has no Hex rule, so the new helper adds `PLANS['hex']=1` only inside its own reminder process, with visible Hex/confirmation checks. No shared learning/navigation helper was changed.

The build starts only from the reviewed level90 Calm Cofa, EV[252,4,252,0,0,2], and moves[TrickRoom,ShadowBall,WillOWisp,DestinyBond]. It refuses partial mint/berry/moveset states. After a partial stop, inspect and resume manually; never rerun four berries blindly. `use_field_item.py` selects the first party member, hence putting Cofa first is required and the final native check verifies the mint actually affected Cofa.

## Bounded EV pilot, then two KOs

Installed `Battle.rb:2707–2753` replaces all normal EV yields when a boosted Power item is held and gives32 in the Lens stat, subject to the252/510 limits and other switches. `ItemEffects.rb:1649–1685` removes20 per Pomeg. Therefore four berries free80 EV total; three successful Lens KOs should add32+32+16 SpA. Prove the first32 rather than presuming Pokerus/EV switches are absent.

Normal Fly to Opal519; the existing reviewed grass approach is519[35,51]→[28,51], up:.12. The approved common targets are Rattata/Bidoof/Patrat/Zigzagoon/Meowth/Spinarak, from installed map519 encounter definitions. Use Cofa **DarkPulse slot3**, so Normal targets are hittable. The phase uses the existing guarded `train_wild_bulk.py`, runs other species, includes faint/HP/status/PP guards, and marks its public win ledger provisional until the native EV checkpoint.

- `training-pilot`: one KO only, checkpoint `Agate-Cofa-Lens-pilot`; require SpA EV exactly32.
- `training-finish`: only from that32 checkpoint, two KOs, checkpoint `Agate-Cofa-EVs-complete`; require EV exactly[172,4,252,80,0,2].
- `finish-lens`: return355, remove Lens normally, heal, checkpoint `Agate-Cofa-prepared`; require no held item and exact stats252HP/93Atk/333Def/210SpA/218SpD/68Speed.

`train_wild_bulk.py` can hit its encounter batch limit before the requested wins; a zero exit code alone is insufficient. The native post-phase EV/stat gates refuse to credit an incomplete or excessive training result. No save per KO is planned: one pilot checkpoint and one final checkpoint settle the two meaningful EV boundaries.

## Phase commands and commitment guard

Each phase is dry-run by default:

```sh
python3 scripts/agate_prep_phase.py shops --status notes/<fresh-circus-status>.json
python3 scripts/agate_prep_phase.py build --status notes/<fresh-build-start-status>.json
python3 scripts/agate_prep_phase.py training-pilot --status notes/<fresh-opal-status>.json
python3 scripts/agate_prep_phase.py training-finish --status notes/Agate-Cofa-Lens-pilot-status.json
python3 scripts/agate_prep_phase.py finish-lens --status notes/<fresh-circus-trained-status>.json
```

Root may add `--execute` only after inspecting the proposal and supplying a **fresh normal outside-battle checkpoint** for the expected map. File freshness is the caller's responsibility: the helper checks visible overworld/map before acting, but cannot infer whether an arbitrarily supplied JSON is current. All proposed movement/action inputs go through existing `play.act` helpers. No phase was executed during this review.

Before Agate commitment, heal and native-check the fixed six: Cofa/Arc/Swamp/Mien/Exc/Hexan, exact Cofa build above, Hexan holding the borrowed Sash, required bag supplies, weather and391=52. Source-proven event-free checkpoint is763[45,53]. **Do not cross x43–48,y52** until prepared: the touch strip sets391=53 and immediately starts the uninterrupted Howaya/Christina→Solaris chain. No confirmation/PC/menu separates the fights. Full-heal between them restores HP/status/PP, including fainted members, but consumed held Sash does not return. Keep Hexan out of the warmup unless needed.

Refresh quantities after Hypno and buy a margin for6 XSpecial/3 XSpeed/2 XSpDef/2 XDefend/1 XAccuracy, roughly15 UltraPotions, status cures and a few Revives. The combat proof and guarded branches are in `notes/agate-chain-plan-2026-10-03.md`. Archive only Solaris as a major fight; retain both fights and failed runs in the full journey recording.

Validation: six pure phase fixtures pass; both new files pass `py_compile`. No live UI/game input or current state/log read occurred.
