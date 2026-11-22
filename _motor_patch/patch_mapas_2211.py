"""Parche 22/11 (e) — Mapas 'esta semana en campo' de base, imprimación y micro:
 - base: se pinta también lo hecho ANTES de la semana (REGISTRO DIARIO de Base emulsión XV);
 - línea ámbar en el km 276+810 (fin del suelo-cemento: hasta ahí llega la base emulsión);
 - lo hecho antes se ve más fuerte;
 - botón 'Vista panorámica' (pantalla completa, zoom, nombres de filas fijos, se abre en lo de esta semana)."""

PY_A1 = "BS_MAPA = _mapa_sem({k: v for k, v in _bsm.items() if v}, orden=True)\n"
PY_ADD1 = '''# ---------- base: lo hecho antes de la semana + meta 276+810 — parche 22/11 mapas
try:
    if BS_MAPA:
        _d0 = min(DIAS)
        _orden = [k for k, _ in _BS_ACT]
        _prev = {lbl: [] for _, lbl in _BS_ACT}
        for r in WB['base']['REGISTRO DIARIO'].iter_rows(min_row=10, values_only=True):
            if not (isinstance(r[0], dt.datetime) and _D(r[0]) < _d0 and str(r[2]).startswith('Base emulsión XV')
                    and isinstance(r[4], (int, float)) and isinstance(r[5], (int, float))):
                continue
            _i = next((i for i, k in enumerate(_orden) if str(r[3]).startswith(k)), None)
            if _i is None:
                continue
            for _j, (_, lbl) in enumerate(_BS_ACT):
                if _j >= _i:
                    _prev[lbl].append([min(r[4], r[5]), max(r[4], r[5])])
        _hmax = BS_MAPA['hasta']
        for fila in BS_MAPA['filas']:
            iv = sorted(_prev.get(fila['capa'], []))
            mg = []
            for x, y in iv:
                if mg and x <= mg[-1][1] + 5:
                    mg[-1][1] = max(mg[-1][1], y)
                else:
                    mg.append([x, y])
            semana = [[t[0], t[1]] for t in fila['tramos']]
            ant = []
            for x, y in mg:
                for u, w in _resta_sem(x, y, semana):
                    ant.append([u, w, 'antes'])
                    _hmax = max(_hmax, w)
            fila['tramos'] = ant + fila['tramos']
        BS_MAPA['desde'] = min(BS_MAPA['desde'], 276810 - 400)
        BS_MAPA['hasta'] = min(295348, _hmax + 300)
except Exception as e:
    print('mapa base antes', e)
'''

PY_A2 = "EST['prod'] = dict(semana=f\"S-{LUN.isocalendar()[1]}\""
PY_ADD2 = '''for _f in FR:   # meta 276+810 en los mapas de la semana — parche 22/11 mapas
    _m = _f.get('mapa_sem')
    if _m and _f['id'] in ('base', 'imprimacion', 'micro'):
        _m['meta'] = 276810
        _m['meta_lbl'] = 'Fin del suelo-cemento · aquí llega la base emulsión' if _f['id'] == 'base' else 'Fin del suelo-cemento (Sector XIV)'
        _m['desde'] = min(_m['desde'], 276810 - 400)
        _m['hasta'] = max(_m['hasta'], 276810 + 400)
'''

JS = [
    ("  const W=1100,L=o.day?150:190,R=o.pct?78:o.day?96:18,top=o.sectors?50:26,rh=o.day?40:38,n=o.rows.length,H=top+n*rh+34;",
     "  const W=o.W||1100,L=o.L!=null?o.L:(o.day?150:190),R=o.pct?78:o.day?96:18,top=o.sectors?50:(o.day&&o.hitos&&o.hitos.length?52:26),rh=o.day?40:38,n=o.rows.length,H=top+n*rh+34;"),
    ("    s.append(sv('text',{x:0,y:y+rh/2,class:'lbl','dominant-baseline':'middle'},r.capa));\n    const ra=r.rango||[o.A,o.B];",
     "    if(!o.nolab)s.append(sv('text',{x:0,y:y+rh/2,class:'lbl','dominant-baseline':'middle'},r.capa));\n    const ra=r.rango||[o.A,o.B];"),
    ("if(ant)g.setAttribute('opacity','.35');", "if(ant)g.setAttribute('opacity','.6');"),
    ("      if(o.day&&!ant&&x(b)-x(a)>40)",
     "      if(o.day&&ant&&x(b)-x(a)>70)s.append(sv('text',{x:(x(a)+x(b))/2,y:by+bh/2+1,'text-anchor':'middle','dominant-baseline':'middle',class:'antl'},'hecho · '+fmt(b-a)+' m'));\n      if(o.day&&!ant&&x(b)-x(a)>40)"),
    ("  (o.hitos||[]).forEach(h=>{if(h.km<o.A||h.km>o.B)return;const X=x(h.km);\n    s.append(sv('line',{x1:X,x2:X,y1:26,y2:top+n*rh+2,stroke:'var(--amber)','stroke-width':1.4,'stroke-dasharray':'4 3'}));\n    s.append(sv('rect',{x:X-1,y:24,width:2,height:6,fill:'var(--amber)'}));\n    s.append(sv('text',{x:X+6,y:33,class:'hito'},h.t+' · '+km(h.km)))});",
     "  (o.hitos||[]).forEach(h=>{if(h.km<o.A||h.km>o.B)return;const X=x(h.km),hy=o.day?top-16:33,rt=X>W*0.7;\n    s.append(sv('line',{x1:X,x2:X,y1:o.day?top-26:26,y2:top+n*rh+2,stroke:'var(--amber)','stroke-width':o.day?2:1.4,'stroke-dasharray':'4 3'}));\n    s.append(sv('rect',{x:X-1,y:o.day?top-28:24,width:2,height:6,fill:'var(--amber)'}));\n    s.append(sv('text',{x:rt?X-6:X+6,y:hy,class:'hito','text-anchor':rt?'end':'start'},(o.day?'▼ ':'')+h.t+' · '+km(h.km)))});"),
]

