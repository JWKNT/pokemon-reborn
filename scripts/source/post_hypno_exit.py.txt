"""Guarded ordinary controls: post-Hypno758 loop and recovery to Calcenon.

Import/source validation send no inputs. --execute requires the frozen verified
Hypno post-bag report BEFORE recovery, medicine, held-item or PC changes.
Whitelisted story touches stop movement queues at the first meaningful event.
No future battle is started. Root retains ownership of recording/archive/saves.
"""
from __future__ import annotations

import argparse
import difflib
import functools
import hashlib
import json
import pathlib
import re
import subprocess
import sys
import time

ROOT = pathlib.Path(__file__).resolve().parents[1]
STATE_FILE = ROOT / "notes/navigation-state.json"
RECEIPTS = ROOT / "work/post-hypno-batch-progress.json"
PHASES = ["zel", "shade", "luna", "void-exit", "recovery"]
TOUCHES = {758: {17, 36, 62, 63, 89, 91, 92, 28, 99, 100, 30, 101, 102, 103, 107, 108, 35},
           759: {4, 6, 7, 8, 9, 10, 11, 12, 5}}
FOLLOW = {89: (90, 1), 30: (104, 0), 101: (104, 0),
          102: (105, 0), 103: (105, 0), 107: (31, 1), 108: (31, 1)}
RECOVERY = [(735, 4, 0), (715, 85, 0), (734, 16, 0), (735, 7, 0), (735, 4, 2)]


def need(value, message):
    if not value:
        raise ValueError(message)


@functools.lru_cache(maxsize=None)
def source_event(mid, eid):
    return json.loads(subprocess.check_output(
        ["ruby", str(ROOT / "scripts/event_dump.rb"), str(mid), str(eid)],
        stderr=subprocess.DEVNULL))


def no_battle_or_choice(commands, *, anna_choice=False):
    choices = [c for c in commands if c["code"] == 102]
    need(not any(c["code"] in [103, 104, 301] or any(token in str(c["parameters"])
                 for token in ["pbTrainerBattle", "pbDoubleTrainerBattle", "pbWildBattle"])
                 for c in commands), "Installed source contains an unapproved input or battle")
    need(not choices or anna_choice and len(choices) == 1 and
         choices[0]["parameters"][0] == ["Yes", "No"], "Installed source contains an unapproved choice")


def validate_sources():
    proof = []
    pairs = {(mid, eid) for mid, ids in TOUCHES.items() for eid in ids}
    pairs |= {(758, eid) for eid in [33, 34, 90, 104, 105, 31]}
    for mid, eid in sorted(pairs):
        event = source_event(mid, eid)
        for page in event["pages"]:
            no_battle_or_choice(page["list"])
        proof.append({"map": mid, "event": eid, "position": [event["x"], event["y"]], "approved": True})
    for mid, eid, page_index in RECOVERY:
        page = source_event(mid, eid)["pages"][page_index]
        need(page["trigger"] == 3, f"Expected automatic recovery scene {mid}E{eid}p{page_index}")
        no_battle_or_choice(page["list"], anna_choice=(mid, eid, page_index) == (735, 4, 2))
        proof.append({"map": mid, "event": eid, "page": page_index, "autorun": True})
    return proof


def frozen_post_gate(status_path, report_path):
    status_path, report_path = status_path.resolve(), report_path.resolve()
    need(status_path.is_relative_to(ROOT) and report_path.is_relative_to(ROOT), "Use explicit frozen R evidence only")
    status, report = [json.loads(path.read_text()) for path in [status_path, report_path]]
    # status_full.rb intentionally exports only a small switch subset and
    # omits1874. Victory is bound by the retained125 reconciliation; the full
    # navigation snapshot's1874 is checked independently before any UI input.
    need(status.get("map") == 758, "Frozen outside-battle Hypno post-status on758 required")
    need(report.get("status") == "verified_counts" and report.get("errors") == [] and
         report.get("native_save_inventories_verified") is True,
         "Freeze and reconcile native post-Hypno bag BEFORE running this route")
    rows = report.get("per_round", [])
    need(len(rows) == 1 and rows[0].get("major_id") == 125, "Require the one-Hypno125 item report")
    bound = report.get("evidence", {}).get("after", {})
    need(bound.get("sha256") == hashlib.sha256(status_path.read_bytes()).hexdigest(),
         "Item report is not bound to this exact frozen post-status")
    need(isinstance(status.get("bag", {}).get("contents"), dict), "Frozen complete post-bag inventory missing")
    return status


