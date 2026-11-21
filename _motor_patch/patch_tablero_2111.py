"""Parche 21/11 — Resumen general:
 1) 'Alertas del día' se reemplaza por 'Producción del día' (meta, hecho y % del último día con partes, y la restricción principal);
 2) diagrama lineal: botón 'Ampliar' (pantalla completa, por sector y con zoom + / −);
 3) tabla de frentes: TERMINA = según el plan y a este ritmo; columna 'Diferencia' (días de atraso vs plan).
Uso: patch_tablero_2111.py <tablero.html o index.html> [dash_data.py]"""
import sys

CSS = """.zbtn{font:600 12px var(--f-ui,inherit);padding:6px 10px;border:1px solid var(--line);border-radius:8px;background:var(--card,transparent);color:var(--ink);cursor:pointer;white-space:nowrap}
.zbtn:hover{border-color:var(--navy)}
.zov{position:fixed;inset:0;z-index:1000;background:var(--bg,#fff);display:flex;flex-direction:column}
.zbar{display:flex;flex-wrap:wrap;gap:8px;align-items:center;padding:12px 16px;border-bottom:1px solid var(--line)}
.zbar b{margin-right:auto;font-size:15px}
.zb{font:600 12.5px inherit;padding:7px 12px;border:1px solid var(--line);border-radius:8px;background:transparent;color:var(--ink);cursor:pointer}
.zb[aria-pressed=true]{background:var(--navy);color:#fff;border-color:var(--navy)}
.zb.zx{border-color:var(--bad);color:var(--bad)}
.zbox{flex:1;overflow:auto;padding:16px}
.zbox svg{display:block;height:auto}
.dr td small{color:var(--muted);font-size:11.5px;line-height:1.35;display:block;max-width:420px}
.lnk{font:600 12px inherit;background:none;border:0;color:var(--navy);cursor:pointer;padding:4px 0}
"""

