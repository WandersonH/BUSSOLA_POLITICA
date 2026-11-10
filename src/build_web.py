# -*- coding: utf-8 -*-
"""Gera ../index.html a partir de spec.py e web_template.html."""
import json
from spec import *
data = dict(title=TITLE, author=AUTHOR, info=INFO, goals=GOALS,
    vars=[dict(name=n, values=vs, question=q) for n,_,vs,q in VARS],
    rules=[dict(name=r['name'], prem=[list(p) for p in r['prem']], concl=list(r['concl']), cnf=r['cnf']) for r in RULES])
html = open('web_template.html', encoding='utf-8').read().replace('/*DATA*/', json.dumps(data, ensure_ascii=False))
open('../index.html', 'w', encoding='utf-8').write(html)
