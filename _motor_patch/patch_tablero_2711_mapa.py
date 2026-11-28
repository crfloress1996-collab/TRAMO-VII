"""Parche 27/11 — Pestaña MAPA (v2: uno, varios o todos los frentes a la vez, cada uno en su carril, y aviso de frentes que se cruzan): eje del Tramo VII (KMZ Ejes_Chala@Puquio, punto cada 20 m) con progresivas,
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

FN = r"""/*mapa-v2*/(function(){const s=document.createElement('style');s.textContent=".mp-card .mp-bar{display:flex;flex-wrap:wrap;gap:6px;align-items:center;padding:12px 16px;border-bottom:1px solid var(--line2)}.mp-card .mp-bar .mp-lb{font-size:12px;color:var(--muted);margin-right:2px}.mp-chip{font:inherit;font-size:13px;font-weight:600;padding:6px 11px;min-height:34px;border-radius:999px;border:1px solid var(--line);background:var(--panel);color:var(--ink);cursor:pointer}.mp-chip[aria-pressed=true]{background:var(--navy);border-color:var(--navy);color:#fff}.mp-chip.mp-sec{font-weight:500;color:var(--muted)}.mp-chip i{display:inline-block;width:10px;height:10px;border-radius:50%;margin-right:6px;vertical-align:0;box-shadow:0 0 0 1.5px #fff}.mp-go{display:flex;gap:6px;margin-left:auto}.mp-go input{font:inherit;font-size:16px;width:150px;padding:6px 10px;border:1px solid var(--line);border-radius:8px;background:var(--panel);color:var(--ink)}#mp-map{height:min(72vh,760px);min-height:420px;background:var(--sunk);z-index:0}.mp-leg{display:flex;flex-wrap:wrap;gap:6px 16px;padding:10px 16px;font-size:12px;color:var(--muted);border-top:1px solid var(--line2)}.mp-leg span{display:inline-flex;align-items:center;gap:6px}.mp-leg svg{flex:none}.mp-leg b.mp-dot{display:inline-block;width:12px;height:12px;border-radius:50%}.mp-leg b.mp-sq{display:inline-block;width:12px;height:12px;border-radius:2px}.mp-note{padding:8px 16px;font-size:12px;color:var(--warn);background:var(--warn-s)}.mp-km span{display:inline-block;transform:translate(-50%,-50%);background:rgba(17,22,33,.78);color:#fff;font:600 11px/1.3 var(--f-mono,monospace);padding:1px 5px;border-radius:4px;white-space:nowrap;pointer-events:none}.mp-km.mp-kc span{background:rgba(17,22,33,.55);font-size:10px;font-weight:500}.mp-pt span{display:inline-flex;align-items:center;justify-content:center;transform:translate(-50%,-50%);min-width:24px;height:24px;padding:0 5px;border-radius:12px;color:#fff;font:700 11px/1 var(--f-body,sans-serif);border:2px solid #fff;box-shadow:0 1px 4px rgba(0,0,0,.45);white-space:nowrap}.mp-pt.mp-lg span{padding:0 8px}.mp-mu span{display:block;transform:translate(-50%,-50%);width:16px;height:16px;border-radius:3px;border:2px solid #fff;box-shadow:0 1px 3px rgba(0,0,0,.45)}.mp-fr span{display:inline-block;transform:translate(-50%,-130%);color:#fff;font:700 12px/1.3 var(--f-body,sans-serif);padding:3px 8px;border-radius:6px;box-shadow:0 1px 5px rgba(0,0,0,.5);white-space:nowrap}.mp-pop{font:13px/1.45 var(--f-body,sans-serif);color:#111621;min-width:180px}.mp-pop b{display:block;font-size:14px;margin-bottom:2px}.mp-pop small{color:#5B6474}.mp-pop a{display:inline-block;margin-top:6px;font-weight:600}.mp-list{display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:8px;padding:12px 16px}.mp-list button{font:inherit;text-align:left;padding:9px 11px;border:1px solid var(--line);border-left:5px solid var(--c);border-radius:8px;background:var(--panel);color:var(--ink);cursor:pointer}.mp-list button small{display:block;color:var(--muted);font-size:12px;margin-top:2px}.mp-int{padding:4px 16px 14px}.mp-int h3{font-size:13px;margin:8px 0 6px;color:var(--ink)}.mp-int p{margin:0;font-size:13px;color:var(--muted)}.mp-int button{display:flex;gap:10px;align-items:baseline;width:100%;font:inherit;font-size:13px;text-align:left;padding:8px 10px;margin-top:6px;border:1px solid var(--line);border-radius:8px;background:var(--panel);color:var(--ink);cursor:pointer}.mp-int button b{flex:none;min-width:86px;font-family:var(--f-mono,monospace);font-size:12px}.mp-int button.x b{color:var(--bad)}.mp-int button.c b{color:var(--warn)}";document.head.append(s)})();
let MAPI=null,LLP=null,EJE=null,MBASE='sat';const MSEL=new Set(['hoy']);
function loadLeaflet(){if(window.L)return Promise.resolve();if(LLP)return LLP;
  if(!document.querySelector('link[data-lf]')){const l=document.createElement('link');l.rel='stylesheet';l.href='leaflet.css';l.dataset.lf='1';document.head.append(l)}
  const add=src=>new Promise((ok,ko)=>{const s=document.createElement('script');s.src=src;s.onload=ok;s.onerror=ko;document.head.append(s)});
  LLP=add('leaflet.js').catch(()=>add('https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.js')).catch(e=>{LLP=null;throw e});return LLP}
