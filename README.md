# Bússola Política · Expert SINTA

Sistema especialista de pergunta e resposta que classifica o posicionamento político do usuário. Trabalho da disciplina de Inteligência Artificial (ferramenta Expert SINTA 1.1b, LIA/UFC).

## Arquivos de entrega

| Arquivo | O que é |
|---|---|
| `entrega/DOMINIO_E_OBJETIVOS.txt` | Domínio de conhecimento, objetivos, variáveis e regras |
| `entrega/BUSSOLA_POLITICA.BCM` | Base de conhecimento do Expert SINTA |
| `entrega/BUSSOLA_POLITICA.txt` | Base exportada pelo SINTA (Arquivo / Exportar / Base de Conhecimento...) |

## Como o sistema raciocina

- 6 perguntas: 4 de múltipla escolha e 2 de Sim/Não.
- 10 variáveis univaloradas: 6 perguntadas, 2 intermediárias (eixo econômico, eixo de costumes) e 2 objetivos (posição política, perfil institucional).
- 23 regras: 5 para cada eixo, 9 que combinam os eixos e 4 para o perfil institucional.
- Regras de respostas mistas concluem o valor central do eixo com CNF 80%.

## Visualizador

`index.html` executa as mesmas 23 regras no navegador, com encadeamento para trás, botão "Por quê?" e histórico de regras, como na consulta do SINTA. Basta abrir o arquivo.

## Como abrir no Expert SINTA

Abra o `ExSINTA.exe` (Windows, ou Wine no Mac/Linux), menu Arquivo / Abrir base, e escolha `BUSSOLA_POLITICA.BCM`. O botão de play inicia a consulta.

## Código-fonte (`src/`)

- `spec.py`: a base de conhecimento (variáveis, perguntas, regras). Fonte única.
- `gen_bcm.py`: grava o `.BCM` no formato binário do Expert SINTA. Uso: `python3 gen_bcm.py saida.BCM`.
- `engine.py`: motor de referência em Python, usado para conferir as 324 combinações de respostas.
- `build_web.py` e `web_template.html`: geram o `index.html`.

O `.BCM` foi gerado por script e validado no Expert SINTA 1.1b: a base abre, a consulta roda e o `.txt` da entrega foi exportado pelo próprio SINTA.

Finalidade didática: a classificação é simplificada e não é juízo de valor sobre nenhuma posição.
