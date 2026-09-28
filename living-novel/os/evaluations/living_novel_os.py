import importlib.util
import sys
from pathlib import Path
p=Path(__file__).parents[1]/"engine"/"novel_os.py"
s=importlib.util.spec_from_file_location("novel_os",p)
m=importlib.util.module_from_spec(s)
sys.modules[s.name]=m
s.loader.exec_module(m)
for k,v in vars(m).items():
    if not k.startswith("_"): globals()[k]=v
