"""Parche 21/11 (c) — Los indicadores de arriba (cierre del tramo, corte, base, restricciones, PPC) solo se ven
en el Resumen general: el atributo hidden no ganaba al display:grid de .kstrip."""

O = "$('#kpis').hidden=!!f||VIEW==='dia';"
N = "$('#kpis').style.display=(f||VIEW==='dia')?'none':'';"


def patch_html(h):
    if N in h:
        return h
    assert h.count(O) == 1, 'kpis hidden'
    return h.replace(O, N, 1)


def aplicar(motor):
    from pathlib import Path
    f = Path(motor) / 'tablero.html'
    a = f.read_text(encoding='utf8')
    b = patch_html(a)
    if b != a:
        f.write_text(b, encoding='utf8')
        return ['tablero.html']
    return []


if __name__ == '__main__':
    import sys
    p = sys.argv[1]
    h = patch_html(open(p, encoding='utf8').read())
    open(p, 'w', encoding='utf8').write(h)
    print('ok')
