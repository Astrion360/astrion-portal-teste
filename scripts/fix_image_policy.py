"""Publica fotografia contextual para cada abertura, sem diagramas."""
from pathlib import Path
from urllib.request import Request,urlopen
from io import BytesIO
from PIL import Image,ImageOps,ImageEnhance
from hashlib import sha256
import time

# Nove fotografias com assuntos associados aos capitulos.
# 01: montagem editorial realista de produtos, mercado e comercial;
# 02 consorcio/imoveis; 03 mercado e dados; 04 administracao;
# 05 alternativas e analise; 06 apoio profissional; 07 financeiro;
# 08 atendimento e relacionamento; 09 parceria.
SOURCES=[
 ("photo-1560518883-ce09059eeffa","photo-1503376780353-7e6692767b70","photo-1454165804606-c3d57bc86b40","photo-1556761175-b413da4baf72"),
 ("photo-1560518883-ce09059eeffa",),
 ("photo-1551288049-bebda4e38f71",),
 ("photo-1486406146926-c627a92ad1ab",),
 ("photo-1454165804606-c3d57bc86b40",),
 ("photo-1556761175-b413da4baf72",),
 ("photo-1579621970563-ebec7560ff3e",),
 ("photo-1522071820081-009f0129c71c",),
 ("photo-1521791136064-7986c2920216",),
]

def fetch(photo):
    url=f"https://images.unsplash.com/{photo}?fit=crop&w=1350&h=850&q=85&fm=jpg"
    error=None
    for attempt in range(3):
        try:
            req=Request(url,headers={"User-Agent":"Mozilla/5.0","Accept":"image/jpeg,image/*"})
            with urlopen(req,timeout=45) as response:
                if response.status!=200: raise RuntimeError(f"HTTP {response.status}")
                data=response.read()
            if len(data)<10000: raise RuntimeError("Photo too small")
            with Image.open(BytesIO(data)) as im:
                im=ImageOps.exif_transpose(im).convert("RGB")
                if im.width<650 or im.height<400: raise RuntimeError("Resolution too low")
                return ImageOps.fit(im,(1350,850),method=Image.Resampling.LANCZOS)
        except Exception as e:
            error=e
            time.sleep(attempt+1)
    raise RuntimeError(f"Photo {photo} unavailable: {error}")

def compose(sources):
    if len(sources)==1: return fetch(sources[0])
    # Montagem fotografica sem icones, setas, graficos desenhados ou legendas.
    # Casa, automovel, indicadores economicos e relacao comercial:
    # quatro areas da cadeia que a Astrion conhece.
    canvas=Image.new("RGB",(1350,850))
    quadrants=[(0,0,675,425),(675,0,1350,425),(0,425,675,850),(675,425,1350,850)]
    for source,rect in zip(sources,quadrants):
        im=fetch(source)
        crop=ImageOps.fit(im,(675,425),method=Image.Resampling.LANCZOS,centering=(.5,.46))
        canvas.paste(crop,rect[:2])
    return canvas

def prepare_images():
    hashes=[]
    for index,sources in enumerate(SOURCES,1):
        image=compose(sources)
        image=ImageEnhance.Contrast(image).enhance(1.07)
        path=Path(f"assets/chapter-{index:02}.webp")
        image.save(path,"WEBP",quality=86,method=5)
        with Image.open(path) as check: check.verify()
        hashes.append(sha256(path.read_bytes()).hexdigest())
        print(f"{path}: {path.stat().st_size} bytes")
    assert len(set(hashes))==9,"Photographs duplicated"

def patch_html(path):
    src=path.read_text(encoding="utf-8")
    original=src
    prefix="assets/" if path.parent==Path(".") else "../assets/"
    var="$"+"{esc(s.chapterNumber)}"
    old=prefix+"section-editorial-"+var+".svg"
    new=prefix+"chapter-"+var+".webp"
    assert old in src or new in src, f"{path}: chapter image unavailable"
    src=src.replace(old,new)
    assert src.count(new)==1
    css="""<style id="astrion-contextual-photos-v1">
    /* Fotografias em vez de diagramas; somente nas aberturas. */
    .slide.chapter .chapter-art.chapter-photo{background:none!important;overflow:hidden!important}
    .slide.chapter .chapter-art.chapter-photo .chapter-visual{
      position:absolute!important;inset:0!important;width:100%!important;height:100%!important;
      display:block!important;object-fit:cover!important;object-position:center!important;
      max-width:none!important;z-index:1!important}
    .slide.chapter .chapter-art.chapter-photo .chapter-marker{display:none!important}
    </style>"""
    if "astrion-contextual-photos-v1" not in src:
        assert src.count("</head>")==1
        src=src.replace("</head>",css+"</head>",1)
    assert "astrion-typography-refinement-v2" in src
    assert "header-logo-astrion" in src
    assert src.count('chapter-visual" src=')==1
    assert src[:500]==original[:500],"Unexpected cover change"
    path.write_text(src,encoding="utf-8")
    print(f"{path}: photographs installed, cover preserved")

prepare_images()
for file in (Path("index.html"),Path("revisao/index.html")):
    patch_html(file)
