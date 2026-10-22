"""V3/2035 fit study. Run stages through the official Blender MCP.

Original objects are preserved in their scene and in a pre-edit checkpoint.
This study intentionally leaves the unresolved case/back geometry unchanged.
"""
import bpy,bmesh,math,json,hashlib,struct
from pathlib import Path
from mathutils import Vector

ROOT=Path(r'C:\Users\Sunny gupta\Downloads\Radial37_Watch_Project')
DEST=ROOT/'development'/'v3_refinement'
SCENE='RADIAL 37 | V3 2035 FIT STUDY 01'
BASE='RADIAL 37 | V3 slim screw-down engineering'

def scene(): return bpy.data.scenes[SCENE]
def source(name):
    return next(o for o in scene().objects if o.get('source_object')==name)
def material(name,color):
    m=bpy.data.materials.new(name);m.diffuse_color=(*color,1);m.use_nodes=True
    p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=(*color,1);p.inputs['Roughness'].default_value=.35
    return m
def cyl(name,r,h,z,mat=None,x=0,y=0):
    bpy.ops.mesh.primitive_cylinder_add(vertices=192,radius=r,depth=h,location=(x,y,z))
    o=bpy.context.object;o.name=name
    if mat:o.data.materials.append(mat)
    return o
def box(name,size,loc):
    bpy.ops.mesh.primitive_cube_add(size=1,location=loc);o=bpy.context.object;o.name=name;o.dimensions=size
    bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);return o
def boolean(a,b,operation='DIFFERENCE'):
    bpy.context.view_layer.objects.active=a
    m=a.modifiers.new('FIT2035 '+operation,'BOOLEAN');m.solver='EXACT';m.operation=operation;m.object=b
    bpy.ops.object.modifier_apply(modifier=m.name);bpy.data.objects.remove(b,do_unlink=True)
def footprint(name,clearance,z0,z1,mat=None):
    o=cyl(name,9.25+clearance,z1-z0,(z0+z1)/2,mat)
    clip=box('GEO-2035-footprint-clip',(15.3+2*clearance,18.5+2*clearance,z1-z0+2),(0,0,(z0+z1)/2))
    boolean(o,clip,'INTERSECT');return o
def hide(o):o.hide_render=True;o.hide_set(True)
def clean(o):
    bm=bmesh.new();bm.from_mesh(o.data)
    bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=.00001)
    bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(o.data);bm.free();o.data.update()

def stage1():
    if SCENE in bpy.data.scenes:raise RuntimeError('Fit scene already exists; inspect before rerunning')
    checkpoint=DEST/'checkpoints'/'v3_live_before_2035.blend';checkpoint.parent.mkdir(exist_ok=True)
    if checkpoint.exists():raise RuntimeError('Checkpoint exists; will not overwrite')
    bpy.ops.wm.save_as_mainfile(filepath=str(checkpoint),copy=True)
    old=bpy.context.scene
    if old.name!=BASE:raise RuntimeError('Unexpected active scene')
    s=bpy.data.scenes.new(SCENE);s.unit_settings.system='METRIC';s.unit_settings.scale_length=.001;s.unit_settings.length_unit='MILLIMETERS'
    if old.world:s.world=old.world.copy()
    for o in old.objects:
        n=o.copy()
        if o.data:n.data=o.data.copy()
        s.collection.objects.link(n);n['source_object']=o.name
        prefix='CAM-' if o.type=='CAMERA' else 'LGT-' if o.type=='LIGHT' else 'GEO-'
        n.name=prefix+'FIT2035-'+o.name
        n.hide_render=o.hide_render
        if o==old.camera:s.camera=n
    bpy.context.window.scene=s
    for o in s.objects:
        src=bpy.data.objects[o['source_object']]
        o.hide_set(src.hide_get(view_layer=old.view_layers[0]))
    s['baseline_file']='project/radial37_v3/radial37_v3.blend'
    s['manufacturing_release']=False;s['movement']='Miyota 2035';s['closure_status']='unchanged historical thread; decision pending'
    return {'scene':s.name,'copied_objects':len(s.objects),'checkpoint':str(checkpoint)}

