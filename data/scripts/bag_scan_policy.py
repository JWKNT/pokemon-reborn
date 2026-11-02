"""Pure visible-viewport policy for a bounded seven-row bag scan.

No controls, game/save/runtime reads or hidden item indexes. A four-step scan can
wrap over unseen tail rows; it therefore needs a rendered end-page backfill
unless CLOSE BAG was already visible. Selection/use stays caller-owned.
"""
from pathlib import Path
import re

ROWS = 7
STRIDE = 4


def installed_stride_supported(game_scripts=Path('/Applications/Reborn.app/Contents/Game/Scripts')):
    try:
        bag = (game_scripts / 'Bag.rb').read_text()
        window = (game_scripts / 'SW Subclasses.rb').read_text()
    except OSError:
        return False
    compact = re.sub(r'\s+', '', window)
    return bool(re.search(r'ITEMSVISIBLE\s*=\s*7\b', bag)) and all(token in compact for token in [
        '@index=(@index+@column_max)%@item_max',
        '@index=(@index-@column_max+@item_max)%@item_max',
        'self.top_row=row-(self.page_row_max-1)',
        'self.top_row=[self.top_row,self.row_max-self.page_row_max].min',
    ])


def viewport(names, current, normalize):
    """Require seven core rows; allow the source's extra clipped draw row."""
    ordered = sorted(names, key=lambda v: float(v['y']) + float(v['h'])/2)
    if len(ordered) not in [ROWS, ROWS+1]:
        return None
    observed_labels = [normalize(v['text']) for v in ordered]
    centers = [float(v['y']) + float(v['h'])/2 for v in ordered]
    if any(not label for label in observed_labels) or len(set(observed_labels)) != len(ordered) or any(
            not .055 <= b-a <= .087 for a, b in zip(centers, centers[1:])):
        return None
    # Bag.rb refresh/itemRect draws through top+page_item_max (the eighth edge
    # text). Cursor scrolling still guarantees the FIRST7, independently of
    # whether OCR recovers that clipped extra text on successive captures.
    core = ordered[:ROWS]
    labels = observed_labels[:ROWS]
    selected = next((i for i, row in enumerate(core) if row is current), None)
    if selected is None:
        return None
    return {'labels': labels, 'selected_row': selected,
            'observed_labels': observed_labels,
            'tail_visible': any(label == 'closebag' for label in observed_labels)}


def transition(previous, observed):
    """Prove an ordinary <=4-row advance, or require an actual end-page probe."""
    if previous is None or observed is None:
        return 'uncertain'
    old, new = previous['labels'], observed['labels']
    offsets = {i-new.index(label) for i, label in enumerate(old) if label in new}
    if len(offsets) > 1:
        return 'uncertain'
    if offsets:
        offset = next(iter(offsets))
        advance = offset + observed['selected_row'] - previous['selected_row']
        if 0 <= offset <= STRIDE and 0 <= advance <= STRIDE:
            return 'forward-covered'
        if offset < 0 or advance < 0:
            if observed['selected_row'] >= STRIDE:
                return 'uncertain'
            return 'wrap-covered' if previous['tail_visible'] else 'backfill-tail'
        return 'uncertain'
    # Disjoint complete pages after <=4 normal taps can be a large-pocket wrap.
    # Never infer tail item names: UP4 must render CLOSE BAG before continuing.
    if observed['selected_row'] >= STRIDE:
        return 'uncertain'
    return 'wrap-covered' if previous['tail_visible'] else 'backfill-tail'
