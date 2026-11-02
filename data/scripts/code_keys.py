"""Build digit adjustments from a visually verified value; no game access."""
import sys
old,new=sys.argv[1:3];assert len(old)==len(new)==4
keys=['right']
for i,(x,y) in enumerate(zip(old,new)):
 d=(int(y)-int(x))%10;keys+=['up']*d if d<=5 else ['down']*(10-d)
 if i<3:keys.append('right')
print(' '.join(keys))
