from nav import *
from locate import locate
assert locate(293)[0]==293
p=ROOT/'notes/navigation-state.json';v=json.loads(p.read_text());v['variables']['150']=7;p.write_text(json.dumps(v))
for a,b in [(0,2),(2,4),(4,5)]:subprocess.run([sys.executable,str(ROOT/'scripts/party_swap.py'),str(a),str(b)],check=True)
save();raw=subprocess.check_output(['ruby',str(ROOT/'scripts/status.rb')],stderr=subprocess.DEVNULL);(ROOT/'notes/g8-before-cain.json').write_bytes(raw);v=json.loads(raw)
expected=['SWAMPERT','ARCANINE','AMPHAROS','DRAPION','COFAGRIGUS','KLINKLANG'];assert [p['species'] for p in v['party']]==expected
assert all(p['hp']==p['totalhp'] and p['status'] is None for p in v['party'])
assert v['party'][-1]['item']=='WIDELENS'
print('SAVED AND VERIFIED FULL TEAM AND CHESS ORDER',flush=True)
