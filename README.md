# Lotus BI Suite

***Automatização de tratamento, integração e consolidação de arquivos de vendas e movimentações bancárias, gerando uma base limpa e incremental pronta para análises em Power BI. Interface desktop moderna, simples e amigável, desenvolvida em Python com CustomTkinter.***

---

## ✨ Principais Funcionalidades

- Automação total: tratamento de arquivos de vendas e bancos em poucos cliques
- Interface moderna: frontend 100% Python CustomTkinter, centralizada e autoexplicativa
- Processamento incremental: tratamento inteligente, sem duplicação de dados já processados
- Logs detalhados: logs de tratamento gerados por segmento/pasta
- Suporte integrado: botão de WhatsApp direto na interface
- Feedback visual: barra de progresso, status e porcentagem em tempo real

---

## 📦 Bibliotecas Utilizadas

- [customtkinter](https://github.com/TomSchimansky/CustomTkinter) (interface gráfica desktop)
- [Pillow (PIL)](https://pypi.org/project/Pillow/) (manipulação de imagens)
- [Pandas](https://pandas.pydata.org/) (tratamento e fusão de dados)
- [BeautifulSoup 4](https://pypi.org/project/beautifulsoup4/) (parsing de HTML/XML quando necessário no backend)
- [PyInstaller (opcional)](https://pyinstaller.org/) (só para build do .exe)
- Bibliotecas padrão do Python: tkinter, threading, sys, os, webbrowser, glob, time, datetime

> Todas as dependências obrigatórias estão no arquivo **requirements.txt**.

---

## 🖥️ Frontend

O frontend da Lotus BI Suite foi construído em **CustomTkinter**, entregando uma interface moderna, responsiva e intuitiva.  

Todo o código está em:  
`frontend/lotus_bi_app.py`

**Destaques:**
- Layout centralizado com foco em produtividade.
- Barra de progresso visual, percentual em laranja abaixo do status.
- Botões de ação grandes, textos claros e visual autônomo.
- Seleção facilitada de pastas via dialogs Tkinter.
- Carregamento dinâmico de logo (PNG) e ícone (ICO) direto dos assets.
- Suporte via botão de WhatsApp na interface.
- Cores/fonte fáceis de customizar.

**Principais bibliotecas frontend:**  
CustomTkinter, Pillow, tkinter, threading, sys, os, webbrowser.

---

**Exemplo de uso integrado:**  

```
from backend.processing import processar_vendas_backend, processar_bancario_backend
...
self.threaded(processar_vendas_backend, pasta, self.update_progress)
```

---

## 🛠️ Backend

O backend, em `backend/processing.py`, realiza todas as tarefas de leitura, processamento, consolidação e logging dos dados de vendas e bancários.

**Como trabalha:**
- Lê arquivos .xls("dados_brutos") e trata para formato padrão.
- Consolida incrementalmente dados, evitando duplicidade.
- Cria/atualiza automaticamente:
   - `dados_tratados/` (.csv)
   - `historico_consolidado/`
   - `log_tratamento_*.txt` (log por segmento).
- Utiliza logs para rastreabilidade e análise do pipeline.
- Pode ser expandido para outros fluxos (estoque, compras, etc.)

**Tecnologias:**  
pandas, beautifulsoup4 (opcional), datetime, glob, time, os

**Exemplo de import no backend:**

```
import os
import glob
import time
import pandas as pd
from datetime import datetime
from bs4 import BeautifulSoup
```
**Integração:**  
Frontend importa as funções backend e exibe o status/progresso em tempo real.

---

## 📁 Estrutura de Pastas

```
Lotus BI Suite/
├── assets/
│   ├── logotipo_oficial.png
│   └── lotus_icon.ico
├── backend/
│   ├── processing.py
│   └── __init__.py
├── frontend/
│   └── lotus_bi_app.py
├── Banco de Dados/                     
│   ├── Histórico de Vendas/
│   │   ├── dados_brutos/
│   │   ├── dados_tratados/              # (*) CRIADA AUTOMATICAMENTE PELO SCRIPT
│   │   ├── historico_consolidado/       # (*) CRIADA AUTOMATICAMENTE PELO SCRIPT
│   │   └── log_tratamento_vendas.txt    # (*) CRIADO AUTOMATICAMENTE PELO SCRIPT
│   ├── Movimentações Bancárias/
│   │   ├── dados_brutos/
│   │   ├── dados_tratados/              # (*) CRIADA AUTOMATICAMENTE PELO SCRIPT
│   │   ├── historico_consolidado/       # (*) CRIADA AUTOMATICAMENTE PELO SCRIPT
│   │   └── log_tratamento_bancario.txt  # (*) CRIADO AUTOMATICAMENTE PELO SCRIPT
├── requirements.txt
└── README.md
```
> **Nota:** As pastas `dados_tratados`, `historico_consolidado` e os arquivos `log_tratamento_xxx.txt` são **criadas automaticamente pelo sistema**, não sendo necessário prepará-las manualmente.

---

## 🚀 Instalação

### Clone o repositório:
```
git clone https://github.com/seu-usuario/lotus-bi-suite.git
cd lotus-bi-suite
```
### Crie seu ambiente virtual e instale as dependências
**Windows:**
```
python -m venv venv
venv\Scripts\activate # Windows
pip install -r requirements.txt
```

**Linux/Mac:**

```
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

> **Dica:** Mantenha sua pasta de dados na estrutura sugerida acima para maior integração!

---

## 💻 Como Usar

### Execute a interface: 
```
python ./frontend/lotus_bi_app.py
```

- Use os botões e selecione a pasta correta quando solicitado.
- Acompanhe o progresso e logs diretamente na interface.

---

## 🛠️ Build do Executável (.exe) (Opcional)

### Para empacotar e gerar o `.exe` standalone:
```
venv\Scripts\pyinstaller.exe --onefile --noconsole ^
--icon="Lotus BI Suite/assets/lotus_icon.ico" ^
--add-data="Lotus BI Suite/assets/logotipo_oficial.png;assets" ^
--add-data="Lotus BI Suite/assets/lotus_icon.ico;assets" ^
--paths="Lotus BI Suite" "Lotus BI Suite/frontend/lotus_bi_app.py"
```

O executável estará em `dist/lotus_bi_app.exe`.

---

## 🧑‍💻 Suporte

Dúvidas/sugestões?  
Use o botão de WhatsApp no app ou:

[WhatsApp: Suporte Técnico](https://wa.me/5511991708356)

---

## 📚 Sobre o Projeto

Voltado para operações de conveniência, mercados, varejo e pequenas empresas.  
Código aberto para adaptação e expansão.

---

## 📝 Licença

Este projeto é livre para uso interno. Consulte o repositório para detalhes da licença.
