import streamlit as st
import random
import time

st.set_page_config(page_title="Concurso Deletreo Chile", page_icon="🎡", layout="wide")
st.title("🎡 Concurso de Deletreo Escolar por Categorías")

CATEGORIAS = [
    "1° básico", "2° básico", "3° y 4° básico", 
    "5° y 6° básico", "7° y 8° básico", 
    "1° y 2° medio", "3° y 4° medio"
]
DIFICULTADES = ["Inicial", "Intermedio", "Avanzado"]

if "palabra_actual" not in st.session_state:
    st.session_state.palabra_actual = ""
if "historial" not in st.session_state:
    st.session_state.historial = []  
if "disparar_timer" not in st.session_state:
    st.session_state.disparar_timer = False
if "estado_final" not in st.session_state:
    st.session_state.estado_final = ""

if "estudiantes_raw" not in st.session_state:
    st.session_state.estudiantes_raw = {cat: ", ".join([f"Estudiante {i}" for i in range(1, 11)]) for cat in CATEGORIAS}

if "palabras_raw" not in st.session_state:
    st.session_state.palabras_raw = {}
    ejemplos = {
        "Inicial": "CASA, SOL, MESA, LUNA, GATO",
        "Intermedio": "ZAPATO, CIGARRA, HUEVO, LLUVIA",
        "Avanzado": "EXCEPCIÓN, SANGUÍNEO, HÁBITAT, CÓNDOR"
    }
    for cat in CATEGORIAS:
        st.session_state.palabras_raw[cat] = {dif: ejemplos[dif] for dif in DIFICULTADES}

tab_juego, tab_config = st.tabs(["🎮 PANTALLA DEL CONCURSO", "⚙️ CONFIGURACIÓN Y CARGA DE DATOS"])

with tab_config:
    st.header("⚙️ Centro de Carga Masiva (Estudiantes y Palabras)")
    col_g1, col_g2 = st.columns(2)
    with col_g1:
        modo_juego = st.radio("🛠️ Mecánica de evaluación:", ["Con Tiempo", "Sin Tiempo"], index=0, horizontal=True)
    with col_g2:
        tiempo_maximo = st.number_input("⏱️ Tiempo límite (segundos):", min_value=3, max_value=60, value=10, step=1, disabled=(modo_juego == "Sin Tiempo"))
    
    if st.button("🔄 Reiniciar Todo el Certamen (Borrar Historial)", type="secondary"):
        st.session_state.historial = []
        st.session_state.palabra_actual = ""
        st.session_state.disparar_timer = False
        st.session_state.estado_final = ""
        st.rerun()
        
    st.divider()
    cat_editar = st.selectbox("Selecciona la categoría escolar que deseas editar o revisar:", CATEGORIAS)
    col_c1, col_c2 = st.columns(2)
    
    with col_c1:
        st.subheader(f"👥 Alumnos - {cat_editar}")
        st.session_state.estudiantes_raw[cat_editar] = st.text_area(f"Lista de alumnos ({cat_editar}):", value=st.session_state.estudiantes_raw[cat_editar], height=120, label_visibility="collapsed")
        lista_alumnos = [a.strip() for a in st.session_state.estudiantes_raw[cat_editar].split(",") if a.strip()]
        st.info(f"Total alumnos detectados en {cat_editar}: **{len(lista_alumnos)}**")

    with col_c2:
        st.subheader(f"📋 Palabras - {cat_editar}")
        for dif in DIFICULTADES:
            st.session_state.palabras_raw[cat_editar][dif] = st.text_input(f"Nivel {dif}:", value=st.session_state.palabras_raw[cat_editar][dif])

