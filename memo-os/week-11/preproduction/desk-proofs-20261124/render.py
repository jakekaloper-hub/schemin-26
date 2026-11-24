"""Typeset internal Week 11 desk proofs using the current reader lettering and original set studies."""
from functools import cache
from hashlib import sha256
import json
from pathlib import Path
import re
import subprocess

from PIL import Image, ImageDraw, ImageFont, ImageOps


ROOT = Path(__file__).resolve().parent
COPY = ROOT.parent / "W11_READER_LETTERING_2026-11-24.md"
MARGIN = 68
RIGHT = 1080 - MARGIN
WIDTH = RIGHT - MARGIN
PAGES = {
    2: ("Opening drive", "League Chamber", "ESPN final scoreboard · November 24"),
    4: ("League wire", "Final scoreboard", "ESPN via Flaim · November 24"),
    7: ("League archive", "The playoff line", "ESPN standings · November 24"),
    23: ("Sports desk", "Starter investigations I", "ESPN starter sheets · Week 11"),
    24: ("Sports desk", "Starter investigations II", "ESPN starter sheets · Week 11"),
    25: ("Availability desk", "The House & the lineup", "Pittsy’s Book · November 19  /  ESPN · November 24"),
    26: ("Lineup desk", "The starting sheet", "ESPN starters and reserves · Week 11"),
    27: ("Waiver wire", "Roster ledger", "ESPN transactions and starter sheets · Week 11"),
    28: ("League archive", "The divisional register", "ESPN records and schedule · November 24"),
    29: ("Sports desk", "Scoring index", "ESPN scores / Sports Desk calculation · Week 11"),
    30: ("Playoff desk", "Postseason model", "TheFFHub · November 24"),
    32: ("Schedule desk", "Divisional travel", "ESPN fixtures · Week 12"),
}
FAMILIES = {"serif": "Nimbus Roman:style=Regular", "italic": "Nimbus Roman:style=Italic",
            "sans": "Nimbus Sans Narrow:style=Regular", "bold": "Nimbus Sans Narrow:style=Bold"}


@cache
def font(face, size):
    path = subprocess.check_output(["fc-match", "-f", "%{file}", FAMILIES[face]], text=True)
    return ImageFont.truetype(path,size)


def wrap(text, f, width):
    lines = []
    for word in text.split():
        if not lines or f.getlength(lines[-1] + ' ' + word) > width:
            lines.append(word)
        else:
            lines[-1] += ' ' + word
        assert f.getlength(word) <= width, (word, width)
    return lines


