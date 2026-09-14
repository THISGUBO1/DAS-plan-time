import json
rows=json.load(open('rows.json'))
c=lambda s:sum(1 for r in rows if r['st']==s)
ontime,late,vac,miss,norec=c('정시'),c('지연'),c('휴가'),c('누락'),c('기록없음')
times=[r['min'] for r in rows if r['min']]
avg=sum(times)/len(times); fm=lambda v:'%02d:%02d'%(int(v)//60,int(v)%60)
SHORT={'정시':'','지연':'09시 이후','휴가':'휴가','누락':'확정 없음','기록없음':'기록 없음'}
tr=[]
for r in rows:
    lab=SHORT[r['st']]
    if r['time']:
        t='<span class="%s">%s</span>'%('late' if r['st']=='지연' else 'ok', r['time'])
    else:
        t='<span class="none">&mdash;</span>'
    cls=' class="dim"' if r['st'] in ('휴가','기록없음') else (' class="warn"' if r['st']=='누락' else '')
    tr.append('<tr%s><td class="dt">%s</td><td class="wd">%s</td><td class="tm">%s</td><td class="nt">%s</td></tr>'
              %(cls,r['date'],r['w'],t,lab))
tb='\n'.join(tr)
doc="""<!DOCTYPE html>
<html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>계획 확정 시각 (2026.07.13 ~ 09.14)</title>
<style>
:root{--ink:#1d1d1f;--muted:#86868b;--hair:#e8e8ea;--late:#c2410c;--warn:#c62828}
*{box-sizing:border-box}
body{margin:0;background:#fff;color:var(--ink);
font-family:-apple-system,BlinkMacSystemFont,"Apple SD Gothic Neo","Malgun Gothic",system-ui,sans-serif;
font-size:16px;line-height:1.5;letter-spacing:-0.3px;-webkit-font-smoothing:antialiased}
.wrap{max-width:620px;margin:0 auto;padding:64px 24px 80px}
h1{font-size:28px;font-weight:600;letter-spacing:-0.6px;margin:0 0 6px}
.sub{color:var(--muted);font-size:15px;margin:0 0 8px}
.sum{color:var(--muted);font-size:15px;margin:0 0 36px}
.sum b{color:var(--ink);font-weight:600}
table{width:100%;border-collapse:collapse;font-size:16px}
th{text-align:left;font-weight:400;font-size:13px;color:var(--muted);padding:0 0 10px;
border-bottom:1px solid var(--hair)}
td{padding:11px 0;border-bottom:1px solid #f4f4f6}
.dt{font-variant-numeric:tabular-nums;width:76px}
.wd{color:var(--muted);width:40px}
.tm{font-variant-numeric:tabular-nums;width:88px}
.nt{color:var(--muted);font-size:13px;text-align:right}
.late{color:var(--late)} .none{color:#c8c8cc}
tr.dim td{color:#b8b8bd} tr.dim .wd{color:#c8c8cc}
tr.warn .nt{color:var(--warn)}
footer{color:var(--muted);font-size:13px;margin-top:40px}
@media print{.wrap{padding:0}body{font-size:12px}}
</style></head><body><div class="wrap">
<h1>계획 확정 시각</h1>
<p class="sub">생산실적방 &middot; 신민섭매니저 &ldquo;계획 확정했습니다&rdquo; 기준</p>
<p class="sum">2026.07.13 ~ 09.14 &middot; 일요일 제외 &middot; 평균 <b>__AVG__</b> &middot;
09시 이후 <b>__LATE__</b>일 &middot; 확정 없음 <b>__MISS__</b>일</p>
<table>
<thead><tr><th>날짜</th><th>요일</th><th>확정 시각</th><th></th></tr></thead>
<tbody>
__TB__
</tbody></table>
<footer>08/01~08/09 하계휴가. &lsquo;기록 없음&rsquo;은 해당일 채팅방 대화가 없는 날입니다.</footer>
</div></body></html>"""
out=doc.replace('__AVG__',fm(avg)).replace('__LATE__',str(late)).replace('__MISS__',str(miss)).replace('__TB__',tb)
open('report.html','w',encoding='utf-8').write(out)
print(len(out),ontime,late,vac,miss,norec)
