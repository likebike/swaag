#!/usr/bin/env python
# -*- coding: utf-8 -*-

# LiberationMono Regular, size 9 ~= Cairo 'LiberationMono' n b 12.75 # Terminal "box" size = 7x14
#
# ../font2png.py 'LiberationMono' n b 12.75 7x14 0,11         # Original dimensions
# ../font2png.py 'LiberationMono' n b 114.75 63x126 -3,99     # High-res dimensions

import sys, cairo

#def text_size(font, font_size, text):
#    # This is a placeholder until I figure out how to use cairo.ScaledFont properly.
#    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, 128, 128)
#    ctx = cairo.Context(surface)
#    ctx.set_font_size(font_size)
#    ctx.set_font_face(font)
#    ctx.move_to(50, 20)
#    (x, y, width, height, dx, dy) = extents = ctx.text_extents(text)
#    #print(x, y, width, height, dx, dy, width+dx)
#    ctx.show_text(text)
#
#    ctx.move_to(50, 50)
#    (x, y, width, height, dx, dy) = extents = ctx.text_extents(text*10)
#    #print(x, y, width, height, dx, dy)
#    ctx.show_text(text*10)
#    surface.write_to_png(text+".png")
#    
#    del ctx
#    del surface
#    return width, height

def render_char(char, font_family, font_slant, font_weight, font_size, box_size, origin):
    font = cairo.ToyFontFace(font_family, {'n':cairo.FONT_SLANT_NORMAL}[font_slant], {'n':cairo.FONT_WEIGHT_NORMAL, 'b':cairo.FONT_WEIGHT_BOLD}[font_weight])
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, box_size[0], box_size[1])
    ctx = cairo.Context(surface)
    ctx.set_font_size(font_size)
    ctx.set_font_face(font)
    ctx.set_source_rgb(0,0,0)
    ctx.move_to(origin[0], origin[1])   # NOTE that there seems to be a bug with move_to and show_text.  It only renders to integer coordinates.  :/
    ctx.show_text(char)
    surface.write_to_png('%03d.png'%(ord(char),))

def render_ascii(*args):
    for c in u''' !"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijklmnopqrstuvwxyz{|}~€‚ƒ„…†‡ˆ‰Š‹ŒŽ‘’“”•–—˜™š›œžŸ¡¢£¤¥¦§¨©ª«¬®¯°±²³´µ¶·¸¹º»¼½¾¿ÀÁÂÃÄÅÆÇÈÉÊËÌÍÎÏÐÑÒÓÔÕÖ×ØÙÚÛÜÝÞßàáâãäåæçèéêëìíîïðñòóôõö÷øùúûüýþÿ''':
    #for c in r''' !"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijklmnopqrstuvwxyz{|}~''':
        render_char(c, *args)

if __name__ == '__main__':
    font_family = sys.argv[1]
    font_slant = sys.argv[2]
    font_weight = sys.argv[3]
    font_size = float(sys.argv[4])
    box_size = [int(x) for x in sys.argv[5].split('x')]
    origin = [float(x) for x in sys.argv[6].split(',')]
    render_ascii(font_family, font_slant, font_weight, font_size, box_size, origin)

