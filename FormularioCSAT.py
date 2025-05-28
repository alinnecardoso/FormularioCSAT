
import streamlit as st
import gspread
import json
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

# Autenticação segura com Google Sheets via secrets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
credentials = json.loads(st.secrets["gcp_service_account"])
creds = ServiceAccountCredentials.from_json_keyfile_dict(credentials, scope)
client = gspread.authorize(creds)

# Conecta na aba "Respostas_CSAT"
sheet = client.open_by_key("1iT8qsuCqCpm-59PsfAe8B1dmwHg4gX7rJ09x-b_43sg").worksheet("Respostas_CSAT")

# Formulário visualmente melhorado
st.set_page_config(page_title="Formulário de CSAT", layout="centered", initial_sidebar_state="collapsed")
st.title("📋 Formulário de CSAT")

# --- Seção 1: Informações da empresa ---
st.markdown("### 🏢 Informações da Empresa")
col1, col2 = st.columns(2)
with col1:
    empresa = st.text_input("Empresa (igual ao nome do grupo no WhatsApp)", placeholder="Ex: Loja das Canecas")
    custid = st.text_input("CustID", placeholder="Ex: 12345")
with col2:
    consultor = st.text_input("Nome do consultor", placeholder="Ex: João Silva")

# --- Seção 2: Avaliação da Reunião ---
st.markdown("### 🤝 Avaliação da Reunião")
satisfeito = st.radio("Você está satisfeito(a) com as reuniões e com o atendimento do(a) consultor(a)?", ["Sim", "Não"])
relacionamento = st.slider("Nota de relacionamento com o assessor da conta", 1, 5, 3)
resultados = st.slider("Nota de acordo com os resultados apresentados até o momento", 1, 5, 3)

# --- Seção 3: Feedback e sugestões ---
st.markdown("### 💬 Feedback e Sugestões")
assuntos = st.text_area("Quais assuntos gostaria que abordássemos mais daqui pra frente? (Explique o motivo)")
sugestoes = st.text_area("Sugestões de melhorias")

# --- Seção 4: Resultados e alinhamento ---
st.markdown("### 📈 Resultados e Alinhamento")
col3, col4 = st.columns(2)
with col3:
    resultados_negocio = st.radio("As ações discutidas têm gerado resultados para o seu negócio?", ["Sim", "Não", "Parcialmente"])
with col4:
    objetivos_atuais = st.radio("Os temas abordados estão alinhados com seus objetivos atuais?", ["Sim", "Não", "Parcialmente"])

situacao = st.selectbox("Situação atual da parceria", ["Ativo", "Inativo", "Pausado", "Outro"])

# --- Seção 5: Observações finais ---
st.markdown("### 📝 Observações Finais")
observacoes = st.text_area("Caso queira deixar algum comentário adicional (opcional)", placeholder="Ex: Estamos aguardando retorno sobre a proposta...")

# --- Cálculo automático ---
media_notas = round((relacionamento + resultados) / 2, 2)

# --- Botão de envio ---
if st.button("📤 Enviar Resposta"):
    if not empresa or not consultor:
        st.warning("⚠️ Por favor, preencha os campos obrigatórios: Empresa e Consultor.")
    else:
        data = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        valores = [
            data, empresa, custid, consultor,
            satisfeito, relacionamento, resultados,
            assuntos, sugestoes,
            resultados_negocio, objetivos_atuais,
            media_notas, situacao, observacoes
        ]
        sheet.append_row(valores)
        st.success("✅ Resposta enviada com sucesso!")