def record(kind, **data):
    value = json.loads(RECEIPTS.read_text()) if RECEIPTS.exists() else {"events": []}
    value["events"].append({"epoch": time.time(), "kind": kind, **data})
    RECEIPTS.write_text(json.dumps(value, indent=2) + "\n")


def normalized(text):
    return re.sub("[^a-z]", "", text.lower()).replace("pokemonreborn", "")


def mirror_page(mid, eid, page):
    """Planner-note effects only, AFTER the approved scene actually settles."""
    state = json.loads(STATE_FILE.read_text())
    for command in page["list"]:
        if command["indent"] != 0:
            continue
        a = command["parameters"]
        if command["code"] == 123:
            state.setdefault("self_switches", {})[f"{mid},{eid},{a[0]}"] = a[1] == 0
        elif command["code"] == 121 and a[0] == a[1]:
            state.setdefault("switches", {})[str(a[0])] = a[2] == 0
        elif command["code"] == 122 and a[0] == a[1] and a[2:4] == [0, 0]:
            state.setdefault("variables", {})[str(a[0])] = a[4]
    STATE_FILE.write_text(json.dumps(state) + "\n")


def model(mid, xy):
    value = json.loads(subprocess.check_output(
        ["ruby", str(ROOT / "scripts/route_map.rb"), str(mid), *map(str, xy)], stderr=subprocess.DEVNULL))
    state = json.loads(STATE_FILE.read_text())
    if mid == 758:
        need(state.get("switches", {}).get("1874") is True, "Source planning status must confirm Hypno won")
        need(not any("pbTrainerBattle" in str(e.get("list", [])) for e in value["events"].values()),
             "Unexpected active battle event in post-Hypno model")
        # Installed animations remove these actors at their END. The saved
        # planner may retain original coordinates until the next normal save.
        if state.get("self_switches", {}).get("758,90,A"):
            value["events"]["25"].update(character="", through=True)
        if state.get("variables", {}).get("391", 0) >= 33:
            value["events"]["26"].update(character="", through=True)
    return value


def prefix_at_first_touch(value, nodes, keys, chunk_limit, phase):
    keys, nodes = keys[:chunk_limit], nodes[:chunk_limit + 1]
    for i, xy in enumerate(nodes[1:], 1):
        hits = [(int(eid), event) for eid, event in value["events"].items()
                if event["trigger"] in [1, 2] and (event["x"], event["y"]) == xy and
                any(c["code"] not in [0, 108, 408] for c in event.get("list", []))]
        if not hits:
            continue
        need(len(hits) == 1, f"Ambiguous story touch at{value['map']}{xy}")
        eid, event = hits[0]
        need(eid in TOUCHES.get(value["map"], set()), f"Unplanned story touch{value['map']}E{eid}; no batch sent")
        need(not (value["map"] == 758 and eid == 35 and phase != "luna"), "Luna transfer reached outside its phase")
        need(not (value["map"] == 759 and eid == 5 and phase != "void-exit"), "Void exit reached outside its phase")
        return keys[:i], nodes[:i + 1], (eid, event)
    return keys, nodes, None


