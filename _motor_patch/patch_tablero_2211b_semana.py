"""Parche 22/11 (k) — Resumen general: la tabla de la semana pasa a 'Actividades ejecutadas · Semana NN' con
Programado (meta diaria × días de la semana hasta la fecha), Ejecutado, Ratio de la semana y Cumplimiento
(ejecutado ÷ programado). Se quita 'en N días con parte': los cuadros de colores ya muestran qué días tienen parte.
Va después de patch_tablero_2211 (orden alfabético)."""

NEW = r"""function semResCard(){
  const E=EST.prod||{},L=D(E.lunes),dl=['L','M','M','J','V','S','D'];
  const fs=frentes().filter(f=>{const x=prodMain(f);return x&&x.meta});
  let dk=null;fs.forEach(f=>prodMain(f).dias.forEach(d=>{if(!d.futuro&&d.ef&&(!dk||d.fecha>dk))dk=d.fecha}));
  const bt=el('button','lnk','Ver producción del día →');bt.onclick=()=>go('dia');
  const c=card('Programado vs ejecutado · '+fdm(L)+' al '+fdm(new Date(+L+6*864e5)),'Actividades ejecutadas · Semana '+String(E.semana||'').replace('S-',''),bt);
  const b=el('div','card-b');const t=el('table','ft dr sr sr2');const th=el('thead');const tr=el('tr');
  [['Frente'],['Día a día'],['Programado','r'],['Ejecutado','r'],['Ratio de la semana','r'],['Cumplimiento']].forEach(([h,c2])=>tr.append(el('th',c2||null,h)));th.append(tr);t.append(th);const tb=el('tbody');
  let n80=0;
  fs.forEach(f=>{const x=prodMain(f);const r=el('tr','mr');r.onclick=()=>go(f.id);
    const c1=el('td','fn');const nb=el('button',null,f.nombre);nb.onclick=e=>{e.stopPropagation();go(f.id)};c1.append(nb);
    const c2=el('td');const st=el('div','wkd');
    x.dias.forEach((d,i)=>{if(i===6&&!(d.v>0))return;const q=x.meta?(d.v||0)/x.meta:0;
      const s=el('span','wd '+(d.futuro?'fu':!d.ef?'np':q>=1?'ok':q>=.8?'warn':'bad'),dl[i]);
      s.title=fd(d.fecha)+': '+(d.futuro?'por venir':!d.ef?'sin parte':fmtU(d.v||0,x.und)+' ('+Math.round(q*100)+' %)');st.append(s)});c2.append(st);
    const np=x.dias.filter((d,i)=>i<6&&!d.futuro).length,prog=x.meta*np,real=x.real||0,p=prog?real/prog:0,sm=p>=1?'ok':p>=.8?'warn':'bad';if(p>=.8)n80++;
    const c3=el('td','r');const s3=el('div','two');s3.append(el('span','mono',fmtU(prog,x.und)),el('small',null,fmtU(x.meta,x.und)+'/día × '+np+(np>1?' días':' día')));c3.append(s3);
    const c4=el('td','r');c4.append(el('span','mono',fmtU(real,x.und)));
    const c5=el('td','r');const s5=el('div','two');s5.append(el('span','mono'+((x.ratio||0)<x.meta*.8?' late':''),fmtU(x.ratio||0,x.und)+'/día'),el('small',null,'meta '+fmtU(x.meta,x.und)+'/día'));c5.append(s5);
    const c6=el('td');const ab=el('div','ab');const tr2=el('div','tr');const ii=el('i');ii.style.width=Math.min(100,p*100)+'%';ii.style.background='var(--'+sm+')';tr2.append(ii);ab.append(tr2,el('b',null,Math.round(p*100)+' %'));c6.append(ab);
    const O=(EST.dia_obs||{})[f.id]||{};const cnt={},ult={};let nota=null;
    x.dias.map(d=>d.fecha).forEach(k=>{const o=O[k];if(!o)return;const vis={};
      (o.rx||[]).forEach(z=>{const ca=z.causa||'Otra';if(!vis[ca]){vis[ca]=1;cnt[ca]=(cnt[ca]||0)+1}if(z.que)ult[ca]=z.que});
      if(!(o.rx||[]).length)(o.causas||[]).forEach(ca=>{if(!vis[ca]){vis[ca]=1;cnt[ca]=(cnt[ca]||0)+1}});
      if((o.notas||[]).length)nota=o.notas[0]});
    const top=Object.entries(cnt).sort((a,b)=>b[1]-a[1]);let txt='—';
    if(top.length){const [ca,n]=top[0];txt=ca+' ('+n+(n>1?' días':' día')+')'+(ult[ca]?': '+ult[ca]:'');if(txt.length>140)txt=txt.slice(0,137)+'…';if(top[1])txt+=' · también '+top[1][0]+' ('+top[1][1]+(top[1][1]>1?' días':' día')+')'}
    else if(nota){txt=nota.length>130?nota.slice(0,127)+'…':nota}
    r.append(c1,c2,c3,c4,c5,c6);tb.append(r);
    const r2=el('tr','rxr');r2.onclick=()=>go(f.id);const c7=el('td');c7.colSpan=6;if(txt!=='—'){c7.append(el('b',null,'Lo que más frenó: '),document.createTextNode(txt))}else c7.append(document.createTextNode('Sin restricciones reportadas en la semana.'));r2.append(c7);tb.append(r2)});
  t.append(tb);const sc=el('div','scroll');sc.append(t);b.append(sc);
  b.append(el('div','pnote',n80+' de '+fs.length+' frentes cumplen el 80 % o más de lo programado'+(dk?' (partes hasta el '+fd(dk)+')':'')+'. Programado = meta diaria × días de la semana (lunes a sábado) hasta la fecha. Ratio = lo ejecutado ÷ días con parte. Cumplimiento = ejecutado ÷ programado. Cada cuadro es un día: verde ≥ meta · ámbar 80–99 % · rojo < 80 % · gris sin parte.'));
  c.append(b);return c;
}
(function(){const s=document.createElement('style');s.textContent=".sr2 tr.mr td:nth-child(5),.sr2 tr.mr td:nth-child(6){width:1px;white-space:nowrap}.sr2 tr.mr td{border-bottom:0;padding-bottom:4px}.sr2 tr.rxr td{padding-top:0;padding-bottom:12px;font-size:12px;color:var(--muted);line-height:1.4;white-space:normal}.sr2 tr.rxr td b{color:var(--ink);font-weight:600}.sr2 tr.rxr{cursor:pointer}";document.head.append(s)})();
"""


def old_block(h):
    i = h.index('function semResCard(){')
    j = h.index('\n}\n', i) + 3
    return i, j


def patch_html(h):
    if "'Actividades ejecutadas · Semana '" in h:
        return h
    i, j = old_block(h)
    return h[:i] + NEW + h[j:]


def aplicar(motor):
    from pathlib import Path
    f = Path(motor) / 'tablero.html'
    a = f.read_text(encoding='utf8')
    b = patch_html(a)
    if b != a:
        f.write_text(b, encoding='utf8')
        return ['tablero.html']
    return []


if __name__ == '__main__':
    import sys
    p = sys.argv[1]
    h = patch_html(open(p, encoding='utf8').read())
    open(p, 'w', encoding='utf8').write(h)
    print('ok')
