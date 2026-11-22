"""Parche 22/11 — Página de cada frente con los mismos datos que la tabla del Resumen:
 'Ritmo real · semana' = lo hecho en la semana ÷ días efectivos (con la meta y el % debajo);
 'Termina a este ritmo' con la fecha según el plan y los días de atraso debajo."""

O = ("  k('Ritmo real',(f.ritmo||'—').split(' (')[0],null,(f.ritmo||'').includes('(')?f.ritmo.slice(f.ritmo.indexOf('(')+1,-1):'');\n"
     "  const late=f.meta_fin&&f.fin&&D(f.fin)>D(f.meta_fin);\n"
     "  k(f.fin_lbl||'Termina a este ritmo',fd(f.fin),null,f.fin_sub||(f.meta_fin?'plan de cierre '+fd(f.meta_fin)+(late?' · '+days(D(f.meta_fin),D(f.fin))+' días tarde':''):''),late?'bad':'');\n")

N = ("  {const x=prodMain(f);if(x&&x.meta){const dc=x.ratio<10&&x.ratio%1?1:0;k('Ritmo real · semana',fmt(x.ratio,dc),x.und+'/día','meta '+fmt(x.meta)+' '+x.und+'/día · '+pct(x.pct),x.sem==='bad'?'bad':'')}\n"
     "  else k('Ritmo real',(f.ritmo||'—').split(' (')[0],null,(f.ritmo||'').includes('(')?f.ritmo.slice(f.ritmo.indexOf('(')+1,-1):'')}\n"
     "  if(f.fin_plan||('fin_ritmo' in f)){const fp=f.fin_plan,fr=f.fin_ritmo,dd=fp&&fr?days(D(fp),D(fr)):null;\n"
     "    k('Termina a este ritmo',fr?fd(fr):'—',null,(fr?'':'sin avance esta semana · ')+(fp?'según el plan '+fd(fp):'')+(dd>0?' · +'+dd+' días de atraso':dd<0?' · '+(-dd)+' días antes':dd===0?' · a tiempo':''),dd>0?'bad':'')}\n"
     "  else{const late=f.meta_fin&&f.fin&&D(f.fin)>D(f.meta_fin);\n"
     "  k(f.fin_lbl||'Termina a este ritmo',fd(f.fin),null,f.fin_sub||(f.meta_fin?'plan de cierre '+fd(f.meta_fin)+(late?' · '+days(D(f.meta_fin),D(f.fin))+' días tarde':''):''),late?'bad':'')}\n")


def patch_html(h):
    if N in h:
        return h
    assert h.count(O) == 1, 'kpis del frente'
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
