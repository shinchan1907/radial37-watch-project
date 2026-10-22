"""Radial37 V3-derived titanium bayonet candidate 02. Millimetres.

Print stock and finished references are deliberately different artifacts.
Requires supplier precision finishing and component/physical validation.
"""
from pathlib import Path
import math,json,sys
from cadgen import build123d as bd,step,stl

ROOT=Path(__file__).resolve().parents[1]
PHASE=15.0
TURN=90.0
TAB_HALF_ANGLE=5.5
SHIFT=1.4

def kernel():
    global cq
    import cadquery as cq

def cylinder(r,z0,z1,x=0,y=0):
    return cq.Solid.makeCylinder(r,z1-z0,cq.Vector(x,y,z0))
def ring(ro,ri,z0,z1):return cylinder(ro,z0,z1).cut(cylinder(ri,z0-1,z1+1))
def sector(ri,ro,a0,a1,z0,z1):
    # Exact circular arc edges rather than polygonal track approximations.
    def point(r,a):return (r*math.cos(math.radians(a)),r*math.sin(math.radians(a)))
    am=(a0+a1)/2
    w=cq.Workplane('XY',origin=(0,0,z0)).moveTo(*point(ro,a0)).threePointArc(point(ro,am),point(ro,a1)).lineTo(*point(ri,a1)).threePointArc(point(ri,am),point(ri,a0)).close()
    return w.extrude(z1-z0).val()
def radial_shaft(r,x0,x1,z=5.35):return cq.Solid.makeCylinder(r,x1-x0,cq.Vector(x0,0,z),cq.Vector(1,0,0))
def revolved(profile):
    return cq.Workplane('XZ').polyline(profile).close().revolve(360,(0,0),(0,1)).val()
def lug(sx,sy,stock=False):
    allowance=.4 if stock else 0
    stations=[(11.8,11.4,6.8,3.8,4.3),(14.4,11.6,6.2,3.8,4.25),(17.0,11.5,5.2,3.5,3.9),(19.5,10.9,3.8,3.0,3.4),(22.0,10.5,3.0,2.8,3.1)]
    wires=[]
    for y,cx,width,height,cz in stations:
        cx+=.1  # 18.2 mm finished clearance for a nominal 18 mm strap.
        plane=cq.Plane(origin=(sx*cx,sy*(y+allowance*(y-16.9)/5.1),cz),xDir=(1,0,0),normal=(0,sy,0))
        rect=cq.Workplane(plane).rect(width+2*allowance,height+2*allowance).val()
        face=cq.Face.makeFromWires(rect)
        wires.append(face.fillet2D(.55+allowance,face.Vertices()).outerWire())
    shape=cq.Solid.makeLoft(wires,ruled=False)
    # Rounded tip cap; explicitly fail if a requested fillet cannot build.
    end_edges=[e for e in shape.Edges() if abs(e.Center().y)>21.7]
    if end_edges:shape=shape.fillet(.30,end_edges)
    return shape

def case_shape(stock=False):
    kernel()
    off=.4 if stock else 0
    profile=[(18.35+off,1.6-off),(18.5+off,2.1),(18.5+off,6.8),(18.38+off,7.35),(18.15+off,7.7+off),(14.8 if stock else 15.35,7.7+off),(14.8 if stock else 15.35,1.6-off)]
    body=revolved(profile)
    for sx in (-1,1):
        for sy in (-1,1):body=body.fuse(lug(sx,sy,stock))
    body=body.clean()
    if stock:return body.cut(cylinder(14.8,0,9)).clean()
    body=body.cut(cylinder(16.2,-1,5.3))
    body=body.cut(cylinder(15.9,5.3,6.4))
    body=body.cut(cylinder(16.8,6.8,8.5))
    # Three quarter-turn tracks with downward terminal pockets.
    for i in range(3):
        a=PHASE+i*120
        body=body.cut(sector(16.18,16.85,a-6.5,a+6.5,0,4.0))
        body=body.cut(sector(16.18,16.85,a-6.5,a+95.5,3.0,4.0))
        body=body.cut(sector(16.18,16.85,a+83.8,a+95.5,2.9,4.0))
    body=body.cut(ring(18.0,16.6,1.59,2.33))
    body=body.cut(radial_shaft(.90,15.5,20.0))
    body=body.cut(radial_shaft(.65,7.2,18.1))
    # Recess keyed to the polymer carrier; final carrier remains an interface proposal.
    body=body.cut(cq.Solid.makeBox(1.8,2.2,1.8,cq.Vector(-.9,14.8,3.3)))
    for y in (-20.0,20.0):
        body=body.cut(cq.Solid.makeCylinder(.50,31,cq.Vector(-15.5,y,3.25),cq.Vector(1,0,0)))
    return body.clean()

