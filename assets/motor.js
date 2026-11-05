/* Astrion — motor matemático didático, v0.6.0 | sem planos comerciais oficiais. */
(function(root, factory) {
  const api = factory();
  if (typeof module !== 'undefined' && module.exports) module.exports = api;
  if (root) root.AstrionMotor = api;
})(typeof window !== 'undefined' ? window : null, function() {
  'use strict';
  function num(v, label, min = 0, max = 100000000000) {
    if (v === '' || v === undefined || v === null || !Number.isFinite(Number(v)))
      throw new Error('Informe um valor válido para ' + label + '.');
    const n = Number(v);
    if (n < min || n > max) throw new Error(label + ' deve estar entre ' + min + ' e ' + max + '.');
    return n;
  }
  function months(v, label) {
    const n = num(v, label, 1, 600);
    if (!Number.isInteger(n)) throw new Error(label + ' deve ser um número inteiro.');
    return n;
  }
  function calcCota(p) {
    const credit = num(p.credit, 'crédito', .01);
    const n = months(p.months, 'prazo');
    const ta = num(p.adminPct, 'taxa de administração', 0, 100) / 100;
    const fr = num(p.reservePct, 'fundo de reserva', 0, 100) / 100;
    const ins = num(p.insuranceMonthly ?? 0, 'seguro mensal');
    const other = num(p.otherMonthly ?? 0, 'outras cobranças mensais');
    const common = credit / n, administration = credit * ta / n, reserve = credit * fr / n;
    const baseMonthly = common + administration + reserve + ins + other;
    return {credit, months: n, common, administration, reserve, insurance: ins, other,
      baseMonthly, sumNominal: baseMonthly * n, adminTotal: credit*ta, reserveTotal: credit*fr};
  }
  function calcReduced(p) {
    const base = calcCota(p);
    const reduction = num(p.reductionPct, 'redução percentual', 0, 100) / 100;
    const elapsed = months(p.scenarioMonth, 'mês hipotético de mudança');
    if (elapsed >= base.months) throw new Error('O mês hipotético deve ser anterior ao término do plano.');
    const scope = p.scope || 'funds';
    if (!['funds','all'].includes(scope)) throw new Error('Base de redução inválida.');
    const eligible = scope === 'funds' ? base.common + base.reserve : base.baseMonthly;
    const diffMonthly = eligible * reduction;
    const reducedMonthly = base.baseMonthly - diffMonthly;
    const pendingAmount = diffMonthly * elapsed;
    const remaining = base.months - elapsed;
    return {...base, reductionPct: reduction*100, scenarioMonth: elapsed, scope,
      reducedMonthly, deferredPerMonth: diffMonthly, pendingAmount,
      reconstructedMonthly: base.baseMonthly + pendingAmount/remaining,
      remainingMonths: remaining};
  }
  function calcBid(p) {
    const credit = num(p.credit, 'crédito', .01);
    const own = num(p.own ?? 0, 'lance com recursos próprios', 0, credit);
    const embedded = num(p.embedded ?? 0, 'lance embutido', 0, credit);
    if (own + embedded > credit + 1e-8) throw new Error('Para este exemplo, a soma dos lances não pode ultrapassar o crédito.');
    const limit = p.embeddedLimitPct === null || p.embeddedLimitPct === '' || p.embeddedLimitPct === undefined
      ? null : num(p.embeddedLimitPct, 'limite contratual de embutido', 0, 100);
    if (limit !== null && embedded > credit*limit/100 + 1e-8) throw new Error('O lance embutido ultrapassa o limite hipotético informado.');
    return {credit, own, embedded, totalBid: own+embedded, bidPct:100*(own+embedded)/credit,
      nominalCreditAfterEmbedded:credit-embedded, embeddedLimitPct:limit};
  }
  function calcFinance(p) {
    const asset = num(p.assetPrice, 'valor do bem', .01);
    const entry = num(p.entry ?? 0, 'entrada', 0, asset);
    const financed = asset - entry;
    const n = months(p.months, 'prazo');
    const r = num(p.interestMonthlyPct, 'taxa de juros mensal', 0, 30)/100;
    const extras = num(p.monthlyExtras ?? 0, 'custos mensais adicionais');
    const upfront = num(p.upfrontExpenses ?? 0, 'custos iniciais adicionais');
    const payment = r === 0 ? financed/n : financed*r/(-Math.expm1(-n*Math.log1p(r)));
    return {asset,entry,financed,months:n,monthlyInterestPct:r*100,pricePayment:payment,
      monthlyExtras:extras,upfrontExpenses:upfront,monthlyDisbursement:payment+extras,
      totalNominal:entry+upfront+(payment+extras)*n, interestNominal:payment*n-financed};
  }
  function calcCommission(p) {
    const credit = num(p.credit, 'crédito', .01);
    const rate = num(p.ratePct, 'comissão nominal', 0, 100);
    const installments = months(p.installments, 'parcelas de comissão');
    return {credit, ratePct:rate, installments, nominalTotal:credit*rate/100,
      arithmeticAverage:credit*rate/100/installments};
  }
  function calcKeys(p) {
    const credit = num(p.credit, 'crédito', .01);
    const appraised = num(p.appraised, 'avaliação do bem usado', 0, credit);
    const own = num(p.own ?? 0, 'complemento em recursos próprios', 0, credit);
    const max = p.assetLimitPct === '' || p.assetLimitPct === null || p.assetLimitPct === undefined
      ? null : num(p.assetLimitPct, 'limite contratual de valor do bem',0,100);
    if (max !== null && appraised > credit*max/100 + 1e-8) throw new Error('Avaliação do bem excede o limite informado para o cenário.');
    if (appraised + own > credit + 1e-8) throw new Error('Para este exemplo, a oferta excede o crédito.');
    return {credit,appraised,own,totalBid:appraised+own,bidPct:100*(appraised+own)/credit,assetLimitPct:max};
  }
  function calcRevenue(p) {
    const approaches=num(p.approaches,'abordagens',0,100000);
    const conversion=num(p.conversion,'conversão',0,100);
    const credit=num(p.credit,'crédito médio',0,100000000);
    const commission=num(p.commission,'comissão hipotética',0,20);
    const sales=approaches*conversion/100;
    return {sales,volume:sales*credit,perUnit:credit*commission/100,total:sales*credit*commission/100};
  }
  return Object.freeze({calcRevenue,calcCota,calcReduced,calcBid,calcFinance,calcCommission,calcKeys});
});
