import bpy,bmesh,math,json
from pathlib import Path
from mathutils import Vector
from parameters import *
ROOT=Path(__file__).resolve().parents[1]
N=192
scene=bpy.data.scenes.new('RADIAL 37 | V3 slim screw-down engineering')
bpy.context.window.scene=scene
scene.unit_settings.system='METRIC';scene.unit_settings.scale_length=.001;scene.unit_settings.length_unit='MILLIMETERS'

def material(name,rgb,metal=0,rough=.3):
    m=bpy.data.materials.new(name);m.use_nodes=True;m.diffuse_color=(*rgb,1)
    p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=(*rgb,1)
    p.inputs['Metallic'].default_value=metal;p.inputs['Roughness'].default_value=rough
    return m
metal=material('V3 | brushed titanium',(.48,.51,.53),1,.25)
dialmetal=material('V3 | satin dial arches',(.40,.43,.45),1,.33)
black=material('V3 | dark screw heads',(.032,.038,.042),.85,.25)
red=material('V3 | lacquer red',(.49,.015,.008),.25,.24)
polished=material('V3 | polished hands',(.7,.74,.77),1,.17)
leather=material('V3 | oxblood leather',(.055,.009,.006),0,.53)
cream=material('V3 | stitch',(.64,.50,.28),0,.7)
ground=material('V3 | charcoal studio',(.014,.019,.023),0,.65)

def mesh(name,vs,fs,mat=metal):
    me=bpy.data.meshes.new(name);me.from_pydata(vs,[],fs);me.update()
    bm=bmesh.new();bm.from_mesh(me);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(me);bm.free()
    o=bpy.data.objects.new(name,me);scene.collection.objects.link(o)
    if mat:o.data.materials.append(mat)
    return o
def cyl(name,r,h,z,mat=metal,x=0,y=0):
    bpy.ops.mesh.primitive_cylinder_add(vertices=96,radius=r,depth=h,location=(x,y,z))
    o=bpy.context.object;o.name=name
    if mat:o.data.materials.append(mat)
    return o
def boolean(a,b,operation='UNION'):
    bpy.context.view_layer.objects.active=a
    mod=a.modifiers.new(operation,'BOOLEAN');mod.solver='EXACT';mod.operation=operation;mod.object=b
    bpy.ops.object.modifier_apply(modifier=mod.name);bpy.data.objects.remove(b,do_unlink=True)
def bevel(o,w=.12,segments=3):
    bpy.context.view_layer.objects.active=o
    mod=o.modifiers.new('Finished edge','BEVEL');mod.width=w;mod.segments=segments
    bpy.ops.object.modifier_apply(modifier=mod.name)
def lathe(name,profile,mat=metal,n=N):
    vs=[(r*math.cos(i*2*math.pi/n),r*math.sin(i*2*math.pi/n),z) for r,z in profile for i in range(n)]
    fs=[]
    for j in range(len(profile)):
        k=(j+1)%len(profile)
        for i in range(n):q=(i+1)%n;fs.append((j*n+i,j*n+q,k*n+q,k*n+i))
    return mesh(name,vs,fs,mat)
def ring(name,ro,ri,z0,z1,mat=metal):
    return lathe(name,[(ro,z0),(ro,z1),(ri,z1),(ri,z0)],mat)



def box(name,size,loc,mat=metal):
    bpy.ops.mesh.primitive_cube_add(size=1,location=loc)
    o=bpy.context.object;o.name=name;o.dimensions=size
    bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
    if mat:o.data.materials.append(mat)
    return o
def shaft(name,radius,x0,x1,z=STEM_Z,mat=metal):
    o=cyl(name,radius,x1-x0,z,mat,x=(x0+x1)/2);o.rotation_euler.y=math.pi/2
    bpy.context.view_layer.update()
    return o
def cleanup(o):
    bm=bmesh.new();bm.from_mesh(o.data)
    bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=.0001)
    bmesh.ops.dissolve_degenerate(bm,edges=list(bm.edges),dist=.000001)
    bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(o.data);bm.free();o.data.update()
def finish(o):
    cleanup(o)
    bm=bmesh.new();bm.from_mesh(o.data);bmesh.ops.triangulate(bm,faces=list(bm.faces));bm.to_mesh(o.data);bm.free()
