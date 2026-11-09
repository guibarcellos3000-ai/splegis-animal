# Pesquisa: Projetos de Lei sobre proteção às mulheres — Município de São Paulo

Levantamento feito em 09/11/2026 nos dados oficiais da Câmara Municipal de São Paulo (SPLegis), com o mesmo método usado na pesquisa da causa animal (`../pesquisa/`).

## Arquivos

| Arquivo | Conteúdo |
|---|---|
| `GUIA-PRODUCAO-LEGISLATIVA.md` | **Comece por aqui.** Orientações para evitar apensamento e inconstitucionalidade e, por tema, os projetos em tramitação, as leis já aprovadas e os projetos barrados pela CCJ |
| `SPLegis-Mulheres-Projetos-de-Lei.xlsx` | Planilha com abas **Leia-me**, **Projetos** (684 incluídos), **Em tramitação** (351) e **Excluídos** (95, com o motivo) |
| `inteiro-teor/` | Inteiro teor, em Markdown, dos 351 projetos **em tramitação**: um arquivo por projeto, índice no `README.md` e todos juntos em `todos-os-projetos.md` |
| `projetos-incluidos.csv` / `projetos-excluidos.csv` | As mesmas listas em CSV (abrem no Excel) |
| `scripts/` | Scripts em Python para refazer ou atualizar a pesquisa |

## Método

1. **Coleta:** todos os Projetos de Lei de 1991 a 2026 pelo webservice de dados abertos da Câmara (28.212 PLs).
2. **Recorte temático:** palavras-chave na ementa e nos assuntos indexados (mulher, feminicídio, Maria da Penha, violência doméstica, assédio, importunação sexual, estupro, gestante, parto, maternidade, aborto, menstruação, gênero, machismo etc.). Foram 1.575 candidatos, todos revisados à mão. As listas de inclusão e exclusão estão documentadas em `scripts/selecionar.py`.
3. **Verificação individual:** ficha "Detalhado" de cada um dos 779 projetos selecionados (pareceres das comissões, veto, lei gerada, encerramento).
4. **Exclusões (pedido do usuário):** projetos encerrados por ilegalidade/inconstitucionalidade (art. 79 do RI); com parecer da CCJ **aprovado** pela ilegalidade/inconstitucionalidade; apensados, com proposta de apensamento do relator da CCJ ou de igual teor a outro (art. 212 do RI).
5. **Inteiro teor:** OCR do PDF do texto inicial dos projetos em tramitação (os PDFs da Câmara não permitem copiar o texto).

## Recorte adotado

- **Incluídos:** violência contra a mulher, assédio e violência sexual, segurança, saúde da mulher, gestação/parto/puerpério, aborto legal e projetos contrários a ele, dignidade menstrual, mães solo e atípicas, trabalho e renda, participação política e equidade de gênero.
- **Fora do recorte:** nomes de logradouros, declarações de utilidade pública, projetos só sobre crianças ou recém-nascidos, pauta LGBTQIA+ sem recorte específico de mulheres e medidas gerais de acessibilidade em que a gestante aparece só nos assuntos indexados.

## Cuidados

- A transcrição por OCR pode ter erros pontuais. **Confira o PDF oficial**, linkado em cada arquivo, antes de citar.
- O texto transcrito é o **texto inicial**. Emendas e substitutivos aparecem apenas como link.
- A classificação por tema é automática e serve para facilitar a busca.
- Projetos de lei são atos oficiais, sem proteção de direito autoral (Lei nº 9.610/1998, art. 8º, IV). Trechos de obras de terceiros eventualmente citados nas justificativas continuam pertencendo a seus autores.
