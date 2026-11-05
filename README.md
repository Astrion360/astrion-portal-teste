# Astrion — site para revisão local

Site estático construído a partir do documento mestre e dos materiais da Proposta de Valor, com Astrion como marca protagonista e Âncora como administradora parceira.

## Abrir

Abra a pasta extraída e dê dois cliques em **index.html** (ou botão direito → Abrir com → Chrome/Edge). Não é necessário iniciar servidor nem acessar 127.0.0.1. Mantenha as subpastas junto do arquivo.

Opcional para desenvolvimento: execute Abrir-Astrion.cmd e use http://127.0.0.1:4173/ enquanto a janela estiver aberta. A preservação de sessão ao navegar por arquivos depende do navegador.

## Direção visual atual

Layout azul-marinho e ciano, menu lateral, fotografia de São Paulo e logotipos extraídos do arquivo ASTRION_Portal_Keynote_Apresentacao.html fornecido pelo usuário. A folha assets/presentation.css aplica a nova direção às nove páginas. Os sete simuladores e o conteúdo existente foram preservados. O site não reproduz a apresentação de 68 telas: a navegação inferior percorre os sete capítulos principais do site.

## Conteúdo entregue

- Home com narrativa completa e acesso às trilhas.
- A Astrion: atuação, soluções, método e responsabilidades.
- Consórcios: formação, jornada interativa, perguntas e glossário pesquisável.
- Âncora: administradora, portfólio e planos, com links oficiais.
- Comparativo: critérios equivalentes, administradoras consideradas e roteiro para download.
- Simuladores: cota/parcela, redutora, lance, financiamento PRICE com comparação em mesma base, comissão, Troca de Chaves e receita hipotética.
- Seja parceiro: sete perfis, proposta, implantação e perguntas.
- Contato: resumo local para download, sem transmissão ou falso cadastro.
- Privacidade: comportamento efetivo desta versão local.
- Modo apresentação com sete capítulos, avanço, retorno e saída. Atalhos: Alt+seta para navegação; Escape para sair quando fora dos campos.

## Cálculos

O motor v0.6.0 do Pacote 06 foi reaproveitado. A função de receita foi integrada ao motor com a fórmula do Pacote 07. Os campos são preservados na sessão do navegador, sem envio a um servidor. Cada resultado tem memória de cálculo, premissas e limites. O botão de impressão gera o cenário ativo com campos e data.

Parâmetros são didáticos. Nenhum resultado é proposta comercial, previsão de contemplação, CET completo ou lucro garantido. A seleção de modalidade na comissão contextualiza o exemplo; não carrega uma tabela contratual.

## Verificação

Com Node.js, dentro desta pasta:

```text
npm test
npm run check
```

Não há dependências de produção ou instalação necessária. Os testes verificam o motor final, os links, a estrutura das páginas e a ausência de tabelas restritas. Consulte `RELATORIO_DE_VALIDACAO.md` para o escopo e os resultados da revisão no navegador.

## Arquitetura e manutenção

Cada rota tem seu próprio `index.html`. `assets/site.css` contém a interface comum; `assets/site.js`, os componentes; `assets/motor.js`, as fórmulas; `assets/simulators.js`, os formulários e resultados. `assets/tokens.css` preserva a base visual do Pacote 08. Diagramas e arte foram reaproveitados do ZIP.

O site tem caminhos relativos compatíveis com hospedagem em subdiretório. É adequado à futura publicação estática em GitHub Pages ou Cloudflare Pages, após revisão. O ZIP de planejamento não integra este projeto de saída.

## Antes de publicar

1. Confirmar autorização de uso dos logotipos e da fotografia fornecidos no HTML de referência.
2. Homologar produtos, parâmetros e condições comerciais vigentes.
3. Reconciliar a base primária do BCB antes de habilitar indicadores e gráficos quantitativos. Não há ranking verificado nesta versão.
4. Confirmar domínio, contatos oficiais e canal de atendimento.
5. Se houver captação, contratar/configurar processamento seguro e revisar a política jurídica de privacidade. O resumo atual apenas baixa um arquivo local.
6. Definir URL canônica, sitemap e Open Graph final. A versão entregue usa `noindex,nofollow` e não inventa domínio.
7. Fazer revisão final técnica, comercial e de marca; só então autorizar publicação.

Não houve criação de repositório remoto, envio ao GitHub, registro de Site ou publicação.