class Folio:
    def __init__(self,n,title,paragraphs):
        self.n = n
        self.title = title
        self.department,self.section,self.source = PAGES[n]
        self.texts = [s.strip() for s in paragraphs.splitlines() if s.strip() and not s.startswith('|')]
        self.table = [[cell.strip() for cell in s.strip('|').split('|')] for s in paragraphs.splitlines()
                      if s.startswith('|') and not s.startswith('| ---')]
        self.bg,self.ink,self.soft,self.rule,self.accent = (
            ('#122824','#fff4dc','#d4d3b7','#668175','#ffbe77') if n in (4,24,26,29,32)
            else ('#f2ead6','#24291f','#565846','#a8a58c','#903815')
        )
        self.im = Image.new('RGB',(1080,1920),self.bg)
        self.d = ImageDraw.Draw(self.im)
        self.y = 0

    def line(self,y,width=2,color=None):
        self.d.line((MARGIN,y,RIGHT,y),fill=color or self.rule,width=width)

    def label(self,x,y,text,size=32,color=None,anchor='lt'):
        self.d.text((x,y),text,font=font('bold',size),fill=color or self.accent,anchor=anchor)

    def paragraph(self,text,size=47,face='serif',color=None,width=WIDTH,spacing=1.13):
        f = font(face,size)
        for line in wrap(text,f,width):
            self.d.text((MARGIN,self.y),line,font=f,fill=color or self.ink,anchor='lt')
            self.y += round(size*spacing)

    def frame(self):
        self.line(46,4,self.ink)
        self.label(MARGIN,68,"SCHEMIN’ ’26",37,self.ink)
        self.d.text((540,69),'One Last Crossing',anchor='mt',font=font('italic',32),fill=self.ink)
        self.label(RIGHT,68,"WEEK 11",35,self.ink,'rt')
        self.label(MARGIN,148,self.department.upper()+'   /   '+self.section.upper(),32)
        self.y = 201
        self.paragraph(self.title,size=96,spacing=0.99)
        self.y += 24
        height = {2:530,4:315,7:265,23:432,24:450,25:502,26:500,27:398,28:405,29:239,30:253,32:350}[self.n]
        with Image.open(ROOT / 'plates' / f'F{self.n:02}.jpg') as art:
            self.im.paste(ImageOps.fit(art,(1080,height),method=Image.Resampling.LANCZOS),(0,self.y))
        self.y += height + 43

    def numbers(self,*pairs):
        start = self.y
        for i,(value,label) in enumerate(pairs):
            x=MARGIN+i*485
            self.d.line((x,start,x+450,start),width=3,fill=self.rule)
            self.d.text((x,start+22),value,font=font('serif',110),fill=self.accent,anchor='lt')
            self.label(x,start+135,label.upper(),32,self.ink)
        self.y += 221

    def ledger(self):
        n=self.n
        self.paragraph(self.texts[0],size=42)
        self.y += 15
        nums={4:(1,3),7:(0,2,3),29:(0,2,3),30:(1,)}[n]
        widths={4:(308,132,353,151),7:(115,438,158,233),29:(128,467,150,199),30:(608,336)}[n]
        def col(j):
            return MARGIN+sum(widths[:j]) + (19 if n==4 and j==2 else 0)
        for j,val in enumerate(self.table[0]):
            end=j in nums
            self.label(col(j)+(widths[j]-8 if end else 6),self.y,val.upper(),28,self.soft,'rt' if end else 'lt')
        self.y+=40
        self.line(self.y,3,self.ink)
        for i,row in enumerate(self.table[1:],1):
            winners=[]
            if n==4:
                winners=[0,1] if float(row[1])>float(row[3]) else [2,3]
            color=self.accent if n==7 and i==7 else self.ink
            lines=[]
            for j,val in enumerate(row):
                f=font('bold' if j in winners or n==7 and i==7 else 'sans',42 if n==4 else 40)
                lines.append((f,wrap(val,f,widths[j]-16-(19 if n==4 and j==2 else 0))))
            rowh=max(110 if n==4 else 59, max(len(values) for f,values in lines)*43+9)
            for j,(f,values) in enumerate(lines):
                end=j in nums
                x=col(j)+(widths[j]-8 if end else 6)
                for k,val in enumerate(values):
                    y=self.y+(rowh-43*len(values))//2+2+k*43
                    self.d.text((x,y),val,font=f,fill=self.accent if j in winners else color,anchor='rt' if end else 'lt')
            self.y += rowh
            self.line(self.y,4 if n==7 and i==7 else 1,self.accent if n==7 and i==7 else self.rule)
        self.y+=20
        self.paragraph(self.texts[-1],size=34,face='sans',color=self.soft)

    def stories(self):
        for line in self.texts:
            label,body=re.match(r'\*\*(.*?)\*\* (.*)',line).groups()
            self.line(self.y)
            self.y+=24
            self.label(MARGIN,self.y,label.rstrip('.').upper())
            self.y+=45
            self.paragraph(body,size=47,spacing=1.11)
            self.y+=25

    def caption(self,label,text):
        self.line(self.y)
        self.y+=24
        self.label(MARGIN,self.y,label.upper())
        self.y+=53
        self.paragraph(text,size=50)
        self.y+=31

    def divisions(self):
        for division,names,chance in self.table[1:]:
            self.line(self.y)
            self.y+=19
            self.label(MARGIN,self.y,division.upper())
            self.y+=45
            self.paragraph(names,size=44,face='sans',spacing=1.12)
            self.y+=10
            self.paragraph(chance,size=37,face='italic',color=self.soft)
            self.y+=28

    def travel(self):
        self.paragraph(self.texts[0],size=46)
        self.y+=22
        self.label(MARGIN,self.y,'VISITOR',29,self.soft)
        self.label(592,self.y,'HOME',29,self.soft)
        self.y+=48
        for row in range(1,7,2):
            self.line(self.y)
            self.y+=18
            self.label(MARGIN,self.y,self.table[row][0].upper())
            self.y+=50
            for _,visitor,host in self.table[row:row+2]:
                f=font('sans',46)
                assert f.getlength(visitor)<449 and f.getlength(host)<421
                self.d.text((MARGIN,self.y),visitor,fill=self.ink,font=f,anchor='lt')
                self.d.text((592,self.y),host,fill=self.ink,font=f,anchor='lt')
                self.d.line((533,self.y+16,560,self.y+16),width=3,fill=self.accent)
                self.d.line((551,self.y+7,561,self.y+16,551,self.y+25),width=3,fill=self.accent)
                self.y+=57
            self.y+=15

    def draw(self):
        self.frame()
        n=self.n
        if n in (4,7,29,30):
            self.ledger()
        elif n in (23,24):
            self.stories()
        elif n == 28:
            self.divisions()
            for note in self.texts:
                self.paragraph(note,size=36,face="sans",color=self.soft)
        elif n == 32:
            self.travel()
        elif n == 25:
            first,rest=self.texts[0].split(' The final lineup',1)
            self.caption('November 19 · House posting',first)
            self.caption('November 24 · Final Week 11 lineup','The final lineup'+rest)
        else:
            pairs={2:(('3–8','Mud Dogs'),('7–4','Slob on my Dobb')),
                   26:(('13.00','Chiefs D/ST · Starter'),('23.80','Texans D/ST · Bench')),
                   27:(('28.42','Cam Ward · Starter'),('19.75','Chimere Dike · Starter'))}[n]
            self.numbers(*pairs)
            self.paragraph(self.texts[0],size=49,spacing=1.17)
            if n==27:
                self.y+=34
                self.line(self.y)
                self.y+=24
                self.paragraph(self.texts[1],size=39,face='sans')
        if n not in (4,7,30):
            self.y+=14
            self.paragraph(self.source,size=31,face='sans',color=self.soft)
        assert self.y <= 1826, (n,self.y)
        self.line(1835,2,self.ink)
        self.label(MARGIN,1857,'INTERNAL DESK PROOF',26,self.soft)
        self.label(RIGHT,1857,f'24 NOVEMBER 2026   /   F{n:02}',27,self.soft,'rt')
        return self.im


