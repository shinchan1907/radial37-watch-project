"""Visual assembly of the V3-derived titanium bayonet candidate."""
import bpy,math,json
from pathlib import Path
from mathutils import Vector

ROOT=Path(__file__).resolve().parents[1]
SCENE='RADIAL 37 | Titanium bayonet 02'
FIT='RADIAL 37 | V3 2035 FIT STUDY 01'

def stage1():
    if SCENE in bpy.data.scenes:raise RuntimeError('Candidate scene exists; inspect before rebuilding')
    old=bpy.data.scenes[FIT];s=bpy.data.scenes.new(SCENE)
    s.unit_settings.system='METRIC';s.unit_settings.scale_length=.001;s.unit_settings.length_unit='MILLIMETERS'
    s.world=old.world.copy();bpy.context.window.scene=s
    for obj in old.objects:
        wanted=obj.type in {'CAMERA','LIGHT'} or obj.name in {'GEO-2035-movement-envelope','GEO-2035-carrier-fit','GEO-2035-stem-envelope','GEO-2035-seconds-arbor-envelope'} or any(t in obj.name for t in ['V3 CRYSTAL |','V3 CRYSTAL GASKET |','V3 CROWN |','V3 CROWN TUBE |','V3 HOUR HAND |','V3 MINUTE HAND |','V3 HAND HUB'])
        if not wanted:continue
        n=obj.copy();n.data=obj.data.copy();s.collection.objects.link(n);n['copied_from_fit']=obj.name;n.name='TI02-'+obj.name;n.location.z+=1.4
        if obj.type in {'CAMERA','LIGHT'}:n.location.z-=1.4
        n.hide_set(obj.hide_get(view_layer=old.view_layers[0]));n.hide_render=obj.hide_render
        if obj==old.camera:s.camera=n
    s['manufacturing_release']=False;s['process']='TC4 titanium SLM plus quoted precision finishing'
    s['printed_part_count']=3;s['movement']='Miyota 2035';s['closure']='90 degree bayonet with terminal pocket'
    return {'scene':s.name,'copied':len(s.objects)}

def stage2():
    s=bpy.data.scenes[SCENE];bpy.context.window.scene=s
    material=bpy.data.materials.new('MAT-TI02-satin-titanium');material.use_nodes=True;material.diffuse_color=(.46,.48,.51,1)
    bsdf=material.node_tree.nodes.get('Principled BSDF');bsdf.inputs['Base Color'].default_value=(.46,.48,.51,1);bsdf.inputs['Metallic'].default_value=1;bsdf.inputs['Roughness'].default_value=.40
    noise=material.node_tree.nodes.new('ShaderNodeTexNoise');noise.inputs['Scale'].default_value=320;noise.inputs['Detail'].default_value=2
    bump=material.node_tree.nodes.new('ShaderNodeBump');bump.inputs['Strength'].default_value=.09;bump.inputs['Distance'].default_value=.004
    material.node_tree.links.new(noise.outputs['Fac'],bump.inputs['Height']);material.node_tree.links.new(bump.outputs['Normal'],bsdf.inputs['Normal'])
    imported=[]
    for part in ['case','back','dial']:
        bpy.ops.wm.stl_import(filepath=str(ROOT/'STL_FINISHED_REFERENCE'/f'{part}_FINISHED_REFERENCE.stl'))
        o=bpy.context.object;o.name='GEO-TI02-'+part;o.data.materials.clear();o.data.materials.append(material)
        if part=='back':o.rotation_euler.z=math.pi/2
        o['status']='FINISHED TARGET; NOT AS-PRINTED UPLOAD'
        for p in o.data.polygons:p.use_smooth=True
        o.data.set_sharp_from_angle(angle=math.radians(38))
        imported.append(o.name)
    # Provisional compressed seal envelope, not a qualified elastomer model.
    bpy.ops.mesh.primitive_torus_add(major_segments=192,minor_segments=32,major_radius=17.3,minor_radius=.5,location=(0,0,1.915))
    gasket=bpy.context.object;gasket.name='GEO-TI02-back-gasket-envelope'
    for v in gasket.data.vertices:
        r=math.hypot(v.co.x,v.co.y);t=math.atan2(v.co.y,v.co.x);dr=(r-17.3)/.83
        v.co.x=(17.3+dr)*math.cos(t);v.co.y=(17.3+dr)*math.sin(t);v.co.z*=.83
    gasket.hide_render=True;gasket.hide_set(True)
    gasket['status']='Provisional installed 1.0mm CS, 0.83mm compressed-height envelope'
    return {'imported_finished_targets':imported,'gasket_height':.83}

