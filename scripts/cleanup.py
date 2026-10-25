# -*- coding: utf-8 -*-
import io, shutil, sys
from pathlib import Path
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
S = Path(r'C:\Users\LZ\Desktop\软工\scripts')
drop = ['diag_quotes.py', 'fix_quotes.py', 'fix_quotes2.py', 'fix_quotes3.py',
        'inspect_cover.py', 'inspect_tpl.py', 'inspect_tpl2.py',
        'prepare_convert.py', 'final_check.py']
for n in drop:
    p = S / n
    if p.exists():
        p.unlink()
        print('removed', n)
pc = S / '__pycache__'
if pc.exists():
    shutil.rmtree(pc)
    print('removed __pycache__')
print('remaining:', sorted(p.name for p in S.iterdir()))
