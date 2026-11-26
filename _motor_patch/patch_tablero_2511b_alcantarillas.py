"""Parche 25/11 (b) — Alcantarillas: lista de estructuras por km (hoja PROGRAMA del CF de obras de arte) con lo que
lleva cada una (cabezal de entrada, cabezal de salida, emboquillado, disipador: hecho / falta / no lleva) y su estado.
Agrupada por sector como la de cunetas (usa sus estilos .cul). Reemplaza la tarjeta 'Lo que falta' de alcantarillas.
Va después de patch_tablero_2511_cunetas (orden alfabético), porque usa sus marcas en renderFrente."""

PY_A = "EST['prod'] = dict(semana=f\"S-{LUN.isocalendar()[1]}\""
PY_ADD = '''# ---------- alcantarillas: lista por estructura (hoja PROGRAMA del CF de obras de arte) — parche 25/11 alcantarillas lista
try:
    OA_LISTA = []
    _fx = lambda x: iso(x) if isinstance(x, (dt.datetime, dt.date)) else (str(x).strip() if x not in (None, '') else None)
    _el = lambda x: (1 if x == 1 else 0) if isinstance(x, (int, float)) and not isinstance(x, bool) else None   # None = no lleva
    for r in WB['oa']['PROGRAMA'].iter_rows(min_row=7, max_row=300, values_only=True):
        if r[0] and str(r[0]).strip().upper().startswith('TOTAL'):
            break
        if not r[1] or not r[2]:
            continue
        _m = re.search(r'(\\d+)\\s*\\+\\s*(\\d+(?:\\.\\d+)?)', str(r[6] or r[1]))
        OA_LISTA.append(dict(cod=str(r[1]).strip(), tipo=str(r[2]).strip(), clase=txt(r[3]), comp=txt(r[4]), sec=str(r[5] or '').strip().upper(),
                             km=(int(_m.group(1)) * 1000 + float(_m.group(2))) if _m else None, largo=num(r[7]),
                             ent=_el(r[10]), sal=_el(r[11]), emb=_el(r[20]), dis=_el(r[21]), avance=num(r[12]),
                             estado=str(r[13] or '').strip().upper() or 'PENDIENTE', fin=_fx(r[17]), atraso=num(r[18]),
                             proy=_fx(r[19]), obs=txt(r[52]) if len(r) > 52 else None))
    for _f0 in FR:
        if _f0['id'] == 'alcantarillas':
            _f0['oa_lista'] = OA_LISTA
except Exception as e:
    print('alcantarillas lista', e)
'''

