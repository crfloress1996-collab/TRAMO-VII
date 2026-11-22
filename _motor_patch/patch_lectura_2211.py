"""Parche 22/11 (b) — Se quita el recuadro 'Lectura del frente' de la página de todos los frentes."""

O = "  if(f.nota){const a=el('div','fact');a.append(el('b',null,'Lectura del frente'),el('p',null,f.nota));fx.append(a)}\n"


def patch_html(h):
    if 'Lectura del frente' not in h:
        return h
    assert h.count(O) == 1, 'lectura del frente'
    return h.replace(O, '', 1)


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
