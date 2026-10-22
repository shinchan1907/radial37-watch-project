# Miyota 2035 adaptation — confirmed component, pending geometry

The owner confirmed Miyota 2035 on 22 October 2026. V3 remains the active design baseline. The archived V3 scene still contains 5Y20 geometry; changing the component record does not make that scene compatible.

## Verified differences

| Interface | Archived 5Y20 basis | Confirmed 2035 basis |
|---|---:|---:|
| Movement body height | 2.54 mm | 3.15 mm |
| Catalog plan envelope | 13 x 15.75 mm | 18.5 x 15.3 mm |
| Stem axis below dial support face | 0.80 mm | 0.85 mm |
| Stem thread nominal diameter | 0.70 mm | 0.90 mm |
| Stem thread pitch | 0.175 mm | 0.225 mm |
| Dial central hole | 1.50 mm | 1.20 mm |
| Dial feet projection | 1.30 mm in V3 | 1.40–1.60 mm on 2035 drawing |
| Dial foot positions, stem +X | (-1.20, -6.85), (-2.08, 6.62) mm | (-7.900, -3.000), (8.234, -1.900) mm |

Both drawings specify a nominal 0.40 mm dial plate and 0.70 mm feet. Catalog dimensions are envelope inputs, not a complete outline or an approved carrier pocket. Hand fitting diameters are nominal; use the manufacturer's actual tolerances and purchased hand specifications for interfaces.

At the old movement-bottom datum Z=1.65 mm, the 2035 dial support face becomes Z=4.80 mm, dial top Z=5.20 mm, and stem axis Z=3.95 mm. This raises the dial by 0.61 mm and stem axis by 0.56 mm. The archived hour-hand envelope at Z=5.04 mm would intersect a dial raised this way; the whole hand stack must be repositioned and checked. The old 0.70 mm stem placeholder also under-represents the 2035's 0.90 mm threaded end.

The standard 2035 is a three-hand movement. Retaining two-hand styling requires keeping the seconds arbor's physical envelope and confirming the actual hand fitting; do not delete the arbor from clearance analysis simply because no seconds hand is pictured. The casing drawing places its nominal top 1.60 mm above the dial-support face, or Z=6.40 mm at this comparison datum. The actual purchased movement/hand-height version and fitted hand geometry still control final clearance.

## Adaptation work

1. Replace the 5Y20 proxy using the 2035 drawing and a measured sample; preserve the supported perimeter, battery and stem-release access.
2. Redesign the carrier rather than scaling the old pocket. Check chapter interference around the larger movement, support and antirotation.
3. Update dial feet, center bore and retention using the new drawing. A 1.20 mm hole is a nominal component requirement, not a guaranteed as-printed hole size.
4. Reposition stem/crown/tube and hands; check all setting positions and the complete rotational hand sweep against chapter and crystal.
5. Decide the closure, then resolve back support and the complete tolerance stack before final export.

No geometry adaptation or manufacturing approval is claimed by this record. Live scene editing is pending restoration of the existing Blender MCP connection, which still refused connections after the owner reported starting it. Component research and repository documentation proceeded independently.

Sources: [Miyota product page](https://miyotamovement.com/product/2035/), [three-page manufacturer drawing](https://miyotamovement.com/uploads/product/product_4tdsbpNVQi1WcE5lUw.pdf), [manufacturer specification](https://miyotamovement.com/uploads/product/product_pgSIG6yWb0akqcUhDf.pdf), checked 22 October 2026. Manufacturer PDFs are referenced by URL and not redistributed under the project licence.