def thread_radius(z,t,extra=0,lead=False):
    # Explicit matched custom 60-degree-derived trapezoidal helix, not ISO fit certification.
    phase=((z-THREAD_START)/THREAD_PITCH-t/(2*math.pi))%1
    d=abs(phase-.5)*THREAD_PITCH
    crest=.0625
    h=max(0,min(THREAD_DEPTH,THREAD_DEPTH-(d-crest/2)*math.sqrt(3)))
    if lead:h*=min(1,max(0,(z-THREAD_START)/.10),max(0,(THREAD_END-z)/.10))
    return THREAD_ROOT_RADIUS+extra+h
def threaded(name,extra=0,inner=0,lead=False):
    lo,hi=THREAD_START,THREAD_END;nt=192;nz=88
    vs=[];fs=[]
    for j in range(nz+1):
        z=lo+(hi-lo)*j/nz
        for i in range(nt):
            t=2*math.pi*i/nt;r=thread_radius(z,t,extra,lead);vs.append((r*math.cos(t),r*math.sin(t),z))
    for j in range(nz):
        for i in range(nt):q=(i+1)%nt;fs.append((j*nt+i,j*nt+q,(j+1)*nt+q,(j+1)*nt+i))
    if inner:
        base=len(vs)
        for z in (lo,hi):vs += [(inner*math.cos(i*2*math.pi/nt),inner*math.sin(i*2*math.pi/nt),z) for i in range(nt)]
        for i in range(nt):
            q=(i+1)%nt
            fs += [(i,base+i,base+q,q),(nz*nt+i,nz*nt+q,base+nt+q,base+nt+i),(base+i,base+nt+i,base+nt+q,base+q)]
    else:
        b=len(vs);vs += [(0,0,lo),(0,0,hi)]
        for i in range(nt):q=(i+1)%nt;fs += [(b,q,i),(b+1,nz*nt+i,nz*nt+q)]
    return mesh(name,vs,fs)

profile=[(17.5,1.25),(17.9,1.35),(18.25,1.6),(18.45,2.05),(18.5,2.55),
         (18.5,3.45),(18.45,3.95),(18.3,4.4),(18.1,4.65),(18.05,4.85),
         (16.8,4.85),(16.8,3.85),(15.9,3.85),(15.9,3.4),(15.15,3.4),
         (15.15,2.8),(16.3,2.8),(16.3,1.25)]
case=lathe('V3 CASE | finished reference, 37mm',profile)
cleanup(case)
for sx in (-1,1):
    for sy in (-1,1):
        stations=[(12.2,9.,14.15,3.85,1.5),(14.8,9.,13.85,3.8,1.4),
                  (17.1,9.,12.9,3.4,1.1),(19.6,9.,11.85,2.9,.8),(22.,9.,10.9,2.5,.65)]
        vs=[]
        for y,xi,xo,zt,zb in stations:vs += [(sx*xi,sy*y,zb),(sx*xo,sy*y,zb),(sx*xo,sy*y,zt),(sx*xi,sy*y,zt)]
        fs=[(3,2,1,0)]
        for j in range(4):
            for i in range(4):q=(i+1)%4;fs.append((j*4+i,j*4+q,(j+1)*4+q,(j+1)*4+i))
        fs.append(tuple(range(16,20)))
        lug=mesh('Rounded lug',vs,fs);bevel(lug,.30,5);boolean(case,lug)
# Restore cavity after integral lugs, preserving the dial's annular seat.
boolean(case,cyl('Lower cavity',16.3,1.55,2.0),'DIFFERENCE')
boolean(case,cyl('Dial location pocket',15.9,.55,3.675),'DIFFERENCE')
boolean(case,cyl('Crystal/gasket pocket',16.8,3.0,5.35),'DIFFERENCE')
bevel(case,.12,4)
# Preserve a smooth print stock before introducing fine machined interfaces.
stock_case=case.copy();stock_case.data=case.data.copy();scene.collection.objects.link(stock_case)
stock_case.name='V3 PRINT STOCK | case, machining required'
boolean(stock_case,cyl('Rear bore stock',15.9,1.6,2.0),'UNION')
boolean(stock_case,cyl('Rear pilot bore',15.45,2.3,1.8),'DIFFERENCE')
boolean(case,threaded('Female thread cutter',extra=THREAD_RADIAL_GAP),'DIFFERENCE')
boolean(case,ring('Face gasket groove',17.75,16.85,1.249,1.70),'DIFFERENCE')
boolean(case,shaft('Crown tube bore',.90,15.5,20.0),'DIFFERENCE')
boolean(case,shaft('Stem swept tunnel',STEM_PASSAGE_RADIUS,6.15,18.0),'DIFFERENCE')
boolean(case,box('Carrier key recess',(1.8,1.7,1.20),(0,15.6,3.0)),'DIFFERENCE')
for y in (-20.,20.):
    b=cyl('Spring-bar finish drilling',.5,29,1.65,y=y);b.rotation_euler.y=math.pi/2
    boolean(case,b,'DIFFERENCE')