def settle(mid, eid, active, *, transfer=False):
    from void_batch_route import textbox, world_guard
    from play import read
    event = source_event(mid, eid)
    matching = [page for page in event["pages"] if page["list"] == active["list"]]
    need(matching, f"Active source page differs for{mid}E{eid}")
    page = matching[-1]
    commands = list(page["list"])
    follower = FOLLOW.get(eid) if mid == 758 else None
    if follower:
        follow_event = source_event(mid, follower[0])
        follow_page = follow_event["pages"][follower[1]]
        commands += follow_page["list"]
    no_battle_or_choice(commands)
    text = read()
    blocks = []
    for command in commands:
        if command["code"] == 101:
            blocks.append(str(command["parameters"][0]))
        elif command["code"] == 401 and blocks:
            blocks[-1] += " " + str(command["parameters"][0])
    if textbox() and blocks:
        n = normalized(text)
        need(any(difflib.SequenceMatcher(None, n, normalized(block)).ratio() >= .50 for block in blocks),
             f"Visible dialogue does not match approved{mid}E{eid}: {text}")
    args = ["--burst", "--world-settle", "20" if follower or eid in [91, 92, 33, 34, 35] else "9"]
    if follower:
        # Existing helper applies --source-page after --follow-source; avoid
        # combining them or it would discard the follower's source commands.
        args += ["--follow-source", str(mid), str(follower[0])]
    else:
        args += ["--source-page", str(event["pages"].index(page))]
    if any(c["code"] in [241, 242] for c in commands):
        args += ["--log-scripted-bgm"]
    run("linear_dialog", mid, eid, *args)
    if not transfer:
        world_guard()
    mirror_page(mid, eid, page)
    if follower:
        mirror_page(mid, follower[0], follow_page)
    record("approved-scene-settled", map=mid, event=eid, follow=follower)


def run(script, *args):
    subprocess.run([sys.executable, str(ROOT / "scripts" / (script + ".py")), *map(str, args)], check=True)


def walk(mid, goal, phase, chunk_limit, transfer_map=None):
    from play import act
    from locate import locate
    from void_batch_route import world_guard
    from void_static_paths import path
    seen = []
    for _ in range(150):
        world_guard()
        actual, x, y = locate(mid)
        need(actual == mid, f"Unexpected map{actual}; expected{mid}")
        world_guard()
        if (x, y) == goal:
            return actual, x, y
        seen.append((x, y))
        need(len(seen) < 3 or len(set(seen[-3:])) > 1, "Repeated coordinate; movement timing/actor review")
        value = model(mid, (x, y))
        keys, nodes = path(value, (x, y), goal)
        keys, nodes, stop = prefix_at_first_touch(value, nodes, keys, chunk_limit, phase)
        need(keys, "Empty planned route away from target")
        sequence = []
        for key in keys:
            sequence.extend([key[5:] + ":.12", "wait:.9"] if key.startswith("jump:") else [key + ":.12"])
        print("POST-HYPNO SEGMENT", mid, (x, y), "->", nodes[-1], len(keys), "touch", stop[0] if stop else None, flush=True)
        try:
            act(*sequence)
        except subprocess.CalledProcessError as error:
            if error.returncode != 2:
                raise
            # A capture interruption may stop midway through a movement batch.
            # Restore capture, require a genuine overworld, and replan from the
            # next observed coordinate rather than replaying unexecuted keys.
            from locate import capture_ready
            capture_ready()
            world_guard()
            record("capture-recovered-replan", map=mid, planned_endpoint=list(nodes[-1]))
            print("CAPTURE RECOVERED; replan from actual coordinate", flush=True)
            continue
        if stop:
            eid, active = stop
            is_exit = (mid, eid) == (759, 5)
            if is_exit:
                #735 immediately starts the first recovery autorun. No extra
                # coordinate hotkey/dialogue taps are sent during that scene.
                record("void-exit-touch-sent", map=759, event=5, expected_map=735)
                return 735, None, None
            settle(mid, eid, active, transfer=transfer_map is not None and eid == 35)
            if transfer_map is not None and eid == 35:
                actual = locate(transfer_map)
                need(actual[0] == transfer_map, "Luna did not reach759")
                return actual
    raise ValueError("Post-Hypno movement limit")


