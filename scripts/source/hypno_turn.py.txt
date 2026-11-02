"""Run one explicitly requested Hypno action through existing ordinary UI helpers.

No action selection, native battle state, battle logs, or unseen-outcome inference.
Importing this module is safe; only main() captures a public screen or sends inputs.
"""
from __future__ import annotations

import argparse
import difflib
import json
import pathlib
import re
import subprocess
import sys
import time
import unicodedata

ROOT = pathlib.Path(__file__).resolve().parent.parent
SCREEN_JOURNAL = ROOT / "recordings/screens.jsonl"
OUTPUT_DIR = ROOT / "work/hypno-public-turns"
SELF_ITEMS = {"xattack", "xdefend", "xspatk", "xspdef", "xspeed", "xaccuracy", "direhit", "guardspec"}
MESSAGE_PATTERN = re.compile(
    r"used|fainted|critical|super effective|not very effective|missed|avoided|"
    r"hypnosis|safeguard|protected|calm mind|dark pulse|dream eater|crunch|"
    r"fell|rose|raised|sharply|asleep|sleep|woke|restored|recovered|healed|"
    r"wore off|no longer|failed|flinch|defeated|for winning|out of usable", re.I)
# Public pixel-font OCR substitutes these visually identical Cyrillic letters
# inside otherwise Latin names (observed Hypnо and Нурnо). This is a small glyph
# alias table, not general transliteration or a relaxed species-name matcher.
NAME_CONFUSABLES = str.maketrans({
    "Н": "H", "н": "h", "У": "Y", "у": "y", "Р": "P", "р": "p", "О": "O", "о": "o",
    "А": "A", "а": "a", "С": "C", "с": "c", "Е": "E", "е": "e", "І": "I", "і": "i",
})
RUN_LABEL_ALIASES = {"run", "riun"}
RUN_I_CONFUSABLES = str.maketrans({"Ι": "I", "ι": "i", "І": "I", "і": "i"})


def canonical(value: str) -> str:
    plain = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]", "", plain.lower())


def normalized_name_text(text: str) -> str:
    value = unicodedata.normalize("NFKD", text).translate(NAME_CONFUSABLES)
    return "".join(c for c in value if not unicodedata.combining(c)).lower()


def name_matches(text: str, name: str) -> bool:
    # A HUD row can contain its name, gender sign and level together. Match a
    # complete word only, allowing one ordinary OCR substitution in long names.
    # Unicode word boundaries prevent accepting a Latin-name fragment embedded
    # in a larger unrecognized-script word. Unmapped letters remain uncertain.
    normalized = normalized_name_text(text)
    if name.lower()=='klinklang':
        # Public Xavier134 HUD rendered the same installed name as two OCR
        # words, while its independent current-actor prompt retained Klinklang.
        normalized=re.sub(r'(?<!\w)klink\s+lang(?!\w)','klinklang',normalized)
    if '-' in name:
        # Preserve the COMPLETE named species token. Splitting Kommo-o into
        # "Kommo"/"o" previously rejected even an exact public HUD. This is
        # punctuation handling, not a fuzzy match for a different species.
        parts = name.lower().split('-')
        pattern = r'(?<!\w)' + r'(?:\s*[-\u2010\u2011]\s*|\s+)'.join(map(re.escape, parts)) + r'(?!\w)'
        return re.search(pattern, normalized) is not None
    words = re.findall(r"[^\W\d_]+", normalized)
    return any(word.isascii() and (word == name.lower() or
               (len(word) >= 5 and difflib.SequenceMatcher(None, word, name.lower()).ratio() >= .87))
               for word in words)


def run_command_row(row: dict) -> bool:
    """Exact standalone RUN/observed RIUN in the lower-right command cell."""
    label = unicodedata.normalize("NFKC", str(row.get("text", ""))).translate(RUN_I_CONFUSABLES)
    label = label.strip(" \t\r\n›>•").lower()
    return label in RUN_LABEL_ALIASES and .70 <= float(row.get("x", -1)) <= .98 \
        and .80 <= float(row.get("y", -1)) <= .95


