#!/usr/bin/env python

from __future__ import division

import sys, cairo, json, os

def rgba_to_intensity(r,g,b,a):
    intensity = ( (1 - max(r,g,b)/255) * a/255 )
    if int(os.environ.get('INVERT', '0')): intensity = 1 - intensity
    return intensity

def getPixelRGB(buf, width, x, y):
    # Assume that the surface format is FORMAT_ARGB32.
    offset = ((y*width) + x ) * 4
    B = ord(buf[offset+0])
    G = ord(buf[offset+1])
    R = ord(buf[offset+2])
    A = 255
    I = rgba_to_intensity(R,G,B,A)
    return R,G,B,A,I

def getPixelRGBA(buf, width, x, y):
    # Assume that the surface format is FORMAT_ARGB32.
    offset = ((y*width) + x ) * 4
    B = ord(buf[offset+0])
    G = ord(buf[offset+1])
    R = ord(buf[offset+2])
    A = ord(buf[offset+3])
    I = rgba_to_intensity(R,G,B,A)
    return R,G,B,A,I

def calcBlock(surface):
    buf = surface.get_data()
    width, height = surface.get_width(), surface.get_height()
    getPixel = {cairo.FORMAT_ARGB32:getPixelRGBA,
                cairo.FORMAT_RGB24:getPixelRGB}[surface.get_format()]

    intensity_total = 0
    intensity_moment_x = 0
    intensity_moment_y = 0
    for y in range(height):
        for x in range(width):
            intensity = getPixel(buf, width, x, y)[-1]    # we only care about 'I'
            intensity_moment_x += (x+0.5)*intensity    #
            intensity_moment_y += (y+0.5)*intensity    # a pixel's "weight" is at the center of the pixel
            intensity_total += intensity

    if intensity_total == 0: return {'COM_x':.5, 'COM_y':.5, 'intensity':0}    # Avoid division by 0.

    COM_x = intensity_moment_x / intensity_total
    COM_y = intensity_moment_y / intensity_total
    normalized_intensity = intensity_total / (width * height)
    return {'COM_x':COM_x/width, 'COM_y':COM_y/height, 'intensity':normalized_intensity}

def scaleSurface(surface, new_width, new_height):
    width, height = surface.get_width(), surface.get_height()
    new_surf = surface.create_similar(surface.get_content(), new_width, new_height)
    ctx = cairo.Context(new_surf)
    ctx.scale(new_width/width, new_height/height)
    pat = cairo.SurfacePattern(surface)
    pat.set_filter(cairo.FILTER_FAST)
    ctx.set_source(pat)
    ctx.rectangle(0, 0, new_width, new_height)
    ctx.fill()
    return new_surf

def splitSurface(surface, x_pieces, y_pieces):
    width, height = surface.get_width(), surface.get_height()
    if width % x_pieces:
        raise ValueError, "Image width (%d) not divisible by %d"%(width, x_pieces,)
    if height % y_pieces:
        raise ValueError, "Image height (%d) not divisible by %d"%(height, y_pieces,)
    miniWidth = int(width / x_pieces)
    miniHeight = int(height / y_pieces)

    miniSurfs = {}
    for y in range(y_pieces):
        for x in range(x_pieces):
            this_minisurf = surface.create_similar(surface.get_content(), miniWidth, miniHeight)
            ctx = cairo.Context(this_minisurf)
            origin_x, origin_y = (miniWidth * x), (miniHeight * y)
            ctx.set_source_surface(surface, 0 - origin_x, 0 - origin_y)
            ctx.rectangle(0, 0, miniWidth, miniHeight)
            ctx.fill()
            miniSurfs[(x,y)] = this_minisurf
    return miniSurfs

CALC_IMAGE_SLICES = [3,5,7]
def calcImage(surface):
    image_COMs = {}
    for numSlices in CALC_IMAGE_SLICES:
        image_COMs[numSlices] = calcImageSingle(surface, numSlices)
    return image_COMs

def calcImageSingle(surface, numSlices):
    scaled = scaleSurface(surface, surface.get_width()*numSlices, surface.get_height()*numSlices)
    miniSurfs = splitSurface(scaled, numSlices, numSlices)
    miniSurf_COMs = {}  # COM = Center Of Mass
    for y in range(numSlices):
        for x in range(numSlices):
            miniSurf_COMs['%d,%d'%(x,y)] = calcBlock(miniSurfs[x,y])
    return miniSurf_COMs


if __name__ == '__main__':
    for pngPath in sys.argv[1:]:
        surface = cairo.ImageSurface.create_from_png(open(pngPath, 'rb'))
        json.dump(calcImage(surface), open(pngPath+'.com', 'w'), indent=2, sort_keys=True)
