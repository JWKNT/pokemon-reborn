"""Enter the inspected seven-digit password via arrows; stop before confirmation."""
from play import *
t=read().lower()
if 'enter password' not in t and 'enter passuord' not in t:raise SystemExit('Password prompt review')
# Installed Window_InputNumberPokemon starts on its last digit; right wraps first.
initial=sys.argv[1];assert len(initial)==7 and initial.isdigit()
keys=['right']
for i,digit in enumerate('5083164'):
 n=(int(digit)-int(initial[i]))%10;keys.extend(['up' if n<=5 else 'down']*(n if n<=5 else 10-n))
 if i<6:keys.append('right')
act(*keys,'wait:.7');print(read(),flush=True)
print('5083164 SET — confirmation intentionally pending visual check',flush=True)