for f in case.data.polygons:
    if abs(f.normal.z)<.92:f.use_smooth=True

back=cyl('V3 BACK | finished threaded, no screws',17.9,.90,.45)
boolean(back,ring('Back flange',17.9,14.6,.65,1.25))
bevel(back,.18,4)
boolean(back,ring('Male sleeve root',16.20,14.6,1.15,2.45))
boolean(back,threaded('Male thread',inner=14.6,lead=True))
for x in (-10.,10.):boolean(back,cyl('Blind wrench socket',.8,.27,.125,x=x),'DIFFERENCE')
stock_back=cyl('V3 PRINT STOCK | back, machining required',18.1,1.60,.4)
boolean(stock_back,ring('Thread turning stock',16.75,14.4,1.0,2.65))
bevel(stock_back,.12,3)

# Metal chapter ring, separate from the conventional 0.4mm brass center dial.
dial=ring('V3 ARCHES | fine-detail metal chapter',9.85,9.35,3.85,4.54,dialmetal)
rim=ring('Outer chapter ring',15.7,15.0,3.40,4.35,dialmetal)
bpy.ops.object.select_all(action='DESELECT');dial.select_set(True);rim.select_set(True);bpy.context.view_layer.objects.active=dial;bpy.ops.object.join()
for i in range(60):
    a=math.pi/2-i*2*math.pi/60;major=i%5==0;crown_bridge=i==15;steps=28;vs=[]
    for j in range(steps+1):
        t=j/steps;r=9.65+5.85*t
        z=4.52-(.65 if major else 1.80)*math.sin(math.pi*t)**.85-.10*t
        if crown_bridge or i==0:z=4.70
        width=1.75 if crown_bridge else (1.10 if major else RIB_WIDTH)
        d=width/(2*r)
        for ang,h in [(a-d,z-RIB_THICKNESS),(a+d,z-RIB_THICKNESS),(a+d,z),(a-d,z)]:vs.append((r*math.cos(ang),r*math.sin(ang),h))
    fs=[(3,2,1,0)]
    for j in range(steps):
        for k in range(4):q=(k+1)%4;fs.append((4*j+k,4*j+q,4*j+4+q,4*j+4+k))
    fs.append(tuple(range(4*steps,4*steps+4)))
    boolean(dial,mesh('Arched web',vs,fs,dialmetal))
boolean(dial,shaft('Stem channel under three oclock',STEM_PASSAGE_RADIUS,6.15,18.0),'DIFFERENCE')
bevel(dial,.025,2)

plate=ring('V3 CENTER DIAL | brass 0.40mm',9.25,.75,MOVEMENT_FACE,DIAL_TOP,dialmetal)
for x,y in FEET:boolean(plate,cyl('Dial foot, drawing coordinate',.35,1.30,MOVEMENT_FACE-.65,dialmetal,x,y))

def footprint(name,clearance,z0,z1,mat=black):
    o=cyl(name,8.90+clearance,z1-z0,(z0+z1)/2,mat)
    clip=box('Frame flats',(13.0+2*clearance,15.75+2*clearance,z1-z0+1),(-.1,0,(z0+z1)/2))
    boolean(o,clip,'INTERSECT');return o
