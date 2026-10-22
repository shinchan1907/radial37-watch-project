"""Phase 1 proportion study. Millimeters. NOT a manufacturing release."""
from cadgen import build123d as bd

CASE_OD = 37.0
LUG_GAP = 18.0
LUG_TO_LUG = 44.0
BODY_BOTTOM = 1.5
BODY_TOP = 7.0
DIAL_OD = 32.0
CRYSTAL_OD = 33.0

def ring(ro, ri, z0, height):
    return bd.Pos(0, 0, z0 + height/2) * (bd.Cylinder(ro, height) - bd.Cylinder(ri, height + 2))

def case_shape():
    shell = ring(18.5, 16.8, BODY_BOTTOM, BODY_TOP-BODY_BOTTOM)
    for sx in (-1, 1):
        for sy in (-1, 1):
            pts = [(sx*9.0, sy*13.0), (sx*14.0, sy*12.0),
                   (sx*12.0, sy*20.5), (sx*9.0, sy*22.0)]
            face = bd.Polygon(*pts, align=None)
            lug = bd.extrude(face, amount=3.0, dir=(0,0,1))
            shell = shell.fuse(bd.Pos(0,0,2.1) * lug)
    shell.label = 'Case_37mm_PROPORTION_STUDY'
    return shell

def dial_shape():
    dial = bd.Pos(0,0,4.55) * bd.Cylinder(16, 1.5)
    dial.label = 'Dial_blank_32mm_NOT_MOVEMENT_FITTED'
    return dial

def back_shape():
    back = bd.Pos(0,0,0.75) * bd.Cylinder(18.3, 1.5)
    back.label = 'Caseback_blank_NO_RETENTION_YET'
    return back
