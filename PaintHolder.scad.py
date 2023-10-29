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

if __name__ == '__main__':
    R = 62
    fn = 64
    d_base=145
    d_small=27
    outer = 3
    # citadel = False
    citadel = True
    d_citadel = 32.5

    if citadel:
        d_bottle = d_citadel
        h_bottle = 45
        n_bottle = 9
    else:
        d_bottle = 25
        h_bottle = 80
        n_bottle = 12
    d_large = d_bottle+2

    r=2
    upknob = 70
    section = sd.translate([(d_base-r)/2, 0])(sd.circle(r))
    section += sd.translate([(d_base-r)/2, 10])(sd.circle(r))
    section += sd.translate([(d_base)/2-2*r-d_citadel, 0])(sd.circle(r))
    # section += sd.translate([(d_base)/2-2*r-d_citadel, 2*r+d_citadel])(sd.circle(r))
    section += sd.translate([0, .3*d_base])(sd.circle(2*r))
    section = sd.hull()(section)
    knob = sd.translate([0, upknob])(sd.circle(r=20))
    knob += sd.translate([0, upknob+20])(sd.circle(r=10))
    knob += sd.translate([0, upknob-20])(sd.circle(r=10))
    knob = sd.hull()(knob)
    section += knob
    section += sd.square([10,upknob])
    section = sd.intersection()(section, halfPlane('R'))
    base = sd.cylinder(d=d_base, h=22)
    base = sd.translate([0,0,-2])(base)
    base = sd.rotate_extrude()(section)

    large = sd.cylinder(d=d_large, h=100, center=False)
    large = sd.translate([(d_base-d_large)/2-outer,0,10])(large)
    small = sd.cylinder(d=d_small, h=100, center=False)
    small = sd.translate([(d_base-d_large)/2-outer,0,0])(small)
    finger = sd.cylinder(d=d_small-10, h=100, center=True)
    finger = sd.translate([(d_base-d_large)/2-outer,0,0])(finger)
    grip = sd.cylinder(d=10, h=100, center=False)
    grip = sd.translate([20,0,upknob*.8])(grip)
    hole = large + finger + grip
    holes = sd.union()(*[sd.rotate([0,0,i*360/n_bottle])(hole) for i in range(n_bottle)])

    bottle = sd.cylinder(d=d_bottle, h=h_bottle, center=False)
    bottle = sd.translate([(d_base-d_large)/2-outer,0,0])(bottle)
    bottles = sd.union()(*[sd.rotate([0,0,i*360/n_bottle])(bottle) for i in range(n_bottle)])

    final = base - holes + bottles
    final -= sd.translate([0,0,-upknob])(final)
    final = sd.scad_render(final, file_header=f'$fn={fn};')
    print(final)