def command_guard(rows: list[dict], *, captured_at: float, now: float) -> dict:
    """Pure, conservative fresh-command/actor/foe guard for the singles fight."""
    if not (-2 <= now - captured_at <= 15):
        raise ValueError("Public command capture is not fresh")
    if not rows or any("text" not in row or "y" not in row for row in rows):
        raise ValueError("Public OCR positions are required for the command guard")
    low = "\n".join(str(row["text"]) for row in rows).lower()
    if re.search(r"de.?feated|for winning|out of usable|choose a pok|switch in|change pok|switch your", low):
        raise ValueError("Victory, replacement, or unexpected input screen; no action sent")
    bottom = " ".join(str(row["text"]).lower() for row in rows if float(row["y"]) >= .65)
    if re.search(r"pp\s*[:.]|pp.?\s*\d+\s*[/0]\s*\d+", bottom):
        raise ValueError("Move grid is open; no action sent")
    if not all(re.search(r"\b" + label + r"\b", bottom) for label in ("fight", "bag")) \
            or not any(run_command_row(row) for row in rows):
        raise ValueError("Fresh battle command labels Fight/Bag/Run are required")
    foe_rows = [row for row in rows if float(row["y"]) < .37 and name_matches(str(row["text"]), "Hypno")]
    actor_rows = [row for row in rows if .37 <= float(row["y"]) < .70 and name_matches(str(row["text"]), "Arcanine")]
    if not foe_rows or not actor_rows:
        raise ValueError("Expected visible Hypno foe HUD and Arcanine actor HUD")
    # A contradictory actor in a visible command prompt must not pass merely
    # because Arcanine appears elsewhere on the image.
    prompt = re.search(r"\bwhat\s+will\s+([^\W\d_]+)\s+do\b", normalized_name_text(bottom))
    if prompt and not name_matches(prompt.group(1), "Arcanine"):
        raise ValueError("Command prompt names a different acting Pokemon")
    return {"actor": "Arcanine", "foe": "Hypno", "capture_epoch": captured_at,
            "guard_age_seconds": round(now - captured_at, 3),
            "actor_hud": actor_rows, "foe_hud": foe_rows,
            "observed_command_text": bottom}


def final_classification(rows: list[dict], *, captured_at: float, now: float) -> str:
    text = "\n".join(str(row["text"]) for row in rows).lower()
    if re.search(r"de.?feated|for winning", text):
        return "visible_victory_message"
    if "out of usable" in text:
        return "visible_no_usable_pokemon_message"
    if "choose a pok" in text or ("cancel" in text and text.count("hp") >= 5):
        return "visible_replacement_menu"
    try:
        command_guard(rows, captured_at=captured_at, now=now)
    except ValueError:
        return "review_required"
    return "fresh_arcanine_hypno_command"


def helper_argv(args: argparse.Namespace, root: pathlib.Path = ROOT) -> list[str]:
    if args.item is not None:
        cmd = [sys.executable, str(root / "scripts/battle_item.py"), args.item, "Arcanine"]
        if canonical(args.item) in SELF_ITEMS:
            cmd.append("--active")
        return cmd
    return [sys.executable, str(root / "scripts/battle_move.py"), str(args.move_slot), "--watch"]


