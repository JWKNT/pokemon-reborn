"""Summarize latest flushed official battle log, read-only; never predict future RNG."""
import pathlib,re,json
folder=pathlib.Path.home()/'Library/Application Support/Pokemon Reborn/Battle Logs'
files=[p for p in folder.glob('*.txt') if re.match(r'\d{4}-\d{2}-\d{2}_.* - Aster(?: and| vs\.)',p.name)]
p=max(files,key=lambda p:p.stat().st_mtime);text=p.read_text(errors='replace');rounds=re.findall(r'Round (\d+)',text)
events=[l for l in text.splitlines() if re.search(r'used |lost \d+ HP|now has |fainted|rose!|fell!|Trick Room|twisted|was burned|recovered',l,re.I) and len(l)<150]
print(json.dumps({'file':p.name,'mtime':p.stat().st_mtime,'bytes':p.stat().st_size,'last_round':rounds[-1] if rounds else None,'recent_events':events[-24:]},indent=2))
