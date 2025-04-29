import os
from rich.console import Console
console=Console()
from gai.scripts._scripts_utils import _publish_package
import subprocess

def publish_sdk(proj_path):
    try:
        console.print(f"[yellow] publishing from project path {proj_path}[/]")
        _publish_package(proj_path)
    except subprocess.CalledProcessError as e:
        print("An error occurred while publishing package:", e)
        
import sys, zipfile, pathlib
whl = pathlib.Path("dist").glob("*.whl").__next__()
with zipfile.ZipFile(whl) as z:
    for name in z.namelist():
        if name.startswith("gai/scripts/data/"):
            print(" •", name.removeprefix("gai/scripts/data/"))