# -*- coding: utf-8 -*-
import io, shutil, sys
from pathlib import Path
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
ROOT = Path(r'C:\Users\LZ\Desktop\软工')
for n in ['fix_fignum.py', 'check_report2.py', 'check_shots.py', 'make_app_bat.py']:
    p = ROOT / 'scripts' / n
    if p.exists():
        p.unlink(); print('removed scripts/' + n)
d = ROOT / '_work' / 'rep'
if d.is_dir():
    shutil.rmtree(d); print('removed _work/rep')
f = ROOT / 'library-app' / 'target' / 'sources.txt'
if f.exists():
    f.unlink(); print('removed target/sources.txt')
pc = ROOT / 'scripts' / '__pycache__'
if pc.exists():
    shutil.rmtree(pc); print('removed scripts/__pycache__')
print('scripts:', sorted(p.name for p in (ROOT / 'scripts').iterdir()))
