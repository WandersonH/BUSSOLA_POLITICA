# -*- coding: utf-8 -*-
"""Base de conhecimento 'Bussola Politica' - fonte unica para o .BCM e para o visualizador web."""
TITLE = "Bússola Política - Sistema Especialista de Posicionamento Político"
AUTHOR = "Wanderson Honorio Roberto da Silva"
INFO = [
 "Sistema especialista que identifica o posicionamento político-ideológico",
 "do usuário a partir de onze perguntas sobre economia, costumes e",
 "instituições.",
 "",
 "Cada par de perguntas define um tema (intervenção estatal, redistribuição",
 "de renda, valores sociais, lei e ordem). Os temas formam dois eixos: o",
 "eixo econômico (esquerda, centro, direita) e o eixo de costumes",
 "(progressista, moderado, conservador). A combinação dos eixos define a",
 "posição política. Um segundo objetivo indica o perfil institucional",
 "(democrático, ambivalente ou autoritário).",
 "",
 "Finalidade exclusivamente didática: o resultado é uma classificação",
 "simplificada e não um juízo de valor sobre qualquer posição.",
]
UNI, MULTI, NUM = 0, 1, 2
# perguntas de multipla escolha: as alternativas vao sempre do polo 1 ao polo 3
PE, ES = "papel do Estado", "empresas estatais"
IS, PS = "impostos e serviços", "programas sociais"
MC, RL = "mudanças nos costumes", "religião e leis"
SP, PD = "segurança pública", "política de drogas"
LD, IM, DJ = "aceita líder sem freios", "defende imprensa livre", "cumpre decisões da Justiça"
IE, RR, VS, LO = "intervenção estatal", "redistribuição de renda", "valores sociais", "lei e ordem"
EE, EC, PP, PI = "eixo econômico", "eixo de costumes", "posição política", "perfil institucional"
# (nome, tipo, [valores], pergunta)   valores [] => Sim/Nao
VARS = [
 (PE, UNI, ["Conduzir a economia e planejar o desenvolvimento",
            "Regular o mercado e corrigir desigualdades",
            "Interferir o mínimo possível"],
  "Na sua opinião, qual deve ser o papel do Estado na economia?"),
 (ES, UNI, ["Manter e fortalecer as estatais",
            "Privatizar apenas as que dão prejuízo",
            "Privatizar a maioria das estatais"],
  "O que o governo deve fazer com as empresas estatais?"),
 (IS, UNI, ["Mais impostos e mais serviços públicos",
            "Manter o equilíbrio atual",
            "Menos impostos e menos serviços públicos"],
  "Entre impostos e serviços públicos, qual combinação você prefere?"),
 (PS, UNI, ["Ampliar os programas",
            "Manter os programas no nível atual",
            "Reduzir os programas"],
  "O que fazer com os programas de transferência de renda?"),
 (MC, UNI, ["Acolher as mudanças e ampliar direitos",
            "Mudar aos poucos, com cautela",
            "Preservar os valores tradicionais"],
  "Diante de mudanças nos costumes (família, comportamento, identidade), o que a sociedade deve fazer?"),
 (RL, UNI, ["Nenhuma: o Estado deve ser totalmente laico",
            "Alguma, como um dos valores da sociedade",
            "Grande: as leis devem refletir valores religiosos"],
  "Qual deve ser a influência da religião sobre as leis?"),
 (SP, UNI, ["Prevenção e políticas sociais",
            "Equilíbrio entre prevenção e punição",
            "Penas mais duras e mais policiamento"],
  "Qual deve ser a prioridade no combate à criminalidade?"),
 (PD, UNI, ["Tratar como saúde pública e descriminalizar",
            "Manter a legislação atual",
            "Endurecer as leis e a punição"],
  "Como o Estado deve tratar o uso de drogas?"),
 (LD, UNI, [], "Você aceitaria um líder forte que governasse sem depender do Congresso e do Judiciário?"),
 (IM, UNI, [], "A imprensa deve ser livre para criticar o governo, mesmo quando erra?"),
 (DJ, UNI, [], "Um governo deve cumprir as decisões da Justiça mesmo quando discorda delas?"),
 (IE, UNI, ["Alta", "Moderada", "Baixa"], None),
 (RR, UNI, ["Ampla", "Moderada", "Restrita"], None),
 (VS, UNI, ["Liberais", "Moderados", "Tradicionais"], None),
 (LO, UNI, ["Garantista", "Equilibrada", "Punitivista"], None),
 (EE, UNI, ["Esquerda", "Centro", "Direita"], None),
 (EC, UNI, ["Progressista", "Moderado", "Conservador"], None),
 (PP, UNI, ["Esquerda", "Centro-esquerda", "Esquerda conservadora nos costumes",
            "Centro", "Centro-direita", "Liberal (economia e costumes)", "Direita"], None),
 (PI, UNI, ["Democrático", "Ambivalente", "Autoritário"], None),
]
GOALS = [PP, PI]
v = {n: vals for n, _, vals, _ in VARS}
def R(name, prem, concl, cnf=100):
    return dict(name=name, prem=prem, concl=concl, cnf=cnf)
