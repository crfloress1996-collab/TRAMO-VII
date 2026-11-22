"""Parche 22/11 (g) — Micropavimento: se quita 'Cierre de brecha' y va 'Ventaja de la base sobre el micro':
cuánto falta al micro para alcanzar a la base, solo con carpeta completa (1ra capa en los dos lados):
suelo-cemento XIV sin micro + base emulsión XV ya terminada = ventaja de la base (y en días al ritmo del micro)."""

PY_A = "EST['prod'] = dict(semana=f\"S-{LUN.isocalendar()[1]}\""
PY_ADD = '''# ---------- ventaja de la base sobre el micro (carpeta completa) — parche 22/11 ventaja
try:
    def _sin_carpeta(a0, b0):
        n = 0
        for x in range(int(a0), int(b0), _paso):
            if not (_tiene('1ra capa', 'IZQUIERDO', x) and _tiene('1ra capa', 'DERECHO', x)):
                n += _paso
        return n
    _be_seg = _union([(min(r[4], r[5]), max(r[4], r[5])) for r in WB['base']['REGISTRO DIARIO'].iter_rows(min_row=10, values_only=True)
                      if isinstance(r[0], dt.datetime) and str(r[2]).startswith('Base emulsión XV') and str(r[3]).startswith('Terminado')
                      and isinstance(r[4], (int, float)) and isinstance(r[5], (int, float))])
    _v13 = _sin_carpeta(_A, 251820)
    _v14 = _sin_carpeta(251820, 276810)
    _v15 = sum(_sin_carpeta(a, b) for a, b in _be_seg)
    _rm = (PROD.get('micro') or {}).get('series') or []
    _rm = next((s.get('ratio') for s in _rm if s.get('principal')), None) or MP_RITMO
    _rb = next((s.get('ratio') for s in ((PROD.get('base') or {}).get('series') or []) if s.get('principal')), None)
    _rl = (_rm or 0) / 2
    _tot = _v13 + _v14 + _v15
    VENTAJA = dict(xiii=_v13, xiv=_v14, xv=_v15, xv_desde=min((a for a, b in _be_seg), default=None), xv_hasta=max((b for a, b in _be_seg), default=None),
                   total=_tot, ritmo_micro=round(_rl), ritmo_base=round(_rb) if _rb else None, dias=round(_tot / _rl, 1) if _rl else None)
    for _f in FR:
        if _f['id'] == 'micro':
            _f['ventaja'] = VENTAJA
except Exception as e:
    print('ventaja', e)
'''

FN_V1 = r"""function ventajaCard(f){
  const v=f.ventaja;const c=card('Ventaja de la base sobre el micro','Cuánto nos falta para alcanzar a la base · solo carpeta completa');
  const ks=el('div','kstrip');
  const k=(lab,val,unit,sub,cls)=>{const d=el('div','k '+(cls||''));d.append(el('div','eyebrow',lab));const vv=el('div','v',val);if(unit)vv.append(el('small',null,unit));d.append(vv,el('div','s',sub||''));ks.append(d)};
  if(v.xiii>0)k('Sector XIII sin micro',fmt(v.xiii),'m','base terminada · 217+340 – 251+820');
  k('Suelo-cemento XIV sin micro',fmt(v.xiv),'m','251+820 – 276+810 · ahí estamos con el micro');
  k('Base emulsión XV ya terminada',fmt(v.xv),'m',v.xv_desde?('de '+km(v.xv_hasta)+' a '+km(v.xv_desde)+' · todavía sin micro'):'todavía sin micro');
  k('Ventaja de la base',fmt(v.total),'m',v.dias!=null?('≈ '+fmt(v.dias,1)+' días de micro a '+fmt(v.ritmo_micro)+' m/día de carpeta completa'):'','bad');
  c.append(ks);
  const b=el('div','card-b');const gana=v.ritmo_base&&v.ritmo_micro?v.ritmo_base-v.ritmo_micro:null;
  b.append(el('div','pnote','Carpeta completa = micro 1ra capa en los dos lados (lo que falta en un solo lado cuenta como pendiente). '+(gana!=null?('Esta semana la base avanza '+fmt(v.ritmo_base)+' m/día y el micro '+fmt(v.ritmo_micro)+' m/día de carpeta completa: '+(gana>0?'la ventaja de la base crece unos '+fmt(gana)+' m por día.':gana<0?'el micro le descuenta unos '+fmt(-gana)+' m por día.':'la ventaja se mantiene.')):'')));
  c.append(b);return c;
}
"""
FN = r"""function ventajaCard(f){
  const v=f.ventaja;const c=card('Ventaja de la base sobre el micro','Cuánto nos falta para alcanzar a la base · solo carpeta completa');
  const xm=prodMain(f),fb=(EST.frentes||[]).find(z=>z.id==='base'),xb=fb?prodMain(fb):null;
  const rm=xm&&xm.ratio?xm.ratio/2:v.ritmo_micro,rb=xb&&xb.ratio?xb.ratio:v.ritmo_base,dias=rm?v.total/rm:null;
  const ks=el('div','kstrip');
  const k=(lab,val,unit,sub,cls)=>{const d=el('div','k '+(cls||''));d.append(el('div','eyebrow',lab));const vv=el('div','v',val);if(unit)vv.append(el('small',null,unit));d.append(vv,el('div','s',sub||''));ks.append(d)};
  if(v.xiii>0)k('Sector XIII sin micro',fmt(v.xiii),'m','base terminada · 217+340 – 251+820');
  k('Suelo-cemento XIV sin micro',fmt(v.xiv),'m','251+820 – 276+810 · ahí estamos con el micro');
  k('Base emulsión XV ya terminada',fmt(v.xv),'m',v.xv_desde?('de '+km(v.xv_hasta)+' a '+km(v.xv_desde)+' · todavía sin micro'):'todavía sin micro');
  k('Ventaja de la base',fmt(v.total),'m',dias!=null?('≈ '+fmt(dias,1)+' días de micro a '+fmt(rm)+' m/día de carpeta completa'):'','bad');
  c.append(ks);
  const b=el('div','card-b');const gana=rb&&rm?Math.round(rb-rm):null;
  b.append(el('div','pnote','Carpeta completa = micro 1ra capa en los dos lados (lo que falta en un solo lado cuenta como pendiente). Ritmos de la semana: micro = la mitad de lo colocado por día (suma de lados). '+(gana!=null?('La base avanza '+fmt(rb)+' m/día y el micro '+fmt(rm)+' m/día de carpeta completa: '+(gana>0?'la ventaja de la base crece unos '+fmt(gana)+' m por día.':gana<0?'el micro le descuenta unos '+fmt(-gana)+' m por día.':'la ventaja se mantiene.')):'')));
  c.append(b);return c;
}
"""


JS_O = "if(f.brecha)box.append(brechaCard(f));"
JS_N = "if(f.ventaja)box.append(ventajaCard(f));"


def patch_py(s):
    if 'parche 22/11 ventaja' in s:
        return s
    assert s.count(PY_A) == 1, 'ancla EST prod'
    return s.replace(PY_A, PY_ADD + PY_A, 1)


def patch_html(h):
    if FN_V1 in h:
        h = h.replace(FN_V1, FN, 1)
    if 'function ventajaCard' not in h:
        assert h.count('function alertsCard(){') == 1
        h = h.replace('function alertsCard(){', FN + 'function alertsCard(){', 1)
    if JS_N not in h:
        assert h.count(JS_O) == 1, 'brechaCard'
        h = h.replace(JS_O, JS_N, 1)
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
