import streamlit as st
import random
import time

# Configuración de pantalla ancha para proyección en aula
st.set_page_config(page_title="CONCURSO DE DELETREO 2026", page_icon="🎡", layout="wide")

# 1. ENCABEZADO INSTITUCIONAL Y LOGOS
col_logo, col_titulo = st.columns([1, 4])

with col_logo:
    # URL del escudo oficial enviado en la conversación
    URL_LOGO = "https://raw.githubusercontent.com/uccossio/ruleta-deletreo/main/logo.png"
    st.image(URL_LOGO, width=150, caption="80 años: 1946-2026")

with col_titulo:
    st.markdown("<h2 style='margin: 0; color: #1a365d;'>Colegio Bicentenario Santa María de Aconcagua</h2>", unsafe_allow_html=True)
    st.markdown("<h1 style='margin: 0; color: #ff4b4b; font-size: 42px;'>CONCURSO DE DELETREO 2026</h1>", unsafe_allow_html=True)
    st.markdown("<p style='font-size: 11px; color: #888; margin: 0;'>Dev by uccossio</p>", unsafe_allow_html=True)

st.divider()

# 2. DEFINICIÓN DE CATEGORÍAS Y NIVELES CONSTANTES
CATEGORIAS = [
    "1° básico", "2° básico", "3° y 4° básico", 
    "5° y 6° básico", "7° y 8° básico", 
    "1° y 2° medio", "3° y 4° medio"
]
DIFICULTADES = ["Inicial", "Intermedio", "Avanzado"]

# 3. INICIALIZACIÓN DE ESTADOS INTERNOS (SESSION STATE)
if "palabra_actual" not in st.session_state:
    st.session_state.palabra_actual = ""
if "historial" not in st.session_state:
    st.session_state.historial = []  
if "estado_final" not in st.session_state:
    st.session_state.estado_final = ""
if "timer_activo" not in st.session_state:
    st.session_state.timer_activo = False

# Inicializar puntajes de los estudiantes (10 alumnos por categoría)
if "puntajes" not in st.session_state:
    st.session_state.puntajes = {cat: {f"Estudiante {i}": 0 for i in range(1, 11)} for cat in CATEGORIAS}

# Inicializar nombres de estudiantes mapeados de forma editable
if "estudiantes_nombres" not in st.session_state:
    st.session_state.estudiantes_nombres = {cat: [f"Estudiante {i}" for i in range(1, 11)] for cat in CATEGORIAS}

# Palabras base preestablecidas de ejemplo
if "palabras_raw" not in st.session_state:
    st.session_state.palabras_raw = {}
    ejemplos = {
        "Inicial": "CASA, SOL, MESA, LUNA, GATO",
        "Intermedio": "ZAPATO, CIGARRA, HUEVO, LLUVIA",
        "Avanzado": "EXCEPCIÓN, SANGUÍNEO, HÁBITAT, CÓNDOR"
    }
    for cat in CATEGORIAS:
        st.session_state.palabras_raw[cat] = {dif: ejemplos[dif] for dif in DIFICULTADES}

# 4. CREACIÓN DE PESTAÑAS DE CONTROL
tab_juego, tab_puntajes, tab_config = st.tabs([
    "🎮 PANTALLA DEL CONCURSO", 
    "📊 TABLA DE PUNTAJES", 
    "⚙️ CONFIGURACIÓN Y CARGA DE DATOS"
])

with tab_config:
    st.header("⚙️ Centro de Configuración General")
    
    col_g1, col_g2 = st.columns(2)
    with col_g1:
        modo_juego = st.radio("🛠️ Mecánica de evaluación:", ["Con Tiempo", "Sin Tiempo"], index=0, horizontal=True)
    with col_g2:
        tiempo_maximo = st.number_input("⏱️ Tiempo límite (segundos):", min_value=3, max_value=60, value=10, step=1, disabled=(modo_juego == "Sin Tiempo"))
    
    if st.button("🔄 Reiniciar Todo el Certamen (Historial y Puntajes)", type="secondary"):
        st.session_state.historial = []
        st.session_state.palabra_actual = ""
        st.session_state.estado_final = ""
        st.session_state.timer_activo = False
        st.session_state.puntajes = {cat: {f"Estudiante {i}": 0 for i in range(1, 11)} for cat in CATEGORIAS}
        st.session_state.estudiantes_nombres = {cat: [f"Estudiante {i}" for i in range(1, 11)] for cat in CATEGORIAS}
        st.rerun()
        
    st.divider()
    
    cat_editar = st.selectbox("Selecciona la categoría escolar que deseas editar o revisar:", CATEGORIAS)
    col_c1, col_c2 = st.columns(2)
    
    with col_c1:
        st.subheader(f"👥 Personalizar Nombres de Alumnos - {cat_editar}")
        st.caption("Escribe los 10 nombres de los estudiantes separados por comas:")
        formato_inicial = ", ".join(st.session_state.estudiantes_nombres[cat_editar])
        texto_alumnos_input = st.text_area(f"Lista de alumnos ({cat_editar}):", value=formato_inicial, height=120, label_visibility="collapsed")
        
        # Procesar y guardar de manera limpia actualizando las llaves del puntaje preservando datos previos si coinciden
        nuevos_nombres = [a.strip() for a in texto_alumnos_input.split(",") if a.strip()][:10]
        while len(nuevos_nombres) < 10:
            nuevos_nombres.append(f"Estudiante {len(nuevos_nombres)+1}")
        
        st.session_state.estudiantes_nombres[cat_editar] = nuevos_nombres
        
        # Ajustar el diccionario de puntajes para reflejar los nuevos nombres
        puntajes_viejos = st.session_state.puntajes[cat_editar]
        nuevo_dict_puntajes = {}
        for nom in nuevos_nombres:
            nuevo_dict_puntajes[nom] = puntajes_viejos.get(nom, 0)
        st.session_state.puntajes[cat_editar] = nuevo_dict_puntajes
        st.info(f"Lista de 10 estudiantes guardada para {cat_editar}.")

    with col_c2:
        st.subheader(f"📋 Carga Masiva de Palabras - {cat_editar}")
        st.caption("Separa las palabras usando comas ( , )")
        for dif in DIFICULTADES:
            st.session_state.palabras_raw[cat_editar][dif] = st.text_input(
                f"Nivel {dif}:", 
                value=st.session_state.palabras_raw[cat_editar][dif]
            )

