import os
import glob
import time
import pandas as pd
from datetime import datetime
from bs4 import BeautifulSoup

def extrair_tabela_html_vendas(arquivo_html):
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

def processar_vendas_backend(pasta_orig, update_callback):
    pasta_bruto = os.path.join(pasta_orig, "dados_brutos")
    pasta_tratado = os.path.join(pasta_orig, "dados_tratados")
    pasta_consolidado = os.path.join(pasta_orig, "historico_consolidado")
    arquivo_final = os.path.join(pasta_consolidado, "base_vendas.csv")
    log_path = os.path.join(pasta_orig, "log_tratamento_vendas.txt")
    for pasta in [pasta_tratado, pasta_consolidado]:
        if not os.path.exists(pasta):
            os.makedirs(pasta)
    update_callback(0.1, "Buscando arquivos de vendas...")
    arquivos = glob.glob(os.path.join(pasta_bruto, "Histórico de Vendas*.xls"))
    if not arquivos:
        raise Exception("Nenhum arquivo de vendas encontrado!")
    arquivos_logados = set()
    if os.path.exists(log_path):
        with open(log_path, "r", encoding="utf-8") as log_file:
            for linha in log_file:
                if "Nome do Relatório:" in linha:
                    nome = linha.split(":",1)[1].strip()
                    arquivos_logados.add(nome)
    bloco_data = datetime.now().strftime('%d/%m/%Y')
    novos_dfs = []
    start_total = time.time()
    arquivos_processados_hoje = False
    if os.path.exists(arquivo_final):
        df_base = pd.read_csv(arquivo_final, encoding="latin-1", sep=";", decimal=",")
    else:
        df_base = None
    update_callback(0.2, "Validando estrutura de dados...")
    total_arquivos = len(arquivos)
    arquivos_novos = [a for a in arquivos if os.path.splitext(os.path.basename(a))[0] + ".csv" not in arquivos_logados]
    with open(log_path, "a", encoding="utf-8") as log_file:
        for idx, arquivo in enumerate(arquivos):
            nome_csv = os.path.splitext(os.path.basename(arquivo))[0] + ".csv"
            if nome_csv in arquivos_logados:
                continue
            if not arquivos_processados_hoje:
                log_file.write(f"------ Tratamento do dia {bloco_data} ------\n\n")
                arquivos_processados_hoje = True
            progresso = 0.2 + (0.6 * (idx + 1) / total_arquivos)
            update_callback(progresso, f"Processando relatório de vendas ({idx+1}/{len(arquivos_novos)})...")
            inicio = time.time()
            hora = datetime.now().strftime('%H:%M:%S')
            df = extrair_tabela_html_vendas(arquivo)
            if df is not None and not df.empty:
                caminho_csv = os.path.join(pasta_tratado, nome_csv)
                df.to_csv(caminho_csv, index=False, encoding="latin-1", sep=";", decimal=",")
                tempo_gasto = time.time() - inicio
                novos_dfs.append(df)
                reg = (f"Horário: {hora}\nNome do Relatório: {nome_csv}\nQuantidade de linhas adicionadas: {len(df)}\nTempo: {tempo_gasto:.2f}s\n")
                log_file.write(reg + "\n")
            else:
                tempo_gasto = time.time() - inicio
                reg = (f"Horário: {hora}\nNome do Relatório: {nome_csv}\nQuantidade de linhas adicionadas: FALHA\nTempo: {tempo_gasto:.2f}s\n")
                log_file.write(reg + "\n")
        update_callback(0.85, "Consolidando histórico...")
        if novos_dfs:
            hora_final = datetime.now().strftime('%H:%M:%S')
            df_novos = pd.concat(novos_dfs, ignore_index=True)
            if df_base is not None:
                df_final = pd.concat([df_base, df_novos], ignore_index=True)
            else:
                df_final = df_novos
            update_callback(0.95, "Salvando arquivos tratados...")
            df_final.to_csv(arquivo_final, index=False, encoding="latin-1", sep=";", decimal=",")
            tempo_total = time.time() - start_total
            log_file.write("------ Compilação Concluída ------\n\n")
            log_file.write(
                f"Horário: {hora_final}\nNome do Relatório: base_vendas.csv\nQuantidade de linhas total: {len(df_final)}\nTempo total: {tempo_total:.2f}s\n\n"
            )
        elif not arquivos_processados_hoje:
            raise Exception("Nenhum novo dado válido para processar em vendas!")
    update_callback(1.0, "Finalizado!")

