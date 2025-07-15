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

# Paso 5: Sedes
st.header("4️⃣ Sedes educativas")

num_sedes = st.number_input("¿Cuántas sedes serán impactadas?", min_value=1, step=1)
sedes = []
for i in range(int(num_sedes)):
    nombre_sede = st.text_input(f"Nombre de la sede #{i+1}", key=f"sede_{i}")
    sedes.append(nombre_sede)

# Guardamos los datos en una variable de sesión para usarlos después
st.session_state["resumen_propuesta"] = {
    "componentes": componentes,
    "modalidades": modalidades,
    "organizacion": org,
    "municipio": municipio,
    "estrategias": estrategias,
    "sedes": sedes,
}

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

# Guardar en sesión
st.session_state["poblacion_por_sede"] = poblacion_por_sede