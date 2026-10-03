# 🛡️ Guardião Pix

> **Sistema Inteligente de Prevenção a Golpes por Engenharia Social**

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://guardiao-pix.streamlit.app)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Database](https://img.shields.io/badge/Database-SQLite-lightgrey.svg)](https://www.sqlite.org/)

---

## 🚀 Aplicação Online (Live Demo)

Aceda à aplicação em tempo real diretamente pelo navegador:  
👉 **[guardiao-pix.streamlit.app](https://guardiao-pix.streamlit.app)**

---

## 📌 Sobre o Projeto

O **Guardião Pix** é uma solução *open-source* focada em mitigação de riscos de fraude financeira decorrentes de técnicas de engenharia social (como falso parente, falsa central telefônica e coação).

A ferramenta realiza uma análise pré-transacional combinando **anonimização de dados (LGPD)**, **análise comportamental** e **base comunitária de denúncias**.

---

## ✨ Principais Funcionalidades

- 🔒 **Proteção LGPD:** Criptografia unidirecional das chaves Pix via Hash SHA-256 antes do processamento.
- 📊 **Cálculo Dinâmico de Risco:** Algoritmo que avalia valor da transação, horário da operação (ex.: madrugadas) e questionários de verificação interpessoal.
- 🚨 **Rede de Alertas Comunitários:** Permite aos utilizadores reportarem abordagens suspeitas para alertar a comunidade.
- 💾 **Persistência de Dados:** Armazenamento seguro de denúncias via SQLite.
- 📈 **Painel de Análise:** Dashboards interativos para monitorização do volume de alertas da rede.

---

## 🛠️ Tecnologias Utilizadas

- **Linguagem:** Python 3.10+
- **Interface & Dashboard:** Streamlit
- **Análise de Dados:** Pandas
- **Persistência de Dados:** SQLite
- **Criptografia / Hashing:** `hashlib` (SHA-256)
- **Hospedagem / Cloud:** Streamlit Community Cloud

---

## 💻 Como Rodar Localmente

1. Clone o repositório:
   ```bash
   git clone [https://github.com/isacunha1207-lab/guardiao-pix.git](https://github.com/isacunha1207-lab/guardiao-pix.git)
   cd guardiao-pix