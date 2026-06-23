# 💼 Consolidador de Fichas Profissionais do Obsidian

Script Python para varrer uma pasta de fichas de contatos profissionais do Obsidian, extrair os metadados (frontmatter YAML) de cada nota e consolidar tudo em um único arquivo de texto estruturado, ordenado alfabeticamente.

---

## Sumário

- [Contexto e Motivação](#contexto-e-motivação)
- [Como funciona a pasta de Profissionais no Obsidian](#como-funciona-a-pasta-de-profissionais-no-obsidian)
- [Estrutura esperada das notas](#estrutura-esperada-das-notas)
- [Campos suportados no frontmatter](#campos-suportados-no-frontmatter)
- [Instalação](#instalação)
- [Como usar](#como-usar)
- [Explicação detalhada do código](#explicação-detalhada-do-código)
- [Exemplo de saída](#exemplo-de-saída)
- [Limitações e próximos passos](#limitações-e-próximos-passos)

---

## Contexto e Motivação

Em sistemas de gestão de conhecimento pessoal (PKM) construídos no Obsidian, é comum manter fichas individuais para contatos profissionais — clientes, parceiros, fornecedores, recrutadores, colegas de mercado. Cada ficha é um arquivo Markdown com metadados estruturados no frontmatter YAML: cargo, empresa, canal de contato, última interação, área de atuação, entre outros.

Com dezenas ou centenas dessas fichas, obter uma visão consolidada de toda a rede profissional se torna inviável manualmente. Este script resolve isso: varre a pasta inteira, extrai o frontmatter de cada ficha e gera um único arquivo ordenado alfabeticamente — ideal para revisões rápidas, prospecção, preparação para reuniões ou análise por IA.

---

## Como funciona a pasta de Profissionais no Obsidian

As fichas profissionais costumam ficar em uma pasta plana, com um arquivo `.md` por contato:

```
Profissional/
├── Carlos Andrade.md
├── Fernanda Costa.md
├── João Silva.md
└── ...
```

O nome do arquivo é o identificador principal do contato e será usado como título no arquivo consolidado.

> O script processa **apenas** arquivos `.md` na raiz da pasta informada. Subpastas são ignoradas.

---

## Estrutura esperada das notas

Cada ficha profissional deve ter um bloco de frontmatter YAML no início, delimitado por `---`:

```markdown
---
nome_completo: João Silva
cargo: Desenvolvedor Sênior
empresa: TechCorp
area: Engenharia de Software
email: joao@techcorp.com
linkedin: linkedin.com/in/joaosilva
telefone: +55 11 98888-0000
cidade: São Paulo
como_conheceu: Indicação de Carlos Andrade
ultima_interacao: 2026-05-10
status: ativo
tags: [backend, python, parceiro]
notas_rapidas: Especialista em APIs. Aberto a freelas. Prefere contato por LinkedIn.
---

## Histórico

- **2026-05-10** — Conversa sobre oportunidade de projeto...
```

O script extrai apenas o frontmatter — o corpo da nota é ignorado.

---

## Campos suportados no frontmatter

O script é **agnóstico aos campos**: extrai **todos** os pares `chave: valor` presentes em cada frontmatter, sem lista pré-definida. Isso garante total flexibilidade — cada ficha pode ter seus próprios campos conforme o contexto profissional.

Exemplos de campos comuns em fichas profissionais:

| Campo | Descrição |
|-------|-----------|
| `nome_completo` | Nome completo do contato |
| `cargo` | Cargo ou função atual |
| `empresa` | Empresa ou organização |
| `area` | Área de atuação (ex: Engenharia, Comercial, Design) |
| `email` | Endereço de e-mail profissional |
| `linkedin` | URL do perfil no LinkedIn |
| `telefone` | Telefone de contato |
| `cidade` | Cidade onde atua |
| `como_conheceu` | Contexto do primeiro contato |
| `ultima_interacao` | Data da interação mais recente |
| `status` | Estado do relacionamento (ex: ativo, dormente, prospect) |
| `tags` | Categorias, especialidades ou grupos |
| `notas_rapidas` | Observações rápidas e contextuais |

---

## Instalação

Nenhuma dependência externa. O script usa apenas a biblioteca padrão do Python 3.

**Requisitos:**
- Python 3.10 ou superior (usa a sintaxe `str | None` para type hints)

**Clone o repositório:**
```bash
git clone https://github.com/seu-usuario/consolidador-profissional-obsidian-python.git
cd consolidador-profissional-obsidian-python
```

---

## Como usar

```
python consolida_profissional.py <pasta_entrada> <arquivo_saida>
```

### Argumentos

| Argumento | Obrigatório | Descrição |
|-----------|-------------|-----------|
| `pasta_entrada` | ✅ | Caminho para a pasta com as fichas `.md` dos contatos profissionais |
| `arquivo_saida` | ✅ | Caminho completo para o arquivo consolidado a ser gerado |

### Validações automáticas

O script verifica antes de processar:
- Se a `pasta_entrada` existe e é um diretório válido
- Se o **diretório pai** do `arquivo_saida` existe — a pasta de destino deve existir previamente; o script não a cria automaticamente

### Exemplos

```bash
# Consolida todas as fichas profissionais
python consolida_profissional.py ~/Obsidian/Profissional ~/Downloads/consolidado_profissional.txt

# Com caminho absoluto
python consolida_profissional.py /mnt/cofre/02-Areas/Profissional /home/usuario/Downloads/profissional.md

# Saída temporária para teste
python consolida_profissional.py ~/Obsidian/Profissional /tmp/profissional_test.txt
```

### Saída esperada no terminal

```
Encontrados 63 arquivo(s) .md. Processando...

  [OK] Carlos Andrade.md
  [OK] Fernanda Costa.md
  [AVISO] Sem frontmatter: modelo-ficha.md — nota ignorada.
  [OK] João Silva.md
  ...

✅ Consolidado gerado com sucesso!
   Arquivo: /home/usuario/Downloads/consolidado_profissional.txt
   Fichas processadas: 62
   Fichas ignoradas (sem frontmatter): 1
```

---

## Explicação detalhada do código

O script está organizado em quatro funções com responsabilidades bem separadas:

### `extrair_frontmatter(conteudo)`
Usa uma expressão regular pré-compilada com `re.DOTALL` para capturar o bloco entre os dois delimitadores `---` no início do arquivo. Ponto importante: aplica `.lstrip("\ufeff")` para remover o **BOM (Byte Order Mark)** — um caractere invisível que editores Windows podem inserir no início de arquivos UTF-8 e que quebraria silenciosamente o regex sem esse tratamento.

```python
padrao = re.compile(r"^---\s*\n(.*?)\n---", re.DOTALL)
match = padrao.match(conteudo.lstrip("\ufeff"))
```

Usa `.match()` em vez de `.search()` porque o frontmatter **deve** estar no início do arquivo — isso evita falsos positivos com blocos `---` no meio do conteúdo da nota.

### `nome_da_nota(nome_arquivo)`
Remove a extensão `.md` usando `os.path.splitext()`, retornando o nome limpo do contato. Ex: `'João Silva.md'` → `'João Silva'`.

### `validar_argumentos(pasta_entrada, arquivo_saida)`
Centraliza a validação dos caminhos antes de qualquer operação de I/O:
- Verifica se `pasta_entrada` é um diretório existente com `os.path.isdir()`
- Verifica se o **diretório pai** do `arquivo_saida` existe, usando `os.path.dirname(os.path.abspath(...))` para converter caminhos relativos antes da verificação
- Encerra com `sys.exit(1)` e mensagem clara em caso de falha

### `main()`
Orquestra todo o fluxo:

1. **argparse** configura os dois argumentos posicionais obrigatórios com geração automática de `--help`
2. `os.path.expanduser()` converte `~` para o home do usuário antes da validação
3. `sorted(..., key=lambda x: x.lower())` garante ordenação **case-insensitive** — `'ana.md'` vem antes de `'Bruno.md'`
4. Fichas sem frontmatter são **ignoradas com aviso**, sem interromper o processamento
5. Contadores separados de `processados` e `ignorados` compõem o resumo final

---

## Exemplo de saída

```
Carlos Andrade
---
nome_completo: Carlos Andrade
cargo: Gerente de Contas
empresa: Distribuidora Norte
area: Comercial
email: carlos@distrnorte.com.br
linkedin: linkedin.com/in/carlosandrade
ultima_interacao: 2026-03-22
status: ativo
tags: [comercial, parceiro, indicacao]
---

Fernanda Costa
---
nome_completo: Fernanda Costa
cargo: UX Designer
empresa: Agência Pixel
area: Design
email: fernanda@agenciapixel.com
status: prospect
notas_rapidas: Portfólio excelente. Aberta a projetos remotos.
---

João Silva
---
nome_completo: João Silva
cargo: Desenvolvedor Sênior
empresa: TechCorp
...
---
```

---

## Limitações e próximos passos

- **Parser YAML simples:** o frontmatter é extraído como bloco de texto — não há parse dos valores individuais. Para filtrar por campo, exportar para CSV ou JSON, seria necessário usar `PyYAML`.
- **Sem recursão em subpastas:** apenas arquivos `.md` na raiz da pasta informada são processados.
- **Encoding fixo em UTF-8:** arquivos em outras codificações precisarão de ajuste.

**Melhorias planejadas:**
- [ ] Exportação para CSV (útil para importar em planilhas ou ferramentas de CRM)
- [ ] Filtro por campo específico (ex: `--status ativo`, `--area Engenharia`)
- [ ] Suporte a subpastas com flag `--recursivo`
- [ ] Parser YAML completo com `PyYAML` para análise dos valores

---

## Licença

MIT — use, modifique e distribua à vontade.