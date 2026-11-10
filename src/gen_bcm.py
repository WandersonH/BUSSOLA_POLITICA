# -*- coding: utf-8 -*-
import struct, sys
from spec import *
OUT = sys.argv[1]
# Campos fixos observados em bases salvas pelo Expert SINTA 1.1b
MAGIC = bytes.fromhex('2d0cbd166328f397ca22')       # assinatura do arquivo
HDR3  = bytes.fromhex('010000')
OPTS  = bytearray(1028); OPTS[0x201] = OPTS[0x302] = OPTS[0x403] = 1   # opcoes padrao, sem arquivo de ajuda
TAIL  = bytes.fromhex('000080000000000000')         # CNF minimo 50% (Real48) e opcoes finais
def pstr(s, size=256):
    b = s.encode('latin1'); assert len(b) <= 255, s
    return (bytes([len(b)]) + b).ljust(size, b'\0')
def w(x): return struct.pack('<H', x & 0xFFFF)
def real48(x):
    if x == 0: return b'\0'*6
    import math
    m, e = math.frexp(x)            # x = m*2^e, 0.5<=m<1
    mant = int(round((m*2 - 1) * (1 << 39)))
    return bytes([e + 128]) + mant.to_bytes(5,'little')
def order(n):                       # ordem de gravacao usada pelo Expert SINTA
    s = n//2 + 1; a = [s]; k = 2
    while len(a) < len([x for x in range(1,n+1) if (x - s) % 2 == 0]):
        for c in (s+k, s-k):
            if 1 <= c <= n: a.append(c)
        k += 2
    b = []; k = 1
    while len(b) < n - len(a):
        for c in (s-k, s+k):
            if 1 <= c <= n: b.append(c)
        k += 2
    return a + b
# codigos
vcode = {name: i+1 for i,(name,_,_,_) in enumerate(VARS)}
vals = []                           # (code, name, var, pos)
valcode = {}
for name,_,vs,_ in VARS:
    for p,val in enumerate(vs):
        c = len(vals)+1; vals.append((c,val,vcode[name],p+1)); valcode[(name,val)] = c
def vc(var,val):
    if val == "Sim": return -2
    if val == "Não": return -3
    return valcode[(var,val)]
out = bytearray()
out += MAGIC + pstr("") + HDR3 + pstr(TITLE) + pstr(AUTHOR)
assert len(out) == 0x30d
out += w(len(INFO)) + b''.join(pstr(l) for l in INFO)
out += OPTS
out += w(len(VARS))
for c in order(len(VARS)):
    name,typ,_,_ = VARS[c-1]; out += w(c) + pstr(name) + w(typ)
out += w(len(vals))
for c in range(1,len(vals)+1):   # ordem natural: o SINTA lista os valores na ordem do arquivo
    _,val,var,pos = vals[c-1]; out += w(c) + pstr(val) + w(var) + w(pos)
ro = order(len(RULES))
out += w(len(RULES))
for c in ro:
    r = RULES[c-1]; var,val = r['concl']; out += w(c) + w(vcode[var]) + w(vc(var,val)) + real48(r['cnf']/100)
out += w(sum(len(RULES[c-1]['prem']) for c in ro))
for c in ro:
    P = RULES[c-1]['prem']
    for i,(var,op,val) in enumerate(P):
        out += w(c) + w(vcode[var]) + pstr(op,3) + w(vc(var,val)) + bytes([2 if i == len(P)-1 else 0, 0, 0])
out += w(len(RULES))
for c in ro: out += w(c) + pstr(RULES[c-1]['name']) + w(c)
out += w(0)
Q = [c for c in order(len(VARS)) if VARS[c-1][3]]
out += w(len(Q))
for c in Q: out += w(c) + pstr(VARS[c-1][3]) + b'\0\0\1'
out += w(len(GOALS)) + b''.join(w(vcode[g]) + b'\1' for g in GOALS)
out += w(0) + TAIL
open(OUT,'wb').write(out); print(OUT, len(out))
