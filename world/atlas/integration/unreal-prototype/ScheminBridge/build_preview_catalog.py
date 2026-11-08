"""Generate a self-contained, local HTML Atlas preview catalog, not Unreal renders."""
import html,json
from pathlib import Path
ROOT=Path(__file__).resolve().parent
m=json.loads((ROOT/"generated/world_preview_manifest.json").read_text())
receipt=json.loads((ROOT/"generated/atlas_build_receipt.json").read_text())
built=set(receipt["built"]) | set(receipt["skipped"])
cards=[]
for loc in m["locations"]:
  status=loc["render_classification"]
  tags=" ".join("<span>"+html.escape(x)+"</span>" for x in loc["landmarks"][:4])
  cards.append('<article><h3>'+html.escape(loc["name"])+'</h3><p class="muted">'+html.escape(loc["region"])+'</p><p><strong>'+html.escape(status)+'</strong></p><p>'+tags+'</p><p class="muted">'+html.escape(loc["id"])+'</p><p>'+("Level created" if loc["id"] in built else "Pending")+'</p></article>')
dots=[]
for i,loc in enumerate(m["locations"]):
  x,y=loc["atlas_position_abstract"]
  cx=35+x*7.9;cy=850-y*7.6
  dots.append('<circle cx="'+str(cx)+'" cy="'+str(cy)+'" r="6" fill="#e0ad65"><title>'+html.escape(loc["name"])+'</title></circle><text x="'+str(cx+9)+'" y="'+str(cy+4)+'" fill="#e2e6e9" font-size="11">'+html.escape(loc["name"])+'</text>')
style="""body{background:#101820;color:#f3f1e9;font-family:-apple-system,Arial,sans-serif;max-width:1280px;margin:auto;padding:38px}h1{font-size:38px}h3{margin-bottom:8px}.muted{color:#abb4bd}p{line-height:1.55}.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(270px,1fr));gap:14px}article{border:1px solid #46505b;border-radius:10px;padding:18px;background:#1c2833}span{font-size:12px;border-radius:10px;background:#39444f;padding:4px 8px;margin-right:5px}.frame{width:100%;background:#1c2833;border-radius:10px}"""
body="""<!doctype html><html lang="en"><meta charset="utf-8"><title>Commonwealth Unreal Preview Catalog</title><style>"""+style+"""</style><h1>Commonwealth Unreal Atlas — Blockout Preview</h1><p>23 schematic levels generated in Unreal Engine 5.8 from pinned Schemin canon. <strong>These are not rendered screenshots.</strong> Positions below are abstract, non-metric Atlas coordinates. Provisional and interpretive locations are not promoted to permanent canon.</p><svg class="frame" viewBox="0 0 900 900" role="img" aria-label="Abstract schematic location map"><rect width="900" height="900" fill="#17252f"/><text x="25" y="32" font-size="20" fill="#fff">Atlas Coordinate Index · Abstract, not geographic scale</text>"""+''.join(dots)+"""</svg><h2>Generated Unreal Levels</h2><div class="grid">"""+''.join(cards)+"""</div><p class="muted">Source commit: """+html.escape(m["source_commit"])+""" · Local HTML export, not published website.</p></html>"""
out=ROOT/"generated/atlas_preview_catalog.html"
out.write_text(body)
print("CATALOG_READY",out,"LEVELS",len(built))
