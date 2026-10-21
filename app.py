import streamlit as st
import random
import time

# Configuración de la página
st.set_page_config(page_title="Ruleta de Deletreo Chile", page_icon="🎡", layout="wide")
st.title("🎡 Ruleta de Deletreo Profesional")

# 1. Inicialización de estados de la aplicación
if "palabra_actual" not in st.session_state:
    st.session_state.palabra_actual = ""
if "historial" not in st.session_state:
    st.session_state.historial = []
if "disparar_timer" not in st.session_state:
    st.session_state.disparar_timer = False

# Definición de palabras por defecto iniciales
palabras_por_defecto = (
    "HÉROE, CIGARRA, ZAPATO, HUEVO, BIENVENIDO, VALENTÍA, EXCEPCIÓN, LLUVIA, CÓNDOR, GUITARRA, "
    "ZORRO, HÁBITAT, CORAZÓN, VELOCIDAD, SANGUÍNEO, AMBULANCIA, BICICLETA, CABALLO, DERECHO, EDIFICIO, "
    "FERROCARRIL, GIGANTE, HORIZONTE, INSECTO, JIRAFA, KILÓMETRO, LUCIÉRNAGA, MARIPOSA, NATURALEZA, ORGULLO, "
    "PARAGUAS, QUITASOL, RATÓN, SILENCIO, TIERRA, UNIVERSO, VENTANA, WATERPOLO, XILÓFONO, YOGUR, "
    "ZANAHORIA, ASIGNATURA, COLEGIO, DOCENTE, ESCRITORIO, ALUMNO, PRUEBA, LECTURA, CIENCIA, HISTORIA"
)

# 2. Configuración en la Barra Lateral
with st.sidebar:
    st.header("⚙️ Configuración del Concurso")
    
    # Campo para configurar el tiempo máximo del temporizador
    tiempo_maximo = st.number_input("⏱️ Tiempo por palabra (segundos):", min_value=3, max_value=60, value=10, step=1)
    
    st.divider()
    
    # Cuadro de texto para pegar o editar las 50 palabras cómodamente
    st.subheader("📋 Lista de Palabras")
    st.caption("Separa las palabras usando comas ( , )")
    texto_palabras = st.text_area("Editar banco de palabras:", value=palabras_por_defecto, height=250)
    
    # Procesar la lista ingresada por el usuario
    lista_procesada = [p.strip().upper() for p in texto_palabras.split(",") if p.strip()]
    st.info(f"Total cargado: **{len(lista_procesada)}** palabras.")
    
    st.divider()
    
    # Historial de control
    st.subheader("🎯 Palabras ya Evaluadas")
    if st.session_state.historial:
        for p in st.session_state.historial:
            st.write(f"✔️ {p}")
        if st.button("🔄 Reiniciar Certamen"):
            st.session_state.historial = []
            st.session_state.palabra_actual = ""
            st.session_state.disparar_timer = False
            st.rerun()
    else:
        st.caption("Aún no se ha jugado ninguna palabra.")

# 3. Interfaz Principal (Panel de Control y Pantalla de Concurso)
col_ruleta, col_timer = st.columns(2)

with col_ruleta:
    st.subheader("🎰 Sorteo de Palabra")
    
    # Botón principal para girar la ruleta
    if st.button("🔥 ¡GIRAR RULETA!", use_container_width=True):
        palabras_disponibles = [p for p in lista_procesada if p not in st.session_state.historial]
        
        if palabras_disponibles:
            # Efecto visual de giro veloz
            placeholder = st.empty()
            for _ in range(6):
                placeholder.markdown(f"<h2 style='text-align: center; color: #888;'>🎲 {random.choice(palabras_disponibles)}</h2>", unsafe_allow_html=True)
                time.sleep(0.08)
            
            # Selección definitiva de la palabra
            seleccion = random.choice(palabras_disponibles)
            st.session_state.palabra_actual = seleccion
            st.session_state.historial.append(seleccion)
            # Activamos la señal para que el bloque de código continuo ejecute el timer de inmediato
            st.session_state.disparar_timer = True
        else:
            st.error("❌ ¡No quedan palabras disponibles en la lista de la barra lateral!")
            st.session_state.palabra_actual = ""
            st.session_state.disparar_timer = False

    # Despliegue de la palabra seleccionada en la pantalla
    if st.session_state.palabra_actual:
        st.markdown(
            f"<div style='background-color: #f8f9fa; padding: 25px; border-radius: 12px; text-align: center; border: 3px solid #ff4b4b; margin-top:15px;'>"
            f"<p style='font-size: 15px; margin: 0; color: #666; font-weight: bold;'>PALABRA A DELETREAR:</p>"
            f"<h1 style='font-size: 55px; margin: 5px 0 0 0; color: #ff4b4b; letter-spacing: 3px;'>{st.session_state.palabra_actual}</h1>"
            f"</div>", 
            unsafe_allow_html=True
        )

with col_timer:
    st.subheader("⏱️ Cronómetro Oficial")
    
    # Botón manual para detener el tiempo antes del vencimiento
    detener_tiempo = st.button("🛑 DETENER TIEMPO", key="stop_btn", use_container_width=True, type="secondary")
    
    # Espacios reservados en pantalla para actualizar de manera dinámica
    barra_progreso = st.progress(0.0)
    contenedor_reloj = st.empty()
    
    # Si la ruleta se giró y se exige activar el temporizador
    if st.session_state.disparar_timer and st.session_state.palabra_actual:
        tiempo_detenido = False
        
        # Bucle del temporizador basado en intervalos cortos para poder leer el botón de detención
        pasos = tiempo_maximo * 10
        for i in range(pasos, -1, -1):
            segundos_restantes = i / 10.0
            
            # Actualizamos los elementos visuales en pantalla
            contenedor_reloj.markdown(f"<h1 style='text-align: center; color: #00cc66; font-size: 65px; margin: 10px 0;'>{segundos_restantes:.1f}s</h1>", unsafe_allow_html=True)
            barra_progreso.progress(i / pasos)
            
            # Verificación del botón de detener (Streamlit evalúa los clics recargando la interfaz)
            # Nota: Debido a la ejecución lineal, si se presiona el botón interactivo, se detiene el ciclo.
            if detener_tiempo:
                tiempo_detenido = True
                break
                
            time.sleep(0.1)
        
        # Apagamos el disparador para evitar bucles infinitos en recargas normales
        st.session_state.disparar_timer = False
        
        if tiempo_detenido:
            contenedor_reloj.markdown("<h2 style='text-align: center; color: #ffcc00; font-size: 40px;'>🛑 TIEMPO DETENIDO</h2>", unsafe_allow_html=True)
        elif i <= 0:
            contenedor_reloj.markdown("<h2 style='text-align: center; color: #ff3333; font-size: 40px;'>🚨 ¡TIEMPO TERMINADO!</h2>", unsafe_allow_html=True)
    else:
        # Estado pasivo cuando no hay un temporizador activo corriendo
        contenedor_reloj.markdown(f"<h1 style='text-align: center; color: #ccc; font-size: 65px; margin: 10px 0;'>{tiempo_maximo}.0s</h1>", unsafe_allow_html=True)
        barra_progreso.progress(1.0)
