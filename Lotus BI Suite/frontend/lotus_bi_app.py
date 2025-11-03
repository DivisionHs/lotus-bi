import sys
import os
import webbrowser
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import customtkinter as ctk
from tkinter import filedialog
import threading
from PIL import Image

from backend.processing import processar_vendas_backend, processar_bancario_backend

# Função para buscar asset sempre funcionando no .py e no .exe
def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

ctk.set_appearance_mode("dark")

class LotusBIApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Lotus BI Suite - Atualização de Dados")
        self.geometry("520x780")
        self.resizable(False, False)
        self.configure(fg_color="#2a2a2a")
        self.center_main_window()

        # Busca dinâmica do ícone com resource_path
        try:
            icon_path = resource_path(os.path.join('assets', 'lotus_icon.ico'))
            self.iconbitmap(icon_path)
        except Exception as e:
            print(f"Erro ao carregar ícone: {e}")

        self.main_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Busca logo com resource_path
        try:
            logo_path = resource_path(os.path.join('assets', 'logotipo_oficial.png'))
            self.logo_img = ctk.CTkImage(Image.open(logo_path), size=(310, 170))
            ctk.CTkLabel(self.main_frame, image=self.logo_img, text="", fg_color="transparent").pack(pady=(20, 15))
        except Exception as e:
            print(f"Erro ao carregar logo: {e}")
            ctk.CTkLabel(self.main_frame, text="LOTUS\nConveniência", font=("Segoe UI", 32, "bold"),
                         text_color="#f05a47", fg_color="transparent").pack(pady=(20,15))

        ctk.CTkLabel(self.main_frame, text="Painel de atualização de relatórios",
                     font=("Segoe UI", 15), text_color="#d0d0d0", fg_color="transparent").pack(pady=(0,6))
        ctk.CTkLabel(self.main_frame, text="Vendas | Bancos | Conveniência e Controle",
                     font=("Segoe UI", 13), text_color="#a0a0a0", fg_color="transparent").pack(pady=(0,30))

        self.btn_all = ctk.CTkButton(self.main_frame, text="Atualizar Tudo 🚀", width=380, height=58,
                                     font=("Segoe UI", 18, "bold"),
                                     fg_color="#f05a47", hover_color="#d64a3a", text_color="#ffffff",
                                     corner_radius=16, border_width=0,
                                     command=self.atualizar_tudo)
        self.btn_all.pack(pady=10)
        self.btn_vendas = ctk.CTkButton(self.main_frame, text="Atualizar Vendas 📈", width=380, height=54,
                                        font=("Segoe UI", 17, "bold"),
                                        fg_color="#1a1a1a", hover_color="#2a2a2a", text_color="#ffffff",
                                        corner_radius=16, border_width=2, border_color="#404040",
                                        command=self.atualizar_vendas)
        self.btn_vendas.pack(pady=8)
        self.btn_banco = ctk.CTkButton(self.main_frame, text="Atualizar Movimentações Bancárias 🏦",
                                       width=380, height=54, font=("Segoe UI", 17, "bold"),
                                       fg_color="#c0c0c0", hover_color="#a8a8a8", text_color="#1a1a1a",
                                       corner_radius=16, border_width=0,
                                       command=self.atualizar_banco)
        self.btn_banco.pack(pady=8)
        self.btn_ajuda = ctk.CTkButton(self.main_frame, text="❓ Precisa de ajuda?",
                                       fg_color="transparent", hover_color="#3a3a3a",
                                       text_color="#f05a47", font=("Segoe UI", 13, "underline"),
                                       width=200, height=32, border_width=0,
                                       command=self.abrir_ajuda)
        self.btn_ajuda.pack(pady=(22,25))

        # Frame do progresso sempre visível!
        self.frame_progress = ctk.CTkFrame(self.main_frame, fg_color="transparent", height=90)
        self.frame_progress.pack(pady=(18,0), fill="x")
        self.frame_progress.pack_propagate(False)

        self.progress = ctk.CTkProgressBar(self.frame_progress, width=400, height=14,
                                           fg_color="#3a3a3a", progress_color="#f05a47", corner_radius=7)
        self.progress.pack(pady=(0,8))
        self.progress.pack_forget()
        self.lbl_status = ctk.CTkLabel(self.frame_progress, text="", font=("Segoe UI", 14),
                                       text_color="#d0d0d0", fg_color="transparent", anchor="center", justify="center")
        self.lbl_status.pack(pady=(0,1))
        self.lbl_status.pack_forget()
        self.lbl_percent = ctk.CTkLabel(self.frame_progress, text="", font=("Segoe UI", 17, "bold"),
                                        text_color="#f05a47", fg_color="transparent", anchor="center", justify="center")
        self.lbl_percent.pack(pady=(0, 10))
        self.lbl_percent.pack_forget()

        ctk.CTkLabel(self.main_frame, text="©2025 Lotus Conveniência - Todos os direitos reservados",
                     font=("Segoe UI", 9), text_color="#606060", fg_color="transparent").pack(side="bottom", pady=(0,5))

        ctk.CTkButton(self.main_frame, text="Suporte: (11) 99170-8356",
                      font=("Segoe UI", 11, "bold"), text_color="#fff",
                      fg_color="#f05a47", hover_color="#d64a3a",
                      corner_radius=20, width=220, height=30, border_width=0,
                      command=self.abrir_whatsapp).pack(side="bottom", pady=(0,2))

        ctk.CTkLabel(self.main_frame, text="Versão 1.0", font=("Segoe UI", 11),
                     text_color="#808080", fg_color="transparent").pack(side="bottom", pady=(0,3))

    def abrir_whatsapp(self):
        url = "https://wa.me/5511991708356"
        webbrowser.open(url)

    def center_main_window(self):
        self.update_idletasks()
        w, h = 520, 780
        sw = self.winfo_screenwidth()
        sh = self.winfo_screenheight()
        x, y = (sw - w) // 2, (sh - h) // 2
        self.geometry(f"{w}x{h}+{x}+{y}")

    def threaded(self, func, *args):
        self.progress.pack(pady=(10,8))
        self.lbl_status.pack(pady=(0,1))
        self.lbl_percent.pack(pady=(0,10))
        self.progress.set(0)
        self.lbl_status.configure(text="Preparando automação...")
        self.lbl_percent.configure(text="0%")
        self.disable_buttons()
        threading.Thread(target=lambda: self.run_and_feedback(func, *args), daemon=True).start()

    def run_and_feedback(self, func, *args):
        try:
            func(*args)
            self.finalizar_feedback()
            self.show_popup("Sucesso! ✅", "Processo finalizado com sucesso.", "green")
        except Exception as e:
            self.finalizar_feedback()
            self.show_popup("Erro! ❌", str(e), "red")

    def finalizar_feedback(self):
        self.progress.pack_forget()
        self.lbl_status.pack_forget()
        self.lbl_percent.pack_forget()
        self.enable_buttons()

    def update_progress(self, percent, msg=None):
        self.progress.set(percent)
        if msg:
            self.lbl_status.configure(text=msg)
        else:
            self.lbl_status.configure(text="")
        self.lbl_percent.configure(text=f"{int(percent*100)}%")
        self.update()

    def atualizar_tudo(self):
        pasta_base = filedialog.askdirectory(title="Selecione a pasta RAIZ da BASE DE DADOS")
        if not pasta_base:
            self.show_popup_centered("⚠️ Operação cancelada!",
                                    "Nenhuma pasta foi selecionada.\nA automação não foi executada.", "alerta")
            return
        pasta_vendas = os.path.join(pasta_base, "Histórico de Vendas")
        pasta_bancario = os.path.join(pasta_base, "Movimentações Bancárias")
        if not os.path.exists(pasta_vendas):
            self.show_popup("Erro! ❌", "Pasta 'Histórico de Vendas' não encontrada.", "red")
            return
        if not os.path.exists(pasta_bancario):
            self.show_popup("Erro! ❌", "Pasta 'Movimentações Bancárias' não encontrada.", "red")
            return
        self.threaded(self.proc_full, pasta_vendas, pasta_bancario)

    def proc_full(self, pasta_vendas, pasta_bancario):
        processar_vendas_backend(pasta_vendas, self.update_progress)
        processar_bancario_backend(pasta_bancario, self.update_progress)

    def atualizar_vendas(self):
        pasta = filedialog.askdirectory(title="Selecione a pasta 'Histórico de Vendas'")
        if not pasta:
            self.show_popup_centered("⚠️ Operação cancelada!",
                                    "Nenhuma pasta foi selecionada.\nA automação não foi executada.", "alerta")
            return
        pasta_nome = os.path.basename(pasta).lower()
        if not (pasta_nome.startswith("histórico de vendas") or pasta_nome.startswith("historico de vendas")):
            self.show_popup_centered("❌ Pasta Incorreta!",
                                    "A pasta selecionada não parece ser a pasta de vendas.\nPor favor, selecione a pasta correta.", "alerta")
            return
        self.threaded(processar_vendas_backend, pasta, self.update_progress)

    def atualizar_banco(self):
        pasta = filedialog.askdirectory(title="Selecione a pasta 'Movimentações Bancárias'")
        if not pasta:
            self.show_popup_centered("⚠️ Operação cancelada!",
                                    "Nenhuma pasta foi selecionada.\nA automação não foi executada.", "alerta")
            return
        pasta_nome = os.path.basename(pasta).lower()
        if not (pasta_nome.startswith("movimentações bancárias") or pasta_nome.startswith("movimentacoes bancarias")):
            self.show_popup_centered("❌ Pasta Incorreta!",
                                    "A pasta selecionada não parece ser a de movimentações bancárias.\nPor favor, selecione a pasta correta.", "alerta")
            return
        self.threaded(processar_bancario_backend, pasta, self.update_progress)

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
        ctk.CTkLabel(popup, text=msg, font=("Segoe UI", 13), text_color="#fff", fg_color="transparent", wraplength=330, anchor="center", justify="center").pack(pady=(5,20))
        ctk.CTkButton(popup, text="OK", command=popup.destroy, fg_color=fg, hover_color="#2a2a2a",
                      text_color="#fff", width=120, height=38, font=("Segoe UI", 14, "bold")).pack(pady=5)
        popup.update_idletasks()
        popup.lift()
        popup.focus_force()
        self.center_popup(popup)
        popup.grab_set()

    def center_popup(self, popup):
        popup.update_idletasks()
        w = popup.winfo_width()
        h = popup.winfo_height()
        root_x = self.winfo_rootx()
        root_y = self.winfo_rooty()
        root_w = self.winfo_width()
        root_h = self.winfo_height()
        x = root_x + (root_w - w)//2
        y = root_y + (root_h - h)//2
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
        help_text = (
            "Use os botões acima para atualizar seus relatórios.\n\n"
            "'Atualizar Tudo' processa todos os relatórios de uma vez.\n"
            "Você também pode atualizar Vendas ou Movimentações Bancárias individualmente.\n\n"
            "Selecione a pasta correta quando solicitado."
        )
        ctk.CTkLabel(
            popup, text=help_text, font=("Segoe UI", 13), text_color="#d0d0d0",
            fg_color="transparent", anchor="center", justify="center", wraplength=430
        ).pack(pady=(0, 25), padx=25, anchor="center")
        ctk.CTkButton(popup, text="OK", command=popup.destroy, fg_color="#f05a47", hover_color="#d64a3a",
                      text_color="#fff", width=140, height=40, font=("Segoe UI", 15, "bold")).pack(pady=10)
        popup.update_idletasks()
        popup.lift()
        popup.focus_force()
        self.center_popup(popup)
        popup.grab_set()

if __name__ == "__main__":
    app = LotusBIApp()
    app.mainloop()
