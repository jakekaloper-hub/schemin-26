"""Repeatable local Atlas pipeline. Rebuild manifest/catalog and run tests.
Use --unreal only when Editor is closed; do not race the live editor.
"""
import argparse,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent
ENGINE=Path("/Users/jakekaloper/Desktop/Desktop - Jake’s MacBook Pro/UE_5.8/Engine/Binaries/Mac/UnrealEditor-Cmd")
def run(args):
 print("RUN",*map(str,args),flush=True)
 subprocess.run(args,cwd=ROOT,check=True)
def main():
 p=argparse.ArgumentParser()
 p.add_argument("--unreal",action="store_true")
 a=p.parse_args()
 for module in ("ScheminBridge.build_world_manifest","ScheminBridge.build_preview_catalog"):
  if module.endswith("build_preview_catalog"):continue
  run([sys.executable,"-m",module])
 run([sys.executable,"-m","ScheminBridge.build_environment_specs"])
 run([sys.executable,"-m","unittest","discover","-s","ScheminBridge/tests","-v"])
 if a.unreal:
  if not ENGINE.exists():raise SystemExit("Unreal commandlet missing")
  run([str(ENGINE),str(ROOT/"Schemin_UE_Prototype.uproject"),"-run=pythonscript",
       "-script="+str(ROOT/"ScheminBridge/unreal_build_atlas.py"),"-unattended","-nosplash","-nullrhi"])
 run([sys.executable,"-m","ScheminBridge.build_preview_catalog"])
 print("ATLAS_PIPELINE_PASS; previews only, no publication or canonical promotion")
if __name__=="__main__":main()
