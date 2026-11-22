"""Parche 22/11 (c) — Corte XV, 'Zonas de corte, roca fija y mejoramiento de subrasante':
 - franja y línea ámbar 'Último parte' = dónde estamos (sale de los partes del día: zona y km);
 - zonas terminadas con ✓ y zonas en proceso con borde ámbar y su %;
 - botón 'Vista panorámica': pantalla completa, más ancho (zoom 100–400 %), nombres de las filas fijos a la izquierda
   y se abre centrado en dónde estamos."""

NEW = r"""function corteSvg(f,W,o){
  o=o||{};const zs=f.zonas;
  const iv=[...zs].map(z=>[Math.min(z.desde,z.hasta),Math.max(z.desde,z.hasta)]).sort((a,b)=>a[0]-b[0]);const mg=[];iv.forEach(([a,b])=>{if(mg.length&&a<=mg[mg.length-1][1]+60)mg[mg.length-1][1]=Math.max(mg[mg.length-1][1],b);else mg.push([a,b])});
  const GAP=160,pad=40;const segs=[];let acc=0;mg.forEach(([a,b],i)=>{if(i)acc+=GAP;segs.push({a:a-pad,b:b+pad,o:acc});acc+=(b-a)+2*pad});const TOT=acc;
  const L=o.L!=null?o.L:176,R=16,rh=64,rows=[['Corte de talud (ensanche)','T'],['Roca fija (voladura)','RF'],['Mejoramiento subrasante','MSR']],top=60,H=top+rows.length*rh+40;
  const x=m=>{let s=segs.find(q=>m>=q.a&&m<=q.b)||segs.reduce((p,q)=>Math.abs(q.a-m)<Math.abs(p.a-m)?q:p);return L+(s.o+(Math.min(Math.max(m,s.a),s.b)-s.a))/TOT*(W-L-R)};
  const s=sv('svg',{viewBox:`0 0 ${W} ${H}`,class:'lin',role:'img','aria-label':'Zonas del Sector XV'});
  segs.forEach((q,i)=>{const x0=x(q.a),x1=x(q.b);s.append(sv('rect',{x:x0,y:top-10,width:x1-x0,height:rows.length*rh+8,fill:i%2?'var(--band)':'transparent'}));
    s.append(sv('text',{x:x0+2,y:H-20,class:'km'},km(q.a+pad)));if(x1-x0>110)s.append(sv('text',{x:x1-2,y:H-20,'text-anchor':'end',class:'km'},km(q.b-pad)));
    if(i){const gx=x0-(GAP/TOT*(W-L-R))/2;s.append(sv('text',{x:gx,y:top+rows.length*rh/2,'text-anchor':'middle','dominant-baseline':'middle',class:'gapl'},'≈'))}});
  s.append(sv('text',{x:L,y:H-4,class:'km'},'escala comprimida: solo las zonas de trabajo; ≈ = tramo sin corte'));
  // dónde estamos: zona y km del último parte
  const dd=(EST.dia_det||{})[f.id]||{};const dk=Object.keys(dd).sort().pop();let here=null;
  if(dk){let a=null,b=null;const zn=[];(dd[dk]||[]).forEach(t=>{const m=String(t).match(/(T-\d+|MSR-\d+)\s*·\s*km\s*(\d+)\+(\d+)(?:\s*→\s*(\d+)\+(\d+))?/);if(!m)return;
    const p=(+m[2])*1000+(+m[3]),q=m[4]?(+m[4])*1000+(+m[5]):p;if(!zn.includes(m[1]))zn.push(m[1]);a=a==null?Math.min(p,q):Math.min(a,p,q);b=b==null?Math.max(p,q):Math.max(b,p,q)});
    if(a!=null)here={a,b,zn,dk}}
  if(here){const xa=x(here.a),xb=Math.max(x(here.b),xa+4);
    s.append(sv('rect',{x:xa,y:top-14,width:xb-xa,height:rows.length*rh+10,fill:'var(--amber)',opacity:.16}));
    s.append(sv('line',{x1:xb,x2:xb,y1:top-24,y2:top+rows.length*rh-4,stroke:'var(--amber)','stroke-width':2,'stroke-dasharray':'5 4',class:'hereln'}));
    const lb='Último parte '+fd(here.dk).slice(0,5)+' · '+here.zn.join(', ')+' · km '+km(here.a)+(here.b>here.a?' → '+km(here.b):'');const rt=xb>W*0.6;
    s.append(sv('text',{x:rt?xb-6:xb+6,y:top-30,'text-anchor':rt?'end':'start',class:'here'},'▼ '+lb))}
  rows.forEach(([lab,key],i)=>{const y=top+i*rh+18,bh=24;
    if(!o.nolab)s.append(sv('text',{x:0,y:y+bh/2,class:'lbl','dominant-baseline':'middle'},lab));
    segs.forEach(q=>s.append(sv('rect',{x:x(q.a),y,width:x(q.b)-x(q.a),height:bh,fill:'var(--track)',rx:2})));
    zs.forEach(z=>{const isT=String(z.zona).startsWith('T-'),isM=String(z.zona).startsWith('MSR');
      if(key==='T'&&!isT)return;if(key==='MSR'&&!isM)return;if(key==='RF'&&!(z.rf>0))return;
      const st=(z.pct>=1||/termin/i.test(z.estado||''))?'ok':(z.pct>0||/proceso/i.test(z.estado||''))?'run':'';
      const a=x(Math.min(z.desde,z.hasta)),w=Math.max(6,x(Math.max(z.desde,z.hasta))-a);const base={T:'var(--seg-pend)',RF:'var(--seg-roca)',MSR:'var(--d5)'}[key];
      const g=sv('rect',{x:a,y,width:w,height:bh,fill:base,stroke:'var(--panel)','stroke-width':1});g.append(sv('title',null,`${z.zona} · ${z.trabajo}: km ${km(z.desde)} → ${km(z.hasta)} · ${key==='RF'?fmt(z.rf)+' m³ R.F.':fmt(z.corte+(z.mej||0))+' m³'} · ${Math.round(z.pct*100)} % · ${z.estado||''}`));s.append(g);
      if(key!=='RF'&&z.pct>0)s.append(sv('rect',{x:a,y,width:w*Math.min(1,z.pct),height:bh,fill:'var(--seg-hecho)'}));
      if(st==='run')s.append(sv('rect',{x:a-2,y:y-2,width:w+4,height:bh+4,fill:'none',stroke:'var(--amber)','stroke-width':2.5,rx:3}));
      const t=key==='RF'?fmt(z.rf)+' m³':z.zona+(st==='ok'?' ✓':'');
      const sub=key==='RF'?'':st==='ok'?'terminado':st==='run'?(Math.round(z.pct*100)+' %'+(key==='T'&&w>90?' · falta '+fmt(z.falta)+' m³':'')):key==='T'?fmt(z.falta)+' m³':fmt(z.corte+(z.mej||0))+' m³';
      if(w>44){s.append(sv('text',{x:a+w/2,y:y+bh/2+1,'text-anchor':'middle','dominant-baseline':'middle',class:key==='T'?'zin2':'zin'},t))}else s.append(sv('text',{x:a+w/2,y:y-6,'text-anchor':'middle',class:'zl'},t));
      if(sub&&(w>44||st))s.append(sv('text',{x:a+w/2,y:y+bh+12,'text-anchor':'middle',class:'zs'+(st==='run'?' zrun':st==='ok'?' zok':'')},sub))})});
  return s;
}
function zoomCorte(f){
  const ov=el('div','zov');ov.setAttribute('role','dialog');ov.setAttribute('aria-label','Zonas de corte · vista panorámica');
  const bar=el('div','zbar');bar.append(el('b',null,'Zonas de corte · Sector XV · vista panorámica'));
  let z=2;const box=el('div','zbox');box.style.cssText='display:flex;align-items:center';
  const draw=keep=>{const sl=box.scrollWidth?box.scrollLeft/box.scrollWidth:0;box.textContent='';const W=Math.round(1100*z);
    const k=Math.max(1,Math.min(1.5,(box.clientHeight-30)/292));
    const wr=el('div','cpw');const lc=el('div','cpl');[['Corte de talud (ensanche)',90],['Roca fija (voladura)',154],['Mejoramiento subrasante',218]].forEach(([t,y])=>{const d=el('div',null,t);d.style.top=(y*k-10)+'px';lc.append(d)});
    const s=corteSvg(f,W,{L:20,nolab:true});s.style.width=(W*k)+'px';s.style.maxWidth='none';s.style.flex='none';wr.append(lc,s);box.append(wr);zl.textContent=Math.round(z*100)+' %';
    if(keep)box.scrollLeft=sl*box.scrollWidth;else{const hl=s.querySelector('.hereln');if(hl)box.scrollLeft=Math.max(0,190+(+hl.getAttribute('x1'))*k-box.clientWidth/2)}};
  const hb=el('button','zb','▼ Ir a dónde estamos');hb.onclick=()=>draw(false);
  const zm=el('button','zb','−');zm.setAttribute('aria-label','Alejar');zm.onclick=()=>{z=Math.max(1,z-0.5);draw(true)};
  const zl=el('span','mono','200 %');const zp=el('button','zb','+');zp.setAttribute('aria-label','Acercar');zp.onclick=()=>{z=Math.min(4,z+0.5);draw(true)};
  const cl=el('button','zb zx','✕ Cerrar');const esc=e=>{if(e.key==='Escape')close()};const close=()=>{ov.remove();document.removeEventListener('keydown',esc)};cl.onclick=close;document.addEventListener('keydown',esc);
  bar.append(hb,zm,zl,zp,cl);const lg=el('div','zleg');lg.append(corteLegend());ov.append(bar,lg,box);document.body.append(ov);draw(false);cl.focus();
}
function corteLegend(){const lg=el('div','legend');[['var(--seg-hecho)','Cortado'],['var(--seg-pend)','Corte pendiente'],['var(--seg-roca)','Roca fija (voladura)'],['var(--d5)','Mejoramiento de subrasante']].forEach(([cc,t])=>{const s=el('span');const i=el('i');i.style.background=cc;s.append(i,document.createTextNode(t));lg.append(s)});
  const s1=el('span');const i1=el('i');i1.style.cssText='background:none;outline:2.5px solid var(--amber);outline-offset:-2px';s1.append(i1,document.createTextNode('En proceso'));
  const s2=el('span');const i2=el('i');i2.style.cssText='background:var(--amber);opacity:.5';s2.append(i2,document.createTextNode('Último parte (dónde estamos)'));lg.append(s1,s2);return lg}
function corteCard(f){
  const zs=f.zonas;const lg=corteLegend();
  const c=card('Sector XV · km 284+000 – 294+495','Zonas de corte, roca fija y mejoramiento de subrasante',lg);
  const zb=el('button','zbtn','⤢ Vista panorámica');zb.title='Ver las zonas en pantalla completa, más de cerca';zb.onclick=()=>zoomCorte(f);c.querySelector('.card-h').append(zb);
  const s=corteSvg(f,1100);
  const sc=el('div','scroll');sc.append(s);const bd=el('div','card-b');bd.append(sc);c.append(bd);
"""

CSS = "(function(){const s=document.createElement('style');s.textContent=\".lin .here{font:700 11.5px var(--f-ui,inherit);fill:var(--amber)}.lin .zs.zrun{fill:var(--amber);font-weight:700}.lin .zs.zok{fill:var(--ok);font-weight:700}.cpw{display:flex;position:relative;width:max-content}.cpl{position:sticky;left:0;z-index:2;width:190px;flex:none;background:var(--bg,#fff);border-right:1px solid var(--line2)}.cpl div{position:absolute;left:12px;font-size:14px;font-weight:600;color:var(--ink)}.cpw{flex:none;margin:auto 0}.zleg{padding:8px 16px;border-bottom:1px solid var(--line2)}\";document.head.append(s)})();\n"


def old_block(h):
    i = h.index('function corteCard(f){')
    j = h.index("  const s2=el('div','scroll');const t=el('table','ft');", i)
    return i, j


def patch_html(h):
    if 'function corteSvg(' in h:
        return h
    i, j = old_block(h)
    return h[:i] + CSS + NEW + h[j:]


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
