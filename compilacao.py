import os
import pandas as pd # type: ignore
import glob
from bs4 import BeautifulSoup # type: ignore
import traceback

def extrair_dados_com_bs4(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    tabela = soup.find('table')
    if not tabela: return None
    todas_as_linhas = tabela.find_all('tr')
    if len(todas_as_linhas) < 4: return None
    linha_cabecalho = todas_as_linhas[3]
    cabecalho = [cel.get_text(strip=True) for cel in linha_cabecalho.find_all('td')]
    linhas_de_dados = todas_as_linhas[4:]
    dados = []
    for linha in linhas_de_dados:
        celulas = [cel.get_text(strip=True) for cel in linha.find_all('td')]
        if len(celulas) == len(cabecalho):
            dados.append(celulas)
    if not dados: return None
    dados_limpos = dados[:-3]
    df = pd.DataFrame(dados_limpos, columns=cabecalho)
    return df

def processar_dataframe_vendas(df):
    colunas_decimais = ['Custo Un.', 'Margem', 'Preço Un.', 'Tot. Custo (R$)', 'Sub-Total (R$)', 'Desconto (R$)', 'Tot. Venda (R$)', 'Lucro Tot. (R$)']
    if 'Margem' in df.columns:
        df['Margem'] = df['Margem'].astype(str).str.replace('%', '', regex=False)
    if 'Data' in df.columns:
        df['Data'] = pd.to_datetime(df['Data'], errors='coerce', dayfirst=True)
    if 'Qtd.' in df.columns:
        s_qtd = df['Qtd.'].astype(str).str.replace('.', '', regex=False).str.replace(',', '.', regex=False)
        df['Qtd.'] = pd.to_numeric(s_qtd, errors='coerce').fillna(0).astype(int)
    for col in colunas_decimais:
        if col in df.columns:
            s_decimal = df[col].astype(str).str.replace('.', '', regex=False).str.replace(r'[^\d,]', '', regex=True).str.replace(',', '.', regex=False)
            df[col] = pd.to_numeric(s_decimal, errors='coerce').fillna(0)
    return df

def compactar_historico_vendas(caminho_da_pasta_xls, callback_msg):
    try:
        caminho_pasta_final = os.path.join(caminho_da_pasta_xls, "Base_Pronta_Vendas")
        if not os.path.exists(caminho_pasta_final): os.makedirs(caminho_pasta_final)
        arquivos_xls = glob.glob(os.path.join(caminho_da_pasta_xls, "*.xls"))
        if not arquivos_xls:
            callback_msg("warning", "Nenhum arquivo .xls foi encontrado.")
            return

        nome_arquivo_csv = "historico_vendas.csv"
        caminho_novo_arquivo = os.path.join(caminho_pasta_final, nome_arquivo_csv)
        primeiro_arquivo = True

        for arquivo_xls in arquivos_xls:
            try:
                print(f"Processando: {os.path.basename(arquivo_xls)}")
                with open(arquivo_xls, 'r', encoding='latin-1') as f:
                    html_content = f.read()
                df_extraido = extrair_dados_com_bs4(html_content)
                if df_extraido is not None and not df_extraido.empty:
                    df_processado = processar_dataframe_vendas(df_extraido)
                    if primeiro_arquivo:
                        df_processado.to_csv(caminho_novo_arquivo, index=False, encoding='latin-1', sep=';', decimal=',', date_format='%d/%m/%Y', header=True)
                        primeiro_arquivo = False
                    else:
                        df_processado.to_csv(caminho_novo_arquivo, index=False, encoding='latin-1', sep=';', decimal=',', date_format='%d/%m/%Y', mode='a', header=False)
                else:
                    print(f"AVISO: Nenhuma tabela válida encontrada em {os.path.basename(arquivo_xls)}")
            except Exception as e:
                print(f"--- ERRO DETALHADO AO PROCESSAR: {os.path.basename(arquivo_xls)} ---")
                traceback.print_exc()

        if primeiro_arquivo:
            callback_msg("warning", "Nenhum dado válido foi processado de nenhum arquivo.")
        else:
            callback_msg("info", f"Compactação concluída!\n\nArquivo salvo em:\n{caminho_novo_arquivo}")

    except Exception as e:
        callback_msg("error", f"Ocorreu um erro geral: {e}")
