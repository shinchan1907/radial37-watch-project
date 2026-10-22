"""37 mm quartz watch, phase-one proportions. Run in Blender Python.
The radial finish, hands, crown and crystal are visual references only.
No crystal seat, stem bore, spring-bar bores or caseback retention is released.
"""
import bpy, math, json
from pathlib import Path
from mathutils import Vector

ROOT = Path(__file__).resolve().parents[1]
scene = bpy.data.scenes.new('RADIAL 37 | Proportion study')
bpy.context.window.scene = scene
scene.unit_settings.system = 'METRIC'
scene.unit_settings.scale_length = 0.001
scene.unit_settings.length_unit = 'MILLIMETERS'

def mat(name, color, metal=0, rough=.3):
    m=bpy.data.materials.new(name); m.diffuse_color=(*color,1); m.use_nodes=True
    p=m.node_tree.nodes.get('Principled BSDF')
    p.inputs['Base Color'].default_value=(*color,1)
    p.inputs['Metallic'].default_value=metal; p.inputs['Roughness'].default_value=rough
    return m
steel=mat('Satin titanium appearance',(.43,.47,.50),1,.26)
dark=mat('Recessed graphite',(.055,.067,.073),.8,.36)
red=mat('Vermilion tips',(.64,.035,.018),.4,.22)
handmat=mat('Hands polished silver',(.75,.78,.8),.9,.19)
def assign(o,m): o.data.materials.append(m)
def bevel(o,w=.15):
    mod=o.modifiers.new('Soft edge','BEVEL'); mod.width=w; mod.segments=3
    bpy.context.view_layer.objects.active=o
    bpy.ops.object.modifier_apply(modifier=mod.name)
def cylinder(name,r,depth,z,material,x=0,y=0):
    bpy.ops.mesh.primitive_cylinder_add(vertices=192,radius=r,depth=depth,location=(x,y,z))
    o=bpy.context.object; o.name=name; assign(o,material); return o
def mesh(name,verts,faces,material):
    me=bpy.data.meshes.new(name); me.from_pydata(verts,[],faces); me.update()
    o=bpy.data.objects.new(name,me); scene.collection.objects.link(o); assign(o,material);return o
def ring(name,ro,ri,z0,z1):
    n=192; vs=[]
    for r,z in [(ro,z0),(ro,z1),(ri,z1),(ri,z0)]:
        vs += [(r*math.cos(2*math.pi*i/n),r*math.sin(2*math.pi*i/n),z) for i in range(n)]
    fs=[]
    for k in range(4):
        for i in range(n):
            j=(i+1)%n; q=(k+1)%4
            fs.append((k*n+i,k*n+j,q*n+j,q*n+i))
    return mesh(name,vs,fs,steel)
case=ring('CASE | 37 OD | 33.6 raw bore | STUDY',18.5,16.8,1.5,7.0)
for sx in (-1,1):
    for sy in (-1,1):
        p=[(sx*9,sy*13),(sx*14,sy*12),(sx*12,sy*20.5),(sx*9,sy*22)]
        if sx*sy<0:p.reverse()
        vs=[(x,y,z) for z in (2.1,5.1) for x,y in p]
        fs=[(3,2,1,0),(4,5,6,7)]+[(i,(i+1)%4,(i+1)%4+4,i+4) for i in range(4)]
        lug=mesh('Lug',vs,fs,steel)
        bpy.context.view_layer.objects.active=case
        mod=case.modifiers.new('Integral lug','BOOLEAN');mod.operation='UNION';mod.object=lug
        bpy.ops.object.modifier_apply(modifier=mod.name);bpy.data.objects.remove(lug,do_unlink=True)
