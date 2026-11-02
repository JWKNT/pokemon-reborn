# Necrozma preparation, session362

All six trained145. Current party Arcanine/Mawile/Latias/Darkrai/Zapdos/Meowstic. Native frozen owned stats Necrozma362-All145. Jace v4 defeated1 round, 1926 payout and12XL, healed. 13XL spent Arcanine, 2XL remain; money2199.

Rainbow halves Dark Pulse and boosts Prism Armor defense1.33. Initial Darkrai sweep idea superseded pending full calculation. Mega Latias with Calm Mind/Recover/Surf is promising because lead Necrozma's Psychic and Fire attacks are resisted, Light Screen expires during setup, and Mega Latias has physical bulk for Dusk Mane/Solgaleo. Ultra Dragon Pulse receives Rainbow1.5 and Neuroforce and must be explicitly budgeted; do not blindly batch. Magical Seed grants +1SpA and75% Wish. Meowstic Misty Terrain is NOT a solution: it still halves Dark Pulse and boosts Moongeist.

Prisma route: GrandHall38E6 -> Fly525 -> connected551 -> connected552 via grass border with near20,8 -> RockSmash552E29/E30 -> connected551 near5,7 -> smash551E16 ->551E15->184E2->185E12->896.
Map896 bridges23/24 scripted3-forward underpasses now modeled nav.py. First successful path23,70->El27,43 publicly proved32,63 arrival. Serra intro triggered23,74; normal save Prisma362-SerraIntro has position23,70 andvar7253. El intro completed checkpointPrisma362-EliasIntro. Luna intro ongoing.

Mega Latias stats508/297/489/455/455/404. At+6 Surf estimates: lead409–481/572HP, Dawn302–355/572, Dusk343–404/572, Lunala233–274withShadowShieldthen466–548/597, Solgaleo603–709/597, Ultra198–234/572. Ultra Dragon Pulse into+6Latias177–208; UltraSpeed~596>404. One normal XSpeed early raises808 and permits timelyRecover. Need12Surf hits of15PP; riskscrit ignoresCM, particularly Dawn Moongeist andUltraDragon. Use fullHPentereachriskyfoe, retainMawileprioritybackup. Not guaranteedwin; no battleattemptyet.


## Prisma363 continuation
First blue orb completed in362. Mirror74 moved to17,64; mirror75 moved to18,64 through normal inputs with public-pixel verification (`work/prisma-public-pushes.jsonl`). Light/dark storage cycle underway. Session362 final review/publish complete: video29 prefix9397frames,313.254333s,SHA3a8d0dd778e45e090bb68ab0c4df5de5b0018fae24a84b810f8cb63ad779afdb. Consumed362sources removed after both QA and publication;363capture prefix reconciled.

Green timed pulse succeeded first attempt: `prisma_green_pulse.py`, native Prisma363-GreenPulse verifies1888true, purple reset2180true,75[18,64]/74[17,64]. Public-frame serieswork/prisma-green-public-1791945570. Starts22,63 facingdown, C,wait.25,right4/down4/right1 with.12press/.1wait,down,C. Purple activates around2.7s while Ubeam is left of initial75. Overworld turbo remainsOFF. Same timing should work dual/triple: other beams pass x18/y64 orx27/y64 at~2.35s and reachcrystals~3.95s. Verify actual result rather than assume.

Green activated and four rocks108,80,109,107 smashed normally, checkpointPrisma363-GreenRocks. Dual shadowsstored75[18,63],74[17,63] atPrisma363-DualShadows; script33162 preparing75[27,64],74[18,64],chargePurple,75[22,61],timeddual. Guide6 verified triple shadow73[26,62], current73[27,64]; move74oneDOWNbeforeRedactivation toavoidrock17,63.
Final-stage approach: afterthirdorbbroken95[19,63]andSerra72[19,64]; talkSerra(to7256),launchLbeamthrough19,64,advancepage1autorun(to7258). MoveSerraawaybeforebroken95up3; aimSerra21,62thenpushright1to22,62facingright. Finalshadowtargets95[19,60],73[27,62],75[26,64],74[26,68]. Helperprisma_serra_push.py usesrecordedpixelproof, notyetcalibratedinlivegame; stopifscorefails. Thenlight/dark,chargePurple,74[18,64],73[23,68], launchall4. TimedactivationafterL/Dpassmirrors; finalpulse needsnewroute/calibration.

Final timing route candidate: start22,63facingdownlaunchC,wait.25; right3/down3/right1/down2 (normal.12+.1taps) to26,68, facerightCactivatesPurpleat~2.7s. Avoids75at26,64andredrock27,67. Shadow74warpsonto26,68underplayerlegitimately; beamignoresplayerandreflectsrightintoPurpleafter~3.55s. Dpass73at23,68~2.35s, so sameactivationwindowshouldwork. Verifyexactrouteagainstnavandall4charge; finalSerraautorunpage4mustcompletebeforecheckpoint.

Dual pulse succeeded FIRST timed attempt atPrisma363-DualPulse:1887Blue=true,1888Green=true. One pre-push vision guard had paused74 at17,63 because shadow overlay covereditsplateborder; nofailedgamepush/pulse. Matchingbottominteriorwith8pxborderexcludedverified.9578 andresumed. Storedshadowsremain75[18,63]/74[17,63], realpositionssameafterpurple. Worker3859activatingBlue/Greenandorb139.

East orb approach also requires rocks96[39,64]/97[40,65]. Initialroute96/139foundnoaccessible: navonlymodeledverticaltwoofeightbridgeevents. Installed896E23–30ALLhaveexactThroughON/3xforward/ThroughOFFroute, nofacingrestriction. Updatednavall8andall4directions, awaitingnormalcoordinateverification. No puzzle input or state changed by the failed route checks.