def recovery():
    """Source-bound autoruns; Anna is the only approved choice in the chain."""
    from play import act, read, snap
    from void_batch_route import textbox, world_guard
    from locate import locate
    blocks, music_anchors, music_seen = [], [], set()
    for mid, eid, pi in RECOVERY:
        cs = source_event(mid, eid)["pages"][pi]["list"]
        no_battle_or_choice(cs, anna_choice=(mid, eid, pi) == (735, 4, 2))
        for c in cs:
            if c["code"] == 101:
                blocks.append(str(c["parameters"][0]))
            elif c["code"] == 401 and blocks:
                blocks[-1] += " " + str(c["parameters"][0])
        # Autoruns cross maps without a safe coordinate hotkey. Preserve their
        # installed BGM changes using actually observed following text anchors.
        for index, command in enumerate(cs):
            if command["code"] not in [241, 242]:
                continue
            following = []
            for c in cs[index + 1:]:
                if c["code"] == 101:
                    if following:
                        break
                    following = [str(c["parameters"][0])]
                elif c["code"] == 401 and following:
                    following.append(str(c["parameters"][0]))
            if following:
                audio = command["parameters"][0]
                track = audio.get("name") if command["code"] == 241 and audio.get("volume", 100) > 0 else "__silence__"
                music_anchors.append(((mid, eid, pi, index), normalized(" ".join(following)), track))
    norms = [normalized(block) for block in blocks]
    anchor = normalized("ANNA: you're coming too, right?")
    last, repeats, empty = "", 0, 0
    for _ in range(1500):
        rows = snap()
        text = "\n".join(row["text"] for row in rows)
        low, n = text.lower(), normalized(text)
        for identity, anchor_text, track in music_anchors:
            if identity not in music_seen and difflib.SequenceMatcher(None, n, anchor_text).ratio() >= .70:
                with (ROOT / "recordings/music-events.jsonl").open("a") as stream:
                    stream.write(json.dumps({"epoch": time.time(), "bgm": {"name": track},
                                             "map": identity[0], "event": identity[1], "source_page": identity[2],
                                             "command_index": identity[3], "source": "inspected-scripted-BGM",
                                             "evidence": text}) + "\n")
                music_seen.add(identity)
        labels = {row["text"].strip().lower() for row in rows}
        need(not re.search(r"\bhp\b|\bpp:|choose a pok", low) and
             not all(label in labels for label in ["fight", "bag", "run"]),
             "Recovery interrupted by battle/party screen")
        if labels & {"yes", "no", "ves", "tes", "mo", "ro"}:
            need(difflib.SequenceMatcher(None, n, anchor).ratio() >= .48 or "comingtooright" in n,
                 "Unrecognized recovery choice; no answer sent")
            run("choose_dialog", "Yes|No", "Yes")
            run("linear_dialog", 735, 4, "--source-page", 2, "--past-choice", "--world-settle", 12)
            world_guard()
            arrived = locate(413)
            need(arrived[0] == 413, "Anna travel did not reach Calcenon")
            # Only the completed Yes branch, not the mutually exclusive No.
            state = json.loads(STATE_FILE.read_text())
            state.setdefault("variables", {})["391"] = 49
            state.setdefault("switches", {})["921"] = True
            STATE_FILE.write_text(json.dumps(state) + "\n")
            record("recovery-anna-yes-completed", map=413, position=list(arrived[1:]))
            print("SAFE CALCENON ARRIVAL", arrived, "bag/medicine/PC flows remain root-owned", flush=True)
            return
        if text != last:
            print(text, flush=True)
        repeats = repeats + 1 if n == normalized(last) else 0
        last = text
        need(repeats < 8 or not textbox(), "Repeated recovery dialogue; no blind replay")
        matched = bool(n) and any(difflib.SequenceMatcher(None, n, block).ratio() >= .52 for block in norms)
        try:
            if textbox() or matched:
                empty = 0
                act("c", "wait:.35")
            else:
                empty += 1
                need(empty <= 90, "Recovery settled without Anna's inspected choice; review actual map/phase")
                act("wait:.5")
        except subprocess.CalledProcessError as error:
            if error.returncode != 2:
                raise
            from locate import capture_ready
            capture_ready()
            record("recovery-capture-restored-reread", observed_text=text)
            print("CAPTURE RECOVERED; re-read current dialogue without replay", flush=True)
    raise ValueError("Recovery scene limit; resume --from-phase recovery after inspecting the actual dialogue")


