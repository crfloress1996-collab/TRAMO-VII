"""Parche 22/11 — Resumen general: en lugar de 'Producción del día' (que ya tiene su propia página) va el
resumen de la semana: día a día por frente, lo hecho en la semana, el cumplimiento y la restricción que más pesó.
Va después de patch_tablero_2111 (orden alfabético)."""

FN = r"""(function(){const s=document.createElement('style');s.textContent=".wkd{display:flex;gap:3px}.wd{width:22px;height:22px;border-radius:5px;display:inline-flex;align-items:center;justify-content:center;font:700 10.5px var(--f-ui,inherit);color:#fff;flex:none}.wd.ok{background:var(--ok)}.wd.warn{background:var(--warn)}.wd.bad{background:var(--bad)}.wd.np{background:var(--track);color:var(--muted)}.wd.fu{background:transparent;border:1px dashed var(--line);color:var(--muted)}.sr td:nth-child(2),.sr td:nth-child(3),.sr td:nth-child(4){width:1px;white-space:nowrap}.sr .ab{min-width:150px}.sr td:first-child{min-width:140px}.sr td:last-child small{max-width:none}";document.head.append(s)})();
function semResCard(){
  const E=EST.prod||{},L=D(E.lunes),dl=['L','M','M','J','V','S','D'];
  const fs=frentes().filter(f=>{const x=prodMain(f);return x&&x.meta});
  let dk=null;fs.forEach(f=>prodMain(f).dias.forEach(d=>{if(!d.futuro&&d.ef&&(!dk||d.fecha>dk))dk=d.fecha}));
  const bt=el('button','lnk','Ver producción del día →');bt.onclick=()=>go('dia');
  const c=card('Producción de la semana '+(E.semana||'')+' · '+fdm(L)+' al '+fdm(new Date(+L+6*864e5)),'Cómo vamos en la semana',bt);
  const b=el('div','card-b');const t=el('table','ft dr sr');const th=el('thead');const tr=el('tr');
  [['Frente'],['Día a día'],['Hecho en la semana','r'],['Cumplimiento'],['Lo que más frenó']].forEach(([h,c2])=>tr.append(el('th',c2||null,h)));th.append(tr);t.append(th);const tb=el('tbody');
  let n80=0;
  fs.forEach(f=>{const x=prodMain(f);const r=el('tr');r.onclick=()=>go(f.id);
    const c1=el('td','fn');const nb=el('button',null,f.nombre);nb.onclick=e=>{e.stopPropagation();go(f.id)};c1.append(nb);
    const c2=el('td');const st=el('div','wkd');
    x.dias.forEach((d,i)=>{if(i===6&&!(d.v>0))return;const q=x.meta?(d.v||0)/x.meta:0;
      const s=el('span','wd '+(d.futuro?'fu':!d.ef?'np':q>=1?'ok':q>=.8?'warn':'bad'),dl[i]);
      s.title=fd(d.fecha)+': '+(d.futuro?'por venir':!d.ef?'sin parte':fmtU(d.v||0,x.und)+' ('+Math.round(q*100)+' %)');st.append(s)});c2.append(st);
    const c3=el('td','r');const h3=el('div','two');h3.append(el('span','mono',fmtU(x.real||0,x.und)),el('small',null,x.nd?('en '+x.nd+(x.nd>1?' días':' día')+' con parte'):'sin partes'));c3.append(h3);
    const c4=el('td');const p=x.pct||0,sm=x.sem||(p>=1?'ok':p>=.8?'warn':'bad');if(p>=.8)n80++;
    const ab=el('div','ab');const tr2=el('div','tr');const ii=el('i');ii.style.width=Math.min(100,p*100)+'%';ii.style.background='var(--'+sm+')';tr2.append(ii);ab.append(tr2,el('b',null,Math.round(p*100)+' %'));c4.append(ab);
    const c5=el('td');const O=(EST.dia_obs||{})[f.id]||{};const cnt={},ult={};let nota=null;
    x.dias.map(d=>d.fecha).forEach(k=>{const o=O[k];if(!o)return;const vis={};
      (o.rx||[]).forEach(z=>{const ca=z.causa||'Otra';if(!vis[ca]){vis[ca]=1;cnt[ca]=(cnt[ca]||0)+1}if(z.que)ult[ca]=z.que});
      if(!(o.rx||[]).length)(o.causas||[]).forEach(ca=>{if(!vis[ca]){vis[ca]=1;cnt[ca]=(cnt[ca]||0)+1}});
      if((o.notas||[]).length)nota=o.notas[0]});
    const top=Object.entries(cnt).sort((a,b)=>b[1]-a[1]);let txt='—';
    if(top.length){const [ca,n]=top[0];txt=ca+' ('+n+(n>1?' días':' día')+')'+(ult[ca]?': '+ult[ca]:'');if(txt.length>140)txt=txt.slice(0,137)+'…';if(top[1])txt+=' · también '+top[1][0]+' ('+top[1][1]+(top[1][1]>1?' días':' día')+')'}
    else if(nota){txt=nota.length>130?nota.slice(0,127)+'…':nota}
    c5.append(el('small',null,txt));
    r.append(c1,c2,c3,c4,c5);tb.append(r)});
  t.append(tb);const sc=el('div','scroll');sc.append(t);b.append(sc);
  b.append(el('div','pnote',n80+' de '+fs.length+' frentes van sobre el 80 % de su meta'+(dk?' (partes hasta el '+fd(dk)+')':'')+'. Cumplimiento = lo hecho ÷ (meta diaria × días con parte). Cada cuadro es un día: verde ≥ meta · ámbar 80–99 % · rojo < 80 % · gris sin parte.'));
  c.append(b);return c;
}
"""

OLD = 'box.append(diaResCard(),linearCard(),'
NEW = 'box.append(semResCard(),linearCard(),'


def patch_html(h):
    if 'function semResCard' not in h:
        assert h.count('function alertsCard(){') == 1, 'alertsCard'
        h = h.replace('function alertsCard(){', FN + 'function alertsCard(){', 1)
    if NEW not in h:
        assert h.count(OLD) == 1, 'resumen: diaResCard'
        h = h.replace(OLD, NEW, 1)
    return h


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
