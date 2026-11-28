"""Parche 27/11 — Pestaña MAPA: eje del Tramo VII (KMZ Ejes_Chala@Puquio, punto cada 20 m) con progresivas,
avance por actividad (base, imprimación, micro 1ra/2da, corte XV, cunetas, alcantarillas, muros), lo programado de la
semana, lo ejecutado día por día, los frentes de hoy (vista inicial) y los puntos fijos de PUNTOS_MAPA.xlsx.
Fondo satelital/relieve (Esri) donde la página puede cargar imágenes externas; si no, se ve sin fondo.
Archivos que acompañan al parche (misma carpeta): eje_tramo7.json, leaflet.js, leaflet.css, PUNTOS_MAPA.xlsx (plantilla)."""
import shutil
from pathlib import Path

PY_A = "json.dump(dict(estado=EST, restricciones=RX), open(OUT, 'w')"
PY_ADD = '''# ---------- mapa: eje del Tramo VII y puntos fijos — parche 27/11 mapa
try:
    EST['eje'] = json.load(open(os.path.join(AQUI, 'assets', 'eje_tramo7.json'), encoding='utf-8'))
except Exception as e:
    print('mapa eje', e)
try:
    import openpyxl as _oxm
    _pm = os.path.join(ROOT, '00 TABLET', 'WEB TABLERO', 'PUNTOS_MAPA.xlsx')
    _PT = []
    if os.path.exists(_pm):
        for _r in _oxm.load_workbook(_pm, data_only=True).worksheets[0].iter_rows(min_row=5, values_only=True):
            if len(_r) < 8 or not _r[2]:
                continue
            _k = None
            _mm = re.search(r'(\\d+)\\s*\\+\\s*(\\d+(?:\\.\\d+)?)', str(_r[3] or ''))
            if _mm:
                _k = int(_mm.group(1)) * 1000 + float(_mm.group(2))
            elif isinstance(_r[3], (int, float)):
                _k = float(_r[3]) * (1000 if _r[3] < 1000 else 1)
            _la = _r[5] if isinstance(_r[5], (int, float)) else None
            _lo = _r[6] if isinstance(_r[6], (int, float)) else None
            if _k is None and (_la is None or _lo is None):
                continue
            _PT.append(dict(tipo=str(_r[1] or 'Otro').strip(), nombre=str(_r[2]).strip(), km=_k, lado=str(_r[4] or '').strip().upper(),
                            lat=_la, lon=_lo, nota=str(_r[7]).strip() if _r[7] else None))
    EST['puntos'] = _PT
except Exception as e:
    print('mapa puntos', e)
'''

