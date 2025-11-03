"""
backend.py

Módulo de funções de processamento de dados tabulares para o projeto Hayslla.

Este arquivo concentra funções utilitárias que podem ser reutilizadas por diferentes fluxos,
tais como: extração de tabelas HTML, tratamento de dados, padronização e conversões.

Ideal para centralizar regras e evitar duplicidade de código.
"""

import pandas as pd
from bs4 import BeautifulSoup

def extrair_tabela_html_vendas(arquivo_html):
    """
    Extrai e converte tabela de um arquivo HTML de vendas para DataFrame pandas.

    Parâmetros:
        arquivo_html (str): Caminho do arquivo HTML a ser processado.

    Retorno:
        pd.DataFrame: Dados extraídos da tabela ou None se não houver dados válidos.

    Lógica:
    - Abre arquivo como texto
    - Usa BeautifulSoup para buscar primeira tabela
    - Usa cabeçalho da primeira linha, (<th> ou <td>)
    - Exclui as 3 últimas linhas do corpo
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
    cabecalho = [cel.get_text(strip=True) for cel in linhas[0].find_all("th")]
    if not cabecalho:
        cabecalho = [cel.get_text(strip=True) for cel in linhas[0].find_all("td")]
    dados = []
    for linha in linhas[1:-3]:
        celulas = [cel.get_text(strip=True) for cel in linha.find_all("td")]
        if len(celulas) == len(cabecalho):
            dados.append(celulas)
    if not dados:
        return None
    df = pd.DataFrame(dados, columns=cabecalho)
    return df

def extrair_tabela_html_bancaria(arquivo_html):
    """
    Extrai e converte movimentações bancárias de HTML para DataFrame, já descartando linhas "sujas".

    Parâmetros:
        arquivo_html (str): Caminho do arquivo HTML a ser processado.

    Retorno:
        pd.DataFrame: Dados extraídos da tabela ou None se não houver dados válidos.

    Lógica:
    - Abre arquivo, busca primeira tabela
    - Descarta 5 primeiras e 7 últimas linhas (incluindo cabeçalho original sujo)
    - Usa cabeçalho fixo via lista
    - Retorna somente linhas válidas para análise
    """
    cabecalho = [
        "Tipo", "Categoria", "Data", "Valor", "Saldo",
        "Observação", "Usuário", "Núm. Fato", "Data/Hora Registro"
    ]
    with open(arquivo_html, "r", encoding="latin-1") as f:
        html_content = f.read()
    soup = BeautifulSoup(html_content, "html.parser")
    tabela = soup.find("table")
    if not tabela:
        return None
    linhas = tabela.find_all("tr")
    if len(linhas) <= 12:
        return None
    linhas_validas = linhas[5:-7]
    dados = []
    for linha in linhas_validas:
        celulas = [cel.get_text(strip=True) for cel in linha.find_all("td")]
        if len(celulas) == len(cabecalho):
            dados.append(celulas)
    if not dados:
        return None
    df = pd.DataFrame(dados, columns=cabecalho)
    return df
