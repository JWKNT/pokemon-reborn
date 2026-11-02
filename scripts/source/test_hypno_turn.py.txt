"""Pure/synthetic public-guard tests. No screenshots, input, or native state."""
import argparse
import json
import pathlib
import tempfile
import unittest

from hypno_turn import (command_guard, deduplicate_screens, final_classification,
                        helper_argv, message_candidates, name_matches, read_generated_screens)


def command(actor="Arcanine", foe="Hypno"):
    return [
        {"text": foe, "x": .12, "y": .13},
        {"text": "Lv100", "x": .30, "y": .13},
        {"text": actor, "x": .66, "y": .53},
        {"text": "HP 294/294", "x": .71, "y": .64},
        {"text": f"What will {actor} do?", "x": .08, "y": .77},
        {"text": "FIGHT", "x": .63, "y": .77},
        {"text": "BAG", "x": .82, "y": .77},
        {"text": "RUN", "x": .83, "y": .86},
    ]


class PublicHypnoTurnTests(unittest.TestCase):
    def test_complete_hyphenated_species_token(self):
        for text in ['Kommo-o','Kommo-o Lv87','Kommo o','Kommo\u2011o']:
            self.assertTrue(name_matches(text,'Kommo-o'))
        for text in ['Kommo','Jangmo-o','Hakamo-o','NotKommo-o','Kommo-oid','Kommo x']:
            self.assertFalse(name_matches(text,'Kommo-o'))
        self.assertTrue(name_matches('Porygon-Z Lv89','Porygon-Z'))
    def test_observed_cyrillic_hypno_glyphs_keep_exact_hud_guard(self):
        for text in ["Hypnо", "Нурnо", "Нурnо ♀ Lv100"]:
            self.assertTrue(name_matches(text, "Hypno"))
            proof = command_guard(command(foe=text), captured_at=100, now=101)
            self.assertEqual(proof["foe"], "Hypno")
        # Initial turn1's public capture split its command prompt into two rows.
        rows = command(foe="Hypnо")
        rows[2]["text"] = "Arcanine F"
        rows[4]["text"] = "What will"
        rows.insert(5, {"text": "Arcanine do", "x": .10, "y": .831})
        self.assertEqual(command_guard(rows, captured_at=100, now=101)["actor"], "Arcanine")
        for text in ["Hypnoid", "Drowzee", "НурnоК", "NotHypno", "Гурnо"]:
            self.assertFalse(name_matches(text, "Hypno"))

    def test_cyrillic_actor_aliases_do_not_hide_a_contradictory_prompt(self):
        proof = command_guard(command(actor="Аrсаnіnе", foe="Нурnо"), captured_at=100, now=101)
        self.assertEqual(proof["actor"], "Arcanine")
        for name in ["Cofagrigus", "Сofagrigus", "Swampert", "Klinklang", "ArcanineК"]:
            rows = command(foe="Нурnо")
            rows[4]["text"] = f"What will {name} do?"
            with self.assertRaisesRegex(ValueError, "different acting"):
                command_guard(rows, captured_at=100, now=101)
        for actor in ["Сofagrigus", "Swampert", "Klinklang", "ArcanineК"]:
            with self.assertRaisesRegex(ValueError, "Expected visible"):
                command_guard(command(actor=actor, foe="Нурnо"), captured_at=100, now=101)

    def test_observed_turn4_riun_is_only_a_proper_run_command_alias(self):
        # Turn4's failed public capture: Cyrillic Hypno, split prompt, RIUN in
        # the observed lower-right cell. The old report sent zero helpers.
        rows = command(foe="Нурnо")
        rows[2].update(text="Arcanine", x=.5928264, y=.5189115)
        rows[3].update(text="210/ 294", x=.7732558, y=.6035242)
        rows[4].update(text="What will", x=.1017442, y=.7615639)
        rows.insert(5, {"text": "Arcanine do", "x": .1031977, "y": .8309091})
        rows[-1].update(text="RIUN", x=.7892442, y=.8418182)
        for label in ["RIUN", "RΙUN", "RІUN", "RUN"]:
            rows[-1]["text"] = label
            self.assertEqual(command_guard(rows, captured_at=100, now=101)["foe"], "Hypno")
        for label in ["REUN", "RIN", "RUM", "RIUN to escape", "NOTRIUN"]:
            rows[-1]["text"] = label
            with self.assertRaisesRegex(ValueError, "command labels"):
                command_guard(rows, captured_at=100, now=101)
        rows[-1]["text"] = "RIUN"
        for x, y in [(.2, .84), (.79, .3), (.79, .97)]:
            rows[-1].update(x=x, y=y)
            with self.assertRaisesRegex(ValueError, "command labels"):
                command_guard(rows, captured_at=100, now=101)
        rows[-1].update(x=.7892442, y=.8418182)
        rows[0]["text"] = "Drowzee"
        with self.assertRaisesRegex(ValueError, "Expected visible"):
            command_guard(rows, captured_at=100, now=101)
        rows[0]["text"] = "Нурnо"
        rows[6]["text"] = "Flamethrower"
        with self.assertRaisesRegex(ValueError, "command labels"):
            command_guard(rows, captured_at=100, now=101)

    def test_fresh_visible_actor_and_foe_required(self):
        proof = command_guard(command(), captured_at=100, now=101)
        self.assertEqual((proof["actor"], proof["foe"]), ("Arcanine", "Hypno"))
        for rows in [command("Klinklang"), command(foe="Gardevoir"),
                     [{**row, "y": .8} if row["text"] == "Hypno" else row for row in command()],
                     command() + [{"text": "PP: 10/10", "y": .84}],
                     command() + [{"text": "Choose a Pokemon", "y": .76}]]:
            with self.assertRaises(ValueError):
                command_guard(rows, captured_at=100, now=101)
        with self.assertRaises(ValueError):
            command_guard(command(), captured_at=100, now=116)
        rows = command()
        rows[4]["text"] = "What will Cofagrigus do?"
        with self.assertRaises(ValueError):
            command_guard(rows, captured_at=100, now=101)

    def test_exact_explicit_action_only(self):
        base = pathlib.Path("/synthetic")
        item = helper_argv(argparse.Namespace(item="X Sp. Def", move_slot=None), base)
        self.assertEqual(item[1:], ["/synthetic/scripts/battle_item.py", "X Sp. Def", "Arcanine", "--active"])
        potion = helper_argv(argparse.Namespace(item="Ultra Potion", move_slot=None), base)
        self.assertEqual(potion[1:], ["/synthetic/scripts/battle_item.py", "Ultra Potion", "Arcanine"])
        move = helper_argv(argparse.Namespace(item=None, move_slot=2), base)
        self.assertEqual(move[1:], ["/synthetic/scripts/battle_move.py", "2", "--watch"])

    def test_adjacent_dedup_does_not_erase_a_later_repeat(self):
        records = [{"epoch": i, "text": text} for i, text in enumerate([
            ["Hypno used Calm Mind!"], ["Hypno used Calm Mind!"],
            ["FIGHT", "BAG", "RUN"], ["Hypno used Calm Mind!"]])]
        result = deduplicate_screens(records)
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0]["captures"], 2)
        messages = message_candidates(result)
        self.assertEqual([row["screen_index"] for row in messages], [0, 2])
        self.assertEqual(messages[0]["lines"], ["Hypno used Calm Mind!"])

    def test_bounded_append_read_and_final_public_state(self):
        with tempfile.TemporaryDirectory(prefix="hypno-public-test-") as directory:
            journal = pathlib.Path(directory) / "screens.jsonl"
            journal.write_text(json.dumps({"epoch": 1, "text": ["old screen"]}) + "\n")
            offset = journal.stat().st_size
            with journal.open("a") as stream:
                for value in [
                    {"epoch": 5, "text": ["too early"]},
                    {"epoch": 11, "text": ["Hypno used Dark Pulse!"]},
                    {"epoch": 15, "text": ["too late"]}]:
                    stream.write(json.dumps(value) + "\n")
            rows, issues = read_generated_screens(journal, offset, 10, 12)
            self.assertEqual([row["text"] for row in rows], [["Hypno used Dark Pulse!"]])
            self.assertFalse(issues)
        self.assertEqual(final_classification(command(), captured_at=100, now=101), "fresh_arcanine_hypno_command")
        self.assertEqual(final_classification(command("Cofagrigus"), captured_at=100, now=101), "review_required")
        self.assertEqual(final_classification([{"text": "You defeated Hypno!", "y": .8}], captured_at=100, now=101), "visible_victory_message")


if __name__ == "__main__":
    unittest.main()
