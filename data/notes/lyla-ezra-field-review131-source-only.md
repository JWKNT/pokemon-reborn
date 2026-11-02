# Lyla/Ezra field and immediate damage review

Source-only review, 2026-10-03. No live battle, AI, RNG, native save, log, or video was consulted. Actual HP, observed Close Combat drop, and battle backdrop descriptions below came from the root player's messages.

Installed `Scripts/Reborn/metatext.rb` map763 specifies `BattleBack: FieldEve`. `PokeBattle_Field.initialize` in `Scripts/Battle_Field.rb` starts from that graphic, with possible explicit forced-field variables, terrain/Surf, and password overrides. Static E45/E46 source contains no field-setting command; `pbTrainerIntro` in `Field.rb:2951` locks movement and plays the trainer intro only. Therefore the street map does **not** source-prove Mountain or Snowy Mountain. Hail itself does not establish Snowy Mountain. Root reported an orange/brown backdrop, so Snowy multipliers must not be assumed from weather alone.

The installed Snowy Mountain definition (`Scripts/Reborn/fieldtext.rb:1609`) boosts Ice1.5, IcyWind2.0 separately, HyperVoice1.5, and halves Fire. FlameBurst changes it to Mountain after that hit. ClangingScales and DazzlingGleam have no Snowy-specific boost listed. The root-observed CF147 HP loss remains authoritative; the earlier no-field calculations were conditional estimates, not a reconstruction of that damage.

From frozen Cryogonal90 SpA205 and installed ordinary trainer defaults (IV10/EV85, neutral nature):

| Target | HP / SpDef | Unboosted Ice Beam on no-field or Mountain | On Snowy Mountain |
|---|---:|---:|---:|
| Haxorus87, full HP |256 /153|237–279|354–417|
| Kommo-o87, no drop |254 /214|171–201|255–300|
| Kommo-o87, one observed Close Combat SpDef−1 |254 /142|255–300|383–450|

Thus unboosted Ice Beam cannot promise a full-HP Haxorus KO on the normal map field. Kommo-o after the actual single Close Combat drop is a guaranteed KO even without a field boost. These figures assume no Light Screen, further defensive boost, SpA loss, or other modifier; use actual public conditions.

Installed `PBStuff.rb:116` Bulletproof move list does not contain Hex. At CF90 baseSpA210, +4SpA Hex into Kommo-o's observed SpDef142 is282–332 on no-field, whereas DarkPulse is115–136 because Fighting resists Dark. Wigglytuff's Normal typing makes Hex ineffective.
