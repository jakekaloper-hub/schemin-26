"""Assemble six review sheets from actual approved-shape page PNGs; never draw scenes.
Usage: python assemble_review_sheets.py --masters /path/to/individuals --output /path/to/sheets
Every master must be an existing full, grayscale 1080x1920 folio. Missing/wrong inputs fail closed.
"""
from pathlib import Path
import argparse,hashlib,json
from PIL import Image,ImageChops,ImageDraw,ImageFont
P=Path(__file__).resolve().parent

def validate_master(path:Path)->Image.Image:
 if not path.is_file():raise FileNotFoundError(f'Missing actual folio master: {path}')
 with Image.open(path) as image:
  if image.format!='PNG' or image.size!=(1080,1920):raise ValueError(f'{path.name}: expected native1080x1920 PNG, got {image.format} {image.size}')
  rgb=image.convert('RGB');r,g,b=rgb.split()
  if ImageChops.difference(r,g).getbbox() or ImageChops.difference(g,b).getbbox():raise ValueError(f'{path.name}: expected grayscale proof, not colored artwork')
  return rgb

def assemble(masters:Path,output:Path,manifest:dict)->dict:
 pages=manifest['pages'];counts=[6,6,6,6,6,4]
 if len(pages)!=34 or len({p['page_id'] for p in pages})!=34:raise ValueError('Exactly34unique page contracts are required')
 if [len([p for p in pages if p['sheet']==i]) for i in range(1,7)]!=counts:raise ValueError('Six-sheet allocation mismatch')
 # Validate every input before writing even the first review sheet.
 for p in pages:
  im=validate_master(masters/(p['page_id']+'.png'));im.close()
 output.mkdir(parents=True,exist_ok=True);receipts=[];tile=(540,960);gap=24;label=34;top=92
 width=3*tile[0]+4*gap;height=top+2*(tile[1]+label)+3*gap
 font=ImageFont.load_default(size=19)
 for n in range(1,7):
  canvas=Image.new('RGB',(width,height),(28,28,28));draw=ImageDraw.Draw(canvas);draw.text((gap,26),f'SCHEMIN 26 | WEEK10 | SHEET {n} OF6 | GRAYSCALE FULL-FOLIO PROOFS',font=font,fill=(235,235,235))
  group=sorted([p for p in pages if p['sheet']==n],key=lambda p:p['slot']);inputs=[]
  for p in group:
   i=p['slot']-1;x=gap+(i%3)*(tile[0]+gap);y=top+gap+(i//3)*(tile[1]+label+gap)
   src=masters/(p['page_id']+'.png');image=validate_master(src);image=image.resize(tile,Image.Resampling.LANCZOS);canvas.paste(image,(x,y));draw.text((x,y+tile[1]+6),f"{p['reading_position']:02d} | {p['page_id']}",font=font,fill=(235,235,235))
   inputs.append({'page_id':p['page_id'],'master_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'scale':0.5,'crop':None,'rewritten':False})
  target=output/f'W10-SHEET-{n:02d}.png';canvas.save(target)
  receipts.append({'sheet':n,'path':target.name,'dimensions':list(canvas.size),'inputs':inputs,'empty_slots':[5,6] if n==6 else []})
 result={'sheets':receipts,'masters_unchanged':True,'generated_scene_count':0,'single_source':'actual individual full-page PNG masters'};(output/'assembly-receipt.json').write_text(json.dumps(result,indent=2)+'\n');return result

def main():
 parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--masters',required=True,type=Path);parser.add_argument('--output',required=True,type=Path);args=parser.parse_args()
 result=assemble(args.masters,args.output,json.loads((P/'render-inputs/manifest.json').read_text()));print(f"Assembled {len(result['sheets'])} review sheets from34existing masters")
if __name__=='__main__':main()
