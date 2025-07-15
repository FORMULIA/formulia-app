import streamlit as st

st.set_page_config(page_title="FormulIA - Generador de propuestas", layout="centered")

st.title("🧠 FormulIA")
st.subheader("Sistema automatizado para estructuración de propuestas")
st.markdown("---")

# Paso 1: Componentes
st.header("1️⃣ ¿Qué componentes incluye tu propuesta?")
componentes = st.multiselect(
    "Selecciona uno o varios:",
    ["Formación", "Monitoreo y Evaluación", "Materiales", "Operación"]
)

# Paso 2: Modalidad
modalidades = {}
for comp in ["Formación", "Operación"]:
    if comp in componentes:
        modalidades[comp] = st.selectbox(
            f"¿Qué modalidad tendrá el componente {comp}?",
            ["Presencial", "Virtual", "Híbrida"],
            key=f"modalidad_{comp}"
        )

# Paso 3: Organización y Municipio
st.header("2️⃣ Datos generales del proyecto")

org = st.text_input("¿A qué organización se dirige la propuesta?")
municipio = st.text_input("¿En qué municipio se ejecutará el proyecto?")

# Paso 4: Estrategias
st.header("3️⃣ Estrategias pedagógicas")

estrategias = st.multiselect(
    "¿Qué estrategias deseas aplicar?",
    ["Transición", "Primero", "Remediación"]
)

# Paso 5: Sedes educativas
st.header("4️⃣ Sedes educativas")

num_sedes = st.number_input("¿Cuántas sedes serán impactadas?", min_value=1, step=1)
sedes = []
for i in range(int(num_sedes)):
    nombre_sede = st.text_input(f"Nombre de la sede #{i+1}", key=f"sede_{i}")
    sedes.append(nombre_sede)

# Paso 6: Población por sede y grado
st.header("5️⃣ Registro de estudiantes y docentes por sede")

poblacion_por_sede = {}

grados_por_estrategia = {
    "Transición": ["0°"],
    "Primero": ["1°"],
    "Remediación": ["2°", "3°", "4°", "5°"]
}

# Determinar grados a preguntar según las estrategias seleccionadas
grados_requeridos = set()
for est in estrategias:
    grados_requeridos.update(grados_por_estrategia[est])

# Preguntar si se desea incluir docentes de todos los grados
incluir_todos_docentes = st.radio(
    "¿Deseas incluir a los docentes de todos los grados, independientemente de la estrategia seleccionada?",
    ["Sí", "No"]
)

for sede in sedes:
    st.subheader(f"Sede: {sede}")
    poblacion_por_sede[sede] = {}

    for grado in ["0°", "1°", "2°", "3°", "4°", "5°"]:
        incluir_grado = grado in grados_requeridos or incluir_todos_docentes == "Sí"

        if incluir_grado:
            col1, col2 = st.columns(2)
            with col1:
                est = st.number_input(
                    f"👩‍🎓 Estudiantes en {grado} - {sede}",
                    min_value=0,
                    key=f"{sede}_{grado}_est"
                )
            with col2:
                doc = st.number_input(
                    f"👨‍🏫 Docentes en {grado} - {sede} (dejar en 0 si no sabes)",
                    min_value=0,
                    key=f"{sede}_{grado}_doc"
                )

            # Estimar docentes si no se ingresa número
            if doc == 0 and est > 0:
                doc = round(est / 25)
                st.markdown(f"🔎 *Docentes estimados: {doc}*")

            poblacion_por_sede[sede][grado] = {
                "estudiantes": est,
                "docentes": doc
            }

# Guardar datos de población en sesión
st.session_state["poblacion_por_sede"] = poblacion_por_sede

# Paso 7: Selección de materiales por estrategia
st.header("6️⃣ Selección de materiales a incluir")

