"""Parche 18/11 — Planta de suelos en el tablero:
 1) gráfico diario: colores distintos para ingreso de base / producción / despacho, y acumulado de la semana en la leyenda;
 2) barras horizontales: fila 'Base emulsión despachada a campo';
 3) indicadores arriba: stock de base preparada (mezcla en acopio) y base sin preparar (material base en acopio).
Uso: patch_planta_1811.py <tablero.html o index.html> [dash_data.py]"""
import sys, re

JS = [
 # color propio por serie (x.color) en el gráfico
 ("const NEU=['var(--navy-s)','var(--line)'];let ni=0;const col=ss.map(x=>x.meta?null:NEU[(ni++)%2]);",
  "const NEU=['var(--navy-s)','var(--line)'];let ni=0;const col=ss.map(x=>x.meta?null:(x.color||NEU[(ni++)%2]));"),
 ("const r=sv('rect',{x:bx,y:y(v),width:gw,height:Math.max(0,H-B-y(v)),fill,rx:2});if(!x.meta)r.setAttribute('stroke','var(--navy)');",
  "const r=sv('rect',{x:bx,y:y(v),width:gw,height:Math.max(0,H-B-y(v)),fill,rx:2});if(!x.meta&&!x.color)r.setAttribute('stroke','var(--navy)');"),
 # leyenda con color propio y acumulado de la semana
 ("if(ss.length>1){const l2=el('div','legend');ss.forEach((x,j)=>{const s2=el('span');const i=el('i');i.style.background=x.meta?'var(--ok)':['var(--navy-s)','var(--line)'][ss.filter(z=>!z.meta).indexOf(x)%2];if(!x.meta)i.style.outline='1px solid var(--navy)';s2.append(i,document.createTextNode(x.nombre));l2.append(s2)});hh.append(l2)}",
  "if(ss.length>1){const l2=el('div','legend');ss.forEach((x,j)=>{const s2=el('span');const i=el('i');i.style.background=x.meta?'var(--ok)':(x.color||['var(--navy-s)','var(--line)'][ss.filter(z=>!z.meta).indexOf(x)%2]);if(!x.meta&&!x.color)i.style.outline='1px solid var(--navy)';const tw=x.dias.reduce((q,d)=>q+(d.futuro?0:(d.v||0)),0);s2.append(i,document.createTextNode(x.nombre+' · semana '),el('b',null,fmt(tw)+' '+x.und));l2.append(s2)});hh.append(l2)}"),
]
PY_OLD = "PROD['planta']['kpis'] = [dict(l='Stock de emulsión en planta'"


def patch_html(h):
    for o, n in JS:
        if n in h:
            continue
        assert h.count(o) == 1, ('no encontrado', o[:70])
        h = h.replace(o, n)
    return h


PY_ADD = '''
# ---------- planta: stocks de base (preparada / sin preparar), despacho acumulado y colores del gráfico (parche 18/11)
def _plv2(lbl, col):
    try:
        return plv(lbl, col)
    except Exception:
        return None
try:
    _pp = PROD['planta']
    _desp = _plv2('Despachado a campo', 'Q')
    _mez = _plv2('Mezcla en acopio', 'Q')
    _bsp = _plv2('STOCK EN ACOPIO', 'A')
    _k = _pp.setdefault('kpis', [])
    _k[0:0] = [dict(l='Stock de base preparada (mezcla en acopio)', v=round(_mez) if _mez is not None else None, u='m³', s='base emulsión lista para despachar a campo'),
               dict(l='Base sin preparar en acopio', v=round(_bsp) if _bsp is not None else None, u='m³', s='material base de San Pedro que falta mezclar')]
    for _s in _pp['series']:
        if _s['nombre'].startswith('Ingreso'):
            _s['color'] = '#5B8BD6'
        elif _s['nombre'].startswith('Despacho'):
            _s['color'] = '#8E6BB8'
    _fpl = next(f for f in FR if f['id'] == 'planta')
    _mt = _fpl.get('materiales') or []
    if _mt and _desp is not None:
        _mt[0]['nota'] = re.sub(r'despachado a campo [\\d,\\.]+', f'despachado a campo {_desp:,.0f} m³', _mt[0].get('nota') or '')
        if not any(m['nombre'].startswith('Base emulsión despachada') for m in _mt):
            _mt.insert(1, dict(nombre='Base emulsión despachada a campo', meta=_mt[0]['meta'], hecho=_desp, und='m³ suelto',
                               nota=f'en acopio {(_mez or 0):,.0f} m³ listos para despachar'))
except Exception as e:
    print('planta parche', e)
'''


def patch_py(s):
    if 'parche 18/11' in s:
        return s
    anchor = "EST['dia_obs'] = DIA_OBS\n"
    assert s.count(anchor) == 1
    return s.replace(anchor, anchor + PY_ADD, 1)


if __name__ == '__main__':
    p = sys.argv[1]
    h = patch_html(open(p, encoding='utf8').read())
    open(p, 'w', encoding='utf8').write(h)
    if len(sys.argv) > 2:
        q = sys.argv[2]
        t = patch_py(open(q, encoding='utf8').read())
        open(q, 'w', encoding='utf8').write(t)
    print('ok')
