RADIAL 37 WATCH PROJECT - DEVELOPMENT HANDOFF
Packaged 2026-10-22

STATUS: DEVELOPMENT ARCHIVE, NOT A METAL-PRINT MANUFACTURING RELEASE.
The requested quarter-turn bayonet twistback has NOT been implemented yet.

START HERE
Open project/radial37_v2/radial37_v2.blend in Blender 5.2.
This is the most developed visual prototype with the sculpted radial dial.
Preview: project/radial37_v2/radial37_v2_hero.png.
Latest experimental work: project/radial37_v3/radial37_v3.blend.
Read the version status below before using any STL files.

DESIGN BRIEF
37 mm outside case diameter, inexpensive slim quartz movement, domed crystal,
rounded edges and matching lugs, radial curved dial ribs inspired by supplied
watch photographs, stainless steel or titanium printing through JLC.
18 mm strap gap and approximately 44 mm lug-to-lug are design targets.
Latest closure decision: quarter-turn bayonet; print-only route without extra
precision machining. Some earlier files assume machining and are superseded.

VERSION STATUS
V1: project/watch_study.blend and project/src - initial proportion study.
V2: project/radial37_v2 - visual prototype, 60 curved ribs and 12 hour arches.
    Saved STL mesh checks passed (closed, one component per exported part).
    These checks do not establish manufacturability or functional fit.
    The back uses small screw holes; mating case fastening is unfinished.
    Fine ribs and dial details require redesign/vendor assessment for metal.
V3: project/radial37_v3 - UNFINISHED / SUPERSEDED screw-down experiment.
    Case and back mesh checks FAILED: non-manifold geometry is recorded in
    geometry-checks.json. Do not print these files, including files labelled
    FINISHED_reference or PRINT_STOCK_HOLD. Names are historical, not approvals.
    Nominal internal clearance checks are partial development evidence only.
    The chapter STL predates the latest dial change in the Blender/source files.
    V3 exports, source and validation reports are not a synchronized release.
    Fine thread and machining-stock concepts do not meet the latest print-only
    bayonet requirement. No functioning bayonet model is included.

CONTENTS
project/ contains native Blender scenes, Python source, STL exports, preview
images, design notes, historical validation reports and Miyota 5Y20 PDFs.
references/ contains available user-supplied reference images and source URLs.
MANIFEST.json lists SHA-256 checksums and sizes for packaged files.
Runtime environments, caches, Blender autosave duplicates and private app
configuration are omitted. No valid STEP export was produced.

EDITING / REBUILDING
The .blend files are directly editable. Units are millimeters; STL files carry
no unit metadata, so import them as millimeters and verify the 37 mm case OD.
Blender source scripts use Blender's bundled bpy/bmesh, mathutils and Python.
For V2, use Blender's Scripting workspace to open src/radial37_v2.py and run it
in a fresh file. Scripts can create scenes and write files in their parent
project folder; work from a copy. V3 also imports adjacent parameters.py;
its src folder must be on Python's module search path. V3 is retained for
engineering continuation, not as a validated reproducible manufacturing build.
Initial cadgen source sketches are historical; their CAD kernel could not run
under the original Windows application-control policy. They are not validated
alternatives to the Blender geometry.

REMAINING WORK BEFORE ORDERING METAL
1. Replace the superseded closure with matching quarter-turn tabs, entry slots,
   retention tracks, positive stops and a suitable anti-unlock arrangement.
2. Reconcile slimness, metal printing limits, assembly clearance and sealing.
3. Confirm exact purchased movement, hands, stem/crown/tube, crystal and gasket;
   verify their drawings, mounting, battery access and assembly sequence.
4. Check dial support, stem travel and hands throughout the complete assembly;
   verify bayonet insertion/rotation with tolerances, not just nominal overlaps.
5. Repair meshes, regenerate synchronized exports, recheck all parts and obtain
   vendor feedback. Prototype the fit before an expensive metal order.
No water-resistance rating or metal-print fit has been established.

REFERENCE ATTRIBUTION
Reference watch photographs are supplied inspiration, associated with Carter
Hurd's watch project. No ownership or redistribution licence is claimed for
third-party images or manufacturer PDFs; retain their original attribution.
Historical notes/reports may describe earlier choices. This README records the
latest brief and takes precedence for interpreting archive status.
