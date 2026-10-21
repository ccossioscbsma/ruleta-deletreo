import streamlit as st
import random
import time

# Configuración de la página completa para máxima visibilidad en proyectores
st.set_page_config(page_title="Ruleta de Deletreo Chile", page_icon="??", layout="wide")
st.title("?? Concurso de Deletreo Profesional")

# 1. Inicialización de estados internos
if "palabra_actual" not in st.session_state:
    st.session_state.palabra_actual = ""
if "historial" not in st.session_state:
    st.session_state.historial = []
if "disparar_timer" not in st.session_state:
    st.session_state.disparar_timer = False
if "estado_final" not in st.session_state:
    st.session_state.estado_final = ""

# 50 Palabras base preestablecidas en español
palabras_por_defecto = (
    "HÉROE, CIGARRA, ZAPATO, HUEVO, BIENVENIDO, VALENTÍA, EXCEPCIÓN, LLUVIA, CÓNDOR, GUITARRA, "
    "ZORRO, HÁBITAT, CORAZÓN, VELOCIDAD, SANGUÍNEO, AMBULANCIA, BICICLETA, CABALLO, DERECHO, EDIFICIO, "
    "FERROCARRIL, GIGANTE, HORIZONTE, INSECTO, JIRAFA, KILÓMETRO, LUCIÉRNAGA, MARIPOSA, NATURALEZA, ORGULLO, "
    "PARAGUAS, QUITASOL, RATÓN, SILENCIO, TIERRA, UNIVERSO, VENTANA, WATERPOLO, XILÓFONO, YOGUR, "
    "ZANAHORIA, ASIGNATURA, COLEGIO, DOCENTE, ESCRITORIO, ALUMNO, PRUEBA, LECTURA, CIENCIA, HISTORIA"
)

# 2. PANEL DE CONFIGURACIÓN SUPERIOR (Reemplaza al menú lateral invisible)
tab_juego, tab_config = st.tabs(["?? PANTALLA DEL CONCURSO", "?? PANEL DE CARGA Y CONFIGURACIÓN"])

with tab_config:
    st.subheader("Configura tu concurso antes de proyectar")
    col_c1, col_c2 = st.columns(2)
    
    with col_c1:
        # Control de Tiempos
        tiempo_maximo = st.number_input("?? Configuración de Tiempos (Segundos por palabra):", min_value=3, max_value=60, value=10, step=1)
    
    with col_c2:
        # Botón para resetear todo el certamen
        st.write("¿Quieres reiniciar el concurso actual?")
        if st.button("?? Borrar Historial y Reiniciar", use_container_width=True):
            st.session_state.historial = []
            st.session_state.palabra_actual = ""
            st.session_state.disparar_timer = False
            st.session_state.estado_final = ""
            st.rerun()

    st.divider()
    # Carga Masiva Remota de las 50 palabras en pantalla principal
    st.subheader("?? Carga Masiva de Palabras")
    texto_palabras = st.text_area("Copia y pega tus palabras aquí (separadas por comas):", value=palabras_por_defecto, height=180)
    
    # Procesamiento inmediato de las palabras
    lista_procesada = [p.strip().upper() for p in texto_palabras.split(",") if p.strip()]
    st.success(f"?? Sistema: Se han cargado exitosamente **{len(lista_procesada)}** palabras para el concurso.")

