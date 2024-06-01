
import os 
import json
import requests
import streamlit as st
from dotenv import load_dotenv
load_dotenv()



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