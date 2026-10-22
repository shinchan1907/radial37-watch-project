"""Verify original archive hashes without requiring private reference assets.

Usage: python tools/verify_archive.py [repository_root] [--require-references]
"""
import hashlib,json,sys
from pathlib import Path

root=Path(sys.argv[1]) if len(sys.argv)>1 and not sys.argv[1].startswith('--') else Path(__file__).resolve().parents[1]
require_refs='--require-references' in sys.argv
entries=json.loads((root/'MANIFEST.json').read_text(encoding='utf-8'))
passed=[];omitted=[];failed=[]
for entry in entries:
    rel=entry['path'];p=root/rel
    reference=(rel.startswith('references/') and rel.endswith('.png')) or (rel.startswith('project/radial37_v3/reference/') and rel.endswith('.pdf'))
    if not p.exists() and reference and not require_refs:
        omitted.append(rel);continue
    if not p.exists() or p.stat().st_size!=entry['bytes'] or hashlib.sha256(p.read_bytes()).hexdigest()!=entry['sha256']:
        failed.append(rel)
    else:passed.append(rel)
print(json.dumps({'passed':len(passed),'omitted_third_party_references':omitted,'failed':failed,'ok':not failed},indent=2))
sys.exit(bool(failed))