def read_generated_screens(path: pathlib.Path, offset: int, start: float, end: float) -> tuple[list[dict], list[str]]:
    """Read only appended public OCR records within this invocation's timespan.

    The existing journal has no caller ID. Ordinary input/capture helpers must
    be run sequentially; unrelated concurrent public captures cannot be proven
    to belong to this wrapper and are not silently attributed as turn outcomes.
    """
    issues = []
    records = []
    if not path.exists():
        return records, ["Public screen journal is missing"]
    if path.stat().st_size < offset:
        return records, ["Public screen journal was truncated during the wrapper"]
    with path.open("rb") as stream:
        stream.seek(offset)
        lines = stream.read().splitlines()
    for line in lines:
        try:
            value = json.loads(line)
            epoch = float(value["epoch"])
            if start <= epoch <= end and isinstance(value.get("text"), list):
                records.append({"epoch": epoch, "ocr_complete_epoch": value.get("ocr_complete_epoch"),
                                "text": [str(text) for text in value["text"]]})
        except (ValueError, KeyError, TypeError, json.JSONDecodeError) as exc:
            issues.append("Unparsed appended public OCR line: " + str(exc))
    return records, issues


def deduplicate_screens(records: list[dict]) -> list[dict]:
    """Merge only adjacent identical OCR frames; repeated later events survive."""
    result = []
    for row in records:
        signature = tuple(" ".join(line.split()).lower() for line in row["text"])
        if result and signature == result[-1]["_signature"]:
            result[-1]["last_epoch"] = row["epoch"]
            result[-1]["captures"] += 1
        else:
            result.append({"first_epoch": row["epoch"], "last_epoch": row["epoch"],
                           "captures": 1, "text": row["text"], "_signature": signature})
    return [{key: value for key, value in row.items() if key != "_signature"} for row in result]


def message_candidates(screens: list[dict]) -> list[dict]:
    # These are literal OCR lines, not certified move events or complete turns.
    # Bag descriptions and move names may match; retain context via screen index.
    result = []
    previous = ()
    for index, screen in enumerate(screens):
        selected = tuple(text for text in screen["text"] if MESSAGE_PATTERN.search(text))
        if selected and selected != previous:
            result.append({"screen_index": index, "epoch": screen["first_epoch"], "lines": list(selected)})
        previous = selected
    return result


