"""Parche 22/11 (m) — Mapas de la semana de imprimación y micro: en cada hueco a cerrar se escriben las progresivas
donde se quedó el trabajo a cada lado (inicio ▸ y ◂ fin), y en la nota de abajo los tramos de cada hueco."""

O1 = "fmt(gb-ga)+' m'))})});"
N1 = ("fmt(gb-ga)+' m'));\n"
      "      if(X2-X1>150){s.append(sv('text',{x:X1+5,y:y-8,'text-anchor':'start',class:'cotk'},km(ga)+' ▸'));s.append(sv('text',{x:X2-5,y:y-8,'text-anchor':'end',class:'cotk'},'◂ '+km(gb)))}\n"
      "      else if(X2-X1>78)s.append(sv('text',{x:(X1+X2)/2,y:y-8,'text-anchor':'middle',class:'cotk'},km(ga)+' – '+km(gb)))})});")
O2 = "fmt(g.reduce((q,[a,b])=>q+b-a,0))+' m en '+g.length+(g.length>1?' huecos':' hueco')"
N2 = "fmt(g.reduce((q,[a,b])=>q+b-a,0))+' m ('+g.map(([a,b])=>km(a)+' – '+km(b)).join(' · ')+')'"


def patch_html(h):
    if N2 in h:
        return h
    for o, n in ((O1, N1), (O2, N2)):
        assert h.count(o) == 1, ('huecos', o[:30])
        h = h.replace(o, n, 1)
    return h


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
