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

if __name__ == '__main__':
    R = 62
    fn = 64
    d_base=145
    d_small=27
    outer = 3
    # citadel = False
    citadel = True

    if citadel:
        d_bottle = 32.5
        h_bottle = 45
        n_bottle = 9
    else:
        d_bottle = 25
        h_bottle = 80
        n_bottle = 12
    d_large = d_bottle+2

    base = sd.cylinder(d=d_base, h=22)
    base = sd.translate([0,0,-2])(base)
    large = sd.cylinder(d=d_large, h=100, center=False)
    large = sd.translate([(d_base-d_large)/2-outer,0,10])(large)
    small = sd.cylinder(d=d_small, h=100, center=False)
    small = sd.translate([(d_base-d_large)/2-outer,0,0])(small)
    finger = sd.cylinder(d=d_small-10, h=100, center=True)
    finger = sd.translate([(d_base-d_large)/2-outer,0,0])(finger)
    hole = large + finger
    holes = sd.union()(*[sd.rotate([0,0,i*360/n_bottle])(hole) for i in range(n_bottle)])

    bottle = sd.cylinder(d=d_bottle, h=h_bottle, center=False)
    bottle = sd.translate([(d_base-d_large)/2-outer,0,0])(bottle)
    bottles = sd.union()(*[sd.rotate([0,0,i*360/n_bottle])(bottle) for i in range(n_bottle)])

    final = base - holes + bottles
    final = sd.scad_render(final, file_header=f'$fn={fn};')
    print(final)


