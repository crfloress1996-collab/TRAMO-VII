"""Parche 18/11 (b) — Planta: el gráfico diario pasa a barras HORIZONTALES (un renglón por día, ingreso / producción / despacho)
y a la derecha el ACUMULADO de la semana. Uso: patch_planta_h_1811.py <tablero.html o index.html>"""
import sys
FN = r"""function prodHChart(ss,P){
  const dd=ss[0].dias,W=980,L=92,CW=560,RX=L+CW+70,RW=W-RX-14,bh=11,gap=3,n=ss.length,rh=n*(bh+gap)+16,T=30,H=T+dd.length*rh+30;
  const meta=(ss.find(x=>x.meta)||{}).meta||0,mx=Math.max(1,meta*1.15,...ss.flatMap(x=>x.dias.map(d=>d.v||0)));
  const step=Math.pow(10,Math.floor(Math.log10(mx)));const nice=[1,2,2.5,5,10].map(m=>m*step).find(v=>mx/v<=5)||step*10;const top=Math.ceil(mx/nice)*nice;
  const x=v=>L+CW*v/top,NEU=['var(--navy-s)','var(--line)'];let ni=0;const col=ss.map(z=>z.color||(z.meta?null:NEU[(ni++)%2]));
  const s=sv('svg',{viewBox:`0 0 ${W} ${H}`,class:'wk',role:'img','aria-label':'Producción por día (barras horizontales) y acumulado de la semana'});s.style.maxWidth='100%';
  s.append(sv('text',{x:L,y:14,class:'sb'},'Por día (m³)'));
  for(let v=0;v<=top+1e-9;v+=nice){s.append(sv('line',{x1:x(v),x2:x(v),y1:T-6,y2:H-26,stroke:'var(--line2)'}));s.append(sv('text',{x:x(v),y:H-10,'text-anchor':'middle'},fmt(v)))}
  dd.forEach((d,i)=>{const y0=T+i*rh;if(i%2===0)s.append(sv('rect',{x:0,y:y0-4,width:L+CW+60,height:rh,fill:'var(--band)'}));
    s.append(sv('text',{x:8,y:y0+rh/2-2,'dominant-baseline':'middle',class:'sb'},d.dia+' '+fdm(D(d.fecha))));
    const anyEf=ss.some(z=>z.dias[i].ef);
    if(d.futuro||!anyEf){s.append(sv('text',{x:L+6,y:y0+rh/2-2,'dominant-baseline':'middle',class:'fut'},d.futuro?'por reportar':'sin parte'));return}
    ss.forEach((z,j)=>{const v=z.dias[i].v||0,yy=y0+j*(bh+gap);
      const fill=z.meta?(v>=z.meta?'var(--ok)':v>=.8*z.meta?'var(--warn)':'var(--bad)'):col[j];
      const r=sv('rect',{x:L,y:yy,width:Math.max(v?2:0,x(v)-L),height:bh,fill,rx:2});r.append(sv('title',null,`${z.nombre} · ${d.dia}: ${fmt(v)} ${z.und}`));s.append(r);
      if(v)s.append(sv('text',{x:x(v)+5,y:yy+bh/2+1,'dominant-baseline':'middle',class:'vv'},fmt(v)))})});
  if(meta){s.append(sv('line',{x1:x(meta),x2:x(meta),y1:T-10,y2:H-26,class:'meta'}));s.append(sv('text',{x:x(meta)+4,y:T-12,class:'mt'},'meta '+fmt(meta)+'/día'))}
  // acumulado de la semana (derecha)
  s.append(sv('line',{x1:RX-24,x2:RX-24,y1:4,y2:H-6,stroke:'var(--line)'}));
  s.append(sv('text',{x:RX,y:14,class:'sb'},'Acumulado de la semana'));
  const nh=(EST.prod&&EST.prod.nhab)||6,tots=ss.map(z=>z.dias.reduce((q,d)=>q+(d.futuro?0:(d.v||0)),0)),ms=meta?meta*nh:0,tmx=Math.max(1,ms,...tots);
  ss.forEach((z,j)=>{const t=tots[j],yy=T+12+j*86,w=RW*t/tmx,p=z.meta&&ms?t/ms:null;
    s.append(sv('text',{x:RX,y:yy,class:'sb'},z.nombre));
    s.append(sv('rect',{x:RX,y:yy+8,width:RW,height:18,rx:3,fill:'var(--track)'}));
    const fill=z.meta?(p>=1?'var(--ok)':p>=.8?'var(--warn)':'var(--bad)'):col[j];
    s.append(sv('rect',{x:RX,y:yy+8,width:Math.max(t?2:0,w),height:18,rx:3,fill}));
    const tv=sv('text',{x:RX+RW,y:yy+44,'text-anchor':'end',class:'vv tot'},fmt(t)+' '+z.und);s.append(tv);
    if(z.meta&&ms){s.append(sv('line',{x1:RX+RW*ms/tmx,x2:RX+RW*ms/tmx,y1:yy+4,y2:yy+30,class:'meta'}));
      s.append(sv('text',{x:RX,y:yy+58,class:'mt'},'meta a la fecha '+fmt(ms)+' ('+nh+(nh===1?' día':' días')+') · '+Math.round(p*100)+' %'))}});
  return s;
}
"""
OLD_CALL = "const sc=el('div','scroll');sc.append(prodChart(ss,P));"
NEW_CALL = "const sc=el('div','scroll');sc.append(f.id==='planta'&&ss.length>1?prodHChart(ss,P):prodChart(ss,P));"


def patch(h):
    if 'function prodHChart' not in h:
        assert h.count('function prodChart(ss,P){') == 1
        h = h.replace('function prodChart(ss,P){', FN + 'function prodChart(ss,P){', 1)
    if NEW_CALL not in h:
        assert h.count(OLD_CALL) == 1
        h = h.replace(OLD_CALL, NEW_CALL, 1)
    return h


def aplicar(motor):
    from pathlib import Path
    f = Path(motor) / 'tablero.html'
    a = f.read_text(encoding='utf8')
    b = patch(a)
    if b != a:
        f.write_text(b, encoding='utf8')
        return ['tablero.html']
    return []


if __name__ == '__main__':
    p = sys.argv[1]
    h = patch(open(p, encoding='utf8').read())
    open(p, 'w', encoding='utf8').write(h)
    print('ok')
