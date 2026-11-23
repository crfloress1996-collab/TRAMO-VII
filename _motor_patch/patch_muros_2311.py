"""Parche 23/11 — Muros bolsacreto: lista de los 16 muros (como las zonas del corte) con progresiva, lado,
longitud, alto, bolsas del muro, hechas, faltan, avance y estado. Sale de la hoja PROGRAMA del CF de muros
(y de METRADOS PGV para las progresivas de inicio y fin)."""

PY_A = "EST['prod'] = dict(semana=f\"S-{LUN.isocalendar()[1]}\""
PY_ADD = '''# ---------- muros: lista por muro (hojas PROGRAMA y METRADOS PGV del CF de muros) — parche 23/11 muros lista
try:
    _pg = {}
    for r in WB['mb']['METRADOS PGV'].iter_rows(min_row=8, max_row=60, values_only=True):
        if r[1] and isinstance(r[7], (int, float)):
            _pg[str(r[1]).strip()] = (r[7], r[9] if isinstance(r[9], (int, float)) else None)
    MB_LISTA = []
    for r in WB['mb']['PROGRAMA'].iter_rows(min_row=7, max_row=60, values_only=True):
        if not r[1] or not isinstance(r[7], (int, float)):
            continue
        _cod = str(r[1]).strip()
        _a, _b = _pg.get(_cod, (None, None))
        _real = r[20] if len(r) > 20 else None
        MB_LISTA.append(dict(cod=_cod, comp=r[3], sector=r[4], prog=r[5], desde=_a, hasta=_b, lado=r[6], largo=num(r[7]), alto=num(r[8]),
                             meta=num(r[9]), hecho_m=num(r[12]), hechas=num(r[13]), faltan=num(r[14]), pct=num(r[15]), estado=r[16],
                             real=iso(_real) if isinstance(_real, dt.datetime) else (str(_real) if _real else None),
                             fin=iso(r[22]) if len(r) > 22 and isinstance(r[22], dt.datetime) else None,
                             obs=(str(r[44]) if len(r) > 44 and r[44] else None)))
    for _f in FR:
        if _f['id'] == 'muros':
            _f['muros_lista'] = MB_LISTA
except Exception as e:
    print('muros lista', e)
'''