def report_text(report: dict) -> str:
    action = report["explicit_action"]
    lines = [f"Hypno public turn {report['turn']} — explicitly requested {action}",
             "Observed OCR only. No unseen outcome, completed-turn count, enemy choice, HP/stage or Safeguard inference.",
             f"Result: {report['result']}; final screen: {report.get('final_classification', 'not captured')}"]
    if report.get("error"):
        lines.append("Stopped for review: " + report["error"])
    lines.append("\nObserved message candidates (literal OCR; inspect context for menus/descriptions):")
    for group in report["message_candidates"]:
        lines.append(f"[{group['epoch']:.3f}; screen {group['screen_index']}] " + " | ".join(group["lines"]))
    lines.append("\nFresh final public screen:")
    lines.extend(str(row["text"]) for row in report.get("final_rows", []))
    lines.append("\nAll public OCR frames, adjacent duplicates collapsed:")
    for index, frame in enumerate(report["public_screens"]):
        lines.append(f"\nScreen {index} [{frame['first_epoch']:.3f}–{frame['last_epoch']:.3f}; {frame['captures']} capture(s)]")
        lines.extend(frame["text"])
    for issue in report["journal_issues"]:
        lines.append("Journal issue: " + issue)
    return "\n".join(lines) + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--turn", type=int, required=True, help="Explicit ledger number, positive and never overwritten")
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument("--item", help="Exact named Medicine-pocket item; target is Arcanine, X items use --active")
    action.add_argument("--move-slot", type=int, choices=range(4), help="Explicit currently reviewed move slot, 0..3")
    args = parser.parse_args(argv)
    if args.turn < 1 or (args.item is not None and not args.item.strip()):
        parser.error("A positive turn number and a nonempty explicit action are required")
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    json_path = OUTPUT_DIR / f"turn-{args.turn}.json"
    txt_path = OUTPUT_DIR / f"turn-{args.turn}.txt"
    # Reserve first: a typo/repeated invocation must never execute another turn.
    try:
        reservation = json_path.open("x")
    except FileExistsError:
        parser.error(f"Turn {args.turn} already has a report; use a new explicit number after review")
    if txt_path.exists():
        reservation.close()
        json_path.unlink()
        parser.error(f"Turn {args.turn} already has a text report")
    start = time.time()
    offset = SCREEN_JOURNAL.stat().st_size if SCREEN_JOURNAL.exists() else 0
    report = {"kind": "public_hypno_one_action", "turn": args.turn, "start_epoch": start,
              "explicit_action": {"item": args.item, "target": "Arcanine"} if args.item is not None else {"move_slot": args.move_slot},
              "result": "not_started", "helpers": [], "input_policy": "existing ordinary-input helpers only; no automatic action selection",
              "observation_policy": "public screenshots/OCR only; gaps and unseen outcomes remain unknown",
              "journal_binding": "appended byte offset plus capture timespan; run UI helpers sequentially because screens.jsonl has no caller ID"}
    try:
        from play import snap
        captured = time.time()
        rows = snap()
        report["initial_rows"] = rows
        report["initial_guard"] = command_guard(rows, captured_at=captured, now=time.time())
        print(f"Public guard passed: Arcanine/Hypno command; executing explicit turn {args.turn}.", flush=True)
        for cmd in [helper_argv(args), [sys.executable, str(ROOT / "scripts/battle_ready.py")]]:
            stage = {"argv": cmd, "start_epoch": time.time()}
            report["helpers"].append(stage)
            try:
                run = subprocess.run(cmd, capture_output=True, text=True, timeout=180, cwd=ROOT)
                stage.update(returncode=run.returncode, stdout=run.stdout, stderr=run.stderr, end_epoch=time.time())
            except subprocess.TimeoutExpired as exc:
                stage.update(returncode=None, stdout=str(exc.stdout or ""), stderr=str(exc.stderr or ""), end_epoch=time.time())
                raise RuntimeError("Existing input helper timed out; inspect the public screen before another action") from exc
            if run.returncode:
                raise RuntimeError(f"{pathlib.Path(cmd[1]).name} stopped with code {run.returncode}: {run.stderr.strip() or run.stdout[-500:].strip()}")
        report["result"] = "helpers_returned"
    except Exception as exc:
        report.update(result="stopped_for_review", error=f"{type(exc).__name__}: {exc}")
    finally:
        # Capture even a guard/helper failure without sending any further input.
        try:
            from play import snap
            captured = time.time()
            report["final_rows"] = snap()
            report["final_capture_epoch"] = captured
            report["final_classification"] = final_classification(report["final_rows"], captured_at=captured, now=time.time())
        except Exception as exc:
            report["final_capture_error"] = f"{type(exc).__name__}: {exc}"
        report["end_epoch"] = time.time()
        records, issues = read_generated_screens(SCREEN_JOURNAL, offset, start, report["end_epoch"])
        report["journal_issues"] = issues
        report["public_capture_count"] = len(records)
        report["public_screens"] = deduplicate_screens(records)
        report["message_candidates"] = message_candidates(report["public_screens"])
        reservation.write(json.dumps(report, indent=2, ensure_ascii=False) + "\n")
        reservation.close()
        with txt_path.open("x") as stream:
            stream.write(report_text(report))
    print(f"{report['result']}; final public screen: {report.get('final_classification', 'unavailable')}", flush=True)
    for group in report["message_candidates"]:
        print("PUBLIC OCR: " + " | ".join(group["lines"]), flush=True)
    print("FRESH FINAL SCREEN:\n" + "\n".join(row["text"] for row in report.get("final_rows", [])), flush=True)
    print(f"Observed ledger: {json_path}\nReadable ledger: {txt_path}", flush=True)
    return 0 if report["result"] == "helpers_returned" and report.get("final_classification") in {"fresh_arcanine_hypno_command", "visible_victory_message"} and "final_capture_error" not in report else 2


if __name__ == "__main__":
    raise SystemExit(main())
