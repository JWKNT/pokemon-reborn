"""Enter an observed four-digit scripture prompt using ordinary arrow keys."""
from play import *
import re
from PIL import Image
wanted=sys.argv[1];assert len(wanted)==4 and wanted.isdigit()
if '--current' not in sys.argv:raise SystemExit('Requires --current VERIFIED_VALUE because this font misreads 3 as 1.')
def value():
 snap();im=Image.open(STATE);w,h=im.size;crop=ROOT/'work/number-prompt.png';im.crop((int(w*.735),int(h*.605),int(w*.905),int(h*.669))).resize((680,256)).save(crop);r=json.loads(subprocess.check_output([str(ROOT/'scripts/observe'),str(crop)]));print(r,flush=True);nums=[]
 for v in r:
  z=v['text'].strip().translate(str.maketrans({'O':'0','o':'0','I':'1','l':'1','|':'1'}));z=z.replace(' ','')
  if re.fullmatch(r'\d{4}',z):nums.append(z)
 if not nums:
  joined=''.join(v['text'].strip().replace(' ','') for v in sorted(r,key=lambda v:v['x']))
  if re.fullmatch(r'\d{4}',joined):nums=[joined]
 if len(nums)!=1:raise SystemExit('Number prompt requires visual review')
 return nums[0]
current=sys.argv[sys.argv.index('--current')+1];keys=['right'] # Game source initializes cursor at the last digit.
for i,(a,b) in enumerate(zip(current,wanted)):
 n=(int(b)-int(a))%10;keys+=['up']*n if n<=5 else ['down']*(10-n)
 if i<3:keys+=['right']
act(*keys,'wait:0.4')
print('Expected',wanted,'VERIFY work/number-prompt.png visually before confirming.');value()
