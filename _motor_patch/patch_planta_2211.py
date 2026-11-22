"""Parche 22/11 (j) — Planta de suelos Santa Cruz: los indicadores salen de la gráfica de producción y van en su propia
tarjeta, en dos bloques que se entienden: primero el SALDO EN PLANTA (base preparada, base sin preparar, emulsión,
cemento) y después el ACUMULADO (base ingresada, emulsión ingresada, producido, despachado, dosis)."""

PY_A = "_ALS += [a for a in alc if not re.match(r'(?i)\\s*(suelo-cemento|cantera santa cruz|corte xv)', a)]"
PY_ADD = '''# ---------- planta: primero SALDO EN PLANTA y luego ACUMULADO — parche 22/11 planta kpis
try:
    def _pv(lbl, col):
        ws = WB['pl']['CONTROL']; vc = {'A': 'E', 'I': 'M', 'Q': 'U', 'Y': 'AC'}[col]
        for r in range(8, 30):
            v = ws[f'{col}{r}'].value
            if isinstance(v, str) and v.strip().lower().startswith(lbl.lower()):
                return num(ws[f'{vc}{r}'].value)
        return None
    _fc = WB['pl']['CONTROL']['D8'].value
    _G1 = 'Saldo en planta' + (f' · al {_fc:%d/%m}' if isinstance(_fc, dt.datetime) else '')
    _G2 = 'Acumulado desde el inicio de la planta'
    _old = PROD['planta'].get('kpis', [])
    _cem = next((k for k in _old if k['l'].startswith('Stock de cemento')), None)
    _mz, _bs, _bsd = _pv('Mezcla en acopio', 'Q'), _pv('STOCK EN ACOPIO', 'A'), _pv('Alcanza para', 'A')
    _ec, _eq, _ed = _pv('STOCK CALCULADO', 'I'), _pv('Stock según cuaderno', 'I'), _pv('Alcanza para', 'I')
    _e = _eq if _eq is not None else _ec
    _des = None if (_eq is None or _ec is None) else _eq - _ec
    K = [dict(g=_G1, l='Base emulsión preparada (en acopio)', v=round(_mz or 0), u='m³', s='lista para despachar a campo'),
         dict(g=_G1, l='Material base sin preparar', v=round(_bs or 0), u='m³',
              s='material de San Pedro por mezclar' + (f' · alcanza {_bsd:.1f} días de planta' if _bsd is not None else ''), bad=_bsd is not None and _bsd < 2),
         dict(g=_G1, l='Emulsión en el tanque', v=round(_e) if _e is not None else None, u='gal',
              s='según el cuaderno' + (f' · el cálculo (ingresos − consumo) da {_ec:,.0f} gal: descuadre {_des:+,.0f} gal' if _des is not None and abs(_des) > 500 else '')
                + (f' · alcanza {_ed:.1f} días' if _ed is not None else ''), bad=(_des is not None and abs(_des) > 2000) or (_ed is not None and _ed < 2))]
    if _cem:
        K.append(dict(_cem, g=_G1, l='Cemento', bad=(_cem.get('v') or 0) < CEM_MIN))
    _bi, _vj, _ft, _pa = _pv('Ingresado (acumulado)', 'A'), _pv('Viajes registrados', 'A'), _pv('Falta traer', 'A'), _pv('% abastecido', 'A')
    _ei, _ci, _cf = _pv('Ingresada', 'I'), _pv('Cisternas', 'I'), _pv('Cisternas que faltan', 'I')
    _pr, _pp2, _de = _pv('PRODUCIDO ACUMULADO', 'Q'), _pv('% de la meta', 'Q'), _pv('Despachado a campo', 'Q')
    _da, _do, _dg = _pv('Emulsión acumulada', 'Y'), _pv('Dosis objetivo', 'Y'), _pv('Emulsión de más', 'Y')
    K += [dict(g=_G2, l='Material base ingresado', v=round(_bi or 0), u='m³',
               s=f'{_vj or 0:,.0f} viajes + saldo inicial' + (f' · {_pa:.0%} de la meta · faltan {_ft:,.0f} m³' if _pa is not None and _ft is not None else '')),
          dict(g=_G2, l='Emulsión ingresada', v=round(_ei or 0), u='gal',
               s=f'{_ci or 0:.0f} cisternas + saldo inicial' + (f' · faltan {_cf:.0f} cisternas para el Sector XV' if _cf is not None else '')),
          dict(g=_G2, l='Base emulsión producida', v=round(_pr or 0), u='m³',
               s=f"{_pp2:.0%} de {PL_AC['meta_mezcla']:,.0f} m³ del Sector XV" if _pp2 is not None and PL_AC.get('meta_mezcla') else ''),
          dict(g=_G2, l='Despachado a campo', v=round(_de or 0), u='m³',
               s=f'producido {_pr or 0:,.0f} = despachado {_de or 0:,.0f} + en acopio {_mz or 0:,.0f} m³')]
    if _da is not None and _do:
        K.append(dict(g=_G2, l='Dosis de emulsión (promedio)', v=round(_da, 1), dec=1, u='gal/m³',
                      s=f'objetivo {_do:.1f} gal/m³ ({_da / _do - 1:+.0%})' + (f' · van {abs(_dg):,.0f} gal de menos' if _dg is not None and _dg < 0 else ''), bad=_da < 0.9 * _do))
    PROD['planta']['kpis'] = K
except Exception as e:
    print('planta kpis', e)
'''

FN = r"""(function(){const s=document.createElement('style');s.textContent=".pkg{font-size:12px;font-weight:700;letter-spacing:.06em;text-transform:uppercase;color:var(--ink);margin:2px 0 10px;padding-left:9px;border-left:3px solid var(--navy)}.pkg~.pkg{margin-top:8px}.pkpi .bad{box-shadow:inset 3px 0 0 var(--bad)}";document.head.append(s)})();
function saldoCard(f){
  const P=f.prod;const c=card(f.nombre,'Saldo en planta y acumulado');const b=el('div','card-b');
  const gs=[];P.kpis.forEach(o=>{let g=gs.find(x=>x.g===o.g);if(!g){g={g:o.g,l:[]};gs.push(g)}g.l.push(o)});
  gs.forEach(g=>{b.append(el('div','pkg',g.g||''));const k=el('div','pkpi');
    g.l.forEach(o=>{const d=el('div',o.bad?'bad':null);d.append(el('div','eyebrow',o.l));const v=el('div','pv',o.v==null?'—':fmt(o.v,o.dec||0));v.append(el('small',null,o.u));d.append(v);if(o.s)d.append(el('div','s',o.s));k.append(d)});b.append(k)});
  c.append(b);return c;
}
"""

JS = [("if(P.kpis){const k=el('div','pkpi');", "if(P.kpis&&!P.kpis.some(o=>o.g)){const k=el('div','pkpi');"),
      ("if(f.prod){box.append(prodCard(f));", "if(f.prod){if((f.prod.kpis||[]).some(o=>o.g))box.append(saldoCard(f));box.append(prodCard(f));")]


def patch_py(s):
    if 'parche 22/11 planta kpis' in s:
        return s
    assert s.count(PY_A) == 1, 'ancla _ALS'
    return s.replace(PY_A, PY_ADD + PY_A, 1)


def patch_html(h):
    if 'function saldoCard' in h:
        return h
    for o, n in JS:
        assert h.count(o) == 1, ('planta', o[:40])
        h = h.replace(o, n, 1)
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