with tab_juego:
    # 3. INTERFAZ PRINCIPAL DEL CONCURSO
    col_ruleta, col_timer = st.columns(2)

    with col_ruleta:
        st.subheader("?? Ruleta de Selección")
        
        # Acción para Girar la ruleta
        if st.button("?? ¡GIRAR RULETA!", use_container_width=True):
            palabras_disponibles = [p for p in lista_procesada if p not in st.session_state.historial]
            
            if palabras_disponibles:
                st.session_state.estado_final = "" # Limpiar mensaje previo
                placeholder = st.empty()
                for _ in range(6):
                    placeholder.markdown(f"<h2 style='text-align: center; color: #999;'>?? {random.choice(palabras_disponibles)}</h2>", unsafe_allow_html=True)
                    time.sleep(0.08)
                
                seleccion = random.choice(palabras_disponibles)
                st.session_state.palabra_actual = seleccion
                st.session_state.historial.append(seleccion)
                st.session_state.disparar_timer = True
            else:
                st.error("? ¡No quedan palabras disponibles! Agrega más en la pestaña de Configuración.")
                st.session_state.palabra_actual = ""
                st.session_state.disparar_timer = False

        # Mostrar la palabra en tamaño gigante para los alumnos
        if st.session_state.palabra_actual:
            st.markdown(
                f"<div style='background-color: #f8f9fa; padding: 25px; border-radius: 12px; text-align: center; border: 3px solid #ff4b4b; margin-top:15px;'> "
                f"<p style='font-size: 15px; margin: 0; color: #666; font-weight: bold;'>PALABRA A DELETREAR:</p>"
                f"<h1 style='font-size: 55px; margin: 5px 0 0 0; color: #ff4b4b; letter-spacing: 3px;'>{st.session_state.palabra_actual}</h1>"
                f"</div>", 
                unsafe_allow_html=True
            )

    with col_timer:
        st.subheader("?? Control del Cronómetro")
        
        # Botón de detener
        detener_tiempo = st.button("?? DETENER TIEMPO", use_container_width=True, type="primary")
        
        barra_progreso = st.progress(0.0)
        contenedor_reloj = st.empty()
        
        # Bucle lógico del temporizador automático
        if st.session_state.disparar_timer and st.session_state.palabra_actual:
            tiempo_detenido = False
            pasos = tiempo_maximo * 10
            
            for i in range(pasos, -1, -1):
                segundos_restantes = i / 10.0
                contenedor_reloj.markdown(f"<h1 style='text-align: center; color: #00cc66; font-size: 65px; margin: 10px 0;'>{segundos_restantes:.1f}s</h1>", unsafe_allow_html=True)
                barra_progreso.progress(i / pasos)
                
                # Captura el evento del botón detener en tiempo real
                if detener_tiempo:
                    tiempo_detenido = True
                    break
                    
                time.sleep(0.1)
            
            st.session_state.disparar_timer = False # Apagar disparador automático
            
            # Evaluación del resultado
            if tiempo_detenido:
                st.session_state.estado_final = "EXCELENTE"
            else:
                st.session_state.estado_final = "NO_LOGRADO"
            st.rerun()

        # Mostrar los estados finales fijos tras finalizar el reloj
        if st.session_state.estado_final == "EXCELENTE":
            contenedor_reloj.empty()
            barra_progreso.progress(0.0)
            st.markdown("<div style='background-color: #d4edda; padding: 20px; border-radius: 10px; border: 2px solid #c3e6cb;'><h2 style='text-align: center; color: #155724; font-size: 45px; margin:0;'>?? ¡Excelente!</h2></div>", unsafe_allow_html=True)
        elif st.session_state.estado_final == "NO_LOGRADO":
            contenedor_reloj.empty()
            barra_progreso.progress(0.0)
            st.markdown("<div style='background-color: #f8d7da; padding: 20px; border-radius: 10px; border: 2px solid #f5c6cb;'><h2 style='text-align: center; color: #721c24; font-size: 45px; margin:0;'>? ¡No logrado!</h2></div>", unsafe_allow_html=True)
        elif not st.session_state.palabra_actual:
            contenedor_reloj.markdown(f"<h1 style='text-align: center; color: #ccc; font-size: 65px; margin: 10px 0;'>{tiempo_maximo}.0s</h1>", unsafe_allow_html=True)
            barra_progreso.progress(1.0)

    # 4. Mostrar Historial abajo de manera discreta
    st.divider()
    st.markdown("### ?? Historial de Palabras Evaluadas en esta sesión")
    if st.session_state.historial:
        cols_historial = st.columns(5) # Distribuye el historial en 5 columnas horizontales para ahorrar espacio
        for indice, p in enumerate(st.session_state.historial):
            with cols_historial[indice % 5]:
                st.markdown(f"**{indice + 1}.** ?? {p}")
    else:
        st.caption("Aún no se han registrado palabras jugadas.")
