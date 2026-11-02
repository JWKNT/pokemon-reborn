"""Read-only Glass upper-puzzle planning from an explicitly supplied snapshot.

No input, quicksave, native-state extraction, or shared navigation writes occur.
Stage presets are hypotheses, not evidence that a move succeeded in the game.
Temporary planner JSON isolates nav.route's legacy implicit state-file lookup.

Example:
  python3 scripts/glass_upper_route_plan.py \
    --state notes/Glass-10AM-paused-navigation.json --stage scanner-return \
    --from 40 9 true --following espeon --glaceon 43 16 \
    --query GB13Right
"""
import argparse
import copy
import heapq
import json
import pathlib
import subprocess
import tempfile
from contextlib import contextmanager

import nav
from layer_route import effect
from glass_positions import refresh

ROOT = pathlib.Path(__file__).resolve().parents[1]
# The legacy route_map.rb merges shared navigation even with explicit overrides.
# This static reader deliberately omits that merge. Unspecified progress falls
# back to the native saved file; the caller's explicit snapshot wins every key.
READ_MAP_RUBY = r'''
def iv(o,k);o.instance_variable_get('@'+k.to_s);end
def table(o)
 b=iv(o,:raw).pack('C*');h=b[0,20].unpack('l<*')
 {dims:h[1,3],data:b[20..].unpack('S<*')}
end
id=ARGV[0].to_i
root='/Applications/Reborn.app/Contents/Game/Data/'
v=load_rgss('/Users/jw/Library/Application Support/Pokemon Reborn/Game_3.rxdata')
m=load_rgss(root+'Map%03d.rxdata'%id)
ts=load_rgss(root+'Tilesets.rxdata')[iv(m,:tileset_id)]
sw=iv(v[:switches],:data);va=iv(v[:variable],:data);ss=iv(v[:self_switches],:data)
state=JSON.parse(ARGV[3])
(state['variables']||{}).each{|k,value|va[k.to_i]=value}
(state['switches']||{}).each{|k,value|sw[k.to_i]=value}
(state['self_switches']||{}).each{|k,value|map,event,ch=k.split(',');ss[[map.to_i,event.to_i,ch]]=value}
events=iv(m,:events).filter_map do |k,e|
 p=iv(e,:pages).reverse.find do |pg|
  c=iv(pg,:condition)
  (!iv(c,:switch1_valid)||sw[iv(c,:switch1_id)]) &&
  (!iv(c,:switch2_valid)||sw[iv(c,:switch2_id)]) &&
  (!iv(c,:variable_valid)||(va[iv(c,:variable_id)]||0)>=iv(c,:variable_value)) &&
  (!iv(c,:self_switch_valid)||ss[[id,k,iv(c,:self_switch_ch)]])
 end
 next unless p
 g=iv(p,:graphic)
 [k,{x:iv(e,:x),y:iv(e,:y),name:iv(e,:name),through:iv(p,:through),
 character:iv(g,:character_name),tile_id:iv(g,:tile_id),trigger:iv(p,:trigger),
 move_type:iv(p,:move_type),direction:iv(g,:direction),list:plain(iv(p,:list))}]
end.to_h
puts JSON.generate({map:id,position:ARGV[1,2].map(&:to_i),width:iv(m,:width),
height:iv(m,:height),data:table(iv(m,:data)),passages:table(iv(ts,:passages)),
priorities:table(iv(ts,:priorities)),terrain:table(iv(ts,:terrain_tags)),events:events})
'''
DIR = {"up": (0, -1, 8), "down": (0, 1, 2),
       "left": (-1, 0, 4), "right": (1, 0, 6)}
FACE = {2: "down", 4: "left", 6: "right", 8: "up"}
BASE = {408: 1, 416: 1, 417: 2, 418: 0, 419: 1, 420: 0, 421: 0}
STAGES = {
    "current": {},
    "upper-open": BASE,
    "left-frozen": {**BASE, 402: 60},
    "right-approach": {**BASE, 402: 60, 418: 1, 419: 2},
    "right-frozen": {**BASE, 402: 60, 403: 60, 418: 1, 419: 2},
    "scanner-return": {**BASE, 402: 60, 403: 60, 418: 1, 419: 2,
                       420: 1, 421: 1},
    "door-ready": {**BASE, 402: 60, 403: 60, 418: 1, 419: 2,
                   420: 2, 421: 1},
}
# All pallet parts have the same native directional prompt as their core.
ACTIONS = {
    "GB10Right": (range(146, 153), "right"),
    "GB11Down": (range(153, 157), "down"),
    "GB11Up": (range(153, 157), "up"),
    "GB12Left": (range(157, 165), "left"),
    "GB12Right": (range(157, 165), "right"),
    "GB13Left": (range(165, 170), "left"),
    "GB13Right": (range(165, 170), "right"),
    "GB14Left": (range(170, 174), "left"),
    "GB14Right": (range(170, 174), "right"),
    "freeze-left": ([83, 84], None),
    "freeze-right": ([85, 86], None),
    "scanner": ([174], None),
    "Glaceon": ([63], None),
    "Espeon": ([65], None),
}


