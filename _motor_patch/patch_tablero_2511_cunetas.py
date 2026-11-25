"""Parche 25/11 — Cunetas: lista de tramos por km (hoja TRAMOS del CF de cunetas) con metrado, hecho y falta
en metros y en paños, avance y estado. Agrupada por sector (cabecera con el total del sector, se abre y cierra
con un toque; el sector terminado arranca cerrado). Reemplaza la tarjeta 'Avance por sector' de cunetas.
Va después de patch_muros_2311 (orden alfabético), porque usa sus marcas en renderFrente."""

PY_A = "EST['prod'] = dict(semana=f\"S-{LUN.isocalendar()[1]}\""
PY_ADD = '''# ---------- cunetas: lista por tramo (hoja TRAMOS del CF de cunetas) — parche 25/11 cunetas lista
try:
    CU_LISTA = []
    _fx = lambda x: iso(x) if isinstance(x, (dt.datetime, dt.date)) else (str(x).strip() if x not in (None, '') else None)
    for r in WB['cu']['TRAMOS'].iter_rows(min_row=10, max_row=400, values_only=True):
        if r[0] and str(r[0]).strip().upper().startswith('TOTAL'):
            break
        if not r[0] or not isinstance(r[8], (int, float)) or not r[8]:
            continue
        _est = str(r[18] or '').strip().upper()
        if _est == 'NO VA':
            continue
        CU_LISTA.append(dict(id=str(r[0]).strip(), comp=r[1], sec=str(r[2] or '').strip().upper(), desde=num(r[5]), hasta=num(r[6]),
                             lado=r[7], largo=num(r[8]), panos=num(r[9]), ref=txt(r[10]), hecho=num(r[19]) or 0, pct=num(r[20]),
                             falta=num(r[21]) or 0, panos_falta=num(r[22]) or 0, estado=_est or 'PENDIENTE',
                             f1=_fx(r[23]), f2=_fx(r[24]), obs=txt(r[25])))
    for _f0 in FR:
        if _f0['id'] == 'cunetas':
            _f0['cu_lista'] = CU_LISTA
except Exception as e:
    print('cunetas lista', e)
'''