FN = r"""/*mapa-v1*/(function(){const s=document.createElement('style');s.textContent=".mp-card .mp-bar{display:flex;flex-wrap:wrap;gap:6px;align-items:center;padding:12px 16px;border-bottom:1px solid var(--line2)}.mp-card .mp-bar .mp-lb{font-size:12px;color:var(--muted);margin-right:2px}.mp-chip{font:inherit;font-size:13px;font-weight:600;padding:6px 11px;min-height:34px;border-radius:999px;border:1px solid var(--line);background:var(--panel);color:var(--ink);cursor:pointer}.mp-chip[aria-pressed=true]{background:var(--navy);border-color:var(--navy);color:#fff}.mp-chip i{display:inline-block;width:9px;height:9px;border-radius:50%;margin-right:6px;vertical-align:1px}.mp-go{display:flex;gap:6px;margin-left:auto}.mp-go input{font:inherit;font-size:16px;width:150px;padding:6px 10px;border:1px solid var(--line);border-radius:8px;background:var(--panel);color:var(--ink)}#mp-map{height:min(72vh,760px);min-height:420px;background:var(--sunk);z-index:0}.mp-leg{display:flex;flex-wrap:wrap;gap:6px 16px;padding:10px 16px;font-size:12px;color:var(--muted);border-top:1px solid var(--line2)}.mp-leg span{display:inline-flex;align-items:center;gap:6px}.mp-leg b{display:inline-block;width:22px;height:5px;border-radius:3px}.mp-leg b.mp-ds{background:repeating-linear-gradient(90deg,var(--c) 0 6px,transparent 6px 10px)!important}.mp-leg b.mp-dot{width:12px;height:12px;border-radius:50%}.mp-note{padding:8px 16px;font-size:12px;color:var(--warn);background:var(--warn-s)}.mp-km span{display:inline-block;transform:translate(-50%,-50%);background:rgba(17,22,33,.78);color:#fff;font:600 11px/1.3 var(--f-mono,monospace);padding:1px 5px;border-radius:4px;white-space:nowrap;pointer-events:none}.mp-km.mp-kc span{background:rgba(17,22,33,.55);font-size:10px;font-weight:500}.mp-pt span{display:inline-flex;align-items:center;justify-content:center;transform:translate(-50%,-50%);min-width:24px;height:24px;padding:0 5px;border-radius:12px;color:#fff;font:700 11px/1 var(--f-body,sans-serif);border:2px solid #fff;box-shadow:0 1px 4px rgba(0,0,0,.45);white-space:nowrap}.mp-pt.mp-lg span{padding:0 8px}.mp-fr span{display:inline-block;transform:translate(-50%,-130%);color:#fff;font:700 12px/1.3 var(--f-body,sans-serif);padding:3px 8px;border-radius:6px;box-shadow:0 1px 5px rgba(0,0,0,.5);white-space:nowrap}.mp-pop{font:13px/1.45 var(--f-body,sans-serif);color:#111621;min-width:180px}.mp-pop b{display:block;font-size:14px;margin-bottom:2px}.mp-pop small{color:#5B6474}.mp-pop a{display:inline-block;margin-top:6px;font-weight:600}.mp-list{display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:8px;padding:12px 16px}.mp-list button{font:inherit;text-align:left;padding:9px 11px;border:1px solid var(--line);border-left:5px solid var(--c);border-radius:8px;background:var(--panel);color:var(--ink);cursor:pointer}.mp-list button small{display:block;color:var(--muted);font-size:12px;margin-top:2px}";document.head.append(s)})();
let MAPI=null,LLP=null,EJE=null,MV='hoy',MBASE='sat';
function loadLeaflet(){if(window.L)return Promise.resolve();if(LLP)return LLP;
  if(!document.querySelector('link[data-lf]')){const l=document.createElement('link');l.rel='stylesheet';l.href='leaflet.css';l.dataset.lf='1';document.head.append(l)}
  const add=src=>new Promise((ok,ko)=>{const s=document.createElement('script');s.src=src;s.onload=ok;s.onerror=ko;document.head.append(s)});
  LLP=add('leaflet.js').catch(()=>add('https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.js')).catch(e=>{LLP=null;throw e});return LLP}
function ejeD(){const e=EST.eje;if(!e||!e.p)return null;if(EJE&&EJE.src===e)return EJE;const p=e.p.split(';').map(s=>s.split(',').map(Number));EJE={src:e,k0:e.k0,st:e.paso,kf:e.kfin||(e.k0+e.paso*(p.length-1)),p};return EJE}
function kIx(k){const E=EJE,n=E.p.length,kl=E.k0+E.st*(n-2);if(k<=E.k0)return 0;if(k>=kl)return n-2+Math.min(1,(k-kl)/((E.kf-kl)||1));return (k-E.k0)/E.st}
function kLL(k){const x=kIx(k),i=Math.min(Math.floor(x),EJE.p.length-2),t=x-i,a=EJE.p[i],b=EJE.p[i+1];return [a[0]+(b[0]-a[0])*t,a[1]+(b[1]-a[1])*t]}
function kSeg(a,b){if(a>b)[a,b]=[b,a];const o=[kLL(a)],i1=Math.floor(kIx(a))+1,i2=Math.ceil(kIx(b))-1;for(let i=i1;i<=i2;i++)o.push(EJE.p[i]);o.push(kLL(b));return o}
function kOff(k,lado,m){const p=kLL(k);if(!/^(IZQ|DER)/.test(lado||''))return p;const q=kLL(Math.max(EJE.k0,k-15)),r=kLL(Math.min(EJE.kf,k+15)),c=Math.cos(p[0]*Math.PI/180);
  let e=(r[1]-q[1])*111320*c,n=(r[0]-q[0])*110574;const L=Math.hypot(e,n)||1;e/=L;n/=L;const s=/^DER/.test(lado)?1:-1;return [p[0]+(-e*s*m)/110574,p[1]+(n*s*m)/(111320*c)]}
const mesc=s=>String(s==null?'':s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'})[c]);
const gmap=ll=>'<a href="https://www.google.com/maps/search/?api=1&query='+ll[0].toFixed(6)+','+ll[1].toFixed(6)+'" target="_blank" rel="noopener">Abrir en Google Maps</a>';
const pkm=t=>{const o=[];const re=/(\d{3})\+(\d{3}(?:\.\d+)?)\s*→\s*(\d{3})\+(\d{3}(?:\.\d+)?)/g;let m;while(m=re.exec(t))o.push([+m[1]*1000+ +m[2],+m[3]*1000+ +m[4]]);return o};
const MC={hecho:'#22c55e',parcial:'#facc15',semana:'#fb923c',dia:'#22d3ee',pend:'#9ca3af',bad:'#ef4444'};
const MFR={corte:['Corte XV','#ef4444'],base:['Base','#f59e0b'],imprimacion:['Imprimación','#a855f7'],micro:['Micropavimento','#22d3ee'],cunetas:['Cunetas','#22c55e']};
const MPT={'Acopio':['A','#a16207'],'Punto de agua':['Agua','#0284c7'],'Cantera':['C','#7c3aed'],'Planta':['P','#db2777'],'DME':['DME','#57534e'],'Campamento':['Cp','#059669'],'Descarga':['D','#ea580c'],'Otro':['•','#475569']};
const MVS=[['hoy','Frentes de hoy'],['base','Base'],['imp','Imprimación'],['mp1','Micro 1ra'],['mp2','Micro 2da'],['corte','Corte XV'],['cun','Cunetas'],['alc','Alcantarillas'],['mur','Muros']];
function frHoy(){const dd=EST.dia_det||{},co=D((EST.prod&&EST.prod.corte)||EST.fecha_corte),o=[];
  Object.keys(MFR).forEach(id=>{const x=dd[id];if(!x)return;const k=Object.keys(x).sort().pop();if(!k||(co&&days(D(k),co)>4))return;
    const rs=[].concat(...x[k].map(pkm));if(!rs.length)return;const fl=rs.flat();o.push({id,nom:MFR[id][0],c:MFR[id][1],f:k,a:Math.min(...fl),b:Math.max(...fl),rs,txt:x[k]})});return o}
function renderMapa(){
  if(MAPI){MAPI.remove();MAPI=null}
  const v=$('#view');v.textContent='';const box=el('div');box.style.cssText='display:flex;flex-direction:column;gap:18px';
  const c=card('Tramo VII · km 217+340 – 295+347.77','Mapa con progresivas','toca un tramo o un punto para ver el detalle');c.classList.add('mp-card');
  if(!EST.eje){c.append(el('div','empty','Falta el eje del tramo (archivo eje_tramo7.json del motor). Corre ACTUALIZAR_TABLERO.bat.'));box.append(c);v.append(box);return}
  const bar=el('div','mp-bar');bar.append(el('span','mp-lb','Ver:'));
  MVS.forEach(([k,t])=>{const b=el('button','mp-chip',t);b.setAttribute('aria-pressed',String(MV===k));b.onclick=()=>{MV=k;bar.querySelectorAll('.mp-chip[data-v]').forEach(x=>x.setAttribute('aria-pressed',String(x.dataset.v===MV)));drawV(true);legend()};b.dataset.v=k;bar.append(b)});
  const gw=el('div','mp-go');const inp=el('input');inp.placeholder='Ir al km (274+500)';inp.inputMode='text';const gb=el('button','mp-chip','Ir');gw.append(inp,gb);bar.append(gw);
  const bb=el('div','mp-bar');bb.append(el('span','mp-lb','Fondo:'));
  [['sat','Satélite'],['topo','Relieve'],['no','Sin fondo']].forEach(([k,t])=>{const b=el('button','mp-chip',t);b.dataset.b=k;b.setAttribute('aria-pressed',String(MBASE===k));b.onclick=()=>{setBase(k)};bb.append(b)});
  const all=el('button','mp-chip','Todo el tramo');all.style.marginLeft='auto';bb.append(all);
  const note=el('div','mp-note');note.hidden=true;
  const md=el('div');md.id='mp-map';const lg=el('div','mp-leg');const ls=el('div','mp-list');
  c.append(bar,bb,note,md,lg,ls);box.append(c);v.append(box);
  loadLeaflet().then(init).catch(()=>{md.textContent='';md.append(el('div','empty','No se pudo cargar el mapa (sin conexión). Vuelve a intentar con internet.'))});
  let LY=null,BL=null,KM=null,PT=null,okT=0,erT=0;
  function setBase(k){MBASE=k;bb.querySelectorAll('.mp-chip[data-b]').forEach(x=>x.setAttribute('aria-pressed',String(x.dataset.b===k)));if(!MAPI)return;if(BL){MAPI.removeLayer(BL);BL=null}
    const U={sat:'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',topo:'https://server.arcgisonline.com/ArcGIS/rest/services/World_Topo_Map/MapServer/tile/{z}/{y}/{x}'}[k];
    if(!U)return;okT=0;erT=0;BL=L.tileLayer(U,{maxZoom:19,maxNativeZoom:18,attribution:'Imágenes © Esri'}).addTo(MAPI);BL.bringToBack();
    BL.on('tileload',()=>{okT++});BL.on('tileerror',()=>{erT++;if(erT>=6&&!okT){note.hidden=false;note.textContent='Esta página no puede cargar el fondo satelital: se muestra el eje sin fondo. El mapa con satélite está en la página de GitHub.';setBase('no')}})}
  function init(){if(VIEW!=='mapa'||!md.isConnected)return;ejeD();
    MAPI=L.map(md,{zoomControl:true,preferCanvas:false,attributionControl:true});
    setBase(MBASE);
    const E=EJE;L.polyline(E.p,{color:'#111621',weight:7,opacity:.35,interactive:false}).addTo(MAPI);L.polyline(E.p,{color:'#ffffff',weight:3,opacity:.9,interactive:false}).addTo(MAPI);
    KM=L.layerGroup().addTo(MAPI);PT=L.layerGroup().addTo(MAPI);LY=L.layerGroup().addTo(MAPI);
    MAPI.on('zoomend moveend',kms);pts();drawV(true);legend();
    gb.onclick=()=>{const m=String(inp.value).match(/(\d{3})\s*\+?\s*(\d{0,3})/);if(!m)return;const k=+m[1]*1000+(+(m[2]||0));if(k<E.k0||k>E.kf){inp.value='';inp.placeholder='Fuera del tramo';return}
      const ll=kLL(k);MAPI.setView(ll,17);L.popup().setLatLng(ll).setContent('<div class="mp-pop"><b>km '+km(k)+'</b>'+gmap(ll)+'</div>').openOn(MAPI)};
    inp.onkeydown=e=>{if(e.key==='Enter')gb.onclick()};
    all.onclick=()=>MAPI.fitBounds(L.latLngBounds(E.p),{padding:[20,20]})}
  function kms(){if(!KM)return;KM.clearLayers();const z=MAPI.getZoom(),st=z<10?10000:z<11?5000:z<14?1000:z<15?500:z<16?200:100,bd=MAPI.getBounds().pad(.2);
    for(let k=Math.ceil(EJE.k0/st)*st;k<=EJE.kf;k+=st){const ll=kLL(k);if(!bd.contains(ll))continue;const mj=k%1000===0;
      KM.addLayer(L.marker(ll,{icon:L.divIcon({className:'mp-km'+(mj?'':' mp-kc'),html:'<span>'+(mj?String(k/1000):km(k))+'</span>',iconSize:null}),interactive:false,keyboard:false}))}}
  function pts(){(EST.puntos||[]).forEach(p=>{const ll=(p.lat!=null&&p.lon!=null)?[p.lat,p.lon]:(p.km!=null?kOff(p.km,p.lado,30):null);if(!ll)return;const t=MPT[p.tipo]||MPT.Otro;
    const mk=L.marker(ll,{icon:L.divIcon({className:'mp-pt'+(t[0].length>1?' mp-lg':''),html:'<span style="background:'+t[1]+'">'+mesc(t[0])+'</span>',iconSize:null}),title:p.nombre});
    mk.bindPopup('<div class="mp-pop"><b>'+mesc(p.nombre)+'</b><small>'+mesc(p.tipo)+(p.km!=null?' · km '+km(p.km):'')+(p.lado?' · '+mesc(p.lado):'')+'</small>'+(p.nota?'<div>'+mesc(p.nota)+'</div>':'')+gmap(ll)+'</div>');PT.addLayer(mk)})}
  function seg(a,b,o,pop){if(b-a<1)return;const l=L.polyline(kSeg(a,b),Object.assign({weight:6,opacity:.95,lineCap:'butt'},o));if(pop)l.bindPopup('<div class="mp-pop">'+pop+'</div>');LY.addLayer(l);return l}
  function capa(n){return (EST.mapa||[]).find(x=>x.capa.startsWith(n))}
  function drawCapa(cp,nom,fid,filt){if(!cp)return [];const rg=cp.rango||[EJE.k0,EJE.kf];seg(rg[0],rg[1],{color:MC.pend,weight:4,opacity:.55},'<b>'+mesc(nom)+'</b>Pendiente');
    const B=[];const T={hecho:['Hecho',MC.hecho],parcial:['Un solo lado',MC.parcial],pendiente:['Pendiente',MC.bad],semana:['Programado '+(EST.prod?EST.prod.semana:'semana'),MC.semana]};
    cp.tramos.filter(t=>t[2]!=='semana').forEach(t=>{const s=T[t[2]]||T.hecho;seg(t[0],t[1],{color:s[1]},'<b>'+mesc(nom)+' · '+s[0]+'</b>km '+km(t[0])+' → '+km(t[1])+' <small>('+fmt(Math.abs(t[1]-t[0]))+' m)</small>')});
    cp.tramos.filter(t=>t[2]==='semana').forEach(t=>{seg(t[0],t[1],{color:MC.semana,weight:4,dashArray:'8 7',opacity:1},'<b>'+mesc(nom)+' · programado '+mesc(EST.prod?EST.prod.semana:'')+'</b>km '+km(t[0])+' → '+km(t[1]));B.push(t[0],t[1])});
    const f=EST.frentes.find(x=>x.id===fid);if(f&&f.mapa_sem&&SEM===0)(f.mapa_sem.filas||[]).filter(r=>!filt||filt(r.capa)).forEach(r=>r.tramos.filter(t=>t[2]!=='antes').forEach(t=>{seg(t[0],t[1],{color:MC.dia,weight:8,opacity:.95},'<b>'+mesc(r.capa)+'</b>Ejecutado '+mesc(t[2])+'<br>km '+km(t[0])+' → '+km(t[1])+' <small>('+fmt(Math.abs(t[1]-t[0]))+' m)</small>');B.push(t[0],t[1])}));
    return B}
  function drawV(first){if(!MAPI)return;LY.clearLayers();ls.textContent='';let B=[];
    if(MV==='hoy'){const H=frHoy();H.forEach(h=>{h.rs.forEach(r=>seg(r[0],r[1],{color:h.c,weight:9},'<b>'+mesc(h.nom)+' · '+fdm(D(h.f))+'</b>'+h.txt.map(mesc).join('<br>')));
        const ll=kLL((h.a+h.b)/2);LY.addLayer(L.marker(ll,{icon:L.divIcon({className:'mp-fr',html:'<span style="background:'+h.c+'">'+mesc(h.nom)+'</span>',iconSize:null}),interactive:false}));B.push(h.a,h.b);
        const bt=el('button');bt.style.setProperty('--c',h.c);bt.append(el('b',null,h.nom),el('small',null,fdm(D(h.f))+' · km '+km(h.a)+' → '+km(h.b)));bt.onclick=()=>{MAPI.fitBounds(L.latLngBounds(kSeg(h.a-150,h.b+150)),{padding:[30,30],maxZoom:17});MAPI.getContainer().scrollIntoView({behavior:'smooth',block:'center'})};ls.append(bt)});
      (EST.puntos||[]).filter(p=>/planta/i.test(p.tipo)&&p.km!=null).forEach(p=>B.push(p.km))}
    else if(MV==='base')B=drawCapa(capa('Base'),'Base','base');
    else if(MV==='imp')B=drawCapa(capa('Imprim'),'Imprimación','imprimacion');
    else if(MV==='mp1')B=drawCapa(capa('Micropavimento 1ra'),'Micro 1ra capa','micro',n=>/1ra/.test(n));
    else if(MV==='mp2')B=drawCapa(capa('Micropavimento 2da'),'Micro 2da capa','micro',n=>/2da/.test(n));
    else if(MV==='corte'){const f=EST.frentes.find(x=>x.id==='corte');(f&&f.zonas||[]).forEach(z=>{const e=String(z.estado||'').toUpperCase(),col=e.startsWith('TERM')?MC.hecho:e.includes('PROCESO')?MC.parcial:MC.bad;
        seg(z.desde,z.hasta,{color:col,weight:9},'<b>'+mesc(z.zona)+' · '+mesc(z.trabajo)+'</b>km '+km(z.desde)+' → '+km(z.hasta)+' · '+mesc(z.lado||'')+'<br>'+mesc(z.estado)+(z.falta!=null?' · falta '+fmt(z.falta)+' m³':'')+(z.nota?'<br><small>'+mesc(z.nota)+'</small>':''));B.push(z.desde,z.hasta)});
      (capa('Corte')||{tramos:[]}).tramos.filter(t=>t[2]==='semana').forEach(t=>seg(t[0],t[1],{color:MC.semana,weight:4,dashArray:'8 7'},'<b>Programado '+mesc(EST.prod?EST.prod.semana:'')+'</b>km '+km(t[0])+' → '+km(t[1])))}
    else if(MV==='cun'){const f=EST.frentes.find(x=>x.id==='cunetas');(f&&f.cu_lista||[]).forEach(t=>{const e=String(t.estado).toUpperCase(),col=e.startsWith('TERM')?MC.hecho:e.includes('PROCESO')?MC.parcial:MC.pend,pf=e.startsWith('TERM')?0:(t.panos_falta||0);
        seg(t.desde,t.hasta,{color:col,weight:e.startsWith('TERM')||e.includes('PROCESO')?7:4},'<b>Cuneta '+mesc(t.id)+' · '+mesc(t.lado||'')+'</b>km '+km(t.desde)+' → '+km(t.hasta)+'<br>Hecho '+fmt(t.hecho||0)+' de '+fmt(t.largo||0)+' m · faltan '+fmt(t.falta||0)+' m'+(t.panos!=null?' ('+fmt(pf)+' paños)':''));
        if(e.includes('PROCESO'))B.push(t.desde,t.hasta)})}
    else if(MV==='alc'){const f=EST.frentes.find(x=>x.id==='alcantarillas');(f&&f.oa_lista||[]).forEach(o=>{if(o.km==null)return;const EL=['ent','sal','emb','dis'],NM={ent:'Cabezal entrada',sal:'Cabezal salida',emb:'Emboquillado',dis:'Disipador'};
        const falta=EL.filter(k=>o[k]===0),todo=!falta.length&&EL.some(k=>o[k]===1),e=String(o.estado||'').toUpperCase(),col=todo?MC.hecho:(o.ent!==0&&o.sal!==0)?MC.parcial:e.includes('PROCESO')?MC.semana:MC.bad;
        const ll=kLL(o.km);const m=L.circleMarker(ll,{radius:8,color:'#fff',weight:2,fillColor:col,fillOpacity:1});
        m.bindPopup('<div class="mp-pop"><b>'+mesc(o.cod)+'</b><small>'+mesc(o.tipo)+'</small><br>'+EL.filter(k=>o[k]!=null).map(k=>(o[k]===1?'✓ ':'○ ')+NM[k]).join('<br>')+'<br><small>'+mesc(o.estado)+(o.proy?' · proy. '+fdm(D(o.proy)):'')+'</small><br>'+gmap(ll)+'</div>');LY.addLayer(m);if(!todo)B.push(o.km)})}
    else if(MV==='mur'){const f=EST.frentes.find(x=>x.id==='muros');(f&&f.muros_lista||[]).forEach(o=>{if(o.desde==null)return;const e=String(o.estado||'').toUpperCase(),col=e.startsWith('TERM')?MC.hecho:e.includes('PROCESO')?MC.parcial:MC.bad;
        const ll=kOff((o.desde+(o.hasta||o.desde))/2,o.lado,10);const m=L.circleMarker(ll,{radius:8,color:'#fff',weight:2,fillColor:col,fillOpacity:1});
        m.bindPopup('<div class="mp-pop"><b>'+mesc(o.cod)+'</b><small>'+mesc(o.lado||'')+' · '+fmt(o.largo||0)+' m × '+fmt(o.alto||0,1)+' m</small><br>Bolsas '+fmt(o.hechas||0)+' de '+fmt(o.meta||0)+'<br><small>'+mesc(o.estado)+'</small><br>'+gmap(ll)+'</div>');LY.addLayer(m);if(!e.startsWith('TERM'))B.push(o.desde)})}
    if(first||MV==='hoy'){if(B.length){const a=Math.min(...B),b=Math.max(...B);MAPI.fitBounds(L.latLngBounds(kSeg(Math.max(EJE.k0,a-300),Math.min(EJE.kf,b+300))),{padding:[30,30],maxZoom:16})}else MAPI.fitBounds(L.latLngBounds(EJE.p),{padding:[20,20]})}
    kms()}
  function legend(){lg.textContent='';const it=(c,t,cl)=>{const s=el('span');const b=el('b',cl||null);b.style.background=c;b.style.setProperty('--c',c);s.append(b,document.createTextNode(t));lg.append(s)};
    if(MV==='hoy')Object.values(MFR).forEach(([n,c])=>it(c,n));
    else if(MV==='alc'){it(MC.hecho,'Completa','mp-dot');it(MC.parcial,'Falta emboquillado / disipador','mp-dot');it(MC.semana,'En proceso','mp-dot');it(MC.bad,'Atrasada / pendiente','mp-dot')}
    else if(MV==='mur'){it(MC.hecho,'Terminado','mp-dot');it(MC.parcial,'En proceso','mp-dot');it(MC.bad,'Pendiente','mp-dot')}
    else if(MV==='cun'){it(MC.hecho,'Terminado');it(MC.parcial,'En proceso');it(MC.pend,'Pendiente')}
    else if(MV==='corte'){it(MC.hecho,'Terminado');it(MC.parcial,'En proceso');it(MC.bad,'Pendiente');it(MC.semana,'Programado '+(EST.prod?EST.prod.semana:''),'mp-ds')}
    else{it(MC.hecho,'Hecho (los dos lados)');it(MC.parcial,'Un solo lado');it(MC.dia,'Ejecutado esta semana (toca para ver el día)');it(MC.semana,'Programado '+(EST.prod?EST.prod.semana:''),'mp-ds');it(MC.pend,'Pendiente')}
    Object.entries(MPT).filter(([k])=>(EST.puntos||[]).some(p=>p.tipo===k)).forEach(([k,[a,c]])=>it(c,k,'mp-dot'))}
}
"""