movement=footprint('V3 5Y20 | conservative casing envelope',0,MOVEMENT_BOTTOM,MOVEMENT_FACE,black)
for x,y in FEET:boolean(movement,cyl('Dial-foot interface bore',.42,2.0,3.8,black,x,y),'DIFFERENCE')
carrier=cyl('V3 CARRIER | polymer fit prototype',14.4,.75,1.275,black)
boolean(carrier,cyl('Frame locating tower',10.1,1.25,2.275,black))
boolean(carrier,footprint('Frame pocket 0.15 clearance',.15,MOVEMENT_BOTTOM,4.4),'DIFFERENCE')
boolean(carrier,box('Anti rotation arm',(1.4,6.15,.60),(0,12.775,2.9),black))
boolean(carrier,shaft('Carrier stem clearance',STEM_PASSAGE_RADIUS,6.15,18.0),'DIFFERENCE')
stem=shaft('V3 STEM | physical .70 envelope',STEM_RADIUS,6.4,20.0,mat=polished)
sweep=shaft('CHECK | stem tolerance swept envelope',STEM_SWEEP_RADIUS,6.4,19.5,mat=red)
sweep.hide_render=True;sweep.hide_set(True)
hand_sweep=cyl('CHECK | rotating hands envelope',14.0,.43,5.255,red)
hand_sweep.hide_render=True;hand_sweep.hide_set(True)

# 33mm domed acrylic outer/inner envelope; inner profile remains a procurement hold.
profile=[]
for j in range(33):
    r=16.5*j/32;profile.append((r,6.35+1.80*(1-(r/16.5)**2)))
profile += [(16.5,3.85),(16.0,3.85),(16.0,5.35)]
for j in range(31,-1,-1):
    r=16*j/32;profile.append((r,5.35+1.8*(1-(r/16)**2)))
glass=material('V3 | acrylic dome envelope',(.99,.99,1),0,.05)
gp=glass.node_tree.nodes.get('Principled BSDF');gp.inputs['Transmission Weight'].default_value=1;gp.inputs['IOR'].default_value=1.49
crystal=lathe('V3 CRYSTAL | 33mm H4.30, provisional inner',profile,glass)
cleanup(crystal)
for f in crystal.data.polygons:f.use_smooth=True

# A compressed face O-ring and a crystal gasket, shown as separate purchased parts.
bpy.ops.mesh.primitive_torus_add(major_segments=192,minor_segments=24,major_radius=17.3,minor_radius=.3,location=(0,0,1.475))
gasket=bpy.context.object;gasket.name='V3 BACK GASKET | 34x0.6 envelope';gasket.scale=(1.3333333,1.3333333,.75)
# Preserve mean radius; radial ellipse is generated explicitly to conserve section area.
for v in gasket.data.vertices:
    p=v.co;t=math.atan2(p.y,p.x);r=math.hypot(p.x,p.y);dr=r-17.3
    p.x=(17.3+dr*4/3)*math.cos(t);p.y=(17.3+dr*4/3)*math.sin(t);p.z*=.75
gasket.scale=(1,1,1);gasket.data.materials.append(black)
crystal_gasket=ring('V3 CRYSTAL GASKET | provisional',16.8,16.5,3.85,4.80,black)
tube=shaft('V3 CROWN TUBE | provisional 1.8 OD',.9,16.3,19.1)
boolean(tube,shaft('Tube bore',.55,16.0,19.3),'DIFFERENCE')
crown=cyl('V3 CROWN | fluted reference',1.85,2.0,STEM_Z,metal,x=19.8);crown.rotation_euler.y=math.pi/2;bevel(crown,.15,4)
for i in range(24):
    a=i*2*math.pi/24
    c=shaft('Flute tool',.10,19.05,20.55,z=STEM_Z+1.81*math.sin(a));c.location.y=1.81*math.cos(a)
    boolean(crown,c,'DIFFERENCE')

# Appearance hands only: the exact purchased hand stack is still to be confirmed.
def hand(name,length,width,angle,z):
    pts=[(-width*.3,-.8),(-width*.5,.5),(-width*.35,length-.8),(0,length),(width*.35,length-.8),(width*.5,.5),(width*.3,-.8)]
    n=len(pts);vs=[(x,y,h) for h in (z,z+.12) for x,y in pts]
    fs=[tuple(reversed(range(n))),tuple(range(n,2*n))]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)]
    o=mesh(name,vs,fs,polished);o.rotation_euler.z=-angle;bevel(o,.03,2)
    pts=[(-width*.3,length-1.4,z+.121),(width*.3,length-1.4,z+.121),(width*.25,length-.25,z+.121),(-width*.25,length-.25,z+.121)]
    tip=mesh(name+' red tip',pts,[(0,1,2,3)],red);tip.rotation_euler.z=-angle
