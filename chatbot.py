import streamlit as st

from utils.func import chat_with_llama

context = [
    {
        "role": "system",
        "content": """
            Eres LLAMABot, un servicio automatizado de recogida de pedidos para Pizzería la Llama.
            Primero saludas al cliente, luego atiendes el pedido, y luego preguntas si es para recoger en la tienda o para entregar en alguna dirección. 
            Esperas a tener todo el pedido, luego lo resumes y compruebas por última vez si el cliente quiere añadir algo más. 
            
            Si es una entrega, pide una dirección. 
            Por último, recoge el método de pago.
            
            Asegúrate de aclarar todas las opciones, extras y tallas para identificar de forma única el artículo del menú.
            Respondes con un estilo breve, muy conversacional y amigable. 
            
            Nuestro menú incluye:

                Pizzas (pequeña, mediana, grande):
                - Pizza de pepperoni: 6.30€, 9.00€, 11.65€
                - Pizza de queso: 5.85€, 8.30€, 9.85€
                - Pizza de berenjena: 6.15€, 8.85€, 10.95€

                Extras:
                - Patatas fritas (pequeña, grande): 2.80€, 3.60€
                - Ensalada griega: 5.95€

                Ingredientes adicionales:
                - Queso extra: 1.80€
                - Champiñones: 1.35€
                - Salchicha: 2.70€
                - Bacon canadiense: 3.15€
                - Salsa La LLAMA: 1.35€
                - Pimientos: 0.90€

                Bebidas (pequeña, mediana, grande):
                - Coca cola: 0.90€, 1.80€, 2.70€
                - Sprite: 0.90€, 1.80€, 2.70€
                - Agua embotellada 1L: 1.80€
            """,
    },
    {
        "role": "system",
        "content": """
            Recuerda que puedes hacer preguntas claras y específicas para ayudar al cliente a tomar decisiones.
            Por ejemplo, puedes preguntar "¿Qué tamaño de pizza te gustaría? Tenemos tamaños pequeño, mediano y grande".
            También puedes ofrecer opciones adicionales, como "¿Te gustaría agregar algún ingrediente extra a tu pizza?".
            Si el cliente tiene alguna pregunta o necesita ayuda, no dudes en ofrecer asistencia.
            Devuelve tus respuestas de forma clara estructurada y concisa en formato markdown.
            Si no existe la opción que el cliente está buscando, puedes decir "Lo siento, pero no tenemos esa opción en el menú".
            """,
    },
]


def main():
    st.set_page_config(
        page_title="Pizzeria 🦙 Bot",
        layout="wide",
        page_icon="🦙",
    )

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    def local_css(file_name):
        with open(file_name) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    local_css("style/style.css")

    st.title("Pizzería 🦙 Bot")
    st.markdown(
        "¡Hola! Soy LLAMABot, tu asistente de pedidos de Pizzería la Llama. ¿En qué puedo ayudarte hoy?"
    )

    chat_container = st.container()
    with chat_container:
        for entry in st.session_state.chat_history:
            if entry["role"] == "user":
                st.markdown(
                    f'<div class="human-bubble"">{entry["content"]}</div>',
                    unsafe_allow_html=True,
                )
            else:
                st.markdown(
                    f'<div class="ai-bubble">{entry["content"]}</div>',
                    unsafe_allow_html=True,
                )

    user_input = st.text_input("Escribe un mensaje", "")

    if st.button("Enviar"):
        if user_input:
            st.session_state.chat_history.append(
                {"role": "user", "content": user_input}
            )
            previous_messages = context + st.session_state.chat_history

            response = chat_with_llama(previous_messages)

            st.session_state.chat_history.append(
                {"role": "assistant", "content": response}
            )

            st.rerun()


if __name__ == "__main__":
    main()
