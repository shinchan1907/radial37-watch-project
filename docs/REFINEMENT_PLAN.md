# V3 refinement plan

V3 is the owner-selected working baseline, 22 October 2026. Preserve its radial design and compact proportions. Keep original files unchanged as the historical checkpoint; new work belongs in `development/v3_refinement/`.

## Decisions to reconcile

1. Movement: V3 uses 5Y20; earlier chat approved 2035. Confirm before modifying movement-dependent interfaces.
2. Closure: V3 has a thread; the later archive requests a bayonet. Confirm the architecture before changing the back.
3. Exact crystal, hand set, crown/tube, gasket and strap/spring bars: choose actual parts and obtain drawings or measurements.
4. Target delivered cost, quantity, material/finish and acceptable post-processing: these define feasibility. The archive requests print-only, but that route is not yet validated.

## Work sequence and acceptance

| Stage | Work | Evidence required |
|---|---|---|
| A — preserve and audit | Capture original hashes, scenes, file checks and current failures | Completed in `analysis/`; no original geometry changed |
| B — restore exports | Regenerate nonempty files from the saved V3 scene, isolate latest chapter and carrier, fail on invalid meshes | Per-file triangle count, units, dimensions, connected components, signed volume, topology and independent reimport |
| C — lock real stack | Reconcile movement; acquire exact component dimensions and model interfaces | Component table, source drawings, stack section, tolerance budget, assembly sequence |
| D — closure | Develop the selected back connection and gasket system | Insertion, locking/setting travel, anti-unlock, tool access, worst-case fit and serviceability checks |
| E — process-aware geometry | Correct case/back topology; redesign fine chapter, holes, seals and supports as needed | Material/process-specific minimum features, support/finishing access and supplier review |
| F — fit prototypes | Print inexpensive assembly mock-ups and dedicated closure/crystal/crown coupons | Measured dimensions, assembly feedback, controlled revision and fit results; plastic fit does not prove metal accuracy |
| G — metal prototype | Produce a supplier-accepted prototype and finish it using the agreed process | Inspection, secure movement/strap retention, hand clearance, comfortable edges and repeatable opening/closing |
| H — release | Synchronize native source, meshes, drawings, BOM and instructions | Every release gate passes; no water-resistance claim without appropriate testing |

## Release rules

- No empty or non-manifold manufacturing exports; zero count alone is insufficient. Also inspect intersections, thickness, normals, component count and tolerances.
- Keep appearance-only objects and purchased-part proxies separate from printable parts.
- Include the actual crystal in assembled visual review; verify side profile and wrist readability.
- Avoid generated file names that imply approval before release.
- Record source revision and hashes in every geometry/clearance report; do not mix reports from different builds.
- Document the bill of materials with exact part identity, quantity and measured/source dimensions. Add dated prices only when researched.
- Preserve the original archive and third-party attribution. Never silently overwrite a prior checkpoint.

## Current status

Analysis and independent audit are complete. The public repository begins as a development archive, not a print release. Export recovery can proceed independently of the open movement and closure decisions. Final interface design depends on those decisions and exact component data.
