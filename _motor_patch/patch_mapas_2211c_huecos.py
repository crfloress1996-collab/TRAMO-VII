"""Parche 22/11 (h) — Mapas de la semana de micro e imprimación: cota de cada hueco entre lo hecho
('falta X m') en el lado izquierdo y en el derecho, y debajo el total que falta para cerrar cada lado."""

PY_A = "EST['prod'] = dict(semana=f\"S-{LUN.isocalendar()[1]}\""
PY_ADD = '''for _f in FR:   # huecos a cerrar en micro e imprimación — parche 22/11 huecos
    if _f.get('mapa_sem') and _f['id'] in ('imprimacion', 'micro'):
        _f['mapa_sem']['huecos'] = True
'''

FN = r"""function mGaps(tr,min){const u=[];tr.map(t=>[Math.min(t[0],t[1]),Math.max(t[0],t[1])]).sort((p,q)=>p[0]-q[0]).forEach(([a,b])=>{if(u.length&&a<=u[u.length-1][1]+20)u[u.length-1][1]=Math.max(u[u.length-1][1],b);else u.push([a,b])});
  const g=[];for(let j=1;j<u.length;j++){const a=u[j-1][1],b=u[j][0];if(b-a>=(min||50))g.push([a,b])}return g}
"""

GAPS = r"""  if(o.gaps)o.rows.forEach((r,i)=>{const y=top+i*rh+rh/2;
    mGaps(r.tramos).forEach(([ga,gb])=>{const X1=x(Math.max(ga,o.A))+2,X2=x(Math.min(gb,o.B))-2;if(X2-X1<10)return;
      s.append(sv('line',{x1:X1,x2:X2,y1:y,y2:y,stroke:'var(--ink)','stroke-width':1,opacity:.8}));
      [X1,X2].forEach(X=>s.append(sv('line',{x1:X,x2:X,y1:y-6,y2:y+6,stroke:'var(--ink)','stroke-width':1.3,opacity:.8})));
      if(X2-X1>78)s.append(sv('text',{x:(X1+X2)/2,y:y+1,'text-anchor':'middle','dominant-baseline':'middle',class:'cotf'},'falta '+fmt(gb-ga)+' m'));
      else s.append(sv('text',{x:(X1+X2)/2,y:y-10,'text-anchor':'middle',class:'cotf'},fmt(gb-ga)+' m'))})});
"""
RET = "  return {svg:s,days};\n}"
HIT_O = "hitos:mHitos(m),cota:m.cota"
HIT_N = "hitos:mHitos(m),cota:m.cota,gaps:m.huecos"
# resumen debajo del mapa de la semana: total que falta para cerrar cada lado
LEG_O = "  const zb=el('button','zbtn','⤢ Vista panorámica');zb.title='Ver el mapa en pantalla completa, más de cerca';zb.onclick=()=>zoomWeekMap(f);"
LEG_N = ("  if(m.huecos){const t=m.filas.map(r=>{const g=mGaps(r.tramos);return r.capa+': '+(g.length?fmt(g.reduce((q,[a,b])=>q+b-a,0))+' m en '+g.length+(g.length>1?' huecos':' hueco'):'cerrado')});"
         "const pn=el('div','pnote');pn.append(el('b',null,'Para cerrar lo que está entre lo hecho · '),document.createTextNode(t.join('  ·  ')));c._pn=pn}\n" + LEG_O)
SC_O = "  const sc=el('div','scroll');sc.append(svg);const b=el('div','card-b');b.append(sc,lg);c.append(b);return c;\n}"
SC_N = "  const sc=el('div','scroll');sc.append(svg);const b=el('div','card-b');b.append(sc,lg);if(c._pn)b.append(c._pn);c.append(b);return c;\n}"


def patch_py(s):
    if 'parche 22/11 huecos' in s:
        return s
    assert s.count(PY_A) == 1, 'ancla EST prod'
    return s.replace(PY_A, PY_ADD + PY_A, 1)


def patch_html(h):
    if 'function mGaps' in h:
        return h
    assert h.count(HIT_O) == 2, 'hitos con cota'
    h = h.replace(HIT_O, HIT_N)
    assert h.count(RET) == 1
    h = h.replace(RET, GAPS + RET, 1)
    assert h.count(LEG_O) == 1, 'botón panorámica del mapa'
    h = h.replace(LEG_O, LEG_N, 1)
    i = h.index('function weekMapCard(f){')
    j = h.index(SC_O, i)
    h = h[:j] + SC_N + h[j + len(SC_O):]
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
