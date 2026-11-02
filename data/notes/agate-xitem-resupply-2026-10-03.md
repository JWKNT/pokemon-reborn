# Agate prechain Xitem resupply — source-only proposal

Installed19.5.43 checked; no UI/native/live battle reads or actions performed.
Do this outside battle at reviewed391=52, before entering the true-chain strip
763x43–48,y52. Finish street victories first or keep all remaining trainer
sightlines blocked in normal route planning.

**Agate's shop cannot supply Xitems.** Its real map is751, not753:763E80[27,45]
unconditional entrance→751[8,9]; clerk751E1[5,5] finishes two raid-flavor lines
when989True then calls `pbDefaultMart`. Installed `Mart.rb722–745` at16badges
stocks balls/repels/rope/FullHeal/UltraPotion, no Xitems.753 is the apartment
map; its doors are locked until999True after the later city scenes.

Static scan of every installed Map*.rxdata found exactly one normal event
vendor containing XSPECIAL or XSPEED: **Dept8F4E4[5,5]**, unconditional
`pbPokemonMart([XATTACK,XDEFEND,XSPECIAL,XSPEED,XSPDEF,GUARDSPEC,XACCURACY,DIREHIT])`.
Proof `work/xitem-vendors-all-installed-static.json`. Default marts were checked
separately because they use a shared function. XSpAtk350, XSpeed350,
XAccuracy950 from `Reborn/itemtext.rb4371–4405`; no special merchant price.

Parent-frozen accounting (not a claim about current bag): initial9SpAtk/4Speed/
9Def/4Atk/11SpDef/3Acc/38Ultra,2Herbs16FullHeal1Revive. Antoine intended
spends3SpAtk3Speed1Def1Acc; optional Cryo boost spends1SpAtk. That leaves
**5SpAtk1Speed8Def4Atk11SpDef2Acc**, before any other actual consumption.
Warmup3SpAtk plus Solaris3SpAtk needs6; Solaris3Speed needs3. Proposed cart:

| Purchase | Quantity | Unit | Cost |
|---|---:|---:|---:|
| X Sp. Atk |4|350|1400|
| X Speed |3|350|1050|
| X Accuracy |2|950|1900|
| Total |||**4350**|

Parent selected this4350 cart. It gives9SpAtk/4Speed/4Acc after the cited
spending:3SpAtk1Speed spare after the exact6SpAtk3Speed chain plan. Minimum
shortage-only purchase is1SpAtk2Speed1050. Parent money44106 and
future trainer winnings comfortably cover it; use actual normal money and bag
proof before committing purchases.

## Normal travel and purchase sequence

At752 PC, temporarily exchange whichever reviewed party slot holds Cryo for
Box1slot11 Tranquill24 (parent's reviewed current box slot). Preserve Cryo's
heldSash by boxing it normally. Read the
actual party/box labels; do not assume the pre-doubles order or a stale cursor.
Exit752E8→76346,70. At39152 the earlier allied Fly-arrival enclosure has blank
pages, so returnFly76346,70 is safe; the oldstage51 Vanhanen detour is unnecessary.

Existing reviewed normal helpers, parent executes one guarded phase at a time:

```sh
python3 scripts/fly_to.py 520 --carrier Tranquill
python3 scripts/eventq.py 520 101 enter
python3 scripts/eventq.py 112 6 enter
python3 scripts/eventq.py 113 1 talk
python3 scripts/dept_greet.py
python3 scripts/dept_floor.py 8
python3 scripts/eventq.py 4 4 talk
python3 scripts/mart_open.py
python3 scripts/shop_buy.py 'X Sp. Atk' 4 350
python3 scripts/shop_buy.py 'X Speed' 3 350
python3 scripts/shop_buy.py 'X Accuracy' 2 950
python3 scripts/mart_exit.py
python3 scripts/eventq.py 4 6 enter
python3 scripts/eventq.py 113 1 talk
python3 scripts/dept_greet.py
python3 scripts/dept_floor.py 1
python3 scripts/eventq.py 112 1 enter
python3 scripts/fly_to.py 763 --carrier Tranquill
python3 scripts/eventq.py 763 79 enter
```

Normal MembershipCard and175≥7 already proven by the completed earlier8F
shopping; still use the actual floor-menu labels. Shop helper price/quantity
guards stop on ambiguity; a partial purchase must be reviewed, never blindly
replayed. At752 restore the exact boxedCryo slot for Tranquill, arrange the fixed
six **CF/Arc/Swamp/Mien/Exc/Cryo**, nurse752E4, exit752E8, then parent makes the
fresh finalprechain checkpoint. Count actual purchased quantities/money against
4350 once, and freeze party/bag before chain archive entry. No save-per-purchase
or new major IDs are needed.

The finite dry-run-default implementation is `scripts/agate_pc_resupply.py`.
It requires explicit frozen post-Antoine/Lyla/Ezra completion selfA flags,
stage52, all six Lv90, retained normal Cofa build, CryoSash still held and enough
actual money; it accepts injured members because its first action is a normal
nurse heal. It arranges CF/Arc/Swamp/Mien/Exc/Cryo before the two reviewed
Box1slot11↔party5 exchanges, returns to76346,70 and verifies the single final
checkpoint's full HP/status/PP, retained identities/items/moves/PPUps, exact
4350 money delta and exact bag purchase deltas. Inherited expired-Repel prompts
are cancelled normally on this town trip. Pending journals stop without replay.

```sh
python3 scripts/agate_pc_resupply.py \
  --status notes/<street-won>-status.json \
  --navigation notes/<street-won>-navigation.json
# Add --execute only under the root's sole-controller recording session:
# --journal work/agate-pc-resupply-131.json
# --checkpoint Agate-restocked-south-ready131
```

After actual street victories, stale independently introduced trainer-ray
avoids can survive checkpoints. `sync_navigation.rb` preserves extra keys,
including `agate_party_owned_avoid`; it does not lose ownership metadata. The
finite helper now clears only original E45/46/49 source-footprint cells after
explicit all-three selfA victories and actual saved NPC-position evidence.
It preserves original NPC-origin guards plus current visible/collidable NPC
positions, every other avoid and
the complete y52 commitment barrier. This cleanup happens in planning notes
only during parent-authorized execution, before the ordinary PC approach;
development/pure review never edits the current navigation file. Normal route
helpers still stop if actual NPCs/terrain leave no path.

Five resupply source/pure tests pass, including narrow cleanup preservation;
no control/native/checkpoint was run by the planner.