function ejeD(){const e=EST.eje;if(!e||!e.p)return null;if(EJE&&EJE.src===e)return EJE;const p=e.p.split(';').map(s=>s.split(',').map(Number));EJE={src:e,k0:e.k0,st:e.paso,kf:e.kfin||(e.k0+e.paso*(p.length-1)),p};return EJE}
function kIx(k){const E=EJE,n=E.p.length,kl=E.k0+E.st*(n-2);if(k<=E.k0)return 0;if(k>=kl)return n-2+Math.min(1,(k-kl)/((E.kf-kl)||1));return (k-E.k0)/E.st}
function kLL(k){const x=kIx(k),i=Math.min(Math.floor(x),EJE.p.length-2),t=x-i,a=EJE.p[i],b=EJE.p[i+1];return [a[0]+(b[0]-a[0])*t,a[1]+(b[1]-a[1])*t]}
function kSeg(a,b){if(a>b)[a,b]=[b,a];const o=[kLL(a)],i1=Math.floor(kIx(a))+1,i2=Math.ceil(kIx(b))-1;for(let i=i1;i<=i2;i++)o.push(EJE.p[i]);o.push(kLL(b));return o}
function offPts(P,m){if(!m||P.length<2)return P;return P.map((p,i)=>{const q=P[Math.max(0,i-1)],r=P[Math.min(P.length-1,i+1)],c=Math.cos(p[0]*Math.PI/180);let e=(r[1]-q[1])*111320*c,n=(r[0]-q[0])*110574;const L=Math.hypot(e,n)||1;e/=L;n/=L;return [p[0]-e*m/110574,p[1]+n*m/(111320*c)]})}
function kOff(k,lado,m){if(!/^(IZQ|DER)/.test(lado||''))return kLL(k);return offPts(kSeg(Math.max(EJE.k0,k-15),Math.min(EJE.kf,k+15)),/^DER/.test(lado)?m:-m)[1]||kLL(k)}
const mesc=s=>String(s==null?'':s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'})[c]);
const gmap=ll=>'<a href="https://www.google.com/maps/search/?api=1&query='+ll[0].toFixed(6)+','+ll[1].toFixed(6)+'" target="_blank" rel="noopener">Abrir en Google Maps</a>';
const pkm=t=>{const o=[];const re=/(\d{3})\+(\d{3}(?:\.\d+)?)\s*→\s*(\d{3})\+(\d{3}(?:\.\d+)?)/g;let m;while(m=re.exec(t))o.push([+m[1]*1000+ +m[2],+m[3]*1000+ +m[4]]);return o};
const MACT={corte:['Corte XV','#ef4444'],base:['Base','#f59e0b'],imp:['Imprimación','#a855f7'],mp1:['Micro 1ra','#06b6d4'],mp2:['Micro 2da','#2563eb'],cun:['Cunetas','#16a34a'],alc:['Alcantarillas','#db2777'],mur:['Muros','#78716c']};
const MLANE=['corte','base','imp','mp1','mp2','cun'];
const MST={ok:'#22c55e',mid:'#facc15',run:'#fb923c',bad:'#ef4444'};
const MPT={'Acopio':['A','#a16207'],'Punto de agua':['Agua','#0284c7'],'Cantera':['C','#7c3aed'],'Planta':['P','#db2777'],'DME':['DME','#57534e'],'Campamento':['Cp','#059669'],'Descarga':['D','#ea580c'],'Otro':['•','#475569']};
const MFRA={corte:'corte',base:'base',imprimacion:'imp',cunetas:'cun'};
function frHoy(){const dd=EST.dia_det||{},co=D((EST.prod&&EST.prod.corte)||EST.fecha_corte),o=[];
  ['corte','base','imprimacion','micro','cunetas'].forEach(id=>{const x=dd[id];if(!x)return;const k=Object.keys(x).sort().pop();if(!k||(co&&days(D(k),co)>4))return;
    const rs=[].concat(...x[k].map(pkm));if(!rs.length)return;const fl=rs.flat();const act=id==='micro'?(x[k].some(t=>/2da/.test(t))?'mp2':'mp1'):MFRA[id];
    o.push({id,act,nom:id==='micro'?'Micropavimento':MACT[act][0],c:MACT[act][1],f:k,a:Math.min(...fl),b:Math.max(...fl),rs,txt:x[k]})});return o}
function renderMapa(){
  if(MAPI){MAPI.remove();MAPI=null}
  const v=$('#view');v.textContent='';const box=el('div');box.style.cssText='display:flex;flex-direction:column;gap:18px';
  const c=card('Tramo VII · km 217+340 – 295+347.77','Mapa con progresivas','elige uno o varios frentes · toca un tramo o un punto para ver el detalle');c.classList.add('mp-card');
  if(!EST.eje){c.append(el('div','empty','Falta el eje del tramo (archivo eje_tramo7.json del motor). Corre ACTUALIZAR_TABLERO.bat.'));box.append(c);v.append(box);return}
  const bar=el('div','mp-bar');bar.append(el('span','mp-lb','Ver:'));
  const chip=(k,t,col)=>{const b=el('button','mp-chip');if(col){const i=el('i');i.style.background=col;b.append(i)}b.append(document.createTextNode(t));b.dataset.v=k;b.setAttribute('aria-pressed',String(MSEL.has(k)));
    b.onclick=()=>{MSEL.has(k)?MSEL.delete(k):MSEL.add(k);sync();drawV(true)};bar.append(b)};
  chip('hoy','Frentes de hoy','var(--navy)');Object.entries(MACT).forEach(([k,[t,col]])=>chip(k,t,col));
  const ba=el('button','mp-chip mp-sec','Todos');ba.onclick=()=>{MSEL.add('hoy');Object.keys(MACT).forEach(k=>MSEL.add(k));sync();drawV(true)};
  const bn=el('button','mp-chip mp-sec','Limpiar');bn.onclick=()=>{MSEL.clear();sync();drawV(false)};bar.append(ba,bn);
  function sync(){bar.querySelectorAll('.mp-chip[data-v]').forEach(x=>x.setAttribute('aria-pressed',String(MSEL.has(x.dataset.v))))}
  const bb=el('div','mp-bar');bb.append(el('span','mp-lb','Fondo:'));
  [['sat','Satélite'],['topo','Relieve'],['no','Sin fondo']].forEach(([k,t])=>{const b=el('button','mp-chip',t);b.dataset.b=k;b.setAttribute('aria-pressed',String(MBASE===k));b.onclick=()=>{setBase(k)};bb.append(b)});
  const gw=el('div','mp-go');const inp=el('input');inp.placeholder='Ir al km (274+500)';const gb=el('button','mp-chip','Ir');const all=el('button','mp-chip mp-sec','Todo el tramo');gw.append(inp,gb,all);bb.append(gw);
  const note=el('div','mp-note');note.hidden=true;
  const md=el('div');md.id='mp-map';const lg=el('div','mp-leg');const ix=el('div','mp-int');const ls=el('div','mp-list');
  c.append(bar,bb,note,md,lg,ix,ls);box.append(c);v.append(box);
  loadLeaflet().then(init).catch(()=>{md.textContent='';md.append(el('div','empty','No se pudo cargar el mapa (sin conexión). Vuelve a intentar con internet.'))});
  let LY=null,BL=null,KM=null,PT=null,okT=0,erT=0;
  function setBase(k){MBASE=k;bb.querySelectorAll('.mp-chip[data-b]').forEach(x=>x.setAttribute('aria-pressed',String(x.dataset.b===k)));if(!MAPI)return;if(BL){MAPI.removeLayer(BL);BL=null}
    const U={sat:'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',topo:'https://server.arcgisonline.com/ArcGIS/rest/services/World_Topo_Map/MapServer/tile/{z}/{y}/{x}'}[k];
    if(!U)return;okT=0;erT=0;BL=L.tileLayer(U,{maxZoom:19,maxNativeZoom:18,attribution:'Imágenes © Esri'}).addTo(MAPI);BL.bringToBack();
    BL.on('tileload',()=>{okT++});BL.on('tileerror',()=>{erT++;if(erT>=6&&!okT){note.hidden=false;note.textContent='Esta página no puede cargar el fondo satelital: se muestra el eje sin fondo. El mapa con satélite está en la página de GitHub.';setBase('no')}})}
  function zfit(a,b,mx){MAPI.fitBounds(L.latLngBounds(kSeg(Math.max(EJE.k0,a),Math.min(EJE.kf,b))),{padding:[30,30],maxZoom:mx||16})}
  function init(){if(VIEW!=='mapa'||!md.isConnected)return;ejeD();
    MAPI=L.map(md,{zoomControl:true,attributionControl:true});MAPI.fitBounds(L.latLngBounds(EJE.p),{padding:[20,20]});setBase(MBASE);
    const E=EJE;L.polyline(E.p,{color:'#111621',weight:7,opacity:.35,interactive:false}).addTo(MAPI);L.polyline(E.p,{color:'#ffffff',weight:3,opacity:.9,interactive:false}).addTo(MAPI);
    KM=L.layerGroup().addTo(MAPI);LY=L.layerGroup().addTo(MAPI);PT=L.layerGroup().addTo(MAPI);
    MAPI.on('moveend',kms);MAPI.on('zoomend',()=>drawV(false));pts();drawV(true);
    gb.onclick=()=>{const m=String(inp.value).match(/(\d{3})\s*\+?\s*(\d{0,3})/);if(!m)return;const k=+m[1]*1000+(+(m[2]||0));if(k<E.k0||k>E.kf){inp.value='';inp.placeholder='Fuera del tramo';return}
      const ll=kLL(k);MAPI.setView(ll,17);L.popup().setLatLng(ll).setContent('<div class="mp-pop"><b>km '+km(k)+'</b>'+gmap(ll)+'</div>').openOn(MAPI)};
    inp.onkeydown=e=>{if(e.key==='Enter')gb.onclick()};all.onclick=()=>MAPI.fitBounds(L.latLngBounds(E.p),{padding:[20,20]})}
  function kms(){if(!KM)return;KM.clearLayers();const z=MAPI.getZoom(),st=z<10?10000:z<11?5000:z<14?1000:z<15?500:z<16?200:100,bd=MAPI.getBounds().pad(.2);
    for(let k=Math.ceil(EJE.k0/st)*st;k<=EJE.kf;k+=st){const ll=kLL(k);if(!bd.contains(ll))continue;const mj=k%1000===0;
      KM.addLayer(L.marker(ll,{icon:L.divIcon({className:'mp-km'+(mj?'':' mp-kc'),html:'<span>'+(mj?String(k/1000):km(k))+'</span>',iconSize:null}),interactive:false,keyboard:false}))}}
  function pts(){(EST.puntos||[]).forEach(p=>{const ll=(p.lat!=null&&p.lon!=null)?[p.lat,p.lon]:(p.km!=null?kOff(p.km,p.lado,30):null);if(!ll)return;const t=MPT[p.tipo]||MPT.Otro;
    const mk=L.marker(ll,{icon:L.divIcon({className:'mp-pt'+(t[0].length>1?' mp-lg':''),html:'<span style="background:'+t[1]+'">'+mesc(t[0])+'</span>',iconSize:null}),title:p.nombre});
    mk.bindPopup('<div class="mp-pop"><b>'+mesc(p.nombre)+'</b><small>'+mesc(p.tipo)+(p.km!=null?' · km '+km(p.km):'')+(p.lado?' · '+mesc(p.lado):'')+'</small>'+(p.nota?'<div>'+mesc(p.nota)+'</div>':'')+gmap(ll)+'</div>');PT.addLayer(mk)})}
  const lanes=()=>MLANE.filter(x=>MSEL.has(x));
  function lanePx(act){const ls=lanes();if(ls.length<2)return 0;const i=ls.indexOf(act);return i<0?0:(i-(ls.length-1)/2)*8}
  function mpp(){if(!MAPI._loaded)return 0;const c=MAPI.getCenter();return 156543.03392*Math.cos(c.lat*Math.PI/180)/Math.pow(2,MAPI.getZoom())}
  const STY={hecho:{weight:5,opacity:.95},lado:{weight:5,opacity:.95,dashArray:'2 7',lineCap:'round'},prog:{weight:3,opacity:1,dashArray:'10 7'},sem:{weight:9,opacity:1},pend:{weight:2,opacity:.55}};
  function seg(act,a,b,sty,col,pop){if(Math.abs(b-a)<1)return;const l=L.polyline(offPts(kSeg(a,b),lanePx(act)*mpp()),Object.assign({color:col,lineCap:'butt'},STY[sty]));if(pop)l.bindPopup('<div class="mp-pop">'+pop+'</div>');LY.addLayer(l)}
  const capa=n=>(EST.mapa||[]).find(x=>x.capa.startsWith(n));
  const SEMN=()=>EST.prod?EST.prod.semana:'semana';
  function drawCapa(act,cp,fid,filt,B,R){if(!cp)return;const [nom,col]=MACT[act];const solo=lanes().length<2;
    if(solo){const rg=cp.rango||[EJE.k0,EJE.kf];seg(act,rg[0],rg[1],'pend','#9ca3af','<b>'+mesc(nom)+'</b>Pendiente')}
    cp.tramos.filter(t=>t[2]!=='semana').forEach(t=>{const lado=t[2]==='parcial',pend=t[2]==='pendiente';seg(act,t[0],t[1],pend?'pend':lado?'lado':'hecho',pend?MST.bad:col,'<b>'+mesc(nom)+' · '+(lado?'un solo lado':pend?'pendiente':'hecho')+'</b>km '+km(t[0])+' → '+km(t[1])+' <small>('+fmt(Math.abs(t[1]-t[0]))+' m)</small>')});
    cp.tramos.filter(t=>t[2]==='semana').forEach(t=>{seg(act,t[0],t[1],'prog',col,'<b>'+mesc(nom)+' · programado '+mesc(SEMN())+'</b>km '+km(t[0])+' → '+km(t[1]));B.push(t[0],t[1]);R.push({act,t:'programado',a:Math.min(t[0],t[1]),b:Math.max(t[0],t[1])})});
    const f=EST.frentes.find(x=>x.id===fid);if(f&&f.mapa_sem&&SEM===0)(f.mapa_sem.filas||[]).filter(r=>!filt||filt(r.capa)).forEach(r=>r.tramos.filter(t=>t[2]!=='antes').forEach(t=>{seg(act,t[0],t[1],'sem',col,'<b>'+mesc(r.capa)+'</b>Ejecutado '+mesc(t[2])+'<br>km '+km(t[0])+' → '+km(t[1])+' <small>('+fmt(Math.abs(t[1]-t[0]))+' m)</small>');B.push(t[0],t[1])}))}
  function drawV(fit){if(!MAPI)return;LY.clearLayers();ls.textContent='';const B=[],R=[];
    if(MSEL.has('base'))drawCapa('base',capa('Base'),'base',null,B,R);
    if(MSEL.has('imp'))drawCapa('imp',capa('Imprim'),'imprimacion',null,B,R);
    if(MSEL.has('mp1'))drawCapa('mp1',capa('Micropavimento 1ra'),'micro',n=>/1ra/.test(n),B,R);
    if(MSEL.has('mp2'))drawCapa('mp2',capa('Micropavimento 2da'),'micro',n=>/2da/.test(n),B,R);
    if(MSEL.has('corte')){const col=MACT.corte[1],f=EST.frentes.find(x=>x.id==='corte');(f&&f.zonas||[]).forEach(z=>{const e=String(z.estado||'').toUpperCase(),st=e.startsWith('TERM')?'hecho':e.includes('PROCESO')?'lado':'pend';
        seg('corte',z.desde,z.hasta,st,st==='pend'?MST.bad:col,'<b>'+mesc(z.zona)+' · '+mesc(z.trabajo)+'</b>km '+km(z.desde)+' → '+km(z.hasta)+' · '+mesc(z.lado||'')+'<br>'+mesc(z.estado)+(z.falta!=null?' · falta '+fmt(z.falta)+' m³':'')+(z.nota?'<br><small>'+mesc(z.nota)+'</small>':''));if(st!=='hecho')B.push(z.desde,z.hasta)});
      (capa('Corte')||{tramos:[]}).tramos.filter(t=>t[2]==='semana').forEach(t=>{seg('corte',t[0],t[1],'prog',col,'<b>Corte · programado '+mesc(SEMN())+'</b>km '+km(t[0])+' → '+km(t[1]));R.push({act:'corte',t:'programado',a:Math.min(t[0],t[1]),b:Math.max(t[0],t[1])})})}
    if(MSEL.has('cun')){const col=MACT.cun[1],f=EST.frentes.find(x=>x.id==='cunetas');(f&&f.cu_lista||[]).forEach(t=>{const e=String(t.estado).toUpperCase(),st=e.startsWith('TERM')?'hecho':e.includes('PROCESO')?'lado':'pend',pf=e.startsWith('TERM')?0:(t.panos_falta||0);
        seg('cun',t.desde,t.hasta,st,st==='pend'?'#9ca3af':col,'<b>Cuneta '+mesc(t.id)+' · '+mesc(t.lado||'')+'</b>km '+km(t.desde)+' → '+km(t.hasta)+'<br>Hecho '+fmt(t.hecho||0)+' de '+fmt(t.largo||0)+' m · faltan '+fmt(t.falta||0)+' m'+(t.panos!=null?' ('+fmt(pf)+' paños)':''));if(st==='lado')B.push(t.desde,t.hasta)})}
    if(MSEL.has('alc')){const f=EST.frentes.find(x=>x.id==='alcantarillas');(f&&f.oa_lista||[]).forEach(o=>{if(o.km==null)return;const EL=['ent','sal','emb','dis'],NM={ent:'Cabezal entrada',sal:'Cabezal salida',emb:'Emboquillado',dis:'Disipador'};
        const falta=EL.filter(k=>o[k]===0),todo=!falta.length&&EL.some(k=>o[k]===1),e=String(o.estado||'').toUpperCase(),col=todo?MST.ok:(o.ent!==0&&o.sal!==0)?MST.mid:e.includes('PROCESO')?MST.run:MST.bad;
        const ll=kLL(o.km);const m=L.circleMarker(ll,{radius:8,color:MACT.alc[1],weight:3,fillColor:col,fillOpacity:1});
        m.bindPopup('<div class="mp-pop"><b>'+mesc(o.cod)+'</b><small>'+mesc(o.tipo)+'</small><br>'+EL.filter(k=>o[k]!=null).map(k=>(o[k]===1?'✓ ':'○ ')+NM[k]).join('<br>')+'<br><small>'+mesc(o.estado)+(o.proy?' · proy. '+fdm(D(o.proy)):'')+'</small><br>'+gmap(ll)+'</div>');LY.addLayer(m);if(!todo)B.push(o.km)})}
    if(MSEL.has('mur')){const f=EST.frentes.find(x=>x.id==='muros');(f&&f.muros_lista||[]).forEach(o=>{if(o.desde==null)return;const e=String(o.estado||'').toUpperCase(),col=e.startsWith('TERM')?MST.ok:e.includes('PROCESO')?MST.mid:MST.bad;
        const ll=kOff((o.desde+(o.hasta||o.desde))/2,o.lado,12);const m=L.marker(ll,{icon:L.divIcon({className:'mp-mu',html:'<span style="background:'+col+'"></span>',iconSize:null}),title:o.cod});
        m.bindPopup('<div class="mp-pop"><b>'+mesc(o.cod)+'</b><small>'+mesc(o.lado||'')+' · '+fmt(o.largo||0)+' m × '+fmt(o.alto||0,1)+' m</small><br>Bolsas '+fmt(o.hechas||0)+' de '+fmt(o.meta||0)+'<br><small>'+mesc(o.estado)+'</small><br>'+gmap(ll)+'</div>');LY.addLayer(m);if(!e.startsWith('TERM'))B.push(o.desde)})}
    const H=frHoy();
    if(MSEL.has('hoy')){H.forEach(h=>{h.rs.forEach(r=>{const P=offPts(kSeg(r[0],r[1]),lanePx(h.act)*mpp());LY.addLayer(L.polyline(P,{color:'#111621',weight:14,opacity:.85,interactive:false}));
          const l=L.polyline(P,{color:h.c,weight:9,opacity:1});l.bindPopup('<div class="mp-pop"><b>'+mesc(h.nom)+' · '+fdm(D(h.f))+'</b>'+h.txt.map(mesc).join('<br>')+'</div>');LY.addLayer(l)});
        LY.addLayer(L.marker(kLL((h.a+h.b)/2),{icon:L.divIcon({className:'mp-fr',html:'<span style="background:'+h.c+'">'+mesc(h.nom)+'</span>',iconSize:null}),interactive:false}));B.push(h.a,h.b);
        const bt=el('button');bt.style.setProperty('--c',h.c);bt.append(el('b',null,h.nom),el('small',null,fdm(D(h.f))+' · km '+km(h.a)+' → '+km(h.b)));bt.onclick=()=>{zfit(h.a-150,h.b+150,17);MAPI.getContainer().scrollIntoView({behavior:'smooth',block:'center'})};ls.append(bt)});
      H.forEach(h=>R.push({act:h.act,t:'hoy',a:h.a,b:h.b,nom:h.nom}))}
    if(fit){if(B.length)zfit(Math.min(...B)-300,Math.max(...B)+300);else MAPI.fitBounds(L.latLngBounds(EJE.p),{padding:[20,20]})}
    kms();legend();cruces(R)}
  function cruces(R){ix.textContent='';const lb=x=>(x.nom||MACT[x.act][0])+' '+(x.t==='hoy'?'hoy':'programado');
    if(R.length<2){if(MSEL.size>1)ix.append(el('p',null,'Elige "Frentes de hoy" o actividades con programación para ver si se cruzan.'));return}
    const O=[];for(let i=0;i<R.length;i++)for(let j=i+1;j<R.length;j++){const x=R[i],y=R[j];if(x.act===y.act)continue;const g=Math.max(x.a,y.a)-Math.min(x.b,y.b);if(g<=500)O.push({x,y,g})}
    O.sort((p,q)=>p.g-q.g);ix.append(el('h3',null,O.length?'Frentes que se cruzan o están a menos de 500 m':'Sin cruces: ningún frente elegido está a menos de 500 m de otro'));
    O.slice(0,12).forEach(o=>{const bt=el('button',o.g<0?'x':'c');bt.append(el('b',null,o.g<0?'se cruzan '+fmt(-o.g)+' m':'a '+fmt(o.g)+' m'),el('span',null,lb(o.x)+' km '+km(o.x.a)+' → '+km(o.x.b)+'  ·  '+lb(o.y)+' km '+km(o.y.a)+' → '+km(o.y.b)));
      bt.onclick=()=>{zfit(Math.min(o.x.a,o.y.a)-200,Math.max(o.x.b,o.y.b)+200,17);MAPI.getContainer().scrollIntoView({behavior:'smooth',block:'center'})};ix.append(bt)})}
  function legend(){lg.textContent='';const sw=(col,sty)=>{const s=STY[sty]||{};return '<svg width="26" height="10"><line x1="1" y1="5" x2="25" y2="5" style="stroke:'+col+'" stroke-width="'+Math.min(s.weight||5,8)+'"'+(s.dashArray?' stroke-dasharray="'+s.dashArray+'"':'')+(s.lineCap==='round'?' stroke-linecap="round"':'')+'/></svg>'};
    const it=(h,t)=>{const s=el('span');s.innerHTML=h;s.append(document.createTextNode(t));lg.append(s)};
    const sel=Object.keys(MACT).filter(k=>MSEL.has(k));sel.forEach(k=>it('<b class="'+(k==='mur'?'mp-sq':'mp-dot')+'" style="background:'+MACT[k][1]+'"></b>',MACT[k][0]));
    if(MSEL.has('hoy'))it(sw('#111621','sem'),'Frentes de hoy');
    if(sel.some(k=>MLANE.includes(k))){it(sw('var(--ink)','hecho'),'hecho');it(sw('var(--ink)','lado'),'un solo lado / en proceso');it(sw('var(--ink)','sem'),'ejecutado esta semana');it(sw('var(--ink)','prog'),'programado '+SEMN());it(sw(MST.bad,'pend'),'pendiente')}
    if(MSEL.has('alc')||MSEL.has('mur')){it('<b class="mp-dot" style="background:'+MST.ok+'"></b>','completa');it('<b class="mp-dot" style="background:'+MST.mid+'"></b>','falta poco');it('<b class="mp-dot" style="background:'+MST.bad+'"></b>','atrasada')}
    if(lanes().length>1)it('','  · cada frente va en su propio carril al lado del eje');
    Object.entries(MPT).filter(([k])=>(EST.puntos||[]).some(p=>p.tipo===k)).forEach(([k,[a,c]])=>it('<b class="mp-dot" style="background:'+c+'"></b>',k))}
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
    if '/*mapa-v2*/' not in h:
        if '/*mapa-v1*/' in h:     # versión anterior (un frente a la vez): se reemplaza entera
            i = h.index('/*mapa-v1*/')
            j = h.index('function alertsCard(){', i)
            h = h[:i] + h[j:]
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
    # 27/11: Crhistian pidió quitar los dos puntos de descarga que venían precargados (solo esos dos nombres)
    QUITAR = {'Descarga de cemento · Pte. Vicuñitas', 'Descarga de imprimación'}
    try:
        import openpyxl
        wb = openpyxl.load_workbook(pm)
        ws = wb.worksheets[0]
        n = 0
        for r in range(5, ws.max_row + 1):
            if str(ws.cell(r, 3).value or '').strip() in QUITAR:
                for c in range(2, 9):
                    ws.cell(r, c).value = None
                n += 1
        if n:
            wb.save(pm)
            msg.append(f'PUNTOS_MAPA.xlsx (-{n} descargas)')
    except Exception:
        pass
    return msg


if __name__ == '__main__':
    import sys
    p = sys.argv[1]
    h = patch_html(open(p, encoding='utf8').read())
    open(p, 'w', encoding='utf8').write(h)
    print('ok')
