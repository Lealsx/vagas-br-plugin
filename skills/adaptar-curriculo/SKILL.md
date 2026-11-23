---
name: adaptar-curriculo
description: >
  Use quando o usuário pedir "adapta meu currículo pra essa vaga", "ajusta meu CV", "personaliza o
  currículo", "coloca as palavras-chave da vaga", "deixa meu currículo amigável pra ATS / Gupy",
  "qual minha compatibilidade com essa vaga", ou rodar /adaptar-curriculo com um link, o número de
  uma vaga da última busca ou o texto da vaga colado. Gera um currículo adaptado (DOCX + PDF) e um
  relatório de compatibilidade, sem inventar nada.
---

# Adaptar currículo para uma vaga

Responda sempre em português do Brasil. Saída: `~/vagas/saida/<Nome>_<Empresa>_<Cargo>.docx` e
`.pdf`, mais `...-relatorio.md`.

## Entradas

1. **Vaga**: o número de uma vaga do `~/vagas/saida/vagas-*.md` mais recente, um link (abra a página)
   ou o texto colado.
2. **Currículo mestre**: de preferência `~/vagas/curriculo-mestre.json`, no mesmo formato do
   `scripts/estrutura.md`. Parta de uma **cópia** dele. Se não houver JSON, use o caminho que está no
   `~/vagas/perfil.md`. Se o perfil não existir, rode a skill **perfil** antes. **Nunca edite o
   currículo mestre** a não ser que o usuário peça explicitamente para corrigir o mestre.

## Passo 0: dependências (só na primeira vez)

Rode `python3 ${CLAUDE_PLUGIN_ROOT}/skills/adaptar-curriculo/scripts/montar_curriculo.py --checar`.
Se faltar alguma coisa, o script mostra o comando de instalação. Repasse o comando ao usuário para
ele rodar com `!` no prompt (ele precisa de `sudo`). Não instale nada com `pip --break-system-packages`.

## Idioma do currículo gerado

O currículo sai **no idioma da vaga**:
- vaga em português do Brasil → PT-BR;
- vaga em português de Portugal → **PT-PT** ("licenciatura", "candidatura", "equipa", "utilizador",
  "telemóvel"); use o telefone no formato internacional (+55 ...) e informe a situação de visto ou
  cidadania se o perfil tiver essa informação;
- vaga em inglês → inglês (títulos de seção em inglês via `titulos_secoes`).

Ao traduzir, é só tradução: nenhum fato novo e nenhum nível de idioma aumentado.

## Passo 1: analisar a vaga

Leia `references/palavras-chave.md`. Separe os termos em três grupos:
- **Obrigatórios**: estão em "requisitos" ou "o que esperamos", aparecem 2 vezes ou mais, ou estão no título.
- **Desejáveis**: "diferencial", "será um plus", "desejável".
- **Contexto**: setor, ferramentas, metodologias, comportamentais ("trabalho em equipe", "comunicação").

Anote a **grafia exata** que a vaga usa ("Excel avançado", "Power BI", "Node.js", "CNH B", "Pacote Office").

## Passo 2: comparar com o currículo mestre

Classifique cada termo:
- **Presente**: já está no currículo com a mesma grafia.
- **Presente com outras palavras**: a pessoa tem, mas escreveu diferente → reescreva usando o termo da vaga.
- **Adjacente**: tem algo parecido (sabe Google Sheets e a vaga pede Excel) → **não** coloque o
  termo da vaga no currículo. Leve para o relatório com uma sugestão honesta de frase.
- **Ausente**: não tem → só no relatório, como lacuna.

## Passo 3: montar o conteúdo adaptado

Leia `references/regras-ats.md` e `scripts/estrutura.md`. Gere um JSON nesse formato em
`~/vagas/saida/<base>.json`.

O que pode fazer:
- Reescrever o **resumo** (3 a 4 linhas) mirando no cargo da vaga, só com fatos do mestre.
- Reordenar habilidades e tópicos, com o mais relevante para a vaga primeiro.
- Trocar sinônimos pela grafia da vaga quando for a mesma coisa.
- Esconder tópicos pouco relevantes se o currículo passar de 2 páginas (1 página para estágio e júnior).
- Manter a ordem das seções e o estilo do mestre (anotados no `perfil.md`).

O que não pode fazer:
- Inventar cargo, empresa, data, curso, certificação, número ou ferramenta.
- Aumentar nível de idioma ou de senioridade.
- Tirar ou enfraquecer métricas que já existem.
- Colocar foto, idade, estado civil, CPF, RG ou endereço completo (cidade/UF basta).

## Passo 4: gerar os arquivos

```
python3 ${CLAUDE_PLUGIN_ROOT}/skills/adaptar-curriculo/scripts/montar_curriculo.py \
  ~/vagas/saida/<base>.json ~/vagas/saida/<base>
```

Se o PDF não for gerado (sem LibreOffice), avise o usuário. Ele pode abrir o DOCX e exportar o PDF,
ou instalar o LibreOffice com `! sudo pacman -S libreoffice-fresh`.

Com o PDF gerado, rode a checagem de ATS:

```
python3 ${CLAUDE_PLUGIN_ROOT}/skills/adaptar-curriculo/scripts/verificar_ats.py \
  ~/vagas/saida/<base>.pdf --palavras "<obrigatórios presentes, separados por vírgula>" --paginas 2
```

Corrija e gere de novo até passar. Se passar de 2 páginas, use `"compacto": true` no JSON.

## Passo 5: relatório

Salve `~/vagas/saida/<base>-relatorio.md` e mostre um resumo no chat:

```
Compatibilidade: XX/100 (antes: YY/100)

✅ Obrigatórios atendidos: ...
✏️ Reescritos com o termo da vaga: "X" → "Y"
⚠️ Adjacentes (não colocados): Excel → você tem Google Sheets. Sugestão: "Planilhas (Google Sheets; ...)"
❌ Lacunas: ...  → como estudar ou comprovar rápido (curso curto, projeto)
📄 Arquivos: caminho do DOCX e do PDF
```

Termine oferecendo: "Quer a carta de apresentação e a mensagem pro recrutador também?" (skill
carta-e-mensagem) e "Quer que eu registre essa candidatura?" (skill candidaturas).
