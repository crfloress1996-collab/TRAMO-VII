"""Parche 21/11 (b) — Muros bolsacreto: el aviso 'Frente detenido · se reanuda el lunes 09/11' solo se muestra
antes de esa fecha; después queda la meta de 100 bolsas/día y lo que falta."""

R = [
    ("fin_sub=f\"se reanuda el lunes {CAMPO['muros_reinicio']:%d/%m}\", estado='warn',",
     "fin_sub=(f\"se reanuda el lunes {CAMPO['muros_reinicio']:%d/%m}\" if LUN < CAMPO['muros_reinicio'] else None), estado='warn',"),
    ("donde=f\"Frente detenido · se reanuda el lunes {CAMPO['muros_reinicio']:%d/%m}\", comp=COMP_MUROS,",
     "donde=(f\"Frente detenido · se reanuda el lunes {CAMPO['muros_reinicio']:%d/%m}\" if LUN < CAMPO['muros_reinicio'] else None), comp=COMP_MUROS,"),
    ("nota=f\"Se reanuda el lunes {CAMPO['muros_reinicio']:%d/%m} con 1 frente a 100 bolsas/día. Faltan",
     "nota=(f\"Se reanuda el lunes {CAMPO['muros_reinicio']:%d/%m} con 1 frente a 100 bolsas/día. \" if LUN < CAMPO['muros_reinicio'] else \"1 frente a 100 bolsas/día. \") + f\"Faltan"),
]


def patch_py(s):
    for o, n in R:
        if n in s:
            continue
        assert s.count(o) == 1, ('no encontrado', o[:50])
        s = s.replace(o, n, 1)
    return s


def aplicar(motor):
    from pathlib import Path
    f = Path(motor) / 'dash_data.py'
    a = f.read_text(encoding='utf8')
    b = patch_py(a)
    if b != a:
        f.write_text(b, encoding='utf8')
        return ['dash_data.py']
    return []


if __name__ == '__main__':
    import sys
    p = sys.argv[1]
    s = patch_py(open(p, encoding='utf8').read())
    open(p, 'w', encoding='utf8').write(s)
    print('ok')
