"""Set only Text Speed to Max through normal UI; source-only dry-run by default.

Development/import reads no screens, current saves, native settings or controls.
--execute requires a fresh Pause Menu (or explicitly --start-options), a new
journal, rendered cursor proof and actual red Max proof. Stops on uncertainty.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
import time
import unicodedata

ROOT = Path(__file__).resolve().parents[1]
GAME = Path('/Applications/Reborn.app/Contents/Game')
CANVASES = {(2272,1816):(112,132,2048,1536), (1024,796):(0,28,1024,768)}


def need(ok, message):
    if not ok:
        raise ValueError(message)


def norm(text):
    text = unicodedata.normalize('NFKD', text.lower()).translate(str.maketrans({'а':'a','о':'o','е':'e','х':'x','к':'k'}))
    value = re.sub('[^a-z0-9]', '', text)
    # Actual session132 Agate crop rendered final Controls "s" as "a".
    return {'duitgame':'quitgame','durtgame':'quitgame','controla':'controls'}.get(value,value)


def center(row):
    return (row['y'] + row['h']/2)*384


def unique_label(rows, name, *, side='left', prefix=False):
    # Narrow observed Options glyph alias; all other label matches stay exact.
    aliases = {'options','uptions'} if norm(name)=='options' else {norm(name)}
    hits = [r for r in rows if ((norm(r['text']).startswith(norm(name))) if prefix else norm(r['text']) in aliases)
            and ((r['x'] < .46) if side=='left' else (r['x'] > .55))]
    need(len(hits)==1, 'Expected one visible '+name+' label')
    return hits[0]


def pause_guard(rows):
    for name in ['Bag','Options','Controls','Quit Game']:
        unique_label(rows,name,side='right')
    need(not any(norm(r['text']) in ['fight','general','accessibility','debug'] for r in rows),
         'Unexpected battle/accessibility/debug screen')
    return unique_label(rows,'Options',side='right')


def options_guard(rows):
    title = unique_label(rows,'Options')
    need(title['y'] < .16, 'Options title is not at the top')
    result = {name:unique_label(rows,name,prefix=True) for name in
              ['Autorunning','Text Speed','Text Skip Wait','BGM Volume','SE Volume']}
    positions = [center(r) for r in result.values()]
    need(all(abs(positions[i+1]-positions[i]-32)<8 for i in range(4)),
         'Installed first five option rows do not match visible layout')
    return result


def source_proof():
    path = GAME/'Scripts/Options.rb'
    src = path.read_text()
    for token in ['_INTL("Text Speed"), [_INTL("Normal"), _INTL("Fast"), _INTL("Max")]',
                  'index = @values.length - 1 if index > @values.length - 1',
                  'return -2 if speed == 2', 'if Input.trigger?(Input::B)',
                  '@selBaseColor = Color.new(31 * 8, 6 * 8, 3 * 8)', 'saveSettings']:
        need(token in src, 'Installed option contract changed: '+token)
    need('AnimatedBitmap.new("Graphics/Pictures/selarrow")' in
         (GAME/'Scripts/SW Subclasses.rb').read_text(), 'Installed cursor asset changed')
    return {'options_source_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
            'values':['Normal','Fast','Max'], 'right_clamps':True,
            'queue':'visible Options selection; visible Text Speed row; RIGHT twice; verify red Max; X to save/exit'}


def find_arrow(image, template, region):
    opaque = [(x,y,tuple(p[:3])) for y in range(template.height) for x in range(template.width)
              if (p:=template.getpixel((x,y)))[3]==255]
    need(len(opaque)>100, 'Installed cursor has too few opaque pixels')
    x0,y0,x1,y1 = region
    sample = opaque[len(opaque)//2]
    candidates=[]
    pix=image.load()
    for y in range(y0,y1-template.height+1):
        for x in range(x0,x1-template.width+1):
            if max(abs(pix[x+sample[0],y+sample[1]][i]-sample[2][i]) for i in range(3))>12:
                continue
            score=sum(max(abs(pix[x+dx,y+dy][i]-color[i]) for i in range(3))<=12
                      for dx,dy,color in opaque)/len(opaque)
            if score>=.96:
                candidates.append((score,x,y))
    need(candidates, 'Rendered installed selection arrow not found')
    candidates.sort(reverse=True)
    _,x,y=candidates[0]
    need(not any(abs(xx-x)>3 or abs(yy-y)>3 for _,xx,yy in candidates[1:]),
         'Multiple rendered selection arrows')
    return {'x':x,'y':y,'center_y':y+template.height/2,'score':candidates[0][0]}


def alignment(target, arrow):
    delta=center(target)-arrow['center_y']
    steps=round(delta/32)
    need(abs(delta-steps*32)<10 and abs(steps)<=9, 'Cursor/target row alignment is uncertain')
    return steps


def max_proof(rows, image, target):
    words=[word for r in rows for word in r.get('words',[]) if norm(word['text']) in ['normal','fast','max']
           and word['x']>.40 and abs(center(word)-center(target))<12]
    need(sorted(norm(w['text']) for w in words)==['fast','max','normal'],
         'Normal/Fast/Max value words need independent visible boxes')
    scores={}
    for word in words:
        x,y,w,h=[word[k] for k in ['x','y','w','h']]
        crop=image.crop((max(0,int(x*512)-2),max(0,int(y*384)-2),
                         min(512,int((x+w)*512)+3),min(384,int((y+h)*384)+3)))
        scores[norm(word['text'])]=sum(r>=220 and g<=100 and b<=100 for r,g,b in crop.getdata())
    need(scores['max']>=8 and scores['max']>4*max(scores['normal'],scores['fast']),
         'Max is not independently proved as the red selected value: '+str(scores))
    return scores


class Runner:
    def __init__(self,args):
        from PIL import Image
        import play
        self.Image,self.play,self.args=Image,play,args
        self.path=args.journal.resolve()
        need(self.path.is_relative_to(ROOT) and not self.path.exists(), 'A NEW workspace journal is required; no blind replay')
        self.work=ROOT/'work'/self.path.stem
        need(not self.work.exists(), 'Existing image evidence directory; use a new journal name')
        self.work.mkdir()
        self.journal={'source':source_proof(),'actions':[],'pending':None,'screens':[]}
        self.template=Image.open(GAME/'Graphics/Pictures/selarrow.png').convert('RGBA')
        self.write()

    def write(self):
        self.path.write_text(json.dumps(self.journal,indent=2)+'\n')

    def capture(self):
        need(len(self.journal['screens'])<7, 'Bounded capture limit')
        self.play.snap()
        native=self.Image.open(self.play.NATIVE).convert('RGB')
        canvas=self.args.canvas or CANVASES.get(native.size)
        need(canvas is not None, 'Uncalibrated native capture; supply --canvas L,T,W,H')
        l,t,w,h=canvas
        need(0<=l and 0<=t and l+w<=native.width and t+h<=native.height and abs(w/h-4/3)<.01,
             'Game canvas is outside image or not4:3')
        game=native.crop((l,t,l+w,t+h)).resize((512,384),self.Image.Resampling.NEAREST)
        path=self.work/f'public-{len(self.journal["screens"])}.png'
        game.resize((1536,1152),self.Image.Resampling.NEAREST).save(path)
        rows=json.loads(subprocess.check_output([str(ROOT/'scripts/observe_words'),str(path)],timeout=20))
        self.journal['screens'].append({'epoch':time.time(),'image':str(path),'rows':rows,'canvas':list(canvas)})
        self.write()
        return rows,game

    def act(self,*keys):
        self.journal['pending']={'keys':list(keys),'epoch':time.time()};self.write()
        self.play.act(*keys)
        self.journal['actions'].append(self.journal['pending']);self.journal['pending']=None;self.write()

    def align(self,target,image,region):
        arrow=find_arrow(image,self.template,region)
        steps=alignment(target,arrow)
        if steps:
            self.act(*(['down:.05' if steps>0 else 'up:.05']*abs(steps)),'wait:.3')
        return steps

    def run(self):
        rows,image=self.capture()
        if not self.args.start_options:
            self.align(pause_guard(rows),image,(256,0,512,384))
            rows,image=self.capture()
            need(alignment(pause_guard(rows),find_arrow(image,self.template,(256,0,512,384)))==0,
                 'Options must be the actually selected Pause command; no C sent')
            self.act('c:.08','wait:.8')
            rows,image=self.capture()
        options=options_guard(rows)
        self.align(options['Text Speed'],image,(0,64,100,320))
        rows,image=self.capture()
        options=options_guard(rows)
        need(alignment(options['Text Speed'],find_arrow(image,self.template,(0,64,100,320)))==0,
             'Text Speed must be the actually selected option; no RIGHT sent')
        before=image.copy()
        self.act('right:.05','right:.05','wait:.3')
        rows,image=self.capture()
        options=options_guard(rows)
        need(alignment(options['Text Speed'],find_arrow(image,self.template,(0,64,100,320)))==0,
             'Text Speed cursor changed unexpectedly')
        selected=max_proof(rows,image,options['Text Speed'])
        other_changes={}
        for name,row in options.items():
            if name=='Text Speed':continue
            cy=round(center(row));rect=(230,cy-13,506,cy+14)
            a,b=before.crop(rect),image.crop(rect)
            changed=sum(max(abs(p[i]-q[i]) for i in range(3))>12 for p,q in zip(a.getdata(),b.getdata()))
            need(changed/(a.width*a.height)<.02, 'Another visible option value changed: '+name)
            other_changes[name]=changed
        self.journal['max_proof']=selected;self.journal['other_visible_options_changed_pixels']=other_changes;self.write()
        self.act('x:.08','wait:.8')
        rows,_=self.capture()
        pause_guard(rows)
        self.journal['complete']=True;self.write()
        print('TEXT SPEED MAX verified and normally saved; stopped at Pause Menu',flush=True)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--execute',action='store_true')
    parser.add_argument('--journal',type=Path)
    parser.add_argument('--start-options',action='store_true')
    parser.add_argument('--canvas',type=lambda s:tuple(map(int,s.split(','))))
    args=parser.parse_args()
    proof=source_proof()
    if not args.execute:
        print(json.dumps(proof,indent=2));return
    need(args.journal is not None,'--execute needs --journal with a new path')
    need((ROOT/'scripts/observe_words').exists(),'Compile observe_words.swift before --execute')
    runner=Runner(args)
    try:runner.run()
    except Exception as exc:
        runner.journal['stopped']=str(exc);runner.write();raise


if __name__=='__main__':
    main()
