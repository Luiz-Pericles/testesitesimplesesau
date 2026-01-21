import streamlit as st
import pandas as pd

# Configuração da página para parecer um aplicativo profissional
st.set_page_config(page_title="Calculadora de Dor - Pesquisa", page_icon="🩺", layout="centered")

# --- 1. Lógica de Armazenamento (Session State) ---
# Como o Streamlit recarrega a cada clique, precisamos salvar os dados na memória temporária
if 'banco_dados' not in st.session_state:
    st.session_state['banco_dados'] = pd.DataFrame(columns=[
        "Nome do Médico", "Nome do Paciente", "Score Total", "Tipo de Dor", 
        "Q1-Queimação", "Q1-Frio Doloroso", "Q1-Choque",
        "Q2-Formigamento", "Q2-Alfinetada", "Q2-Adormecimento", "Q2-Coceira",
        "Q3-Hipoestesia Toque", "Q3-Hipoestesia Agulha", "Q4-Escovação"
    ])

# --- 2. Cabeçalho e Dados Iniciais ---
st.title("🩺 Avaliação Clínica de Dor")
st.markdown("### Ferramenta de Coleta de Dados para Pesquisa")

with st.expander("📝 Dados do Atendimento", expanded=True):
    col1, col2 = st.columns(2)
    with col1:
        medico = st.text_input("Nome do Médico Cirurgião")
    with col2:
        paciente = st.text_input("Nome do Paciente")

st.divider()

# --- 3. O Questionário (Lógica DN4) ---
# Checkbox retorna True (1) se marcado, False (0) se não. Isso facilita a soma.
st.subheader("Avaliação dos Sintomas")
st.info("Marque a caixa apenas se a resposta for **SIM**.")

score = 0
respostas = {}

# Questão 1
st.markdown("**Questão 1: A dor tem uma ou mais das seguintes características?**")
c1, c2, c3 = st.columns(3)
respostas["Q1-Queimação"] = c1.checkbox("1. Queimação")
respostas["Q1-Frio Doloroso"] = c2.checkbox("2. Sensação de frio dolorosa")
respostas["Q1-Choque"] = c3.checkbox("3. Choque elétrico")

# Questão 2
st.markdown("**Questão 2: Há presença de um ou mais sintomas na mesma área?**")
c4, c5, c6, c7 = st.columns(4)
respostas["Q2-Formigamento"] = c4.checkbox("4. Formigamento")
respostas["Q2-Alfinetada"] = c5.checkbox("5. Alfinetada e agulhada")
respostas["Q2-Adormecimento"] = c6.checkbox("6. Adormecimento")
respostas["Q2-Coceira"] = c7.checkbox("7. Coceira")

# Questão 3
st.markdown("**Questão 3: O exame físico revela na área dolorosa:**")
c8, c9 = st.columns(2)
respostas["Q3-Hipoestesia Toque"] = c8.checkbox("8. Hipoestesia ao toque")
respostas["Q3-Hipoestesia Agulha"] = c9.checkbox("9. Hipoestesia à picada de agulha")

# Questão 4
st.markdown("**Questão 4: A dor pode ser causada ou aumentada por:**")
respostas["Q4-Escovação"] = st.checkbox("10. Escovação")

# --- 4. Processamento da Lógica ---
# Soma todos os valores True (cada True vale 1 ponto)
score_total = sum(respostas.values())

# Definição do Diagnóstico
if score_total >= 4:
    tipo_dor = "Dor Neuropática"
    cor_resultado = "error" # Vermelho no Streamlit
else:
    tipo_dor = "Dor Nociceptiva"
    cor_resultado = "success" # Verde no Streamlit

# --- 5. Exibição do Resultado em Tempo Real ---
st.divider()
col_res1, col_res2 = st.columns(2)
with col_res1:
    st.metric(label="Score Total (Sim)", value=f"{score_total}/10")
with col_res2:
    if score_total >= 4:
        st.error(f"### Diagnóstico: {tipo_dor}")
    else:
        st.success(f"### Diagnóstico: {tipo_dor}")

# --- 6. Botão para Salvar na Tabela ---
if st.button("💾 Salvar Paciente na Lista"):
    if not paciente or not medico:
        st.warning("⚠️ Preencha o nome do médico e do paciente antes de salvar.")
    else:
        # Cria um dicionário com todos os dados
        novo_registro = {
            "Nome do Médico": medico,
            "Nome do Paciente": paciente,
            "Score Total": score_total,
            "Tipo de Dor": tipo_dor,
            **respostas # Desempacota as respostas (True/False)
        }
        
        # Adiciona ao DataFrame na memória
        st.session_state['banco_dados'] = pd.concat(
            [st.session_state['banco_dados'], pd.DataFrame([novo_registro])], 
            ignore_index=True
        )
        st.success(f"Paciente {paciente} salvo com sucesso!")

# --- 7. Área de Exportação e Visualização ---
st.divider()
st.subheader("📂 Pacientes Registrados")

if not st.session_state['banco_dados'].empty:
    # Mostra a tabela interativa
    st.dataframe(st.session_state['banco_dados'])
    
    # Botão de Download
    csv = st.session_state['banco_dados'].to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Baixar Planilha Completa (CSV)",
        data=csv,
        file_name="resultado_pesquisa_dor.csv",
        mime="text/csv",
    )
else:
    st.info("Nenhum paciente registrado ainda.")