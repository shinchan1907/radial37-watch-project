# Saved candidate results

Quote review only; no manufacturing release. Six native single solids and six watertight, positive-volume single-body STL files passed saved-file checks. All 29 sampled nominal motion poses and ten component envelope pairs were clear. Every finished solid is contained within its corresponding stock. Forbidden reverse/overturn/pull controls produce overlap, as intended.

| Stock | Minimum sampled wall (mm) | Fifth percentile (mm) | Valid samples | Down-facing area at 45° (mm²) |
|---|---:|---:|---:|---:|
| case | 2.293 | 3.997 | 6000 | 153.29 |
| back | 2.300 | 2.300 | 2068 | 0.00 |
| dial | 2.386 | 2.388 | 964 | 0.00 |

These sampled stock measurements exceed JLC3DP's published >1.5 mm wall recommendation. The tool requests 6000 samples but caps sampling for meshes with fewer facets; actual counts are reported above. This is not an exhaustive local-thickness guarantee. PCBWay's numerical minimum wall has not been independently verified.

For the case, the flat and flipped orientations are about 5.6% support area, versus about 11.5–16.4% on its side; flat build height 6.9 mm versus 37.8–44.8 mm on its side. Neither flip gives a material improvement. Back and dial current-orientation estimates are zero by the geometric heuristic, which excludes plate-contact faces; metal anchoring/support/thermal planning still belongs to the supplier. The thin finished dial is intentionally not a print file.

Hash binding is in summary.json and saved_artifact_checks.json. No supplier review, selected-component fit test, complete tolerance/strength assessment, physical retention/wear testing or water-resistance qualification has been completed.