FN = r"""(function(){const s=document.createElement('style');s.textContent=".cul tr.cus td{background:var(--band);font-size:12px;color:var(--muted);padding:8px 10px;cursor:pointer;user-select:none}.cul tr.cus td b{color:var(--ink);font-weight:700}.cul tr.cus .tg{display:inline-block;width:16px;color:var(--ink);font-weight:700}.cul tr.curun td{background:color-mix(in srgb,var(--amber) 9%,transparent)}.cul td{white-space:nowrap;vertical-align:top}.cul .ab{min-width:90px;margin-top:4px}.ft.cul{min-width:620px}.cul td,.cul th{padding-left:8px;padding-right:8px}.cul td .two small.wr{white-space:normal;max-width:260px}.cul .est{font-size:11.5px;font-weight:600;margin-top:3px;white-space:normal;max-width:140px}.cul td .two small.wr{max-width:220px}.cul td .two small{white-space:nowrap}.cul td.r .two{align-items:flex-end}.cul td.kmc{font-family:var(--f-mono);font-weight:700;color:var(--ink);font-size:13px}.cul tr.kmt td{border-top:2px solid var(--line)}.cul tfoot td{font-weight:700;border-top:2px solid var(--line)}.cul td.late b{color:var(--bad)}";document.head.append(s)})();
const CU_OPEN={};
function cunetasCard(f){
  const ORDS={XIII:1,XIV:2,XV:3},SN={XIII:'mejoramiento',XIV:'conservación periódica',XV:'mejoramiento'};
  const L=[...f.cu_lista].sort((a,b)=>((ORDS[a.sec]||9)-(ORDS[b.sec]||9))||((a.desde||0)-(b.desde||0)));
  const secs=[...new Set(L.map(t=>t.sec))];
  const c=card(f.nombre,'Tramos de cuneta por km','en metros (m) y paños de 3 m');
  const b=el('div','card-b');const t=el('table','ft cul');const th=el('thead');const tr=el('tr');
  [['Km'],['Tramo · lado'],['Metrado','r'],['Hecho','r'],['Falta','r'],['Avance']].forEach(([h,cc])=>tr.append(el('th',cc||null,h)));th.append(tr);t.append(th);
  const tb=el('tbody');const T={largo:0,hecho:0,falta:0,panos:0,ph:0,pf:0,n:0};
  const m1=v=>{const r=Math.round((v||0)*10)/10;return fmt(r,r%1?1:0)};
  const two=(a,s,cls)=>{const td=el('td',cls||null);const d=el('div','two');d.append(el('b',null,a));if(s)d.append(el('small',null,s));td.append(d);return td};
  const bar=(p,col)=>{const ab=el('div','ab');const t2=el('div','tr');const ii=el('i');ii.style.width=Math.min(100,Math.max(0,p*100))+'%';ii.style.background=col;t2.append(ii);ab.append(t2,el('b',null,Math.round(p*100)+' %'));return ab};
  secs.forEach(sec=>{
    const R=L.filter(x=>x.sec===sec);
    const S={largo:0,hecho:0,falta:0,panos:0,ph:0,pf:0};
    R.forEach(m=>{const term=String(m.estado).startsWith('TERM');const pn=m.panos||0,pf=term?0:(m.panos_falta||0);
      S.largo+=m.largo||0;S.hecho+=m.hecho||0;S.falta+=m.falta||0;if(m.panos!=null){S.panos+=pn;S.ph+=pn-pf;S.pf+=pf}});
    const sp=S.largo?S.hecho/S.largo:0;
    if(!(sec in CU_OPEN))CU_OPEN[sec]=sp<0.999;
    const nt=R.filter(x=>!x.nota).length;
    const sr=el('tr','cus');const sd=el('td');sd.colSpan=6;const tg=el('span','tg',CU_OPEN[sec]?'▾':'▸');
    sd.append(tg,el('b',null,'Sector '+sec+(SN[sec]?' · '+SN[sec]:'')),document.createTextNode('  ·  '+(nt?nt+(nt>1?' tramos':' tramo')+' · ':'')+'hecho '+fmt(S.hecho)+' de '+fmt(S.largo)+' m ('+Math.round(sp*100)+' %) · '+(S.falta>0.5?'faltan '+fmt(S.falta)+' m'+(S.pf?' = '+fmt(S.pf)+' paños':''):'terminado')));
    sr.append(sd);tb.append(sr);
    const rows=[];let kk=null;
    R.forEach(m=>{
      const est=String(m.estado||'PENDIENTE').toUpperCase(),sm=est.startsWith('TERM')?'ok':est.includes('PROCESO')?'warn':'na';
      const kmn=m.desde!=null?Math.floor(m.desde/1000):null;const nk=kmn!==kk;
      const r=el('tr',(sm==='warn'?'curun':'')+(nk&&kk!==null?' kmt':'')||null);kk=kmn;
      r.append(el('td','kmc',nk&&kmn!=null?String(kmn):''));
      const lado=String(m.lado||'').toUpperCase().startsWith('IZQ')?'Izq.':String(m.lado||'').toUpperCase().startsWith('DER')?'Der.':(m.lado||'');
      {const c2=two(m.desde!=null?km(m.desde)+' – '+km(m.hasta):'—',m.nota||[m.id,lado].filter(Boolean).join(' · '));if(m.nota)c2.querySelector('small').className='wr';r.append(c2)}
      const pn=m.panos,pf=sm==='ok'?0:(m.panos_falta||0);
      r.append(two(m1(m.largo),pn!=null?fmt(pn)+' paños':null,'r mono'));
      r.append(two(m1(m.hecho),pn!=null?fmt(pn-pf)+' paños':null,'r mono'));
      r.append(two((m.falta>0.05?m1(m.falta):'0'),pn!=null?fmt(pf)+' paños':null,'r mono'+(m.falta>0.05?' late':'')));
      const p=m.pct!=null?m.pct:(m.largo?(m.hecho||0)/m.largo:0);
      const ca=el('td');ca.append(bar(p,'var(--'+(sm==='na'?'faint':sm)+')'));
      const ul=m.f2==='previo'?'antes del 14/10':(m.f2&&/^\d{4}-/.test(m.f2)?'último '+fdm(D(m.f2)):'');
      const es=el('div','est',(sm==='ok'?'Terminado':sm==='warn'?'En proceso':'Pendiente')+(ul?' · '+ul:''));es.style.color=sm==='na'?'var(--muted)':'var(--'+sm+')';ca.append(es);r.append(ca);
      const tip=[m.ref,m.obs].filter(Boolean).join(' · ');if(tip)r.title=tip;
      if(!CU_OPEN[sec])r.style.display='none';rows.push(r);tb.append(r)});
    sr.onclick=()=>{CU_OPEN[sec]=!CU_OPEN[sec];tg.textContent=CU_OPEN[sec]?'▾':'▸';rows.forEach(r=>r.style.display=CU_OPEN[sec]?'':'none')};
    T.largo+=S.largo;T.hecho+=S.hecho;T.falta+=S.falta;T.panos+=S.panos;T.ph+=S.ph;T.pf+=S.pf;T.n+=nt});
  t.append(tb);const tf=el('tfoot');const fr2=el('tr');const f1=el('td');f1.colSpan=2;f1.textContent='Total Tramo VII · '+T.n+' tramos';
  const tt=(a,s,cls)=>two(a,s,cls);
  fr2.append(f1,tt(fmt(T.largo),T.panos?fmt(T.panos)+' paños':null,'r mono'),tt(fmt(T.hecho),T.panos?fmt(T.ph)+' paños':null,'r mono'),tt(fmt(T.falta),T.panos?fmt(T.pf)+' paños':null,'r mono late'));
  const fa=el('td');fa.append(bar(T.largo?T.hecho/T.largo:0,'var(--navy)'));fr2.append(fa);tf.append(fr2);t.append(tf);
  const sc=el('div','scroll');sc.append(t);b.append(sc);
  b.append(el('div','pnote','Tramos y metrado de la hoja TRAMOS del control de cunetas (XIII replanteo Set final, XIV replanteo R2, XV metrado P.M.). Hecho sale del REGISTRO del capataz, paños de 3 m. Toca un sector para abrir o cerrar su lista. En ámbar los tramos en proceso.'));
  c.append(b);return c;
}
"""

