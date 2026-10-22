"""Read saved V3 mesh data directly; export only topology-clean review parts.

Run with Blender --disable-autoexec --background ORIGINAL.blend --python THIS.
Original scene and source files are never saved or modified on disk.
"""
import bpy,bmesh,hashlib,json,struct
from pathlib import Path

root=Path(bpy.data.filepath).parents[2]
dest=root/'development'/'v3_refinement'
(dest/'STL_REVIEW_ONLY').mkdir(parents=True,exist_ok=True)
source=Path(bpy.data.filepath)
report={'status':'DEVELOPMENT REVIEW ONLY; NOT RELEASED FOR PRINTING','source_file':source.relative_to(root).as_posix(),'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'method':'direct world-space mesh serialization; no selection/visibility-dependent export','units':'mm','parts':[]}
pairs=[('V3 CASE | finished reference, 37mm','case'),('V3 BACK | finished threaded, no screws','back'),('V3 ARCHES | fine-detail metal chapter','chapter'),('V3 CENTER DIAL | brass 0.40mm','center_dial'),('V3 CARRIER | polymer fit prototype','carrier'),('V3 PRINT STOCK | case, machining required','case_stock'),('V3 PRINT STOCK | back, machining required','back_stock')]
for name,slug in pairs:
    obj=bpy.data.objects[name]
    bm=bmesh.new();bm.from_mesh(obj.data)
    bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=0.00001)
    bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces))
    bm.normal_update()
    bad=sum(not e.is_manifold for e in bm.edges)
    remaining=set(bm.verts); components=0
    while remaining:
        components+=1; stack=[remaining.pop()]
        while stack:
            v=stack.pop()
            for edge in v.link_edges:
                other=edge.other_vert(v)
                if other in remaining:remaining.remove(other);stack.append(other)
    volume=bm.calc_volume(signed=True)
    item={'object':name,'slug':slug,'dimensions_mm':list(obj.dimensions),'nonmanifold_edges':bad,'components':components,'signed_volume_mm3':volume,'released_for_printing':False}
    if not bm.faces or bad or components!=1 or volume<=0:
        item.update({'exported':False,'reason':'rejected by geometry gate; no STL written'})
    else:
        bmesh.ops.triangulate(bm,faces=list(bm.faces))
        path=dest/'STL_REVIEW_ONLY'/f'{slug}_v3_recovered_REVIEW_ONLY.stl'
        with path.open('wb') as f:
            f.write(b'RADIAL37 V3 RECOVERY - REVIEW ONLY - NOT A PRINT RELEASE'.ljust(80,b' '));f.write(struct.pack('<I',len(bm.faces)))
            for face in bm.faces:
                vs=[obj.matrix_world@v.co for v in face.verts]
                normal=(vs[1]-vs[0]).cross(vs[2]-vs[0]).normalized()
                f.write(struct.pack('<12fH',*normal,*vs[0],*vs[1],*vs[2],0))
        item.update({'exported':True,'path':path.relative_to(root).as_posix(),'triangles':len(bm.faces),'bytes':path.stat().st_size,'sha256':hashlib.sha256(path.read_bytes()).hexdigest()})
    report['parts'].append(item);bm.free()
(dest/'export_recovery_report.json').write_text(json.dumps(report,indent=2))
print(json.dumps(report,indent=2))
