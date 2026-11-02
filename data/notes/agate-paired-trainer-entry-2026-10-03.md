# Paired ordinary trainer entry and opening

`trainer_enter.py` now safely imports without UI/runtime reads. Its default CLI
keeps the existing normal controls and fresh-intro/choice refusals. The source
extension accepts `--paired-event46` only when the two distinct same-map active
lists each declare the exact named ordinary trainer and both are choice-free.
Primary45 must be NWCultistF/Lyla; paired46 must be NWCultist/Ezra for the
combined name **Lyla & Ezra**. Defeated pages, wrong class/order/name, duplicate
events and any102/103/104 choice reject before controls. The actual controller
may use `--active-dialogue` only when that dialogue has already been publicly
observed, as in the existing workflow.

```sh
# Pure installed-source proof only:
python3 scripts/trainer_enter.py 763 45 NWCultistF 'Lyla & Ezra' \
  --paired-event 46 --dry-run
# Root's actual normal entry, after route/public prerequisites:
python3 scripts/trainer_enter.py 763 45 NWCultistF 'Lyla & Ezra' \
  --paired-event 46
```

Source waiting-trainer ordering is in
`notes/agate-double-order-source-proof-2026-10-03.md`. For the reviewed
simultaneous overlap, waitingLyla remains opponent0/Noivern@index1; currentEzra
is opponent1/Ditto@index3. Ditto3 copies own0. Cryo first/Mien second is correct.
Still observe the actual intro, Noivern/Ditto HUDs and Ditto→Hexan transformation
before choosing a move; an old waiting trainer or changed encounter sequence
needs fresh review.

`scripts/agate_double_opener_plan.py` is **always source-only**. Its default
output is `work/agate-double-opener-source-proposal.json`. Optional explicit
frozen `--status`/`--navigation` validate source-stage52, Antoine victory, both
double opponents unbeaten, Cryo-first/Mien-second, fullHP/status-free Lv90,
CryoSash/IceBeam slot1 and MienFakeOut slot2. It never executes the printed
commands. Normal UI registration is Cryo IceBeam Noivern first, then Mien
FakeOut Ditto; priority3 makes FakeOut resolve first. Root must verify each
fresh actor and physical target separately and stop after the turn for actual
public damage/status/foe results. Five paired-entry pure/source fixtures and
syntax/default source dry-runs passed; no UI controls were used in development.
