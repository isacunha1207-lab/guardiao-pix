import streamlit as st
import hashlib
import pandas as pd
import datetime
import sqlite3
import re

# Configuração da página
st.set_page_config(page_title="Guardião Pix", page_icon="🛡️", layout="centered")

st.title("🛡️ Guardião Pix")
st.caption("Sistema Inteligente de Prevenção a Golpes por Engenharia Social")

# --- BASE DE DADOS SQLITE ---
def init_db():
    conn = sqlite3.connect('guardiao_pix.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS denuncias (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            chave TEXT NOT NULL,
            motivo TEXT NOT NULL,
            data TEXT NOT NULL
        )
    ''')
    
    c.execute("SELECT COUNT(*) FROM denuncias")
    if c.fetchone()[0] == 0:
        data_atual = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        c.execute(
            "INSERT INTO denuncias (chave, motivo, data) VALUES (?, ?, ?)",
            ("11999998888", "Tentativa de golpe via WhatsApp (Falso parente)", data_atual)
        )
    
    conn.commit()
    conn.close()

def carregar_denuncias():
    conn = sqlite3.connect('guardiao_pix.db')
    df = pd.read_sql_query("SELECT chave, motivo, data FROM denuncias ORDER BY id DESC", conn)
    conn.close()
    return df

def salvar_denuncia(chave, motivo):
    conn = sqlite3.connect('guardiao_pix.db')
    c = conn.cursor()
    data_atual = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    c.execute("INSERT INTO denuncias (chave, motivo, data) VALUES (?, ?, ?)", (chave, motivo, data_atual))
    conn.commit()
    conn.close()

# Inicializa a base de dados
init_db()

# Função de Hash SHA-256 (Anonimização LGPD)
def gerar_hash_lgpd(chave):
    return hashlib.sha256(chave.strip().encode('utf-8')).hexdigest()

# Função para validar DDD em números de telefone
def analisar_ddd(chave):
    apenas_numeros = re.sub(r'\D', '', chave)
    # Verifica se é um número de telefone (10 ou 11 dígitos)
    if len(apenas_numeros) in [10, 11]:
        ddd = apenas_numeros[:2]
        ddds_validos = [
            '11','12','13','14','15','16','17','18','19', # SP
            '21','22','24', # RJ
            '27','28', # ES
            '31','32','33','34','35','37','38', # MG
            '41','42','43','44','45','46', # PR
            '47','48','49', # SC
            '51','53','54','55', # RS
            '61', # DF
            '62','64', # GO
            '63', # TO
            '65','66', # MT
            '67', # MS
            '68', # AC
            '69', # RO
            '71','73','74','75','77', # BA
            '79', # SE
            '81','87', # PE
            '82', # AL
            '83', # PB
            '84', # RN
            '85','88', # CE
            '86','89', # PI
            '91','93','94', # PA
            '92','97', # AM
            '95', # RR
            '96', # AP
            '98','99' # MA
        ]
        if ddd not in ddds_validos:
            return False, f"DDD ({ddd}) inválido ou não mapeado na rede telefônica nacional."
    return True, ""

# Navegação por Abas
aba1, aba2, aba3 = st.tabs(["🔍 Consultar Chave Pix", "🚨 Reportar Suspeita", "⚙️ Painel do Guardião"])

# --- ABA 1: CONSULTAR CHAVE ---
with aba1:
    st.subheader("Verificação Pré-Transacional")
    st.write("Antes de realizar uma transferência, verifique o nível de risco de fraude.")

    col1, col2 = st.columns([2, 1])
    with col1:
        chave_input = st.text_input("Digite a Chave Pix (CPF, Telefone, E-mail ou Chave Aleatória):")
    with col2:
        valor_input = st.number_input("Valor da Transação (R$):", min_value=0.0, value=100.0, step=50.0)

    # Questionário de Engenharia Social
    with st.expander("⚠ Verificação de Engenharia Social (Responda se houver dúvida)"):
        q1 = st.checkbox("A pessoa pediu urgência ou solicitou segredo?")
        q2 = st.checkbox("Você recebeu uma chamada dizendo ser do seu banco ou de uma central de segurança?")
        q3 = st.checkbox("A chave Pix cadastrada pertence a um terceiro desconhecido?")

    if st.button("Consultar Risco da Chave", type="primary"):
        if not chave_input:
            st.warning("Por favor, digite uma chave Pix.")
        else:
            hash_gerado = gerar_hash_lgpd(chave_input)
            st.code(f"Identificador Seguro da Chave (Hash LGPD): {hash_gerado[:20]}...", language="text")

            pontuacao_risco = 0
            motivos = []

            # 1. Análise de DDD
            ddd_valido, msg_ddd = analisar_ddd(chave_input)
            if not ddd_valido:
                pontuacao_risco += 30
                motivos.append(msg_ddd)

            # 2. Horário atípico (22h às 06h)
            hora_atual = datetime.datetime.now().hour
            if hora_atual >= 22 or hora_atual < 6:
                pontuacao_risco += 25
                motivos.append("Transação realizada em horário de alto risco (22h - 06h).")

            # 3. Valor elevado
            if valor_input > 1000:
                pontuacao_risco += 20
                motivos.append("Valor elevado para transação rápida.")

            # 4. Questionário interpessoal
            if q1:
                pontuacao_risco += 30
                motivos.append("Padrão clássico de urgência/coação (Falso parente).")
            if q2:
                pontuacao_risco += 35
                motivos.append("Padrão de falsa central telefônica.")
            if q3:
                pontuacao_risco += 20
                motivos.append("Titularidade da chave divergente.")

            # 5. Base Comunitária SQLite
            df_denuncias = carregar_denuncias()
            denuncias_existentes = df_denuncias[df_denuncias['chave'] == chave_input]
            if not denuncias_existentes.empty:
                qtd = len(denuncias_existentes)
                pontuacao_risco += 50
                motivos.append(f"Chave com {qtd} denúncia(s) ativa(s) na base comunitária.")

            pontuacao_risco = min(pontuacao_risco, 100)

            # Resultado
            st.divider()
            if pontuacao_risco >= 60:
                st.error(f"🔴 Nível de Risco: ALTO ({pontuacao_risco}/100)")
                st.error("Alerta! Padrão com forte indício de fraude por engenharia social.")
            elif pontuacao_risco >= 30:
                st.warning(f"🟡 Nível de Risco: MÉDIO ({pontuacao_risco}/100)")
                st.warning("Atenção! Confirme a identidade do recebedor por outro canal seguro.")
            else:
                st.success(f"🟢 Nível de Risco: BAIXO ({pontuacao_risco}/100)")
                st.success("Nenhuma anomalia significativa encontrada. Prossiga com atenção habitual.")

            if motivos:
                st.write("**Fatores de Risco Detetados:**")
                for m in motivos:
                    st.write(f"- {m}")

# --- ABA 2: REPORTAR SUSPEITA ---
with aba2:
    st.subheader("Reportar Abordagem Suspeita")
    st.write("Registe tentativas de fraude para alertar outros utilizadores da rede.")

    chave_reporte = st.text_input("Chave Pix Suspeita:")
    motivo_reporte = st.text_area("Descreva a abordagem (ex.: ligaram fingindo ser do banco, pedido via WhatsApp):")

    if st.button("Enviar Reporte"):
        if chave_reporte and motivo_reporte:
            salvar_denuncia(chave_reporte, motivo_reporte)
            st.success("Denúncia gravada na base de dados SQLite com sucesso!")
            st.rerun()
        else:
            st.warning("Preencha todos os campos para enviar o reporte.")

# --- ABA 3: PAINEL DO GUARDIÃO ---
with aba3:
    st.subheader("🔒 Acesso Restrito - Equipe de Antifraude")
    
    # Sistema de Autenticação Simples
    if "autenticado" not in st.session_state:
        st.session_state.autenticado = False

    if not st.session_state.autenticado:
        senha_input = st.text_input("Digite a palavra-passe do Administrador:", type="password")
        if st.button("Entrar no Painel"):
            if senha_input == "guardiao123":
                st.session_state.autenticado = True
                st.success("Acesso autorizado!")
                st.rerun()
            else:
                st.error("Palavra-passe incorreta.")
    else:
        st.success("Sessão ativa como Administrador")
        if st.button("Sair"):
            st.session_state.autenticado = False
            st.rerun()

        st.divider()
        df_denuncias = carregar_denuncias()
        
        col_m1, col_m2 = st.columns(2)
        col_m1.metric("Total de Alertas Registados", len(df_denuncias))
        col_m2.metric("Base de Dados", "SQLite Activa")

        if not df_denuncias.empty:
            st.write("**Gráfico: Volume de Denúncias Registadas**")
            st.bar_chart(df_denuncias['chave'].value_counts())

            st.write("**Histórico de Denúncias Recentes:**")
            st.dataframe(df_denuncias, use_container_width=True)

            # Exportação de Relatório CSV
            csv_data = df_denuncias.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Descarregar Relatório Completo (CSV)",
                data=csv_data,
                file_name=f"relatorio_guardiao_pix_{datetime.date.today()}.csv",
                mime="text/csv",
                type="primary"
            )
        else:
            st.info("Nenhuma denúncia registada na base de dados até ao momento.")