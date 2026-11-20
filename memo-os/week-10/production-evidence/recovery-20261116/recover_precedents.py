from pathlib import Path
import hashlib,json
import pymupdf
from PIL import Image,ImageDraw,ImageOps
ROOT=Path(__file__).resolve().parents[4]
OUT=Path(__file__).resolve().parent
BASE=Path("/Users/jakekaloper/Desktop/Desktop - Jake’s MacBook Pro/Fantasy Football/Pro Schemin'/2026 Memos/Weeks/official")
FILES={2:'Week 2 memo.pdf',7:'Schemin_26_Official_Week_7_Memo.pdf',8:'Schemin_26_Official_Week_8_Memo.pdf',9:'Schemin_26_Week_9_Memo_Shareable_v2.pdf'}
receipts=[]
for week,name in FILES.items():
 src=BASE/name;doc=pymupdf.open(src);w,h=200,330;cols=6;rows=(len(doc)+5)//6
 sheet=Image.new('RGB',(cols*w,rows*h),(24,24,24));draw=ImageDraw.Draw(sheet)
 for i,page in enumerate(doc):
  pix=page.get_pixmap(matrix=pymupdf.Matrix(0.8,0.8),alpha=False);im=Image.frombytes('RGB',(pix.width,pix.height),pix.samples);thumb=ImageOps.contain(im,(w-8,h-24));x=(i%cols)*w+(w-thumb.width)//2;y=(i//cols)*h
  sheet.paste(thumb,(x,y));draw.text(((i%cols)*w+6,y+h-20),f'WEEK {week} / PHYSICAL PAGE {i+1:02}',fill='white')
  if i+1 in [1,2,3,4] or (week==9 and i+1 in [12,13,14,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,34]):
   pix=page.get_pixmap(matrix=pymupdf.Matrix(1.2,1.2),alpha=False);im=Image.frombytes('RGB',(pix.width,pix.height),pix.samples);im=ImageOps.contain(im,(960,1707));im.save(OUT/f'precedent-w{week:02d}-p{i+1:02d}.jpg',quality=88)
 sheet.save(OUT/f'precedent-week-{week}-contact.jpg',quality=85)
 receipts.append({'week':week,'filename':name,'source_local_path':str(src),'sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'bytes':src.stat().st_size,'physical_pages':len(doc),'contact':f'precedent-week-{week}-contact.jpg','source_untouched':True})
 print('RECOVERED',week,len(doc),receipts[-1]['sha256'])
(OUT/'published-memo-source-receipts.json').write_text(json.dumps(receipts,indent=2)+'\n')