with tab_puntajes:
    st.header("📊 Registro y Control de Puntajes en Vivo")
    cat_puntaje_ver = st.selectbox("Filtrar Tabla por Categoría Escolar:", CATEGORIAS, key="sb_puntajes_ver")
    
    st.markdown(f"### Puntajes de la Categoría: **{cat_puntaje_ver}**")
    
    # Renderizar los puntajes de manera interactiva con controles de suma/resta manual rápido
    for alumno, puntos in st.session_state.puntajes[cat_puntaje_ver].items():
        col_al, col_pt, col_btn1, col_btn2 = st.columns([4, 2, 1, 1])
        with col_al:
            st.write(f"👤 **{alumno}**")
        with col_pt:
            st.write(f"⭐ {puntos} Puntos")
        with col_btn1:
            if st.button("➕ 1", key=f"add_{cat_puntaje_ver}_{alumno}"):
                st.session_state.invertir_mod = True
                st.session_state.puntajes[cat_puntaje_ver][alumno] += 1
                st.rerun()
        with col_btn2:
            if st.button("➖ 1", key=f"rem_{cat_puntaje_ver}_{alumno}"):
                st.session_state.puntajes[cat_puntaje_ver][alumno] = max(0, st.session_state.puntajes[cat_puntaje_ver][alumno] - 1)
                st.rerun()

