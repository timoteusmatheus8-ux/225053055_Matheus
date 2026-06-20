import pathlib
import sys
p = pathlib.Path(__file__).resolve().parent.parent / 'assets' / 'certificates'
if not p.exists():
    print('Certificates folder not found:', p)
    sys.exit(1)
removed = []
for f in p.glob('*.pdf'):
    try:
        f.unlink()
        removed.append(f.name)
    except Exception as e:
        print('ERROR', f.name, e)
print('Removed:', removed)
print('Remaining:', [x.name for x in p.iterdir()])
