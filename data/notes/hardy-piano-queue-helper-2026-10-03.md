# Hardy piano normal queue

`scripts/hardy_piano_queue.py` is a source-only dry run by default. Development
read installed map/event/tileset assets and used synthetic rendered fixtures;
no live UI, current save/native data, active battle/log or recording was read,
and no game input was executed.

After normally defeating all three hall trainers, root should take one fresh
checkpoint in map739 with every tuner still at initial x14. Existing checkpoint
produces the named status/navigation evidence and mirrors the actual saved event
positions into planning notes. Then, from actual overworld with an active
healthy recording, within120 seconds of the checkpoint:

```sh
python3 scripts/hardy_piano_queue.py --execute \
  --frozen-status notes/Hardy-piano-ready-status.json \
  --frozen-navigation notes/Hardy-piano-ready-navigation.json \
  --journal work/hardy-piano-first-progress.json
```

The command above assumes root named the checkpoint `Hardy-piano-ready`.
Explicit evidence must prove trainer739E22/E35/E36 self-A True, all eight actual
initial positions, switch1022 False, an owned RockClimb move and a six-member
party. The helper checks public overworld/coordinates and rejects still-active
automatic trainers before queuing movement. It does not defeat trainers or
prepare the Hardy battle party.

Each tuner group walks to its west side, verifies the actual player facingRight
and exact rendered installed tile604 at the adjacent square, then queues at most
seven discrete C/push/right-step pairs. Source `pbPushThisObject` moves only the
tuner; the right step follows into the vacated square. Final actual player
coordinates and rendered tuner tile must both prove the group's exact result
before the new event position and variable x−14 are mirrored into planner notes.
Targets are x17,19,21,16,16,14,15,15; values441–448 are3,5,7,2,2,0,1,1. The sixth
tuner is interacted with vertically, leaving x14 and explicitly refreshing0.
No game/save event positions or variables are written by the script.

The final ordinary climb is739[5,46] facingUp, through source event1. Only a
visible `used Rock Climb` message receives an extra C; otherwise a clear world
screen is required. After the bounded animation settle, actual739[5,8] must be
observed. The helper walks to[11,5] and requires the rendered open-door tile573
at[11,4] before mirroring source switch1022 into planning notes. The closed
source map has tiles[479,573,594], so checking the underlying573 would be
insufficient; its closed-bar overlay matches only25% of open573 pixels and the
synthetic closed-door fixture is rejected. Finally normal door event31 must
actually transfer to740[9,21]. The queue stops there, three tiles below Hardy's
player-touch trigger at[9,18], without starting the gym battle or saving again.

All inputs/helpers are receipted in a new journal, pending before dispatch.
Recording health is required before/after each group; any recorder restart,
unexpected dialogue/battle, uncertain player/facing/tile/coordinate, partial
group or wrong landing stops. Do not replay a stopped journal or substitute a
new name to bypass a partially changed puzzle. Root must inspect the real
screen, take a normal checkpoint if useful, and manually review/replan a
mid-puzzle state. The helper intentionally supports the safe initial case only.

Default scale4 expects the previously calibrated2272×1816 native window capture
and installed boy_walk/boy_run player sprites. Any geometry or sprite mismatch
stops; no inferred tuner movement or estimated hidden variable is credited.

Verification:

```sh
python3 scripts/hardy_piano_queue.py
python3 scripts/test_hardy_piano_queue.py
python3 -m py_compile scripts/hardy_piano_queue.py scripts/test_hardy_piano_queue.py
ruby -c scripts/hardy_piano_source.rb
```

Five meaningful source/synthetic tests pass: installed event targets and climb,
fresh initial-state rejection, all bounded push adjacency traces, actual
player-relative tuner pixel proof and wrong-square rejection, and open/closed
door pixel proof. The default proposal is saved at
`work/hardy-piano-queue-source-proposal.json`. No runtime success is claimed.
