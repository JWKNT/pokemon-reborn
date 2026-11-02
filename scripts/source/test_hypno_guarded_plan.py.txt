"""Bounded semantic fixtures; no game inputs or native files."""
import copy
import unittest

from hypno_guarded_plan import BUILD, MOVES, propose, pulse_ranges


def state(rows=(), *, hp=294, status=None, accept=False):
    return dict(build=dict(BUILD, moves=sorted(MOVES)), ledger_complete=True,
                stock=dict(XSPEED=5, XATTACK=4, XSPDEF=12, FULLHEAL=17,
                           ULTRAPOTION=31, FULLRESTORE=0),
                observation=dict(confirmed=True, command_menu=True, turn=len(rows)+1,
                                 actor="Arcanine", foe="Hypno", field="STARLIGHT",
                                 weather="NONE", hp=hp, status=status,
                                 pp={m: 8 for m in MOVES}),
                turns=list(rows), accept_critical_risk=accept)


def row(n, action, enemy="HYPNOSIS", *, result="success", enemy_result="failed",
        expired=False, damage=None):
    p = dict(action=action, result=result)
    if action.startswith("X") or action in {"FULLHEAL", "ULTRAPOTION", "FULLRESTORE"}:
        p["consumed"] = result == "success"
    return dict(turn=n, completed=True, confirmed=True, player=p,
                enemy=dict(move=enemy, result=enemy_result),
                safeguard_expired=expired, observed_hp_damage=damage)


class HypnoPlanTest(unittest.TestCase):
    def test_initial_speed_is_one_priority_item(self):
        value = propose(state())
        self.assertEqual(value["action"], "XSPEED")
        self.assertEqual(value["ordinary_helper_argv"][-1], "--active")

    def test_sleep_cure_before_any_setup(self):
        first = row(1, "XSPEED", enemy_result="success")
        self.assertEqual(propose(state([first], status="SLEEP"))["action"], "FULLHEAL")

    def test_cure_then_awake_fast_safeguard(self):
        rows = [row(1, "XSPEED", enemy_result="success"),
                row(2, "FULLHEAL", "DREAMEATER")]
        self.assertEqual(propose(state(rows))["action"], "SAFEGUARD")

    def test_hp_critical_margin_healing_precedes_setup(self):
        rows = [row(1, "XSPEED", "DARKPULSE", enemy_result="success", damage=119)]
        self.assertEqual(propose(state(rows, hp=175))["action"], "ULTRAPOTION")

    def test_safeguard_cast_end_is_four_not_five(self):
        rows = [row(1, "XSPEED"), row(2, "SAFEGUARD")]
        value = propose(state(rows))
        self.assertEqual(value["derived"]["safeguard"], 4)
        self.assertEqual(value["action"], "XATTACK")

    def test_expiry_next_command_recast_before_hypnosis(self):
        rows = [row(1, "XSPEED"), row(2, "SAFEGUARD"), row(3, "XATTACK"),
                row(4, "XATTACK"), row(5, "MORNINGSUN"),
                row(6, "MORNINGSUN", expired=True)]
        value = propose(state(rows))
        self.assertEqual(value["derived"]["safeguard"], 0)
        self.assertEqual(value["action"], "SAFEGUARD")

    def test_finishing_crunch_beats_unneeded_recast_after_expiry(self):
        rows = [row(1, "XSPEED"), row(2, "SAFEGUARD"), row(3, "XATTACK"),
                row(4, "XATTACK"), row(5, "MORNINGSUN"),
                row(6, "CRUNCH", expired=True)]
        value = propose(state(rows, hp=30))
        self.assertEqual(value["derived"]["foe_hp_bound"], 157)
        self.assertEqual(value["action"], "CRUNCH")

    def test_false_early_refresh_is_rejected(self):
        rows = [row(1, "XSPEED"), row(2, "SAFEGUARD"), row(3, "SAFEGUARD")]
        self.assertEqual(propose(state(rows))["status"], "review")

    def test_failed_refresh_still_ticks_a_turn(self):
        rows = [row(1, "XSPEED"), row(2, "SAFEGUARD"),
                row(3, "SAFEGUARD", result="failed")]
        self.assertEqual(propose(state(rows))["derived"]["safeguard"], 3)

    def test_missing_expiry_line_fails_closed(self):
        rows = [row(1, "XSPEED"), row(2, "SAFEGUARD"), row(3, "XATTACK"),
                row(4, "XATTACK"), row(5, "MORNINGSUN"), row(6, "MORNINGSUN")]
        self.assertEqual(propose(state(rows))["status"], "review")

    def test_critical_ignores_all_defensive_boosts(self):
        self.assertEqual(pulse_ranges(2, 0)[1], [326, 383])
        self.assertEqual(pulse_ranges(2, 6)[1], [326, 383])
        rows = [row(1, "XSPEED", "CALMMIND", enemy_result="success"),
                row(2, "SAFEGUARD", "CALMMIND", enemy_result="success")]
        self.assertEqual(propose(state(rows))["status"], "review")
        value = propose(state(rows, accept=True))
        self.assertTrue(value["critical_can_ohko_full_hp"])
        self.assertEqual(value["action"], "XSPDEF")

    def test_stock_refund_and_turn_omission_are_not_assumed(self):
        bad = state([row(1, "XSPEED")])
        bad["turns"][0]["player"]["consumed"] = False
        self.assertEqual(propose(bad)["status"], "review")
        missing = state([row(2, "XSPEED")])
        self.assertEqual(propose(missing)["status"], "review")
        changed = copy.deepcopy(state())
        changed["build"]["speed"] = 177
        self.assertEqual(propose(changed)["status"], "review")


if __name__ == "__main__":
    unittest.main()
