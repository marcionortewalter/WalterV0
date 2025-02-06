import streamlit as st

from graph import graph

from uuid import uuid4

import json

# Configuração da página
st.set_page_config(
    page_title="🧙‍♂️ Walter",
    layout="centered",
    initial_sidebar_state="collapsed"
)
if "thread_id" not in st.session_state:
    st.session_state.thread_id = str(uuid4())

config = {"configurable": {"thread_id": st.session_state.thread_id}}

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

# Inicializar histórico de mensagens
if "messages" not in st.session_state:
    st.session_state.messages = []

# Container principal
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
                    {"messages": [("human", prompt)]},
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
                                # Atualizar resposta
                                full_response = message.content
                                if len(full_response) > 10000:
                                    full_response = full_response[:10000] + " ... (truncated)"
                                message_placeholder.markdown(full_response)
                    
                    except Exception as e:
                        message_placeholder.markdown("Ops, ocorreu um erro. Por favor, tente novamente.")
                        print(f"Erro ao processar mensagem: {str(e)}")
                        continue
                
                # Adicionar resposta final ao histórico
                if full_response:
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": full_response
                    })