def stage2():
    bpy.context.window.scene=scene()
    if 'GEO-2035-movement-envelope' in bpy.data.objects:raise RuntimeError('2035 geometry already exists')
    blue=material('MAT-2035-movement-proxy',(.035,.12,.24));polymer=material('MAT-2035-polymer-carrier',(.035,.045,.055))
    brass=source('V3 CENTER DIAL | brass 0.40mm').data.materials[0]
    for name in ['V3 5Y20 | conservative casing envelope','V3 CARRIER | polymer fit prototype','V3 CENTER DIAL | brass 0.40mm','V3 STEM | physical .70 envelope','CHECK | stem tolerance swept envelope','CHECK | rotating hands envelope']:
        hide(source(name))
    movement=footprint('GEO-2035-movement-envelope',0,1.65,4.8,blue)
    movement['status']='CONSERVATIVE ENVELOPE; NOT VENDOR CAD'
    feet=[(-7.9,-3),(8.234,-1.9)]
    for x,y in feet:boolean(movement,cyl('GEO-2035-dial-foot-interface',.40,1.75,4.025,x=x,y=y))
    carrier=cyl('GEO-2035-carrier-fit',14.4,.75,1.275,polymer)
    boolean(carrier,cyl('GEO-2035-carrier-locator',10.65,.80,2.05,polymer),'UNION')
    boolean(carrier,footprint('GEO-2035-carrier-pocket',.20,1.65,5.1))
    boolean(carrier,box('GEO-2035-antirotation-connector',(1.4,1.4,.8),(0,10.2,2.5)),'UNION')
    boolean(carrier,box('GEO-2035-antirotation-arm',(1.4,6.15,.6),(0,12.775,2.9)),'UNION')
    carrier['status']='FIT PROPOSAL; 0.20 mm nominal pocket clearance; retention and process limits pending'
    plate=cyl('GEO-2035-center-dial-fit',9.25,.40,5.0,brass)
    boolean(plate,cyl('GEO-2035-dial-center-hole',.60,1,5))
    for x,y in feet:boolean(plate,cyl('GEO-2035-dial-foot',.35,1.60,4.10,brass,x,y),'UNION')
    plate['status']='Nominal manufacturer dial/feet; fit tolerances and fabrication pending'
    stem=cyl('GEO-2035-stem-envelope',.45,13.0,3.95,x=13.9);stem.rotation_euler.y=math.pi/2
    stem['status']='0.90 mm envelope, not full setting stem CAD'
    arbor=cyl('GEO-2035-seconds-arbor-envelope',.10,1.60,5.60,blue)
    arbor['status']='Kept for clearance despite two-hand styling; actual variant pending'
    for o in [movement,carrier,plate,stem,arbor]:clean(o)
    hide(movement);hide(carrier);hide(arbor)
    return {'created':[o.name for o in [movement,carrier,plate,stem,arbor]],'dial_top':5.2,'stem_axis':3.95,'carrier_locator_top':2.45}

def stage3():
    bpy.context.window.scene=scene()
    # New nominal hand placements are proposals, not purchased hand geometry.
    for name in ['V3 HOUR HAND | envelope','V3 HOUR HAND | envelope red tip','V3 MINUTE HAND | envelope','V3 MINUTE HAND | envelope red tip','V3 HAND HUB']:
        o=source(name);o.location.z+=.26
        o['status']='2035 appearance/clearance proposal; exact hand fitting pending'
        if 'MINUTE' in name:o.scale.y*=13.0/13.8
    # Appearance crown/tube move with stem; the old case bore is deliberately unchanged.
    for name in ['V3 CROWN | fluted reference','V3 CROWN TUBE | provisional 1.8 OD']:
        o=source(name);o.location.z+=.56;o['status']='REPOSITIONED PROXY; CASE BORE NOT YET UPDATED'
    s=scene();s.render.engine='CYCLES';s.cycles.samples=48;s.cycles.use_denoising=True
    s.cycles.use_adaptive_sampling=True;s.cycles.adaptive_threshold=.07;s.cycles.transmission_bounces=24
    s.render.resolution_x=1100;s.render.resolution_y=1100;s.render.resolution_percentage=100
    s.render.image_settings.file_format='PNG';s.view_settings.view_transform='AgX'
    nodes=s.world.node_tree.nodes;nodes.clear()
    bg=nodes.new('ShaderNodeBackground');bg.inputs['Color'].default_value=(.04,.04,.05,1);bg.inputs['Strength'].default_value=.4
    out=nodes.new('ShaderNodeOutputWorld');s.world.node_tree.links.new(bg.outputs[0],out.inputs['Surface'])
    crystal=source('V3 CRYSTAL | 33mm H4.30, provisional inner');crystal.hide_render=False;crystal.hide_set(False)
    if s.camera is None:raise RuntimeError('Missing camera')
    for area in bpy.context.screen.areas:
        if area.type=='VIEW_3D':area.spaces.active.shading.type='MATERIAL'
    s['fit_study_status']='Movement/dial/carrier/hand proposals only; unchanged case bore is misaligned by 0.56 mm'
    bpy.context.view_layer.update()
    target=DEST/'radial37_v3_2035_fit_01.blend'
    bpy.ops.wm.save_as_mainfile(filepath=str(target))
    return {'saved':str(target),'minute_hand_proposal_mm':13.0,'original_minute_hand_mm':13.8,'case_stem_bore_requires_update_mm':.56,'manufacturing_release':False}

def topology(o):
    bm=bmesh.new();bm.from_mesh(o.data);bm.normal_update()
    remaining=set(bm.verts);components=0
    while remaining:
        components+=1;stack=[remaining.pop()]
        while stack:
            v=stack.pop()
            for e in v.link_edges:
                other=e.other_vert(v)
                if other in remaining:remaining.remove(other);stack.append(other)
    vs=[o.matrix_world@v.co for v in o.data.vertices]
    r={'name':o.name,'nonmanifold_edges':sum(not e.is_manifold for e in bm.edges),'components':components,'volume_mm3':abs(bm.calc_volume()),'vertices':len(bm.verts),'faces':len(bm.faces),'world_bounds_dimensions_mm':[max(v[i] for v in vs)-min(v[i] for v in vs) for i in range(3)]}
    bm.free();return r

