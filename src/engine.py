# -*- coding: utf-8 -*-
"""Motor de referencia (encadeamento para tras, CNF = min das premissas x CNF da regra, limiar 50%)."""
from spec import *
QUESTION = {n: q for n,_,_,q in VARS}
def consult(answers):
    facts = {k:(v,100) for k,v in answers.items()}; fired = []
    def ev(var):
        if var in facts: return facts[var]
        if QUESTION[var]: raise KeyError(var)
        for i,r in enumerate(RULES):
            if r['concl'][0] != var: continue
            cnf = 100; ok = True
            for pv,op,val in r['prem']:
                f = ev(pv)
                if f is None or (f[0]==val) != (op=='='): ok = False; break
                cnf = min(cnf, f[1])
            c = cnf*r['cnf']/100
            if ok and c >= 50:
                facts[var] = (r['concl'][1], c); fired.append(i+1); return facts[var]
        facts[var] = None; return None
    return {g: ev(g) for g in GOALS}, fired
if __name__ == '__main__':
    import itertools, json
    qs = [(n, vs or ["Sim","Não"]) for n,_,vs,q in VARS if q]
    out = []
    for combo in itertools.product(*[vs for _,vs in qs]):
        res, fired = consult(dict(zip([n for n,_ in qs], combo)))
        assert all(res[g] for g in GOALS), combo
        out.append([list(combo), [[res[g][0], res[g][1]] for g in GOALS], fired])
    json.dump(out, open('expected.json','w'), ensure_ascii=False)
    from collections import Counter
    print(len(out), Counter(o[1][0][0] for o in out), Counter(o[1][1][0] for o in out), Counter(o[1][0][1] for o in out))
    r,f = consult({PE:v[PE][0], IS:v[IS][2], VC:v[VC][0], SP:v[SP][0], LD:"Não", IM:"Sim"}); print(r,f)
