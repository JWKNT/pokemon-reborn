# One normal HeartScale for Cofa Hex

Source-only proposal for installed19.5.43. No live UI, active native save/log, AI or RNG was read; no input was sent. Full proposed dry edges and precise phase guards: `work/heartscale715-normal-route-PROPOSAL.json`. Map illustration `work/agate-map715-SOURCE-ONLY.png` uses installed tiles and explicit historical/hypothetical event pages only.

**Prefer Route4 Map715E64[57,20], on the central island.** [BigJRA's Upper Route4 section](https://bigjra.github.io/reborn/#upper-route-4) corroborates the island/Surf requirement. Installed events and passability supply the exact recipe below. The model uses the named historical post-Glass navigation plus hypothetical completed briefing39151; root must inspect fresh actual progress and layer before execution.

The first post-Hypno735 arrival briefly transfers to715[39,20]/39145, but Radomus715E85 is trigger3 **autorun**, immediately continuing recovery to734. There is no controllable overworld window for a Scale detour there. Leave that recovery chain intact. The post-Hypno source helper owns735E4→715E85→734E16→735E7 and Anna's final choice.

## Normal later approach

After recovery/Calcenon briefing, use the already reviewed ordinary transfers/climbs:413E21→418[17,7];418E2→412[12,18];412E1 RockClimb→710[23,49];710E2→711;711E3→713;713E5→714;714E3→715[65,17]. Keep a healed level90 lead and use an owned Repel normally; an unexpected encounter/dialogue/capture failure stops the route for review. Do not replay an interrupted queue blindly.

710E3[44,43] does transfer directly to715[14,12], but it occupies an isolated upper710 ledge. Source-only walking/layer/Surf planning found no path from the normal710[23,49] entrance to any of its faces. **It is not a shortcut from Calcenon.** If a future actual position already reaches that ledge, its715 entry shortens the dock approach to58 edges; the normal715[65,17] approach is87 dry ordinary/hop edges.

## Bounded control recipe on715

1. Inspect actual715 coordinates and current410 layer. Run the existing **`layer_walk.py 715 50 23 <observed410 0/1> 0`**. It uses bounded28-edge chunks, verifies actual endpoints, preserves calibrated jump taps and stops on unapproved screens/wilds. The source path stays dry, ends at50,23/410False, and avoids the story transfers at21,16 and39,15. Root must not replace observed layer with the proposal's initial value.
2. At **50,23**, face DOWN with the usual short turning tap, press C and resolve only the verified normal Surf prompt, or its source-backed convenience transition. `HiddenMoves.rb:469–510` requires the ordinary Surf move/permission and jumps to the facing water tile. Verify the visible Surf avatar and actual **715[50,24]** before continuing. A hop-rock landing is not proof of Surf.
3. Send one normal **DOWN:.12**, then verify **715[50,25]** and overworld completion. **E97** at50,25 has tile417 and unconditional `code121[410,410,0]`; this is the reliable source-backed **410True** anchor. Root may reflect that completed observed source effect into planner notes. Do not assume E31 set410 on the50,24 boarding landing: its here-trigger can be rejected because that water tile is not an `over_trigger?` tile (`Game_Event.rb:60`, `Game_Player.rb:411`).
4. From that verified **50,25 / Surf /410True** anchor, run existing **`surface_walk.py 715 57 21`**. Installed-only planning gives15 edges: RIGHT8, UP1, RIGHT1, UP3, land LEFT from59,21 to58,21, LEFT to57,21. It has no artificial jump edge or further layer change. The surface helper verifies coordinates before/after its chunks and stops on a715 encounter rather than auto-fleeing it. Native `pbEndSurf`/`pbJumpToward` handles the adjacent island landing normally.
5. At **57,21**, run **`eventq.py 715 64 item`** (or the `agate_prep_phase.py scale` final-pickup phase). It selects the southern face, turns UP and presses C. E64 calls `pbItemBall(:HEARTSCALE)` and sets self-A only on success. Inspect the acquisition message; a normal checkpoint/native bag proof may verify exactly1 HeartScale and715,64,A before crediting the unlock. Do not use collected710E64.

All controls remain ordinary `play.act` helper inputs; neither this note nor its JSON changes game state. The layer source effect is only mirrored after its exact actual coordinate/completion is witnessed. Stop if the native event page, arrival, partner, Surf permission, stock, source geometry or visible screen differs.

## Why the generic island route failed

715's hop rocks use Neutral13 overlays over Water6/7. Existing `surface_plan.py` infers mode from the destination terrain tag, so it changes a native ordinary jump into `surf:jump:down`. That jump does **not** invoke `pbStartSurfing`, and `surface_walk.py` would parse the nested key as direction `jump`. Do not use that generated edge. The dry approach above keeps explicit SurfFalse throughout; boarding begins only at the normal50,23 action boundary. Once visibly boarded, the existing surface model is valid for the short island crossing.

704E87[34,53] is an uncollected backup in the historical saved self-switches. Tourmaline has no direct Fly point and uses four changing layouts, so a704 trip needs a separate train/layout/coordinate route; none is represented as a ready shortcut here. Route715 supplies one source-proven practical approach with the already owned Surf/RockClimb roster.

Verification: pure installed-only dry/layer/explicit-Surf exploration found the complete approach from both715 entry candidates. The final15-edge water/land segment was also checked against the existing `surface_plan` function with a true Surf start and410True. No live route was executed.
