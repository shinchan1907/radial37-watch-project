"""Make OCCT STL edge subdivisions conforming without filling real holes.

Only splits an existing boundary triangle edge at an existing boundary vertex
already on that edge within 0.00001 mm. No scaling, voxelisation or smoothing.
"""
from pathlib import Path
import json,hashlib
import numpy as np
import trimesh
from scipy.spatial import cKDTree

def conform(path,out,tolerance=1e-5):
    mesh=trimesh.load_mesh(path);before_volume=float(mesh.volume);before_faces=len(mesh.faces)
    vertices=mesh.vertices.copy();faces=mesh.faces.copy();splits=0;max_deviation=0.0
    tree=cKDTree(vertices);reps=np.full(len(vertices),-1,dtype=np.int64)
    for i,point in enumerate(vertices):
        if reps[i]>=0:continue
        neighbours=np.asarray(tree.query_ball_point(point,tolerance),dtype=np.int64)
        neighbours=neighbours[reps[neighbours]<0];reps[neighbours]=i
    max_weld=float(np.linalg.norm(vertices-vertices[reps],axis=1).max())
    if max_weld>tolerance:raise RuntimeError('Weld cluster exceeds allowed displacement')
    faces=reps[faces]
    collapsed=(faces[:,0]==faces[:,1])|(faces[:,1]==faces[:,2])|(faces[:,2]==faces[:,0])
    removed_collapsed=int(collapsed.sum());faces=faces[~collapsed]
    _,unique=np.unique(np.sort(faces,axis=1),axis=0,return_index=True)
    duplicate_count=len(faces)-len(unique);faces=faces[np.sort(unique)]
    for iteration in range(12):
        current=trimesh.Trimesh(vertices=vertices,faces=faces,process=False)
        counts=np.bincount(current.edges_unique_inverse)
        boundary=current.edges_unique[counts==1]
        if not len(boundary):break
        boundary_set={tuple(sorted(e)) for e in boundary};boundary_vertices=np.unique(boundary)
        changed=False;new_faces=[]
        for face in faces:
            split=False
            for j in range(3):
                a,b,c=int(face[j]),int(face[(j+1)%3]),int(face[(j+2)%3])
                if tuple(sorted((a,b))) not in boundary_set:continue
                delta=vertices[b]-vertices[a];length2=float(delta@delta)
                if length2<1e-16:raise RuntimeError('Degenerate source boundary')
                ts=(vertices[boundary_vertices]-vertices[a])@delta/length2
                projected=vertices[a]+ts[:,None]*delta
                errors=np.linalg.norm(vertices[boundary_vertices]-projected,axis=1)
                ids=np.where((ts>1e-7)&(ts<1-1e-7)&(errors<=tolerance))[0]
                if not len(ids):continue
                ids=ids[np.argsort(ts[ids])]
                points=[a]+[int(boundary_vertices[k]) for k in ids]+[b]
                for u,v in zip(points,points[1:]):
                    if np.linalg.norm(np.cross(vertices[v]-vertices[u],vertices[c]-vertices[u]))<1e-12:raise RuntimeError('Would create a degenerate triangle')
                    new_faces.append((u,v,c))
                max_deviation=max(max_deviation,float(errors[ids].max()));splits+=len(ids);changed=True;split=True;break
            if not split:new_faces.append(face)
        faces=np.asarray(new_faces,dtype=np.int64)
        if not changed:raise RuntimeError('Real boundary or unresolved mesh defect; refusing hole fill: '+str(path)+'; remaining='+str(vertices[boundary].tolist()[:12]))
    result=trimesh.Trimesh(vertices=vertices,faces=faces,process=True)
    if not result.is_watertight or not result.is_volume or result.body_count!=1:raise RuntimeError('Mesh gate failed: '+str(path))
    if abs(float(result.volume)-before_volume)>1e-3:raise RuntimeError('Unexpected volume change')
    out.parent.mkdir(parents=True,exist_ok=True);result.export(out,file_type='stl')
    saved=trimesh.load_mesh(out)
    if not saved.is_watertight or not saved.is_volume or saved.body_count!=1:raise RuntimeError('Saved-file gate failed')
    return {'input':str(path.name),'output':out.name,'welded_vertex_count':len(vertices)-len(np.unique(reps)),'removed_collapsed_triangles':removed_collapsed,'removed_duplicate_triangles':duplicate_count,'max_weld_displacement_mm':max_weld,'edge_splits':splits,'max_existing_vertex_to_edge_deviation_mm':max_deviation,'triangle_count_before':before_faces,'triangle_count_after':len(saved.faces),'volume_change_mm3':float(saved.volume)-before_volume,'watertight':bool(saved.is_watertight),'body_count':int(saved.body_count),'sha256':hashlib.sha256(out.read_bytes()).hexdigest()}

def conform_all(root):
    root=Path(root);records=[]
    for mode,folder in [('PRINT_STOCK','STL_PRINT_STOCK'),('FINISHED_REFERENCE','STL_FINISHED_REFERENCE')]:
        for part in ['case','back','dial']:
            name=f'{part}_{mode}.stl';records.append(conform(root/'build'/'raw_stl'/name,root/folder/name))
    (root/'validation').mkdir(exist_ok=True);(root/'validation'/'mesh_conformity.json').write_text(json.dumps(records,indent=2))
    return records

if __name__=='__main__':
    import sys
    print(json.dumps(conform_all(sys.argv[1]),indent=2))
