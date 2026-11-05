from pathlib import Path

for path in (Path("index.html"), Path("revisao/index.html")):
    src = path.read_text(encoding="utf-8")
    assert "chapter-photo chapter-photo-" in src, f"{path}: aberturas com imagens ausentes"
    assert 'class="header-logo-astrion"' in src, f"{path}: logotipo ausente"

    # A regra antiga era mais específica e encobria as fotos individuais das aberturas.
    src = src.replace(
        ".slide.chapter .chapter-art{background-image:",
        ".slide.chapter .chapter-art:not(.chapter-photo){background-image:",
        1,
    )

    # Seção 9 não pode repetir a arte da seção 2.
    src = src.replace(
        ".chapter-photo-9{background-image:linear-gradient(180deg,#082643cc,#051a30cc),url('assets/hero.svg')}",
        ".chapter-photo-9{background-image:linear-gradient(180deg,#082643cc,#051a30cc),url('assets/astrion-logo.svg')}",
        1,
    )
    src = src.replace(
        ".chapter-photo-9{background-image:linear-gradient(180deg,#082643cc,#051a30cc),url('../assets/hero.svg')}",
        ".chapter-photo-9{background-image:linear-gradient(180deg,#082643cc,#051a30cc),url('../assets/astrion-logo.svg')}",
        1,
    )
    assert ".slide.chapter .chapter-art:not(.chapter-photo){background-image:" in src
    assert src.count(".chapter-photo-9{") == 1
    path.write_text(src, encoding="utf-8")
    print(f"{path}: prioridade das imagens corrigida e imagens distintas por secao")
