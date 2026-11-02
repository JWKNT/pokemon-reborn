"""Buy reviewed medicine and travel to the safe side of the castle trigger."""
import os,subprocess,sys,json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
os.environ.update(REBORN_FAST_KEYS='1',REBORN_COORD_CACHE='1',REBORN_ROUTE_CHUNK='84')
def run(s,*a):
 print('CASTLE TRAVEL',s,*a,flush=True);subprocess.run([sys.executable,str(R/'scripts'/f'{s}.py'),*map(str,a)],check=True)
s=json.loads((R/'notes/Postgame259-CastleBuild-status.json').read_text());assert s['trainer']['money']>=21600 and all(m['level']==120 and m['hp']==m['totalhp'] for m in s['party'])
run('eventq',38,5,'talk');run('choose_dialog','Buy|Sell|Quit','Buy')
run('shop_buy','Full Restore',4,3000);run('shop_buy','Ultra Potion',8,1200)
run('play','x','wait:.6');run('choose_dialog','Buy|Sell|Quit','Quit');run('play','c','wait:1');run('overworld')
run('checkpoint','Postgame259-Supplied')
run('eventq',38,6,'enter');run('fly_to',292,'--carrier','Zapdos')
run('eventq',292,1,'enter');run('eventq',293,3,'enter');run('eventq',293,16,'enter')
for start,end in [(313,316),(316,317),(317,318),(318,315)]:run('city_enter',start,end)
run('q','315,10,19');run('checkpoint','Postgame259-CastleReady')
nav=json.loads((R/'notes/Postgame259-CastleReady-navigation.json').read_text());assert nav['variables']['670']==2
print('READY BEFORE CASTLE STORY TRIGGER',flush=True)
