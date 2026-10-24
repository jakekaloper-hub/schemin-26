"""Load sibling standalone archivist module without changing package names."""
import importlib.util
from pathlib import Path

def load_archivist():
    path=Path(__file__).resolve().parents[1]/"engine"/"commonwealth_archivist.py"
    spec=importlib.util.spec_from_file_location("commonwealth_archivist",path)
    module=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.build