materiales_por_estrategia = {
    "Transición": [
        "Cartilla docente transición",
        "Cartilla estudiante transición",
        "Cartilla de cuentos transición",
        "Kit aula transición"
    ],
    "Primero": [
        "Guía docente tomo I",
        "Guía docente tomo II",
        "Guía estudiante unidad I",
        "Guía estudiante unidad II",
        "Guía estudiante unidad III",
        "Guía estudiante unidad IV",
        "Libro de cuentos",
        "Big Book",
        "Fichas",
        "Componedores aula",
        "Componedores individuales"
    ],
    "Remediación": [
        "Guía docente remediación",
        "Guía estudiante remediación",
        "Cartilla cuentos remediación",
        "Fichas de apoyo remediación"
    ]
}

materiales_seleccionados = {}

for estrategia in estrategias:
    st.subheader(f"📦 Materiales para {estrategia}")
    seleccion = st.multiselect(
        f"Selecciona los materiales que deseas incluir para {estrategia}",
        materiales_por_estrategia[estrategia],
        key=f"materiales_{estrategia}"
    )
    materiales_seleccionados[estrategia] = seleccion

# Guardar materiales seleccionados
st.session_state["materiales_seleccionados"] = materiales_seleccionados

# Paso 8: Refrigerios (solo si Formación presencial)
if "Formación" in componentes and modalidades.get("Formación") == "Presencial":
    st.header("7️⃣ Logística de formación - Refrigerios")

    incluir_refrigerios = st.radio("¿Deseas incluir refrigerios?", ["Sí", "No"])

    if incluir_refrigerios == "Sí":
        # Preguntar valor unitario
        valor_actual_refrigerio = 8000  # valor base que puedes cambiar si se conecta a Excel
        st.markdown(f"💰 Valor actual del refrigerio: **COP ${valor_actual_refrigerio:,.0f}**")
        actualizar_valor = st.radio("¿Deseas actualizar este valor?", ["No", "Sí"])

        if actualizar_valor == "Sí":
            valor_actual_refrigerio = st.number_input("Nuevo valor del refrigerio (COP)", min_value=1000, step=500)

        # Número de sesiones
        num_sesiones = st.number_input("¿En cuántas sesiones se ofrecerán refrigerios?", min_value=1, step=1)

        # Total de docentes
        total_docentes = sum(
            info["docentes"]
            for sede in st.session_state["poblacion_por_sede"].values()
            for info in sede.values()
        )

        cantidad_refrigerios = int(round(total_docentes * 1.2 * num_sesiones))

        st.success(f"🥤 Total de refrigerios estimados: {cantidad_refrigerios} unidades")
        st.session_state["refrigerios"] = {
            "valor_unitario": valor_actual_refrigerio,
            "num_sesiones": num_sesiones,
            "total_docentes": total_docentes,
            "cantidad_refrigerios": cantidad_refrigerios
        }

# Paso 9: Viajes, hotel y temas (solo si Formación presencial)
if "Formación" in componentes and modalidades.get("Formación") == "Presencial":
    st.header("8️⃣ Logística de formación - Viajes, hotel y temas")

    # Pregunta: número de viajes
    num_viajes = st.number_input(
        "¿Cuántos viajes estimas para desarrollar las formaciones?",
        min_value=1,
        value=3,
        step=1
    )

    # Pregunta: valor noche de hotel
    valor_hotel = st.number_input(
        "¿Cuál es el valor por noche del hotel (COP)?",
        min_value=50000,
        value=150000,
        step=10000
    )

    # Pregunta: selección de temas de formación
    st.markdown("## 🧠 Selección de temas de formación")

    # Lista simulada de temas (en la versión con Excel se extraerán dinámicamente)
    temas_formacion = [
        "Modelo pedagógico y didáctico",
        "Didáctica para transición",
        "Didáctica para primero",
        "Evaluación formativa",
        "Uso de materiales en el aula",
        "Acompañamiento a docentes"
    ]

    temas_seleccionados = st.multiselect(
        "Selecciona los temas que deseas incluir en la formación",
        temas_formacion
    )

    # Guardar en sesión
    st.session_state["formacion_logistica"] = {
        "num_viajes": num_viajes,
        "valor_hotel": valor_hotel,
        "temas": temas_seleccionados
    }
