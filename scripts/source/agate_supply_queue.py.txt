"""Normal Agate/Hardy restocking queue; explicit frozen checkpoint, dry-run first.

Import and planning do not observe/control the game. --execute delegates only to
the existing ordinary UI helpers. A partial phase is never resumed at a guessed
menu cursor: recover to a reviewed entrance, make a fresh checkpoint, and use a
new journal with --from-phase. The final Circus checkpoint is the sole new save.
"""
import argparse
from datetime import datetime
import hashlib
import json
import re
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GAME = Path("/Applications/Reborn.app/Contents/Game")
PHASES = ("dept", "herbs", "ultra", "return-circus")
START_MAP = dict(dept=519, herbs=520, ultra=520, **{"return-circus": 519})
END_MAP = dict(dept=520, herbs=520, ultra=519, **{"return-circus": 355})
ITEMS = {
    "XSPECIAL": ("dept", "X Sp. Atk", 12, 350),
    "XSPEED": ("dept", "X Speed", 7, 350),
    "XDEFEND": ("dept", "X Defend", 9, 550),
    "XATTACK": ("dept", "X Attack", 4, 500),
    "REVIVALHERB": ("herbs", "Revival Herb", 2, 2800),
    "ULTRAPOTION": ("ultra", "Ultra Potion", 40, 1200),
}
FINAL_EV = [172, 4, 252, 80, 0, 2]
FINAL_MOVES = ["TRICKROOM", "HEX", "WILLOWISP", "DARKPULSE"]
IDENTITY_KEYS = ("species", "form", "name", "level", "item", "nature", "ability",
                 "ev", "iv", "totalhp", "attack", "defense", "spatk", "spdef",
                 "speed", "moves", "hp", "status")


def need(ok, message):
    if not ok:
        raise ValueError(message)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def identity(status):
    return [{k: m.get(k) for k in IDENTITY_KEYS} for m in status["party"]]


def training_proof(status):
    party = status["party"]
    need(len(party) == 6, "Expected the reviewed six-member travel party")
    carriers = [m for m in party if m["species"] == "TRANQUILL"
                and m["name"] == "Tranquill"
                and "FLY" in [v["move"] for v in m["moves"]]]
    need(len(carriers) == 1 and carriers[0]["hp"] > 0,
         "Unique conscious named Tranquill with Fly required")
    cfs = [m for m in party if m["species"] == "COFAGRIGUS"
           and m["name"] == "Cofagrigus"]
    need(len(cfs) == 1, "Unique named Cofagrigus required")
    cf = cfs[0]
    need(cf["level"] == 90 and (cf.get("natureflag") or cf["nature"]) == "TIMID" and cf["ev"] == FINAL_EV
         and cf["item"] == "POWERLENS"
         and [v["move"] for v in cf["moves"]] == FINAL_MOVES,
         "Cofa EV/build/Lens proof differs; finish training before this queue")
    need([cf[k] for k in ("totalhp", "attack", "defense", "spatk", "spdef", "speed")]
         == [252, 93, 333, 210, 218, 68], "Cofa final native stats differ")
    need(cf["hp"] > 0 and all(m["status"] is None for m in party),
         "Conscious Cofa and status-free travel party required")
    need(sum(bool(v) for v in status["trainer"]["badges"]) == 16,
         "Reviewed Grand Hall stock requires the current16-badge checkpoint")