FN = r"""function diaResCard(){
  const dn=['Dom','Lun','Mar','Mié','Jue','Vie','Sáb'];
  const fs=frentes().filter(f=>{const x=prodMain(f);return x&&x.meta});
  let dk=null;fs.forEach(f=>prodMain(f).dias.forEach(d=>{if(!d.futuro&&d.ef&&(!dk||d.fecha>dk))dk=d.fecha}));
  const bt=el('button','lnk','Ver detalle del día →');bt.onclick=()=>go('dia');
  const c=card('Producción del día',dk?('Cómo nos fue el '+dn[D(dk).getDay()]+' '+fd(dk)):'Todavía no hay partes',bt);
  const b=el('div','card-b');const t=el('table','ft dr');const th=el('thead');const tr=el('tr');
  [['Frente'],['Meta / día','r'],['Hecho','r'],['Cumplimiento'],['Restricción principal']].forEach(([h,c2])=>tr.append(el('th',c2||null,h)));th.append(tr);t.append(th);const tb=el('tbody');
  fs.forEach(f=>{const x=prodMain(f);const d=x.dias.find(z=>z.fecha===dk);const r=el('tr');r.onclick=()=>go(f.id);
    const c1=el('td','fn');const nb=el('button',null,f.nombre);nb.onclick=e=>{e.stopPropagation();go(f.id)};c1.append(nb);
    const ob=((EST.dia_obs||{})[f.id]||{})[dk];const sinParte=!d||!d.ef;
    const v=d?(d.v||0):0,p=x.meta?v/x.meta:0,sm=p>=1?'ok':p>=.8?'warn':'bad';
    const c2=el('td','r');c2.append(el('span','mono',fmt(x.meta)+' '+x.und));
    const c3=el('td','r');c3.append(el('span','mono',sinParte?'—':fmt(v)+' '+x.und));
    const c4=el('td');if(sinParte)c4.append(el('small',null,'Sin parte'));else{const ab=el('div','ab');const tr2=el('div','tr');const i=el('i');i.style.width=Math.min(100,p*100)+'%';i.style.background='var(--'+sm+')';tr2.append(i);ab.append(tr2,el('b',null,Math.round(p*100)+' %'));c4.append(ab)}
    const c5=el('td');const rx=ob&&ob.rx&&ob.rx.length?ob.rx[0]:null;let txt=rx?((rx.causa?rx.causa+': ':'')+(rx.que||'')):((ob&&ob.notas&&ob.notas[0])||(sinParte?'':'—'));if(txt.length>120)txt=txt.slice(0,117)+'…';c5.append(el('small',null,txt));
    r.append(c1,c2,c3,c4,c5);tb.append(r)});
  t.append(tb);const sc=el('div','scroll');sc.append(t);b.append(sc);c.append(b);return c;
}
function zoomLinear(){
  const ov=el('div','zov');ov.setAttribute('role','dialog');ov.setAttribute('aria-label','Diagrama lineal ampliado');
  const bar=el('div','zbar');bar.append(el('b',null,'Diagrama lineal · avance por capa'));
  const R=[['Todo el tramo',KM_A,KM_B,5000],['Sector XIII',217340,251820,2000],['Sector XIV',251820,276810,2000],['Sector XV',276810,295348,1000],['Corte XV · km 284–295',284000,295348,1000]];
  const SEC=[[217340,251820,'SECTOR XIII · MEJORAMIENTO'],[251820,276810,'SECTOR XIV · CONSERV. PERIÓDICA'],[276810,295348,'SECTOR XV · MEJORAMIENTO']];
  let cur=0,z=1;const box=el('div','zbox');let bs=[];
  const draw=()=>{box.textContent='';const [n,a,b,st]=R[cur];const hit=(EST.hitos||[]).filter(h=>h.km!==251820&&h.km!==276810);
    const {svg}=linearSvg({rows:EST.mapa||[],A:a,B:b,step:st,pct:cur===0,hitos:hit,label:'Diagrama lineal · '+n,
      sectors:SEC.filter(s=>s[1]>a&&s[0]<b).map(s=>[Math.max(s[0],a),Math.min(s[1],b),s[2]])});
    svg.style.width=(100*z)+'%';svg.style.maxWidth='none';box.append(svg);bs.forEach((x,i)=>x.setAttribute('aria-pressed',i===cur?'true':'false'));zl.textContent=Math.round(z*100)+' %'};
  bs=R.map((r,i)=>{const x=el('button','zb',r[0]);x.onclick=()=>{cur=i;draw()};bar.append(x);return x});
  const zm=el('button','zb','−');zm.setAttribute('aria-label','Alejar');zm.onclick=()=>{z=Math.max(1,z-0.5);draw()};
  const zl=el('span','mono','100 %');const zp=el('button','zb','+');zp.setAttribute('aria-label','Acercar');zp.onclick=()=>{z=Math.min(4,z+0.5);draw()};
  const cl=el('button','zb zx','✕ Cerrar');const esc=e=>{if(e.key==='Escape')close()};const close=()=>{ov.remove();document.removeEventListener('keydown',esc)};cl.onclick=close;document.addEventListener('keydown',esc);
  bar.append(zm,zl,zp,cl);ov.append(bar,box);document.body.append(ov);draw();cl.focus();
}
"""

JS = [
    # el diagrama no dibuja la pista con ancho negativo cuando se mira un sector
    ("s.append(sv('rect',{x:x(Math.max(ra[0],o.A)),y:by,width:x(Math.min(ra[1],o.B))-x(Math.max(ra[0],o.A)),height:bh,rx:3,fill:'var(--track)'}));",
     "s.append(sv('rect',{x:x(Math.max(ra[0],o.A)),y:by,width:Math.max(0,x(Math.min(ra[1],o.B))-x(Math.max(ra[0],o.A))),height:bh,rx:3,fill:'var(--track)'}));"),
    # botón Ampliar en el diagrama lineal
    ("const sc=el('div','scroll');sc.append(svg);const b=el('div','card-b');b.append(sc);c.append(b);return c;\n}\nfunction weekMapCard(f){",
     "const zb=el('button','zbtn','⤢ Ampliar');zb.title='Ver el diagrama en pantalla completa, por sector y con zoom';zb.onclick=()=>zoomLinear();c.querySelector('.card-h').append(zb);\n  const sc=el('div','scroll');sc.append(svg);const b=el('div','card-b');b.append(sc);c.append(b);return c;\n}\nfunction weekMapCard(f){"),
    # resumen: producción del día en lugar de alertas
    ("box.append(alertsCard(),linearCard(),", "box.append(diaResCard(),linearCard(),"),
    # tabla: encabezado
    ("['Termina','r'],['Plan / referencia','r']]", "['Termina','r'],['Diferencia','r']]"),
]
OLD_TERM_START = "    const late=f.meta_fin&&f.fin&&D(f.fin)>D(f.meta_fin);"
OLD_TERM_END = "c7.append(s7);"
NEW_TERM = """    const fp=f.fin_plan,fr=f.fin_ritmo,late=fp&&fr&&D(fr)>D(fp);
    const c6=el('td','r');const s6=el('div','two');
    if(fp||('fin_ritmo' in f)){if(fp)s6.append(el('span','mono',fd(fp)),el('small',null,'según el plan'));s6.append(el('span','mono'+(late?' late':''),fr?fd(fr):'—'),el('small',null,fr?'a este ritmo':'sin avance esta semana'))}
    else s6.append(el('span','mono',fd(f.fin)),el('small',null,f.fin_lbl?f.fin_lbl.toLowerCase():'a este ritmo'));c6.append(s6);
    const c7=el('td','r');const s7=el('div','two');if(fp&&fr){const dd=days(D(fp),D(fr));s7.append(el('span','mono'+(dd>0?' late':''),dd>0?'+'+dd+' días':dd<0?(dd+' días'):'a tiempo'),el('small',null,dd>0?'de atraso vs el plan':'vs el plan'))}else s7.append(el('small',null,f.fin_sub||'—'));c7.append(s7);"""