with tab_juego:
    st.subheader("🎯 Panel de Control de Rondas")
    col_f1, col_f2, col_f3 = st.columns(3)
    
    with col_f1:
        cat_activa = st.selectbox("1. Filtrar Categoría Escolar:", CATEGORIAS, key="cat_activa")
    with col_f2:
        dif_activa = st.selectbox("2. Filtrar Dificultad:", DIFICULTADES, key="dif_activa")
    with col_f3:
        alumnos_ronda = st.session_state.estudiantes_nombres[cat_activa]
        alumno_turno = st.selectbox("3. Alumno en turno:", ["-- Seleccionar Alumno --"] + alumnos_ronda)

    st.divider()

    col_ruleta, col_timer = st.columns(2)

    with col_ruleta:
        st.subheader("🎰 Ruleta de Selección")
        
        palabras_filtradas_raw = st.session_state.palabras_raw[cat_activa][dif_activa]
        banco_activo = [p.strip().upper() for p in palabras_filtradas_raw.split(",") if p.strip()]
        
        historial_palabras_usadas = [h[0] for h in st.session_state.historial if isinstance(h, tuple) and h[1] == cat_activa and h[2] == dif_activa]
        palabras_disponibles = [p for p in banco_activo if p not in historial_palabras_usadas]
        
        st.write(f"Palabras disponibles en esta dificultad: **{len(palabras_disponibles)}**")

        if st.button("🔥 ¡GIRAR RULETA!", use_container_width=True):
            if palabras_disponibles:
                st.session_state.estado_final = ""  
                st.session_state.timer_activo = False
                placeholder = st.empty()
                
                # Efecto visual de ruleta: El último elemento generado coincidirá exactamente con la palabra principal
                seleccion = random.choice(palabras_disponibles)
                giros_falsos = [random.choice(banco_activo) for _ in range(5)]
                
                for palabra_giro in giros_falsos:
                    placeholder.markdown(f"<h2 style='text-align: center; color: #999;'>🎲 {palabra_giro}</h2>", unsafe_allow_html=True)
                    time.sleep(0.08)
                
                # Coincidencia perfecta al frenar
                placeholder.markdown(f"<h2 style='text-align: center; color: #ff4b4b; font-size: 32px;'>🎯 {seleccion}</h2>", unsafe_allow_html=True)
                time.sleep(0.2)
                
                st.session_state.palabra_actual = seleccion
                st.session_state.historial.append((seleccion, cat_activa, dif_activa))
            else:
                st.error(f"❌ ¡No quedan palabras disponibles para {cat_activa} en nivel {dif_activa}!")
                st.session_state.palabra_actual = ""

        # Mostrar la palabra principal seleccionada
        if st.session_state.palabra_actual:
            st.markdown(
                f"<div style='background-color: #f8f9fa; padding: 25px; border-radius: 12px; text-align: center; border: 3px solid #ff4b4b; margin-top:15px;'> "
                f"<p style='font-size: 14px; margin: 0; color: #555;'>PALABRA SELECCIONADA ({cat_activa.upper()} - {dif_activa.upper()}):</p>"
                f"<h1 style='font-size: 55px; margin: 5px 0 0 0; color: #ff4b4b; letter-spacing: 3px;'>{st.session_state.palabra_actual}</h1>"
                f"</div>", 
                unsafe_allow_html=True
            )

    with col_timer:
        if modo_juego == "Con Tiempo":
            st.subheader("⏱️ Control del Cronómetro")
            
            # Botones de control de flujo secuenciales solicitados
            col_b1, col_b2 = st.columns(2)
            with col_b1:
                btn_iniciar = st.button("▶️ INICIAR TEMPORIZADOR", use_container_width=True, type="secondary", disabled=(not st.session_state.palabra_actual or st.session_state.timer_activo))
            with col_b2:
                btn_detener = st.button("🛑 DETENER TIEMPO", use_container_width=True, type="primary", disabled=(not st.session_state.timer_activo))
            
            barra_progreso = st.progress(0.0)
            contenedor_reloj = st.empty()
            
            if btn_iniciar:
                st.session_state.timer_activo = True
                st.session_state.estado_final = ""
                st.rerun()

            # Lógica secuencial del temporizador tras presionar el botón de inicio
            if st.session_state.timer_activo and st.session_state.palabra_actual:
                tiempo_detenido = False
                pasos = tiempo_maximo * 10
                
                for i in range(pasos, -1, -1):
                    segundos_restantes = i / 10.0
                    contenedor_reloj.markdown(f"<h1 style='text-align: center; color: #00cc66; font-size: 65px; margin: 10px 0;'>{segundos_restantes:.1f}s</h1>", unsafe_allow_html=True)
                    barra_progreso.progress(i / pasos)
                    
                    if btn_detener:
                        tiempo_detenido = True
                        break
                    time.sleep(0.1)
                
                st.session_state.timer_activo = False
                
                if tiempo_detenido:
                    st.session_state.estado_final = "EXCELENTE"
                    # Asignación automática de puntaje al alumno seleccionado si la evaluación es exitosa
                    if alumno_turno != "-- Seleccionar Alumno --":
                        st.session_state.puntajes[cat_activa][alumno_turno] += 1
                else:
                    st.session_state.estado_final = "NO_LOGRADO"
                st.rerun()

            # Renderización de estados gráficos finales
            if st.session_state.estado_final == "EXCELENTE":
                contenedor_reloj.empty()
                st.markdown("<div style='background-color: #d4edda; padding: 20px; border-radius: 10px; border: 2px solid #c3e6cb;'><h2 style='text-align: center; color: #155724; font-size: 45px; margin:0;'>🎉 ¡Excelente!</h2></div>", unsafe_allow_html=True)
                if alumno_turno != "-- Seleccionar Alumno --":
                    st.caption(f"Puntaje sumado automáticamente a {alumno_turno}")
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
                    if alumno_turno != "-- Seleccionar Alumno --":
                        st.session_state.puntajes[cat_activa][alumno_turno] += 1
            with col_b2:
                if st.button("❌ NO LOGRADO", use_container_width=True, type="secondary", disabled=(not st.session_state.palabra_actual)):
                    st.session_state.estado_final = "NO_LOGRADO"
            
            st.write("")
            if st.session_state.estado_final == "LOGRADO":
                st.markdown("<div style='background-color: #d4edda; padding: 20px; border-radius: 10px; border: 2px solid #c3e6cb;'><h2 style='text-align: center; color: #155724; font-size: 45px; margin:0;'>🎉 ¡Logrado!</h2></div>", unsafe_allow_html=True)
            elif st.session_state.estado_final == "NO_LOGRADO":
                st.markdown("<div style='background-color: #f8d7da; padding: 20px; border-radius: 10px; border: 2px solid #f5c6cb;'><h2 style='text-align: center; color: #721c24; font-size: 45px; margin:0;'>❌ ¡No logrado!</h2></div>", unsafe_allow_html=True)