FN = r"""(function(){const s=document.createElement('style');s.textContent=".mbl tr.mbs td{background:var(--band);font-size:12px;color:var(--muted);padding:7px 10px}.mbl tr.mbs td b{color:var(--ink);font-weight:700}.mbl tr.mbrun td{background:color-mix(in srgb,var(--amber) 9%,transparent)}.mbl td{white-space:nowrap}.mbl .ab{min-width:96px}.mbl td .two small{white-space:nowrap}.mbl tfoot td{font-weight:700;border-top:2px solid var(--line)}";document.head.append(s)})();
function murosCard(f){
  const L=[...f.muros_lista].sort((a,b)=>(a.desde||0)-(b.desde||0));
  const c=card('Muros bolsacreto · '+L.length+' muros','Lista de muros por progresiva');
  const b=el('div','card-b');const t=el('table','ft mbl');const th=el('thead');const tr=el('tr');
  [['Muro · progresiva'],['Lado'],['Long. (m)','r'],['Alto (m)','r'],['Bolsas','r'],['Hechas','r'],['Faltan','r'],['Avance'],['Estado']].forEach(([h,cc])=>tr.append(el('th',cc||null,h)));th.append(tr);t.append(th);
  const tb=el('tbody');let sec=null;const T={largo:0,meta:0,hechas:0,faltan:0};
  L.forEach(m=>{
    if(m.sector!==sec){sec=m.sector;const n=L.filter(x=>x.sector===sec);const sr=el('tr','mbs');const sd=el('td');sd.colSpan=9;
      sd.append(el('b',null,'Sector '+sec+(m.comp?' · '+String(m.comp).toLowerCase():'')),document.createTextNode('  ·  '+n.length+(n.length>1?' muros':' muro')+' · faltan '+fmt(n.reduce((q,x)=>q+(x.faltan||0),0))+' bolsas'));sr.append(sd);tb.append(sr)}
    const est=String(m.estado||'PENDIENTE').toUpperCase(),sm=est.startsWith('TERM')?'ok':est.includes('PROCESO')?'warn':'na';
    const r=el('tr',sm==='warn'?'mbrun':null);
    const c1=el('td');
    const lado=String(m.lado||'').toUpperCase().startsWith('IZQ')?'Izq.':String(m.lado||'').toUpperCase().startsWith('DER')?'Der.':(m.lado||'—');
    const pr=m.desde?km(m.desde)+(m.hasta?' – '+km(m.hasta):''):(m.prog||'—');
    {const s1=el('div','two');s1.append(el('b',null,m.cod),el('small',null,pr));c1.append(s1)}
    const p=m.pct!=null?m.pct:(m.meta?(m.hechas||0)/m.meta:0);
    const ab=el('div','ab');const t2=el('div','tr');const ii=el('i');ii.style.width=Math.min(100,p*100)+'%';ii.style.background='var(--'+(sm==='na'?'faint':sm)+')';t2.append(ii);ab.append(t2,el('b',null,Math.round(p*100)+' %'));
    const ce=el('td');const s2=el('div','two');s2.append(semPill(sm,sm==='ok'?'Terminado':sm==='warn'?'En proceso':'Pendiente'));
    const fr=m.real&&/^\d{4}-/.test(m.real)?'terminó el '+fd(m.real):(sm!=='ok'&&m.fin?'fin proyectado '+fd(m.fin):'');if(fr)s2.append(el('small',null,fr));ce.append(s2);
    const td=(v,cls)=>el('td',cls||null,v);
    r.append(c1,td(lado),td(fmt(m.largo||0,(m.largo||0)%1?1:0),'r mono'),td(fmt(m.alto||0),'r mono'),td(fmt(m.meta||0),'r mono'),td(fmt(m.hechas||0),'r mono'),td(fmt(m.faltan||0),'r mono'+((m.faltan||0)>0?' late':'')));
    const ca=el('td');ca.append(ab);r.append(ca,ce);if(m.obs)r.title=m.obs;tb.append(r);
    T.largo+=m.largo||0;T.meta+=m.meta||0;T.hechas+=m.hechas||0;T.faltan+=m.faltan||0});
  t.append(tb);const tf=el('tfoot');const fr2=el('tr');const f1=el('td');f1.colSpan=2;f1.textContent='Total Tramo VII · '+L.length+' muros';
  const pt=T.meta?T.hechas/T.meta:0;const fa=el('td');const ab2=el('div','ab');const t3=el('div','tr');const i3=el('i');i3.style.width=Math.min(100,pt*100)+'%';i3.style.background='var(--navy)';t3.append(i3);ab2.append(t3,el('b',null,Math.round(pt*100)+' %'));fa.append(ab2);
  fr2.append(f1,el('td','r mono',fmt(T.largo)),el('td'),el('td','r mono',fmt(T.meta)),el('td','r mono',fmt(T.hechas)),el('td','r mono late',fmt(T.faltan)),fa,el('td'));tf.append(fr2);t.append(tf);
  const sc=el('div','scroll');sc.append(t);b.append(sc);
  b.append(el('div','pnote','Bolsas del muro = metrado del PGV. Hechas y estado salen de la hoja PROGRAMA del control de muros (lo reportado en el REGISTRO DIARIO). En ámbar los muros en proceso.'));
  c.append(b);return c;
}
"""

JS_O = "if(f.zonas)box.append(corteCard(f));"
JS_N = "if(f.zonas)box.append(corteCard(f));if(f.muros_lista&&f.muros_lista.length)box.append(murosCard(f));"


def patch_py(s):
    if 'parche 23/11 muros lista' in s:
        return s
    assert s.count(PY_A) == 1, 'ancla EST prod'
    return s.replace(PY_A, PY_ADD + PY_A, 1)


def patch_html(h):
    if 'function murosCard' in h:
        return h
    assert h.count(JS_O) == 1, 'corteCard en renderFrente'
    h = h.replace(JS_O, JS_N, 1)
    assert h.count('function alertsCard(){') == 1
    return h.replace('function alertsCard(){', FN + 'function alertsCard(){', 1)


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
