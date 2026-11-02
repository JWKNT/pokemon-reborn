"""Identify the two tournament backdrops from rendered pixels only."""
from PIL import Image


def observe(path):
    im = Image.open(path).convert('RGB')
    w, h = im.size
    # Above the opponent sprites and to the right of the left-hand HUD.
    # Sigilyph's upper wing covers the old center patch. The far-right
    # strip stays above both opponent sprites in this window layout.
    patch = im.crop((int(w*.88), int(h*.086), int(w*.92), int(h*.113)))
    pixels = list(patch.getdata())
    dark = sum(max(p) < 65 for p in pixels)/len(pixels)
    lilac = sum(r > 110 and b > 135 and b > g+15 for r, g, b in pixels)/len(pixels)
    if dark > .65:
        return 'inverse'
    if lilac > .65:
        return 'misty'
    return 'unknown'
