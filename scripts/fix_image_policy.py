from pathlib import Path
import re

for file in (Path("index.html"),Path("revisao/index.html")):
    src=file.read_text(encoding="utf-8")
    prefix="assets/" if file.parent==Path(".") else "../assets/"
    assert "chapter-photo chapter-photo-" in src
    assert "header-logo-astrion" in src

    # As aberturas usam agora diagramas editoriais desenhados
    # especificamente para os nove assuntos, hospedados no repositorio.
    variable="$"+"{esc(s.chapterNumber)}"
    newer=prefix+"section-editorial-"+variable+".svg"
    previous=prefix+"chapter-"+variable+".webp"
    assert previous in src or newer in src, f"{file}: marcador de imagem de capitulo nao encontrado"
    src=src.replace(previous,newer)
    assert src.count(newer)==1

    css="""<style id="astrion-topic-visuals-v1">
    .slide.chapter .chapter-art.chapter-photo{background:none!important;overflow:hidden!important}
    .slide.chapter .chapter-art.chapter-photo .chapter-visual{
      position:absolute!important;inset:0!important;display:block!important;
      width:100%!important;height:100%!important;object-fit:cover!important;
      max-width:none!important;z-index:1!important}
    .slide.chapter .chapter-art.chapter-photo .chapter-marker{display:none!important}
    </style>"""
    if "astrion-topic-visuals-v1" not in src:
        assert src.count("</head>")==1
        src=src.replace("</head>",css+"</head>",1)

    assert "astrion-typography-refinement-v2" in src, f"{file}: quote revision missing"
    assert '<span>Pensamos com quem vende.</span><span>Entendemos quem administra.</span>' in src
    assert src.count('chapter-visual" src=')==1
    assert "header-logo-astrion" in src
    file.write_text(src,encoding="utf-8")
    print(f"{file}: imagens editoriais por assunto, numeracao oculta, frase revisada")
