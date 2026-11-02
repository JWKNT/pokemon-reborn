# Small supply run before Agate → Hardy

Source-only proposal; no purchases or controls executed. Baseline is the frozen post-Hypno128 inventory supplied by root:74180 money,30UltraPotion,16FullHeal,2XAttack,6XDefend,4XSpeed,7XSpecial,11XSpDef,3XAccuracy,21SuperRepel,15ExpCandyXL. The named closed checkpoint additionally confirms1Revive, no MaxPotion/FullRestore/RevivalHerb, MembershipCard1 and floor-unlock variable175=7. **Reserve17000 for4Pomeg(2000)+PowerLens(15000).** This is PowerLens for Cofa training, not a new WideLens.

Existing stock already meets the basic one-attempt Agate setup. This inexpensive margin covers route/training expenditure, the two separate Agate setups, backup counters and Hardy without bulk-buying distant League supplies.

|Buy|Unit cost|Total|Resulting stock|
|---|---:|---:|---:|
|5XSp.Atk|350|1750|12|
|3XSpeed|350|1050|7|
|3XDefend|550|1650|9|
|2XAttack|500|1000|4|
|10UltraPotion|1200|12000|40|
|2RevivalHerb|2800|5600|2, plus existing1Revive|
|**Total**||**23050**||

Money after this cart:51130; after the reserved team prep: **34130 remains**. Do not buy more XSpDef, XAccuracy, FullHeal, Repels or candy now. Ultra restores200HP; RevivalHerb is full-HP revival. At16badges `Mart.rb:pbDefaultMart` sells Ultra but **not MaxPotion or Revive**. MaxPotion enters default marts at17badges, Revive at18. The previous plan's optional MaxPotion suggestion is therefore not a confirmed pre-Agate purchase.

Why these targets: Agate baseline uses up to6XSpecial across its separate fights and3XSpeed in Solaris;12XS leaves room for Cryo's one-item backup, two Ludi items at Hardy and a small margin.7Speed permits one Solaris rebuild after a forced switch.9Def covers the Solaris opener, both Hardy actors' own first-turn Defense items and extra restoration.4Attack covers the Swamp Solaris backup and Hardy Swamp/KG alternatives.40Ultra covers the proposed15-ish Agate budget,8Hardy reserve, ordinary defenders/training and some extra critical recovery. These are practical stock goals, **not a guaranteed bound against unlimited crits/repeated failed chains**. Recheck after street defenders, before crossing763x43–48,y52; consumed items remain spent even though the warmup's normal partner heal restores HP/status/PP. Refresh again after Solaris before Hardy.

## Exact normal vendors

* **Dept8F, map4E4[5,5]**: all six relevant Xitems, unconditional shop page. Frozen MembershipCard1 and175=7 permit8F through113E1's normal floor menu. Variable91=3 is not the elevator's unlock counter.
* **GrandHall38E5[25,18]**: `pbDefaultMart`; at our16badges UltraPotion1200 is present. Circus355E90 instead sells HyperPotion, not Ultra, so do not call an Ultra purchase there.
* **Obsidia herb shop611E2[9,4]**: RevivalHerb2800. Frozen719=False selects its ordinary shop page0. If a future719True first greeting appears, finish that reviewed greeting and interact again for page2; do not treat dialogue alone as a shop. Existing `city_enter.py 520 611` normal entrance is used by the previously completed city-supply route.
* Reserved prep stays at Circus355E136[46,36] for4Pomeg500,355E83[36,14] for PowerLens15000 while715=False. Existing `agate_prep_phase.py shops --status <fresh-circus-status> --execute` computes any already-owned deficit and verifies the budget.

Efficient order: do the Circus berries/Lens/build, the normal Opal EV pilot/finish, then use the carrier for **Obsidia Dept8F + nearby herbs → Opal GrandHall → Circus finish-lens/heal**. Do not restore the final six or remove the Fly carrier prematurely.

## Existing helper commands at inspected vendor anchors

Use fresh normal outside-battle state and deficit quantities if any purchases already happened. These snippets start on the named map; they do not independently certify travel. Each `shop_buy` verifies item/count/price before payment.

```sh
python3 scripts/eventq.py 4 4 talk
python3 scripts/mart_open.py
python3 scripts/shop_buy.py 'X Sp. Atk' 5 350
python3 scripts/shop_buy.py 'X Speed' 3 350
python3 scripts/shop_buy.py 'X Defend' 3 550
python3 scripts/shop_buy.py 'X Attack' 2 500
python3 scripts/mart_exit.py

python3 scripts/eventq.py 611 2 talk
python3 scripts/mart_open.py
python3 scripts/shop_buy.py 'Revival Herb' 2 2800
python3 scripts/mart_exit.py

python3 scripts/eventq.py 38 5 talk
python3 scripts/mart_open.py
python3 scripts/shop_buy.py 'Ultra Potion' 10 1200
python3 scripts/mart_exit.py
```

The established department entry sequence is `fly_to.py 520`, `eventq.py 520 101 enter`, `eventq.py 112 6 enter`, `eventq.py 113 1 talk`, `dept_greet.py`, `dept_floor.py 8`. It uses normal travel and visible floor confirmation. Returning uses4E6→113, normal floor1, then112E1 to520. Do not run `glass_stock_supplies.py` unchanged: its old cart adds unneeded SpDef/Accuracy/Repels and omits the new Attack reserve.

Primary proof: `work/agate-shopping-source-2026-10-03.json`, `work/agate-shopping-extra-source-2026-10-03.json`, `work/agate-dept-floor-source.json`, installed `Mart.rb:722`, `Reborn/itemtext.rb:4353–4406,5583,2380`, and the explicitly named frozen128 files. A machine-readable **proposal only** is `work/agate-hardy-shopping-frozen-proposal-2026-10-03.json`.
