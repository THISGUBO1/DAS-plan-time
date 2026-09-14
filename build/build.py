import re, datetime, json, html as H
p="/root/.claude/uploads/4e76de40-aaf2-5cbc-b9ec-82206b704b47/50980f34-KakaoTalk_20260914_1505_32_761_group.txt"
date_re=re.compile(r'^-+ (\d{4})년 (\d{1,2})월 (\d{1,2})일 (\S+요일) -+$')
msg_re=re.compile(r'^\[([^\]]+)\] \[(오전|오후) (\d{1,2}):(\d{2})\] (.*)$')
cur=None; days={}
for line in open(p,encoding='utf-8'):
    line=line.rstrip('\n')
    m=date_re.match(line.strip())
    if m:
        cur=datetime.date(int(m.group(1)),int(m.group(2)),int(m.group(3))); days.setdefault(cur,[]); continue
    m=msg_re.match(line)
    if m and cur:
        h=int(m.group(3))%12
        if m.group(2)=='오후': h+=12
        days[cur].append((datetime.time(h,int(m.group(4))),m.group(1),m.group(5)))
W='월화수목금토일'
VAC={datetime.date(2026,8,d) for d in range(1,10)}
rows=[]
d=datetime.date(2026,7,13); end=datetime.date(2026,9,14)
while d<=end:
    wd=d.weekday()
    if wd!=6:
        msgs=days.get(d)
        conf=[(t,x) for t,s,x in (msgs or []) if '신민섭' in s and '확정했' in x]
        pre=[(t,x) for t,s,x in (msgs or []) if '신민섭' in s and '확정' in x and '확정했' not in x]
        if d in VAC: st='휴가'
        elif conf: st='지연' if conf[0][0]>datetime.time(9,0) else '정시'
        elif msgs is not None: st='누락'
        else: st='기록없음'
        note=''
        if len(conf)>1: note='1/4열 %s · 2/3열 %s 분할 확정'%(conf[0][0].strftime('%H:%M'),conf[1][0].strftime('%H:%M'))
        elif pre: note='%s 지연 예고 — %s'%(pre[0][0].strftime('%H:%M'), pre[0][1].strip()[:60])
        elif conf and len(conf[0][1])>12: note=conf[0][1].replace('계획 확정했습니다.','').replace('계획 확정했습니다','').replace('계획확정했습니다','').strip(' .')[:70]
        elif st=='누락': note='확정 멘트 없음 (07:25 계획량 20대분 추가 공유만 있음)'
        elif st=='기록없음': note='해당일 채팅방 대화 없음'
        elif st=='휴가': note='하계휴가'
        rows.append({'date':d.strftime('%m/%d'),'full':d.strftime('%Y-%m-%d'),'w':W[wd],
                     'time':conf[0][0].strftime('%H:%M') if conf else '','st':st,'note':note,
                     'min':conf[0][0].hour*60+conf[0][0].minute if conf else None})
    d+=datetime.timedelta(days=1)
json.dump(rows,open('rows.json','w'),ensure_ascii=False)
c=lambda s:sum(1 for r in rows if r['st']==s)
tot=len(rows); done=c('정시')+c('지연')
times=[r['min'] for r in rows if r['min']]
avg=sum(times)/len(times)
print(tot,c('정시'),c('지연'),c('휴가'),c('누락'),c('기록없음'),'%02d:%02d'%(avg//60,avg%60))