def boolean(value):
    if str(value).lower() in ("true", "1", "yes"): return True
    if str(value).lower() in ("false", "0", "no"): return False
    raise argparse.ArgumentTypeError("layer/switch must be true or false")


@contextmanager
def isolated_navigation(state):
    """Redirect only this process's nav lookup; never touch shared notes."""
    with tempfile.TemporaryDirectory(prefix="glass-readonly-plan-") as folder:
        root = pathlib.Path(folder)
        (root / "notes").mkdir()
        (root / "notes/navigation-state.json").write_text(json.dumps(state))
        original = nav.ROOT
        nav.ROOT = root
        try:
            yield
        finally:
            nav.ROOT = original


class Planner:
    def __init__(self, state, start):
        self.state = copy.deepcopy(state)
        self.start = tuple(start)
        if self.start[:2] in ((38, 8), (39, 8)):
            raise ValueError("Starting on a gauntlet transfer tile is unsafe")
        self.maps, self.graphs = {}, {}
        self.forbidden = {}
        for layer in (False, True):
            argument = json.dumps({
                "switches": {**self.state.get("switches", {}), "410": layer},
                "variables": self.state.get("variables", {}),
                "self_switches": self.state.get("self_switches", {}),
            })
            model = json.loads(subprocess.check_output([
                "ruby", "-r", str(ROOT / "scripts/read_rgss.rb"), "-e", READ_MAP_RUBY, "732",
                str(start[0]), str(start[1]), argument], stderr=subprocess.DEVNULL))
            for eid, xy in self.state.get("positions", {}).get("732", {}).items():
                if eid in model["events"]:
                    model["events"][eid]["x"], model["events"][eid]["y"] = xy
            forbidden = {(38, 8), (39, 8)}
            following = [name for name, sw in (("Glaceon", "946"), ("Espeon", "947"))
                         if self.state.get("switches", {}).get(sw)]
            for event in model["events"].values():
                commands = event.get("list") or []
                if any(c["code"] == 201 for c in commands):
                    forbidden.add((event["x"], event["y"]))
                if event["trigger"] == 1 and any(
                        'pbRemoveDependency2("' + name + '")' in str(commands)
                        for name in following):
                    forbidden.add((event["x"], event["y"]))
            graph_state = copy.deepcopy(self.state)
            avoid = graph_state.setdefault("avoid", {}).setdefault("732", [])
            avoid.extend([list(p) for p in sorted(forbidden)])
            with isolated_navigation(graph_state):
                graph = nav.route(model, None, True)
            self.maps[layer], self.graphs[layer] = model, graph
            self.forbidden[layer] = forbidden
        self.dist, self.prev = {self.start: 0}, {self.start: None}
        todo = [(0, self.start)]
        while todo:
            cost, point = heapq.heappop(todo)
            if cost != self.dist[point]: continue
            x, y, layer = point
            for key, (nx, ny) in self.graphs[layer].get((x, y), []):
                dx, dy, direction = DIR[key.removeprefix("jump:")]
                touches = [(x + dx, y + dy), (nx, ny)] if key.startswith("jump:") else [(nx, ny)]
                if any(p in self.forbidden[layer] for p in touches): continue
                next_layer = layer
                for tile in dict.fromkeys(touches):
                    for event in self.maps[layer]["events"].values():
                        if event["trigger"] == 1 and (event["x"], event["y"]) == tile:
                            next_layer = effect(event, direction, next_layer)
                destination = (nx, ny, next_layer)
                next_cost = cost + (2 if key.startswith("jump:") else 1)
                if next_cost < self.dist.get(destination, float("inf")):
                    self.dist[destination] = next_cost
                    self.prev[destination] = (point, key,
                        nav.action_jump(self.maps[layer], point[:2], key))
                    heapq.heappush(todo, (next_cost, destination))

    def path(self, target):
        target = tuple(target)
        if target not in self.prev: return None
        steps, cursor = [], target
        while self.prev[cursor]:
            previous, key, action_jump = self.prev[cursor]
            steps.append({"from": previous, "key": key, "to": cursor,
                          "action_jump": action_jump})
            cursor = previous
        return list(reversed(steps))

    def interaction(self, query):
        ids, push = ACTIONS[query]
        candidates = []
        for layer, model in self.maps.items():
            if query in ("Glaceon", "Espeon"):
                follow, flag = ("946", "964") if query == "Glaceon" else ("947", "965")
                # Installed event: flagTrue requires410False; flagFalse410True.
                if self.state.get("switches", {}).get(follow): continue
                if layer == bool(self.state.get("switches", {}).get(flag)): continue
            for eid in ids:
                event = model["events"].get(str(eid))
                if not event or event["trigger"] != 0: continue
                for facing, (dx, dy, _) in ((d, DIR[name]) for d, name in FACE.items()):
                    if push and facing == 10 - DIR[push][2]: continue
                    target = (event["x"] - dx, event["y"] - dy, layer)
                    path = self.path(target)
                    if path is not None:
                        candidates.append({"event": eid, "event_position": [event["x"], event["y"]],
                            "position": target, "face": FACE[facing], "cost": self.dist[target],
                            "path": path})
        candidates.sort(key=lambda c: (c["cost"], c["event"], c["position"]))
        return {"query": query, "push": push, "reachable": bool(candidates),
                "candidates": candidates}


