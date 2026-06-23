#!/usr/bin/env python3
"""
consolidar_profissional.py

Lê todos os arquivos .md da pasta de fichas de contatos profissionais
do sistema EMM, extrai o nome da nota e seu frontmatter YAML, e gera
um arquivo consolidado_profissional.txt com tudo em sequência alfabética.

Uso:
    python3 consolidar_profissional.py

Caminhos configurados:
    Entrada : /home/arthur/obsidian/02-Areas/sistema-emm/profissional-emm/arquivo
    Saída   : /home/arthur/Downloads/00-Arquivo-EMM/consolidado_profissional.txt
"""

import os
import re

PASTA_ENTRADA = "/home/arthur/obsidian/02-Areas/sistema-emm/profissional-emm/arquivo"
ARQUIVO_SAIDA = "/home/arthur/Downloads/00-Arquivo-EMM/consolidado_profissional.txt"


def extrair_frontmatter(conteudo: str) -> str | None:
    """
    Extrai o bloco frontmatter YAML (entre os delimitadores ---).
    Retorna a string do bloco incluindo os delimitadores, ou None
    se não houver frontmatter.
    """
    padrao = re.compile(r"^---\s*\n(.*?)\n---", re.DOTALL)
    match = padrao.match(conteudo.lstrip("\ufeff"))  # remove BOM se houver
    if match:
        return "---\n" + match.group(1) + "\n---"
    return None


def nome_da_nota(nome_arquivo: str) -> str:
    """Remove a extensão .md do nome do arquivo."""
    return os.path.splitext(nome_arquivo)[0]


def main():
    # Verifica se a pasta de entrada existe
    if not os.path.isdir(PASTA_ENTRADA):
        print(f"[ERRO] Pasta não encontrada: {PASTA_ENTRADA}")
        return

    # Lista e ordena alfabeticamente apenas os arquivos .md
    arquivos = sorted(
        [f for f in os.listdir(PASTA_ENTRADA) if f.endswith(".md")],
        key=lambda x: x.lower()
    )

    if not arquivos:
        print("[AVISO] Nenhum arquivo .md encontrado na pasta.")
        return

    linhas_saida = []

    for nome_arquivo in arquivos:
        caminho = os.path.join(PASTA_ENTRADA, nome_arquivo)
        nota = nome_da_nota(nome_arquivo)

        with open(caminho, "r", encoding="utf-8") as f:
            conteudo = f.read()

        frontmatter = extrair_frontmatter(conteudo)

        if frontmatter:
            linhas_saida.append(nota)
            linhas_saida.append(frontmatter)
            linhas_saida.append("")  # linha em branco entre entradas
            print(f"[OK] {nome_arquivo}")
        else:
            print(f"[AVISO] Sem frontmatter: {nome_arquivo} — nota ignorada.")

    # Garante que a pasta de saída existe
    os.makedirs(os.path.dirname(ARQUIVO_SAIDA), exist_ok=True)

    # Escreve o arquivo consolidado
    with open(ARQUIVO_SAIDA, "w", encoding="utf-8") as f:
        f.write("\n".join(linhas_saida))

    print(f"\n✅ Consolidado gerado em: {ARQUIVO_SAIDA}")
    print(f"   {len(arquivos)} nota(s) processada(s).")


if __name__ == "__main__":
    main()
