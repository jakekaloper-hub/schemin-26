"""Safe resumable local Commonwealth production batch.
No background agent, GitHub writeback, or canon promotion.
"""
import datetime,json,subprocess,sys,traceback
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent
OUT=ROOT/"ScheminBridge/generated"
OUT.mkdir(exist_ok=True)
LEDGER=OUT/"production_status.json"
TASKS=[
 ("source_drift",[sys.executable,"-m","ScheminBridge.source_drift_check"]),
 ("manifest",[sys.executable,"-m","ScheminBridge.build_world_manifest"]),
 ("environment_specs",[sys.executable,"-m","ScheminBridge.build_environment_specs"]),
 ("region_packets",[sys.executable,"-m","ScheminBridge.build_region_packets"]),
 ("travel_graph",[sys.executable,"-m","ScheminBridge.build_travel_graph"]),
 ("regression",[sys.executable,"-m","unittest","discover","-s","ScheminBridge/tests","-v"]),
 ("preview_catalog",[sys.executable,"-m","ScheminBridge.build_preview_catalog"]),
]
def main():
 state={"schema_version":1,"run_utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),"source":"schemin-26 pinned Atlas","tasks":[],"overall":"RUNNING"}
 LEDGER.write_text(json.dumps(state,indent=2))
 for name,cmd in TASKS:
  result=subprocess.run(cmd,cwd=ROOT,capture_output=True,text=True)
  record={"task":name,"command":cmd,"exit_code":result.returncode,"state":"PASS" if result.returncode==0 else "BLOCKED"}
  (OUT/(name+".runner.log")).write_text(result.stdout+"\n"+result.stderr)
  state["tasks"].append(record)
  LEDGER.write_text(json.dumps(state,indent=2)+"\n")
  print(name,record["state"],flush=True)
  if result.returncode:
   state["overall"]="BLOCKED";LEDGER.write_text(json.dumps(state,indent=2)+"\n");return result.returncode
 state["overall"]="LOCAL_PIPELINE_PASS_NOT_RELEASED"
 LEDGER.write_text(json.dumps(state,indent=2)+"\n")
 return 0
if __name__=="__main__":sys.exit(main())
