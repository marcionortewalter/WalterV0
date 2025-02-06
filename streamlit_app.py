import streamlit as st
from uuid import uuid4
import json
from google_auth_oauthlib import get_user_credentials

from streamlit_google_signin import st_google_signin
from graph import graph

# Configuração da página
st.set_page_config(
    page_title="🧙‍♂️ Walter",
    layout="centered",
    initial_sidebar_state="collapsed"
)
if "thread_id" not in st.session_state:
    st.session_state.thread_id = str(uuid4())
if "user" not in st.session_state:
    st.session_state.user = None
if "messages" not in st.session_state:
    st.session_state.messages = []

config = {"configurable": {"thread_id": st.session_state.thread_id,
                            "user_email": st.session_state.user["email"] if st.session_state.user else None,
                              "user_name": st.session_state.user["name"] if st.session_state.user else None}}

# CSS personalizado para corresponder ao estilo do frontend
st.markdown("""
    <style>
    .stApp {
        background-color: #f5f5f0;
    }
    
    /* Estilo do cabeçalho */
    .header {
        border-bottom: 2px solid #F3D03E;
        margin-bottom: 1rem;
    }
    
    .title {
        font-family: monospace;
        font-size: 2rem;
        font-weight: bold;
        color: #000000;
    }
    
    /* Remove bordas padrão do Streamlit */
    .stTextInput > div > div > input {
        border: 1px solid #e2e8f0;
        border-radius: 0.375rem;
    }
    
    .stButton > button {
        background-color: #000000;
        color: white;
        border-radius: 0.375rem;
    }
    
    [data-testid="stChatInput"] {
        position: fixed;
        bottom: 0;
        margin: 10px auto;
        background: #f5f5f0;
        z-index: 100;
    }
    </style>
    """, unsafe_allow_html=True)

# Cabeçalho
st.markdown('<div class="header"><h1 class="title">🧙‍♂️ Walter</h1></div>', unsafe_allow_html=True)
st.markdown("<div style='font-size: 10px;'>Walter é um assistente virtual em desenvolvimento. Suas informações podem estar desatualizadas.</div>", unsafe_allow_html=True)
st.markdown("<div style='font-size: 10px;'>Ele pode acessar documentos internos, fazer consultas em algumas tabelas do attio (dados de 21/01)e criar novas tasks no attio. Outras features estão em desenvolvimento, bem como a atualização de texto incremental.</div>", unsafe_allow_html=True)

# Verificação de login antes de mostrar o chat
if not st.session_state.user:
    token = st_google_signin(st.secrets.web_client_id)
    if token is None:
        st.stop()
    st.session_state.user = token

# Adicionar botão de logout na sidebar
if st.sidebar.button("Logout", type="primary"):
    st.session_state.user = None
    st.session_state.credentials = None
    st.rerun()

with st.sidebar:
    st.subheader("Informações do usuário")
    st.write(st.session_state.user["name"])
    st.write(st.session_state.user["email"])

# Container principal
if st.session_state.user:
    with st.container():
        # Container para mensagens
        message_container = st.container()
        
        # Container para input
        input_container = st.container()
        
        # Área de mensagens
        with message_container:
            # Exibir histórico
            for message in st.session_state.messages:
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])
        
        # Área de input
        with input_container:
            if prompt := st.chat_input("Digite sua mensagem"):
                # Adicionar mensagem do usuário ao histórico
                st.session_state.messages.append({"role": "user", "content": prompt})
                
                # Exibir mensagem do usuário
                with st.chat_message("user"):
                    st.markdown(prompt)
                
                # Exibir resposta do assistente
                with st.chat_message("assistant"):
                    message_placeholder = st.empty()
                    full_response = ""
                    
                    # Stream da resposta
                    for step in graph.stream(
                        {"messages": [("human", prompt + f"\n\nYou are helping {config['configurable']['user_name']} ({config['configurable']['user_email']}).")]},
                        stream_mode="values",
                        config=config
                    ):
                        try:
                            message = step.get("messages")
                            if message:
                                if isinstance(message, list):
                                    message = message[-1]
                                
                                # Ignorar mensagens do usuário
                                if hasattr(message, 'type') and message.type == 'human':
                                    continue
                                
                                # Processar tool calls
                                if "tool_calls" in str(message):
                                    tool_name = message.tool_calls[0]["name"]
                                    tool_args = json.dumps(message.tool_calls[0]["args"], indent=2, ensure_ascii=False)
                                    message_placeholder.markdown(f"🔧 Consultando: {tool_name}")
                                else:
                                    # Atualizar resposta de forma incremental
                                    if hasattr(message, 'content'):
                                        new_content = message.content
                                        if new_content != full_response:  # Apenas atualiza se houver mudança
                                            full_response = new_content
                                            if len(full_response) > 10000:
                                                full_response = full_response[:10000] + " ... (truncated)"
                                            message_placeholder.markdown(full_response + "|")
                        
                        except Exception as e:
                            message_placeholder.markdown("Opa, parece que os servidores estão ocupados.")
                            print(f"Erro ao processar mensagem: {str(e)}")
                            continue
                    
                    # Adicionar resposta final ao histórico
                    if full_response:
                        st.session_state.messages.append({
                            "role": "assistant",
                            "content": full_response
                        })

