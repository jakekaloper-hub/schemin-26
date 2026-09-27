import importlib.util
from pathlib import Path
p=Path(__file__).parents[1]/"engine"/"novel_os.py"
s=importlib.util.spec_from_file_location("novel_os",p); m=importlib.util.module_from_spec(s); s.loader.exec_module(m)
for k,v in vars(m).items():
    if not k.startswith("_"): globals()[k]=v