def main():
    parts=re.split(r'^## F(\d\d) · (.+)\n',COPY.read_text(),flags=re.M)
    sections={int(parts[i]):(parts[i+1],parts[i+2].strip()) for i in range(1,len(parts),3)}
    files=[]
    for n in PAGES:
        stem=f'F{n:02}'
        native=Folio(n,*sections[n]).draw()
        for folder,im in [('native',native),('phone',native.resize((390,693),Image.Resampling.LANCZOS))]:
            path=ROOT / folder / (stem+'.png')
            path.parent.mkdir(exist_ok=True)
            im.save(path,optimize=True)
            files.append({'folio':stem,'path':path.relative_to(ROOT).as_posix(),'dimensions':list(im.size),
                          'sha256':sha256(path.read_bytes()).hexdigest(),'bytes':path.stat().st_size})
    receipt={'classification':'INTERNAL_DESK_PROOF','publication_approved':False,
             'source_lettering':COPY.name,
             'folio_lettering_sha256':{f'F{n:02}':sha256((sections[n][0]+'\n'+sections[n][1]).encode()).hexdigest() for n in PAGES},
             'phone_method':'Lanczos downsample of each exact native 1080 x 1920 folio to 390 x 693.',
             'art':'New generated anonymous set studies. No protected reference images supplied. Scene identity and Atlas geography are unapproved.',
             'files':files}
    (ROOT/'proofs.json').write_text(json.dumps(receipt,indent=2)+'\n')


if __name__=='__main__':
    main()