FN = r"""/*alc-v2*/(function(){const s=document.createElement('style');s.textContent=".cul tr.cus td{white-space:normal}.oal th.c,.oal td.c{text-align:center}.oal td.c{vertical-align:middle}.oal .mk{display:inline-flex;align-items:center;justify-content:center;width:22px;height:22px;border-radius:50%;font-size:12px;font-weight:700;line-height:1}.oal .mk.si{background:color-mix(in srgb,var(--ok) 20%,transparent);color:var(--ok)}.oal .mk.no{box-shadow:inset 0 0 0 2px var(--bad);width:18px;height:18px}.oal td.c,.oal th.c{padding-left:4px;padding-right:4px}.oal .est{max-width:130px}.oal .mk.na{color:var(--faint);font-weight:400}.oal tfoot td.c b{font-family:var(--f-mono)}";document.head.append(s)})();
function alcCard(f){
  const ORDS={XIII:1,XIV:2,XV:3},SN={XIII:'mejoramiento',XIV:'conservación periódica',XV:'mejoramiento'};
  const L=[...f.oa_lista].sort((a,b)=>((ORDS[a.sec]||9)-(ORDS[b.sec]||9))||((a.km||0)-(b.km||0)));
  const secs=[...new Set(L.map(t=>t.sec))];
  const c=card(f.nombre,'Obras por km','cabezal de entrada y salida, emboquillado y disipador · ✓ hecho · ○ falta · — no lleva');
  const b=el('div','card-b');const t=el('table','ft cul oal');const th=el('thead');const tr=el('tr');
  [['Km'],['Estructura'],['Entrada','c'],['Salida','c'],['Emboq.','c'],['Disip.','c'],['Estado']].forEach(([h,cc])=>tr.append(el('th',cc||null,h)));th.append(tr);t.append(th);
  const tb=el('tbody');
  const nice=s=>{s=String(s||'').toLowerCase().replace(/\b(tmc|hdpe|pvc)\b/g,x=>x.toUpperCase()).replace(/ø/g,'Ø');return s.charAt(0).toUpperCase()+s.slice(1)};
  const mk=v=>{const td=el('td','c');td.append(el('span','mk '+(v===1?'si':v===0?'no':'na'),v===1?'✓':v===0?'':'—'));return td};
  const EL=['ent','sal','emb','dis'];
  const cnt=R=>{const o={};EL.forEach(k=>{o[k]=[R.filter(x=>x[k]===1).length,R.filter(x=>x[k]===0||x[k]===1).length]});o.term=R.filter(x=>EL.every(k=>x[k]!==0)).length;o.n=R.length;return o};
  const fr=(a)=>a[1]?a[0]+' de '+a[1]:'—';
  secs.forEach(sec=>{
    const R=L.filter(x=>x.sec===sec);const S=cnt(R);
    const pend=EL.reduce((s,k)=>s+S[k][1]-S[k][0],0);
    if(!(('oa'+sec) in CU_OPEN))CU_OPEN['oa'+sec]=pend>0;
    const sr=el('tr','cus');const sd=el('td');sd.colSpan=7;const tg=el('span','tg',CU_OPEN['oa'+sec]?'▾':'▸');
    const cab=[S.ent[0]+S.sal[0],S.ent[1]+S.sal[1]];
    const txt=['  ·  '+S.n+(S.n>1?' obras':' obra'),S.term+(S.term===1?' completa':' completas'),'cabezales '+fr(cab)];
    if(S.emb[1])txt.push('emboquillados '+fr(S.emb));if(S.dis[1])txt.push('disipadores '+fr(S.dis));
    sd.append(tg,el('b',null,'Sector '+sec+(SN[sec]?' · '+SN[sec]:'')),document.createTextNode(txt.join(' · ')));
    sr.append(sd);tb.append(sr);
    const rows=[];let kk=null;
    R.forEach(m=>{
      const est=String(m.estado||'').toUpperCase();
      const falta=EL.filter(k=>m[k]===0);const todo=falta.length===0&&EL.some(k=>m[k]===1);
      const cabOk=m.ent!==0&&m.sal!==0;
      let sm,lab;
      if(todo){sm='ok';lab='Terminado'}
      else if(cabOk&&est.startsWith('TERM')){sm='warn';lab='Falta '+falta.map(k=>({emb:'emboquillado',dis:'disipador'})[k]||k).join(' y ')}
      else if(est.includes('ATRAS')){sm='bad';lab='Atrasado'+(m.atraso?' '+Math.round(m.atraso)+' d':'')}
      else if(est.includes('PROCESO')){sm='warn';lab='En proceso'}
      else{sm='na';lab=est?nice(est):'Pendiente'}
      const fe=todo?(m.fin==='antes'?'antes del control':(m.fin&&/^\d{4}-/.test(m.fin)?fdm(D(m.fin)):'')):(m.proy&&/^\d{4}-/.test(m.proy)?'proy. '+fdm(D(m.proy)):'');
      const kmn=m.km!=null?Math.floor(m.km/1000):null;const nk=kmn!==kk;
      const r=el('tr',(est.includes('PROCESO')?'curun':'')+(nk&&kk!==null?' kmt':'')||null);kk=kmn;
      r.append(el('td','kmc',nk&&kmn!=null?String(kmn):''));
      const c2=el('td');const d2=el('div','two');d2.append(el('b',null,m.cod));const ti=String(m.clase||'').toUpperCase()==='OC'?'Obra complementaria':nice(m.tipo).replace(/^(alcantarilla|pase de agua)\s+/i,'');d2.append(el('small',null,ti+(m.largo?' · '+fmt(m.largo,m.largo%1?2:0)+' m':'')));c2.append(d2);r.append(c2);
      EL.forEach(k=>r.append(mk(m[k])));
      const ce=el('td');const es=el('div','est',lab+(fe?' · '+fe:''));es.style.color=sm==='na'?'var(--muted)':'var(--'+sm+')';ce.append(es);r.append(ce);
      if(m.obs)r.title=m.obs;
      if(!CU_OPEN['oa'+sec])r.style.display='none';rows.push(r);tb.append(r)});
    sr.onclick=()=>{const k='oa'+sec;CU_OPEN[k]=!CU_OPEN[k];tg.textContent=CU_OPEN[k]?'▾':'▸';rows.forEach(r=>r.style.display=CU_OPEN[k]?'':'none')};
  });
  t.append(tb);const T=cnt(L);const tf=el('tfoot');const fr2=el('tr');const f1=el('td');f1.colSpan=2;f1.textContent='Total Tramo VII · '+T.n+' obras';fr2.append(f1);
  EL.forEach(k=>{const td=el('td','c');td.append(el('b',null,fr(T[k])));fr2.append(td)});
  fr2.append(el('td',null,T.term+' de '+T.n+' completas'));tf.append(fr2);t.append(tf);
  const sc=el('div','scroll');sc.append(t);b.append(sc);
  b.append(el('div','pnote','Lista de la hoja PROGRAMA del control de obras de arte. Terminado = tiene todo lo que lleva (cabezales, emboquillado y disipador). Atrasado = según el programa base, con su fecha proyectada. Toca un sector para abrir o cerrar su lista. En ámbar las obras en proceso.'));
  c.append(b);return c;
}
"""

JS_O = "if(f.cu_lista&&f.cu_lista.length)box.append(cunetasCard(f));"
JS_N = "if(f.oa_lista&&f.oa_lista.length)box.append(alcCard(f));" + JS_O

CO_O = "if(!(f.cu_lista&&f.cu_lista.length))if(f.comp&&!(f.muros_lista&&f.muros_lista.length))box.append(compCard(f));"
CO_N = "if(!(f.oa_lista&&f.oa_lista.length))" + CO_O   # alcantarillas: solo la lista


def patch_py(s):
    if 'parche 25/11 alcantarillas lista' in s:
        return s
    assert s.count(PY_A) == 1, 'ancla EST prod'
    return s.replace(PY_A, PY_ADD + PY_A, 1)


def patch_html(h):
    if 'function alcCard' in h and '/*alc-v2*/' not in h:     # versión anterior de la tarjeta: se reemplaza
        i = h.index("(function(){const s=document.createElement('style');s.textContent=\".oal ")
        j = h.index('function alertsCard(){', i)
        h = h[:i] + FN + h[j:]
    if 'function alcCard' not in h:
        assert h.count(JS_O) == 1, 'cunetasCard en renderFrente'
        h = h.replace(JS_O, JS_N, 1)
        assert h.count('function alertsCard(){') == 1
        h = h.replace('function alertsCard(){', FN + 'function alertsCard(){', 1)
    if CO_N not in h:
        assert h.count(CO_O) == 1, 'compCard (cunetas) en renderFrente'
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
