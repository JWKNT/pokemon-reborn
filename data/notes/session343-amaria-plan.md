# Amaria207 attempt3 preparation

Session342 both attempts reset; both retained in Video27 through342. Session343 training ongoing.

Owned Mienshao is135, Reckless, no item, High Jump Kick/Wide Guard/Fake Out/Acrobatics. Buy Peridot522E10 five EV Tuners for40000; Defense2→Speed5 (installed STATSTRINGS confirms order) keeps HPbulk and raises Speed past Bulu334. Existing careful nature retained. Training funding through Jace gives1926+12XL per round, free full heal; Magearna carriesAmuletCoin. Stop at45000, shop EscapeRopes.

Proposed lead Volcanion/Mienshao. T1 FlamethrowerBulu+FakeOutBulu. T2 AcrobaticsBulu before its334Speed; Volcanion can Flamethrower same slot (redirectCel ifBuluKO) to ensure KO. Then prefer WideGuard+SteamEruption againstVolcarona; do not gamble Mienshao's survival on Volcarona usingQuiverDance. RepeatWideGuard allowed installedMove0AC has no consecutive failure check. Watch GigaDrain/BugBuzz and Celesteela chip/seed: WG onlyblocks spread, notsingle-target. KeepZapdos healthy forKyogre.

AfterVolcarona: ProtectVolcanion+Mienshao→Meowstic blocks expectedPalkiaThunder withoutassumingAI; then MeowLightScreen whileVolcanion→Magearna. MistyTerrain nextturn+MageXSpDef, thenCM/heal aspublicHPrequires. Safeguard ifneeded, consider TrickRoom before attacks so Magearna acts beforePalkia/Kyogre. Do not stall at maxboosts. In Misty, DazzlingGleam1.5 and MagearnaFairySpDef1.5; SoulHeart ALSO addsSpDef on eachfaint. MistycanreplaceWaterSurface. Mistyduration5 or8withAmplifieldRock. ConsiderAmplifieldRockonMeowinsteadLightClay; planned terrain mattersmorethan3extrascreenturns. Terrain ending mustbe tracked.

Misty also strengthens enemySteamEruption1.5; removesWaterSurfacegroundimmunity, soenemyVolcanionEarthPower threatensourVolcanion. PrimordialSea still blocksFire. Misty removesWaterSurfaceOriginPulse/Electricboost; FairySpDefbonus specificallyprotectsMagearna. CelesteelaLeechSeed persists afterCelKO; account60HP perturn plusheals enemyoccupant. Never Surf intoenemyVolcanionWaterAbsorb. PreserveWideGuard forOriginPulse andFly/DischargeZapdos forKyogre.

Q owned inspection ONLY atfreshturn before anyqueuedaction: Qrestarts commandselection andrefunds earlieritem. own_field_inspect now requires--fresh-turn.

Static source: Battle_MoveEffects8387 Misty; Battler1141SoulHeart; Battle_Move386FairySpDef; FielddataMISTY. No battle internals read. Actualfight strategy mustrespond topublicresults.

Entry field confirmation:850E125 explicitly forcesWATERSURFACE, so alternate approachtile cannotavoidit. Titania850E124 doesNOTforcefield; map850defaultCave. Amaria entry54,51island, notsurf. Static event dumps work/343-amaria-battle-event.json and343-titania-battle-event.json.

Misty preventsstatuson grounded allies (Battle_Effects15), soSafeguardisredundantduringMisty. CannotrefreshMistywhilealreadyactive; castnextturnafterexpiry. Amplifield8turns, LightScreenwithoutLightClay5turns.
