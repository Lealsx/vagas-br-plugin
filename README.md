# vagas-br: plugin do Claude Code para busca de emprego (Brasil 🇧🇷 + Portugal 🇵🇹)

Plugin em português que transforma o Claude Code num assistente de busca de emprego:

| Skill | O que faz | Como pedir |
|-------|-----------|------------|
| `perfil` | Lê seu currículo mestre e cria seu perfil de busca | "cria meu perfil" |
| `buscar-vagas` | Busca vagas recentes no LinkedIn, Gupy, Indeed, Catho, InfoJobs, ITJobs.pt, Net-Empregos... e dá nota de compatibilidade | "acha vagas pra mim" |
| `adaptar-curriculo` | Adapta o currículo para uma vaga (DOCX + PDF amigável a ATS) **sem inventar nada**, no idioma da vaga | "adapta meu currículo pra vaga 3" |
| `carta-e-mensagem` | Carta de apresentação + mensagens para o recrutador (LinkedIn, indicação, follow-up) | "escreve a carta pra essa vaga" |
| `candidaturas` | Controla suas candidaturas e diz quem cobrar | "me candidatei na X" / "como estão minhas candidaturas?" |

## Instalação

```bash
# dependências (Arch Linux)
sudo pacman -S python-docx python-pypdf poppler
sudo pacman -S libreoffice-fresh   # opcional: gera o PDF automaticamente
```

No Claude Code:

```
/plugin marketplace add Lealsx/vagas-br-plugin
/plugin install vagas-br@vagas-br-plugin
```

## Seus dados ficam fora do plugin

```
~/vagas/
├── curriculo-original.pdf # seu CV como você mandou (backup)
├── curriculo-mestre.json  # seu CV em formato estruturado: base de tudo
├── curriculo-mestre.pdf   # gerado a partir do JSON
├── perfil.md
├── candidaturas.md
└── saida/                 # currículos, cartas e listas de vagas geradas
```

## Princípios

- **Nunca inventa** experiência, número, curso ou nível de idioma. O que falta vira uma lacuna
  no relatório, nunca uma mentira no currículo.
- **Não envia nada por você.** Ele prepara o material e você revisa e envia.
- Descarta anúncios com cara de golpe (que cobram taxa, pedem dados bancários etc.).

## Créditos

Os scripts de montagem e verificação do currículo foram adaptados de
[job-hunt-copilot](https://github.com/chavan-omkar/job-hunt-copilot) (MIT, Omkar Chavan).
