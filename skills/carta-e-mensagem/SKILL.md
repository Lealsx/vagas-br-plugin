---
name: carta-e-mensagem
description: >
  Use quando o usuário pedir "escreve uma carta de apresentação", "carta pra essa vaga", "mensagem
  pro recrutador", "o que eu mando no LinkedIn", "texto pra pedir indicação", "mensagem de
  follow-up", ou rodar /carta-e-mensagem. Escreve uma carta de apresentação curta e mensagens para
  o recrutador (conexão no LinkedIn, InMail, pedido de indicação e follow-up) para uma vaga,
  usando só fatos do currículo.
---

# Carta de apresentação e mensagens para o recrutador

Responda em português do Brasil. O **texto gerado** sai no idioma da vaga: PT-BR, PT-PT ou inglês
(veja as regras de idioma na skill adaptar-curriculo).

## Entradas

- A vaga: número da última busca, link ou texto colado.
- `~/vagas/perfil.md` e o currículo mestre. Se existir, use também o currículo adaptado para essa
  vaga e o relatório dele em `~/vagas/saida/`.
- Nome do recrutador ou de um contato na empresa, se o usuário souber. Se não souber, use uma
  saudação neutra e não invente nome.

## O que gerar

### 1. Carta de apresentação (180 a 250 palavras)
1. **Abertura (1 a 2 frases)**: a vaga exata e por que *esta empresa*, com algo concreto da vaga ou
   da empresa. Nada de "venho por meio desta".
2. **Duas ou três evidências**: cada uma liga um requisito da vaga a um fato do currículo
   (projeto, experiência, resultado com número, se existir).
3. **Lacuna honesta (opcional)**: se faltar um requisito importante, uma frase mostrando o que é
   parecido e como está aprendendo.
4. **Fechamento**: disponibilidade para conversar (e para início ou mudança, se for Portugal) e despedida.

### 2. Mensagens curtas
- **Pedido de conexão no LinkedIn (até 300 caracteres)**: quem é, a vaga e um gancho.
- **InMail / e-mail para o recrutador (até 600 caracteres)**.
- **Pedido de indicação** para alguém da empresa (até 500 caracteres): fácil de dizer "sim", com o
  link da vaga.
- **Follow-up** (7 dias depois de se candidatar, até 400 caracteres).

Mostre a contagem de caracteres de cada mensagem.

## Estilo

- Frases curtas e diretas, voz ativa, sem clichês ("sou apaixonado por desafios", "proativo",
  "sinergia").
- Nunca inventar fato, número, nome de contato ou motivação pessoal. Se precisar de um motivo
  pessoal ("por que essa empresa?") e não houver nada no perfil, **pergunte**.
- Não usar o mesmo texto para empresas diferentes.

## Saída

Salve em `~/vagas/saida/<Nome>_<Empresa>_<Cargo>-carta.md` e mostre no chat.
**Não envie nada.** Quem copia e envia é o usuário.
Termine oferecendo registrar a candidatura (skill candidaturas).
