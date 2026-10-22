"""Reference-led sculptural development. Blender 5.2, millimeters.
NOT A MANUFACTURING RELEASE: fine ribs, crystal fit, movement mount pending.
Original proportions: 37 OD, 18 strap gap, 44 lug-to-lug.
"""
import bpy, bmesh, math, json
from pathlib import Path
from mathutils import Vector, Quaternion
ROOT=Path(__file__).resolve().parents[1]
N=256
CASE_OD=37.0
RIB_COUNT=60
MINUTE_RIB_WIDTH=.62
HOUR_RIB_WIDTH=1.12
RIB_VERTICAL_THICKNESS=1.05
DIAL_OUTER_RADIUS=16.2
CENTER_RADIUS=9.3
scene=bpy.data.scenes.new('RADIAL 37 | V2 sculpted arches')
bpy.context.window.scene=scene
scene.unit_settings.system='METRIC';scene.unit_settings.scale_length=.001
scene.unit_settings.length_unit='MILLIMETERS'

def material(name,rgb,metal=0,rough=.3):
    m=bpy.data.materials.new(name);m.use_nodes=True;m.diffuse_color=(*rgb,1)
    p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=(*rgb,1)
    p.inputs['Metallic'].default_value=metal;p.inputs['Roughness'].default_value=rough
    return m
metal=material('V2 | brushed titanium',(.48,.51,.53),1,.25)
dialmetal=material('V2 | satin dial arches',(.40,.43,.45),1,.33)
black=material('V2 | dark screw heads',(.032,.038,.042),.85,.25)
red=material('V2 | lacquer red',(.49,.015,.008),.25,.24)
polished=material('V2 | polished hands',(.7,.74,.77),1,.17)
leather=material('V2 | oxblood leather',(.055,.009,.006),0,.53)
cream=material('V2 | stitch',(.64,.50,.28),0,.7)
ground=material('V2 | charcoal studio',(.014,.019,.023),0,.65)

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

# Sculpted waist and small upper facet: shell remains 37 mm at widest point.
case=lathe('V2 CASE | sculpted 37mm',[(18.05,1.5),(18.25,2.0),(18.5,3.2),(18.5,4.7),
    (18.35,5.7),(18.25,6.4),(18.2,6.75),(16.65,6.75),(16.65,5.45),
    (16.45,5.45),(16.45,1.5)])
# Lofts follow the wrist: lower/tapered at the tips, broader at their roots.
for sx in (-1,1):
    for sy in (-1,1):
        stations=[(12.2,9.0,14.2,5.0,2.2),(14.8,9.0,13.9,4.9,2.1),
                  (17.2,9.0,12.9,4.3,1.75),(19.6,9.0,11.8,3.55,1.35),
                  (22.0,9.0,10.65,2.85,.85)]
        vs=[]
        for y,xi,xo,zt,zb in stations:
            vs += [(sx*xi,sy*y,zb),(sx*xo,sy*y,zb),
                   (sx*xo,sy*y,zt-.3),(sx*xi,sy*y,zt)]
        fs=[(3,2,1,0)]
        for j in range(len(stations)-1):
            for i in range(4):q=(i+1)%4;fs.append((j*4+i,j*4+q,(j+1)*4+q,(j+1)*4+i))
        fs.append(tuple(range((len(stations)-1)*4,len(stations)*4)))
        boolean(case,mesh('Curved lug tool',vs,fs))
boolean(case,cyl('Clear cavity',16.45,12,3), 'DIFFERENCE')
# Provisional drilled bores; final positions depend on real spring bars/crown tube.
for y in (-19.8,19.8):
    bore=cyl('Spring bar drilling',.5,31,2.55,y=y);bore.rotation_euler.y=math.pi/2
    boolean(case,bore,'DIFFERENCE')
stem=cyl('Crown tube drilling',.75,7,3.25,x=17.7);stem.rotation_euler.y=math.pi/2
boolean(case,stem,'DIFFERENCE')
bevel(case,.12)
for f in case.data.polygons:
    if abs(f.normal.z)<.92:f.use_smooth=True

