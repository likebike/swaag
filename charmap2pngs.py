#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division

import sys, os, cairo
import centerOfInk

def extractChars(chars, surface):
    lines = [l.strip() for l in chars.splitlines()]
    for l in lines: assert len(l) == len(lines[0])  # Make sure our input is rectangular
    width, height = surface.get_width(), surface.get_height()
    boxWidth, boxHeight = width/len(lines[0]),  height/len(lines)
    assert abs(boxWidth-int(boxWidth)) < 0.001
    assert abs(boxHeight-int(boxHeight)) < 0.001
    boxWidth = int(boxWidth)
    boxHeight = int(boxHeight)
    miniSurfs = centerOfInk.splitSurface(surface, len(lines[0]), len(lines))
    for y in range(len(lines)):
        if y in [0, 1, len(lines)-1, len(lines)-2]:             #
            for c in lines[y]: assert c in [lines[0][0], lines[1][1]]   # Exclude Borders.
            continue                                            #
        for x in range(len(lines[0])):
            if x in [0, 1, len(lines[0])-1, len(lines[0])-2]:   #
                assert lines[y][x] in [lines[0][0], lines[1][1]]        # Exclude Borders.
                continue                                        #
            miniSurfs[(x,y)].write_to_png('%03d.png'%(ord(lines[y][x]),))
    return (boxWidth, boxHeight)

if __name__ == '__main__':
    chars_txt = sys.argv[1]
    chars_png = sys.argv[2]
    surface = cairo.ImageSurface.create_from_png(open(chars_png, 'rb'))

    chars = open(chars_txt).read().decode('utf8')

    # It's possible that this contains an ascii border (unicode \u2588) with unicode characters.
    # For sake of the above logic's simplicity, we want to replace every "\u2588\u2588" pair with a single character,
    # so that it contributes 1 to length, not 2. We'll use a unicode 'Wei' (\u56d7) although any non-space character would do.
    if u'\u3000' in chars: chars = chars.replace(u'\u2588\u2588', u'\u56d7')

    box_size = extractChars(chars, surface)

    if not int(os.environ.get('QUIET', '0')): print("Complete. Box size is %dx%d" % box_size)
