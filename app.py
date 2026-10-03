import datetime
import streamlit as st
from risk_engine import gerar_hash_chave, calcular_risk_score

st.set_page_config(
    page_title="Guardião Pix - Prevenção a Golpes",
    page_icon="🛡️",
    layout="centered"
)

if "banco_chaves" not in st.session_state:
    st.session_state["banco_chaves"] = {
        gerar_hash_chave("golpe@pixfalso.com.br"): [
            {"data": datetime.datetime.now() - datetime.timedelta(hours=2), "confiabilidade_usuario": 0.9, "tipo": "Falso Parente"},
            {"data": datetime.datetime.now() - datetime.timedelta(hours=5), "confiabilidade_usuario": 0.8, "tipo": "Falsa Central"},
            {"data": datetime.datetime.now() - datetime.timedelta(days=1), "confiabilidade_usuario": 1.0, "tipo": "Falso Parente"}
        ],
        gerar_hash_chave("11999998888"): [
            {"data": datetime.datetime.now() - datetime.timedelta(days=10), "confiabilidade_usuario": 0.6, "tipo": "Produto Não Entregue"}
        ]
    }

if "guardiao" not in st.session_state:
    st.session_state["guardiao"] = {
        "nome": "Maria Silva (Filha)",
        "telefone": "5511987654321",
        "email": "maria.silva@email.com"
    }

st.title("🛡️ Guardião Pix")
st.subheader("Sistema Inteligente de Prevenção a Golpes por Engenharia Social")

aba1, aba2, aba3 = st.tabs(["🔍 Consultar Chave Pix", "🚨 Reportar Suspeita", "⚙️ Painel do Guardião"])

with aba1:
    st.markdown("### Verificação Pré-Transacional")
    st.write("Antes de realizar uma transferência, insira a chave Pix para verificar o nível de risco de fraude.")
    chave_input = st.text_input("Digite a Chave Pix (CPF, Telefone, E-mail ou Chave Aleatória):")
    
    with st.expander("⚠ Verificação de Engenharia Social (Responda se houver dúvida)"):
        q1 = st.checkbox("A pessoa solicitou urgência dizendo ser um caso de emergência ou saúde?")
        q2 = st.checkbox("A pessoa afirmou que mudou de número de telefone recentemente?")
        q3 = st.checkbox("O recebedor pediu para que você não contasse sobre a transferência para ninguém?")
    
    gatilhos_ativados = sum([q1, q2, q3])
    factor_alpha = 1.0 + (gatilhos_ativados * 0.25)

    if st.button("Consultar Risco da Chave", type="primary"):
        if not chave_input:
            st.warning("Por favor, digite uma chave Pix para consultar.")
        else:
            hash_chave = gerar_hash_chave(chave_input)
            denuncias_encontradas = st.session_state["banco_chaves"].get(hash_chave, [])
            score_calculado = calcular_risk_score(
                denuncias=denuncias_encontradas,
                alpha=factor_alpha
            )
            st.divider()
            st.markdown(f"**Identificador Seguro da Chave (Hash LGPD):** `{hash_chave[:16]}...`")

            if score_calculado < 30.0:
                st.success(f"### 🟢 Nível de Risco: BAIXO ({score_calculado}/100)")
                st.write("Nenhuma anomalia significativa encontrada. Prossiga com atenção habitual.")
            elif 30.0 <= score_calculado < 70.0:
                st.warning(f"### 🟡 Nível de Risco: MÉDIO ({score_calculado}/100)")
                st.write("Atenção! Esta chave possui registros prévios ou o contexto indica possível tentativa de engenharia social.")
                guardiao = st.session_state["guardiao"]
                link_whatsapp = f"https://wa.me/{guardiao['telefone']}?text=Olá%20{guardiao['nome']},%20estou%20prestes%20a%20fazer%20um%20Pix%20e%20o%20app%20indicou%20risco%20médio.%20Pode%20me%20ajudar?"
                st.link_button("📲 Confirmar com o Guardião pelo WhatsApp", link_whatsapp)
            else:
                st.error(f"### 🔴 Nível de Risco: CRÍTICO ({score_calculado}/100)")
                st.write("🛑 **ALERTA DE GOLPE PROVÁVEL!** Esta chave apresenta histórico recente recorrente de denúncias.")
                st.markdown("#### **Ação Recomendada:** Não realize a transferência!")
                guardiao = st.session_state["guardiao"]
                link_wa = f"https://wa.me/{guardiao['telefone']}?text=URGENTE:%20{guardiao['nome']},%20o%20app%20bloqueou%20um%20Pix%20por%20alto%20risco%20de%20golpe.%20Preciso%20falar%20com%20você!"
                
                col1, col2 = st.columns(2)
                with col1:
                    st.link_button("💬 Falar com Guardião no WhatsApp", link_wa, type="primary")
                with col2:
                    st.markdown(f"[📞 Ligar para o Guardião](tel:+{guardiao['telefone']})")

with aba2:
    st.markdown("### Reportar Tentativa de Golpe")
    nova_chave = st.text_input("Chave Pix do Golpista:")
    tipo_golpe = st.selectbox("Qual foi o tipo de abordagem?", ["Falso Parente (WhatsApp)", "Falsa Central Telefônica", "Produto/Serviço Falso", "Outros"])
    detalhes = st.text_area("Descreva brevemente o ocorrido:")
    if st.button("Registrar Denúncia"):
        if not nova_chave:
            st.error("Informe a chave Pix suspeita.")
        else:
            hash_nova = gerar_hash_chave(nova_chave)
            nova_denuncia = {"data": datetime.datetime.now(), "confiabilidade_usuario": 0.85, "tipo": tipo_golpe}
            if hash_nova in st.session_state["banco_chaves"]:
                st.session_state["banco_chaves"][hash_nova].append(nova_denuncia)
            else:
                st.session_state["banco_chaves"][hash_nova] = [nova_denuncia]
            st.success("Denúncia registrada com sucesso! Base de dados atualizada.")

with aba3:
    st.markdown("### Configuração da Rede de Apoio (Guardião)")
    nome_g = st.text_input("Nome do Guardião:", value=st.session_state["guardiao"]["nome"])
    tel_g = st.text_input("Telefone (com DDD e sem espaços):", value=st.session_state["guardiao"]["telefone"])
    email_g = st.text_input("E-mail do Guardião:", value=st.session_state["guardiao"]["email"])
    if st.button("Salvar Dados do Guardião"):
        st.session_state["guardiao"] = {"nome": nome_g, "telefone": tel_g, "email": email_g}
        st.success("Informações do guardião atualizadas com sucesso!")