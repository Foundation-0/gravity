"""Read-only checks for the reconciled documentation and frozen numerical tree."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess

parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('checkout', type=Path, help='Path to the reconciled gravity checkout')
parser.add_argument('--output-dir', type=Path, default=Path(__file__).resolve().parent)
args=parser.parse_args()
root=args.checkout.resolve()
out=args.output_dir.resolve()
out.mkdir(parents=True, exist_ok=True)
files=['CHANGELOG.md','METHODS_AND_PLAYBOOK.md','RESEARCH_NOTEBOOK_AND_REASONING.md','SHA256SUMS','research/wave11-12-review-20261112/README.md']
frozen=['wave11_machian_pairing_unification.py','wave12_cosmic_dawn_quasar_collapse.py','results/wave11_machian_pairing_certificates.json','results/wave12_cosmic_dawn_quasar_certificates.json','test_wave11_12_corrections.py','WAVE11_12_CORRECTIONS.md','research/wave11-12-review-20261112/REVIEW.md','research/wave11-12-review-20261112/check.py','research/wave11-12-review-20261112/checkpoint.json','research/wave11-12-review-20261112/evidence.json']
for name in frozen:
    assert (root/name).read_bytes()==subprocess.check_output(['git','show','03f96e977c1852930c85d7568aff087e093e4d50:'+name],cwd=root),name
for name in files:
    assert all(marker not in (root/name).read_text() for marker in ('<<<<<<<','=======','>>>>>>>')),name
methods=(root/'METHODS_AND_PLAYBOOK.md').read_text()
for name in ['wave11_machian_pairing_certificates.json','wave12_cosmic_dawn_quasar_certificates.json']:
    assert json.loads((root/'results'/name).read_text())['sha256_canonical'] in methods
notebook=(root/'RESEARCH_NOTEBOOK_AND_REASONING.md').read_text().split('## 5.',1)[1]
for value in ('200.08','121.72','127.16','273.78','161.23','451.54','396.22'):
    assert value in notebook,value
for obsolete in ('109.04','122.79','165-276','Braun','solving pure baryon','matching the canonical'):
    assert obsolete not in notebook,obsolete
changelog=(root/'CHANGELOG.md').read_text()
assert changelog.count('## Wave 12 --')==1
assert changelog.count('## Wave 11 --')==1
assert 'quadrature`formal/' not in changelog
assert 'Claim identifiers currently run from `C-01` through `C-33`.' in changelog
assert 'reconciled in Wave 8' not in changelog
assert 'Manuel Urueña Palomo' in changelog
wrapper=(root/'research/wave11-12-review-20261112/README.md').read_text()
assert 'git worktree add --detach' in wrapper and 'e5d7ee813e33de03c91857e48a2d55a0caf55506' in wrapper
entries={name:digest for digest,name in (line.split('  ',1) for line in (root/'SHA256SUMS').read_text().splitlines())}
for name in files:
    if name!='SHA256SUMS':assert entries[name]==hashlib.sha256((root/name).read_bytes()).hexdigest(),name
all_mismatches=[n for n,d in entries.items() if hashlib.sha256((root/n).read_bytes()).hexdigest()!=d]
manifest={n:hashlib.sha256((root/n).read_bytes()).hexdigest() for n in files+frozen}
(out/'tree-hashes.json').write_text(json.dumps(manifest,indent=2)+'\n')
(out/'checks.json').write_text(json.dumps({'frozen_files_unchanged':len(frozen),'changed_file_hashes_pass':4,'certificate_checksum_table_pass':2,'doc_consistency_pass':True,'full_manifest_mismatches':all_mismatches},indent=2)+'\n')
s=subprocess.check_output(['git','diff','03f96e977c1852930c85d7568aff087e093e4d50','--unified=0','--']+files,cwd=root,text=True)
(out/'added-prose.md').write_text('\n\n'.join(l[1:] for l in s.splitlines() if l.startswith('+') and not l.startswith('+++'))+'\n')
(out/'review.diff').write_text(subprocess.check_output(['git','diff','03f96e977c1852930c85d7568aff087e093e4d50','--']+files,cwd=root,text=True))
print('Documentation, checksum table, changed hashes and ten frozen files pass.')
print('Unrelated manifest mismatch count:',len(all_mismatches))
