from pathlib import Path
import re

old = "const feature=['manifesto','editorial','statement','fullBleed','closing','heroStat'].includes(s.kind);"
new = "const feature=[6,54].includes(Number(s.number));"
automatic = r''' else if(!['cover','chapter','productFocus'].includes(s.kind)){
 const heading=html.match(/<h1[\s\S]*?<\/h1>(?:<p class="slide-lead[\s\S]*?<\/p>)?/);
 if(heading){html=html.replace(heading[0],'<div class="photo-heading"><div class="photo-heading-copy">'+heading[0]+'</div><figure class="editorial-photo heading-photo" aria-hidden="true"></figure></div>');photoClass='photo-supported';}
 }'''

for path in (Path("index.html"), Path("revisao/index.html")):
    src = path.read_text(encoding="utf-8")
    if "astrion-image-policy-v2" in src:
        print(f"{path}: already updated")
        continue
    assert src.count(old) == 1, f"{path}: feature rule changed"
    assert src.count(automatic) == 1, f"{path}: automatic photography rule changed"
    dst = src.replace(old, new).replace(automatic, "")
    dst, n1 = re.subn(r'\.slide\.chapter \.chapter-art\{background-image:[^}]*\}\s*', "", dst, count=1)
    dst, n2 = re.subn(r'\.slide\.chapter \.chapter-art>svg,\.slide\.chapter \.chapter-art>i\{display:none\}\.slide\.chapter \.slide-inner\{[^}]*\}\.slide\.chapter \.chapter-marker\{[^}]*\}', "", dst, count=1)
    assert n1 == 1 and n2 == 1, f"{path}: chapter photo rule changed"
    dst = dst.replace(".slide.chapter .slide-inner{padding-right:0;min-height:0;display:flex;flex-direction:column;align-items:stretch}.slide.chapter .chapter-art{position:relative;inset:auto;transform:none;width:100%;height:auto;max-height:360px;aspect-ratio:3/2;margin:0 0 28px;order:0}.slide.chapter .chapter-art~*{order:1}", "")
    dst = dst.replace(".slide.chapter .chapter-art{max-height:260px;margin-bottom:24px}.slide.chapter .chapter-marker{width:44px;height:44px;font-size:22px;top:15px;left:15px}", "")
    dst = dst.replace(".slide.chapter .chapter-art{max-height:230px}", "")
    anchor = ".slide .editorial-photo{"
    assert anchor in dst, f"{path}: editorial photo rule missing"
    dst = dst.replace(anchor, "/* astrion-image-policy-v2: photography only where relevant */\n#s6{--editorial-photo:var(--photo-parceria)}\n#s54{--editorial-photo:var(--photo-planejamento)}\n" + anchor, 1)
    assert dst[:300] == src[:300], "Opening page markup/header changed"
    assert dst.count(new) == 1
    path.write_text(dst, encoding="utf-8")
    print(f"{path}: image policy applied")
