# Titanium quote review — candidate 02

**NOT AN ORDER RELEASE. All dimensions are millimetres.** The user accepts supplier finishing and requires a monolithic titanium dial. Material proposal: TC4 / Ti-6Al-4V, SLM/metal PBF, supplier certificate requested.

## Stock versus finished geometry

| Part | Print preform | Finished target / machining |
|---|---|---|
| Case | OD 37.8, open bore 29.6; substantial lug stock; no tiny holes or bayonet cuts | OD 37, approximately 44 lug-to-lug; machine all internal steps, seal gland, bayonet slots/pockets, crown bore and pin holes; finish outside/bevels |
| Back | OD 37.4; floor 2.3 thick; continuous 3.0 radial ring; support boss stock | OD 36.6; floor 1.5; spigot OD 32 / ID 29.6; three tabs to radius 16.65; machine underside spanner sockets and support boss |
| One-piece dial | OD 32.2, Z 3.5–7.2; flat 3.7-thick preform; 16 webs about 2.8 wide, core radius 10; outer ring radial width 2.4 | OD 31.4; 16 curved webs about 2.0 wide; center radius 9.6 with 0.40 thickness; machine integral feet, center hole, stem clearance, locating notch and 0.85 outer rail |

Stock containment is checked against all finished solids. It is not an uncertainty simulation. Supplier must confirm allowance remains sufficient after its actual distortion/undersize, support removal, stress relief and fixturing. Dial slot access and small open-slot powder/support cleanup require explicit review. No unsupported fine detail is to be accepted on the basis of a render.

## Interfaces and datums for review

Shared axis is Z; stem is +X; 12 o'clock is +Y; back underside is Z0. Proposed finishing datum is the central axis plus the back seating plane and a 12 o'clock angular datum. Supplier must establish a practical fixturing/inspection scheme before a drawing is released.

- Case underside Z1.6; top Z7.7. Rear loading bore radius 16.2 to Z5.3. Dial locating pocket radius 15.9 to Z6.4. Retaining bezel opening radius 15.35. Crystal pocket radius 16.8 starts Z6.8.
- Lug gap 18.2 for a nominal 18 mm strap; pin-hole target diameter 1.0, axes along X at Y ±20 and Z3.25. Hole diameter/depth and bar compression must be finalized with the selected bars. Rounded lug cross sections R0.55 and tip fillet R0.30 are modeled; final blending must preserve fits.
- Bayonet: three tabs at 15 + 120n degrees in the insertion orientation, each 11 degrees wide; 90-degree closure, 0.10 axial push before reverse release. Track Z3.0–4.0; terminal pocket Z2.9–4.0; tab Z2.9–3.7. Nominal spigot and track radial clearance 0.20. Stop and retention overlaps are intentional outside the permitted motion sequence.
- Seal gland radial range 16.6–18.0; floor Z2.33, opening Z1.60; nominal depth 0.73. Back top mating plane Z1.50 gives 0.10 face gap and 0.83 gland height when locked. During release gland height 0.73. Candidate installed seal cross section 1.00; compound, actual CS, stretch, compression force and surface finish are unresolved.
- Movement bottom Z3.05, dial seating face Z6.20; 2035 body height 3.15. Stem center Z5.35. Dial center top Z6.60, nominal center hole diameter 1.20. Integral feet diameter 0.70 at XY (-7.9,-3.0), (8.234,-1.9), projection 1.50. Verify actual movement and official drawing before machining.
- Dial outer rail underside Z5.55/top Z6.40. Rear-load dial and movement; bezel prevents upward escape. Holder antirotation key seats in case recess. Back support boss top Z1.70; holder underside Z2.30 gives a 0.60 locked / 0.50 pushed gap for qualified compliant pads. This is a proposed preload system, not a validated retainer.
- Crown hole nominal diameter 1.80 and internal stem passage 1.30 are placeholders until the purchased tube/crown are defined. Do not machine an assumed press fit.
- Crystal envelope only: nominal diameter 33, seating base Z6.80, rim top Z7.75, exterior dome apex Z9.55, interior apex Z8.55. No actual purchased crystal is yet matched. Complete watch height is therefore provisional; it is not just case wall height.

## Requested finishing capability — not agreed tolerances

| Feature | Quote request / review target |
|---|---|
| Spigot, track and dial locating radii | ±0.025 per radius; 0.20 nominal clearance gives 0.15–0.25 radial clearance under these assumptions |
| Bayonet axial levels | ±0.02 each; 0.10 nominal drop gives 0.06–0.14 before other effects |
| Seal groove depth / locked mating gap | ±0.01 / ±0.015; request flatness, runout and roughness recommendations with measurement method |
| Dial center | 0.40 ±0.02 requested; machine flat without distortion; inspect against hand stack and feet seating |
| Dial hole, feet, pin holes, tube and crystal seat | Per actual component drawings and agreed fits; supplier must propose achievable tolerances and inspection |
| Seals and sliding fits | Supplier to recommend finished roughness, burr removal and dimensional change from finishing/coatings |

The tolerance budget in `validation/saved_artifact_checks.json` is partial and assumption-based. It does not include every positional tolerance, distortion, seal force, hand setting variation, crystal installation, coating or thermal effect. It must not be treated as a complete stack-up or GD&T drawing.

Request broad satin titanium faces and restrained polished bevels. Laser mark the supplied text after final face finishing; agree contrast, stroke readability and depth so the 0.40 center is preserved. Twelve narrow hour indices are artwork only. Ti-on-Ti bayonet sliding requires a supplier-approved surface/lubrication strategy and physical cycling/galling tests. Do not silently coat a precision surface without revising its fit.

## Release holds

1. Identify and inspect actual crystal/gasket, crown/tube, hands, seals, spring bars and movement variant; revise geometry to their data.
2. Supplier accepts all machining access, three-piece production, print allowances, minimum features, supports, tolerances, finish and itemized price. The extensive dial machining may dominate cost.
3. Complete detailed dimensioned drawings, tolerance/structural and retention review; finish-machined thin titanium features require separate strength/handling evaluation.
4. Prototype the assembly; measure fit, pin engagement, hand/crystal clearance, pad preload, bayonet release/pull strength, accidental opening, galling and repeated wear. Pressure test only after a water-resistance specification is agreed.

Neither supplier has approved this candidate. No order or supplier message has been sent.
