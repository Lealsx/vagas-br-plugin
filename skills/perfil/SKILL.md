---
name: perfil
description: >
  Use quando o usuário pedir "cria meu perfil", "lê meu currículo", "configura minha busca de vagas",
  "atualiza meu perfil", "mudei de área", ou rodar /perfil. Lê o currículo mestre e cria ou atualiza
  ~/vagas/perfil.md, que as outras skills do vagas-br usam (buscar-vagas, adaptar-curriculo,
  carta-e-mensagem). Também é chamada pelas outras skills quando o perfil ainda não existe.
---

# Perfil do candidato

Responda sempre em português do Brasil.

## Onde ficam os dados

Tudo o que é pessoal fica em `~/vagas/` e **nunca** no repositório do plugin:

```
~/vagas/
├── curriculo-mestre.json       # fonte da verdade (formato de adaptar-curriculo/scripts/estrutura.md)
├── curriculo-mestre.pdf|docx   # gerado a partir do JSON
├── curriculo-original.pdf      # backup do CV como veio do usuário
├── perfil.md                   # criado por esta skill
├── candidaturas.md             # usado pela skill candidaturas
└── saida/                      # currículos, cartas e relatórios gerados
```

Crie as pastas que faltarem.

## Passo 1: achar o currículo mestre

1. Se o usuário passou um arquivo, use esse.
2. Senão, procure `~/vagas/curriculo-mestre.*`.
3. Se não achar nenhum, peça o caminho. Se a pessoa ainda não tem currículo, ofereça montar um
   conversando (cargo, experiências, formação, habilidades, idiomas) e salve como
   `~/vagas/curriculo-mestre.md`.

Quando o arquivo vier de outro lugar, guarde uma cópia como `~/vagas/curriculo-original.<ext>`.
Se ainda não existir `~/vagas/curriculo-mestre.json`, converta o CV para esse formato
(`adaptar-curriculo/scripts/estrutura.md`) **sem mudar fatos**, mostre ao usuário e salve depois da
confirmação. Links clicáveis do PDF podem ser extraídos com pypdf (`/Annots` → `/URI`). Se o texto
e o link divergirem (ex.: dois e-mails diferentes), pergunte qual é o certo.

Para ler: PDF com `pdftotext arquivo.pdf -`, DOCX com `python3 -c` + `python-docx`.

## Passo 2: escrever ~/vagas/perfil.md

Extraia só o que está escrito no currículo. Pergunte o que faltar, **numa única pergunta**:

```markdown
# Perfil
- Nome:
- Cargo atual / último cargo:
- Cargos-alvo (2 a 4):            # derive da trajetória e confirme
- Área:                           # ex.: tecnologia, administrativo, vendas, saúde...
- Senioridade:                    # estágio, júnior, pleno, sênior
- Tempo de experiência:
- Habilidades principais (10–15):
- Idiomas e nível:
- Cidade / estado:
- Mercados:                       # Brasil, Portugal (ou os dois)
- Cidadania / autorização de trabalho na UE:   # importante para vagas em Portugal
- Modalidade aceita:              # presencial, híbrido, remoto
- Regime aceito:                  # CLT, PJ, estágio, temporário
- Pretensão salarial:             # opcional; não inventar
- Disponibilidade para início:
- Empresas a evitar:
- Currículo mestre: ~/vagas/curriculo-mestre.<ext>

## Estilo do currículo mestre
- Ordem e nome das seções:
- Formato dos tópicos (ex.: verbo + o que fez + resultado):
- Números/métricas que aparecem:
```

## Passo 3: confirmar

Mostre o perfil em poucas linhas e pergunte se está certo. Salve só depois do "sim" ou das correções.

## Regras

- Nunca inventar experiência, número, curso ou nível de idioma.
- Pretensão salarial e empresas a evitar são opcionais. Não insista nelas.