JS_O = "if(f.zonas)box.append(corteCard(f));"
JS_N = "if(f.cu_lista&&f.cu_lista.length)box.append(cunetasCard(f));if(f.zonas)box.append(corteCard(f));"

CO_O = "if(f.comp&&!(f.muros_lista&&f.muros_lista.length))box.append(compCard(f));"
CO_N = "if(!(f.cu_lista&&f.cu_lista.length))" + CO_O   # cunetas: solo la lista (deja intacta la marca del parche de muros)


def patch_py(s):
    if 'parche 25/11 cunetas lista' in s:
        return s
    assert s.count(PY_A) == 1, 'ancla EST prod'
    return s.replace(PY_A, PY_ADD + PY_A, 1)


def patch_html(h):
    if 'function cunetasCard' not in h:
        assert h.count(JS_O) == 1, 'corteCard en renderFrente'
        h = h.replace(JS_O, JS_N, 1)
        assert h.count('function alertsCard(){') == 1
        h = h.replace('function alertsCard(){', FN + 'function alertsCard(){', 1)
    if CO_N not in h:
        assert h.count(CO_O) == 1, 'compCard (muros) en renderFrente'
        h = h.replace(CO_O, CO_N, 1)
    return h


def aplicar(motor):
    from pathlib import Path
    motor, msg = Path(motor), []
    for nom, fn in (('dash_data.py', patch_py), ('tablero.html', patch_html)):
        f = motor / nom
        a = f.read_text(encoding='utf8')
        b = fn(a)
        if b != a:
            f.write_text(b, encoding='utf8')
            msg.append(nom)
    return msg


if __name__ == '__main__':
    import sys
    p = sys.argv[1]
    h = patch_html(open(p, encoding='utf8').read())
    open(p, 'w', encoding='utf8').write(h)
    print('ok')
