# Run this first: python -m build

import sys, zipfile, pathlib
whl = pathlib.Path("dist").glob("*.whl").__next__()
with zipfile.ZipFile(whl) as z:
    for name in z.namelist():
        if name.startswith("gai/scripts/data/"):
            print(" •", name.removeprefix("gai/scripts/data/"))