def combina(a, b, out, rot, mix):
    """7 regras que combinam duas variaveis de 3 valores (polo 1, meio, polo 3) em uma terceira.
    Toda regra usa as duas variaveis, entao as duas sao sempre avaliadas."""
    A, B, O = v[a], v[b], v[out]
    return [
     R(f"{rot}: {O[0]} 1", [(a,"=",A[0]), (b,"<>",B[2])], (out,O[0])),
     R(f"{rot}: {O[0]} 2", [(a,"=",A[1]), (b,"=",B[0])],  (out,O[0])),
     R(f"{rot}: {O[2]} 1", [(a,"=",A[2]), (b,"<>",B[0])], (out,O[2])),
     R(f"{rot}: {O[2]} 2", [(a,"=",A[1]), (b,"=",B[2])],  (out,O[2])),
     R(f"{rot}: {O[1]}",   [(a,"=",A[1]), (b,"=",B[1])],  (out,O[1])),
     R(f"{rot}: {O[1]} por respostas opostas 1", [(a,"=",A[0]), (b,"=",B[2])], (out,O[1]), mix),
     R(f"{rot}: {O[1]} por respostas opostas 2", [(a,"=",A[2]), (b,"=",B[0])], (out,O[1]), mix),
    ]
RULES = []
RULES += combina(PE, ES, IE, "Intervenção estatal", 90)
RULES += combina(IS, PS, RR, "Redistribuição", 90)
RULES += combina(IE, RR, EE, "Eixo econômico", 80)
RULES += combina(MC, RL, VS, "Valores sociais", 90)
RULES += combina(SP, PD, LO, "Lei e ordem", 90)
RULES += combina(VS, LO, EC, "Eixo de costumes", 80)
POS = [["Esquerda", "Centro-esquerda", "Esquerda conservadora nos costumes"],
       ["Centro-esquerda", "Centro", "Centro-direita"],
       ["Liberal (economia e costumes)", "Centro-direita", "Direita"]]
for i, e in enumerate(v[EE]):
    for j, c in enumerate(v[EC]):
        RULES.append(R(f"Posição: {e} + {c}", [(EE,"=",e), (EC,"=",c)], (PP, POS[i][j])))
# perfil institucional: resposta democratica = lider Nao, imprensa Sim, Justica Sim
for l in ("Não", "Sim"):
    for m in ("Sim", "Não"):
        for d in ("Sim", "Não"):
            n = (l == "Não") + (m == "Sim") + (d == "Sim")
            out = "Democrático" if n == 3 else "Autoritário" if n == 0 else "Ambivalente"
            RULES.append(R(f"Instituições: {out} ({n} de 3)", [(LD,"=",l), (IM,"=",m), (DJ,"=",d)], (PI,out)))
