"""Parche 22/11 (d) — Cajas de mejoramiento de subrasante (MSR): el avance sale de los 4 pasos de la hoja
MEJORAMIENTO SUBRASANTE (① corte pav., ② excavación, ③ relleno, ④ reposición). Una caja solo queda 'terminada'
cuando se repone el pavimento; mientras tanto se muestra el paso que falta."""

PY_ANCHOR = "# ---------- imprimación: hoja TRAMOS del CF_F-04"
PY_ADD = '''# ---------- cajas MSR: avance por los 4 pasos (hoja MEJORAMIENTO SUBRASANTE, sección 5) — parche 22/11 MSR
try:
    _mw = WB['co']['MEJORAMIENTO SUBRASANTE']
    for _r in range(49, 52):
        _z = next((z for z in CO_ZONAS if z['zona'] == _mw.cell(_r, 1).value), None)
        if not _z:
            continue
        _p = [float(_mw.cell(_r, c).value or 0) for c in (4, 6, 8, 10)]
        _z['pasos'] = _p
        _z['paso'] = _mw.cell(_r, 11).value
        _z['pct'] = sum(_p) / 4
        if _p[3] < 0.999:
            _z['estado'] = 'En proceso' if any(_p) else 'Pendiente'
except Exception as e:
    print('pasos MSR', e)
'''

JS_O = "st==='run'?(Math.round(z.pct*100)+' %'+(key==='T'&&w>90?' · falta '+fmt(z.falta)+' m³':''))"
JS_N = "st==='run'?(z.paso&&key==='MSR'?z.paso:Math.round(z.pct*100)+' %'+(key==='T'&&w>90?' · falta '+fmt(z.falta)+' m³':''))"


def patch_py(s):
    if 'parche 22/11 MSR' in s:
        return s
    assert s.count(PY_ANCHOR) == 1, 'ancla imprimación'
    return s.replace(PY_ANCHOR, PY_ADD + PY_ANCHOR, 1)


def patch_html(h):
    if JS_N in h or JS_O not in h:
        return h
    return h.replace(JS_O, JS_N, 1)


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
