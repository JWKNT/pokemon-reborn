"""Pure synthetic rendered-menu fixtures; no controls/live screenshots."""
import unittest
from PIL import Image, ImageDraw
from text_speed_max import (GAME, alignment, find_arrow, max_proof,
                            options_guard, pause_guard, source_proof)


def row(text,x=.06,y=80,w=.28,h=20):
    return {'text':text,'x':x,'y':y/384,'w':w,'h':h/384}


class Tests(unittest.TestCase):
    def test_source(self):
        self.assertEqual(source_proof()['values'],['Normal','Fast','Max'])
        self.assertTrue(source_proof()['right_clamps'])

    def test_pause_guard(self):
        rows=[row(n,x=.7,y=32+i*32) for i,n in enumerate(['Bag','Options','Controls','Quit Game'])]
        self.assertEqual(pause_guard(rows)['text'],'Options')
        alias=[dict(r,text='Uptions') if r['text']=='Options' else r for r in rows]
        self.assertEqual(pause_guard(alias)['text'],'Uptions')
        with self.assertRaises(ValueError):pause_guard([dict(r,x=.3) if r['text']=='Uptions' else r for r in alias])
        with self.assertRaises(ValueError):pause_guard([dict(r,text='Actions') if r['text']=='Options' else r for r in rows])
        with self.assertRaises(ValueError):pause_guard(rows+[row('Fight')])
        with self.assertRaises(ValueError):pause_guard([r for r in rows if r['text']!='Controls'])

    def test_options_guard(self):
        rows=[row('Options',y=12)]+[row(n,y=80+i*32) for i,n in enumerate(
            ['Autorunning','Text Speed','Text Skip Wait','BGM Volume','SE Volume'])]
        self.assertEqual(options_guard(rows)['Text Speed']['text'],'Text Speed')
        rows[2]=row('Battle Scene',y=112)
        with self.assertRaises(ValueError):options_guard(rows)

    def test_actual_static_arrow(self):
        template=Image.open(GAME/'Graphics/Pictures/selarrow.png').convert('RGBA')
        image=Image.new('RGB',(512,384),'white')
        image.paste(template,(360,40),template)
        arrow=find_arrow(image,template,(256,0,512,120))
        self.assertEqual((arrow['x'],arrow['y']),(360,40))
        self.assertEqual(alignment(row('Options',x=.73,y=44),arrow),0)
        self.assertEqual(alignment(row('Options',x=.73,y=108),arrow),2)
        image.paste(template,(360,80),template)
        with self.assertRaises(ValueError):find_arrow(image,template,(256,0,512,120))

    def test_max_red_word_proof(self):
        words=[row(n,x=x,y=112,w=.09) for n,x in [('Normal',.44),('Fast',.64),('Max',.82)]]
        rows=[dict(row('Normal Fast Max',x=.44,y=112),words=words)]
        target=row('Text Speed',y=112)
        image=Image.new('RGB',(512,384),'white')
        ImageDraw.Draw(image).rectangle((424,116,440,128),fill=(248,48,24))
        self.assertGreater(max_proof(rows,image,target)['max'],8)
        image=Image.new('RGB',(512,384),'white')
        ImageDraw.Draw(image).rectangle((331,116,344,128),fill=(248,48,24))
        with self.assertRaises(ValueError):max_proof(rows,image,target)
        with self.assertRaises(ValueError):max_proof([dict(rows[0],words=words[:2])],image,target)


if __name__=='__main__':unittest.main()