with tab_juego:
    st.subheader("🎯 Panel de Control de Rondas")
    col_f1, col_f2, col_f3 = st.columns(3)
    
    with col_f1:
        cat_activa = st.selectbox("1. Filtrar Categoría Escolar:", CATEGORIAS, key="cat_activa")
    with col_f2:
        dif_activa = st.selectbox("2. Filtrar Dificultad:", DIFICULTADES, key="dif_activa")
    with col_f3:
        alumnos_ronda = [a.strip() for a in st.session_state.estudiantes_raw[cat_activa].split(",") if a.strip()]
        alumno_turno = st.selectbox("3. Alumno en turno (Visual):", ["-- Seleccionar Alumno --"] + alumnos_ronda)

    st.divider()
    col_ruleta, col_timer = st.columns(2)

    with col_ruleta:
        st.subheader("🎰 Ruleta de Selección")
        palabras_filtradas_raw = st.session_state.palabras_raw[cat_activa][dif_activa]
        banco_activo = [p.strip().upper() for p in palabras_filtradas_raw.split(",") if p.strip()]
        
        historial_palabras_usadas = []
        for h in st.session_state.historial:
            if isinstance(h, tuple) and len(h) == 3:
                if h[1] == cat_activa and h[2] == dif_activa:
                    historial_palabras_usadas.append(h[0])

        palabras_disponibles = [p for p in banco_activo if p not in historial_palabras_usadas]
        st.write(f"Palabras disponibles en esta dificultad: **{len(palabras_disponibles)}**")

        if st.button("🔥 ¡GIRAR RULETA!", use_container_width=True):
            if palabras_disponibles:
                st.session_state.estado_final = ""  
                placeholder = st.empty()
                for _ in range(6):
                    placeholder.markdown(f"<h2 style='text-align: center; color: #999;'>🎲 {random.choice(palabras_disponibles)}</h2>", unsafe_allow_html=True)
                    time.sleep(0.08)
                
                seleccion = random.choice(palabras_disponibles)
                st.session_state.palabra_actual = seleccion
                st.session_state.historial.append((seleccion, cat_activa, dif_activa))
                st.session_state.disparar_timer = (modo_juego == "Con Tiempo")
            else:
                st.error(f"❌ ¡No quedan palabras disponibles para {cat_activa} en nivel {dif_activa}!")
                st.session_state.palabra_actual = ""
                st.session_state.disparar_timer = False

        if st.session_state.palabra_actual:
            st.markdown(f"<div style='background-color: #f8f9fa; padding: 25px; border-radius: 12px; text-align: center; border: 3px solid #ff4b4b; margin-top:15px;'><p style='font-size: 14px; margin: 0; color: #555;'>CATEGORÍA: {cat_activa.upper()} ({dif_activa.upper()})</p><h1 style='font-size: 55px; margin: 5px 0 0 0; color: #ff4b4b; letter-spacing: 3px;'>{st.session_state.palabra_actual}</h1></div>", unsafe_allow_html=True)

    with col_timer:
        if modo_juego == "Con Tiempo":
            st.subheader("⏱️ Control del Cronómetro")
            detener_tiempo = st.button("🛑 DETENER TIEMPO", use_container_width=True, type="primary")
            barra_progreso = st.progress(0.0)
            contenedor_reloj = st.empty()
            
            if st.session_state.disparar_timer and st.session_state.palabra_actual:
                tiempo_detenido = False
                pasos = tiempo_maximo * 10
                
                for i in range(pasos, -1, -1):
                    segundos_restantes = i / 10.0
                    contenedor_reloj.markdown(f"<h1 style='text-align: center; color: #00cc66; font-size: 65px; margin: 10px 0;'>{segundos_restantes:.1f}s</h1>", unsafe_allow_html=True)
                    barra_progreso.progress(i / pasos)
                    if detener_tiempo:
                        tiempo_detenido = True
                        break
                    time.sleep(0.1)
                
                st.session_state.disparar_timer = False
                st.session_state.estado_final = "EXCELENTE" if tiempo_detenido else "NO_LOGRADO"
                st.rerun()

            if st.session_state.estado_final == "EXCELENTE":
                contenedor_reloj.empty()
                st.markdown("<div style='background-color: #d4edda; padding: 20px; border-radius: 10px; border: 2px solid #c3e6cb;'><h2 style='text-align: center; color: #155724; font-size: 45px; margin:0;'>🎉 ¡Excelente!</h2></div>", unsafe_allow_html=True)
            elif st.session_state.estado_final == "NO_LOGRADO":
                contenedor_reloj.empty()
                st.markdown("<div style='background-color: #f8d7da; padding: 20px; border-radius: 10px; border: 2px solid #f5c6cb;'><h2 style='text-align: center; color: #721c24; font-size: 45px; margin:0;'>❌ ¡No logrado!</h2></div>", unsafe_allow_html=True)
            elif not st.session_state.palabra_actual:
                contenedor_reloj.markdown(f"<h1 style='text-align: center; color: #ccc; font-size: 65px; margin: 10px 0;'>{tiempo_maximo}.0s</h1>", unsafe_allow_html=True)
                barra_progreso.progress(1.0)
        else:
            st.subheader("🎯 Calificación Manual (Sin Tiempo)")
            col_b1, col_b2 = st.columns(2)
            with col_b1:
                if st.button("✔️ LOGRADO", use_container_width=True, type="primary", disabled=(not st.session_state.palabra_actual)):
                    st.session_state.estado_final = "LOGRADO"
            with col_b2:
                if st.button("❌ NO LOGRADO", use_container_width=True, type="secondary", disabled=(not st.session_state.palabra_actual)):
                    st.session_state.estado_final = "NO_LOGRADO"
            
            if st.session_state.estado_final == "LOGRADO":
                st.markdown("<div style='background-color: #d4edda; padding: 20px; border-radius: 10px; border: 2px solid #c3e6cb;'><h2 style='text-align: center; color: #155724; font-size: 45px; margin:0;'>🎉 ¡Logrado!</h2></div>", unsafe_allow_html=True)
            elif st.session_state.estado_final == "NO_LOGRADO":
                st.markdown("<div style='background-color: #f8d7da; padding: 20px; border-radius: 10px; border: 2px solid #f5c6cb;'><h2 style='text-align: center; color: #721c24; font-size: 45px; margin:0;'>❌ ¡No logrado!</h2></div>", unsafe_allow_html=True)

    st.divider()
    st.markdown("### 📋 Historial de Palabras Usadas en esta sesión")
    if st.session_state.historial:
        cols_historial = st.columns(4)
        for indice, item in enumerate(st.session_state.historial):
            with cols_historial[indice % 4]:
                if isinstance(item, tuple) and len(item) == 3:
                    st.markdown(f"**{indice + 1}.** `{item[0]}` ({item[1]} - {item[2]})")
                else:
                    st.markdown(f"**{indice + 1}.** `{item}`")
    else:
        st.caption("Aún no hay registros en la sesión actual.")
