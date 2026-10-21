import streamlit as st
import random
import time

# 1. Configuración de la página y título
st.set_page_config(page_title="Ruleta de Deletreo Chile", page_icon="🎡", layout="centered")
st.title("🎡 Ruleta Interactiva: Concurso de Deletreo")
st.write("Gira la ruleta para seleccionar una palabra al azar y activar el cronómetro.")

# 2. Base de datos de palabras (puedes editar esta lista con tus propias palabras)
if "lista_palabras" not in st.session_state:
    st.session_state.lista_palabras = [
        "HÉROE", "CIGARRA", "ZAPATO", "HUEVO", "BIENVENIDO", 
        "VALENTÍA", "EXCEPCIÓN", "LLUVIA", "CÓNDOR", "GUITARRA",
        "ZORRO", "HÁBITAT", "CORAZÓN", "VELOCIDAD", "SANGUÍNEO"
    ]

# Inicializar estados de la app
if "palabra_actual" not in st.session_state:
    st.session_state.palabra_actual = ""
if "historial" not in st.session_state:
    st.session_state.historial = []

# 3. Controles principales
col1, col2 = st.columns(2)

with col1:
    # Botón para girar la ruleta
    if st.button("🔥 ¡GIRAR RULETA!", use_container_width=True):
        palabras_disponibles = [p for p in st.session_state.lista_palabras if p not in st.session_state.historial]
        
        if palabras_disponibles:
            placeholder = st.empty()
            for _ in range(8):
                placeholder.markdown(f"<h2 style='text-align: center; color: gray;'>🎲 {random.choice(palabras_disponibles)}</h2>", unsafe_allow_html=True)
                time.sleep(0.1)
            
            palabra_seleccionada = random.choice(palabras_disponibles)
            st.session_state.palabra_actual = palabra_seleccionada
            st.session_state.historial.append(palabra_seleccionada)
        else:
            st.warning("¡Se han acabado las palabras de la lista!")
            st.session_state.palabra_actual = ""

    # Mostrar la palabra seleccionada en pantalla gigante
    if st.session_state.palabra_actual:
        st.markdown(
            f"<div style='background-color: #f0f2f6; padding: 20px; border-radius: 10px; text-align: center; border: 2px solid #ff4b4b;'> "
            f"<p style='font-size: 14px; margin: 0; color: #555;'>PALABRA A DELETREAR:</p>"
            f"<h1 style='font-size: 50px; margin: 0; color: #ff4b4b; letter-spacing: 2px;'>{st.session_state.palabra_actual}</h1>"
            f"</div>", 
            unsafe_allow_html=True
        )

with col2:
    st.markdown("⏱️ **Temporizador**")
    if st.button("⏱️ Iniciar 10s", disabled=(st.session_state.palabra_actual == ""), use_container_width=True):
        progreso = st.progress(1.0)
        reloj_texto = st.empty()
        
        for i in range(10, -1, -1):
            reloj_texto.markdown(f"<h2 style='text-align: center; color: red;'>{i} segundos</h2>", unsafe_allow_html=True)
            progreso.progress(i / 10.0)
            time.sleep(1)
        
        st.error("🚨 ¡TIEMPO TERMINADO!")

# 4. Barra lateral con reglas e historial
with st.sidebar:
    st.header("⚙️ Panel de Control")
    st.subheader("📋 Palabras Jugadas")
    if st.session_state.historial:
        for p in st.session_state.historial:
            st.write(f"✔️ {p}")
    else:
        st.caption("Aún no ha salido ninguna palabra.")
        
    if st.button("🔄 Reiniciar Concurso"):
        st.session_state.historial = []
        st.session_state.palabra_actual = ""
        st.rerun()

    st.divider()
    st.markdown('''
    **💡 Recordatorio de Reglas (Español):**
    1. Escuchar la palabra.
    2. Pronunciar la palabra completa.
    3. Deletrear letra por letra (mencionar tildes).
    4. Pronunciar la palabra al finalizar.
    ''')