raw_bore=cylinder('Raw bore cutter',16.8,12,4,steel)
bpy.context.view_layer.objects.active=case
mod=case.modifiers.new('Clear integral lugs from bore','BOOLEAN');mod.operation='DIFFERENCE';mod.object=raw_bore
bpy.ops.object.modifier_apply(modifier=mod.name);bpy.data.objects.remove(raw_bore,do_unlink=True)
bevel(case,.16)
back=cylinder('CASEBACK | 36.6 x 1.5 | blank',18.3,1.5,.75,steel);bevel(back,.18)
dial=cylinder('DIAL | 32 x 1.5 blank | fit unresolved',16,1.5,4.55,dark)
# Surface-only graphic: 60 light rays and twelve heavier hour rays.
dm=bpy.data.materials.new('Radial dial | visual shader only');dm.use_nodes=True
nt=dm.node_tree;nt.nodes.clear()
out=nt.nodes.new('ShaderNodeOutputMaterial');pr=nt.nodes.new('ShaderNodeBsdfPrincipled')
pr.inputs['Metallic'].default_value=.88;pr.inputs['Roughness'].default_value=.37
tex=nt.nodes.new('ShaderNodeTexCoord');sep=nt.nodes.new('ShaderNodeSeparateXYZ')
nt.links.new(tex.outputs['Object'],sep.inputs[0])
def mathnode(op,a=None,b=None):
    n=nt.nodes.new('ShaderNodeMath');n.operation=op
    for i,v in enumerate((a,b)):
        if v is not None:
            if isinstance(v,(float,int)):n.inputs[i].default_value=v
            else:nt.links.new(v,n.inputs[i])
    return n.outputs[0]
x,y=sep.outputs['X'],sep.outputs['Y']
angle=mathnode('ARCTAN2',y,x)
minor=mathnode('GREATER_THAN',mathnode('COSINE',mathnode('MULTIPLY',angle,60)),.55)
major=mathnode('GREATER_THAN',mathnode('COSINE',mathnode('MULTIPLY',angle,12)),.97)
radius=mathnode('SQRT',mathnode('ADD',mathnode('MULTIPLY',x,x),mathnode('MULTIPLY',y,y)))
pattern=mathnode('MAXIMUM',minor,major)
mask=mathnode('GREATER_THAN',radius,8.6)
mix=nt.nodes.new('ShaderNodeMixRGB');mix.inputs[1].default_value=(.045,.055,.06,1);mix.inputs[2].default_value=(.42,.46,.48,1)
nt.links.new(mathnode('MULTIPLY',pattern,mask),mix.inputs[0]);nt.links.new(mix.outputs[0],pr.inputs['Base Color'])
nt.links.new(pr.outputs[0],out.inputs[0]);dial.data.materials.clear();assign(dial,dm)

def hand(name,length,width,angle,z):
    bpy.ops.mesh.primitive_cube_add(size=1,location=(0,0,z))
    o=bpy.context.object;o.name=name;o.dimensions=(width,length,.12)
    bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
    # At 10:10, hour points upper-left, minute points upper-right.
    o.location.x=-math.sin(angle)*(length/2-1);o.location.y=math.cos(angle)*(length/2-1)
    o.rotation_euler.z=angle;assign(o,handmat);bevel(o,.06)
    tip=cylinder(name+' | red tip',width*.62,.14,z+.02,red,
        -math.sin(angle)*(length-1.8),math.cos(angle)*(length-1.8))
    return o
hand('Hour hand | visual only',9.5,.78,math.radians(55),5.65)
hand('Minute hand | visual only',13.5,.58,math.radians(-60),5.9)
cylinder('Hand hub | reference',.9,.4,5.8,handmat)
crown=cylinder('Crown | reference only',2.1,2.3,3.8,steel,x=19.4)
crown.rotation_euler.y=math.pi/2;bevel(crown,.12)
# Low single dome, approximate envelope of 33 x H2.5 x edge1.3 crystal.
n=192;nr=24;vs=[(0,0,9.1)];fs=[]
for j in range(1,nr+1):
    r=16.5*j/nr; z=7.9+1.2*(1-(r/16.5)**2)
    vs.extend([(r*math.cos(i*2*math.pi/n),r*math.sin(i*2*math.pi/n),z) for i in range(n)])
