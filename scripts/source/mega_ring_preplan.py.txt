"""Static Ring-quest cost report from explicitly named frozen files only.

No controls, captures, current save/runtime/planner reads, or game mutations.
Absent observed cage self-switches are unknown ownership, not proof of absence.
"""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "work/mega-ring-installed-source.json"
STATUS = ROOT / "notes/Void-Hypno-won-128-status.json"
NAV = ROOT / "notes/Void-Hypno-won-128-navigation.json"
CAGES = [(16, "VANILLITE", "PURPLESHARD", 3, "Eustace"),
         (17, "LOUDRED", "BLUESHARD", 5, "Lillin"),
         (18, "CYNDAQUIL", "REDSHARD", 9, "Sanford"),
         (19, "LICKITUNG", "BLUESHARD", 7, "Myles"),
         (20, "MAKUHITA", "GREENSHARD", 3, "Felicia"),
         (21, "JIGGLYPUFF", "GREENSHARD", 5, "Santiago"),
         (22, "ABRA", "PURPLESHARD", 8, "Arzelle"),
         (23, "ROGGENROLA", "REDSHARD", 3, "Mr. McKrezzy"),
         (24, "DITTO", "GREENSHARD", 8, "Sanford")]


def report():
    source, status, nav = [json.loads(p.read_text()) for p in [SOURCE, STATUS, NAV]]
    events = {(e["map"], e["id"]): e["event"] for e in source["events"]}
    total = {s: 0 for s in ["REDSHARD", "BLUESHARD", "GREENSHARD", "PURPLESHARD"]}
    rows = []
    for eid, mon, shard, count, owner in CAGES:
        e = events[(324, eid)]
        commands = e["pages"][0]["list"]
        assert any(c["code"] == 355 and c["parameters"] ==
                   [f"$PokemonBag.pbDeleteItem(:{shard},{count})"] for c in commands)
        assert mon in str(commands) and f'knownTrainer("{owner}")' in str(commands)
        observed = nav.get("self_switches", {}).get(f"324,{eid},A")
        total[shard] += count
        rows.append(dict(event=eid, position=[e["x"],e["y"]], species=mon,
                         shard=shard, cost=count, original_owner=owner,
                         observed_purchased=True if observed is True else None))
    stock = {s: status["bag"]["contents"].get(s, 0) for s in total}
    return dict(scope="Static plan, not a game action or current inventory query",
                frozen_binding={p.name:hashlib.sha256(p.read_bytes()).hexdigest()
                                for p in [SOURCE, STATUS, NAV]},
                cage_rows=rows, all_nine_cost=total, frozen_shards=stock,
                worst_case_additional_shards={s:max(0,total[s]-stock[s]) for s in total},
                earlier_ditto_flag426=nav.get("switches",{}).get("426"),
                observed_quest_variable160=nav.get("variables",{}).get("160"),
                cage_ownership_caveat="Unmarked cages need ordinary visible event/PC inspection; mirror absence does not prove not owned.",
                mandatory_battles=["Santiago0", "Colin0+Matthew0 doubles", "Eustace0 singles immediately after doubles"],
                optional_battle="McKrezzy0; autograph is given on the preceding page",
                required_returns=["Lillin Loudred", "Felicia Makuhita", "Mr. McKrezzy Roggenrola", "Lillin/Santiago Jigglypuff", "Eustace Vanillite"],
                ring_reward="826E8p4, variable160>=25 and switch479; normal reward sets160=26")


if __name__ == "__main__":
    print(json.dumps(report(), indent=2))