def plan(status, navigation, from_phase="dept"):
    training_proof(status)
    need(status["map"] == START_MAP[from_phase], "Frozen map differs from phase entrance")
    # sync_navigation.rb's full checkpoint has flags/positions, not a map key.
    need("map" not in navigation or navigation["map"] == status["map"],
         "Frozen navigation/status maps disagree")
    need(navigation.get("switches", {}).get("719") is False,
         "Herb page0 requires explicit frozen switch719=False; other pages need review")
    need(navigation.get("variables", {}).get("175", -1) >= 7,
         "Department floor8 membership counter175 is not proven")
    need(status["bag"]["contents"].get("MEMBERSHIPCARD", 0) >= 1,
         "Owned Membership Card required")
    bag = status["bag"]["contents"]
    start = PHASES.index(from_phase)
    cart = []
    for key, (phase, name, target, price) in ITEMS.items():
        qty = max(0, target - bag.get(key, 0))
        need(not qty or PHASES.index(phase) >= start,
             "Earlier phase target missing: " + key + "; do not skip that vendor")
        if qty:
            cart.append(dict(item=key, phase=phase, name=name, quantity=qty,
                             unit_price=price, total=qty * price))
    cost = sum(c["total"] for c in cart)
    money = status["trainer"]["money"]
    # The completed build/Lens proof means its17000 has already been spent.
    need(money >= cost, "Insufficient actual frozen money for the deficit cart")
    commands = {p: [] for p in PHASES[start:]}

    def cmd(phase, script, *args, purchase=None):
        row = dict(script=script, args=list(args))
        if purchase:
            row["purchase"] = purchase
        commands[phase].append(row)

    def buy(phase, mid, eid):
        rows = [c for c in cart if c["phase"] == phase]
        if not rows:
            return
        cmd(phase, "eventq", mid, eid, "talk")
        cmd(phase, "vendor-ready", mid, eid)
        cmd(phase, "mart_open")
        for row in rows:
            cmd(phase, "shop_buy", row["name"], row["quantity"], row["unit_price"],
                purchase=row)
        cmd(phase, "mart_exit")

    if "dept" in commands:
        cmd("dept", "fly_to", 520, "--carrier", "Tranquill")
        if any(c["phase"] == "dept" for c in cart):
            for script, args in [("eventq", (520, 101, "enter")),
                                 ("eventq", (112, 6, "enter")),
                                 ("eventq", (113, 1, "talk")),
                                 ("dept_greet", ()), ("dept_floor", (8,))]:
                cmd("dept", script, *args)
            buy("dept", 4, 4)
            for script, args in [("eventq", (4, 6, "enter")),
                                 ("eventq", (113, 1, "talk")),
                                 ("dept_greet", ()), ("dept_floor", (1,)),
                                 ("eventq", (112, 1, "enter"))]:
                cmd("dept", script, *args)
    if "herbs" in commands and any(c["phase"] == "herbs" for c in cart):
        cmd("herbs", "city_enter", 520, 611)
        buy("herbs", 611, 2)
        cmd("herbs", "city_enter", 611, 520)
    if "ultra" in commands:
        cmd("ultra", "fly_to", 519, "--carrier", "Tranquill")
        if any(c["phase"] == "ultra" for c in cart):
            cmd("ultra", "eventq", 519, 116, "enter")
            buy("ultra", 38, 5)
            cmd("ultra", "eventq", 38, 6, "enter")
    cmd("return-circus", "fly_to", 355, "--carrier", "Tranquill")
    cmd("return-circus", "checkpoint", "Circus-restocked129")
    return dict(proposal=True, executed=False, from_phase=from_phase, cart=cart,
                actual_start_money=money, total_cost=cost, expected_money=money-cost,
                commands=commands, final_checkpoint="Circus-restocked129")


def source_proof(navigation):
    """Installed asset reads only; no game, UI, save or planner reads."""
    facts = []
    for mid, eid, wanted in [(4, 4, "pbPokemonMart"), (38, 5, "pbDefaultMart"),
                              (611, 2, "pbPokemonMart")]:
        raw = subprocess.check_output(["ruby", str(ROOT / "scripts/event_dump.rb"),
                                       str(mid), str(eid)], stderr=subprocess.DEVNULL)
        event = json.loads(raw)
        page = event["pages"][0]
        condition = page["condition"]
        need(not any(condition.get(k) for k in ("switch1_valid", "switch2_valid",
                     "variable_valid", "self_switch_valid")), "Source base vendor page changed")
        script = "\n".join(str(c["parameters"][0]) for c in page["list"]
                            if c["code"] in (355, 655))
        need(wanted in script and not any(c["code"] in (102, 301) for c in page["list"]),
             "Source merchant script changed")
        if mid != 611:
            need(len(event["pages"]) == 1, "Merchant acquired an unreviewed higher page")
        else:
            need(len(event["pages"]) == 3 and all(
                p["condition"].get("switch2_valid")
                and p["condition"].get("switch2_id") == 719
                for p in event["pages"][1:]), "Herb higher-page conditions changed")
            need(navigation["switches"]["719"] is False, "Herb source page not proven")
        stock = re.findall(r":([A-Z][A-Z0-9]+)", script)
        for key, (phase, _, _, _) in ITEMS.items():
            if phase == {4: "dept", 611: "herbs"}.get(mid):
                need(key in stock, "Source stock missing " + key)
        facts.append(dict(map=mid, event=eid, page=0, event_sha256=hashlib.sha256(raw).hexdigest()))
    itemtext = (GAME / "Scripts/Reborn/itemtext.rb").read_text()
    for key, (_, name, _, price) in ITEMS.items():
        match = re.search(r"(?m)^\s*:" + key + r"\s*=>\s*\{(.*?)\n\s*\},", itemtext, re.S)
        need(match is not None, "Installed item missing " + key)
        need(re.search(r":price\s*=>\s*" + str(price) + r"\b", match[1]) is not None,
             "Installed price differs for " + name)
    mart = (GAME / "Scripts/Mart.rb").read_text()
    need(re.search(r"when 13\.\.16\s+stock\s*=\s*\[([^]]*:ULTRAPOTION[^]]*)\]", mart),
         "Installed16-badge Ultra Potion stock changed")
    return facts


