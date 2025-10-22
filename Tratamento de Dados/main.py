"""
main.py

Script principal da aplicação de tratamento e consolidação de dados do Projeto Hayslla.

Funções:
- Permite ao usuário escolher a pasta principal ("Histórico de Vendas") via interface Tkinter
- Processa arquivos brutos ainda não tratados
- Cria arquivos de saída tratados (.csv) e um arquivo consolidado incremental ("base_vendas.csv")
- Gera log detalhado de cada execução, agrupado por data
- Não duplica dados já tratados e não polui o log com arquivos repetidos

Fluxo principal:
1. Usuário seleciona a pasta raiz ("Histórico de Vendas").
2. O script percorre a subpasta "dados_brutos" e identifica apenas arquivos novos.
3. Se houver arquivos novos, trata, gera log e atualiza o consolidado.
4. Interface gráfica orienta o usuário com mensagens de sucesso/erro.
"""

import os
import glob
import pandas as pd
import time
from datetime import datetime
from bs4 import BeautifulSoup
from tkinter import Tk, filedialog, messagebox
import threading
from backend import extrair_tabela_html  # Importa função modularizada do backend

def processar_pasta():
    """
    Função principal do pipeline de tratamento e consolidação:
    - Cria/atualiza subpastas necessárias
    - Processa apenas arquivos novos
    - Gera log detalhado por data (log_tratamento.txt) fora das subpastas
    - Atualiza base_vendas.csv incrementalmente (sem duplicidade)
    - Mensagens amigáveis e detalhadas para o usuário
    """
    # Interface para seleção da pasta principal
    root = Tk()
    root.withdraw()
    pasta_orig = filedialog.askdirectory(title="Selecione a pasta HISTÓRICO DE VENDAS")
    if not pasta_orig:
        messagebox.showwarning("Aviso", "Nenhuma pasta selecionada.")
        return

    # Define subpastas fixas do projeto
    pasta_bruto = os.path.join(pasta_orig, "dados_brutos")
    pasta_tratado = os.path.join(pasta_orig, "dados_tratados")
    pasta_consolidado = os.path.join(pasta_orig, "historico_consolidado")
    arquivo_final = os.path.join(pasta_consolidado, "base_vendas.csv")
    log_path = os.path.join(pasta_orig, "log_tratamento.txt")

    # Cria subpastas se não existirem
    for pasta in [pasta_tratado, pasta_consolidado]:
        if not os.path.exists(pasta):
            os.makedirs(pasta)

    # Lista todos arquivos .xls para tratar
    arquivos = glob.glob(os.path.join(pasta_bruto, "Histórico de Vendas*.xls"))
    if not arquivos:
        messagebox.showinfo("Aviso", "Nenhum arquivo encontrado na pasta dados_brutos!")
        return

    # Lê log para saber quais arquivos já foram tratados
    arquivos_logados = set()
    if os.path.exists(log_path):
        with open(log_path, "r", encoding="utf-8") as log_file:
            for linha in log_file:
                if "Nome do Relatório:" in linha:
                    nome = linha.split(":",1)[1].strip()
                    arquivos_logados.add(nome)

    # Dados e variáveis auxiliares da sessão atual
    bloco_data = datetime.now().strftime('%d/%m/%Y')
    novos_dfs = []
    resultados_individuais = []  # Para uso futuro/log extra
    start_total = time.time()

    # Se base consolidada já existe, carrega para evitar duplicação
    if os.path.exists(arquivo_final):
        df_base = pd.read_csv(arquivo_final, encoding="latin-1", sep=";", decimal=",")
    else:
        df_base = None

    arquivos_processados_hoje = False  # Controla se haverá log do dia

    with open(log_path, "a", encoding="utf-8") as log_file:
        for arquivo in arquivos:
            nome_csv = os.path.splitext(os.path.basename(arquivo))[0] + ".csv"
            if nome_csv in arquivos_logados:
                # Arquivo já tratado anteriormente, apenas ignora (ótimo para evitar duplicidade!)
                continue

            # Se pelo menos um arquivo novo vai ser processado, cria o bloco de log do dia
            if not arquivos_processados_hoje:
                log_file.write(f"------ Tratamento do dia {bloco_data} ------\n\n")
                arquivos_processados_hoje = True

            inicio = time.time()
            hora = datetime.now().strftime('%H:%M:%S')
            print(f"Processando: {os.path.basename(arquivo)}")
            # Utiliza função auxiliar do backend para extrair o DataFrame
            df = extrair_tabela_html(arquivo)
            if df is not None and not df.empty:
                caminho_csv = os.path.join(pasta_tratado, nome_csv)
                df.to_csv(caminho_csv, index=False, encoding="latin-1", sep=";", decimal=",")
                tempo_gasto = time.time() - inicio
                novos_dfs.append(df)
                reg = (f"Horário: {hora}\nNome do Relatório: {nome_csv}\nQuantidade de linhas adicionadas: {len(df)}\nTempo: {tempo_gasto:.2f}s\n")
                resultados_individuais.append(reg)
                log_file.write(reg + "\n")
                print(f"Arquivo tratado salvo em: {caminho_csv}")
            else:
                tempo_gasto = time.time() - inicio
                reg = (f"Horário: {hora}\nNome do Relatório: {nome_csv}\nQuantidade de linhas adicionadas: FALHA\nTempo: {tempo_gasto:.2f}s\n")
                resultados_individuais.append(reg)
                log_file.write(reg + "\n")
                print(f"Falha ao processar {os.path.basename(arquivo)}. Nenhum dado extraído.")

        # Após tratar todos, só consolida se houver arquivos novos
        if novos_dfs:
            hora_final = datetime.now().strftime('%H:%M:%S')
            df_novos = pd.concat(novos_dfs, ignore_index=True)
            if df_base is not None:
                df_final = pd.concat([df_base, df_novos], ignore_index=True)
            else:
                df_final = df_novos
            df_final.to_csv(arquivo_final, index=False, encoding="latin-1", sep=";", decimal=",")
            tempo_total = time.time() - start_total
            log_file.write("------ Compilação Concluída ------\n\n")
            log_file.write(
                f"Horário: {hora_final}\nNome do Relatório: base_vendas.csv\nQuantidade de linhas total: {len(df_final)}\nTempo total: {tempo_total:.2f}s\n\n"
            )
            print(f"Arquivo CSV único gerado em: {arquivo_final}")
            messagebox.showinfo(
                "Sucesso", 
                f"Tratamento e consolidação finalizada!\nArquivo: {arquivo_final}\nLinhas totais: {len(df_final)}\nTempo total: {tempo_total:.2f}s"
            )
        elif not arquivos_processados_hoje:
            # Se não houve arquivos novos, não gera bloco de log do dia
            messagebox.showinfo("Aviso", "Nenhum novo dado válido para processar!")

def rodar_thread():
    """
    Executa o processamento em thread separada para não travar a interface Tkinter.
    """
    threading.Thread(target=processar_pasta).start()

if __name__ == "__main__":
    rodar_thread()