OLD_WMC = "  const sc=el('div','scroll');sc.append(svg);const b=el('div','card-b');b.append(sc,lg);c.append(b);return c;\n}"
NEW_WMC = "  const zb=el('button','zbtn','⤢ Vista panorámica');zb.title='Ver el mapa en pantalla completa, más de cerca';zb.onclick=()=>zoomWeekMap(f);c.querySelector('.card-h').append(zb);\n  const sc=el('div','scroll');sc.append(svg);const b=el('div','card-b');b.append(sc,lg);c.append(b);return c;\n}"
OLD_WMC_SVG = "const {svg,days}=linearSvg({rows:m.filas,A:m.desde,B:m.hasta,day:true,label:'Tramos ejecutados '+(SEM?'en la '+EST.prod.semana:'esta semana')});"
NEW_WMC_SVG = "const {svg,days}=linearSvg({rows:m.filas,A:m.desde,B:m.hasta,day:true,hitos:m.meta?[{km:m.meta,t:m.meta_lbl||'Meta'}]:[],label:'Tramos ejecutados '+(SEM?'en la '+EST.prod.semana:'esta semana')});"

FN = r"""(function(){const s=document.createElement('style');s.textContent=".lin .antl{font:600 10.5px var(--f-ui,inherit);fill:var(--ink);opacity:.85}";document.head.append(s)})();
function zoomWeekMap(f){
  const m=f.mapa_sem;const ov=el('div','zov');ov.setAttribute('role','dialog');ov.setAttribute('aria-label','Mapa de la semana · vista panorámica');
  const bar=el('div','zbar');bar.append(el('b',null,(SEM?'Semana '+EST.prod.semana:'Esta semana')+' en campo · '+f.nombre+' · vista panorámica'));
  let z=2;const box=el('div','zbox');box.style.cssText='display:flex;align-items:center;padding-left:0';let days=[];
  const wk=m.filas.flatMap(r=>r.tramos.filter(t=>t[2]!=='antes'));const c0=wk.length?(Math.min(...wk.map(t=>Math.min(t[0],t[1])))+Math.max(...wk.map(t=>Math.max(t[0],t[1]))))/2:(m.desde+m.hasta)/2;
  const draw=keep=>{const sl=box.scrollWidth?box.scrollLeft/box.scrollWidth:0;box.textContent='';const W=Math.round(1100*z),L=20,R=96;
    const r=linearSvg({rows:m.filas,A:m.desde,B:m.hasta,day:true,W,L,nolab:true,hitos:m.meta?[{km:m.meta,t:m.meta_lbl||'Meta'}]:[],label:'Mapa de la semana'});days=r.days;const s=r.svg;
    const top=m.meta?52:26,rh=40,H=top+m.filas.length*rh+34;const k=Math.max(1,Math.min(1.6,(box.clientHeight-30)/H));
    const wr=el('div','cpw');const lc=el('div','cpl');m.filas.forEach((rw,i)=>{const d=el('div',null,rw.capa);d.style.top=((top+i*rh+rh/2)*k-10)+'px';lc.append(d)});
    s.style.width=(W*k)+'px';s.style.maxWidth='none';s.style.flex='none';wr.append(lc,s);box.append(wr);zl.textContent=Math.round(z*100)+' %';
    if(keep)box.scrollLeft=sl*box.scrollWidth;else{const X=(L+(c0-m.desde)/(m.hasta-m.desde)*(W-L-R))*k;box.scrollLeft=Math.max(0,190+X-box.clientWidth/2)}};
  const hb=el('button','zb','▼ Ir a esta semana');hb.onclick=()=>draw(false);
  const zm=el('button','zb','−');zm.setAttribute('aria-label','Alejar');zm.onclick=()=>{z=Math.max(1,z-0.5);draw(true)};
  const zl=el('span','mono','200 %');const zp=el('button','zb','+');zp.setAttribute('aria-label','Acercar');zp.onclick=()=>{z=Math.min(6,z+0.5);draw(true)};
  const cl=el('button','zb zx','✕ Cerrar');const esc=e=>{if(e.key==='Escape')close()};const close=()=>{ov.remove();document.removeEventListener('keydown',esc)};cl.onclick=close;document.addEventListener('keydown',esc);
  bar.append(hb,zm,zl,zp,cl);const lgw=el('div','zleg');ov.append(bar,lgw,box);document.body.append(ov);draw(false);
  const lg=el('div','legend');days.forEach((d,i)=>{const s=el('span');const ii=el('i');ii.style.background=`var(--d${i%6+1})`;s.append(ii,document.createTextNode(d));lg.append(s)});
  if(m.filas.some(r=>r.tramos.some(t=>t[2]==='antes'))){const s=el('span');const ii=el('i');ii.style.background='var(--seg-hecho)';ii.style.opacity='.6';s.append(ii,document.createTextNode('Hecho antes de esta semana'));lg.append(s)}
  if(m.meta){const s=el('span');const ii=el('i');ii.style.cssText='background:none;border-left:2px dashed var(--amber);border-radius:0;width:2px';s.append(ii,document.createTextNode((m.meta_lbl||'Meta')+' · '+km(m.meta)));lg.append(s)}
  lgw.append(lg);cl.focus();
}
"""


