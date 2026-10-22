"""Independent checks of the saved quote-candidate CAD and mesh files."""
from pathlib import Path
import json,hashlib,math
import cadquery as cq
import trimesh

ROOT=Path(__file__).resolve().parents[1]
def cyl(r,z0,z1,x=0,y=0):return cq.Solid.makeCylinder(r,z1-z0,cq.Vector(x,y,z0))
def footprint(clearance,z0,z1):
    return cyl(9.25+clearance,z0,z1).intersect(cq.Solid.makeBox(15.3+2*clearance,18.5+2*clearance,z1-z0+2,cq.Vector(-7.65-clearance,-9.25-clearance,z0-1)))

parts={};meshes={};hashes={}
for name in ['case','back','dial']:
    for mode,folder in [('PRINT_STOCK','STL_PRINT_STOCK'),('FINISHED_REFERENCE','STL_FINISHED_REFERENCE')]:
        key=f'{name}_{mode}';p=ROOT/'STEP'/(key+'.step');s=cq.importers.importStep(str(p)).val()
        if not s.isValid() or len(s.Solids())!=1:raise RuntimeError('Invalid saved STEP: '+key)
        parts[key]=s;hashes[p.relative_to(ROOT).as_posix()]=hashlib.sha256(p.read_bytes()).hexdigest()
        path=ROOT/folder/(key+'.stl');m=trimesh.load_mesh(path)
        meshes[key]={'watertight':bool(m.is_watertight),'is_volume':bool(m.is_volume),'body_count':int(m.body_count),'triangles':len(m.faces),'dimensions_mm':m.extents.tolist(),'sha256':hashlib.sha256(path.read_bytes()).hexdigest()}
        if not m.is_watertight or not m.is_volume or m.body_count!=1:raise RuntimeError('Invalid saved mesh: '+key)
        print('SAVED_ARTIFACT_VALID',key,flush=True)
c=parts['case_FINISHED_REFERENCE'];b=parts['back_FINISHED_REFERENCE'];d=parts['dial_FINISHED_REFERENCE']
poses=[]
for angle in range(0,91,5):
    posed=b.rotate((0,0,0),(0,0,1),angle).translate((0,0,.1))
    poses.append({'angle_deg':angle,'z_mm':.1,'overlap_mm3':c.intersect(posed).Volume()})
for dz in [-3,-2,-1,0,.1]:poses.append({'angle_deg':0,'z_mm':dz,'overlap_mm3':c.intersect(b.translate((0,0,dz))).Volume()})
for dz in [0,.025,.05,.075,.1]:poses.append({'angle_deg':90,'z_mm':dz,'overlap_mm3':c.intersect(b.rotate((0,0,0),(0,0,1),90).translate((0,0,dz))).Volume()})
closed=b.rotate((0,0,0),(0,0,1),90)
movement=footprint(0,3.05,6.2)
for x,y in [(-7.9,-3),(8.234,-1.9)]:movement=movement.cut(cyl(.40,4.5,6.3,x,y))
carrier=cyl(14.4,2.3,3.05).fuse(cyl(10.65,3.05,3.85)).cut(footprint(.2,3.05,6.5))
carrier=carrier.fuse(cq.Solid.makeBox(1.4,1.4,.8,cq.Vector(-.7,9.5,3.5))).fuse(cq.Solid.makeBox(1.4,7.0,.60,cq.Vector(-.7,9.7,4.0)))
stem=cq.Solid.makeCylinder(.45,13,cq.Vector(7.4,0,5.35),cq.Vector(1,0,0))
intersections={}
for label,a,bb in [('dial_case',d,c),('dial_back',d,closed),('movement_dial',movement,d),('movement_carrier',movement,carrier),('carrier_dial',carrier,d),('carrier_case',carrier,c),('carrier_back_closed',carrier,closed),('carrier_back_pushed',carrier,closed.translate((0,0,.1))),('stem_dial',stem,d),('stem_case',stem,c)]:
    intersections[label]=a.intersect(bb).Volume()
    print('PAIR',label,intersections[label],flush=True)
