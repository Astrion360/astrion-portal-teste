from pathlib import Path
from io import BytesIO
from urllib.request import Request, urlopen
from hashlib import sha256
from PIL import Image, ImageOps
import re,time

PHOTOS = [
 'photo-1521737711867-e3b97375f902',
 'photo-1600596542815-ffad4c1539a9',
 'photo-1460925895917-afdab827c52f',
 'photo-1497366216548-37526070297c',
 'photo-1554224155-6726b3ff858f',
 'photo-1556761175-b413da4baf72',
 'photo-1554224154-26032ffc0d07',
 'photo-1522071820081-009f0129c71c',
 'photo-1521791136064-7986c2920216'
]
STYLE="""<style id="astrion-official-brand-v1">
.brand-button{background:linear-gradient(135deg,#fff,#edf2f6)!important;border:1px solid #c6d6e1!important;border-radius:12px!important;padding:4px 11px!important;min-height:64px!important;box-shadow:0 7px 20px rgba(0,5,16,.16)!important}
.header-logo-astrion{width:230px!important;height:54px!important;object-fit:contain!important}
.slide.chapter .chapter-art.chapter-photo{background:none!important;overflow:hidden!important}
.slide.chapter .chapter-art.chapter-photo .chapter-visual{position:absolute!important;inset:0!important;width:100%!important;height:100%!important;object-fit:cover!important;display:block!important;max-width:none!important;z-index:1!important}
.slide.chapter .chapter-art.chapter-photo .chapter-marker{display:none!important}
.slide.chapter .chapter-art.chapter-photo:after{content:"";position:absolute;inset:0;background:linear-gradient(145deg,rgba(3,17,38,.08),rgba(4,23,43,.18));z-index:2;pointer-events:none}
@media(max-width:970px){.brand-button{min-height:53px!important;padding:3px 7px!important}.header-logo-astrion{width:155px!important;height:45px!important}}
@media(max-width:640px){.brand-button{min-height:45px!important;padding:2px 5px!important}.header-logo-astrion{width:115px!important;height:39px!important}}
</style>"""

def download(photo_id,path):
    url=f'https://images.unsplash.com/{photo_id}?fit=crop&w=1250&h=800&q=82&fm=jpg'
    err=None
    for attempt in range(3):
        try:
            req=Request(url,headers={'User-Agent':'Mozilla/5.0','Accept':'image/jpeg,image/*'})
            with urlopen(req,timeout=35) as resp:
                if resp.status!=200: raise ValueError(f'HTTP {resp.status}')
                data=resp.read()
            if len(data)<9000: raise ValueError(f'Image too small {len(data)}')
            with Image.open(BytesIO(data)) as source:
                im=ImageOps.exif_transpose(source).convert('RGB')
                if im.width<700 or im.height<400: raise ValueError('Image resolution insufficient')
                im=ImageOps.fit(im,(1250,800),method=Image.Resampling.LANCZOS)
                im.save(path,'WEBP',quality=83,method=5)
            with Image.open(path) as check: check.verify()
            return sha256(path.read_bytes()).hexdigest()
        except Exception as e:
            err=e
            time.sleep(attempt+1)
    raise RuntimeError(f'Cannot download {photo_id}: {err}')

def update_html(path):
    src=path.read_text(encoding='utf-8')
    original_start=src[:500]
    prefix='assets/' if path.parent==Path('.') else '../assets/'
    assert 'chapter-photo chapter-photo-' in src
    assert 'header-logo-astrion' in src
    pattern=r'<img\s+src="data:image/svg\+xml;base64,[A-Za-z0-9+/=]+"\s+alt="Astrion Assessoria"\s+class="header-logo-astrion"\s*/>'
    new_img=f'<img src="{prefix}astrion-logo-oficial.png" alt="Astrion Assessoria" class="header-logo-astrion"/>'
    src,count=re.subn(pattern,lambda _:new_img,src,count=1)
    if not count: assert new_img in src, f'{path}: official logo link missing'
    variable='$'+'{esc(s.chapterNumber)}'
    svg='chapter-'+variable+'.svg'
    webp='chapter-'+variable+'.webp'
    assert svg in src or webp in src, f'{path}: chapter image missing'
    src=src.replace(svg,webp)
    if 'astrion-official-brand-v1' not in src:
        assert src.count('</head>')==1
        src=src.replace('</head>',STYLE+'</head>',1)
    assert src[:500]==original_start
    assert src.count('astrion-official-brand-v1')==1
    assert src.count('chapter-visual" src=')==1
    path.write_text(src,encoding='utf-8')
    print(path,'official logo and distinct photos referenced')

def main():
    with Image.open('assets/astrion-logo-oficial.png') as logo: logo.verify()
    hashes=[]
    for idx,photo in enumerate(PHOTOS,1):
        path=Path(f'assets/chapter-{idx:02}.webp')
        hashes.append(download(photo,path))
        print(f'Chapter {idx:02}: {path.stat().st_size} bytes')
    assert len(set(hashes))==9,'Photos duplicated'
    for path in [Path('index.html'),Path('revisao/index.html')]:
        update_html(path)
    print('Nine chapter photographs installed; cover unchanged.')

if __name__=='__main__': main()
