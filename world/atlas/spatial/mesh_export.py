"""Export experimental grid to deterministic OBJ text, without changing canonical geography."""
from world.atlas.spatial.landscape_experiment import build_landscape

def render_obj(n=33,step_m=50):
    d=build_landscape(n=n,step_m=step_m)
    rows=["# SCHEMIN SYNTHETIC / NOT CANON","o Central_Basin_Experimental_Surface"]
    for j,row in enumerate(d["heightfield"]):
        for i,h in enumerate(row):
            rows.append(f"v {i*step_m:.3f} {j*step_m:.3f} {h:.5f}")
    for j in range(n-1):
        for i in range(n-1):
            a=j*n+i+1;b=a+1;c=a+n;dd=c+1
            rows.extend([f"f {a} {b} {dd}",f"f {a} {dd} {c}"])
    return "\n".join(rows)+"\n"

if __name__=="__main__":
    import argparse
    p=argparse.ArgumentParser()
    p.add_argument("--output",required=True)
    args=p.parse_args()
    from pathlib import Path
    Path(args.output).write_text(render_obj(),encoding="utf-8")