def back_shape(stock=False):
    kernel()
    if stock:
        body=cylinder(18.7,-.4,1.9)
        body=body.fuse(cylinder(12.4,1.5,2.7))
        body=body.fuse(ring(17.1,14.1,1.5,4.4))
        return body.clean()
    body=revolved([(0,0),(17.9,0),(18.3,.35),(18.3,1.5),(0,1.5)])
    body=body.fuse(cylinder(12.0,1.3,1.7))
    body=body.fuse(ring(16.0,14.8,1.3,3.60))
    for i in range(3):
        a=PHASE+i*120
        body=body.fuse(sector(15.8,16.65,a-TAB_HALF_ANGLE,a+TAB_HALF_ANGLE,2.9,3.7))
    for x in (-10,10):body=body.cut(cylinder(1.0,-.1,.60,x=x))
    return body.clean()

def dial_shape(stock=False):
    kernel()
    if stock:
        # A robust flat machining preform. The wave faces are finish-machined.
        # 0.4 mm lateral web allowance; generous axial allowance avoids thin
        # local print features and nearly tangent Boolean/tessellation slivers.
        preform=cylinder(10.0,3.5,7.2).fuse(ring(16.1,13.7,3.5,7.2))
        for i in range(16):
            a=math.pi/2-i*2*math.pi/16
            wires=[]
            for r in (9.3,14.15):
                h=1.4/r
                pts=[cq.Vector(r*math.cos(a-h),r*math.sin(a-h),3.5),cq.Vector(r*math.cos(a+h),r*math.sin(a+h),3.5),cq.Vector(r*math.cos(a+h),r*math.sin(a+h),7.2),cq.Vector(r*math.cos(a-h),r*math.sin(a-h),7.2)]
                wires.append(cq.Wire.makePolygon(pts,close=True))
            preform=preform.fuse(cq.Solid.makeLoft(wires,ruled=True))
        return preform.clean()
    # Coarser wave architecture makes room for 2 mm webs and cleanable slots.
    body=cylinder(10.0 if stock else 9.6,4.0 if stock else 4.4,7.2 if stock else 6.6)
    if stock:body=body.fuse(ring(16.1,13.7,4.0,6.8))
    else:body=body.fuse(revolved([(15.55,4.4),(15.7,4.55),(15.7,6.25),(15.55,6.4),(13.7,6.4),(13.7,4.4)]))
    for i in range(16):
        a=math.pi/2-i*2*math.pi/16
        crown=i==4; wires=[]
        for j in range(33):
            t=j/32;r=9.3+4.85*t
            u=max(0,min(1,(r-10.0)/3.4));smooth=u*u*(3-2*u)
            base=6.6-(.1 if crown else .2)*smooth
            wave=max(0,min(1,(r-10.0)/3.3))
            dip=0 if crown else (.25 if i%4==0 else .45)*math.sin(math.pi*wave)**2
            top=base-dip+(.4 if stock else 0);bottom=(4.0 if stock else 4.4)-dip
            half=(1.4 if stock else 1.0)/r
            pts=[cq.Vector(r*math.cos(a-half),r*math.sin(a-half),bottom),cq.Vector(r*math.cos(a+half),r*math.sin(a+half),bottom),cq.Vector(r*math.cos(a+half),r*math.sin(a+half),top),cq.Vector(r*math.cos(a-half),r*math.sin(a-half),top)]
            wires.append(cq.Wire.makePolygon(pts,close=True))
        body=body.fuse(cq.Solid.makeLoft(wires,ruled=True))
    body=body.fuse(sector(13.65,16.1 if stock else 15.7,-5,5,6.2,6.9 if stock else 6.5)).clean()
    if stock:return body
    body=body.cut(cylinder(9.62,0,6.2))
    for x,y in [(-7.9,-3),(8.234,-1.9)]:body=body.fuse(cylinder(.35,4.7,6.3,x,y))
    body=body.cut(cylinder(.6,0,8))
    body=body.cut(radial_shaft(.65,7.2,17.0))
    body=body.cut(cq.Solid.makeBox(2.4,7.0,5.0,cq.Vector(-1.2,9.0,0)))
    # Post-machine a 0.85mm outer rail, captured from above by the bezel.
    body=body.cut(ring(20.0,14.3,0,5.55))
    body=body.cut(ring(20.0,15.35,6.4,8.0))
    # OCCT same-domain cleanup after this cut invalidates otherwise valid
    # small channel faces. Preserve the valid, unmerged B-rep.
    return body

