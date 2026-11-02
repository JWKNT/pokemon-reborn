"""Pure installed-source/synthetic UI tests. No actual game input/capture."""
import copy
from datetime import datetime,timezone
import unittest
from PIL import Image
from hardy_piano_queue import (GAME,TARGETS,YS,group_keys,preflight,source_proof,tile_asset,tile_score)


def frozen():
    status={'map':739,'save_mtime':datetime.fromtimestamp(1000,timezone.utc).isoformat(),
            'party':[{'moves':[{'move':'ROCKCLIMB'}]}]+[{'moves':[]} for _ in range(5)]}
    nav={'switches':{'1022':False},'variables':{'391':51},
         'self_switches':{f'739,{eid},A':True for eid in [22,35,36]},
         'positions':{'739':{str(23+i):[14,y] for i,y in enumerate(YS)}}}
    return status,nav


class Tests(unittest.TestCase):
    def test_installed_source(self):
        proof=source_proof()
        self.assertEqual([e['target'][0] for e in proof['tuners']],[17,19,21,16,16,14,15,15])
        self.assertEqual(proof['climb'],[739,5,46,5,8])
        self.assertEqual(proof['open_door'],[739,11,4,740,9,21])

    def test_fresh_initial_only(self):
        status,nav=frozen();preflight(status,nav,now=1001)
        for mutate in [lambda s,n:n['self_switches'].update({'739,36,A':False}),
                       lambda s,n:n['positions']['739'].update({'23':[15,45]}),
                       lambda s,n:n['switches'].update({'1022':True}),
                       lambda s,n:s.update({'map':740})]:
            s,n=copy.deepcopy((status,nav));mutate(s,n)
            with self.assertRaises(ValueError):preflight(s,n,now=1001)
        with self.assertRaises(ValueError):preflight(status,nav,now=1121)

    def test_exact_group_adjacency(self):
        for n in TARGETS:
            if not n:continue
            player,tuner=13,14
            for k in group_keys(n):
                if k.startswith('c:'):
                    self.assertEqual(player+1,tuner);tuner+=1
                elif k.startswith('right:'):player+=1
            self.assertEqual((player,tuner),(13+n,14+n))
        with self.assertRaises(ValueError):group_keys(0)
        with self.assertRaises(ValueError):group_keys(8)

    def test_saved_prefix_resume(self):
        status,nav=frozen()
        for i in range(3):
            nav['positions']['739'][str(23+i)]=[14+TARGETS[i],YS[i]]
            nav.setdefault('variables',{})[str(441+i)]=TARGETS[i]
        preflight(status,nav,now=1001,start_tuner=3)
        with self.assertRaises(ValueError):preflight(status,nav,now=1001)
        wrong=copy.deepcopy(nav);wrong['variables']['443']=6
        with self.assertRaises(ValueError):preflight(status,wrong,now=1001,start_tuner=3)
        wrong=copy.deepcopy(nav);wrong['positions']['739']['26']=[15,33]
        with self.assertRaises(ValueError):preflight(status,wrong,now=1001,start_tuner=3)

    def test_rendered_actual_tuner_relative_square(self):
        for scale in [1,2,4]:
            image=Image.new('RGB',(512*scale,384*scale),'white');tile=tile_asset(604)
            side=32*scale
            # Actual player13,45 at foot256,224; tuner14,45 is one tile east.
            left,top=272*scale,192*scale
            image.paste(tile.resize((side,side),Image.Resampling.NEAREST).convert('RGB'),(left,top))
            score=tile_score(image,tile,(256*scale,224*scale),(13,45),(14,45),scale)
            self.assertEqual(score['score'],1)
            with self.assertRaises(ValueError):tile_score(image,tile,(256*scale,224*scale),(13,45),(15,45),scale)
            image.paste('white',(left,top,left+side,top+side))
            with self.assertRaises(ValueError):tile_score(image,tile,(256*scale,224*scale),(13,45),(14,45),scale)

    def test_open_door_template_and_bounds(self):
        tile=tile_asset(573);image=Image.new('RGB',(512,384),'white')
        image.paste(tile.convert('RGB'),(240,160))
        self.assertEqual(tile_score(image,tile,(256,224),(11,5),(11,4),1)['score'],1)
        with self.assertRaises(ValueError):tile_score(image,tile,(0,0),(11,5),(11,4),1)
        # The closed map paints573 below594: the opaque event573 must cover the
        # actual bars before we credit1022. Underlying573 alone is not enough.
        sheet=Image.open(GAME/'Graphics/Tilesets/Agate Gym.png').convert('RGBA')
        n=594;x=(n-384)%8*32;y=(n-384)//8*32
        closed=sheet.crop((x,y,x+32,y+32));image.paste(closed,(240,160),closed)
        with self.assertRaises(ValueError):tile_score(image,tile,(256,224),(11,5),(11,4),1)


if __name__=='__main__':unittest.main()
