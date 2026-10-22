# Evidence and limits

Only the exact current saved files and hashes in `saved_artifact_checks.json` and `mesh_conformity.json` identify this candidate. `*_stock_dfam.json` and `*_stock_orientations.json` are fact-only reports on the exact stock STLs; `summary.json` binds their hashes. Older V3 audit reports elsewhere describe historical files.

The independent checker reimports six native STEP solids and six STL meshes; checks validity, single body, watertight positive-volume meshes; checks the finished targets are contained in print stock; samples 29 bayonet insertion/turn/release poses; checks ten component envelope pairs; and includes forbidden-motion overlaps as positive controls. Nominal clearances do not prove a complete worst-case assembly.

Mesh conformance welds points within 0.00001 mm and splits existing triangle edges at existing vertices within that tolerance. It removes collapsed/duplicate triangles, rejects unresolved boundaries, and records displacement, volume difference and hashes. It does not fill real holes or claim to repair invalid native CAD.

Wall checks are sampled at 6000 locations, not exhaustive. Report both minimum and fifth percentile. Supports, small open-slot cleanability, residual stress, distortion and surface quality require supplier review. Orientation reports are coarse cost/access signals, not a metal build plan; the supplier must account for thermal distortion, machining stock and datum access.

## Primary sources checked 22 October 2026

- [JLC3DP TC4](https://jlc3dp.com/help/article/titanium-tc4): SLM; recommended wall **greater than 1.5 mm**; general tolerance ±0.3 mm within 100 mm. These apply to the printed preforms, not permission to print a 0.40 mm finished dial.
- [JLC3DP design guide](https://jlc3dp.com/help/article/3d-printing-design-guideline): general process guidance for print details, clearances and cleanup. Its general escape-hole recommendations are not a certification of these open slots.
- [PCBWay TC4](https://www.pcbway.com/rapid-prototyping/3d-printing/metal/Titanium/Titanium-TC4/): published accuracy 200 microns or 0.2%, surface Ra 3.2–6.3 micrometres. No independently verified numerical PCBWay wall minimum is asserted here. [Wall guidance](https://www.pcbway.com/helpcenter/3d_engineering_questions/Wall_thickness_issue.html) requires part review.
- [Miyota 2035](https://miyotamovement.com/product/2035/), [drawing](https://miyotamovement.com/uploads/product/product_4tdsbpNVQi1WcE5lUw.pdf), [specification](https://miyotamovement.com/uploads/product/product_pgSIG6yWb0akqcUhDf.pdf): movement/dial/stem input. Manufacturer PDFs remain external third-party references.
- [Rogers PORON supported 4701-30 data](https://rogerscorp.com/-/media/project/rogerscorp/documents/elastomeric-material-solutions/poron/english/data-sheets/17-037-poron-4701-30-very-soft---supported-materials.pdf): a possible pad material only. The supported 320 density / 0.79 mm variant lists 21–55 kPa at 25% compression. Three diameter-3 pads imply about 0.45–1.17 N at that test point. This is not a complete force curve, watch qualification, preload recommendation or aging/outgassing approval.

The important unresolved risk is precision finishing and the complete assembly, not merely nominal STL watertightness. No print order, machining approval, completed tolerance stack-up, water-resistance rating or physical validation is represented by these files.
