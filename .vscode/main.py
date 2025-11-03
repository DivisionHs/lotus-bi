import os
import glob
import pandas as pd
import time
from datetime import datetime
from tkinter import Tk, filedialog, messagebox, Button, Label
import threading
from backend import extrair_tabela_html_vendas, extrair_tabela_html_bancaria

def processar_vendas(pasta_orig, finalizar=True):
    """
    Pipeline de tratamento do histórico de vendas.
    """
    pasta_bruto = os.path.join(pasta_orig, "dados_brutos")
    pasta_tratado = os.path.join(pasta_orig, "dados_tratados")
    pasta_consolidado = os.path.join(pasta_orig, "historico_consolidado")
    arquivo_final = os.path.join(pasta_consolidado, "base_vendas.csv")
    log_path = os.path.join(pasta_orig, "log_tratamento_vendas.txt")

    for pasta in [pasta_tratado, pasta_consolidado]:
        if not os.path.exists(pasta):
            os.makedirs(pasta)

    arquivos = glob.glob(os.path.join(pasta_bruto, "Histórico de Vendas*.xls"))
    if not arquivos:
        if finalizar:
            messagebox.showinfo("Aviso", "Nenhum arquivo de vendas encontrado!")
        return

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

    with open(log_path, "a", encoding="utf-8") as log_file:
        for arquivo in arquivos:
            nome_csv = os.path.splitext(os.path.basename(arquivo))[0] + ".csv"
            if nome_csv in arquivos_logados:
                continue
            if not arquivos_processados_hoje:
                log_file.write(f"------ Tratamento do dia {bloco_data} ------\n\n")
                arquivos_processados_hoje = True
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
            if finalizar:
                messagebox.showinfo(
                    "Sucesso", 
                    f"Tratamento e consolidação VENDAS finalizada!\nArquivo: {arquivo_final}\nLinhas totais: {len(df_final)}\nTempo total: {tempo_total:.2f}s"
                )
        elif not arquivos_processados_hoje and finalizar:
            messagebox.showinfo("Aviso", "Nenhum novo dado válido para processar em vendas!")

def processar_bancario(pasta_orig, finalizar=True):
    """
    Pipeline de tratamento do histórico de movimentações bancárias.
    """
    pasta_bruto = os.path.join(pasta_orig, "dados_brutos")
    pasta_tratado = os.path.join(pasta_orig, "dados_tratados")
    pasta_consolidado = os.path.join(pasta_orig, "historico_consolidado")
    arquivo_final = os.path.join(pasta_consolidado, "base_bancaria.csv")
    log_path = os.path.join(pasta_orig, "log_tratamento_bancario.txt")

    for pasta in [pasta_tratado, pasta_consolidado]:
        if not os.path.exists(pasta):
            os.makedirs(pasta)

    arquivos = glob.glob(os.path.join(pasta_bruto, "Movimentações Conta Banco*.xls"))
    if not arquivos:
        if finalizar:
            messagebox.showinfo("Aviso", "Nenhum arquivo bancário encontrado!")
        return

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

    with open(log_path, "a", encoding="utf-8") as log_file:
        for arquivo in arquivos:
            nome_csv = os.path.splitext(os.path.basename(arquivo))[0] + ".csv"
            if nome_csv in arquivos_logados:
                continue
            if not arquivos_processados_hoje:
                log_file.write(f"------ Tratamento do dia {bloco_data} ------\n\n")
                arquivos_processados_hoje = True
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
                f"Horário: {hora_final}\nNome do Relatório: base_bancaria.csv\nQuantidade de linhas total: {len(df_final)}\nTempo total: {tempo_total:.2f}s\n\n"
            )
            if finalizar:
                messagebox.showinfo(
                    "Sucesso", 
                    f"Tratamento e consolidação BANCÁRIO finalizada!\nArquivo: {arquivo_final}\nLinhas totais: {len(df_final)}\nTempo total: {tempo_total:.2f}s"
                )
        elif not arquivos_processados_hoje and finalizar:
            messagebox.showinfo("Aviso", "Nenhum novo dado válido para processar em bancário!")

def start_ui():
    """
    Constrói interface gráfica com três botões:
    - Atualizar tudo (processa os dois fluxos baseados nas subpastas internas!)
    - Atualizar relatório de Vendas
    - Atualizar Movimentações Bancárias
    """
    def atualizar_tudo():
        root = Tk()
        root.withdraw()
        pasta_base = filedialog.askdirectory(title="Selecione a pasta RAIZ da BASE DE DADOS")
        if not pasta_base:
            return
        # Busca as subpastas principais conforme o padrão do projeto
        pasta_vendas = os.path.join(pasta_base, "Histórico de Vendas")
        pasta_bancario = os.path.join(pasta_base, "Movimentações Bancárias")
        qualquer_processado = False
        if os.path.exists(pasta_vendas):
            processar_vendas(pasta_vendas, finalizar=False)
            qualquer_processado = True
        else:
            messagebox.showinfo("Aviso", "Pasta 'Histórico de Vendas' não encontrada dentro da Base de Dados.")
        if os.path.exists(pasta_bancario):
            processar_bancario(pasta_bancario, finalizar=False)
            qualquer_processado = True
        else:
            messagebox.showinfo("Aviso", "Pasta 'Movimentações Bancárias' não encontrada dentro da Base de Dados.")
        if qualquer_processado:
            messagebox.showinfo(
                "Sucesso",
                "Automação finalizada! Ambos relatórios (Vendas e Bancário) foram atualizados. Confira os logs e arquivos consolidados."
            )

    def atualizar_vendas():
        root = Tk()
        root.withdraw()
        pasta_base = filedialog.askdirectory(title="Selecione a pasta 'Histórico de Vendas'")
        if pasta_base:
            processar_vendas(pasta_base, finalizar=True)

    def atualizar_bancario():
        root = Tk()
        root.withdraw()
        pasta_base = filedialog.askdirectory(title="Selecione a pasta 'Movimentações Bancárias'")
        if pasta_base:
            processar_bancario(pasta_base, finalizar=True)

    janela = Tk()
    janela.title("Lotus BI Suite - Tratamento de Dados")
    Label(janela, text="Selecione uma ação para atualizar os relatórios:").pack(pady=10)
    Button(janela, text="Atualizar tudo", width=30, command=lambda: threading.Thread(target=atualizar_tudo).start()).pack(pady=5)
    Button(janela, text="Atualizar relatório de Vendas", width=30, command=lambda: threading.Thread(target=atualizar_vendas).start()).pack(pady=5)
    Button(janela, text="Atualizar Movimentações Bancárias", width=30, command=lambda: threading.Thread(target=atualizar_bancario).start()).pack(pady=5)
    janela.mainloop()

if __name__ == "__main__":
    start_ui()
