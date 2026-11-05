/* Protótipo Astrion — controladores de interface sem API e sem armazenamento. */
(function(){
 'use strict';
 const M = window.AstrionMotor;
 const tabs = [...document.querySelectorAll('[role="tab"]')];
 const panels = [...document.querySelectorAll('[role="tabpanel"]')];

 const money = v => Number(v).toLocaleString('pt-BR',{style:'currency',currency:'BRL',minimumFractionDigits:2,maximumFractionDigits:2});
 const pct = v => Number(v).toLocaleString('pt-BR',{minimumFractionDigits:2,maximumFractionDigits:2})+'%';
 const row=(label,value)=>`<div class="result-row"><span>${label}</span><strong>${value}</strong></div>`;
 const note=msg=>`<p class="explain-note">${msg}</p>`;
 const box=(caption,hero,subtitle,other='',noteText='')=>
  `<div class="result-caption">${caption}</div><div class="hero-value">${hero}</div><div class="result-sub">${subtitle}</div>${other}${note(noteText)}`;
 function values(form){return Object.fromEntries(new FormData(form).entries());}
 function draw(id) {
   const form=document.getElementById('form-'+id), out=document.getElementById('result-'+id);
   if(!form||!out)return;
   const p=values(form); let html='';
   try{
     switch(id){
     case 'cota':{
       const r=M.calcCota(p), parts=[['common',r.common],['admin',r.administration],['reserve',r.reserve],['extras',r.insurance+r.other]];
       const bars=parts.map(([klass,n])=>`<span class="${klass}" style="width:${(n/r.baseMonthly*100).toFixed(3)}%"></span>`).join('');
       html=box('Parcela mensal ilustrativa',money(r.baseMonthly),'Divisão uniforme, sem atualizações do crédito',
         `<div class="bar" aria-label="Distribuição aproximada da prestação">${bars}</div><div class="result-rows">${row('Fundo comum',money(r.common))}${row('Administração',money(r.administration))}${row('Fundo de reserva',money(r.reserve))}${row('Seguros e outros',money(r.insurance+r.other))}${row('Soma nominal das prestações',money(r.sumNominal))}</div>`,
         'As taxas podem ser antecipadas ou distribuídas de forma desigual. Não inclui reajustes, custos excepcionais nem eventos da cota.');
       break;}
     case 'reduzida':{
       const r=M.calcReduced(p);
       html=box('Prestação hipotética reduzida',money(r.reducedMonthly),`Redução de ${pct(r.reductionPct)} ${r.scope==='funds'?'sobre fundo comum e reserva':'sobre a parcela integral'}`,
       `<div class="result-rows">${row('Parcela uniforme de referência',money(r.baseMonthly))}${row('Valor não recolhido por mês',money(r.deferredPerMonth))}${row('Diferido em '+r.scenarioMonth+' meses',money(r.pendingAmount))}${row('Parcela recomposta hipotética',money(r.reconstructedMonthly))}${row('Meses remanescentes',String(r.remainingMonths))}</div>`,
       'O mês escolhido é apenas uma hipótese matemática, não uma previsão de contemplação. Recomposição, reajustes e rubricas reduzíveis dependem do regulamento real.');
       break;}
     case 'lance':{
       const r=M.calcBid(p);
       html=box('Lance total hipotético',pct(r.bidPct),'Proporção da oferta sobre o crédito usado como base ilustrativa',
       `<div class="result-rows">${row('Recursos próprios ofertados',money(r.own))}${row('Lance embutido',money(r.embedded))}${row('Oferta total',money(r.totalBid))}${row('Crédito após dedução do embutido',money(r.nominalCreditAfterEmbedded))}${row('Limite do embutido',r.embeddedLimitPct===null?'Não informado':pct(r.embeddedLimitPct))}</div>`,
       'A base percentual e os limites reais dependem do grupo. Lance vencedor se destina a prestações vincendas; não há garantia de contemplação.');
       break;}
     case 'fin':{
       const r=M.calcFinance(p);
       html=box('Prestação PRICE estimada',money(r.pricePayment),'Modelo de juros mensais informado, sem apuração integral do CET',
       `<div class="result-rows">${row('Principal financiado',money(r.financed))}${row('Entrada',money(r.entry))}${row('Juros nominais somados',money(r.interestNominal))}${row('Desembolso mensal com extras',money(r.monthlyDisbursement))}${row('Total nominal (com entrada)',money(r.totalNominal))}</div>`,
       'Financiamento normalmente permite adquirir o bem após aprovação e liberação; consórcio depende de contemplação. Não comparar os totais sem considerar o momento de uso, reajustes, tributos e CET contratual.');
       break;}
     case 'com':{
       const r=M.calcCommission(p), mode='Premissas livres · '+p.context;
       html=box('Comissão nominal ilustrativa',money(r.nominalTotal),`${mode} · ${pct(r.ratePct)} sobre o crédito comercializado`,
       `<div class="result-rows">${row('Crédito de referência',money(r.credit))}${row('Comissão percentual',pct(r.ratePct))}${row('Quantidade referencial de parcelas',String(r.installments))}${row('Média matemática por parcela',money(r.arithmeticAverage))}</div>`,
       'Percentuais são hipóteses livres, sem tabela comercial aplicada. A média não representa pagamentos iguais, liquidação imediata ou ausência de estornos. Elegibilidade e repasse exigem acordo vigente.');
       break;}
     case 'receita':{
       const r=M.calcRevenue(p);
       html=box('Comissão nominal do cenário',money(r.total),'Hipóteses de produção e remuneração, sem vínculo contratual',
       '<div class="result-rows">'+row('Cotas matemáticas no mês',r.sales.toLocaleString('pt-BR',{maximumFractionDigits:3}))+row('Crédito nominal do cenário',money(r.volume))+row('Comissão nominal por cota',money(r.perUnit))+'</div>',
       'Cotas fracionárias representam média matemática. Não é previsão de vendas, fluxo de caixa nem lucro. Tributos, despesas, inadimplência e calendário de repasses não estão calculados.');
       break;}
     case 'chaves':{
       const r=M.calcKeys(p);
       html=box('Oferta baseada no bem usado',pct(r.bidPct),'Exemplo condicionado à existência de modalidade contratual',
       `<div class="result-rows">${row('Avaliação do usado',money(r.appraised))}${row('Complemento com recursos próprios',money(r.own))}${row('Oferta hipotética total',money(r.totalBid))}${row('Valor nominal da carta',money(r.credit))}${row('Limite contratual para bem usado',r.assetLimitPct===null?'Não informado':pct(r.assetLimitPct))}</div>`,
       'O bem avaliado não equivale automaticamente a dinheiro disponível. Não foi calculado crédito líquido ou pagamento ao vendedor: o fluxo depende da modalidade aprovada e do regulamento. Não é lance embutido.');
       break;}
     }
     const formulas={
       cota:'Parcela = crédito × (1 + administração total/100 + reserva total/100) ÷ meses + seguro mensal + outras cobranças. Soma nominal = parcela × meses. Sem reajustes e com distribuição uniforme.',
       reduzida:'Elegível = fundo comum + reserva (ou parcela integral, se selecionado). Diferença mensal = elegível × redução/100. Diferido = diferença × mês hipotético. Recomposição = parcela-base + diferido ÷ meses restantes. Não é a regra contratual de uma administradora.',
       lance:'Lance total = recursos próprios + embutido. Percentual ilustrativo = lance total ÷ crédito × 100. Crédito após embutido = crédito − embutido. A base e os limites reais dependem do grupo.',
       fin:'Principal P = bem − entrada. Com i = juros mensais/100 e n = meses: PRICE = P × i ÷ [1 − (1+i) elevado a −n]. Se i = 0, PRICE = P/n. Total = entrada + despesas iniciais + n × (PRICE + extras mensais). Não apura CET completo.',
       com:'Comissão nominal = crédito × percentual/100. Média aritmética por parcela = comissão nominal ÷ parcelas informadas. A modalidade serve apenas de contexto; não preenche nem confirma condições comerciais.',
       chaves:'Oferta hipotética = avaliação do usado + complemento próprio. Percentual ilustrativo = oferta ÷ crédito × 100. Não calcula crédito líquido, recebimento pelo vendedor ou elegibilidade real.',
       receita:'Cotas matemáticas = abordagens × conversão/100. Crédito nominal = cotas × crédito médio. Comissão nominal = crédito nominal × comissão/100. Comissão por cota = crédito médio × comissão/100. Não arredondamos cotas antes do cálculo financeiro.'
     };
     if(id==='fin'){
       const f=M.calcFinance(p),cota=values(document.getElementById('form-cota'));
       if(f.financed>0){const c=M.calcCota({...cota,credit:f.financed,months:p.months});
       html+='<div class="finance-comparison"><h3>Mesma base, mesmo prazo</h3>'+row('Crédito comparado',money(f.financed))+row('Prazo em ambos',p.months+' meses')+row('Parcela consórcio ilustrativa',money(c.baseMonthly))+row('Parcela PRICE (sem extras)',money(f.pricePayment))+row('Soma consórcio + entrada',money(c.sumNominal+f.entry))+row('Total financiamento com despesas',money(f.totalNominal))+'<p>Consórcio usa as taxas, seguro e outros custos da aba Parcela, sobre o saldo após a entrada. Sem reajustes. Entrada é recurso próprio reservado no cenário de consórcio; disponibilidade de aquisição difere: financiamento após aprovação, consórcio após contemplação e requisitos. Os totais não definem qual opção é melhor.</p></div>';}
     }
     html+='<details class="formula-box"><summary>Ver memória de cálculo e limites</summary><div><p>'+formulas[id]+'</p><p>Premissas livres · motor v0.6.0 / receita v1.0 · referência didática 05/11/2026.</p></div></details>';
     out.classList.remove('error');out.innerHTML=html;
   }catch(e){out.classList.add('error');out.innerHTML='<p class="result-caption">Revise os campos</p><p class="error-msg"></p>';out.querySelector('.error-msg').textContent=e.message;}
 }
 function switchTab(id,focus=false){
  for(const tab of tabs){const on=tab.dataset.tab===id;tab.classList.toggle('active',on);tab.setAttribute('aria-selected',on?'true':'false');tab.tabIndex=on?0:-1;if(on&&focus)tab.focus();}
  for(const panel of panels)panel.hidden=panel.id!=='panel-'+id;
  draw(id);
  window.AstrionSession?.set("astrion.activeSimulator",id);
 }
 tabs.forEach((tab,i)=>{tab.addEventListener('click',()=>switchTab(tab.dataset.tab));tab.addEventListener('keydown',e=>{if(!['ArrowLeft','ArrowRight','Home','End'].includes(e.key))return;e.preventDefault();let n=e.key==='Home'?0:e.key==='End'?tabs.length-1:(i+(e.key==='ArrowRight'?1:-1)+tabs.length)%tabs.length;switchTab(tabs[n].dataset.tab,true);});});
 let clearing=false;
 document.querySelectorAll('form').forEach(form=>{
   const id=form.id.replace('form-','');
   form.addEventListener('submit',e=>e.preventDefault());
   form.addEventListener('input',()=>{persist(form);draw(id);});
   form.addEventListener('change',()=>{persist(form);draw(id);});
   form.addEventListener('reset',()=>{const erase=clearing;requestAnimationFrame(()=>{if(!erase)persist(form);draw(id);});});
 });
 function persist(form){window.AstrionSession?.set('astrion.sim.'+form.id,JSON.stringify(values(form)));}
 document.querySelectorAll('form').forEach(form=>{try{const saved=JSON.parse(window.AstrionSession?.get('astrion.sim.'+form.id)||'null');if(saved)for(const [key,val] of Object.entries(saved)){if(form.elements[key])form.elements[key].value=val;}}catch{}});
 for(const tab of tabs)draw(tab.dataset.tab);
 function fromHash(){const id=location.hash.slice(1)||window.AstrionSession?.get('astrion.activeSimulator')||'cota';switchTab(tabs.some(t=>t.dataset.tab===id)?id:'cota');}
 fromHash();window.addEventListener('hashchange',fromHash);
 document.getElementById('clear-simulations').addEventListener('click',()=>{clearing=true;document.querySelectorAll('form').forEach(form=>{window.AstrionSession?.remove('astrion.sim.'+form.id);form.reset();});clearing=false;window.AstrionSession?.remove('astrion.activeSimulator');document.getElementById('simulation-status').textContent='Cenários removidos; exemplos restaurados.';});
 document.getElementById('print-simulation').addEventListener('click',()=>{const active=tabs.find(t=>t.getAttribute('aria-selected')==='true').dataset.tab;draw(active);const panel=document.getElementById('panel-'+active);let date=panel.querySelector('.print-date');if(!date){date=document.createElement('p');date.className='print-date';panel.prepend(date);}date.textContent='Cenário calculado em '+new Date().toLocaleString('pt-BR')+' · Simulação educativa, sem oferta ou garantia de contemplação.';window.print();});
})();
