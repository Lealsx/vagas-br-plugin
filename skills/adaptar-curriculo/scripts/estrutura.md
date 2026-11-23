# Formato do JSON para montar_curriculo.py

```json
{
  "nome": "Nome Sobrenome",
  "titulo": "Assistente Administrativo | Excel · Atendimento · Rotinas Financeiras",
  "contato": ["(11) 91234-5678", "email@exemplo.com", "São Paulo/SP", "linkedin.com/in/usuario"],
  "resumo": "Parágrafo de 3 a 4 linhas.",
  "experiencia": [
    {"cargo": "Auxiliar Administrativo", "empresa": "Empresa X", "local": "São Paulo/SP",
     "periodo": "mar/2023 – atual", "topicos": ["...", "..."]}
  ],
  "formacao": [
    {"curso": "Tecnólogo em Gestão Financeira", "instituicao": "Faculdade Y",
     "periodo": "2021 – 2023", "detalhes": "Concluído"}
  ],
  "habilidades": [ {"rotulo": "Ferramentas", "itens": "Excel avançado, Power BI, SAP"} ],
  "idiomas": ["Inglês: intermediário", "Espanhol: básico"],
  "projetos": [ {"nome": "Site do brechó", "tecnologias": "Vite, GSAP", "link": "github.com/usuario/repo", "topicos": ["..."]} ],
  "cursos": ["Excel Avançado – Fundação Bradesco (2024)"],
  "conquistas": ["..."],
  "titulos_secoes": {"habilidades": "Competências Técnicas"},
  "ordem": ["resumo", "experiencia", "formacao", "habilidades", "idiomas", "cursos", "projetos", "conquistas"],
  "compacto": false
}
```

- Só `nome` e `contato` são obrigatórios. Seções vazias são puladas.
- `formacao` também aceita itens como texto simples.
- `titulos_secoes` troca o título de uma seção, para manter o nome que o mestre usa.
- `ordem` define a ordem das seções. Para estágio e primeiro emprego, coloque `formacao` e
  `projetos` antes de `experiencia`.
- `"compacto": true` diminui margens, espaços e fonte para caber em menos páginas.