def execute(args, frozen):
    from play import act
    from locate import locate
    from void_batch_route import world_guard
    state = json.loads(STATE_FILE.read_text())
    need(state.get("switches", {}).get("1874") is True, "Root's normal post-Hypno checkpoint must sync1874True")
    if args.from_phase == "recovery":
        recovery()
        return
    world_guard()
    actual = locate()
    if args.from_phase:
        first = PHASES.index(args.from_phase)
    elif actual[0] == 758:
        first = 0
    elif actual[0] == 759:
        first = 3
    else:
        raise ValueError("At an automatic recovery dialogue use explicit --from-phase recovery, not coordinate resume")
    for phase in PHASES[first:]:
        if phase == "recovery":
            recovery()
        elif phase == "void-exit":
            need(locate()[0] == 759, "Void exit phase expects759 overworld")
            walk(759, (43, 191), phase, args.chunk_tiles, transfer_map=735)
        else:
            need(locate()[0] == 758, f"{phase} phase expects758 overworld")
            eid, goal, facing = {"zel": (33, (11, 146), "right"),
                                 "shade": (34, (17, 180), "down"),
                                 "luna": (35, (40, 176), None)}[phase]
            state = json.loads(STATE_FILE.read_text())
            if state.get("self_switches", {}).get(f"758,{eid},A"):
                print("SOURCE-COMPLETED PHASE", phase, flush=True)
            else:
                walk(758, goal, phase, args.chunk_tiles, transfer_map=759 if phase == "luna" else None)
                if facing:
                    active = model(758, goal)["events"][str(eid)]
                    act(facing + ":.03", "c", "wait:.6")
                    settle(758, eid, active)
        # Input receipt is not transfer/story proof. The forced recovery chain
        # itself is verified only at the final Calcenon coordinate check.
        record("phase-touch-sent" if phase == "void-exit" else "phase-completed", phase=phase)
        if args.stop_phase == phase:
            print("STOPPED AFTER APPROVED TOUCH; RECOVERY UNVERIFIED" if phase == "void-exit" else "STOPPED AFTER APPROVED PHASE", phase, flush=True)
            return


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--execute", action="store_true")
    parser.add_argument("--from-phase", choices=PHASES)
    parser.add_argument("--stop-phase", choices=PHASES)
    parser.add_argument("--chunk-tiles", type=int, default=56)
    parser.add_argument("--post-status", type=pathlib.Path)
    parser.add_argument("--item-report", type=pathlib.Path)
    args = parser.parse_args()
    need(1 <= args.chunk_tiles <= 84, "Chunk bound must be1..84")
    proof = validate_sources()
    print(json.dumps({"proposal": True, "phases": PHASES, "source_validation": proof,
                      "recovery_is_uninterrupted_autoruns": True,
                      "no_controllable_715_scale_window": True}, indent=2), flush=True)
    if args.execute:
        need(args.post_status is not None and args.item_report is not None,
             "--execute requires frozen --post-status and verified --item-report")
        frozen = frozen_post_gate(args.post_status, args.item_report)
        execute(args, frozen)


if __name__ == "__main__":
    main()
