# Bússola Política · Expert SINTA

Sistema especialista de pergunta e resposta que classifica o posicionamento político do usuário. Trabalho da disciplina de Inteligência Artificial (ferramenta Expert SINTA 1.1b, LIA/UFC).

## Arquivos de entrega

| Arquivo | O que é |
|---|---|
| `entrega/DOMINIO_E_OBJETIVOS.txt` | Domínio de conhecimento, objetivos, variáveis e regras |
| `entrega/BUSSOLA_POLITICA.BCM` | Base de conhecimento do Expert SINTA |
| `entrega/BUSSOLA_POLITICA.txt` | Base exportada pelo SINTA (Arquivo / Exportar / Base de Conhecimento...) |

## Como o sistema raciocina

- 11 perguntas: 8 de múltipla escolha e 3 de Sim/Não. Todas são sempre feitas.
- 19 variáveis univaloradas: 11 perguntadas, 4 de tema (intervenção estatal, redistribuição de renda, valores sociais, lei e ordem), 2 de eixo (eixo econômico, eixo de costumes) e 2 objetivos (posição política, perfil institucional).
- 59 regras: 7 para cada tema e cada eixo (42), 9 que combinam os eixos e 8 para o perfil institucional.
- Respostas em polos opostos concluem o valor central com CNF 90% (tema) ou 80% (eixo); o SINTA multiplica as confianças ao encadear.

## Visualizador

`index.html` executa as mesmas 59 regras no navegador, com encadeamento para trás, botão "Por quê?" e histórico de regras, como na consulta do SINTA. Basta abrir o arquivo.

## Como abrir no Expert SINTA

Abra o `ExSINTA.exe` (Windows, ou Wine no Mac/Linux), menu Arquivo / Abrir base, e escolha `BUSSOLA_POLITICA.BCM`. O botão de play inicia a consulta.

## Código-fonte (`src/`)

- `spec.py`: a base de conhecimento (variáveis, perguntas, regras). Fonte única.
- `gen_bcm.py`: grava o `.BCM` no formato binário do Expert SINTA. Uso: `python3 gen_bcm.py saida.BCM`.
- `engine.py`: motor de referência em Python, usado para conferir as 52.488 combinações de respostas.
- `build_web.py` e `web_template.html`: geram o `index.html`.

O `.BCM` foi gerado por script e validado no Expert SINTA 1.1b: a base abre, duas consultas completas deram o resultado previsto e o `.txt` da entrega foi exportado pelo próprio SINTA.

Finalidade didática: a classificação é simplificada e não é juízo de valor sobre nenhuma posição.
