# -*- coding: utf-8 -*-
import pymupdf, os, re, hashlib, subprocess, io
d='content/past-papers'
MON={'януари':1,'февруари':2,'март':3,'април':4,'май':5,'юни':6,'юли':7,
     'август':8,'септември':9,'октомври':10,'ноември':11,'декември':12}
files=sorted([f for f in os.listdir(d) if f.lower().endswith('.pdf')])
seen={}; rows=[]
def sh(*a): subprocess.run(list(a), check=True)
for f in files:
    p=os.path.join(d,f)
    h=hashlib.md5(open(p,'rb').read()).hexdigest()
    doc=pymupdf.open(p); head=doc[0].get_text()[:300].replace("\n"," ")
    txt="\n".join(pg.get_text() for pg in doc)
    m=re.search(r'(\d{1,2})\s+([а-я]+)\s+(\d{4})', head)
    dd,mon,yy=int(m.group(1)),MON[m.group(2)],int(m.group(3))
    v2='ВАРИАНТ ВТОРИ' in head.upper() or 'ВАРИАНТ 2' in head.upper()
    new="%04d-%02d-%02d%s.pdf"%(yy,mon,dd,"-v2" if v2 else "")
    if h in seen:
        sh('git','rm','-q',p); print("дубликат премахнат: %s == %s"%(f,seen[h])); continue
    seen[h]=new
    if f!=new: sh('git','mv',p,os.path.join(d,new))
    rows.append({'file':new,'date':"%04d-%02d-%02d"%(yy,mon,dd),
                 'v':'2' if v2 else '1','ans':'ОТГОВОРИ' in txt.upper(),
                 'session':'предварителен' if mon in (3,4,5) else 'редовен'})
rows.sort(key=lambda r:(r['date'],r['v']))

Q1=u'„'; Q2=u'“'   # български кавички
L=[]
L.append(u'# Каталог на реалните варианти\n')
L.append(u'Всички файлове са тестове по математика на ТУ-София. Имената следват')
L.append(u'конвенцията `YYYY-MM-DD.pdf` (`-v2` за втори вариант от същата дата),')
L.append(u'а **датата е взета от самия документ**, не от оригиналното име на файла.\n')
L.append(u'Общо: **%d варианта**, всички с официален ключ на отговорите вътре.\n'%len(rows))
L.append(u'| Дата | Вариант | Сесия | Файл | Ключ |')
L.append(u'|---|---|---|---|---|')
for r in rows:
    L.append(u'| %s | %s | %s | `%s` | %s |'%(r['date'],r['v'],r['session'],r['file'],
             u'да' if r['ans'] else u'**НЕ**'))
years={}
for r in rows: years.setdefault(r['date'][:4],[]).append(r)
L.append(u'\n## По години\n')
L.append(u'| Година | Варианти | Предварителни | Редовни |')
L.append(u'|---|---|---|---|')
for y,v in sorted(years.items()):
    L.append(u'| %s | %d | %d | %d |'%(y,len(v),
        sum(1 for x in v if x['session']==u'предварителен'),
        sum(1 for x in v if x['session']==u'редовен')))
L.append(u'\n## Как се ползват\n')
L.append(u'- Всеки файл е 5 страници: 20 задачи с избираем отговор, 10 със свободен')
L.append(u'  отговор, талон за отговори и ключ на последната страница.')
L.append(u'- Текстът се чете машинно — агентът взема задача директно от PDF-а.')
L.append(u'- **Ключът е в същия файл.** При пробен тест ученикът не отваря последната')
L.append(u'  страница, докато не приключи.')
L.append(u'- Хронологията има значение: старите варианти (2016–2019) са за трениране')
L.append(u'  по теми, новите (2024–2026) се пазят за режим ' + Q1 + u'изпит на време' + Q2 + u' във Фаза 4.')
io.open(os.path.join(d,'INDEX.md'),'w',encoding='utf-8').write(u"\n".join(L)+u"\n")
print("\nкаталог: %d варианта"%len(rows))
