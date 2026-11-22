"""Parche 22/11 (f) — Mapa de la semana de base: línea de inicio 283+700, 'Fin suelo-cemento' 276+810, cota general
283+700 → 276+810 (como en planos) y, en cada actividad (refine, batido, aporte, escarificado), la cota de lo que falta
desde su frente hasta el fin del suelo-cemento. En imprimación y micro la línea queda como 'Fin suelo-cemento'."""

PY_A = "EST['prod'] = dict(semana=f\"S-{LUN.isocalendar()[1]}\""
PY_ADD = '''for _f in FR:   # inicio y cotas de la base emulsión XV — parche 22/11 cotas
    _m = _f.get('mapa_sem')
    if _m and _f['id'] in ('base', 'imprimacion', 'micro'):
        _m['meta'] = 276810
        _m['meta_lbl'] = 'Fin suelo-cemento'
        if _f['id'] == 'base':
            _m['inicio'] = 283700          # la base emulsión XV empezó en el 283+700 (Crhistian, 22/11)
            _m['inicio_lbl'] = 'Inicio base emulsión'
            _m['cota'] = [276810, 283700]
            _m['hasta'] = max(_m['hasta'], 283700 + 300)
'''

CSS_FN = r"""(function(){const s=document.createElement('style');s.textContent=".lin .cotl{font-size:12px;font-weight:700;fill:var(--ink)}.lin .cotf{font-size:11.5px;font-weight:700;fill:var(--ink);paint-order:stroke;stroke:var(--track);stroke-width:5px;stroke-linejoin:round}";document.head.append(s)})();
function mHitos(m){const h=[];if(m.meta)h.push({km:m.meta,t:m.meta_lbl||'Meta'});if(m.inicio)h.push({km:m.inicio,t:m.inicio_lbl||'Inicio'});return h}
"""

COTA = r"""  if(o.cota){const [ca,cb]=o.cota,y0=top+n*rh+50,xa=x(Math.max(ca,o.A)),xb=x(Math.min(cb,o.B));
    [xa,xb].forEach(X=>{s.append(sv('line',{x1:X,x2:X,y1:top+n*rh+2,y2:y0+7,stroke:'var(--muted)','stroke-width':1}));s.append(sv('line',{x1:X-5,x2:X+5,y1:y0+5,y2:y0-5,stroke:'var(--ink)','stroke-width':1.6}))});
    s.append(sv('line',{x1:xa,x2:xb,y1:y0,y2:y0,stroke:'var(--ink)','stroke-width':1.2}));
    s.append(sv('text',{x:(xa+xb)/2,y:y0-6,'text-anchor':'middle',class:'cotl'},fmt(Math.abs(cb-ca))+' m  ·  '+km(cb)+' → '+km(ca)));
    o.rows.forEach((r,i)=>{if(!r.tramos.length)return;const fr=Math.min(...r.tramos.map(t=>Math.min(t[0],t[1])));if(!(fr>ca))return;
      const y=top+i*rh+rh/2,X1=x(Math.max(ca,o.A))+2,X2=x(Math.min(fr,o.B))-2;if(X2-X1<50)return;
      s.append(sv('line',{x1:X1,x2:X2,y1:y,y2:y,stroke:'var(--ink)','stroke-width':1,opacity:.8}));
      [X1,X2].forEach(X=>s.append(sv('line',{x1:X,x2:X,y1:y-6,y2:y+6,stroke:'var(--ink)','stroke-width':1.3,opacity:.8})));
      s.append(sv('text',{x:(X1+X2)/2,y:y+1,'text-anchor':'middle','dominant-baseline':'middle',class:'cotf'},'falta '+fmt(fr-ca)+' m'))})}
"""

JS = [
    ("rh=o.day?40:38,n=o.rows.length,H=top+n*rh+34;", "rh=o.day?40:38,n=o.rows.length,H=top+n*rh+34+(o.cota?40:0);"),
    ("const top=m.meta?52:26,rh=40,H=top+m.filas.length*rh+34;", "const top=m.meta?52:26,rh=40,H=top+m.filas.length*rh+34+(m.cota?40:0);"),
]
HIT_O = "hitos:m.meta?[{km:m.meta,t:m.meta_lbl||'Meta'}]:[]"
HIT_N = "hitos:mHitos(m),cota:m.cota"
RET = "  return {svg:s,days};\n}"


def patch_py(s):
    if 'parche 22/11 cotas' in s:
        return s
    assert s.count(PY_A) == 1, 'ancla EST prod'
    return s.replace(PY_A, PY_ADD + PY_A, 1)


def patch_html(h):
    if 'function mHitos' in h:
        return h
    for o, n in JS:
        assert h.count(o) == 1, ('cotas', o[:40])
        h = h.replace(o, n, 1)
    assert h.count(HIT_O) == 2, 'hitos del mapa'
    h = h.replace(HIT_O, HIT_N)
    assert h.count(RET) == 1, 'return linearSvg'
    h = h.replace(RET, COTA + RET, 1)
    assert h.count('function alertsCard(){') == 1
    return h.replace('function alertsCard(){', CSS_FN + 'function alertsCard(){', 1)


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
