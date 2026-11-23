---
name: candidaturas
description: >
  Use quando o usuário disser "me candidatei na X", "registra essa candidatura", "fui chamado pra
  entrevista", "recebi retorno", "fui reprovado", "recebi proposta", "como estão minhas
  candidaturas?", "quem eu preciso cobrar?", "o que tenho essa semana?", ou rodar /candidaturas.
  Mantém o controle das candidaturas em ~/vagas/candidaturas.md e diz o que fazer a seguir.
---

# Controle de candidaturas

Responda sempre em português do Brasil. Arquivo: `~/vagas/candidaturas.md`. Crie se não existir.

## Formato do arquivo

```markdown
# Candidaturas

| # | Empresa | Cargo | País | Fonte | Link | Data | Etapa | Próximo passo | Data do próximo passo | Contato | CV usado | Notas |
|---|---------|-------|------|-------|------|------|-------|---------------|-----------------------|---------|----------|-------|
```

**Etapas** (use sempre estes nomes): `Para enviar` → `Enviada` → `Triagem/teste` → `Entrevista RH`
→ `Entrevista técnica` → `Entrevista final` → `Proposta` → `Aceita` | `Recusada por mim` |
`Reprovado` | `Sem resposta`.

## Ações

- **Registrar**: preencha com o que o usuário disse e com o que já existe. Use a vaga da última
  busca (`~/vagas/saida/vagas-*.md`) e o CV adaptado (`~/vagas/saida/...`). A data padrão é hoje.
  Pergunte só o que for essencial e estiver faltando (empresa e cargo).
- **Atualizar**: ache a linha pela empresa e/ou pelo cargo. Se houver mais de uma, pergunte qual. Mude a
  etapa, o próximo passo e a data, e acrescente nas Notas o que aconteceu, com a data.
- **Panorama** ("como estão minhas candidaturas?"):
  1. **Para hoje e atrasados**: o próximo passo vence hoje ou já venceu.
  2. **Cobrar**: `Enviada` há mais de 7 dias sem retorno, ou entrevista feita há mais de 5 dias sem
     resposta. Ofereça a mensagem de follow-up (skill carta-e-mensagem).
  3. **Marcar como "Sem resposta"**: `Enviada` há mais de 30 dias. Pergunte antes de mudar.
  4. Números: total, por etapa e taxa de resposta (passaram de `Enviada` ÷ total enviadas).

## Regras

- Datas no formato `AAAA-MM-DD`.
- Nunca apague uma linha. Encerrar é mudar a etapa.
- Antes de editar o arquivo, mostre a linha como vai ficar se a mudança for grande (várias linhas
  de uma vez).
- Para entrevista marcada: no próximo passo, coloque "Entrevista <tipo>" com a data, e ofereça ajuda para se
  preparar (perguntas prováveis a partir da vaga + histórias do currículo).