def processar_bancario_backend(pasta_orig, update_callback):
    pasta_bruto = os.path.join(pasta_orig, "dados_brutos")
    pasta_tratado = os.path.join(pasta_orig, "dados_tratados")
    pasta_consolidado = os.path.join(pasta_orig, "historico_consolidado")
    arquivo_final = os.path.join(pasta_consolidado, "base_bancaria.csv")
    log_path = os.path.join(pasta_orig, "log_tratamento_bancario.txt")
    for pasta in [pasta_tratado, pasta_consolidado]:
        if not os.path.exists(pasta):
            os.makedirs(pasta)
    update_callback(0.1, "Buscando movimentações bancárias...")
    arquivos = glob.glob(os.path.join(pasta_bruto, "Movimentações Conta Banco*.xls"))
    if not arquivos:
        raise Exception("Nenhum arquivo bancário encontrado!")
    arquivos_logados = set()
    if os.path.exists(log_path):
        with open(log_path, "r", encoding="utf-8") as log_file:
            for linha in log_file:
                if "Movimentações Conta Banco:" in linha:
                    nome = linha.split(":",1)[1].strip()
                    arquivos_logados.add(nome)
    bloco_data = datetime.now().strftime('%d/%m/%Y')
    novos_dfs = []
    start_total = time.time()
    arquivos_processados_hoje = False
    if os.path.exists(arquivo_final):
        df_base = pd.read_csv(arquivo_final, encoding="latin-1", sep=";", decimal=",")
    else:
        df_base = None
    update_callback(0.2, "Validando estrutura de dados...")
    total_arquivos = len(arquivos)
    arquivos_novos = [a for a in arquivos if os.path.splitext(os.path.basename(a))[0] + ".csv" not in arquivos_logados]
    with open(log_path, "a", encoding="utf-8") as log_file:
        for idx, arquivo in enumerate(arquivos):
            nome_csv = os.path.splitext(os.path.basename(arquivo))[0] + ".csv"
            if nome_csv in arquivos_logados:
                continue
            if not arquivos_processados_hoje:
                log_file.write(f"------ Tratamento do dia {bloco_data} ------\n\n")
                arquivos_processados_hoje = True
            progresso = 0.2 + (0.6 * (idx + 1) / total_arquivos)
            update_callback(progresso, f"Lendo movimentações bancárias ({idx+1}/{len(arquivos_novos)})...")
            inicio = time.time()
            hora = datetime.now().strftime('%H:%M:%S')
            df = extrair_tabela_html_bancaria(arquivo)
            if df is not None and not df.empty:
                caminho_csv = os.path.join(pasta_tratado, nome_csv)
                df.to_csv(caminho_csv, index=False, encoding="latin-1", sep=";", decimal=",")
                tempo_gasto = time.time() - inicio
                novos_dfs.append(df)
                reg = (f"Horário: {hora}\nNome do Relatório: {nome_csv}\nQuantidade de linhas adicionadas: {len(df)}\nTempo: {tempo_gasto:.2f}s\n")
                log_file.write(reg + "\n")
            else:
                tempo_gasto = time.time() - inicio
                reg = (f"Horário: {hora}\nNome do Relatório: {nome_csv}\nQuantidade de linhas adicionadas: FALHA\nTempo: {tempo_gasto:.2f}s\n")
                log_file.write(reg + "\n")
        update_callback(0.85, "Consolidando informações...")
        if novos_dfs:
            hora_final = datetime.now().strftime('%H:%M:%S')
            df_novos = pd.concat(novos_dfs, ignore_index=True)
            if df_base is not None:
                df_final = pd.concat([df_base, df_novos], ignore_index=True)
            else:
                df_final = df_novos
            update_callback(0.95, "Salvando dados consolidados...")
            df_final.to_csv(arquivo_final, index=False, encoding="latin-1", sep=";", decimal=",")
            tempo_total = time.time() - start_total
            log_file.write("------ Compilação Concluída ------\n\n")
            log_file.write(
                f"Horário: {hora_final}\nNome do Relatório: base_bancaria.csv\nQuantidade de linhas total: {len(df_final)}\nTempo total: {tempo_total:.2f}s\n\n"
            )
        elif not arquivos_processados_hoje:
            raise Exception("Nenhum novo dado válido para processar em bancário!")
    update_callback(1.0, "Finalizado!")
