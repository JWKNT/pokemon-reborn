"""Type one reviewed quest answer through native UI; never confirm it automatically."""
from play import *
answers={'GMKR@','K=XJ7','F5@@5#','%5H','YGFFX5M','?RG@','J5TR'}
answer=sys.argv[1];assert answer in answers
text=read().lower();compact=re.sub('[^a-z]','',text)
assert 'whatisit' in compact and 'keyboard' in compact,('Expected empty quest keyboard entry',text)
act('wait:.1')
start=time.time()
subprocess.run(['/usr/bin/osascript','-e','on run argv\n tell application "System Events" to keystroke (item 1 of argv)\nend run',answer],check=True)
with (ROOT/'recordings/actions.jsonl').open('a')as f:f.write(json.dumps({'start':start,'end':time.time(),'keys':'native text entry '+answer})+'\n')
act('wait:.5');print(read(),flush=True)
print('TEXT ENTERED; INSPECT BEFORE PRESSING RETURN',flush=True)