# The dial is real open geometry: sixty arched webs between a center and rim.
dial=ring('V2 DIAL | real 60 arched webs',CENTER_RADIUS,.65,4.0,5.5,dialmetal)
rim=ring('Dial outer carrier',DIAL_OUTER_RADIUS,15.55,4.5,5.8,dialmetal)
# Combine the two shells, then bridge them with positive-volume arch meshes.
bpy.ops.object.select_all(action='DESELECT');dial.select_set(True);rim.select_set(True)
bpy.context.view_layer.objects.active=dial;bpy.ops.object.join()
def radial_z(t,depth=2.60):
    # Deep valley with smooth tangent reversal, both ends blend into raised rims.
    return 5.42-depth*math.sin(math.pi*t)**.85+.26*t
for i in range(RIB_COUNT):
    major=(i%5==0);angle=math.pi/2-i*2*math.pi/RIB_COUNT
    vs=[];steps=34
    for j in range(steps+1):
        t=j/steps;r=9.12+(15.92-9.12)*t
        z=radial_z(t,1.15 if major else 2.60)
        width=(HOUR_RIB_WIDTH if major else MINUTE_RIB_WIDTH)
        if major:width*=1+.30*math.sin(math.pi*t)
        # Arc-shaped ribs dip into the annulus, allowing light through each slot.
        da=width/(2*r)
        for a,h in [(angle-da,z-RIB_VERTICAL_THICKNESS),(angle+da,z-RIB_VERTICAL_THICKNESS),
                    (angle+da,z),(angle-da,z)]:
            vs.append((r*math.cos(a),r*math.sin(a),h))
    fs=[(3,2,1,0)]
    for j in range(steps):
        for k in range(4):q=(k+1)%4;fs.append((4*j+k,4*j+q,4*(j+1)+q,4*(j+1)+k))
    fs.append(tuple(range(4*steps,4*steps+4)))
    boolean(dial,mesh('Arch %02d'%i,vs,fs,dialmetal))
# Tiny easing preserves the narrow ribs; not a claim of print acceptance.
bevel(dial,.035,2)
for f in dial.data.polygons:
    if abs(f.normal.z)<.94:f.use_smooth=True

# Subtle brushed texture, no radial-pattern shader: ribs survive STL export.
p=dialmetal.node_tree.nodes.get('Principled BSDF');nt=dialmetal.node_tree
tex=nt.nodes.new('ShaderNodeTexNoise');tex.inputs['Scale'].default_value=210
bump=nt.nodes.new('ShaderNodeBump');bump.inputs['Strength'].default_value=.13;bump.inputs['Distance'].default_value=.018
nt.links.new(tex.outputs['Fac'],bump.inputs['Height']);nt.links.new(bump.outputs['Normal'],p.inputs['Normal'])

# Removable back development; retention/gasket features are deliberately provisional.
back=cyl('V2 CASEBACK | stepped development',18.1,1.8,.6);bevel(back,.2)
lip=ring('Back locating lip',16.25,14.75,1.35,2.0)
boolean(back,lip)
for a in (45,135,225,315):
    t=math.radians(a);x,y=15.8*math.cos(t),15.8*math.sin(t)
    boolean(back,cyl('Back screw clearance',.9,4,1,x=x,y=y),'DIFFERENCE')
    boolean(back,cyl('Back screw counterbore',1.45,.38,-.15,x=x,y=y),'DIFFERENCE')
    sc=cyl('Back screw | visual only',1.22,.3,-.08,black,x,y)
    bevel(sc,.07)
back['status']='retention bosses and seals not finalized; do not order'

# Two slender tapered hands with lacquered rectangular tips, set to 10:10.
def hand(name,length,width,angle,z):
    p=[(-width*.28,-1.2),(-width*.55,.7),(-width*.43,length-1.1),
       (0,length), (width*.43,length-1.1),(width*.55,.7),(width*.28,-1.2)]
    vs=[(x,y,h) for h in (z,z+.12) for x,y in p];m=len(p)
    fs=[tuple(reversed(range(m))),tuple(range(m,m*2))]
    fs += [(i,(i+1)%m,(i+1)%m+m,i+m) for i in range(m)]
    o=mesh(name,vs,fs,polished);o.rotation_euler.z=-angle;bevel(o,.04,2)
    tipvs=[(-width*.38,length-1.5,z+.12),(width*.38,length-1.5,z+.12),
           (width*.30,length-.25,z+.12),(-width*.30,length-.25,z+.12)]
    tip=mesh(name+' | red enamel',tipvs,[(0,1,2,3)],red);tip.rotation_euler.z=-angle