NAV_O = "gd.style.setProperty('--sev','var(--amber)');n.append(gd);"
NAV_N = NAV_O + "const gm=el('button','gen');gm.dataset.v='mapa';gm.append(el('span','nm','Mapa'),el('span','gr','Tramo VII con progresivas y avance'));gm.style.setProperty('--sev','var(--d5)');n.append(gm);"
RD_O = "else if(VIEW==='dia'){RF='todos';renderDia()}"
RD_N = "else if(VIEW==='mapa'){RF='todos';renderMapa()}" + RD_O
KP_O = "$('#kpis').style.display=(f||VIEW==='dia')?'none':'';"
KP_N = KP_O + "if(VIEW==='mapa')$('#kpis').style.display='none';"   # deja intacta la marca de patch_kpis_2111
KP_X = "$('#kpis').style.display=(f||VIEW==='dia'||VIEW==='mapa')?'none':'';"   # versión anterior de este parche


def patch_py(s):
    if 'parche 27/11 mapa' in s:
        return s
    assert s.count(PY_A) == 1, 'ancla json.dump final'
    return s.replace(PY_A, PY_ADD + PY_A, 1)


def patch_html(h):
    if '/*mapa-v1*/' not in h:
        assert h.count('function alertsCard(){') == 1
        h = h.replace('function alertsCard(){', FN + 'function alertsCard(){', 1)
    if KP_X in h:
        h = h.replace(KP_X, KP_N, 1)
    for o, n in ((NAV_O, NAV_N), (RD_O, RD_N), (KP_O, KP_N)):
        if n not in h:
            assert h.count(o) == 1, o[:40]
            h = h.replace(o, n, 1)
    return h