def overworld_guard(text):
    lines = [v.strip().lower() for v in text.splitlines() if v.strip()]
    lines = [v for v in lines if re.sub(r"[^a-z]", "", v) != "pokemonreborn"]
    need(not re.search(r"\bfight\b|\bwild\b|\bpp\s*:|\bhp\b", "\n".join(lines)),
         "Unexpected battle/party screen; no queue action")
    need(len(lines) < 4 and all(len(v) < 55 for v in lines)
         and not any(re.search(r"\b(yes|no|buy|sell|quit|cancel|bag|save|options)\b", v)
                     for v in lines), "Fresh ordinary overworld required")


def vendor_guard(text):
    low = text.lower()
    need("buy" in low and "sell" in low and "quit" in low
         and any(v in low for v in ("welcome", "how may i serve", "anything else")),
         "Expected source merchant Buy/Sell/Quit greeting; no advancement")
    need(not any(v in low for v in ("how many", "would you", "fight", "break:")),
         "Unreviewed merchant page/dialogue; stop")


def vendor_ready_public():
    """Retry only OCR from the same public native menu crop; never send keys."""
    from play import read, NATIVE
    text=read()
    try:
        vendor_guard(text)
        return
    except ValueError:
        from PIL import Image
        image=Image.open(NATIVE); w,h=image.size
        crop=ROOT/"work/agate-vendor-menu-public.png"
        image.crop((int(w*.78),int(h*.38),int(w*.99),int(h*.77))).resize((700,1100),Image.Resampling.NEAREST).save(crop)
        rows=json.loads(subprocess.check_output([str(ROOT/"scripts/observe"),str(crop)]))
        vendor_guard(text+"\n"+"\n".join(r["text"] for r in rows))


def final_proof(before, after, proposal):
    need(after["map"] == 355, "Final checkpoint is not Circus")
    training_proof(after)
    need(identity(after) == identity(before), "Travel unexpectedly changed the reviewed party")
    need(after["trainer"]["money"] == proposal["expected_money"],
         "Final native money does not reconcile all receipts")
    purchased = {c["item"]: c["quantity"] for c in proposal["cart"]}
    for key, (_, _, target, _) in ITEMS.items():
        expected = before["bag"]["contents"].get(key, 0) + purchased.get(key, 0)
        actual = after["bag"]["contents"].get(key, 0)
        need(actual == expected and actual >= target, "Final native bag differs: " + key)


