import json
import os

import requests
import streamlit as st
from dotenv import load_dotenv

load_dotenv()
context = [
    {
        'role': 'system',
        'content': """
            Eres OrderBot, un servicio automatizado de recogida de pedidos para Pizzería la Llama.
            Primero saludas al cliente, luego atiendes el pedido, y luego preguntas si es para recoger en la tienda o para entregar en alguna dirección. 
            Esperas a tener todo el pedido, luego lo resumes y compruebas por última vez si el cliente quiere añadir algo más. 
            
            Si es una entrega, pide una dirección. 
            Por último, recoge el método de pago.
            
            Asegúrate de aclarar todas las opciones, extras y tallas para identificar de forma única el artículo del menú.
            Respondes con un estilo breve, muy conversacional y amigable. 
            
            Nuestro menú incluye:

                Pizzas (pequeña, mediana, grande):
                - Pizza de pepperoni: $7.00, $10.00, $12.95
                - Pizza de queso: $6.50, $9.25, $10.95
                - Pizza de berenjena: $6.75, $9.75, $11.95

                Extras:
                - Patatas fritas (pequeña, grande): $3.50, $4.50
                - Ensalada griega: $7.25

                Ingredientes adicionales:
                - Queso extra: $2.00
                - Champiñones: $1.50
                - Salchicha: $3.00
                - Bacon canadiense: $3.50
                - Salsa La LLAMA: $1.50
                - Pimientos: $1.00

                Bebidas (pequeña, mediana, grande):
                - Coca cola: $1.00, $2.00, $3.00
                - Sprite: $1.00, $2.00, $3.00
                - Agua embotellada 1L: $2.00
            """
    },
    {
        'role': 'system',
        'content': """
            Recuerda que puedes hacer preguntas claras y específicas para ayudar al cliente a tomar decisiones.
            Por ejemplo, puedes preguntar "¿Qué tamaño de pizza te gustaría? Tenemos tamaños pequeño, mediano y grande".
            También puedes ofrecer opciones adicionales, como "¿Te gustaría agregar algún ingrediente extra a tu pizza?".
            Si el cliente tiene alguna pregunta o necesita ayuda, no dudes en ofrecer asistencia.
            Devuelve tus respuestas de forma clara estructurada y concisa.
            Si no existe la opción que el cliente está buscando, puedes decir "Lo siento, pero no tenemos esa opción en el menú".
            """
    }
]


if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
    
auth_token = os.getenv("AUTH_TOKEN")

def chat_with_llama(messages):

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f"Bearer {auth_token}"
    }
    url = 'https://api.awanllm.com/v1/chat/completions'
    
    payload = json.dumps({
        "model": "Meta-Llama-3-8B-Instruct",
        "messages": messages,
    })
    
    response = requests.request("POST", url, headers=headers, data=payload).json()
    
    if 'choices' in response:
        if len(response['choices']) > 0:
            return response['choices'][0]['message']['content']
        else:
            st.error("La respuesta de la API contiene 'choices' pero está vacía.")
    else:
        st.error("Error en la respuesta de la API: 'choices' no encontrado")
        st.json(response)
    
    return "Lo siento, hubo un error al procesar tu solicitud. Aquí está la respuesta de la API: " + str(response)


def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


local_css("style/style.css")


st.title("Pizzería 🦙 Bot")


chat_container = st.container()
with chat_container:
    for entry in st.session_state.chat_history:
        if entry['role'] == 'user':
            st.markdown(f'<div class="human-bubble"">{entry["content"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="ai-bubble">{entry["content"]}</div>', unsafe_allow_html=True)


user_input = st.text_input("Escribe un mensaje", "")



if st.button("Enviar"):
    if user_input:
        
        st.session_state.chat_history.append({'role': 'user', 'content': user_input})
        previous_messages = context + st.session_state.chat_history
        
        response = chat_with_llama(previous_messages)
        
        st.session_state.chat_history.append({'role': 'assistant', 'content': response})

        st.rerun()