def aplicar(motor):
    motor, msg = Path(motor), []
    aqui = Path(__file__).resolve().parent
    for nom, fn in (('dash_data.py', patch_py), ('tablero.html', patch_html)):
        f = motor / nom
        a = f.read_text(encoding='utf8')
        b = fn(a)
        if b != a:
            f.write_text(b, encoding='utf8')
            msg.append(nom)
    # archivos que acompañan: eje (assets del motor), Leaflet (junto a cada index.html) y la plantilla de puntos (no se pisa)
    cop = [(aqui / 'eje_tramo7.json', motor / 'assets' / 'eje_tramo7.json')]
    for d in (motor, motor.parent):
        cop += [(aqui / 'leaflet.js', d / 'leaflet.js'), (aqui / 'leaflet.css', d / 'leaflet.css')]
    for src, dst in cop:
        if src.exists() and (not dst.exists() or dst.read_bytes() != src.read_bytes()):
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy(src, dst)
            msg.append(dst.name)
    pm = motor.parent / 'PUNTOS_MAPA.xlsx'
    if (aqui / 'PUNTOS_MAPA.xlsx').exists() and not pm.exists():
        shutil.copy(aqui / 'PUNTOS_MAPA.xlsx', pm)
        msg.append(pm.name)
    return msg


if __name__ == '__main__':
    import sys
    p = sys.argv[1]
    h = patch_html(open(p, encoding='utf8').read())
    open(p, 'w', encoding='utf8').write(h)
    print('ok')