def execute(status, navigation, proposal, journal_path, status_path, nav_path):
    # Import only after explicit execution and all frozen/source preflight checks.
    from play import read
    from locate import locate
    saved = datetime.fromisoformat(status["save_mtime"]).timestamp()
    need(-5 <= time.time() - saved <= 300,
         "Execute requires a fresh normal checkpoint, at most300 seconds old")
    need(status_path.resolve().is_relative_to(ROOT) and nav_path.resolve().is_relative_to(ROOT)
         and journal_path.resolve().is_relative_to(ROOT), "Keep evidence/journal in workspace")
    actual_nav = json.loads((ROOT / "notes/navigation-state.json").read_text())
    need(actual_nav.get("switches", {}).get("719") is False
         and actual_nav.get("variables", {}).get("175", -1) >= 7,
         "Current planner merchant/floor flags differ; refresh a normal checkpoint")
    need(not journal_path.exists(), "Journal already exists; never replay a partial phase. "
         "Recover manually, make a fresh entrance checkpoint, use a new journal/from-phase.")
    final_path = ROOT / "notes/Circus-restocked129-status.json"
    need(not final_path.exists(), "Circus-restocked129 already exists; preserve its evidence")
    state = dict(schema=1, status=str(status_path.resolve()), status_sha256=digest(status_path),
                 navigation=str(nav_path.resolve()), navigation_sha256=digest(nav_path),
                 start_epoch=time.time(), proposal=proposal, phases=[], verified=False)
    journal_path.parent.mkdir(parents=True, exist_ok=True)
    with journal_path.open("x") as f:
        json.dump(state, f, indent=2)

    def write():
        temp = journal_path.with_suffix(journal_path.suffix + ".tmp")
        temp.write_text(json.dumps(state, indent=2) + "\n")
        temp.replace(journal_path)

    def map_guard(mid):
        overworld_guard(read())
        need(locate(mid)[0] == mid, "Observed map differs; queue stopped")

    try:
        for phase, commands in proposal["commands"].items():
            entry = dict(phase=phase, state="pending", entry_epoch=time.time(),
                         commands=commands, finished_steps=0, receipts=[])
            state["phases"].append(entry)
            write()
            map_guard(START_MAP[phase])
            for index, command in enumerate(commands):
                entry["pending_step"] = index
                write()
                if command["script"] == "vendor-ready":
                    vendor_ready_public()
                else:
                    result = subprocess.run([sys.executable, str(ROOT / "scripts" /
                                             (command["script"] + ".py")),
                                             *map(str, command["args"])],
                                            text=True, capture_output=True)
                    entry["last_output_tail"] = (result.stdout + result.stderr)[-6000:]
                    write()
                    if result.returncode:
                        print(entry["last_output_tail"], flush=True)
                        raise ValueError("Helper stopped: " + command["script"])
                    if command.get("purchase"):
                        row = command["purchase"]
                        need("PURCHASE VERIFIED " + row["name"] + " " + str(row["quantity"])
                             in result.stdout, "Purchase receipt not verified; stop")
                        entry["receipts"].append(dict(row, verified_epoch=time.time()))
                        print("PURCHASE VERIFIED", row["name"], row["quantity"], flush=True)
                    else:
                        print("QUEUE STEP VERIFIED", phase, command["script"], command["args"], flush=True)
                entry["finished_steps"] = index + 1
                entry.pop("pending_step", None)
                write()
            map_guard(END_MAP[phase])
            if phase == "return-circus":
                after = json.loads(final_path.read_text())
                need(final_path.stat().st_mtime >= state["start_epoch"], "Final checkpoint is stale")
                final_proof(status, after, proposal)
                state["final_status_sha256"] = digest(final_path)
                state["verified"] = True
            entry.update(state="complete", complete_epoch=time.time())
            write()
    except BaseException as error:
        state["stopped_epoch"] = time.time()
        state["stop_reason"] = str(error)
        write()
        raise
    print("CIRCUS RESTOCK VERIFIED; Lens still held; use finish-lens separately.", flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--status", required=True, type=Path)
    parser.add_argument("--navigation", type=Path,
                        help="Matching full frozen navigation; defaults to checkpoint sibling")
    parser.add_argument("--from-phase", choices=PHASES, default="dept")
    parser.add_argument("--journal", type=Path,
                        default=ROOT / "work/agate-shopping-129-journal.json")
    parser.add_argument("--execute", action="store_true")
    args = parser.parse_args()
    nav_path = args.navigation or args.status.with_name(
        args.status.name.replace("-status.json", "-navigation.json"))
    need(nav_path != args.status, "Status filename must end-status.json or pass--navigation")
    status = json.loads(args.status.read_text())
    navigation = json.loads(nav_path.read_text())
    proposal = plan(status, navigation, args.from_phase)
    proposal["source_proof"] = source_proof(navigation)
    print(json.dumps(proposal, indent=2), flush=True)
    if args.execute:
        execute(status, navigation, proposal, args.journal, args.status, nav_path)


if __name__ == "__main__":
    main()
