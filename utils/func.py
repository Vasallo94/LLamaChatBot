import json
import os

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
    
    try:
        response = requests.post(url, headers=headers, data=payload, timeout=30)
        response.raise_for_status()  # Raise an exception for bad status codes
        
        data = response.json()
        
        if 'choices' in data and data['choices']:
            return data['choices'][0]['message']['content']
        else:
            st.warning("La respuesta de la API no contiene 'choices' o está vacía.")
            st.json(data)
            return "Lo siento, no pude generar una respuesta. Por favor, inténtalo de nuevo."
    
    except requests.exceptions.RequestException as e:
        st.error(f"Error en la solicitud a la API: {e}")
        return "Lo siento, hubo un problema al comunicarse con el servicio. Por favor, inténtalo de nuevo más tarde."
    
    except json.JSONDecodeError as e:
        st.error(f"Error al decodificar la respuesta JSON: {e}")
        st.text(response.text)  # Display the raw response
        return "Lo siento, recibí una respuesta inesperada del servicio. Por favor, inténtalo de nuevo."
    
    except Exception as e:
        st.error(f"Error inesperado: {e}")
        return "Lo siento, ocurrió un error inesperado. Por favor, inténtalo de nuevo."