"""
backend.py

Módulo de funções de processamento de dados tabulares para o projeto Hayslla.

Este arquivo concentra funções utilitárias que podem ser reutilizadas por diferentes fluxos,
tais como: extração de tabelas HTML, tratamento de dados, padronização e conversões.

Ideal para centralizar regras e evitar duplicidade de código.
"""

import pandas as pd
from bs4 import BeautifulSoup

def extrair_tabela_html(arquivo_html):
    """
    Extrai e converte uma tabela de um arquivo HTML exportado do Excel para um DataFrame pandas.

    Parâmetros:
        arquivo_html (str): Caminho do arquivo HTML a ser processado.

    Retorno:
        pd.DataFrame: Dados extraídos da tabela, ou None se não houver dados válidos.

    Lógica:
    - Abre o arquivo como texto
    - Utiliza BeautifulSoup para buscar a primeira tabela
    - Identifica o cabeçalho na primeira linha, seja usando <th> ou <td>
    - Exclui as 3 últimas linhas do corpo da tabela (geralmente contém rodapé ou células mescladas)
    - Retorna DataFrame com dados limpos para uso analítico
    """
    with open(arquivo_html, "r", encoding="latin-1") as f:
        html_content = f.read()
    soup = BeautifulSoup(html_content, "html.parser")
    tabela = soup.find("table")
    if not tabela:
        return None
    linhas = tabela.find_all("tr")
    if len(linhas) < 2:
        return None
    # Tenta extrair cabeçalho pelos <th>, senão pelo <td>
    cabecalho = [cel.get_text(strip=True) for cel in linhas[0].find_all("th")]
    if not cabecalho:
        cabecalho = [cel.get_text(strip=True) for cel in linhas[0].find_all("td")]
    dados = []
    # Começa na segunda linha e exclui as 3 últimas do corpo
    for linha in linhas[1:-3]:
        celulas = [cel.get_text(strip=True) for cel in linha.find_all("td")]
        # Só adiciona se número de células corresponde ao cabeçalho
        if len(celulas) == len(cabecalho):
            dados.append(celulas)
    if not dados:
        return None
    df = pd.DataFrame(dados, columns=cabecalho)
    return df
