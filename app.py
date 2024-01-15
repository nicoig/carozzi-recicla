# Para crear el requirements.txt ejecutamos 
# pipreqs --encoding=utf8 --force

# Primera Carga a Github
# git init
# git add .
# git remote add origin https://github.com/nicoig/carozzi-recicla.git
# git commit -m "Initial commit"
# git push -u origin master

# Actualizar Repo de Github
# git add .
# git commit -m "Se actualizan las variables de entorno"
# git push origin master

# En Render
# agregar en variables de entorno
# PYTHON_VERSION = 3.9.12

# git remote set-url origin https://github.com/nicoig/carozzi-recicla.git
# git remote -v
# git push -u origin main


################################################
##


import streamlit as st
import base64
from langchain.chat_models import ChatOpenAI
from langchain.schema.messages import HumanMessage, AIMessage
from dotenv import load_dotenv, find_dotenv
from openai import OpenAI
from langchain.prompts import PromptTemplate
from langchain.schema import StrOutputParser
import streamlit as st
import requests
import os
from dotenv import load_dotenv
from io import BytesIO

# Cargar las variables de entorno para las claves API
load_dotenv(find_dotenv())

# Función para codificar imágenes en base64
def encode_image(image_file):
    return base64.b64encode(image_file.read()).decode('utf-8')


# Configuración de la página para utilizar todo el layout
st.set_page_config(layout="centered")  # Puedes cambiar a "wide" si prefieres

