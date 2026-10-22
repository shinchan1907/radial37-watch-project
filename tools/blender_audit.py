import bpy,bmesh,json,sys
from pathlib import Path
args=sys.argv[sys.argv.index('--')+1:]
root=Path(args[0]); out=Path(args[1]); mode=args[2]
results=[]
def inspect(o):
    bm=bmesh.new(); bm.from_mesh(o.data)
    bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=0.00001)
    bm.normal_update()
    r={'name':o.name,'dimensions_mm':[round(v,6) for v in o.dimensions], 'vertices':len(bm.verts),'faces':len(bm.faces),'nonmanifold_edges':sum(not e.is_manifold for e in bm.edges),'boundary_edges':sum(e.is_boundary for e in bm.edges),'hidden_viewport':o.hide_get(),'hidden_render':o.hide_render}
    bm.free(); return r
if mode=='stl':
    bpy.ops.object.select_all(action='SELECT'); bpy.ops.object.delete(use_global=False)
    for p in sorted(root.rglob('*.stl')):
        bpy.ops.wm.stl_import(filepath=str(p))
        obs=list(bpy.context.selected_objects)
        results.append({'path':p.relative_to(root).as_posix(),'objects':[inspect(o) for o in obs if o.type=='MESH']})
        for o in obs: bpy.data.objects.remove(o,do_unlink=True)
else:
    results={'file':Path(bpy.data.filepath).relative_to(root).as_posix(),'unit_system':bpy.context.scene.unit_settings.system,'scale_length':bpy.context.scene.unit_settings.scale_length,'objects':[inspect(o) if o.type=='MESH' else {'name':o.name,'type':o.type} for o in bpy.context.scene.objects]}
out.write_text(json.dumps(results,indent=2))
print('AUDIT_SAVED',out)
