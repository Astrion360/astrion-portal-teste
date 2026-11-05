from pathlib import Path
import re

ROOT = Path('.')
TARGETS = [ROOT / 'index.html', ROOT / 'revisao' / 'index.html']

FEATURE_PATTERNS = [
    "const feature=['manifesto','editorial','statement','fullBleed','closing','heroStat'].includes(s.kind);",
    "const feature=[6,54].includes(Number(s.number));",
]

AUTO_HEADING_BLOCK = """ else if(!['cover','chapter','productFocus'].includes(s.kind)){
 const heading=html.match(/<h1[\\s\\S]*?<\\/h1>(?:<p class=\"slide-lead[\\s\\S]*?<\\/p>)?/);
 if(heading){html=html.replace(heading[0],'<div class=\"photo-heading\"><div class=\"photo-heading-copy\">'+heading[0]+'</div><figure class=\"editorial-photo heading-photo\" aria-hidden=\"true\"></figure></div>');photoClass='photo-supported';}
 }"""

CHAPTER_RE = re.compile(
    r"case 'chapter': html=`<div class=\"chapter-art\" aria-hidden=\"true\"><span class=\"chapter-marker\">\$\{esc\(s\.chapterNumber\)\}</span><svg[\s\S]*?</div><div class=\"eyebrow reveal\">CAPÍTULO \$\{esc\(s\.chapterNumber\)\}</div>\$\{title\(s\)\}<div class=\"chapter-subtitle reveal\">[\s\S]*?</div>`;break;"
)

CHAPTER_REPLACEMENT = (
    "case 'chapter': html=`<div class=\"chapter-art chapter-photo chapter-photo-${esc(s.chapterNumber)}\" aria-hidden=\"true\">"
    "<span class=\"chapter-marker\">${esc(s.chapterNumber)}</span></div>"
    "<div class=\"eyebrow reveal\">CAPÍTULO ${esc(s.chapterNumber)}</div>${title(s)}"
    "<div class=\"chapter-subtitle reveal\">ASTRION / CONHECIMENTO QUE CONECTA</div>`;break;"
)

CHAPTER_CSS_BASE = (
    '.chapter-art{position:absolute;inset:0 0 0 auto;width:36%;border:1px solid #4ccce644;'
    'border-radius:28px;background:linear-gradient(145deg,#173b53c9,#071b30c9);overflow:hidden;'
    'display:grid;place-items:center;box-shadow:0 24px 70px #0003}.chapter-art>svg{width:48%;height:48%;'
    'color:#88e9fc;filter:drop-shadow(0 0 22px #38c5ed55)}'
)


def chapter_css(asset_prefix: str) -> str:
    return CHAPTER_CSS_BASE + (
        f"/* astrion-section-intro-photos-v2 */"
        f".chapter-photo{{background-repeat:no-repeat;background-size:cover;background-position:center}}"
        f".chapter-photo-1{{background-image:linear-gradient(180deg,#031b35b8,#031b351f),url('{asset_prefix}sao-paulo.webp')}}"
        f".chapter-photo-2{{background-image:linear-gradient(180deg,#082643cc,#051a30cc),url('{asset_prefix}hero.svg')}}"
        f".chapter-photo-3{{background-image:linear-gradient(180deg,#052843cc,#041b31cc),url('{asset_prefix}texture.svg')}}"
        f".chapter-photo-4{{background-image:linear-gradient(180deg,#062541cc,#04192dcc),url('{asset_prefix}ancora-logo.svg')}}"
        f".chapter-photo-5{{background-image:linear-gradient(180deg,#082643cc,#051a30cc),url('{asset_prefix}fluxo.svg')}}"
        f".chapter-photo-6{{background-image:linear-gradient(180deg,#082643cc,#051a30cc),url('{asset_prefix}parceiro.svg')}}"
        f".chapter-photo-7{{background-image:linear-gradient(180deg,#082643cc,#051a30cc),url('{asset_prefix}parcela.svg')}}"
        f".chapter-photo-8{{background-image:linear-gradient(180deg,#082643cc,#051a30cc),url('{asset_prefix}jornada.svg')}}"
        f".chapter-photo-9{{background-image:linear-gradient(180deg,#082643cc,#051a30cc),url('{asset_prefix}hero.svg')}}"
    )


def patch_file(path: Path) -> bool:
    src = path.read_text(encoding='utf-8')
    original = src
    assert 'header-logo-astrion' in src, f'{path}: logo da Astrion não encontrado no HTML'

    for patt in FEATURE_PATTERNS:
        if patt in src:
            src = src.replace(patt, 'const feature=false;', 1)

    if AUTO_HEADING_BLOCK in src:
        src = src.replace(AUTO_HEADING_BLOCK, '', 1)

    src, chapter_count = CHAPTER_RE.subn(CHAPTER_REPLACEMENT, src, count=1)
    assert chapter_count == 1 or 'chapter-photo chapter-photo-' in src, f'{path}: bloco de abertura de capítulo não localizado'

    marker_v1 = 'astrion-section-intro-photos-v1'
    marker_v2 = 'astrion-section-intro-photos-v2'
    asset_prefix = 'assets/' if path.parent == ROOT else '../assets/'
    if marker_v2 not in src:
        if marker_v1 in src:
            src = re.sub(
                r'/\* astrion-section-intro-photos-v1 \*/\.chapter-photo\{[\s\S]*?\.chapter-photo-9\{[^}]*\}',
                chapter_css(asset_prefix),
                src,
                count=1,
            )
        elif CHAPTER_CSS_BASE in src:
            src = src.replace(CHAPTER_CSS_BASE, chapter_css(asset_prefix), 1)
        else:
            raise AssertionError(f'{path}: base CSS do capítulo não encontrada')

    # cobre casos já atualizados com caminhos assets/ dentro de revisao/
    if path.parent != ROOT:
        src = src.replace("url('assets/", "url('../assets/")

    # primeira página/capa geral preservada
    assert src[:500] == original[:500], f'{path}: cabeçalho/capa foi alterado indevidamente'
    if src != original:
        path.write_text(src, encoding='utf-8')
        return True
    return False


def main():
    changed = False
    for target in TARGETS:
        changed = patch_file(target) or changed
    if changed:
        print('Ajuste aplicado: imagens apenas na primeira página de cada seção, com artes distintas.')
    else:
        print('Nenhuma alteração necessária; política de imagens já aplicada.')


if __name__ == '__main__':
    main()
