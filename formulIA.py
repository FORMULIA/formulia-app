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
