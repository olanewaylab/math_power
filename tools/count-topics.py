# -*- coding: utf-8 -*-
import pymupdf, os, re, collections, io, json
d='content/past-papers'
RULES=[  # (код, модул, регекс по условието) — първото съвпадение печели
 ('C2','C', r'вероятн'),
 ('C3','C', r'медиана(та)? им|средна аритметична|мода|средн(а|ата) температура|средн(ия|ият) успех'),
 ('C1','C', r'начини|пермутац|комбинац|вариац|подредб|наред(ят|и)|избира(не|т)|числа.{0,40}цифри'),
 ('A11','A', r'log|логарит'),
 ('F4','F', r'аритметична прогресия'),
 ('F5','F', r'геометричн(а|ата) прогресия'),
 ('G6','G', r'пирамида|призма|конус|цилиндър|сфера|топка|ръб|околна повърхнина|обем'),
 ('T4','T', r'(sin|cos|tg|синус|косинус)[^.]{0,80}триъгълник|триъгълник[^.]{0,80}(sin|cos|tg)'),
 ('T3','T', r'да се реш[^.]{0,60}(sin|cos|tg)|(sin|cos|tg)[^.]{0,40}=\s*[-−]?\d'),
 ('T2','T', r'sin|cos|tg|cotg|синус|косинус|тангенс'),
 ('G4','G', r'окръжност'),
 ('G3','G', r'трапец|успоредник|ромб|четириъгълник'),
 ('G1','G', r'триъгълник'),
 ('G8','G', r'права|координатн|разстояние от точка|окръжност с център|абсцис'),
 ('F1','F', r'дефиниционн|дефинирана'),
 ('F2','F', r'парабола|квадратна функция|най-голяма(та)? стойност|най-малка(та)? стойност'),
 ('A7','A', r'модул|\|'),
 ('A10','A', r'показател|степен на|\d\s*\^|2\s*[хx𝑥]'),
 ('A8','A', r'неравенство'),
 ('A12','A', r'скорост|км/ч|работник|сплав|смес|влак|лодка|басейн|процент'),
 ('A9','A', r'системата|система'),
 ('A6','A', r'√|корен(и)? на уравнението.{0,30}√'),
 ('A4','A', r'уравнение'),
 ('A3','A', r'израз'),
]
def classify(t):
    for code,mod,rx in RULES:
        if re.search(rx, t, re.I): return code,mod
    return '??','?'
part1=collections.Counter(); part2=collections.Counter()
m1=collections.Counter(); m2=collections.Counter()
n1=n2=0; unknown=[]
for f in sorted(os.listdir(d)):
    if not f.lower().endswith('.pdf'): continue
    doc=pymupdf.open(os.path.join(d,f))
    txt="\n".join(p.get_text() for p in doc)
    txt=re.split(r'ОТГОВОРИ', txt.upper().replace('ОТГОВОРИ','ОТГОВОРИ'))[0] if 'ОТГОВОРИ' in txt else txt
    full="\n".join(p.get_text() for p in doc)
    # отрязваме ключа: всичко след последното "ОТГОВОРИ"
    i=full.rfind('ОТГОВОРИ')
    body=full[:i] if i>0 else full
    j=body.find('ВТОРА ЧАСТ')
    p1, p2 = (body[:j], body[j:]) if j>0 else (body, '')
    for src, cnt, mc, which in ((p1,part1,m1,1),(p2,part2,m2,2)):
        tasks=re.split(r'(?m)^\s*(?=\d{1,2}\.\s)', src)
        for t in tasks:
            t=t.strip()
            if not re.match(r'^\d{1,2}\.\s', t) or len(t)<25: continue
            code,mod=classify(t)
            cnt[code]+=1; mc[mod]+=1
            if which==1: globals().__setitem__('n1', globals()['n1']+1)
            else: globals().__setitem__('n2', globals()['n2']+1)
            if code=='??' and len(unknown)<8: unknown.append(t[:100].replace("\n"," "))
print("задачи разпознати: Част 1 =", n1, " Част 2 =", n2)
print("\n--- по модули, Част 1 ---")
tot=sum(m1.values())
for m,c in m1.most_common(): print("  %s: %3d  (%4.1f%%)"%(m,c,100.0*c/tot))
print("\n--- по модули, Част 2 ---")
tot2=sum(m2.values())
for m,c in m2.most_common(): print("  %s: %3d  (%4.1f%%)"%(m,c,100.0*c/tot2))
print("\n--- по теми, Част 1 (топ 20) ---")
for k,c in part1.most_common(20): print("  %-4s %3d  (%4.1f%%)"%(k,c,100.0*c/sum(part1.values())))
print("\n--- по теми, Част 2 (топ 20) ---")
for k,c in part2.most_common(20): print("  %-4s %3d  (%4.1f%%)"%(k,c,100.0*c/sum(part2.values())))
print("\n--- неразпознати примери ---")
for u in unknown: print("  ", u)
json.dump({'p1':part1,'p2':part2,'m1':m1,'m2':m2,'n1':n1,'n2':n2},
          io.open('/tmp/claude-0/-home-user-math-power/e68921e1-2c9f-5bd5-bf6e-e3990b987aa2/scratchpad/freq.json','w',encoding='utf-8'), ensure_ascii=False)