hand('V2 hour hand | reference',9.5,.75,math.radians(-55),5.82)
hand('V2 minute hand | reference',13.8,.53,math.radians(60),6.05)
cyl('V2 hand cap',.72,.32,6.0,polished);cyl('V2 hand pin',.22,.33,6.03,black)

# A fluted crown with real geometry rather than a plain cylinder.
vs=[];fs=[];nc=96
for x in (18.2,18.45,20.35,20.65):
    for i in range(nc):
        t=i*2*math.pi/nc;r=(1.82 if x in (18.2,20.65) else (2.04 if i%4<2 else 1.92))
        vs.append((x,r*math.cos(t),3.25+r*math.sin(t)))
fs.append(tuple(reversed(range(nc))))
for j in range(3):
    for i in range(nc):q=(i+1)%nc;fs.append((j*nc+i,j*nc+q,(j+1)*nc+q,(j+1)*nc+i))
fs.append(tuple(range(3*nc,4*nc)))
crown=mesh('V2 fluted crown | reference',vs,fs)

# 33 mm low-domed single sapphire envelope. Flat inner face clears hands.
glass=material('V2 | domed sapphire reference',(.98,.99,1),0,.035)
gp=glass.node_tree.nodes.get('Principled BSDF');gp.inputs['Transmission Weight'].default_value=1;gp.inputs['IOR'].default_value=1.76
vs=[(0,0,9.05)];fs=[];nr=32;nc=256
for j in range(1,nr+1):
    r=16.5*j/nr;z=7.85+1.2*(1-(r/16.5)**2)
    vs += [(r*math.cos(i*2*math.pi/nc),r*math.sin(i*2*math.pi/nc),z) for i in range(nc)]
for i in range(nc):fs.append((0,i+1,(i+1)%nc+1))
for j in range(nr-1):
    a=1+j*nc;b=a+nc
    for i in range(nc):q=(i+1)%nc;fs.append((a+i,b+i,b+q,a+q))
start=len(vs)
vs += [(16.5*math.cos(i*2*math.pi/nc),16.5*math.sin(i*2*math.pi/nc),6.55) for i in range(nc)]
for i in range(nc):q=(i+1)%nc;fs.append((1+(nr-1)*nc+i,start+i,start+q,1+(nr-1)*nc+q))
fs.append(tuple(reversed(range(start,start+nc))))
crystal=mesh('V2 crystal | 33mm envelope, not supplier geometry',vs,fs,glass)
crystal.hide_render=True # Geometry-review hero shows the uncovered dial.
crystal.hide_set(True) # Unhide this named object to inspect the optical envelope.
for f in crystal.data.polygons:f.use_smooth=True

def strap(sy):
    stations=[(19.8,9,2.2),(23,9,1.75),(30,8.8,.3),(43,8.2,-1),(52,8,-1.5)]
    vs=[]
    for y,w,z in stations:vs += [(-w,sy*y,z-1.4),(w,sy*y,z-1.4),(w,sy*y,z),(-w,sy*y,z)]
    fs=[(3,2,1,0)]
    for j in range(len(stations)-1):
        for i in range(4):q=(i+1)%4;fs.append((j*4+i,j*4+q,(j+1)*4+q,(j+1)*4+i))
    fs.append(tuple(range(16,20)))
    st=mesh('V2 oxblood strap | visual',vs,fs,leather);bevel(st,.35,4)
    for sx in (-1,1):
        for j in range(4):
            bpy.ops.mesh.primitive_uv_sphere_add(segments=12,ring_count=6,radius=1,location=(sx*(6.3+j*.45),sy*24,1.6))
            o=bpy.context.object;o.name='V2 saddle stitch';o.scale=(.24,.48,.12);o.data.materials.append(cream)
strap(1);strap(-1)