# CSS para ocultar la barra de menú y el pie de página de Streamlit
hide_streamlit_style = """
            <style>
            /* Ocultar el menú Hamburguesa */
            #MainMenu {visibility: hidden;}
            /* Ocultar el pie de página de Streamlit */
            footer {visibility: hidden;}
            /* Ocultar la barra de herramientas de Streamlit */
            header {visibility: hidden;}
            /* Quitar el espacio extra en la parte superior */
            .css-1d391kg {padding-top: 0px;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# Configura el título y subtítulo de la aplicación en Streamlit

# Estableciendo la franja superior
st.image("img/franja_inferior_1.png")

# Agregar un espacio o salto
st.write("")

# Estableciendo el logo de Carozzi
st.image("img/logo_carozzi.png", width=200)

st.markdown("""
    <style>
    .small-font {
        font-size:15px !important;
    }
    </style>
    <p class="small-font">¡Hola! soy el Mono de Carozzi 🐵. Te daré algunos consejos de cómo puedes reciclar tu producto, sólo toma una fotografía del producto que estás consumiendo y listo.</p>
    """, unsafe_allow_html=True)

# Imagen de cabecera
st.image('img/mono.png', width=300)

# Carga de imagen por el usuario
uploaded_file = st.file_uploader("Carga una imagen del producto que deseas reciclar", type=["jpg", "png", "jpeg"])


if uploaded_file is not None:
    # Para mostrar la imagen subida como una vista preliminar en tamaño reducido
    st.image(uploaded_file, caption='Vista preliminar', width=100)


    # Restablecer el contenido generado al cargar una nueva imagen
    if 'last_uploaded_file' not in st.session_state or (uploaded_file != st.session_state['last_uploaded_file']):
        st.session_state['last_uploaded_file'] = uploaded_file
        st.session_state['generated_content'] = False

    # Botón de enviar y proceso principal
    if st.button("Analizar Producto"):
        with st.spinner('Identificando el producto y material...'):
            image = encode_image(uploaded_file)
            st.session_state['generated_content'] = True


            # Identificar el producto y el material con la IA
            chain = ChatOpenAI(model="gpt-4-vision-preview", max_tokens=1024)
            msg = chain.invoke(
                [AIMessage(content="Basándose en la imagen, identifique el producto y el tipo de material."),
                HumanMessage(content=[{"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image}"}}])
                ]
            )

            st.session_state['identificacion'] = msg.content
            #st.markdown("**Identificación del producto y material:**")
            #st.write(st.session_state['identificacion'])

            # Generar recomendaciones de reciclaje
            prompt_reciclaje = PromptTemplate.from_template(
                """
                Dado el siguiente producto y material identificado:
                {identification}
                ¿Qué consejos de reciclaje se pueden dar para este producto?
                Debes responder como si fueras el Mono, que es un personaje de la empresa Carozzi, está impulsando temas de reciclaje,
                También ten en contexto que Carozzi en sus oficinas tiene lugares para reciclar con colores por material:
                - Plásticos PET (Color Amarillo): Botellas plásticas, bandejas de galletas.
                - Aluminio (Color Plomo): Latas y envoltorios de aluminio 
                - Papel y Cartón (Color Azul): Todo tipo de papeles, cartulinas y cartón.
                - Envases Plásticos PP (Color Amarillo): Envoltorios de plástico flexible como galletas, pastas, barritas de cereal, etc.
                - Otros (Color Negro): Frutas, bolsas de té, envolturas de dulces, yogurt, tetrapack, etc.
                
                La idea es que respondas como si fueras el Mono, aparte de aconsejar como reciclar, también aconseja en donde debemos reciclar según el contexto entregado de los botes por tipo de material y su color
                Intenta agregar algunos emojis que vayan en contexto al final de cada párrafo para darle un contexto más amigable con el medio ambiente
                
                Si toca un producto como el yogurth que contiene un envase plastico y tapa de aluminio, puedes indicar que laven todo y luego voten la parte plástica donde corresponda y la parte metálica en donde corresponda por separado. Esto aplicalo a otro tipo de producto donde el escenario sea similar al del yogurth
                
                Debes partir respondiendo identificando el producto y donde debes reciclarlo, luego das un poco de info extra y motivación para el reciclaje,
                y finalmente explica qué es el impacto positivo que tiene el reciclaje. La respuesta debe tener máximo un párrafo de largo de 3-4 lineas.
                
                El Mono igual es un poco irónico, por ejemplo algunas frases del son:
                "Recuerden chicos que estaré vigilando que reciclen bien, sobre todo a Moraga"
                "Hey muchacho, hoy me puedes prestar tu pelota, perfecto! compartir es la escencia de la vida, compartir es el amor, compartir es estar en familia" una frase media filosofica de vez en cuando.
                
                al final de la respuesta debes decir: "Y recuerden chicos, estaré vigilando que reciclen de la manera correcta, sobre todo a Moraga" Puedes variar en la forma como abordas el final, no neesariamente debe ser identico el texto
                
                La repuesta debe ser precisa, en un parrafo de 80 palabras máximo. Recuerda que en el caso de ser necesario, debes aconsejar a como reciclarlo.
                Output:
                """
            )
            runnable = prompt_reciclaje | chain | StrOutputParser()
            st.session_state['consejos_reciclaje'] = runnable.invoke({"identification": st.session_state['identificacion']})
            st.markdown("**Consejos para reciclar este producto:**")
            st.write(st.session_state['consejos_reciclaje'])
            
        

# Función para compilar la información en un string
def compile_information():
    info = ""
    if st.session_state.get('generated_content', False):
        #info += "Identificación del producto y material:\n" + st.session_state.get('identificacion', '') + "\n\n"
        info += "Consejos para reciclar este producto:\n" + st.session_state.get('consejos_reciclaje', '') + "\n\n"
        #info += "Impacto Ecológico del Material:\n" + st.session_state.get('impacto_ecologico', '') + "\n\n"
    return info


# Carga las variables de entorno desde el archivo .env
load_dotenv()

# Función para text-to-speech utilizando ElevenLabs API
def generate_audio_from_text(text):
    XI_API_KEY = os.getenv('XI_API_KEY')
    if not XI_API_KEY:
        st.error("XI_API_KEY no está definida en las variables de entorno.")
        return None

    CHUNK_SIZE = 1024
    url = "https://api.elevenlabs.io/v1/text-to-speech/eolrIrYW76wwfCBK3QGf"

    headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": XI_API_KEY
    }

    data = {
        "text": text,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {
            "stability": 0.9,
            "similarity_boost": 0.8
        }
    }

    # Muestra spinner y mensaje de "Generando Audio..." mientras se ejecuta el bloque
    with st.spinner('Generando Audio...'):
        try:
            response = requests.post(url, json=data, headers=headers, timeout=30)  # Añadimos un timeout por si acaso la API se demora
            if response.status_code == 200:
                # Convertir el contenido del audio a base64
                base64_audio = base64.b64encode(response.content).decode('utf-8')
                # Crear el HTML para el elemento audio con autoplay
                audio_html = f'<audio controls autoplay><source src="data:audio/mpeg;base64,{base64_audio}" type="audio/mpeg"></audio>'
                return audio_html
            else:
                st.error(f"Error en la solicitud de texto a voz: {response.status_code}")
                return None
        except requests.exceptions.Timeout:
            st.error("La solicitud de audio ha excedido el tiempo de espera. Por favor, intenta de nuevo.")
            return None


# Botón para descargar la información
# Botón para generar y reproducir audio
if st.session_state.get('generated_content', False):
#    info_to_download = compile_information()
#    st.download_button(label="Descargar Información", data=info_to_download, file_name="ecoGPT_info.txt", mime="text/plain")

    # Agregar esta parte después de generar el texto para el audio
    texto_para_audio = st.session_state['consejos_reciclaje']
    if texto_para_audio:  # Verifica si hay texto para generar el audio
        audio_html = generate_audio_from_text(texto_para_audio)
        if audio_html:
            # Muestra el reproductor de audio con autoreproducción en la página
            st.markdown(audio_html, unsafe_allow_html=True)


# Estableciendo la franja superior
st.image("img/franja_inferior_1.png")



