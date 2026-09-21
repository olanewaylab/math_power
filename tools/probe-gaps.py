# -*- coding: utf-8 -*-
import pymupdf, os, re, collections
d='content/past-papers'
PROBE={
 'граници (lim)': r'\blim\b|границата|граница на',
 'производна':    r'производна|допирателна(та)? към графиката|нараства(ща|не).{0,30}интервал',
 'проценти (%)':  r'%',
 'куб':           r'\bкуб\b|куба|телесен диагонал',
 'четност/ограниченост на функция': r'четна|нечетна|ограничена|периодична',
 'статистика':    r'медиана(та)? на|средна аритметична|мода(та)?\b|размах',
 'комплексни числа': r'комплексн|имагинер',
 'матрици/детерминанти': r'матрица|детерминанта',
 'интеграл':      r'интеграл',
}
hits=collections.Counter(); papers=collections.Counter(); tot=0
for f in sorted(os.listdir(d)):
    if not f.lower().endswith('.pdf'): continue
    tot+=1
    full="\n".join(p.get_text() for p in pymupdf.open(os.path.join(d,f)))
    i=full.rfind('ОТГОВОРИ'); body=full[:i] if i>0 else full
    for name,rx in PROBE.items():
        n=len(re.findall(rx, body, re.I))
        if n:
            hits[name]+=n; papers[name]+=1
print("варианти: %d\n"%tot)
print("%-36s %8s %10s"%("тема","срещания","в N варианта"))
for name in PROBE:
    print("%-36s %8d %10d"%(name, hits[name], papers[name]))
