import json, html as H
rows=json.load(open('rows.json'))
c=lambda s:sum(1 for r in rows if r['st']==s)
tot=len(rows); ontime=c('정시'); late=c('지연'); vac=c('휴가'); miss=c('누락'); norec=c('기록없음')
done=ontime+late; base=tot-vac
times=[r['min'] for r in rows if r['min']]
avg=sum(times)/len(times); mn=min(times); mx=max(times)
fm=lambda v:'%02d:%02d'%(int(v)//60,int(v)%60)
STY={'정시':('ok','정시 확정'),'지연':('late','09시 이후'),'휴가':('vac','휴가'),'누락':('miss','확정 없음'),'기록없음':('none','기록 없음')}
tr=[]
for r in rows:
    cls,lab=STY[r['st']]
    t=r['time'] if r['time'] else '<span class="empty">비어있음</span>'
    bar=''
    if r['min']:
        left=(r['min']-6*60)/(11.5*60-6*60)*100
        bar='<span class="dot %s" style="left:%.2f%%"></span>'%(cls,left)
    tr.append('<tr data-st="%s"><td class="dt">%s</td><td class="wd %s">%s</td><td class="tm">%s</td>'
              '<td><span class="chip %s">%s</span></td><td class="track">%s</td><td class="note">%s</td></tr>'
              %(r['st'],r['date'],'sat' if r['w']=='토' else '',r['w'],t,cls,lab,bar,H.escape(r['note'])))
tbody='\n'.join(tr)
mon={}
for r in rows:
    m=r['date'][:2]; d=mon.setdefault(m,{'정시':0,'지연':0,'휴가':0,'누락':0,'기록없음':0}); d[r['st']]+=1
monrows=''.join('<tr><td>%s월</td><td>%d</td><td>%d</td><td>%d</td><td>%d</td><td>%d</td></tr>'%(int(m),v['정시'],v['지연'],v['누락'],v['기록없음'],v['휴가']) for m,v in sorted(mon.items()))

tpl = """<!DOCTYPE html>
<html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>계획 확정 시각 점검 (2026.07.13 ~ 09.14)</title>
<style>
:root{--accent:#0066cc;--canvas:#fff;--parch:#f5f5f7;--ink:#1d1d1f;--muted:#7a7a7a;--hair:#e0e0e0;
--ok:#0066cc;--late:#c2410c;--miss:#ff4d4f;--none:#b0b0b5;--vac:#9aa0a6;}
*{box-sizing:border-box}
body{margin:0;background:var(--parch);color:var(--ink);
font-family:-apple-system,BlinkMacSystemFont,"SF Pro Text","Apple SD Gothic Neo",Inter,system-ui,sans-serif;
font-size:17px;line-height:1.47;letter-spacing:-0.374px;-webkit-font-smoothing:antialiased}
.wrap{max-width:1080px;margin:0 auto;padding:48px 24px 80px}
header{margin-bottom:32px}
h1{font-size:40px;font-weight:600;letter-spacing:-0.8px;margin:0 0 8px}
.sub{color:var(--muted);font-size:17px;margin:0}
.kpis{display:grid;grid-template-columns:repeat(4,1fr);gap:16px;margin:32px 0}
.kpi{background:var(--canvas);border:1px solid var(--hair);border-radius:18px;padding:24px}
.kpi .n{font-size:36px;font-weight:600;letter-spacing:-0.8px;line-height:1.1}
.kpi .l{font-size:14px;color:var(--muted);margin-top:6px}
.kpi.late .n{color:var(--late)} .kpi.miss .n{color:var(--miss)}
.panel{background:var(--canvas);border:1px solid var(--hair);border-radius:18px;padding:24px;margin-bottom:24px}
h2{font-size:22px;font-weight:600;letter-spacing:-0.4px;margin:0 0 4px}
.hint{color:var(--muted);font-size:14px;margin:0 0 16px}
.controls{display:flex;gap:8px;flex-wrap:wrap;margin-bottom:16px}
button{font:inherit;font-size:14px;border:1px solid rgba(0,0,0,.12);background:var(--canvas);color:var(--ink);
border-radius:9999px;padding:8px 16px;cursor:pointer;letter-spacing:-0.1px}
button:hover{background:var(--parch)} button.on{background:var(--ink);color:#fff;border-color:var(--ink)}
button:active{transform:scale(.96)} button:focus-visible{outline:2px solid #0071e3}
table{width:100%;border-collapse:collapse;font-size:15px}
th{text-align:left;font-weight:600;font-size:13px;color:var(--muted);padding:10px 8px;
border-bottom:1px solid var(--hair);position:sticky;top:0;background:var(--canvas);z-index:2}
td{padding:9px 8px;border-bottom:1px solid #f0f0f2;vertical-align:middle}
.scroll{max-height:640px;overflow:auto;border-radius:12px}
.dt{font-variant-numeric:tabular-nums;font-weight:600;white-space:nowrap}
.wd{color:var(--muted);width:36px} .wd.sat{color:var(--accent)}
.tm{font-variant-numeric:tabular-nums;font-weight:600;white-space:nowrap;width:72px}
.empty{color:var(--miss);font-weight:400;font-size:13px}
.chip{display:inline-block;border-radius:9999px;padding:3px 11px;font-size:12px;white-space:nowrap;
border:1px solid transparent}
.chip.ok{background:rgba(0,102,204,.10);color:var(--ok)}
.chip.late{background:rgba(194,65,12,.10);color:var(--late)}
.chip.miss{background:rgba(255,77,79,.12);color:var(--miss)}
.chip.none{background:#f2f2f4;color:var(--none)}
.chip.vac{background:#f2f2f4;color:var(--vac)}
.track{position:relative;min-width:200px;height:20px}
.track:before{content:"";position:absolute;left:0;right:0;top:9px;height:1px;background:#ececed}
.dot{position:absolute;top:5px;width:10px;height:10px;border-radius:50%;margin-left:-5px}
.dot.ok{background:var(--ok)} .dot.late{background:var(--late)}
.note{color:var(--muted);font-size:13px}
.axis{display:flex;justify-content:space-between;font-size:11px;color:var(--muted);
margin:4px 0 0;padding-left:calc(36px + 72px + 110px + 32px)}
.sum{font-size:15px}
.sum td,.sum th{padding:8px}
footer{color:var(--muted);font-size:13px;margin-top:32px;text-align:center}
.legend{display:flex;gap:16px;flex-wrap:wrap;font-size:13px;color:var(--muted);margin-top:12px}
.legend span{display:flex;align-items:center;gap:6px}
.legend i{width:9px;height:9px;border-radius:50%;display:inline-block}
@media(max-width:820px){.kpis{grid-template-columns:repeat(2,1fr)}.track,.axis{display:none}h1{font-size:30px}}
@media print{body{background:#fff}.controls{display:none}.scroll{max-height:none}.wrap{padding:0}
.panel,.kpi{border:1px solid #ddd}}
</style></head><body><div class="wrap">
<header>
<h1>계획 확정 시각 점검</h1>
<p class="sub">생산실적방 · 다스 신민섭매니저 &ldquo;계획 확정했습니다&rdquo; 기준 &middot; 2026.07.13 ~ 09.14 (일요일 제외, __TOT__일)</p>
</header>

<div class="kpis">
<div class="kpi"><div class="n">__DONE__ / __BASE__</div><div class="l">확정 기록 확인 (휴가 __VAC__일 제외)</div></div>
<div class="kpi"><div class="n">__AVG__</div><div class="l">평균 확정 시각 · 최초 __MN__ / 최종 __MX__</div></div>
<div class="kpi late"><div class="n">__LATE__</div><div class="l">09시 이후 확정</div></div>
<div class="kpi miss"><div class="n">__MISS__</div><div class="l">대화는 있으나 확정 멘트 없음 (08/13)</div></div>
</div>

<div class="panel">
<h2>일자별 확정 시각</h2>
<p class="hint">점은 06:00~11:30 구간에서의 확정 시각 위치입니다. 휴가·기록 없음 일자는 비어있음으로 표시했습니다.</p>
<div class="controls">
<button class="on" data-f="all">전체</button>
<button data-f="정시">정시 확정</button>
<button data-f="지연">09시 이후</button>
<button data-f="empty">비어있는 날</button>
</div>
<div class="scroll"><table>
<thead><tr><th>날짜</th><th>요일</th><th>확정 시각</th><th>상태</th><th>06:00 &mdash; 11:30</th><th>비고</th></tr></thead>
<tbody id="tb">
__TBODY__
</tbody></table></div>
<div class="legend">
<span><i style="background:var(--ok)"></i>09:00 이전 확정</span>
<span><i style="background:var(--late)"></i>09:00 이후 확정</span>
<span><i style="background:var(--none)"></i>기록 없음 / 휴가</span>
</div>
</div>

<div class="panel">
<h2>월별 요약</h2>
<p class="hint">일요일을 제외한 영업일 기준입니다.</p>
<table class="sum"><thead><tr><th>구분</th><th>정시 확정</th><th>09시 이후</th><th>확정 없음</th><th>기록 없음</th><th>휴가</th></tr></thead>
<tbody>__MON__</tbody></table>
</div>

<footer>KakaoTalk 대화 내보내기 원본 기준 자동 집계 &middot; 데이터는 파일 안에 포함되어 있어 오프라인에서도 그대로 열립니다.</footer>
</div>
<script>
var btns=document.querySelectorAll('[data-f]');
var rowsEl=document.querySelectorAll('#tb tr');
for(var i=0;i<btns.length;i++){
  btns[i].addEventListener('click',function(){
    for(var j=0;j<btns.length;j++){btns[j].classList.remove('on');}
    this.classList.add('on');
    var f=this.getAttribute('data-f');
    for(var k=0;k<rowsEl.length;k++){
      var st=rowsEl[k].getAttribute('data-st');
      var show = f==='all' ? true : (f==='empty' ? (st!=='정시'&&st!=='지연') : st===f);
      rowsEl[k].style.display = show ? '' : 'none';
    }
  });
}
</script>
</body></html>"""
out=(tpl.replace('__TOT__',str(tot)).replace('__DONE__',str(done)).replace('__BASE__',str(base))
 .replace('__VAC__',str(vac)).replace('__AVG__',fm(avg)).replace('__MN__',fm(mn)).replace('__MX__',fm(mx))
 .replace('__LATE__',str(late)).replace('__MISS__',str(miss)).replace('__TBODY__',tbody).replace('__MON__',monrows))
open('report.html','w',encoding='utf-8').write(out)
print(len(out))