PY_ANCHOR = "# ---------- PPC de la última semana cerrada"
PY_ADD = '''# ---------- fecha de término por frente: según el plan y a este ritmo (parche 21/11)
try:
    _pl = {'corte': _co_f, 'base': _be_f, 'imprimacion': _im_f, 'micro': _mp_f, 'cunetas': _cu_f, 'alcantarillas': _al_f, 'muros': _mb_f}
    _q = {'base': BE_FALTA, 'imprimacion': _imp_q, 'micro': _mp_q, 'cunetas': _fr['cunetas'].get('falta') or 0,
          'alcantarillas': _fr['alcantarillas'].get('falta') or 0, 'muros': _fr['muros'].get('falta') or 0}
    _pt = _fr.get('planta')
    if _pt and _pt.get('materiales'):
        _m0 = _pt['materiales'][0]
        _q['planta'] = max(0, (_m0.get('meta') or 0) - (_m0.get('hecho') or 0))
        _pl['planta'] = _fi(_q['planta'], 550)
    for _f in FR:
        _i = _f['id']
        if _i in _pl:
            _f['fin_plan'] = iso(_pl[_i])
        _s = next((x for x in (PROD.get(_i) or {}).get('series', []) if x.get('principal')), None)
        _r = _s.get('ratio') if _s else None
        if _i == 'corte':
            _f['fin_ritmo'] = _f.get('fin')
        elif _i in _q:
            _f['fin_ritmo'] = iso(_fi(_q[_i], _r)) if _r and _r > 0 else None
except Exception as e:
    print('termina', e)
'''


def patch_html(h):
    if 'function diaResCard' not in h:
        assert h.count('function alertsCard(){') == 1, 'alertsCard'
        h = h.replace('function alertsCard(){', FN + 'function alertsCard(){', 1)
    if '.zov{' not in h:
        i = h.index('</style>')
        h = h[:i] + CSS + h[i:]
    for o, n in JS:
        if n in h:
            continue
        assert h.count(o) == 1, ('no encontrado', o[:60])
        h = h.replace(o, n, 1)
    if 'const fp=f.fin_plan' not in h:
        i = h.index(OLD_TERM_START)
        j = h.index(OLD_TERM_END, i) + len(OLD_TERM_END)
        h = h[:i] + NEW_TERM + h[j:]
    return h


def patch_py(s):
    if 'parche 21/11' in s:
        return s
    assert s.count(PY_ANCHOR) == 1, 'ancla PPC'
    return s.replace(PY_ANCHOR, PY_ADD + PY_ANCHOR, 1)


def aplicar(motor):
    from pathlib import Path
    motor, msg = Path(motor), []
    for nom, fn in (('tablero.html', patch_html), ('dash_data.py', patch_py)):
        f = motor / nom
        a = f.read_text(encoding='utf8')
        b = fn(a)
        if b != a:
            f.write_text(b, encoding='utf8')
            msg.append(nom)
    return msg


if __name__ == '__main__':
    p = sys.argv[1]
    h = patch_html(open(p, encoding='utf8').read())
    open(p, 'w', encoding='utf8').write(h)
    if len(sys.argv) > 2:
        q = sys.argv[2]
        t = patch_py(open(q, encoding='utf8').read())
        open(q, 'w', encoding='utf8').write(t)
    print('ok')
