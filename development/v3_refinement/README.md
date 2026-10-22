# V3 refinement workspace

Base: `project/radial37_v3/radial37_v3.blend` (original preserved).

Do not treat recovered exports as manufacturing-approved parts. The current case/back topology and component interfaces are unresolved. New scripts and native scenes in this folder must state their starting revision and validation status. Movement and closure choices are pending owner reconciliation; export recovery is independent of those choices.

## Export recovery started

Four review STLs have now been recovered directly from the saved V3 scene: current chapter, center dial, polymer carrier and the historical machining-stock back. Independent reimport confirms nonempty geometry and zero non-manifold edges for all four. Each source part is one connected component with positive signed volume. This resolves export availability only, not printability or interface fit. The case, threaded back and case stock are rejected by the geometry gate and have no new STL.

See `export_recovery_report.json` for original-source hash, per-part checks and recovered-file hashes; `reimport_audit.json` for independent saved-file checks. The exporter bypasses object-selection/visibility dependence. Run it against the original V3 file in background Blender; it never saves over that file.

Live Blender MCP at localhost:9876 was unreachable during this review. Background inspection/recovery used Blender 5.2.2 LTS in separate processes; no live scene was edited. Movement and closure decisions are pending owner reconciliation before interface redesign.

## Movement confirmed

The owner selected Miyota 2035 on 22 October 2026. See [the adaptation record](MIYOTA_2035_ADAPTATION.md) and machine-readable component inputs. Original V3 geometry is still 5Y20-based. Closure remains pending; live connector remains unreachable after reported startup.
