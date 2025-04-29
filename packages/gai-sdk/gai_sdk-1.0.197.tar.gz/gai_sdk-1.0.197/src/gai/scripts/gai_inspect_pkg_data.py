# Run this first: python -m build

def inspect_pkg_data():
    import sys, zipfile, pathlib
    whl = pathlib.Path("dist").glob("*.whl").__next__()
    with zipfile.ZipFile(whl) as z:
        for name in z.namelist():
            if name.startswith("gai/scripts/data/"):
                print(" •", name.removeprefix("gai/scripts/data/"))
                
if __name__ == "__main__":
    inspect_pkg_data()