def aim(o,p):o.rotation_euler=(Vector(p)-o.location).to_track_quat('-Z','Y').to_euler()
bpy.ops.mesh.primitive_plane_add(size=300,location=(0,0,-3.5));bpy.context.object.data.materials.append(ground)
for loc,power,size in [((-45,-10,75),90000,50),((45,35,55),55000,35),((0,50,25),30000,24)]:
    bpy.ops.object.light_add(type='AREA',location=loc);o=bpy.context.object;o.data.energy=power;o.data.shape='DISK';o.data.size=size;aim(o,(0,0,3))
bpy.ops.object.camera_add(location=(28,-42,90));cam=bpy.context.object;aim(cam,(0,0,3));cam.data.type='ORTHO';cam.data.ortho_scale=56;scene.camera=cam
scene.world=bpy.data.worlds.new('V2 studio world');scene.world.use_nodes=True
scene.world.node_tree.nodes['Background'].inputs[0].default_value=(.15,.18,.21,1)
scene.render.engine='CYCLES';scene.cycles.samples=48;scene.cycles.use_denoising=True
scene.cycles.transmission_bounces=8;scene.cycles.transparent_max_bounces=8
scene.render.resolution_x=1100;scene.render.resolution_y=1300;scene.render.resolution_percentage=100
scene.view_settings.view_transform='AgX'
scene['stage']='PHASE 2, sculptural geometry development. NOT FOR METAL ORDER'
scene['source']='Carter Hurd Prototype B photographs; 37mm adaptation, inferred geometry'
scene['material_flags']='0.62mm minute webs, 1.05mm vertical thickness below JLC general 1.5mm wall guidance'

report={'units':'mm','stage':'V2 development, not for manufacture','parts':[],
        'nominal_rib_width_mm':MINUTE_RIB_WIDTH,'web_vertical_thickness_mm':RIB_VERTICAL_THICKNESS,
        'reference':'https://altapowderdog.wixsite.com/my-site/watches',
        'unverified':['movement fit and carrier','dial interface thickness','crystal gasket fit',
                      'back retention and sealing','fine-rib vendor acceptance','watertightness of assembled watch']}
for o,stem in [(case,'case_v2'),(dial,'arched_dial_v2'),(back,'caseback_v2')]:
    # Remove sub-micron boolean slivers before STL float precision triangulation.
    clean=bmesh.new();clean.from_mesh(o.data)
    bmesh.ops.remove_doubles(clean,verts=list(clean.verts),dist=.0001)
    bmesh.ops.dissolve_degenerate(clean,edges=list(clean.edges),dist=.000001)
    bmesh.ops.triangulate(clean,faces=list(clean.faces))
    bmesh.ops.recalc_face_normals(clean,faces=list(clean.faces))
    clean.to_mesh(o.data);clean.free();o.data.update()
    bpy.context.view_layer.update()
    bm=bmesh.new();bm.from_mesh(o.data)
    bad=sum(not e.is_manifold for e in bm.edges);vol=bm.calc_volume(signed=False);bm.free()
    report['parts'].append({'name':stem,'dimensions_mm':list(o.dimensions),'nonmanifold_edges':bad,'volume_mm3':vol})
    bpy.ops.object.select_all(action='DESELECT');o.select_set(True);bpy.context.view_layer.objects.active=o
    bpy.ops.wm.stl_export(filepath=str(ROOT/'STL'/f'{stem}.stl'),export_selected_objects=True,global_scale=1,use_scene_unit=False)
(ROOT/'geometry-checks.json').write_text(json.dumps(report,indent=2))
bpy.ops.object.select_all(action='DESELECT');dial.select_set(True);bpy.context.view_layer.objects.active=dial
for area in bpy.context.screen.areas:
    if area.type=='VIEW_3D':
        sp=area.spaces.active;sp.region_3d.view_distance=58;sp.region_3d.view_location=(0,0,3)
        sp.region_3d.view_rotation=cam.rotation_euler.to_quaternion();sp.shading.type='MATERIAL'
scene.render.filepath=str(ROOT/'radial37_v2_hero.png')
bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'radial37_v2.blend'))
print('V2_COMPLETE',json.dumps(report))
