# 🧹 Smart CSV/Excel Cleaner & Data Quality Auditor Bot

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Pandas](https://img.shields.io/badge/Pandas-2.1%2B-darkblue.svg)](https://pandas.pydata.org/)
[![ReportLab](https://img.shields.io/badge/ReportLab-PDF-red.svg)](https://www.reportlab.com/)
[![Architecture](https://img.shields.io/badge/Architecture-src--layout%20%7C%20SOLID-success.svg)]()

> Pipeline profissional de engenharia de dados para higienização, padronização, tratamento semântico de ausentes e auditoria de qualidade em arquivos tabulares heterogêneos (**CSV** e **Excel**).

---

## 📌 O Problema que Esta Ferramenta Resolve

No dia a dia corporativo, a ingestão de planilhas de diferentes fornecedores e sistemas costuma ser um processo caótico:
- **Datas Heterogêneas e Conflitantes:** Mistura de padrões (`2024-01-10`, `12/01/2024`, `18-Jan-2024`), que em versões modernas de bibliotecas analíticas frequentemente geram perdas de dados silenciosas.
- **Corrupção Silenciosa (*Silent Data Corruption*):** Scripts amadores costumam converter valores nulos em textos literais `"nan"` ou inventam números médios sem alertar ninguém, distorcendo métricas financeiras e de BI.
- **Formatação de Moeda Quebrada:** Símbolos monetários (`R$`, `$`, `€`), pontos de milhar e vírgulas decimais que impedem análises numéricas downstream.
- **Falta de Rastreabilidade e Auditoria:** Alterações feitas sem gerar relatórios de auditoria que indiquem exatamente o que foi corrigido e quais linhas continham falhas graves de negócio.

---

## 🚀 A Solução

O **Smart CSVCleaner Bot** atua como uma esteira automatizada e desacoplada baseada no padrão profissional **`src-layout`** e princípios **SOLID**:
1. **Desduplicação Atômica:** Elimina linhas idênticas duplicadas preservando a integridade da memória através de `.copy()`.
2. **Higienização Textual Protegida:** Padroniza textos em *Title Case* e e-mails em *lowercase*, utilizando máscaras booleanas (`.notna()`) para garantir que dados nulos não sejam corrompidos para `"nan"`.
3. **Conversão Monetária Vetorizada:** Remove símbolos monetários e converte valores para `float64` com suporte nativo a múltiplos padrões regionais (**Brasil**, **EUA** e **Europa**) via `Enum` tipado.
4. **Padronização Temporal Resiliente (ISO 8601):** Converte múltiplos formatos de data heterogêneos para `YYYY-MM-DD` com `format="mixed"` e `dayfirst` declarativo.
5. **Tratamento Semântico de Ausentes:** Separa de forma inteligente:
   - **Padrões Lógicos:** Valores implícitos óbvios (`discount: 0.0`, `receive_newsletter: False`).
   - **Placeholders Explícitos:** Marcações claras para campos categóricos não preenchidos (`"NOT INFORMED"`).
6. **Motor de Auditoria Independente (*Data Quality*):** Fiscaliza sem alterar os dados, rastreando anomalias de negócio (preços negativos, quantidades zeradas, e-mails ausentes e datas anacrônicas ou futuras).

---

## 📦 Entregáveis da Esteira

Após o processamento, a ferramenta gera automaticamente no diretório `data/processed/`:

1. **`cleaned_data.csv`:** Base 100% higienizada e padronizada em CSV UTF-8, sem colunas fantasmas de índice (`index=False`).
2. **`cleaned_data.xlsx`:** Planilha nativa do Excel pronta para consumo analítico.
3. **`AUDIT.md`:** Relatório de auditoria executivo em formato Markdown com tabela tabulada.
4. **`AUDIT.pdf`:** Relatório visual executivo em PDF (A4 Paisagem) com tabela zebrada profissional estilizada via **ReportLab**.

---

## 🏗️ Arquitetura do Projeto

```text
Smart_CSVCleaner_Bot/
│
├── .gitignore
├── pyproject.toml              # Especificação de empacotamento (PEP 621)
├── requirements.txt            # Dependências mínimas do pipeline
├── README.md                   # Documentação do projeto
│
├── data/
│   ├── raw/                    # Entrada de arquivos brutos
│   │   └── raw_data.csv
│   └── processed/              # Saídas limpas e relatórios gerados
│       ├── cleaned_data.csv
│       ├── cleaned_data.xlsx
│       ├── AUDIT.md
│       └── AUDIT.pdf
│
└── src/
    └── cleaner/
        ├── __init__.py
        ├── __main__.py         # Entrypoint da CLI
        ├── config.py           # Regras de negócio, Dataclasses e Enums
        ├── pipeline.py         # Orquestrador central (Service Layer)
        │
        ├── core/               # Infraestrutura e utilitários agnósticos
        │   ├── __init__.py
        │   ├── exceptions.py   # Hierarquia de exceções personalizadas
        │   └── logger.py       # Logging estruturado
        │
        ├── reader/             # Ingestão de dados (CSV / Excel)
        │   ├── __init__.py
        │   └── loader.py
        │
        ├── transformator/      # Microsserviços puros de transformação
        │   ├── __init__.py
        │   ├── deduplication.py
        │   ├── string_cleaner.py
        │   ├── currency_cleaner.py
        │   ├── date_normalizer.py
        │   └── missings_handler.py
        │
        ├── quality/            # Módulo de observabilidade e auditoria
        │   ├── __init__.py
        │   ├── auditor.py
        │   └── report_gen.py
        │
        └── exporter/           # Exportadores multi-formato
            ├── __init__.py
            └── writer.py
```

---

## ⚙️ Como Usar

### 1. Clonar o repositório e criar o ambiente virtual

```bash
git clone https://github.com/Pedroguij0/CSV_Cleaner.git
cd CSV_Cleaner

python -m venv .venv
# No Windows:
.venv\Scripts\activate
# No Linux/Mac:
source .venv/bin/activate
```

### 2. Instalar as dependências

```bash
pip install -r requirements.txt
```

### 3. Executar o pipeline

Coloque o seu arquivo de entrada em `data/raw/` (ex: `data/raw/raw_data.csv`) e execute:

```bash
python -m src.cleaner
```

Você verá o log detalhado no terminal e os arquivos serão gerados instantaneamente em `data/processed/`.

---

## 📋 Exemplo de Saída da Auditoria (`AUDIT.md`)

```markdown
########## Data Quality & Cleansing Audit Report ##########

##### 1. Metrics Summary #####
- **Initial Rows:** 12
- **Duplicates Removed:** 2
- **Final Clean Rows:** 10
- **Encountered Anomalies:** 4

##### 2. Critical Anomalies Table #####
| Record ID | Anomaly Type     | Details                        | Raw Value     | Column        | Warning Message                                            |
| :-------- | :--------------- | :----------------------------- | :------------ | :------------ | :--------------------------------------------------------- |
| `TX1006`  | Negative Price   | Price:-90.0                    | -90.0         | unity_price   | Price bellow zero. Please, enter a valid value.            |
| `TX1005`  | Invalid Quantity | Quantity: 0                    | 0             | quantity      | Invalid Quantity. Please, enter a valid quantity.          |
| `TX1005`  | Missing Email    | Missing Email of: Marcos Lima  | NOT INFORMED  | client_email  | Missing or corrupted email. Please, enter a valid Email.   |
| `TX1007`  | Invalid Date     | Cannot Parse the date: nan     | nan           | bought_date   | Missing or Invalid date. Please, enter a valid date        |
```

---

## 👤 Autor

Desenvolvido por **Pedro Guijo**  
GitHub: [@Pedroguij0](https://github.com/Pedroguij0)
