# Radial37 — V3 titanium bayonet candidate 02

**QUOTE REVIEW ONLY — NOT RELEASED FOR ORDER.** Updated 22 October 2026.

The owner selected Miyota 2035, a quarter-turn bayonet back, supplier precision finishing, and exactly three titanium prints: case, back and a **single-piece dial**. The archived V3 files are preserved. This is a new CAD candidate derived from that design intent, not a claim that the old invalid case has been repaired.

![Current appearance study](preview.png)

The 37 mm case has tapered, curved vintage-style lugs with rounded tips, bevels and machined strap-pin holes. The dial uses 16 broad curved webs in place of the archived 60 fine webs. Its outer rail is machined to 0.85 mm and its continuous center to 0.40 mm. “Indo / Constantin” and the hour indices are laser-marking artwork, not raised printed letters. Glass, hands and crown in the preview remain provisional component envelopes.

## What to review

- [Manufacturing dimensions, operations and holds](MANUFACTURING_REVIEW.md)
- [Prepared supplier quote request](QUOTE_REQUEST.txt) — not sent
- [BOM and component holds](BOM.md)
- [Assembly sequence](ASSEMBLY.md)
- [Validation and supplier sources](validation/README.md)
- [Design contract](DESIGN_CONTRACT.json)

`STL_PRINT_STOCK/` contains the **three thick machining preforms**, in millimetres. Matching native CAD is in `STEP/*_PRINT_STOCK.step`. Do not print the thin `FINISHED_REFERENCE` files. Those files are target geometry for quoting precision finishing. Stock and finished parts share the same coordinate system; the back is rotated 90 degrees only in the assembly STEP.

The single-piece dial is feasible here only as a proposed **print plus extensive precision machining** route. Its print preform has flat faces, thick webs and an unpierced center. The supplier must quote machining the wave faces, thin center, integral feet, bore and outer rail. Cost and access have not been approved. No insert, attached dial feet or extra titanium part is silently substituted.

The native `.blend` preserves earlier scenes and opens the new appearance study. CAD, not the presentation mesh/materials, defines the quote geometry. `src/assemble_blender.py` contains staged scene operations that require the previous fit-study scene and are not an idempotent standalone build. The laser SVG is editable outline artwork with an OFL font license in `assets/`.

## Rebuild and verify

Use a dedicated Python 3.11+ environment and `requirements.txt`. Cadgen and CadQuery share OCP; if the no-VTK distribution shadows the full one, reinstall `cadquery-ocp==7.9.3.1.1` last. Tested with the full OCP package and VTK 9.6.2. Commands from this directory:

```powershell
python src/titanium_design.py
python src/check_saved_artifacts.py
```

Run the generator without a model-name argument. It exports six valid native solids and an assembly, then conforms STL edge subdivisions without filling holes. Raw tessellations and caches are in the ignored `build/` directory. The independent checker reopens the saved STEP/STL, checks stock containment and sampled nominal motion/component interference, and writes hashes. A failure must block publication of an updated quote packet.

Use the installed text-to-cad DfAM skill's `dfam_tool.py measure` with 6000 samples and 45 degrees on each exact stock STL, followed by `orientations`. These sampled reports do not certify every wall or supplier acceptance.

Actual crystal, seals, tube/crown, hands and spring bars must be selected and measured; the CAD must then be rechecked. Supplier finishing capability, tolerances, supports, cost and inspection plan require written acceptance. A physical fit and bayonet retention/wear prototype is still required. Water resistance is unqualified.
