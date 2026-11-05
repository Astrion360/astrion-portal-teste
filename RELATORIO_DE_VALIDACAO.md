# Revisão visual com o HTML de referência — 05/11/2026

- Nove páginas atualizadas com cabeçalho, menu lateral, tipografia sem serifa, azul-marinho e ciano. Abertura com a fotografia e os logos do arquivo enviado pelo usuário.
- Verificação atual: 36 testes matemáticos aprovados e 359 referências locais verificadas nas nove páginas. Sete simuladores preservados.
- Foram adicionadas regras responsivas para desktop, tablet e celular. A nova aparência ainda precisa de conferência visual no navegador: a ferramenta disponível bloqueou a abertura de arquivos locais. Não se deve considerar os testes visuais históricos abaixo como validação deste novo CSS.
- Nenhum serviço externo foi publicado. Não foram importados rankings nem tabelas de comissão do HTML de referência.
- Para abrir: index.html diretamente em Chrome/Edge, com toda a pasta extraída.

---

## Registro histórico: versão anterior ao redesenho

# Validação da versão local Astrion

Data: 05/11/2026. Estado: implementação local entregue para revisão; sem publicação e sem homologação comercial.

## Resultado técnico

- **36 testes matemáticos aprovados**, executados sobre `assets/motor.js`, o mesmo motor carregado no site. Incluem os 22 testes originais e regressões para receita, cotas fracionárias, valores inválidos, prazo fracionário e estabilidade PRICE com juros muito pequenos.
- **9 páginas e 245 referências locais verificadas**, incluindo arquivos, links, âncoras e os sete módulos de simulação.
- **72 combinações de página/largura** verificadas no navegador: 9 páginas × 320, 375, 430, 768, 1024, 1280, 1440 e 1920 px. Sem overflow geral ou conteúdo textual fora da área visível. A tabela comparativa permite rolagem interna em telas estreitas.
- **56 combinações de simulador/largura**: sete painéis ativos × as mesmas oito larguras. Sem cortes dos controles ou resultados.
- Nenhum erro ou aviso de console observado durante os testes de interface.

## Fluxos observados no navegador

- Menu móvel abre, navega e fecha; Escape recolhe o menu.
- Perfis alternam conteúdo; navegação por setas e seleção ARIA funcionam.
- Modo apresentação avança da home para A Astrion e mantém progresso 2/7, com saída funcional.
- Jornada da cota alterna etapas. FAQ abre respostas. Busca de glossário encontra reserva.
- Todos os sete simuladores apresentam resultados. Alteração de crédito de R$ 100 mil para R$ 200 mil atualizou a parcela de R$ 1.200 para R$ 2.400. Recarregar a página preservou o valor informado.
- Conversão de 101% e lance embutido acima do limite produziram mensagens de validação. Restaurar exemplo e apagar cenários funcionaram.
- Valor extremo aceito pelo motor (crédito de R$ 100 bilhões) manteve o resultado dentro da tela de 375 px.
- Roteiro comparativo foi baixado, refletindo o item selecionado.
- Resumo para contato foi baixado com dados fictícios de teste; a interface confirmou apenas geração local, sem afirmar recebimento pela Astrion.

## Exemplos de referência confirmados

| Ferramenta | Premissas resumidas | Resultado |
|---|---|---|
| Parcela | R$ 100.000, 100 meses, TA 18%, FR 2% | R$ 1.200/mês |
| Redutora | R$ 100.000, 120 meses, redução 50% sobre fundos, mudança no mês 24 | R$ 575; recomposição R$ 1.106,25 |
| Lance | R$ 12.000 próprios + R$ 18.000 embutidos em crédito de R$ 100.000 | 30%; crédito após embutido R$ 82.000 |
| PRICE | Bem R$ 100.000, entrada R$ 20.000, 60 meses, 1,5% ao mês | R$ 2.031,47/mês |
| Comissão | Crédito R$ 100.000, hipótese 3%, 12 parcelas | R$ 3.000 nominais; média R$ 250 |
| Troca de Chaves | Usado R$ 30.000 + recursos R$ 5.000, crédito R$ 100.000 | Oferta hipotética 35% |
| Receita | 60 abordagens, 3% de conversão, crédito R$ 100.000, comissão hipotética 3% | 1,8 cotas matemáticas; R$ 5.400 nominais |

## Correções feitas na revisão

Corrigido o tamanho mínimo do grid/arte da home que causava corte de conteúdo no celular. Ajustada quebra de números extremos nos resultados. Corrigida a exclusão dos cenários para não salvar novamente os exemplos durante o reset.

## Transparência e limites

- Logos oficiais não vieram no material: nomes tipográficos temporários, sem imitação de marcas.
- Tabelas internas de comissão, remuneração da Astrion e demais documentos restritos ficaram fora da pasta de saída.
- Indicadores BCB e taxas históricas não reconciliados não foram apresentados como dados verificados. O comparativo entrega critérios, método, referências nominais e checklist; os gráficos quantitativos permanecem dependentes da validação da base.
- Simuladores não usam grupos, planos ou tabelas homologadas da Âncora. Modalidades na comissão não aplicam percentuais comerciais.
- WhatsApp/e-mail oficial e backend não constam do ZIP: o fluxo de contato entregue gera resumo local. Não existe envio de lead ativo.
- Não há analytics, serviços externos automáticos, fontes remotas ou coleta de dados pessoais.
- Responsividade foi observada no navegador Chromium integrado. Não foi executada uma auditoria externa de acessibilidade, leitor de tela, testes em aparelhos físicos, Safari/Firefox, CET contratual ou homologação jurídica/comercial. A versão inclui estilos para movimento reduzido e impressão, mas não houve teste físico de impressão.
- Servidor local respondeu HTTP 200. Publicação remota e domínio final não foram configurados.

## Fontes e reaproveitamento

Documento mestre, briefing e conteúdo dos pacotes; tokens e direção visual do Pacote 08; SVGs fornecidos; motor e testes do Pacote 06; fórmulas e trilhas do Pacote 07; arquitetura e SEO do Pacote 09.

Consultas complementares em 05/11/2026: [Âncora — site oficial](https://www.ancoraconsorcios.com.br/), [BCB — consórcios](https://www.bcb.gov.br/meubc/faqs/s/consorcio), [BCB — composição das prestações](https://www.bcb.gov.br/meubc/faqs/p/como-e-feito-o-calculo-do-valor-das-prestacoes). As fontes também estão vinculadas no conteúdo educativo. Nenhum dado do site externo foi usado para transformar as simulações em ofertas.