hand('V3 HOUR HAND | envelope',9.4,.7,math.radians(-55),5.04)
hand('V3 MINUTE HAND | envelope',13.8,.5,math.radians(60),5.24)
cyl('V3 HAND HUB',.65,.34,5.36,polished)

stock_case.hide_render=True;stock_case.hide_set(True);stock_back.hide_render=True;stock_back.hide_set(True)
for o in (movement,carrier,gasket):o.hide_render=True;o.hide_set(True)
crystal.hide_render=True;crystal.hide_set(True)

# Build a staged studio and keep all geometry in its own new scene.
def aim(o,p):o.rotation_euler=(Vector(p)-o.location).to_track_quat('-Z','Y').to_euler()
for loc,power,size in [((-35,-15,65),65000,45),((45,30,40),42000,35),((-5,45,20),28000,25)]:
    bpy.ops.object.light_add(type='AREA',location=loc);o=bpy.context.object;o.data.energy=power;o.data.shape='DISK';o.data.size=size;aim(o,(0,0,3))
bpy.ops.object.camera_add(location=(28,-45,75));cam=bpy.context.object;aim(cam,(0,0,3));cam.data.type='ORTHO';cam.data.ortho_scale=52;scene.camera=cam
scene.world=bpy.data.worlds.new('V3 studio');scene.world.use_nodes=True;scene.world.node_tree.nodes['Background'].inputs[0].default_value=(.14,.17,.20,1)
scene.render.engine='CYCLES';scene.cycles.samples=32;scene.cycles.use_denoising=True
scene.render.resolution_x=1100;scene.render.resolution_y=1250;scene.render.resolution_percentage=100
scene.view_settings.view_transform='AgX'
scene['status']='ENGINEERING DEVELOPMENT, NOT RELEASED FOR METAL ORDER'
scene['stack']='Metal 4.85mm; overall candidate dome 8.15mm. Crystal inner profile provisional.'
scene['threads']='Matched custom nominal 33x0.5 RH; finish-machine, not as-printed fit'

items=[(case,'case_FINISHED_reference'),(back,'back_FINISHED_reference'),(dial,'chapter_fine_VENDOR_REVIEW'),
       (plate,'center_dial_BRASS_0p4'),(carrier,'carrier_POLYMER_fit'),(stock_case,'case_PRINT_STOCK_HOLD'),(stock_back,'back_PRINT_STOCK_HOLD')]
report={'units':'mm','status':'NOT RELEASED FOR ORDER','parts':[],
        'stack':{'metal_height':4.85,'crystal_apex':8.15,'movement_bottom':MOVEMENT_BOTTOM,'movement_face':MOVEMENT_FACE,'dial_top':DIAL_TOP,'stem_axis':STEM_Z},
        'holds':['Crystal inner section and exact retaining gasket','Exact purchased crown/tube and hand stack','Vendor fine-web acceptance',
                 'Machinist thread tolerances, engagement strength and gauges','Pressure test and gasket material','Stock DfAM review']}
for o,stem_name in items:
    finish(o);bpy.context.view_layer.update()
    bm=bmesh.new();bm.from_mesh(o.data)
    report['parts'].append({'name':stem_name,'dimensions_mm':list(o.dimensions),'nonmanifold_edges':sum(not e.is_manifold for e in bm.edges),'volume_mm3':bm.calc_volume(signed=False)})
    bm.free();was=o.hide_get();o.hide_set(False)
    bpy.ops.object.select_all(action='DESELECT');o.select_set(True);bpy.context.view_layer.objects.active=o
    bpy.ops.wm.stl_export(filepath=str(ROOT/'STL'/f'{stem_name}.stl'),export_selected_objects=True,global_scale=1,use_scene_unit=False)
    o.hide_set(was)
(ROOT/'geometry-checks.json').write_text(json.dumps(report,indent=2))
bpy.ops.object.select_all(action='DESELECT');case.select_set(True);bpy.context.view_layer.objects.active=case
for a in bpy.context.screen.areas:
    if a.type=='VIEW_3D':a.spaces.active.region_3d.view_location=(0,0,3);a.spaces.active.region_3d.view_distance=55;a.spaces.active.region_3d.view_rotation=cam.rotation_euler.to_quaternion()
scene.render.filepath=str(ROOT/'v3_hero.png')
bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'radial37_v3.blend'))
print('V3_BUILD',json.dumps(report))



