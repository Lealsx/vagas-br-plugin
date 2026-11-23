---
name: buscar-vagas
description: >
  Use quando o usuário pedir "acha vagas pra mim", "busca vagas", "tem vaga nova?", "vagas de hoje",
  "procura vaga de <cargo> em <cidade>", "vagas no LinkedIn / Gupy / Catho / Indeed / InfoJobs /
  Vagas.com", ou rodar /buscar-vagas. Encontra vagas publicadas recentemente no Brasil que
  combinam com o perfil do usuário e devolve uma lista ranqueada com links que funcionam.
  Também busca em Portugal ("vagas em Portugal / Lisboa / ITJobs / Net-Empregos") se o perfil incluir esse mercado.
---

# Buscar vagas (Brasil e Portugal)

Responda sempre em português do Brasil.

## Passo 1: carregar o perfil

Leia `~/vagas/perfil.md`. Se não existir, siga a skill **perfil** antes de continuar.
Confirme em uma linha: "Buscando <cargos> em <cidade/remoto>, <regime>, últimos <N> dias."
Se o usuário pediu algo diferente nesta mensagem (outro cargo, outra cidade), use o pedido dele.

## Passo 2: buscar

Veja no `perfil.md` quais são os **mercados** do usuário (Brasil, Portugal ou os dois).
- Brasil: leia `references/fontes-br.md`. Use sempre o LinkedIn e a Gupy, e mais as fontes da área.
- Portugal: leia `references/fontes-pt.md`. Use sempre o LinkedIn e o ITJobs.pt (se for TI), e mais
  o Net-Empregos ou o Indeed PT. Confira o visto e a exigência de residência, como explicado lá.

- Por padrão, procure vagas dos **últimos 3 dias**. Se o usuário pedir outro período, use o dele.
- Use **pelo menos 2 fontes por mercado**.
- Para cada cargo-alvo, faça buscas com variações de nome (ex.: "Assistente Administrativo",
  "Auxiliar Administrativo"; "Desenvolvedor Front-end", "Front-end Developer").
- Abra a página da vaga para confirmar: o link funciona, a vaga está aberta e a data é recente.
  Vaga sem data confirmada entra com "data não confirmada".

## Passo 3: filtrar e pontuar

Descarte:
- duplicatas (mesma empresa + mesmo cargo em sites diferentes: fique com o link da própria empresa ou da Gupy);
- vagas encerradas;
- empresas da lista "evitar" do perfil;
- modalidade ou regime incompatíveis com o perfil;
- anúncios suspeitos: cobram taxa, pedem dados bancários, salário alto demais para o cargo, contato
  só por WhatsApp pessoal. Avise o usuário quando descartar por isso.

Dê uma nota de compatibilidade de **0 a 100**:
- 50 pts: requisitos obrigatórios que o currículo comprova;
- 20 pts: senioridade compatível;
- 15 pts: local / modalidade / regime;
- 15 pts: requisitos desejáveis.

## Passo 4: entregar

Salve em `~/vagas/saida/vagas-AAAA-MM-DD.md` e mostre no chat:

Separe em uma tabela por mercado (🇧🇷 Brasil, 🇵🇹 Portugal):

| # | Nota | Cargo | Empresa | Local / modalidade | Regime | Idioma | Visto* | Publicada | Link |
|---|------|-------|---------|--------------------|--------|--------|--------|-----------|------|

\* Coluna "Visto" só na tabela de Portugal. Numere em sequência nas duas tabelas (1, 2, 3...),
para o usuário poder pedir "adapta pra vaga 7".

Embaixo da tabela, para as 3 melhores, escreva uma linha: "por que combina" e "o que falta".

Termine oferecendo: "Quer que eu adapte o currículo para alguma? É só dizer o número."

## Regras

- Nunca invente vaga, link, salário ou data. Se não achou nada, diga isso e sugira ampliar
  (mais dias, cargo parecido, remoto).
- Não se candidate e não envie nada em nome do usuário.
- Respeite os sites: poucas requisições, sem tentar burlar login ou captcha. Se um site bloquear,
  pule para o próximo e avise.