containment={}
for name in ['case','back','dial']:
    containment[name]=parts[name+'_FINISHED_REFERENCE'].cut(parts[name+'_PRINT_STOCK']).Volume()
    print('STOCK_CONTAINMENT',name,containment[name],flush=True)
positive_controls={'reverse_88deg_without_push_overlap_mm3':c.intersect(b.rotate((0,0,0),(0,0,1),88)).Volume(),'overturn_92deg_overlap_mm3':c.intersect(b.rotate((0,0,0),(0,0,1),92)).Volume(),'pull_locked_back_down_overlap_mm3':c.intersect(closed.translate((0,0,-.1))).Volume()}
boss_top=1.5+b.intersect(cyl(1.0,1.5,2.5)).Volume()/math.pi
preload={'back_support_top_z_measured':boss_top,'carrier_floor_bottom_z':2.3,'locked_gap_mm':2.3-boss_top,'pushed_gap_mm':2.2-boss_top,'candidate':'Three small compliant pads; free thickness around 0.8mm, material/load/aging qualification required','manufacturing_release':False}
budget={'status':'REQUESTED FINISHING TOLERANCES; NOT YET AGREED BY SUPPLIER','spigot_radial_gap_mm':{'nominal':.2,'worst_min':.15,'worst_max':.25,'assumed_radius_tolerance_each':.025},'track_radial_gap_mm':{'nominal':.2,'worst_min':.15,'worst_max':.25,'assumed_radius_tolerance_each':.025},'dial_radial_gap_mm':{'nominal':.2,'worst_min':.15,'worst_max':.25,'assumed_radius_tolerance_each':.025},'detent_axial_drop_mm':{'nominal':.1,'worst_min':.06,'worst_max':.14,'assumed_level_tolerance_each':.02},'gasket':{'nominal_installed_cs':1.0,'cs_tolerance_assumed':.02,'groove_depth':.73,'groove_depth_tolerance_requested':.01,'locked_face_gap':.10,'face_gap_tolerance_requested':.015,'locked_squeeze_range_pct':[100*(1-(.73+.01+.10+.015)/.98),100*(1-(.73-.01+.10-.015)/1.02)],'pressed_squeeze_range_pct':[100*(1-.74/.98),100*(1-.72/1.02)],'hold':'Installed CS, compound, squeeze/load, stretch, lubrication and wear require supplier/component validation'}}
report={'status':'QUOTE REVIEW ONLY; NO MANUFACTURING RELEASE','source_sha256':hashlib.sha256((ROOT/'src'/'titanium_design.py').read_bytes()).hexdigest(),'saved_step_hashes':hashes,'saved_meshes':meshes,'sampled_motion_poses':poses,'all_nominal_poses_clear':all(abs(p['overlap_mm3'])<1e-5 for p in poses),'nominal_intersections_mm3':intersections,'all_nominal_component_pairs_clear':all(abs(v)<1e-5 for v in intersections.values()),'finished_material_outside_stock_mm3':containment,'finished_targets_inside_stock':all(abs(v)<1e-5 for v in containment.values()),'positive_retention_controls':positive_controls,'preload_space':preload,'tolerance_budget':budget,'holds':['Supplier acceptance of all finishing and supports','Exact crystal/gasket/crown/tube/hand/spring-bar specifications','Physical fit, detent release force, pull strength and wear','Full tolerance/structural review and pressure testing if water resistance is claimed']}
(ROOT/'validation'/'saved_artifact_checks.json').write_text(json.dumps(report,indent=2))
print(json.dumps({k:v for k,v in report.items() if k not in ['saved_step_hashes','sampled_motion_poses','tolerance_budget']},indent=2))
if not report['all_nominal_poses_clear'] or not report['all_nominal_component_pairs_clear'] or not report['finished_targets_inside_stock']:raise SystemExit(2)
