"""Parche 23/11 (b) — Micropavimento, mapa de la semana: siempre los dos lados (1ra capa LD y LI) y el rango es el
tramo que falta cerrar en el suelo-cemento XIV (el bloque más grande de lo pendiente, lo que dejó la semana anterior),
con lo hecho antes, lo de esta semana y la cota de cada hueco."""

PY_A = "EST['prod'] = dict(semana=f\"S-{LUN.isocalendar()[1]}\""
PY_ADD = '''# ---------- micro: mapa de la semana con los 2 lados y todo lo que falta para cerrar el tramo — parche 23/11 micro cierre
try:
    _fm = next(f for f in FR if f['id'] == 'micro')
    _pz = []
    for _l in ('IZQUIERDO', 'DERECHO'):
        _pz += [list(t) for t in _faltan('1ra capa', _l, 251820, 276810)]
    _bl = []
    for _a, _b in sorted(_pz):
        if _bl and _a <= _bl[-1][1] + 300:
            _bl[-1][1] = max(_bl[-1][1], _b)
        else:
            _bl.append([_a, _b])
    if _bl:
        _A, _B = max(_bl, key=lambda x: x[1] - x[0])
        _fil = {'1ra capa · LD': list(MP_SEM.get('1ra capa · LD', [])), '1ra capa · LI': list(MP_SEM.get('1ra capa · LI', []))}
        _wk = [t for v in _fil.values() for t in v if t[1] > _A - 1500 and t[0] < _B + 1500]
        _a0 = min([_A] + [t[0] for t in _wk]) - 400
        _b0 = max([_B] + [t[1] for t in _wk]) + 400
        _out = []
        for _k in ('1ra capa · LD', '1ra capa · LI'):
            _v = [t for t in _fil[_k] if t[1] > _a0 and t[0] < _b0]
            _prev = []
            for _x, _y in _mp_hecho(_k, int(_a0), int(_b0)):
                _x, _y = max(_x, _a0), min(_y, _b0)
                if _y > _x:
                    for _u, _w in _resta_sem(_x, _y, [[t[0], t[1]] for t in _v]):
                        _prev.append([_u, _w, 'antes'])
            _out.append(dict(capa=_k, tramos=_prev + _v))
        _m = dict(_fm.get('mapa_sem') or {})
        for _q in ('meta', 'meta_lbl'):
            _m.pop(_q, None)
        _m.update(desde=_a0, hasta=_b0, filas=_out, huecos=True, cierre=[_A, _B])
        _fm['mapa_sem'] = _m
except Exception as e:
    print('micro cierre', e)
'''


def patch_py(s):
    if 'parche 23/11 micro cierre' in s:
        return s
    assert s.count(PY_A) == 1, 'ancla EST prod'
    return s.replace(PY_A, PY_ADD + PY_A, 1)


def aplicar(motor):
    from pathlib import Path
    f = Path(motor) / 'dash_data.py'
    a = f.read_text(encoding='utf8')
    b = patch_py(a)
    if b != a:
        f.write_text(b, encoding='utf8')
        return ['dash_data.py']
    return []
