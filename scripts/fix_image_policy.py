from pathlib import Path

for file in (Path('index.html'),Path('revisao/index.html')):
    original=file.read_text(encoding='utf-8')
    src=original
    assert 'case \'chapter\':' in src
    assert 'chapter-photo chapter-photo-' in src
    assert 'header-logo-astrion' in src

    # Insere imagem REAL no HTML do capítulo (em vez de depender do CSS background).
    prefix='assets/' if file.parent==Path('.') else '../assets/'
    tag='chapter-photo-${esc(s.chapterNumber)}" aria-hidden="true">'
    img='<img class="chapter-visual" src="'+prefix+'chapter-${esc(s.chapterNumber)}.svg" alt="" loading="eager" decoding="async">'
    if img not in src:
        assert src.count(tag)==1, f'{file}: markup de capitulo inesperado'
        src=src.replace(tag+'<span class="chapter-marker">${esc(s.chapterNumber)}</span>',tag+img,1)
    # Remove qualquer numero que ainda possa estar posicionado por cima da imagem.
    src=src.replace(tag+'<span class="chapter-marker">${esc(s.chapterNumber)}</span>',tag+img,1)

    style='''<style id="astrion-chapter-visuals-v4">
    /* Uma imagem exclusiva por abertura de capitulo; nao modifica a capa geral. */
    .slide.chapter .chapter-art.chapter-photo{background:none!important;overflow:hidden!important}
    .slide.chapter .chapter-art.chapter-photo .chapter-visual{position:absolute!important;inset:0!important;width:100%!important;height:100%!important;object-fit:cover!important;display:block!important;max-width:none!important;z-index:1!important}
    .slide.chapter .chapter-art.chapter-photo .chapter-marker{display:none!important}
    </style>'''
    if 'astrion-chapter-visuals-v4' not in src:
        assert src.count('</head>')==1
        src=src.replace('</head>',style+'</head>',1)
    assert src[:500]==original[:500]
    assert src.count('chapter-visual" src=')==1
    assert src.count('astrion-chapter-visuals-v4')==1
    file.write_text(src,encoding='utf-8')
    print(file,'imagem por capitulo, sem numeracao sobre as imagens')
