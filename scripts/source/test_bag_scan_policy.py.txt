"""Pure menu geometry/coverage fixtures; no inputs, live files or hidden game data."""
import unittest
from bag_scan_policy import ROWS, STRIDE, viewport, transition, installed_stride_supported


def labels(count):
    return [f'item{i}' for i in range(count-1)] + ['closebag']


def snap_model(count, index, top):
    return {'labels': labels(count)[top:top+ROWS], 'selected_row': index-top,
            'tail_visible': top+ROWS >= count}


def move(count, index, top, direction, steps=STRIDE):
    seen = set(snap_model(count, index, top)['labels'])
    for _ in range(steps):
        index = (index+direction) % count
        if index < top:
            top = index
        if index > top+ROWS-1:
            top = index-ROWS+1
        top = min(top, count-ROWS)
        seen.update(snap_model(count, index, top)['labels'])
    return index, top, seen


class BagStrideTests(unittest.TestCase):
    def test_source_guard_and_complete_observed_rows(self):
        self.assertTrue(installed_stride_supported())
        names = [{'text':f'Item{i}', 'y':.12+i*.071, 'h':.035} for i in range(7)]
        self.assertIsNotNone(viewport(names, names[5], str.lower))
        self.assertIsNone(viewport(names[:-1], names[5], str.lower))
        duplicate = [dict(x) for x in names]; duplicate[6]['text']='Item5'
        self.assertIsNone(viewport(duplicate, duplicate[5], str.lower))
        irregular = [dict(x) for x in names]; irregular[4]['y'] += .03
        self.assertIsNone(viewport(irregular, irregular[5], str.lower))
        edge = names + [{'text':'CLOSEBAG', 'y':.12+7*.071, 'h':.035}]
        eight = viewport(edge, edge[5], str.lower)
        self.assertEqual(eight['labels'], [f'item{i}' for i in range(7)])
        self.assertTrue(eight['tail_visible'])
        self.assertEqual(eight['observed_labels'][-1], 'closebag')
        self.assertIsNone(viewport(edge, edge[7], str.lower))
        self.assertIsNone(viewport(edge+[{'text':'unexpected9', 'y':.12+8*.071, 'h':.035}], edge[5], str.lower))

    def test_wrap_requires_end_page_before_unseen_tail_is_credited(self):
        old = snap_model(20, 17, 11)
        i,t,_ = move(20,17,11,1)
        new = snap_model(20,i,t)
        self.assertEqual(transition(old,new),'backfill-tail')
        i,t,_ = move(20,i,t,-1)
        tail = snap_model(20,i,t)
        self.assertTrue(tail['tail_visible'])
        i,t,_ = move(20,i,t,1)
        self.assertEqual(transition(tail,snap_model(20,i,t)),'wrap-covered')
        # A small pocket wrap can still share several rows; overlap alone is
        # insufficient. Its reversed ordered offset still requests backfill.
        old = snap_model(12,9,3); i,t,_ = move(12,9,3,1)
        self.assertEqual(transition(old,snap_model(12,i,t)),'backfill-tail')

    def test_uncertain_or_overlong_motion_is_not_credited(self):
        old=snap_model(40,12,6)
        i,t,_=move(40,12,6,1,5)
        self.assertEqual(transition(old,snap_model(40,i,t)),'uncertain')
        self.assertEqual(transition(old,None),'uncertain')

    def test_exhaustive_valid_seven_row_windows_leave_no_coverage_holes(self):
        cases=0
        for count in range(7,81):
            for top in range(count-ROWS+1):
                for index in range(top,top+ROWS):
                    old=snap_model(count,index,top)
                    i,t,intermediate=move(count,index,top,1)
                    new=snap_model(count,i,t)
                    observed=set(old['labels'])|set(new['labels'])
                    result=transition(old,new)
                    self.assertNotEqual(result,'uncertain',(count,index,top))
                    if result=='backfill-tail':
                        i,t,_=move(count,i,t,-1)
                        tail=snap_model(count,i,t)
                        self.assertTrue(tail['tail_visible'],(count,index,top))
                        observed.update(tail['labels'])
                    self.assertTrue(intermediate<=observed,(count,index,top,intermediate-observed))
                    cases+=1
        self.assertEqual(cases,19425)


if __name__=='__main__':
    unittest.main()
