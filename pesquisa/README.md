# Pesquisa: Projetos de Lei da causa animal — Município de São Paulo

Levantamento feito em 09/11/2026 nos dados oficiais da Câmara Municipal de São Paulo (SPLegis).

## Arquivos

| Arquivo | Conteúdo |
|---|---|
| `SPLegis-Animal-Projetos-de-Lei.xlsx` | Planilha principal: abas **Leia-me** (critérios e resumo), **Projetos** (todos os incluídos), **Em tramitação** e **Excluídos** (com o motivo) |
| `projetos-incluidos.csv` | Mesma lista da aba "Projetos", em CSV (abre no Excel) |
| `projetos-excluidos.csv` | Projetos retirados da lista e o motivo |
| `inteiro-teor/` | Inteiro teor, em Markdown, dos 264 projetos **em tramitação** (um arquivo por projeto, índice no `README.md` e todos juntos em `todos-os-projetos.md`) |
| `scripts/` | Scripts em Python usados na coleta, para refazer ou atualizar a pesquisa |

## Método

1. **Coleta:** todos os Projetos de Lei (PL) de 1991 a 2026 pelo webservice de dados abertos da Câmara (`splegisws.saopaulo.sp.leg.br`), com ementa, assuntos indexados e motivo de encerramento. Foram 28.212 PLs.
2. **Recorte temático:** busca de palavras-chave na ementa e nos assuntos, seguida de revisão manual de cada resultado.
3. **Verificação individual:** consulta da ficha "Detalhado" de cada projeto em `splegisconsulta.saopaulo.sp.leg.br`, que traz pareceres das comissões, veto, lei gerada e encerramento.
4. **Exclusões (pedido do usuário):**
   - encerrados por ilegalidade/inconstitucionalidade (art. 79 do Regimento Interno);
   - com parecer da CCJ **aprovado** pela ilegalidade ou inconstitucionalidade (vale o último parecer), salvo se viraram lei;
   - apensados, com proposta de apensamento do relator da CCJ, ou de igual teor a outro projeto (art. 212 do RI).

Projetos com **apenas relatório do relator** pela ilegalidade, ainda não votado na CCJ, foram mantidos e estão sinalizados na coluna "Parecer CCJ".

## Como atualizar

```bash
cd pesquisa/scripts && mkdir -p dados fichas
python3 baixar.py 1991 2026   # baixa os PLs por ano
python3 filtrar.py            # pré-seleção por palavras-chave
python3 selecionar.py         # aplica a revisão manual (listas no script)
python3 fichas.py             # consulta a ficha de cada projeto
python3 reparse.py            # detalha os pareceres da CCJ
python3 montar.py             # gera a planilha
python3 inteiro_teor.py       # baixa e faz OCR do texto inicial dos projetos em tramitação (requer tesseract-ocr-por)
python3 markdown.py           # gera os arquivos Markdown do inteiro teor
```

> A classificação por **tema** é automática (por palavras-chave) e serve para facilitar os filtros; confira a ementa antes de usar em documento técnico.
