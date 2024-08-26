#!/usr/bin/env python

'''Nested fidget star with a twist
Uses svgSCAD package.
'''

import solid as sd
import numpy as np
import itertools


def koch_snowflake(R, pieces=6, iterations=3):
    scale = 1/3
    base = svg.hexagram(R)
    for _ in range(iterations):
        base2 = sd.scale(scale)(base)
        base3 = sd.translate([(1-scale)*R,0])(base2)
        base += sd.union()(*[sd.rotate([0,0,i*360/pieces])(base3) for i in range(pieces)])
    base = sd.rotate([0,0,30])(base)
    return base

def perimeter(shape, r, segments=6):
    border = sd.circle(r=r, segments=segments)
    final = sd.minkowski()(shape, border)
    final -= shape
    return final

def ring(R, r, height, twist, slices, scale):
    koch = koch_snowflake(R, iterations=0)
    koch = perimeter(koch, r)
    graphic = sd.linear_extrude(height=10, twist=twist, slices=slices, scale=scale)(koch)
    graphic += sd.rotate([180,0,0])(graphic)
    return graphic

def halfPlane(direction, D=1000):
    r'''Create a 2D half plane. Choose D large enough to be "infinity".
    >>> sd.scad_render(halfPlane('N'))
    '\n\ntranslate(v = [0, 1000]) {\n\tsquare(center = true, size = 2000);\n}'
    '''
    planetype = {
        'N':( 0,  D),
        'S':( 0, -D),
        'E':( D,  0),
        'W':(-D,  0),
        'U':( 0,  D),
        'D':( 0, -D),
        'R':( D,  0),
        'L':(-D,  0),
        }
    plane = sd.square(2*D, center=True)
    plane = sd.translate(planetype[direction])(plane)
    return plane

def chamferCircle(r):
    piece = sd.circle(r)
    side = (np.sqrt(2)-1)*r
    side2 = np.sqrt(3-2*np.sqrt(2))*r

    chamfer = sd.square(side)
    chamfer += sd.translate([side,0])(sd.rotate([0,0,45])(sd.square(side2)))
    chamfer += sd.mirror([1,0])(chamfer)
    piece += sd.translate([0,-r])(chamfer)
    return piece

def curvedChamferCircle(r):
    piece = sd.circle(r)
    side = (np.sqrt(2)-1)*r

    # piece += sd.translate([0,-r])(sd.square(side))
    piece += sd.translate([0,-r])(sd.square(r))
    piece -= sd.translate([r*np.sqrt(2), -r*np.sqrt(2)])(piece)
    piece += sd.mirror([1,0])(piece)
    return piece

if __name__ == '__main__':
    fn = 128
    d_base=145
    outer = 3
    # citadel = False
    citadel = True
    d_citadel = 32.5

    # tamiya sizes

    d_bottle = 35
    h_bottle = 45
    n_bottle = 8
    n_grip = 6
    d_large = d_bottle+2

    r=2
    upknob = 70
    # section = sd.translate([(d_base-r)/2, 0])(sd.circle(r))
    section = sd.translate([(d_base-r)/2, 0])(chamferCircle(r))
    # section = sd.translate([(d_base-r)/2, 0])(curvedChamferCircle(r))
    section += sd.translate([(d_base-r)/2, 10])(sd.circle(r))
    # section += sd.translate([(d_base)/2-2*r-d_citadel, 0])(sd.circle(r))
    section += sd.square(r, center=True)
    # section += sd.translate([(d_base)/2-2*r-d_citadel, 2*r+d_citadel])(sd.circle(r))
    section += sd.translate([0, .35*d_base])(sd.circle(2*r))
    section = sd.hull()(section)
    knob = sd.translate([0, upknob])(sd.circle(r=20))
    knob += sd.translate([0, upknob+20])(sd.circle(r=10))
    knob += sd.translate([0, upknob-20])(sd.circle(r=10))
    knob = sd.hull()(knob)
    knob += sd.translate([0, upknob+25])(sd.circle(r=10))
    section += knob
    section += sd.square([10,upknob])
    section = sd.intersection()(section, halfPlane('R'))
    base = sd.cylinder(d=d_base, h=22)
    base = sd.translate([0,0,-2])(base)
    base = sd.rotate_extrude()(section)

    large = sd.cylinder(d=d_large, h=100, center=False)
    large = sd.translate([(d_base-d_large)/2-outer,0,0])(large)
    finger = sd.cylinder(d=d_large-10, h=100, center=True)
    finger = sd.translate([(d_base-d_large)/2-outer,0,0])(finger)
    hole = large + finger
    holes = sd.union()(*[sd.rotate([0,0,i*360/n_bottle])(hole) for i in range(n_bottle)])
    grip = sd.cylinder(d=10, h=100, center=False)
    grip = sd.rotate([20,0,0])(grip)
    grip = sd.translate([20,0,upknob*.8])(grip)
    grips = sd.union()(*[sd.rotate([0,0,i*360/n_grip])(grip) for i in range(n_grip)])

    bottle = sd.cylinder(d=d_bottle, h=h_bottle, center=False)
    bottle = sd.translate([(d_base-d_large)/2-outer,0,0])(bottle)
    bottles = sd.union()(*[sd.rotate([0,0,i*360/n_bottle])(bottle) for i in range(n_bottle)])

    knob_hole = sd.translate([0, upknob])(sd.circle(r=21))
    knob_hole += sd.translate([0, upknob+20])(sd.circle(r=10))
    knob_hole += sd.translate([0, upknob-20])(sd.circle(r=21))
    knob_hole = sd.hull()(knob_hole)
    knob_hole += sd.translate([0, upknob+25])(sd.circle(r=11))
    knob_hole = sd.intersection()(knob_hole, halfPlane('R'))
    knob_hole = sd.rotate_extrude()(knob_hole)
    knob_hole = sd.translate([0, 0, -upknob+10])(knob_hole)
    final = base - holes
    # final += bottles
    final -= grips
    final -= knob_hole
    # final += sd.translate([0,0,h_bottle+15])(final)
    # final = sd.intersection()(sd.cube(1000), final)
    final = sd.scad_render(final, file_header=f'$fn={fn};')
    print(final)


