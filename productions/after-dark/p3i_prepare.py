import json,re
from pathlib import Path
root=Path(__file__).resolve().parents[2]
s=(root/"productions/after-dark/P3G_LLC_FOLIO_COPY_AND_VISUAL_PACKETS.md").read_text()
pages=re.split(r"(?=^## Page \d{2} — )",s,flags=re.M)[1:]
out=[]
for i,p in enumerate(pages,1):
 def field(name):
  m=re.search(r"^\*\*"+re.escape(name)+r":\*\*\s*(.*)$",p,re.M)
  return m.group(1) if m else ""
 body=p.split("**Exact display copy:**",1)[1].split("**",1)[0].strip()
 out.append({"page":i,"headline":field("Headline"),"copy":body,"fact":field("Fact panel") or field("Source note") or field("Signoff") or field("Deck"),"visual":field("Visual brief") or field("Image brief")})
assert len(out)==6
dest=root/"productions/after-dark/fixtures/p3i_page_copy.json"
dest.write_text(json.dumps(out,ensure_ascii=False,indent=2)+"\n")
print("Prepared",len(out),"pages",dest)
