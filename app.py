import os
import streamlit as st
import base64
from openai import OpenAI

# Función para codificar la imagen en base64
def encode_image(image_file):
    return base64.b64encode(image_file.getvalue()).decode("utf-8")

# Configuración de la página
st.set_page_config(
    page_title="🔎 Análisis de Imagen",
    page_icon="🖼️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Agregar un poquito de CSS para embellecer
st.markdown("""
    <style>
    body {
        background-color: #ffe4e1;
    }
    .stApp {
        background: linear-gradient(to bottom right, #ffe4e1, #ffffff);
        color: #4b2e2e;
        font-family: 'Comic Sans MS', cursive, sans-serif;
    }
    h1, h2, h3 {
        color: #ff69b4;
    }
    .stButton > button {
        background-color: #ff69b4;
        color: white;
        border-radius: 10px;
        font-size: 18px;
        padding: 10px 24px;
        font-weight: bold;
        border: none;
    }
    .stButton > button:hover {
        background-color: #ff85c1;
        color: white;
    }
    .css-1cpxqw2 {
        background: #ffd1dc;
    }
    </style>
""", unsafe_allow_html=True)

# Título principal
st.title("🔍 Análisis de Imagen con IA 🤖🏞️")

# Entrada para la clave de OpenAI
ke = st.text_input('🔑 Ingresa tu clave API de OpenAI:', type="password")
os.environ['OPENAI_API_KEY'] = ke

# Recuperar la API Key
api_key = os.getenv('OPENAI_API_KEY')

# Inicializar cliente OpenAI
client = OpenAI(api_key=api_key)

# Carga de imagen
uploaded_file = st.file_uploader("📂 Sube una imagen para analizar", type=["jpg", "png", "jpeg"])

if uploaded_file:
    with st.expander("🖼️ Vista previa de tu imagen", expanded=True):
        st.image(uploaded_file, caption=uploaded_file.name, use_container_width=True)

# Opción para adicionar detalles
show_details = st.toggle("➕ Añadir detalles sobre la imagen", value=False)

if show_details:
    additional_details = st.text_area(
        "📝 Escribe contexto adicional sobre la imagen:",
        placeholder="Ejemplo: Esta imagen fue tomada en París durante el otoño."
    )

# Botón para analizar
analyze_button = st.button("🔍 Analizar Imagen", type="primary")

# Procesar imagen y enviar solicitud
if uploaded_file is not None and api_key and analyze_button:

    with st.spinner("🛠️ Analizando imagen..."):
        # Codificar imagen
        base64_image = encode_image(uploaded_file)

        prompt_text = "Describe lo que ves en la imagen en español."

        if show_details and additional_details:
            prompt_text += f"\n\nDetalles adicionales proporcionados:\n{additional_details}"

        # Crear los mensajes para enviar
        messages = [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt_text},
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}
                    },
                ],
            }
        ]

        # Solicitar a la API de OpenAI
        try:
            full_response = ""
            message_placeholder = st.empty()

            for completion in client.chat.completions.create(
                model="gpt-4o",
                messages=messages,
                max_tokens=1200,
                stream=True
            ):
                if completion.choices[0].delta.content is not None:
                    full_response += completion.choices[0].delta.content
                    message_placeholder.markdown(full_response + "▌")

            # Finalizar
            message_placeholder.markdown(full_response)

        except Exception as e:
            st.error(f"❌ Ha ocurrido un error: {e}")

# Advertencias si faltan datos
else:
    if not uploaded_file and analyze_button:
        st.warning("⚠️ Por favor sube una imagen antes de analizar.")
    if not api_key:
        st.warning("⚠️ Ingresa tu API Key para continuar.")