def bd_solid(shape,label):
    solids=shape.Solids()
    if len(solids)!=1 or not shape.isValid():raise RuntimeError(label+' invalid or disconnected')
    obj=bd.Solid(solids[0].wrapped);obj.label=label;return obj

@step(out='../STEP/case_PRINT_STOCK.step')
@stl(out='../build/raw_stl/case_PRINT_STOCK.stl')
def case_print_stock():return bd_solid(case_shape(True),'case_PRINT_STOCK')
@step(out='../STEP/back_PRINT_STOCK.step')
@stl(out='../build/raw_stl/back_PRINT_STOCK.stl')
def back_print_stock():return bd_solid(back_shape(True),'back_PRINT_STOCK')
@step(out='../STEP/dial_PRINT_STOCK.step')
@stl(out='../build/raw_stl/dial_PRINT_STOCK.stl')
def dial_print_stock():return bd_solid(dial_shape(True),'dial_PRINT_STOCK')
@step(out='../STEP/case_FINISHED_REFERENCE.step')
@stl(out='../build/raw_stl/case_FINISHED_REFERENCE.stl')
def case_finished():return bd_solid(case_shape(False),'case_FINISHED_REFERENCE')
@step(out='../STEP/back_FINISHED_REFERENCE.step')
@stl(out='../build/raw_stl/back_FINISHED_REFERENCE.stl')
def back_finished():return bd_solid(back_shape(False),'back_FINISHED_REFERENCE')
@step(out='../STEP/dial_FINISHED_REFERENCE.step')
@stl(out='../build/raw_stl/dial_FINISHED_REFERENCE.stl')
def dial_finished():return bd_solid(dial_shape(False),'dial_FINISHED_REFERENCE')

@step(out='../STEP/assembly_FINISHED_REFERENCE.step')
def assembly_finished():
    c=case_finished();b=back_finished().rotate(bd.Axis.Z,90);d=dial_finished()
    return bd.Compound(children=[c,b,d],label='Radial37 finished-target candidate')

def mechanical_checks():
    c=case_shape(False);b=back_shape(False);d=dial_shape(False)
    poses=[]
    for angle in range(0,91,5):
        posed=b.rotate((0,0,0),(0,0,1),angle).translate((0,0,.1))
        poses.append({'angle_deg':angle,'axial_offset_mm':.1,'case_overlap_mm3':c.intersect(posed).Volume()})
    for dz in [-3,-2,-1,0,.1]:
        poses.append({'angle_deg':0,'axial_offset_mm':dz,'case_overlap_mm3':c.intersect(b.translate((0,0,dz))).Volume()})
    for dz in [0,.025,.05,.075,.1]:
        posed=b.rotate((0,0,0),(0,0,1),90).translate((0,0,dz))
        poses.append({'angle_deg':90,'axial_offset_mm':dz,'case_overlap_mm3':c.intersect(posed).Volume()})
    reverse=b.rotate((0,0,0),(0,0,1),88)
    closed=b.rotate((0,0,0),(0,0,1),90)
    report={'status':'CANDIDATE; NOT RELEASED FOR ORDER','units':'mm','quarter_turn_deg':90,'unlock_push_mm':.10,'poses':poses,'all_sampled_motion_poses_clear':all(abs(p['case_overlap_mm3'])<1e-5 for p in poses),'reverse_without_push_overlap_mm3':c.intersect(reverse).Volume(),'dial_vs_case_mm3':d.intersect(c).Volume(),'dial_vs_closed_back_mm3':d.intersect(closed).Volume(),'finished_solids':{'case':{'valid':c.isValid(),'solids':len(c.Solids()),'volume_mm3':c.Volume()},'back':{'valid':b.isValid(),'solids':len(b.Solids()),'volume_mm3':b.Volume()},'dial':{'valid':d.isValid(),'solids':len(d.Solids()),'volume_mm3':d.Volume()}},'holds':['Supplier capability and quote for all finishing','Actual component drawings and physical fit','Gasket force, wear and accidental unlock testing','Complete worst-case assembly tolerance and structural review','Build orientation, supports and finish approval']}
    (ROOT/'validation').mkdir(exist_ok=True);(ROOT/'validation'/'mechanical_checks.json').write_text(json.dumps(report,indent=2))
    print(json.dumps(report,indent=2))

if __name__=='__main__':
    if '--check' in sys.argv:mechanical_checks()
    elif len(sys.argv)>1:globals()[sys.argv[1]]()
    else:
        for f in [case_print_stock,back_print_stock,dial_print_stock,case_finished,back_finished,dial_finished,assembly_finished]:f()
        from conform_meshes import conform_all
        conform_all(ROOT)
