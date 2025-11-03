"""
Lotus BI Suite - Aplicação de Tratamento de Dados
Integração completa do frontend CustomTkinter com backend de processamento
"""

import customtkinter as ctk
from tkinter import filedialog
import threading
import time
import os
import glob
import pandas as pd
from datetime import datetime
from PIL import Image
from backend_ import extrair_tabela_html_vendas, extrair_tabela_html_bancaria

ctk.set_appearance_mode("dark")

class LotusBIApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Lotus BI Suite - Atualização de Dados")
        self.geometry("520x780")
        self.resizable(False, False)
        self.configure(fg_color="#2a2a2a")
        
        try:
            self.iconbitmap("lotus_icon.ico")
        except:
            pass

        self.main_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Logo oficial
        try:
            logo_path = "logotipo-oficial-vertical.png"
            self.logo_img = ctk.CTkImage(Image.open(logo_path), size=(280, 120))
            ctk.CTkLabel(self.main_frame, image=self.logo_img, text="", fg_color="transparent").pack(pady=(20, 15))
        except Exception as e:
            print(f"Erro ao carregar logo: {e}")
            ctk.CTkLabel(self.main_frame, text="LOTUS\nConveniência", font=("Segoe UI", 32, "bold"), 
                        text_color="#f05a47", fg_color="transparent").pack(pady=(20,15))
        
        ctk.CTkLabel(self.main_frame, text="Painel de atualização de relatórios", 
                     font=("Segoe UI", 15), text_color="#d0d0d0", fg_color="transparent").pack(pady=(0,6))
        
        ctk.CTkLabel(self.main_frame, text="Vendas | Bancos | Conveniência e Controle", 
                     font=("Segoe UI", 13), text_color="#a0a0a0", fg_color="transparent").pack(pady=(0,30))

        # Barra de progresso + Labels (inicialmente ocultos)
        self.progress = ctk.CTkProgressBar(self.main_frame, width=400, height=14, 
                                          fg_color="#3a3a3a", progress_color="#f05a47", corner_radius=7)
        self.progress.pack(pady=(0,8))
        self.progress.pack_forget()
        
        self.lbl_status = ctk.CTkLabel(self.main_frame, text="", font=("Segoe UI", 14), 
                                       text_color="#d0d0d0", fg_color="transparent")
        self.lbl_status.pack(pady=(0,5))
        self.lbl_status.pack_forget()
        
        self.lbl_percent = ctk.CTkLabel(self.main_frame, text="", font=("Segoe UI", 15, "bold"), 
                                       text_color="#f05a47", fg_color="transparent")
        self.lbl_percent.pack(pady=(0,20))
        self.lbl_percent.pack_forget()

        # Botões
        self.btn_all = ctk.CTkButton(self.main_frame, text="Atualizar Tudo 🚀", width=380, height=58, 
                                     font=("Segoe UI", 18, "bold"),
                                     fg_color="#f05a47", hover_color="#d64a3a", text_color="#ffffff",
                                     corner_radius=16, border_width=0,
                                     command=lambda: self.threaded(self.atualizar_tudo))
        self.btn_all.pack(pady=10)

        self.btn_vendas = ctk.CTkButton(self.main_frame, text="Atualizar Vendas 📈", width=380, height=54,
                                        font=("Segoe UI", 17, "bold"),
                                        fg_color="#1a1a1a", hover_color="#2a2a2a", text_color="#ffffff",
                                        corner_radius=16, border_width=2, border_color="#404040",
                                        command=lambda: self.threaded(self.atualizar_vendas))
        self.btn_vendas.pack(pady=8)

        self.btn_banco = ctk.CTkButton(self.main_frame, text="Atualizar Movimentações Bancárias 🏦", 
                                       width=380, height=54, font=("Segoe UI", 17, "bold"),
                                       fg_color="#c0c0c0", hover_color="#a8a8a8", text_color="#1a1a1a",
                                       corner_radius=16, border_width=0,
                                       command=lambda: self.threaded(self.atualizar_banco))
        self.btn_banco.pack(pady=8)

        self.btn_ajuda = ctk.CTkButton(self.main_frame, text="❓ Precisa de ajuda?", 
                                       fg_color="transparent", hover_color="#3a3a3a",
                                       text_color="#f05a47", font=("Segoe UI", 13, "underline"),
                                       width=200, height=32, border_width=0,
                                       command=self.abrir_ajuda)
        self.btn_ajuda.pack(pady=(22,25))

        # Rodapé
        ctk.CTkLabel(self.main_frame, text="©2025 Lotus Conveniência - Todos os direitos reservados", 
                     font=("Segoe UI", 9), text_color="#606060", fg_color="transparent").pack(side="bottom", pady=(0,5))
        ctk.CTkLabel(self.main_frame, text="Suporte: (31) 90000-0000", font=("Segoe UI", 11, "bold"), 
                     text_color="#f05a47", fg_color="transparent").pack(side="bottom", pady=(0,2))
        ctk.CTkLabel(self.main_frame, text="Versão 1.0", font=("Segoe UI", 11), 
                     text_color="#808080", fg_color="transparent").pack(side="bottom", pady=(0,3))

    def threaded(self, func):
        self.progress.pack(pady=(10,8))
        self.lbl_status.pack(pady=(0,5))
        self.lbl_percent.pack(pady=(0,20))
        self.progress.set(0)
        self.lbl_status.configure(text="Preparando automação...")
        self.lbl_percent.configure(text="0%")
        self.disable_buttons()
        threading.Thread(target=lambda: self.run_and_feedback(func), daemon=True).start()

    def run_and_feedback(self, func):
        try:
            result = func(self.update_progress)
            if result == "cancelado":
                return
            self.show_popup("Sucesso! ✅", "Processo finalizado com sucesso.", "green")
        except Exception as e:
            self.show_popup("Erro! ❌", f"Ocorreu um erro: {e}", "red")
        finally:
            self.progress.set(0)
            self.lbl_status.pack_forget()
            self.lbl_percent.pack_forget()
            self.progress.pack_forget()
            self.enable_buttons()

    def update_progress(self, percent, msg=None):
        self.progress.set(percent)
        if msg:
            self.lbl_status.configure(text=msg)
        self.lbl_percent.configure(text=f"{int(percent*100)}%")
        self.update()

    def show_popup(self, title, msg, color):
        popup = ctk.CTkToplevel(self)
        popup.title(title)
        popup.geometry("360x150")
        popup.resizable(False, False)
        fg = "#f05a47" if color == "green" else "#d64a3a"
        popup.configure(fg_color="#2a2a2a")
        
        ctk.CTkLabel(popup, text=title, font=("Segoe UI", 20, "bold"), text_color=fg, fg_color="transparent").pack(pady=(18, 8))
        ctk.CTkLabel(popup, text=msg, font=("Segoe UI", 14), text_color="#ffffff", fg_color="transparent").pack(pady=(5,18))
        ctk.CTkButton(popup, text="OK", command=popup.destroy, fg_color=fg, hover_color="#2a2a2a", 
                     text_color="#fff", width=120, height=38, font=("Segoe UI", 14, "bold")).pack(pady=5)
        
        popup.update_idletasks()
        popup.lift()
        popup.focus_force()
        self.center_popup(popup)
        popup.grab_set()

    def show_popup_centered(self, title, msg, color="alerta"):
        popup = ctk.CTkToplevel(self)
        popup.title(title)
        popup.geometry("370x160")
        popup.resizable(False, False)
        fg = "#f05a47"
        popup.configure(fg_color="#2a2a2a")
        
        ctk.CTkLabel(popup, text=title, font=("Segoe UI", 19, "bold"), text_color=fg, fg_color="transparent").pack(pady=(18, 8))
        ctk.CTkLabel(popup, text=msg, font=("Segoe UI", 13), text_color="#fff", fg_color="transparent", wraplength=330).pack(pady=(5,20))
        ctk.CTkButton(popup, text="OK", command=popup.destroy, fg_color=fg, hover_color="#2a2a2a", 
                     text_color="#fff", width=120, height=38, font=("Segoe UI", 14, "bold")).pack(pady=5)
        
        popup.update_idletasks()
        popup.lift()
        popup.focus_force()
        self.center_popup(popup)
        popup.grab_set()

    def center_popup(self, popup):
        popup.update_idletasks()
        x = self.winfo_x() + (self.winfo_width() - popup.winfo_width()) // 2
        y = self.winfo_y() + (self.winfo_height() - popup.winfo_height()) // 2
        popup.geometry(f"+{x}+{y}")

    def disable_buttons(self):
        self.btn_all.configure(state="disabled")
        self.btn_vendas.configure(state="disabled")
        self.btn_banco.configure(state="disabled")

    def enable_buttons(self):
        self.btn_all.configure(state="normal")
        self.btn_vendas.configure(state="normal")
        self.btn_banco.configure(state="normal")

    def abrir_ajuda(self):
        popup = ctk.CTkToplevel(self)
        popup.title("💡 Ajuda")
        popup.geometry("480x260")
        popup.resizable(False, False)
        popup.configure(fg_color="#2a2a2a")
        
        ctk.CTkLabel(popup, text="💡 Ajuda", font=("Segoe UI", 22, "bold"), text_color="#f05a47", fg_color="transparent").pack(pady=(20, 15))
        
        help_text = """Use os botões acima para atualizar seus relatórios.

'Atualizar Tudo' processa todos os relatórios de uma vez.
Você também pode atualizar Vendas ou Movimentações 
Bancárias individualmente.

Selecione a pasta correta quando solicitado."""
        
        ctk.CTkLabel(popup, text=help_text, font=("Segoe UI", 13), text_color="#d0d0d0", 
                     fg_color="transparent", justify="left").pack(pady=(0,20), padx=30)
        
        ctk.CTkButton(popup, text="OK", command=popup.destroy, fg_color="#f05a47", hover_color="#d64a3a",
                     text_color="#fff", width=140, height=40, font=("Segoe UI", 15, "bold")).pack(pady=10)
        
        popup.update_idletasks()
        popup.lift()
        popup.focus_force()
        self.center_popup(popup)
        popup.grab_set()

    # ==================== INTEGRAÇÃO COM BACKEND ====================
    
    def processar_vendas_backend(self, pasta_orig, update_callback):
        """Pipeline de tratamento do histórico de vendas com progresso visual."""
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

    def processar_bancario_backend(self, pasta_orig, update_callback):
        """Pipeline de tratamento do histórico bancário com progresso visual."""
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

    def atualizar_tudo(self, update=None):
        pasta = filedialog.askdirectory(title="Selecione a pasta RAIZ da BASE DE DADOS")
        if not pasta:
            self.show_popup_centered("⚠️ Operação cancelada!", 
                                    "Nenhuma pasta foi selecionada.\nA automação não foi executada.", "alerta")
            return "cancelado"
        
        pasta_vendas = os.path.join(pasta, "Histórico de Vendas")
        pasta_bancario = os.path.join(pasta, "Movimentações Bancárias")
        
        if update:
            update(0.1, "Validando estrutura de pastas...")
        
        processados = 0
        total_processos = 0
        
        if os.path.exists(pasta_vendas):
            total_processos += 1
        if os.path.exists(pasta_bancario):
            total_processos += 1
            
        if total_processos == 0:
            raise Exception("Pastas 'Histórico de Vendas' ou 'Movimentações Bancárias' não encontradas!")
        
        if os.path.exists(pasta_vendas):
            if update:
                update(0.2, "Processando Histórico de Vendas...")
            self.processar_vendas_backend(pasta_vendas, lambda p, m: update(0.2 + p*0.4, m) if update else None)
            processados += 1
            
        if os.path.exists(pasta_bancario):
            if update:
                update(0.6, "Integrando Movimentações Bancárias...")
            self.processar_bancario_backend(pasta_bancario, lambda p, m: update(0.6 + p*0.35, m) if update else None)
            processados += 1
        
        if update:
            update(1.0, "Finalizando e salvando logs...")

    def atualizar_vendas(self, update=None):
        pasta = filedialog.askdirectory(title="Selecione a pasta 'Histórico de Vendas'")
        if not pasta:
            self.show_popup_centered("⚠️ Operação cancelada!", 
                                    "Nenhuma pasta foi selecionada.\nA automação não foi executada.", "alerta")
            return "cancelado"
        
        if "venda" not in pasta.lower() and "histórico" not in pasta.lower() and "historico" not in pasta.lower():
            self.show_popup_centered("❌ Pasta Incorreta!", 
                                    "A pasta selecionada não parece ser a pasta de vendas.\nPor favor, selecione a pasta correta.", "alerta")
            return "cancelado"
        
        self.processar_vendas_backend(pasta, update)

    def atualizar_banco(self, update=None):
        pasta = filedialog.askdirectory(title="Selecione a pasta 'Movimentações Bancárias'")
        if not pasta:
            self.show_popup_centered("⚠️ Operação cancelada!", 
                                    "Nenhuma pasta foi selecionada.\nA automação não foi executada.", "alerta")
            return "cancelado"
        
        if "banc" not in pasta.lower() and "moviment" not in pasta.lower():
            self.show_popup_centered("❌ Pasta Incorreta!", 
                                    "A pasta selecionada não parece ser a de movimentações bancárias.\nPor favor, selecione a pasta correta.", "alerta")
            return "cancelado"
        
        self.processar_bancario_backend(pasta, update)

if __name__ == "__main__":
    app = LotusBIApp()
    app.mainloop()
