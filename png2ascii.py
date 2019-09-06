#!/usr/bin/env python

from __future__ import division

import sys, json, glob, os, re, codecs, math, cairo
import centerOfInk, correlate


def pad_image(png_path, box_size, padding):
    surface = cairo.ImageSurface.create_from_png(open(png_path, 'rb'))
    size = surface.get_width(), surface.get_height()
    new_size = [int(math.ceil((padding[i]+size[i])/box_size[i])*box_size[i]) for i in [0,1]]
    new_surf = surface.create_similar(surface.get_content(), new_size[0], new_size[1])
    ctx = cairo.Context(new_surf)
    ctx.set_source_surface(surface, padding[0], padding[1])
    ctx.rectangle(padding[0], padding[1], size[0], size[1])
    ctx.fill()
    #new_surf.write_to_png('padded.png')
    return new_surf

def calculate_image_COMs(surface, box_size):
    width, height = surface.get_width(), surface.get_height()
    if width % box_size[0]:
        raise ValueError, "Image width (%d) not divisible by box width (%d)"%(width, box_size[0])
    if height % box_size[1]:
        raise ValueError, "Image height (%d) not divisible by box height (%d)"%(height, box_size[1])
    x_pieces, y_pieces = int(width/box_size[0]), int(height/box_size[1])
    image_COMs = {}
    miniSurfs = centerOfInk.splitSurface(surface, x_pieces, y_pieces)
    for y in range(y_pieces):
        for x in range(x_pieces): image_COMs[(x,y)] = centerOfInk.calcImage(miniSurfs[(x,y)])
    return image_COMs

def load_char_COMs(render_dir):
    COMs = {}
    for f in glob.glob(os.path.join(render_dir, '*.com')):
        pattern = '^%s/([0-9]+).png.com$'%(os.path.dirname(f))
        matchObj = re.search(pattern, f)
        charCode = int(matchObj.group(1))
        COM = {}
        for numSlices,val in json.load(open(f)).items(): COM[int(numSlices)] = val
        COMs[charCode] = COM
    return COMs


def correlate_image(image_COMs, char_COMs, intensity_weight):
    #
    #  The user specifies a weighting on Intensity, where:
    #
    #   intensity_weight == 0:  100% positional
    #   intensity_weight == 1:  100% intensity
    #
    #  "Naturally", the intensity_weight is 0.5, meaning equal weighting between position and intesity.
    #
    #  The constant weighting factors A, B, and C above can be calculated as follows:
    #
    #   A = 0.5 * (1-intensity_weight)
    #   B = 0.5 * (1-intensity_weight)
    #   C = intensity_weight
    #
    #  Since 0 <= intensity_weight <= 1, we know that (A + B + C) == 1
    #
    #  (COM_x, COM_y) as a whole represent one quantity, and Intensity represents a second quantity, so the
    #  "natural" weightings for these are such that each quantity accounts for half of the net effect. Since
    #  A and B both modify the positional quantity, these give equal weighting to position and intensity when
    #  intensity_weight == 0.5

    WEIGHTS = { 'x':0.5 * (1-intensity_weight),
                'y':0.5 * (1-intensity_weight),
                'i':intensity_weight }

    # A division naturally contributes N elements to the Grand Vector Comparison, where N = 3*(division^2)
    # For a [3,5,7] split, the "natural" weights would be [27, 75, 147], equivalent to [10.9%, 30.1%, 59.0%].
    # For equal weightings, we multiply by the inverses: [9.22, 3.32, 1.69], or, equivalently, [0.65, 0.23, 0.12]
    #
    # Finally, we may not want equal weighting, so we can finally multiply these items by another weighting. For example,
    # we could use [1.3, 1.2, 1.1] if we wanted division 3 to have higher value than 5, which has higher value than 7
    #
    # It is completely unnecessary for the elements to add to 1, so don't worry about that
    DIVISION_WEIGHTS = { 3: (0.647805394 * 2.25),
                         5: (0.233209942 * 1.50),
                         7: (0.118984664 * 1.00) }
                        
    sliceCharCodes = {}
    for sliceCoord,sliceCOM in sorted(image_COMs.items()):
        slice_vector, weights = [], []
        for numSlices,COM in sorted(sliceCOM.items()):
            for coord,subCOM in sorted(COM.items()):
                slice_vector.extend( (subCOM['COM_x'], subCOM['COM_y'], subCOM['intensity']) );
                weights.extend( (DIVISION_WEIGHTS[numSlices]*WEIGHTS['x'],
                                 DIVISION_WEIGHTS[numSlices]*WEIGHTS['y'],
                                 DIVISION_WEIGHTS[numSlices]*WEIGHTS['i']) )
        charCorrelations = {}
        for charCode,charCOM in char_COMs.items():
            char_vector = []
            for numSlices,COM in sorted(charCOM.items()):
                for coord,subCOM in sorted(COM.items()):
                    char_vector.extend( (subCOM['COM_x'], subCOM['COM_y'], subCOM['intensity']) )
            charCorrelations[charCode] = correlate.correlate(slice_vector, char_vector, weights)
        sliceCharCodes[sliceCoord] = sorted([(charCorrelations[k],k) for k in charCorrelations])[-1]
    return sliceCharCodes


def render_image(sliceCharCodes):
    width = max([x for x,y in sliceCharCodes]) + 1
    height = max([y for x,y in sliceCharCodes]) + 1
    for y in range(height):
        for x in range(width):
            c = unichr(sliceCharCodes[(x,y)][1])
            sys.stdout.write(c)
        sys.stdout.write('\n')


if __name__ == '__main__':
    box_size = [int(x) for x in sys.argv[1].split('x')]
    padding = [int(x) for x in sys.argv[2].split(',')]
    png_path = sys.argv[3]
    render_dir = sys.argv[4]
    intensity_weight = float(sys.argv[5])
    sys.stdout = codecs.getwriter("utf-8")(sys.stdout)  # This is necessary to print extended ascii chars.
    char_COMs = load_char_COMs(render_dir)
    padded_image = pad_image(png_path, box_size, padding)
    image_COMs = calculate_image_COMs(padded_image, box_size)
    cor_results = correlate_image(image_COMs, char_COMs, intensity_weight)
    render_image(cor_results)

