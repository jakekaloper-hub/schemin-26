"""Typeset the unsigned F03 proposal. All source wording comes from the folio manuscript."""
from hashlib import sha256
import json
from pathlib import Path
import subprocess

from PIL import Image, ImageDraw, ImageFont, ImageOps

ROOT=Path(__file__).resolve().parent
COPY=ROOT.parent/'W11_READER_LETTERING_2026-11-24.md'


def font(family,size):
    return ImageFont.truetype(subprocess.check_output(['fc-match','-f','%{file}',family],text=True),size)


def wrapped(text,face,width):
    lines=[]
    for word in text.split():
        if lines and face.getlength(lines[-1]+' '+word)<=width:
            lines[-1]+=' '+word
        else:
            lines.append(word)
    return lines


def render():
    title,body=COPY.read_text().split('## F03 · ',1)[1].split('\n## F04',1)[0].strip().split('\n',1)
    body=' '.join(body.split())
    plate=ROOT/'plate.png'
    with Image.open(plate) as original:
        dims=list(original.size)
        paper=ImageOps.fit(original.convert('RGB'),(1080,1920),Image.Resampling.LANCZOS)
    draw=ImageDraw.Draw(paper)
    label=font('Nimbus Sans Narrow:style=Bold',32)
    large=font('Nimbus Roman:style=Regular',97)
    letter=font('Nimbus Roman:style=Regular',53)
    left,right=96,984
    ink='#201d18'
    draw.text((left,835),'SCHEMIN’ ’26    /    WEEK 11',anchor='lt',font=label,fill='#593820')
    draw.text((right,835),'PROPOSED TEXT · UNSIGNED',anchor='rt',font=label,fill='#593820')
    draw.line((left,885,right,885),width=3,fill='#5e4731')
    assert large.getlength(title) <= right-left
    draw.text((left-3,921),title,anchor='lt',font=large,fill=ink)
    y=1076
    for line in wrapped(body,letter,right-left):
        draw.text((left,y),line,anchor='lt',font=letter,fill=ink)
        y+=63
    assert y < 1815, y
    draw.line((left,1828,right,1828),width=2,fill='#554937')
    draw.text((left,1850),'INTERNAL LAYOUT REVIEW',anchor='lt',font=label,fill='#463a2b')
    draw.text((right,1850),'F03',anchor='rt',font=label,fill='#463a2b')
    files={}
    for k,im,path in [('native',paper,ROOT/'F03.png'),('phone',paper.resize((390,693),Image.Resampling.LANCZOS),ROOT/'F03-390.png')]:
        im.save(path,optimize=True)
        files[k]={'path':path.name,'bytes':path.stat().st_size,'dimensions':list(im.size),'sha256':sha256(path.read_bytes()).hexdigest()}
    receipt={'folio':'F03','title':title,'classification':'INTERNAL_UNSIGNED_LAYOUT_CANDIDATE','publication_approved':False,
             'commissioner_voice_approved':False,'commissioner_signature_present':False,'portrait_present':False,
             'production_card':'shape:w11-os-f03','review_card':'shape:w11-review-f03','copy_file':COPY.name,'lettering':body,
             'lettering_sha256':sha256((title+'\n'+body).encode()).hexdigest(),
             'photographic_source':{'path':plate.name,'dimensions':dims,'sha256':sha256(plate.read_bytes()).hexdigest(),'authority':'New text-only generative set study of an anonymous hand, blank letter, capped pen and desk lamp.'},
             'native_and_phone':files,'brief':'Extreme close desk composition; paper and an unidentified working hand. Unsigned reader proposal for layout review under the Closer’s direction. The actual Commissioner owns voice and signature.'}
    (ROOT/'candidate.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__':
    render()
