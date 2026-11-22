"""Parche 22/11 (l) — Mapa de la semana de base: en cada actividad (refine, batido, aporte, escarificado) se escribe
la progresiva donde se quedó el frente, al final de la cota de lo que falta."""

O = "'falta '+fmt(fr-ca)+' m'))})}"
N = ("'falta '+fmt(fr-ca)+' m'));\n      s.append(sv('text',{x:X2-5,y:y-8,'text-anchor':'end',class:'cotk'},'◂ '+km(fr)))})}")
CSS = ("(function(){const s=document.createElement('style');s.textContent=\".lin .cotk{font-size:10.5px;font-weight:700;fill:var(--amber);"
       "paint-order:stroke;stroke:var(--track);stroke-width:4px;stroke-linejoin:round}\";document.head.append(s)})();\n")


def patch_html(h):
    if "class:'cotk'" in h:
        return h
    assert h.count(O) == 1, 'cota de lo que falta'
    h = h.replace(O, N, 1)
    assert h.count('function alertsCard(){') == 1
    return h.replace('function alertsCard(){', CSS + 'function alertsCard(){', 1)


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