def rearload_components():
    s=bpy.data.scenes[SCENE];bpy.context.window.scene=s
    old=next(o for o in s.objects if 'V3 CRYSTAL |' in o.name)
    glass=old.data.materials[0];bpy.data.objects.remove(old,do_unlink=True)
    profile=[(16.5*j/32,7.75+1.8*(1-(j/32)**2)) for j in range(33)]
    profile.extend([(16.5,6.8),(16.0,6.8)])
    profile.extend([(16*j/32,6.8+1.75*(1-(j/32)**2)) for j in range(31,-1,-1)])
    vs=[];rows=[];n=192
    for r,z in profile:
        if r<1e-8:rows.append([len(vs)]);vs.append((0,0,z))
        else:
            rows.append(list(range(len(vs),len(vs)+n)))
            vs.extend([(r*math.cos(i*2*math.pi/n),r*math.sin(i*2*math.pi/n),z) for i in range(n)])
    faces=[]
    for j,a in enumerate(rows):
        b=rows[(j+1)%len(rows)]
        if len(a)==len(b)==1:continue
        for i in range(n):
            k=(i+1)%n
            if len(a)==1:faces.append((a[0],b[i],b[k]))
            elif len(b)==1:faces.append((a[i],b[0],a[k]))
            else:faces.append((a[i],b[i],b[k],a[k]))
    me=bpy.data.meshes.new('TI02-provisional-double-dome');me.from_pydata(vs,[],faces);me.update()
    import bmesh
    bm=bmesh.new();bm.from_mesh(me);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(me);bm.free()
    o=bpy.data.objects.new('GEO-TI02-crystal-PROVISIONAL',me);s.collection.objects.link(o);me.materials.append(glass)
    for p in me.polygons:p.use_smooth=True
    o['status']='PROVISIONAL 33mm double dome, base 6.80, apex 9.55; not a verified purchasable crystal'
    gasket=next(o for o in s.objects if 'V3 CRYSTAL GASKET |' in o.name)
    for v in gasket.data.vertices:
        v.co.z=6.8+(v.co.z+gasket.location.z-5.25)*(.9/.95)
    gasket.location.z=0
    carrier=next(o for o in s.objects if o.get('copied_from_fit')=='GEO-2035-carrier-fit')
    bpy.ops.mesh.primitive_cube_add(size=1,location=(0,16.1,4.3))
    ext=bpy.context.object;ext.name='GEO-TI02-carrier-key-extension';ext.dimensions=(1.4,1.2,.6)
    bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
    carrier.hide_set(False);bpy.context.view_layer.objects.active=carrier
    mod=carrier.modifiers.new('Key extension','BOOLEAN');mod.solver='EXACT';mod.operation='UNION';mod.object=ext
    bpy.ops.object.modifier_apply(modifier=mod.name);bpy.data.objects.remove(ext,do_unlink=True);carrier.hide_set(True)
    s['carrier_preload_status']='0.60mm locked boss-to-carrier gap; 0.8mm free-thickness compliant pad candidate, load/material validation required'
    return {'provisional_crystal_base':6.8,'provisional_crystal_apex':9.55,'carrier_key_tip_y':16.7,'outer_dial_rail_finished_thickness':.85}

def stage3():
    s=bpy.data.scenes[SCENE];bpy.context.window.scene=s
    font=bpy.data.fonts.load(str(ROOT/'assets'/'CormorantGaramond-Medium.ttf'))
    font.pack();font.filepath='//assets/CormorantGaramond-Medium.ttf'
    ink=bpy.data.materials.new('MAT-TI02-laser-marking-preview');ink.diffuse_color=(.012,.016,.020,1);ink.use_nodes=True
    p=ink.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=(.012,.016,.020,1);p.inputs['Roughness'].default_value=.5
    for body,y,size in [('Indo',7.0,2.7),('Constantin',5.0,2.6)]:
        data=bpy.data.curves.new('ART-'+body,'FONT');data.body=body;data.font=font;data.size=size;data.align_x='CENTER';data.align_y='CENTER';data.space_character=1.1;data.fill_mode='BOTH'
        o=bpy.data.objects.new('ART-TI02-'+body,data);s.collection.objects.link(o);o.location=(0,y,6.608);data.materials.append(ink)
        o['status']='LASER MARK ARTWORK ONLY; NO PRINTED RAISED LETTERS'
    # Readable 12 hour positions independent of the coarser structural web count.
    for i in range(12):
        a=math.pi/2-i*2*math.pi/12
        bpy.ops.mesh.primitive_cube_add(size=1,location=(14.8*math.cos(a),14.8*math.sin(a),6.408))
        o=bpy.context.object;o.name=f'ART-TI02-hour-index-{i+1:02d}';o.dimensions=(.12,.70,.004);o.rotation_euler.z=a-math.pi/2;o.data.materials.append(ink)
        o['status']='LASER MARK ARTWORK ONLY'
    s.render.engine='CYCLES';s.cycles.samples=64;s.cycles.use_denoising=True;s.cycles.use_adaptive_sampling=True;s.cycles.adaptive_threshold=.055;s.cycles.transmission_bounces=24
    s.render.resolution_x=1300;s.render.resolution_y=1300;s.render.resolution_percentage=100;s.render.image_settings.file_format='PNG'
    s.view_settings.view_transform='AgX'
    case=bpy.data.objects['GEO-TI02-case']
    weighted=case.modifiers.new('Presentation weighted normals','WEIGHTED_NORMAL');weighted.keep_sharp=True;weighted.weight=40
    # Aim the retained camera at the taller assembly.
    s.camera.rotation_euler=(Vector((0,0,4.8))-s.camera.location).to_track_quat('-Z','Y').to_euler()
    for area in bpy.context.screen.areas:
        if area.type=='VIEW_3D':area.spaces.active.shading.type='MATERIAL'
    bpy.context.view_layer.update()
    path=ROOT/'radial37_titanium_bayonet_02.blend'
    bpy.ops.wm.save_as_mainfile(filepath=str(path))
    return {'file':str(path),'artwork':['Indo','Constantin'],'print_parts':3,'manufacturing_release':False}
