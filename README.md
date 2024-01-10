# Aplicación de Análisis Ecológico con Streamlit

## Descripción
Esta aplicación utiliza Streamlit y la inteligencia artificial de OpenAI para identificar productos a través de imágenes y proporcionar información ecológica sobre ellos. 

## Requerimientos
- Python 3.7 o superior
- Bibliotecas Python: `streamlit`, `base64`, `langchain`, `dotenv`, `openai`

## Cómo Ejecutar la Aplicación
1. Clona este repositorio.
2. Instala las dependencias con `pip install -r requirements.txt`.
3. Ejecuta la aplicación con `streamlit run nombre_del_archivo.py`.

## Funcionalidades
- **Identificación de Producto y Material:** Permite cargar imágenes de productos para identificarlos y obtener consejos de reciclaje.
- **Impacto Ecológico del Material:** Proporciona información sobre el tiempo de biodegradación y el impacto positivo de reciclar el material.

## Uso
1. La aplicación muestra un mensaje de bienvenida y la imagen del logo de Carozzi.
2. El usuario puede cargar una imagen del producto que desea reciclar.
3. Al presionar el botón "Analizar Producto", la aplicación utiliza inteligencia artificial para identificar el producto y material.
4. Proporciona consejos de reciclaje y detalles sobre el impacto ecológico del material identificado.
5. Se puede descargar la información generada con el botón "Descargar Información".

## Referencias
- [Streamlit](https://streamlit.io/)
- [OpenAI](https://openai.com/)
- [Carozzi](https://www.carozzi.cl/)

## Creador:
@NicoIG