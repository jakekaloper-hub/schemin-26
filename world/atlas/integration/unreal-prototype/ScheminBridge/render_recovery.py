"""Fail-closed crash diagnosis and render route selection; no fake image output."""
import json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parent
LOG=ROOT/"generated/render_attempt.log"
REPORT=ROOT/"generated/render_recovery_report.json"
text=LOG.read_text(errors="replace") if LOG.exists() else ""
crash=list((Path.home()/"Library/Application Support/Epic/UnrealEngine/5.8/Saved/Crashes").glob("CrashReport-UE-Schemin_UE_Prototype-pid-56994-*"))
ctx=(crash[0]/"CrashContext.runtime-xml").read_text(errors="replace") if crash else ""
method="TakeHighResScreenshot" if "TakeHighResScreenshot" in ctx else None
report={"status":"BLOCKED_PENDING_REAL_RENDER","crash_confirmed":bool(crash),
"crash_function":method,"previous_method_blacklisted":method is not None,
"previous_headless_nullrhi":("-nullrhi" in text),
"recovery_route":"UE interactive editor with camera actor, Sequencer/Movie Render Queue using real Metal RHI",
"rendered_frame_verified":False,
"required_evidence":["actual PNG/EXR","image file integrity","visual inspection","UE render log"]}
REPORT.write_text(json.dumps(report,indent=2)+"\n")
print("RENDER_RECOVERY",report["status"],report["crash_function"])
