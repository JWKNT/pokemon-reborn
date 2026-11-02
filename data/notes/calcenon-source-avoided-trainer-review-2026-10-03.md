# Calcenon → Route 4 stationary trainer exclusion review

Source-only independent review of `calcenon_agate_queue.py`'s
`--allow-source-avoided-trainers`, 2026-10-03. No game input, fresh capture,
active native/save, or recording access was used. The running queue was not
modified.

The exception is suitable for the installed climb prefix 412 → 710 → 711 →
713 → 714 → 715. It is restricted to the five climb maps and accepts only
stationary player-touch events with an exact `Trainer(n)` name and a valid
source facing. Moving, autorun, unnamed, and other automatic battles in the
scanned trigger set still stop the queue. It inserts the NPC tile and all `n`
source sightline tiles into the planner's hard `avoid` set before `eventq`
plans any walking.

`nav.route` merges these tiles into `blocked`. Ordinary movement rejects
them; native ledges reject both their intermediate tile and their landing;
scripted/forced jumps reject their landing. `layer_route.plan` uses the same
route graphs for both layer states, and its cache key includes the planner
state, including the exclusions. `layer_walk` therefore retains the hard
exclusions.

Installed stationary trainers on the remainder of this prefix:

| Map | Event / position | Facing / reach |
| --- | --- | --- |
| 710 | 57 / (37,39) | Left / 5 |
| 711 | 82 / (21,30) | Down / 4 |
| 711 | 93 / (23,23) | Right / 2 |
| 713 | 86 / (54,30) | Down / 3 |
| 714 | 46 / (33,15) | Down / 4 |
| 714 | 54 / (20,22) | Down / 2 |

Installed source arrivals and climb staging positions are outside these
sightlines. Map 713's forced jumps occupy x24–43, away from its trainer at
x54. A static scan of the prefix's event pages found no controller moving or
turning these trainers and no parallel-process battle. Map 412's conditional
unnamed wild encounter remains rejected by this exception when its page is
active.

Two generic boundaries should remain explicit: the guard scans trigger
1/2/3, not parallel trigger 4, and a scripted jump's intermediate transit
tiles are not checked individually. Neither creates a concrete overlap in
the installed prefix reviewed here. Reusing this exception for different
maps or changed event pages needs a new source review. No helper fix was
needed for the current route.
