"""Compose the approved internal close-framed F35 audition on the final Word page."""
from hashlib import sha256
import json
from pathlib import Path
import subprocess

from PIL import Image, ImageDraw, ImageFont, ImageOps


ROOT = Path(__file__).resolve().parent
PREPRODUCTION = ROOT.parent
LETTERING = PREPRODUCTION / "W11_READER_LETTERING_2026-11-24.md"


def font(family, size):
    path = subprocess.check_output(["fc-match", "-f", "%{file}", family], text=True)
    return ImageFont.truetype(path, size)


def read_copy():
    head, body = LETTERING.read_text().split("## F35 · ", 1)[1].strip().split("\n", 1)
    return head, ' '.join(body.split())


def run():
    title, body = read_copy()
    lines = ["For three weeks now,", "everybody who can spoil", "your Sunday knows the", "way to your place."]
    assert ' '.join(lines) == body
    plate = ROOT / "plate.png"
    with Image.open(plate) as source:
        original_dimensions = list(source.size)
        source_rgb = source.convert("RGB")
        page = ImageOps.fit(source_rgb,(1080,1920),Image.Resampling.LANCZOS,centering=(.50,.50))
    # Two editorial scrims preserve the photograph while providing continuous contrast under the type.
    scrim = Image.new("L",(1,1920))
    scrim.putdata([max(round(116*max(0,1-y/315)),round(148*max(0,min(1,(y-1160)/310)))) for y in range(1920)])
    page = Image.composite(Image.new("RGB",page.size,(9,20,20)),page,scrim.resize((1080,1920)))
    draw = ImageDraw.Draw(page)
    label = font("Nimbus Sans Narrow:style=Bold",31)
    display = font("Nimbus Roman:style=Regular",77)
    small = font("Nimbus Sans Narrow:style=Regular",29)
    right = 1005
    draw.text((75,70),"SCHEMIN’ ’26",font=label,anchor='lt',fill="#f2e8cf")
    draw.text((right,70),"WEEK 11    /    FINAL WORD",font=label,anchor='rt',fill="#f2e8cf")
    draw.line((75,124,right,124),width=2,fill="#c7bca0")
    draw.text((75,1335),title.upper(),font=label,anchor='lt',fill="#f7c180")
    for i,line in enumerate(lines):
        assert display.getlength(line) < 930
        draw.text((72,1417+i*83),line,font=display,anchor='lt',fill="#fff2d9")
    draw.line((75,1818,right,1818),width=2,fill="#c7bca0")
    draw.text((75,1842),"INTERNAL PRODUCTION CANDIDATE",font=small,anchor='lt',fill="#e5d8bb")
    draw.text((right,1842),"F35",font=label,anchor='rt',fill="#f2e8cf")
    files={}
    for key,img,path in [("native",page,ROOT/"F35.png"),("phone",page.resize((390,693),Image.Resampling.LANCZOS),ROOT/"F35-390.png")]:
        img.save(path,optimize=True)
        files[key]={"path":path.name,"dimensions":list(img.size),"sha256":sha256(path.read_bytes()).hexdigest(),"bytes":path.stat().st_size}
    data={"folio":"F35","title":title,"classification":"INTERNAL_NATIVE_CANDIDATE","publication_approved":False,
          "production_card":"shape:w11-os-f35","review_card":"shape:w11-review-f35","copy_file":LETTERING.name,
          "lettering":body,"lettering_sha256":sha256((title+'\n'+body).encode()).hexdigest(),
          "photographic_source":{"path":plate.name,"dimensions":original_dimensions,"sha256":sha256(plate.read_bytes()).hexdigest(),
            "authority":"New text-to-image close-framed Storm Coast Road study. No protected character or venue reference used. It does not attest to approved wider geography."},
          "brief":"Transport-free, close view of the damp Storm Coast Road approach to Storm Bowl. No visible driver, cast, headlights, panorama or new landmark.",
          "native_and_phone":files,"route_source":"../WEEK11_LOCATION_DESK.md#f33--f35--el-niño-host-approach",
          "review":"Compare as a close-framed candidate. Vehicle and wide camera permissions and independent Umpire release remain separate."}
    (ROOT/"candidate.json").write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')


if __name__=="__main__":
    run()
