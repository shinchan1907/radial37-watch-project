# Radial 37 — complete project review

Review date: 22 October 2026. Active baseline: **V3**, explicitly selected by the owner during this review. Product direction: an affordable, feasible, classy watch that people enjoy wearing, developed publicly as open hardware.

## What I understand

The watch's identity comes from a quiet central medallion surrounded by a deep, sculpted radial chapter, a domed crystal, a small rounded case and curved lugs. It is a quartz watch: the peripheral arches are decorative geometry, not movement components. The design should remain visually distinctive while becoming practical to buy parts for, assemble, service and reproduce.

The central challenge is fitting the radial relief, dial support, hands, movement, stem, crystal and removable back into a small case without losing visual depth or producing fragile, expensive parts. A mesh that looks attractive or passes a closed-surface test does not establish those interfaces.

V3 is the correct continuation point because it contains the newer internal arrangement. V2 remains useful for appearance comparison, not as a replacement baseline. The earlier ATELIER 37 brief and its different dimensions must not silently override this archive.

## Evidence and scope

Read all nine Python files, every project note and JSON report, the archive manifest, and the reference source list. Opened all three native Blender files in separate background processes with automatic execution disabled. Independently inspected all 13 saved STLs, reviewed a contact sheet of all 18 supplied references and four project renders, and rendered/read the three-page 5Y20 drawing and specification.

All 58 files listed in `MANIFEST.json` matched their original sizes and SHA-256 hashes: 46,529,573 bytes in total, excluding the manifest itself. Original source and geometry were not modified for the analysis. There are 18 reference PNGs but 15 unique image hashes.

Audit evidence is in `analysis/archive_audit.json`, `analysis/stl_audit.json`, and `analysis/v1_audit.json` through `v3_audit.json`. The STL audit uses Blender import plus a 0.00001 mm vertex merge. Blender removes some duplicate/degenerate triangles on import; its resulting edge counts therefore differ from native scene counts. These are topology inspections, not comprehensive self-intersection, minimum-wall, strength, tolerance or manufacturing certification.

## Version history

| Version | What exists | Interpretation |
|---|---|---|
| V1 | Proportion model, simple dial, case/back studies, cadgen sketches | Early styling; radial pattern is a shader rather than printable ribs. Saved case STL has three non-manifold edges after current import cleanup despite the historical clean source report. |
| V2 | Actual 60-web dial, 12 stronger hour webs, curved lugs, crown, hands, straps and renders | Strong appearance reference. Its three exported parts have zero non-manifold edges in this audit. Movement is not fitted; screw-back mating and sealing are incomplete. |
| V3 | Thinner case, separate brass center, chapter, movement proxy, polymer carrier, stem/hand envelopes, crystal/gaskets, threaded back and stock concepts | Active baseline. More complete assembly intent, but unresolved closure decision, invalid case/back topology, empty exports and unsynchronized validation prevent release. |

## V3 assembly and dimensions

