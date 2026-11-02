# Normal Agate/Hardy shopping queue

scripts/agate_supply_queue.py is a source-only planner unless --execute is
explicit. The reviewed entry is the new ordinary checkpoint
Agate-Cofa-EVs-complete on map519, with the named Fly carrier Tranquill still
in the six and Cofagrigus90 Timid holding Power Lens after exactly80 SpA EVs.
The helper leaves that Lens equipped; use agate_prep_phase.py finish-lens
after returning to Circus.

    python3 scripts/agate_supply_queue.py --status notes/Agate-Cofa-EVs-complete-status.json
    python3 scripts/agate_supply_queue.py --status notes/Agate-Cofa-EVs-complete-status.json --execute

The full frozen navigation sibling is loaded automatically. Execution requires
the checkpoint be at most300 seconds old, actual ordinary overworld/map guards,
explicit719=False for herb page0, membership counter175≥7, Membership Card, and
the exact completed Cofa build. Source reads recheck installed vendor scripts,
stocks and prices. Each named purchase delegates to shop_buy.py, which checks
the selected label, quantity, total price and Yes/No before payment, then verifies
its receipt. No checkpoint is made between purchases.

The four phases are:

| Phase | Normal route | Target bag quantities |
|---|---|---|
| dept | Fly520;520E101→112E6→113E1, visible8F menu→4E4; return floor1→520 |12X Sp. Atk,7X Speed,9X Defend,4X Attack |
| herbs |520→611;611E2 page0; return520 |2Revival Herb |
| ultra |Fly519;519E116→38E5;38E6→519 |40Ultra Potion |
| return-circus |Fly355; single checkpoint Circus-restocked129 |Final bag/money/party reconciliation |

Only deficits from the actual frozen bag are bought. The actual frozen money
must cover the cart. The17,000 berry/Lens expense has already occurred by this
entry checkpoint, so it is not reserved again. The hypothetical pre-training
baseline yields23,050 shopping cost and34,130 remaining after that build;
training medicine use or income changes the actual cart/money result.

The new default work/agate-shopping-129-journal.json records each phase and each
step as pending before execution. A failure keeps that pending boundary and any
already verified receipts. An existing journal is never replayed. Recovery needs
ordinary manual menu exit/travel to one of the reviewed entrances, then a fresh
named checkpoint and a **new journal**, for example:

    python3 scripts/agate_supply_queue.py --status notes/Agate-shopping-recovered-status.json --from-phase herbs --journal work/agate-shopping-129-recovery1.json --execute

Allowed fresh entrance maps are dept519, herbs520, ultra520, return-circus519.
Every skipped earlier vendor's quantities must already meet its targets; the
cart is recomputed from the fresh checkpoint. Do not resume at a purchase menu.
If the final Circus checkpoint exists but verification stopped, inspect that
existing evidence rather than overwrite it. The final gate requires all target
quantities, exact source-priced money expenditure, and unchanged party build,
held items, HP/status and move PP.

Validation: Python syntax checks and eight pure fixture/source tests passed.
Fixtures modify only copies of closed Hypno128 evidence and do not claim the
future training/shopping was performed. No UI, input, game/save mutation or
actual shopping was executed during development.
