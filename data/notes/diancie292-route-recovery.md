# Session292 Aegir route recovery, October11

No boss fought yet. Recorder292 remains active. Corrected several incomplete older route assumptions through ordinary controls.

- Victory785 E60 sends to55,89; RockClimb145 from24,55left→22,55; portal152from17,52up→85254,7.
- 852 route6,36→11,43, Surf11,44; waterfall down→11,86; surface4,95; portal3→84959,37.
- 849 E54 is a CHOICE: talk hole, Jump? Yes. It transfers85043,60 then autorun85 drops6tiles→43,66 (dry eight-tile isolated shore). Source explicitly confirms6Down.
- From85040,65 faceleft+C Surf→39,65. Southwest pond is isolated from main lake. Climbing35,62falls to35,59 only reaches a shallow western strip bounded by rocks; DON'T repeat this detour.
- Correct continuation fromSWpond: Surf26,65, Dive85126,65; underwater23,61, enterE3→12,50; underwater43,13, enterE7→62,106; underwater68,107, surface85068,107; Surf/walk62,107; enterE57→85062,33 (brief849transfer part of installed script).
- Walk85058,42 then **down only**, wait5. Touch event82 automatically startsSurf, jumps3, walks3, ends58,48. Do NOT pressCafterwards unless ready toDive (CopensDive on darkwater).
- Latest current state: enteredDive85158,48, worker `diancie292_depths_entry.py --underwater` routes55,64→E15→39,103→surface39,106→85039,110→E116→86024,26. It then saves, teachesVolcanionBrickBreak slot2, SwampertBulldoze slot1, savesDepthsBuild.
- EscapeRope attempted underwater approach850: explicitly Can't use that here; none consumed (10remain).
- TwoSuperRepels consumed sofar, 28remain afterunderwaterrenewal.

Scripts: diancie292_main_lake.py now handles the connected underwater rooms and normal ledgejump. diancie292_depths_entry supports --underwater; do not replayits initial lakeapproach if already inside.

IMPORTANT Depths ascent previous summary ladderchain was wrong. New static route (with waterfall underpasses): **10→14→21→23→1**. Source-reviewed sixMoveForward horizontal waterfall passages addedto `nav.py` for map860 only. This changes planning only, no game/save modifications. Actual crossing still must be observed. `diancie292_depths_ascent.py` uses this correctedchain; starts after main descent atbottomlake and approaches86048,107.

Optional PrisonBottle script `diancie292_depths_bottle.py`: surface33,27→upfalls33,14→item144at36,14, reversefalls, approach24,31thenDown+C main descent. Not yet run; verifylanding/prompt.

Recording291 fully finalized/published/cleaned; video25through29146988framesSHA2d4c1fbe1c510d2af4f5da3733cbecb9b920fcd7c8e81949cc9d06b92959fb09. No major in292yet. 292 should rotateatDepthsBuild; archive whiletraversing293. Usage21%usedlastchecked,95%cutoff.