The current numerical coordinate convention is millimetres, with the dial in XY and watch thickness along Z. Stem/crown extend towards +X (3 o'clock). The case nominal outside diameter is 37 mm, lug span 44 mm, strap gap 18 mm. Case STL measures about 36.9947 mm across X because of tessellation; this is not a new target diameter.

The stack in `parameters.py` is:

| Feature | Nominal value |
|---|---:|
| Back floor thickness | 0.90 mm |
| Movement bottom | Z 1.65 mm |
| Movement body height | 2.54 mm |
| Movement face | Z 4.19 mm |
| Brass center thickness | 0.40 mm |
| Dial top | Z 4.59 mm |
| Stem axis | Z 3.39 mm |
| Metal top | Z 4.85 mm |
| Crystal nominal diameter | 33.00 mm |
| Crystal apex | Z 8.15 mm |

The V3 finished-back reference starts nominally at Z=0, so the proposed overall stack is around 8.15 mm, subject to exact components and assembly. The case mesh's 4.181 mm Z bounding box is not assembled watch thickness. V2's earlier overall envelope was about 9.35 mm.

The 5Y20 is a two-hand movement, and the manufacturer's current page confirms a 2.54 mm body height. V3 models a conservative clipped envelope, approximately 13 x 15.75 x 2.54 mm, rather than complete purchased-part CAD. The manufacturer dial drawing shows a 0.40 mm plate, 1.50 mm central hole and 0.70 mm dial feet. V3's plate follows that construction intent. Its STL measures 1.70 mm in total because the feet extend 1.30 mm below the 0.40 mm plate; this is not evidence of an accidentally 1.70 mm-thick plate.

The owner reconfirmed Miyota 2035 on 22 October 2026. V3's archived 5Y20 architecture must be adapted to that selection; movements are not drop-in interchangeable. Hands, stem, crown, carrier and dial interfaces depend on the choice. Current appearance hands are not approved purchased parts.

## What V3 already solves at study level

- Separates the thin dial center from the sculpted metal chapter, avoiding V2's thick solid medallion as a conventional dial.
- Allocates a compact movement and polymer carrier below the central portion, leaving peripheral volume for the arches.
- Includes stem-axis, stem travel/clearance and rotating-hand envelopes, plus nominal collision checks for seven part pairs.
- Includes back and crystal gasket envelopes, a crown tube and removable-back concepts.
- Centralizes several stack parameters in `parameters.py` and preserves an editable native scene.

These are valuable engineering studies. They still require actual purchased components and consistent tolerances.

## Confirmed problems

### 1. Export integrity

Three V3 files contain only the 84-byte binary STL header and zero triangles:

- `carrier_POLYMER_fit.stl`
- `case_PRINT_STOCK_HOLD.stl`
- `back_PRINT_STOCK_HOLD.stl`

The native scene contains nonempty corresponding objects. The historical geometry report describes scene objects, so its positive volumes cannot validate these saved files. Export validation must inspect the file written to disk and reject empty geometry. The precise reason for these empty historical exports is not established by this audit.

### 2. Case and back topology

The V3 native case has 809 non-manifold edges and the threaded back 24,670. Reimported STLs remain invalid even after Blender's import cleanup: case 791 non-manifold edges, back 334. The importer removes 15,289 duplicate back triangles; those removed triangles explain why the two counts should not be directly compared. This is not a successful repair.

The V3 chapter and center-dial STLs have zero non-manifold edges in this audit. The chapter's archived export is described as predating the latest source/scene changes, so a clean mesh does not establish revision consistency.

### 3. Closure architecture

V3 contains a fine helical back connection: nominal pitch 0.50 mm, radial thread gap 0.10 mm and roughly 1.10 mm engagement height. It does not contain a quarter-turn bayonet. The later archive brief requests a print-only bayonet and supersedes the earlier fine-thread/machining assumptions. The owner has now selected V3 as baseline; the intended closure still needs explicit reconciliation before changing its design.

A bayonet requires mating tabs, entry slots, retention tracks, end stops, resistance to unintended unlocking, controlled gasket compression and an insertion/rotation clearance check. Renaming the existing thread cannot implement it. Keeping the threaded option instead requires a deliberate manufacturing/tolerance plan.

### 4. Metal-print feasibility

Minute rib width is 0.62 mm; V3 nominal rib thickness is 0.75 mm. These fall below JLC's general SLM wall guidance of 1.5 mm for small parts. The V3 back floor is also 0.90 mm. The guideline is a general screening constraint, not a proof that every individual feature will fail or that a thicker design automatically passes.

JLC currently lists general SLM model tolerance of +/-0.3 mm, hole tolerance of +/-0.5 mm, and assembly clearance guidance of 0.5 mm, with structure-specific caveats. These figures make the fine thread's 0.10 mm radial gap and precise seal/shaft bores unsuitable to assume valid as printed. Supplier-specific review and fit coupons are needed. Polishing/support removal can also change delicate ribs and fit surfaces. A print-only precision wearable remains unproven.

### 5. Incomplete component and optical definition

V2 uses a provisional low-dome sapphire envelope. V3 changes to a higher acrylic dome with a provisional inner profile. They are not interchangeable seats or equivalent optical appearances. Both scenes hide the crystal from the main geometry review, so those views do not establish how the assembled watch will look through it.

The supplied inspiration relies on deep arches and, according to the archive notes, high-domed acrylic magnification. A final render needs the actual crystal material/profile, along with proper glare and viewing-angle checks. The inspiration author's page timed out during this review; historical claims from the local notes were not independently reconfirmed.

Exact crystal/gasket fits, crown/tube sealing, stem retention and setting travel, spring-bar holes, hand heights and torque/loading, dial mounting, movement retention, battery removal and assembly access remain incomplete. A nominal zero-overlap test does not establish required running clearance, rotational clearance or worst-case tolerances. No water-resistance rating has been demonstrated.

### 6. Build and release consistency

There are duplicate hard-coded dimensions alongside imported parameters. Rebuild scripts also write scenes and reports directly beside archived outputs. The clearance-check JSON is not generated by the same source pipeline and still says closure clarification is pending. A current script syntax pass is not a successful full rebuild.

No STEP model, dimensioned manufacturing drawing, released tolerance table, supplier-approved process plan, priced bill of materials, assembly instructions or physical fit-test record is present. Native Blender models and STL surfaces are editable, but they do not substitute for those release artifacts.

## Design interpretation for the next revision

Keep V3's small case, curved lugs, thin center and radial depth. Refine the design around a real stack of purchasable components. Make the hour positions and hands easy to read at normal wrist distance. Evaluate the crown against the case size, soften wrist-contact edges, and check lug curvature and strap articulation on several wrist sizes.

Affordability must cover the complete delivered watch: movement, hands, stem/crown/tube, crystal, seals, spring bars, strap, printed parts, finishing, assembly, shipping, failures and service. Stainless steel versus titanium is an open tradeoff, not a cost conclusion from this archive. A monetary target and production quantity are not yet specified.

My recommendation is to preserve V3 as the design foundation, restore trustworthy exports first, then resolve components and closure before spending effort on final cosmetics. Develop and test the smallest difficult interfaces as coupons. The first release should be an honestly labelled fit prototype; a metal-order release should follow successful validation and supplier acceptance.

## Primary reference links

- [Miyota 5Y20 product, specification and drawings](https://miyotamovement.com/product/5Y20/) — checked 22 October 2026.
- [JLC3DP design guideline](https://jlc3dp.com/help/article/3d-printing-design-guideline) — checked 22 October 2026; page dated 24 August 2026. Process guidance is not an approval of this project.
- [Carter Hurd watch inspiration](https://altapowderdog.wixsite.com/my-site/watches) — archive attribution; page fetch timed out during this review.

## First V3 refinement action completed

Export recovery is recorded in `development/v3_refinement/`: four nonempty, topology-clean review exports from the saved V3 scene, including the formerly empty carrier and historical back-stock export. The source chapter is exported afresh rather than relying on its stale archived STL. Independent reimport passed all four. The case, threaded back and case-stock meshes are deliberately rejected by the export gate. No original geometry changed and none of these files is released for manufacturing.

## Confirmed movement decision

The owner confirmed Miyota 2035. Verified manufacturer inputs and adaptation implications are recorded in `development/v3_refinement/MIYOTA_2035_ADAPTATION.md`. V3 remains the baseline; its geometry is not yet converted to the new movement. The closure choice remains pending.

## Subsequent V3 refinement checkpoint

The live MCP connection is restored and a separate V3/2035 fit study now exists. It contains a new movement envelope, carrier and dial proposal, repositioned appearance hands/stem/crown and a shorter minute-hand option. Five new meshes pass topology/component checks, four nominal collision checks pass, and the assumed dome yields approximately 0.36 mm minimum vertical minute-hand clearance. Two review STLs independently reimport cleanly. This is partial adaptation: the copied case/back remain invalid and the case stem bore remains 0.56 mm low. See `development/v3_refinement/FIT_STUDY_01.md`.