def prepare(args):
    state = json.loads(pathlib.Path(args.state).read_text())
    state.setdefault("variables", {}).update({str(k): v for k, v in STAGES[args.stage].items()})
    state.setdefault("switches", {})["410"] = args.start[2]
    if args.stage in ("scanner-return", "door-ready"):
        state["switches"]["958"] = True
    for item in args.var:
        key, value = item.split("=", 1)
        state["variables"][str(int(key))] = int(value)
    for item in args.switch:
        key, value = item.split("=", 1)
        state["switches"][str(int(key))] = boolean(value)
    for name, eid, var, flag, following in (
            ("glaceon", 63, 404, "964", "946"),
            ("espeon", 65, 406, "965", "947")):
        xy = getattr(args, name)
        if xy is not None:
            state["variables"][str(var)], state["variables"][str(var + 1)] = xy
            state.setdefault("positions", {}).setdefault("732", {})[str(eid)] = xy
            state["switches"][flag] = getattr(args, name + "_layer")
            state["switches"][following] = False
    if args.following != "state":
        state["switches"].update({"946": args.following == "glaceon", "947": args.following == "espeon"})
        if args.following != "none":
            variable = 404 if args.following == "glaceon" else 406
            state["variables"].update({str(variable): 0, str(variable + 1): 0})
    if not args.no_refresh:
        refresh(state, json.loads((ROOT / "work/story-map-732-events.json").read_text()))
    return state


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--state", required=True, help="explicit navigation snapshot; never modified")
    parser.add_argument("--stage", choices=STAGES, default="current")
    parser.add_argument("--from", dest="start", nargs=3, required=True, metavar=("X", "Y", "LAYER"))
    parser.add_argument("--following", choices=("state", "none", "espeon", "glaceon"), default="state")
    for name in ("glaceon", "espeon"):
        parser.add_argument("--" + name, nargs=2, type=int, help="waiting companion X Y")
        parser.add_argument("--" + name + "-layer", type=boolean, default=False, help="964/965 flag, defaultFalse=B2F")
    parser.add_argument("--var", action="append", default=[], help="hypothetical N=INTEGER override")
    parser.add_argument("--switch", action="append", default=[], help="hypothetical N=true/false override")
    parser.add_argument("--query", choices=[*ACTIONS, "all", "door-standby"], default="all")
    parser.add_argument("--goal", nargs=3, metavar=("X", "Y", "LAYER"))
    parser.add_argument("--limit", type=int, default=3, help="maximum faces per query")
    parser.add_argument("--no-refresh", action="store_true", help="trust supplied observed pallet positions")
    args = parser.parse_args()
    args.start = [int(args.start[0]), int(args.start[1]), boolean(args.start[2])]
    state = prepare(args)
    planner = Planner(state, args.start)
    output = {"read_only": True, "hypothetical_stage": args.stage, "start": args.start,
              "variables": {k: state["variables"].get(k, 0) for k in map(str, (402, 403, 408, 417, 418, 419, 420, 421))},
              "following": {name: bool(state["switches"].get(sw)) for name, sw in (("Glaceon", "946"), ("Espeon", "947"))},
              "door_warning": "38/39,8 transfer to immediate gauntlet autorun; both are always forbidden."}
    if args.goal:
        goal = [int(args.goal[0]), int(args.goal[1]), boolean(args.goal[2])]
        output["goal"] = goal
        output["path"] = planner.path(goal)
    else:
        queries = list(ACTIONS) if args.query == "all" else [args.query]
        output["results"] = []
        for query in queries:
            if query == "door-standby":
                # Outside the doorway, never a transfer destination itself.
                result = {"query": query, "goals": [
                    {"position": [x, 9, layer], "path": planner.path((x, 9, layer))}
                    for x in (38, 39) for layer in (False, True)]}
            else:
                result = planner.interaction(query)
                result["candidate_count"] = len(result["candidates"])
                result["candidates"] = result["candidates"][:max(args.limit, 0)]
                if query.startswith("GB"):
                    result["requires_actual_Espeon_following"] = True
                if query.startswith("freeze"):
                    result["requires_actual_Glaceon_following"] = True
            output["results"].append(result)
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
