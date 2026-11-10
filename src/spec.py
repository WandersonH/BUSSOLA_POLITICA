# -*- coding: utf-8 -*-
"""Base de conhecimento 'Bussola Politica' - fonte unica para o .BCM e para o visualizador web."""
TITLE = "Bússola Política - Sistema Especialista de Posicionamento Político"
AUTHOR = "Wanderson Honorio Roberto da Silva"
INFO = [
 "Sistema especialista que identifica o posicionamento político-ideológico",
 "do usuário a partir de seis perguntas sobre economia, costumes e",
 "instituições.",
 "",
 "O sistema usa dois eixos: o eixo econômico (esquerda, centro, direita)",
 "e o eixo de costumes (progressista, moderado, conservador). A combinação",
 "dos dois eixos define a posição política. Um segundo objetivo indica o",
 "perfil institucional (democrático, ambivalente ou autoritário).",
 "",
 "Finalidade exclusivamente didática: o resultado é uma classificação",
 "simplificada e não um juízo de valor sobre qualquer posição.",
]
UNI, MULTI, NUM = 0, 1, 2
# (nome, tipo, [valores], pergunta)   valores [] => Sim/Nao
VARS = [
 ("papel do Estado", UNI, ["Conduzir a economia e manter empresas estatais",
                            "Regular o mercado e corrigir desigualdades",
                            "Interferir o mínimo possível"],
  "Na sua opinião, qual deve ser o papel do Estado na economia?"),
 ("impostos e serviços", UNI, ["Mais impostos e mais serviços públicos",
                                "Manter o equilíbrio atual",
                                "Menos impostos e menos serviços públicos"],
  "Entre impostos e serviços públicos, qual combinação você prefere?"),
 ("valores e costumes", UNI, ["Acolher as mudanças e ampliar direitos",
                               "Mudar aos poucos, com cautela",
                               "Preservar os valores tradicionais"],
  "Diante de mudanças nos costumes (família, comportamento, identidade), o que a sociedade deve fazer?"),
 ("segurança pública", UNI, ["Prevenção e políticas sociais",
                              "Equilíbrio entre prevenção e punição",
                              "Penas mais duras e mais policiamento"],
  "Qual deve ser a prioridade no combate à criminalidade?"),
 ("aceita líder sem freios", UNI, [],
  "Você aceitaria um líder forte que governasse sem depender do Congresso e do Judiciário?"),
 ("defende imprensa livre", UNI, [],
  "A imprensa deve ser livre para criticar o governo, mesmo quando erra?"),
 ("eixo econômico", UNI, ["Esquerda", "Centro", "Direita"], None),
 ("eixo de costumes", UNI, ["Progressista", "Moderado", "Conservador"], None),
 ("posição política", UNI, ["Esquerda", "Centro-esquerda", "Esquerda conservadora nos costumes",
                             "Centro", "Centro-direita", "Liberal (economia e costumes)", "Direita"], None),
 ("perfil institucional", UNI, ["Democrático", "Ambivalente", "Autoritário"], None),
]
GOALS = ["posição política", "perfil institucional"]
E_, OU_ = "E", "OU"
PE, IS, VC, SP = "papel do Estado", "impostos e serviços", "valores e costumes", "segurança pública"
LD, IM = "aceita líder sem freios", "defende imprensa livre"
EE, EC, PP, PI = "eixo econômico", "eixo de costumes", "posição política", "perfil institucional"
v = {n: vals for n, _, vals, _ in VARS}
def R(name, prem, concl, cnf=100):
    return dict(name=name, prem=prem, concl=concl, cnf=cnf)
RULES = [
 # --- eixo economico ---
 R("Economia: esquerda",  [(PE,"=",v[PE][0]), (IS,"<>",v[IS][2])], (EE,"Esquerda")),
 R("Economia: direita",   [(PE,"=",v[PE][2]), (IS,"<>",v[IS][0])], (EE,"Direita")),
 R("Economia: centro",    [(PE,"=",v[PE][1])],                     (EE,"Centro")),
 R("Economia: centro por respostas mistas 1", [(PE,"=",v[PE][0]), (IS,"=",v[IS][2])], (EE,"Centro"), 80),
 R("Economia: centro por respostas mistas 2", [(PE,"=",v[PE][2]), (IS,"=",v[IS][0])], (EE,"Centro"), 80),
 # --- eixo de costumes ---
 R("Costumes: progressista", [(VC,"=",v[VC][0]), (SP,"<>",v[SP][2])], (EC,"Progressista")),
 R("Costumes: conservador",  [(VC,"=",v[VC][2]), (SP,"<>",v[SP][0])], (EC,"Conservador")),
 R("Costumes: moderado",     [(VC,"=",v[VC][1])],                     (EC,"Moderado")),
 R("Costumes: moderado por respostas mistas 1", [(VC,"=",v[VC][0]), (SP,"=",v[SP][2])], (EC,"Moderado"), 80),
 R("Costumes: moderado por respostas mistas 2", [(VC,"=",v[VC][2]), (SP,"=",v[SP][0])], (EC,"Moderado"), 80),
 # --- posicao politica ---
 R("Posição: esquerda",              [(EE,"=","Esquerda"), (EC,"=","Progressista")], (PP,"Esquerda")),
 R("Posição: centro-esquerda 1",     [(EE,"=","Esquerda"), (EC,"=","Moderado")],     (PP,"Centro-esquerda")),
 R("Posição: esquerda conservadora", [(EE,"=","Esquerda"), (EC,"=","Conservador")],  (PP,"Esquerda conservadora nos costumes")),
 R("Posição: centro-esquerda 2",     [(EE,"=","Centro"),   (EC,"=","Progressista")], (PP,"Centro-esquerda")),
 R("Posição: centro",                [(EE,"=","Centro"),   (EC,"=","Moderado")],     (PP,"Centro")),
 R("Posição: centro-direita 1",      [(EE,"=","Centro"),   (EC,"=","Conservador")],  (PP,"Centro-direita")),
 R("Posição: liberal",               [(EE,"=","Direita"),  (EC,"=","Progressista")], (PP,"Liberal (economia e costumes)")),
 R("Posição: centro-direita 2",      [(EE,"=","Direita"),  (EC,"=","Moderado")],     (PP,"Centro-direita")),
 R("Posição: direita",               [(EE,"=","Direita"),  (EC,"=","Conservador")],  (PP,"Direita")),
 # --- perfil institucional ---
 R("Instituições: democrático",   [(LD,"=","Não"), (IM,"=","Sim")], (PI,"Democrático")),
 R("Instituições: autoritário",   [(LD,"=","Sim"), (IM,"=","Não")], (PI,"Autoritário")),
 R("Instituições: ambivalente 1", [(LD,"=","Sim"), (IM,"=","Sim")], (PI,"Ambivalente")),
 R("Instituições: ambivalente 2", [(LD,"=","Não"), (IM,"=","Não")], (PI,"Ambivalente")),
]
