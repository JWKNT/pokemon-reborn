# Finite explicit Agate items

`scripts/agate_finite_items.py` safely imports without input and defaults to a
source-only dry run. Root supplies a JSON array of1–8 literal `item`/`min_hp`
objects, an exact installed foe list, a mode and a new output directory. It
delegates every action to `agate_public_action.py`; there is no boost-based
policy, automatic attacks, inferred item consumption or hidden battle access.

Example JSON **shape only**, not a current battle instruction:

```json
[
  {"item": "X Sp.Def", "min_hp": 170},
  {"item": "X Speed", "min_hp": 170}
]
```

Normal command after a successful root-reviewed one-action pilot on the same
mode/exact foe set, replacing the plan/pilot/output paths with actual files:

```sh
python3 scripts/agate_finite_items.py --execute --mode warmup \
  --foes Ludicolo,Beheeyem --sequence work/ROOT-REVIEWED-items.json \
  --pilot-journal work/ROOT-completed-warmup-pilot.json \
  --output-dir work/agate-warmup-items-NEW
```

Omit `--execute` for the dry run; it inspects only the supplied plan and static
installed source and creates no queue/evidence output. `--pilot-journal` is
mandatory for execution. The pilot must be a completed guarded public item
receipt, same mode and foe list, within15minutes. The pilot's old HP is never
used for any current action. Solaris, Ricardo and Antoine accept exactly one
installed foe; warmup and Lyla/Ezra require two distinct installed foes. `--canvas` can pass root's
explicit calibration to the existing wrapper.

The sole healing exception is the wrapper's exact recorded error:

> ValueError: Actual HP is below the explicit safe action threshold; no battle action

It additionally requires `helpers=[]`, `pending=null`, no pre-action guard or
capture/journal failure, a positive literal current HP/252 below the requested
threshold, and a fresh public command with the same actor/foes. Only then may
one separate UltraPotion wrapper run with `min_hp=1`. Its successful final
actual HP must meet the original item's threshold. The original item can then
be retried once through a **new** journal. If the heal leaves too little HP, or
the retry stops, there is no second heal/retry and no later queued action.

Any partial helper dispatch, pending receipt, ambiguous outcome, changed actor
or foe, victory, unreadable HP, stale capture, item refusal/no-effect text or
recorder restart stops the queue. An executed item is never replayed merely
because its outcome is uncertain. Each successful child must have the exact
normal item-helper plus battle-ready receipts and a fresh expected command.
Those receipts prove the selected helper returned normally; they do not assert
unseen boost levels or consumption when turbo omitted the message.

Visible own SLP/FRZ/PSN/PAR/BRN/TOX HUD tags, newly displayed status messages,
TrickRoom activation/expiry, weather starts/stops and field/terrain transitions
also stop before the next item or automatic heal. Literal installed
`fieldtext.rb :changeMessage` keys cover transitions such as melted snow or
ignited grass even when the text does not say "field changed". These source
strings are parsed without evaluating game code. Known hail/sand/rain chip or
continuation messages alone are accepted; each item's actual HP threshold still
applies. Missing turbo text does not prove unchanged conditions, so only the
observed public proof is claimed.

Own negative stat messages now also stop the queue before any further item or
automatic heal. Possessive actual Cofagrigus-name attribution is required,
using the existing bounded OCR matcher (including observed **“Cofagrigue’s
Defense fell!”**). Defense/SpDef/Accuracy/Speed and other own attack-stat drops
invalidate the reviewed plan; ordinary/harshly/dramatically-fell grammar is
bound to installed `Battle_Effects.rb716`. Wrapped messages can be joined
within one public screen, never across screens. Foe drops and requested own
boosts do not stop it; a nearby own HUD name cannot attribute a foe's drop to
ours. A visible **“Liepard used Swagger!”** also stops even if confusion text
was missed, since it changes ownAttack and FoulPlay risk. Root must inspect
fresh OWN Q stats and choose updated thresholds manually; no unseen stage
values are inferred or automatically compensated with Xitems.

The hard cap is16 total wrapper invocation slots, counting initial no-action
checks, heals and retries, not16 battle turns. Eight items that all need the
exception may exceed that cap; the queue stops before reserving a17th call.
A15minute wall bound and420second child bound apply. A timed-out or interrupted
wrapper and only its spawned process group are terminated together; pending
remains for root review and can never be resumed automatically. Signal handlers
are installed only during explicit execution and restored when the queue ends.

Each queue directory contains `queue.json` and separate child JSON/text
receipts. Existing wrapper crop evidence remains under `work/<child-stem>`;
unique child stems include the new queue directory name and invocation number.
The aggregate stores the pilot/source hashes, child hashes, requested action,
literal public message candidates, invocation role/count and pending state.
Original child journals retain full public OCR/screens. No existing directory
or partial queue can be overwritten or resumed.

Fourteen pure/source fixtures passed, covering exact no-action healing eligibility,
partial dispatch and capture refusal, changed actor/foes, stale/missing HP,
one heal plus one new retry, post-heal threshold failure, hard16call cap, plan
and output bounds, installed mode rosters, the completed pilot gate and new
status/field/room/weather refusal with known-hail continuation accepted, own
stat-drop attribution and Swagger refusal with foe drops/own boosts accepted. Syntax
and default dry-run also passed. The Agate wrapper's eleven existing fixtures
still pass. No game controls, new public captures, active native/save/battle
logs/AI/RNG or active recording media were used in development. Root must own
the sole input worker when executing it.