def patch_py(s):
    if 'parche 22/11 mapas' in s:
        return s
    assert s.count(PY_A1) == 1, 'ancla BS_MAPA'
    assert s.count(PY_A2) == 1, 'ancla EST prod'
    s = s.replace(PY_A1, PY_A1 + PY_ADD1, 1)
    return s.replace(PY_A2, PY_ADD2 + PY_A2, 1)


def patch_html(h):
    ya = 'function zoomWeekMap' in h     # ya aplicado: otros parches (cotas) cambian luego estas líneas
    for o, n in ([] if ya else JS):
        if n in h:
            continue
        assert h.count(o) == 1, ('linearSvg', o[:50])
        h = h.replace(o, n, 1)
    if NEW_WMC_SVG not in h and not ya:
        assert h.count(OLD_WMC_SVG) == 1, 'weekMap svg'
        h = h.replace(OLD_WMC_SVG, NEW_WMC_SVG, 1)
    if 'zoomWeekMap(f);c.querySelector' not in h:
        i = h.index('function weekMapCard(f){')
        j = h.index(OLD_WMC, i)
        h = h[:j] + NEW_WMC + h[j + len(OLD_WMC):]
    if 'function zoomWeekMap' not in h:
        assert h.count('function alertsCard(){') == 1, 'alertsCard'
        h = h.replace('function alertsCard(){', FN + 'function alertsCard(){', 1)
    # leyenda del mapa de la semana: hecho antes más fuerte + la meta
    o = "ii.style.background='var(--seg-hecho)';ii.style.opacity='.35';s.append(ii,document.createTextNode('Hecho antes de esta semana'));lg.append(s)}\n  const zb="
    n = "ii.style.background='var(--seg-hecho)';ii.style.opacity='.6';s.append(ii,document.createTextNode('Hecho antes de esta semana'));lg.append(s)}\n  if(m.meta){const s=el('span');const ii=el('i');ii.style.cssText='background:none;border-left:2px dashed var(--amber);border-radius:0;width:2px';s.append(ii,document.createTextNode((m.meta_lbl||'Meta')+' · '+km(m.meta)));lg.append(s)}\n  const zb="
    if n not in h and o in h:
        h = h.replace(o, n, 1)
    # vistas panorámicas: sin margen a la izquierda para que los nombres de las filas tapen bien al desplazar
    h = h.replace("box.style.cssText='display:flex;align-items:center'", "box.style.cssText='display:flex;align-items:center;padding-left:0'")
    # 'font:… var(--f-ui,inherit)' no es válido: se cambia por tamaño y peso sueltos
    for a, b in (("font:600 10.5px var(--f-ui,inherit)", "font-size:10.5px;font-weight:600"), ("font:600 12px var(--f-ui,inherit)", "font-size:12px;font-weight:600"),
                 ("font:700 10.5px var(--f-ui,inherit)", "font-size:10.5px;font-weight:700"), ("font:700 11.5px var(--f-ui,inherit)", "font-size:11.5px;font-weight:700")):
        h = h.replace(a, b)
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