for i in range(n):fs.append((0,1+i,1+(i+1)%n))
for j in range(nr-1):
    a=1+j*n;b=a+n
    for i in range(n):k=(i+1)%n;fs.append((a+i,b+i,b+k,a+k))
start=len(vs);vs.extend([(16.5*math.cos(i*2*math.pi/n),16.5*math.sin(i*2*math.pi/n),6.6) for i in range(n)])
for i in range(n): k=(i+1)%n;fs.append((1+(nr-1)*n+i,start+i,start+k,1+(nr-1)*n+k))
fs.append(tuple(reversed(range(start,start+n))))
glass=mat('Crystal | visual envelope',(.9,.96,1),0,.08)
gp=glass.node_tree.nodes.get('Principled BSDF');gp.inputs['Transmission Weight'].default_value=1;gp.inputs['IOR'].default_value=1.76
crystal=mesh('CRYSTAL | 33 low dome | reference envelope',vs,fs,glass)
crystal.hide_render=True # Keep the dial visible in the review render; envelope remains in file.
crystal.hide_set(True)

floor=mat('Backdrop',(.022,.029,.034),0,.55)
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.35));plane=bpy.context.object;plane.name='Studio backdrop';assign(plane,floor)
def aim(obj,point):obj.rotation_euler=(Vector(point)-obj.location).to_track_quat('-Z','Y').to_euler()
for loc,power,size in [((-35,-10,65),100000,45),((30,20,45),70000,30),((-10,40,20),40000,25)]:
    bpy.ops.object.light_add(type='AREA',location=loc);o=bpy.context.object;o.data.energy=power;o.data.shape='DISK';o.data.size=size;aim(o,(0,0,2))
bpy.ops.object.camera_add(location=(38,-48,85));cam=bpy.context.object;aim(cam,(0,0,3));cam.data.type='ORTHO';cam.data.ortho_scale=59;scene.camera=cam
scene.render.engine='CYCLES';scene.cycles.samples=32
scene.render.resolution_x=1200;scene.render.resolution_y=1400;scene.render.resolution_percentage=100
scene.world=bpy.data.worlds.new('Watch studio');scene.world.use_nodes=True;scene.world.node_tree.nodes['Background'].inputs[0].default_value=(.18,.21,.24,1)
scene.view_settings.view_transform='AgX'
scene['stage']='PHASE 1: appearance and proportions, NOT FOR ORDER'
scene['target_mm']='37 OD; 44 lug to lug; 18 lug gap; 9.1 approximate low dome total'
scene['pending']='Movement mount, functional dial relief, bores, gasket seats, back retention, tolerances, finishing'

# Export only the physical blanks as separate studies. No assembly STL for ordering.
import bmesh
checks=[]
for o,stem in [(case,'case_study'),(dial,'dial_study'),(back,'caseback_study')]:
    bpy.ops.object.select_all(action='DESELECT');o.select_set(True);bpy.context.view_layer.objects.active=o
    bpy.ops.wm.stl_export(filepath=str(ROOT/'STL'/f'{stem}.stl'),export_selected_objects=True,apply_modifiers=True,global_scale=1.0,use_scene_unit=False)
    bm=bmesh.new();bm.from_mesh(o.data);nonmanifold=sum(not e.is_manifold for e in bm.edges);bm.free()
    checks.append({'part':stem,'dimensions_mm':list(o.dimensions),'non_manifold_edges':nonmanifold})
(ROOT/'checks.json').write_text(json.dumps({'stage':'proportion study only','parts':checks},indent=2))
bpy.ops.object.select_all(action='DESELECT');case.select_set(True);bpy.context.view_layer.objects.active=case
for area in bpy.context.screen.areas:
    if area.type=='VIEW_3D':
        area.spaces.active.region_3d.view_distance=65
        area.spaces.active.region_3d.view_location=(0,0,3)
scene.render.filepath=str(ROOT/'watch_proportion_review.png')
bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'watch_study.blend'))
print('STUDY_SAVED',checks)
