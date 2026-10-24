"""Reproducible OBJ reference export with a separate constraint manifest."""
import json
from pathlib import Path
from world.atlas.spatial.mesh_export import render_obj
from world.atlas.spatial.historical_constraints import build_historical_constraints


def export_reference(out_dir):
    p=Path(out_dir)
    p.mkdir(parents=True,exist_ok=True)
    geo=build_historical_constraints()
    if geo['physical_requirements']['metric_scale_and_landmark_footprints_approved']:
        raise ValueError('CANDIDATE_MUST_NOT_BE_CERTIFIED')
    (p/'central_basin_candidate.obj').write_text(render_obj(),encoding='utf-8')
    (p/'historical_constraints.json').write_text(json.dumps(geo,indent=2,sort_keys=True)+'\n',encoding='utf-8')
    (p/'README.txt').write_text('Noncanonical experimental heightfield, OBJ geometry and source-backed historical constraint manifest. The terrain does not position landmarks or certify watersheds. No illustrative map is a spatial authority.\n')
    return p

if __name__=='__main__':
    import argparse
    a=argparse.ArgumentParser();a.add_argument('--out',required=True)
    print(export_reference(a.parse_args().out))