def validate():
    bpy.context.window.scene=scene();bpy.context.view_layer.update()
    parts=[bpy.data.objects[n] for n in ['GEO-2035-movement-envelope','GEO-2035-carrier-fit','GEO-2035-center-dial-fit','GEO-2035-stem-envelope','GEO-2035-seconds-arbor-envelope']]
    report={'scene':SCENE,'manufacturing_release':False,'parts':[topology(o) for o in parts],'intersections':[]}
    # Exact Boolean volume checks are nominal only; case/back already have invalid topology.
    pairs=[(parts[0],source('V3 ARCHES | fine-detail metal chapter')),(parts[0],parts[1]),(parts[1],source('V3 ARCHES | fine-detail metal chapter')),(parts[2],source('V3 ARCHES | fine-detail metal chapter')),(parts[0],parts[0])]
    for a,b in pairs:
        tmp=a.copy();tmp.data=a.data.copy();scene().collection.objects.link(tmp);tmp.hide_set(False)
        m=tmp.modifiers.new('nominal_intersection','BOOLEAN');m.operation='INTERSECT';m.solver='EXACT';m.object=b
        deps=bpy.context.evaluated_depsgraph_get();evaluated=tmp.evaluated_get(deps);me=evaluated.to_mesh()
        bm=bmesh.new();bm.from_mesh(me);v=abs(bm.calc_volume());bm.free();evaluated.to_mesh_clear();bpy.data.objects.remove(tmp,do_unlink=True)
        if a==b:report['boolean_positive_control']={'self_intersection_volume_mm3':v,'expected_volume_mm3':report['parts'][0]['volume_mm3'],'pass':abs(v-report['parts'][0]['volume_mm3'])<.001}
        else:report['intersections'].append({'a':a.name,'b':b.name,'nominal_interference_mm3':v,'nominal_pass':v<.0001})
    hs=[]
    for name in ['V3 HOUR HAND | envelope','V3 HOUR HAND | envelope red tip','V3 MINUTE HAND | envelope','V3 MINUTE HAND | envelope red tip']:
        o=source(name);verts=[o.matrix_world@v.co for v in o.data.vertices]
        min_gap=min(7.15-1.8*((math.hypot(v.x,v.y))/16)**2-v.z for v in verts)
        hs.append({'name':name,'max_radius_mm':max(math.hypot(v.x,v.y) for v in verts),'min_gap_to_provisional_crystal_mm':min_gap,'target_gap_mm':.30,'nominal_target_pass':min_gap>=.30})
    report['hand_crystal_analytical_checks']=hs
    report['original_13p8_minute_tip_gap_at_proposed_z_mm']=7.15-1.8*(13.8/16)**2-5.621
    report['holds']=['Case/back topology remains invalid','Existing case stem bore remains 0.56 mm below the proposed 2035 axis','Closure choice pending','Exact purchased movement perimeter/hand heights and crystal inner profile pending','Carrier floor 0.75 mm is a fit-study feature and needs process validation','No water resistance or metal-order release']
    (DEST/'fit_2035_validation.json').write_text(json.dumps(report,indent=2))
    return report

def export_fit_review():
    folder=DEST/'STL_2035_FIT_REVIEW';folder.mkdir(exist_ok=True)
    records=[]
    for name,stem in [('GEO-2035-carrier-fit','carrier_2035_fit_REVIEW_ONLY'),('GEO-2035-center-dial-fit','center_dial_2035_fit_REVIEW_ONLY')]:
        o=bpy.data.objects[name];check=topology(o)
        if check['nonmanifold_edges'] or check['components']!=1 or check['volume_mm3']<=0:raise RuntimeError('Export gate failed: '+name)
        bm=bmesh.new();bm.from_mesh(o.data);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bmesh.ops.triangulate(bm,faces=list(bm.faces))
        p=folder/(stem+'.stl')
        with p.open('wb') as f:
            f.write(b'RADIAL37 2035 FIT STUDY - NOT A MANUFACTURING RELEASE'.ljust(80,b' '));f.write(struct.pack('<I',len(bm.faces)))
            for face in bm.faces:
                vs=[o.matrix_world@v.co for v in face.verts];n=(vs[1]-vs[0]).cross(vs[2]-vs[0]).normalized()
                f.write(struct.pack('<12fH',*n,*vs[0],*vs[1],*vs[2],0))
        records.append({'file':p.relative_to(ROOT).as_posix(),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'triangles':len(bm.faces),'source_topology':check,'manufacturing_release':False});bm.free()
    (DEST/'fit_2035_export_manifest.json').write_text(json.dumps(records,indent=2))
    return records
