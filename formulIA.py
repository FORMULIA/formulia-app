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

# Paso 3: Organización y municipio
st.header("2️⃣ Datos generales del proyecto")
org = st.text_input("¿A qué organización se dirige la propuesta?")
municipio = st.text_input("¿En qué municipio se ejecutará el proyecto?")

# Paso 4: Estrategias pedagógicas
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

# Paso 6: Estudiantes y docentes
st.header("5️⃣ Registro de estudiantes y docentes por sede")

poblacion_por_sede = {}
grados_por_estrategia = {
    "Transición": ["0°"],
    "Primero": ["1°"],
    "Remediación": ["2°", "3°", "4°", "5°"]
}

grados_requeridos = set()
for est in estrategias:
    grados_requeridos.update(grados_por_estrategia[est])

incluir_todos_docentes = st.radio(
    "¿Deseas incluir a los docentes de todos los grados?",
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
                est = st.number_input(f"👩‍🎓 Estudiantes en {grado} - {sede}", min_value=0, key=f"{sede}_{grado}_est")
            with col2:
                doc = st.number_input(f"👨‍🏫 Docentes en {grado} - {sede}", min_value=0, key=f"{sede}_{grado}_doc")
            if doc == 0 and est > 0:
                doc = round(est / 25)
                st.markdown(f"🔎 *Docentes estimados: {doc}*")
            poblacion_por_sede[sede][grado] = {"estudiantes": est, "docentes": doc}

st.session_state["poblacion_por_sede"] = poblacion_por_sede

# Paso 7: Materiales
st.header("6️⃣ Selección de materiales")
materiales_por_estrategia = {
    "Transición": ["Cartilla docente transición", "Cartilla estudiante transición", "Cartilla de cuentos transición", "Kit aula transición"],
    "Primero": ["Guía docente tomo I", "Guía docente tomo II", "Guía estudiante unidad I", "Guía estudiante unidad II", "Guía estudiante unidad III", "Guía estudiante unidad IV", "Libro de cuentos", "Big Book", "Fichas", "Componedores aula", "Componedores individuales"],
    "Remediación": ["Guía docente remediación", "Guía estudiante remediación", "Cartilla cuentos remediación", "Fichas de apoyo remediación"]
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

st.session_state["materiales_seleccionados"] = materiales_seleccionados

# Paso 8: Logística (si presencial)
if "Formación" in componentes and modalidades.get("Formación") == "Presencial":
    st.header("7️⃣ Logística de formación")

    tipo_transporte = st.radio("¿Qué tipo de transporte se usará?", ["Terrestre", "Aéreo"])
    if tipo_transporte == "Aéreo":
        st.markdown("✈️ Costo estimado promedio: COP $400.000 a $600.000")

    costo_transporte = st.number_input("Costo promedio por visita (COP)", min_value=100000, value=500000 if tipo_transporte == "Aéreo" else 150000, step=50000)

    incluir_refrigerios = st.radio("¿Deseas incluir refrigerios?", ["Sí", "No"])
    if incluir_refrigerios == "Sí":
        valor_actual_refrigerio = 8000
        st.markdown(f"💰 Valor actual del refrigerio: **COP ${valor_actual_refrigerio:,.0f}**")
        actualizar_valor = st.radio("¿Deseas actualizar este valor?", ["No", "Sí"])
        if actualizar_valor == "Sí":
            valor_actual_refrigerio = st.number_input("Nuevo valor del refrigerio (COP)", min_value=1000, step=500)
        num_sesiones = st.number_input("¿En cuántas sesiones se ofrecerán refrigerios?", min_value=1, step=1)
        total_docentes = sum(info["docentes"] for sede in poblacion_por_sede.values() for info in sede.values())
        cantidad_refrigerios = int(round(total_docentes * 1.2 * num_sesiones))
        st.success(f"🥤 Total de refrigerios estimados: {cantidad_refrigerios}")
        st.session_state["refrigerios"] = {
            "valor_unitario": valor_actual_refrigerio,
            "num_sesiones": num_sesiones,
            "cantidad_refrigerios": cantidad_refrigerios
        }

    temas_formacion = [
        "Modelo pedagógico y didáctico",
        "Didáctica para transición",
        "Didáctica para primero",
        "Evaluación formativa",
        "Uso de materiales en el aula",
        "Acompañamiento a docentes"
    ]
    temas_seleccionados = st.multiselect("Selecciona los temas a trabajar", temas_formacion)
    st.session_state["formacion_logistica"] = {
        "transporte": tipo_transporte,
        "costo_transporte": costo_transporte,
        "temas": temas_seleccionados
    }
# Paso 9: Grupos de formación
if "Formación" in componentes:
    st.header("8️⃣ Grupos de formación")
    total_docentes = sum(info["docentes"] for sede in poblacion_por_sede.values() for info in sede.values())
    n_grupos = (total_docentes + 39) // 40
    st.success(f"👥 Total de docentes: {total_docentes}")
    st.info(f"🔹 Se requerirán {n_grupos} grupo(s) (máx. 40 personas por grupo)")
    st.session_state["grupos_formacion"] = {
        "total_docentes": total_docentes,
        "n_grupos": n_grupos
    }

# Paso 10: Remediación
if "Remediación" in estrategias:
    st.header("9️⃣ Estrategia de Remediación")
    porcentaje_remediacion = st.slider("¿Qué porcentaje de estudiantes de 2° a 5° requieren remediación?", 0, 100, 25)
    total_estudiantes_remediacion = sum(
        info["estudiantes"]
        for sede in poblacion_por_sede.values()
        for grado, info in sede.items()
        if grado in ["2°", "3°", "4°", "5°"]
    )
    estimado = int(round(total_estudiantes_remediacion * porcentaje_remediacion / 100))
    st.success(f"👧🧒 Se estima que {estimado} estudiantes requieren remediación")
    st.session_state["remediacion"] = {
        "porcentaje": porcentaje_remediacion,
        "total_grados_2_5": total_estudiantes_remediacion,
        "estimado_remediacion": estimado
    }

# Paso 11: Selección de pruebas (Monitoreo)
if "Monitoreo y Evaluación" in componentes and any(e in estrategias for e in ["Primero", "Remediación"]):
    st.header("🔍 Módulo de Monitoreo y Evaluación")
    st.markdown("### 📁 Selecciona las pruebas que deseas aplicar:")
    pruebas_disponibles = ["EGRA entrada", "EGRA salida"]
    if "Primero" in estrategias:
        pruebas_disponibles.extend(["Semana 10", "Semana 20", "Semana 30", "Semana 40"])
    if "Remediación" in estrategias:
        pruebas_disponibles.extend(["Semana 1", "Semana 7", "Semana 14"])
    pruebas_seleccionadas = st.multiselect("Pruebas disponibles según las estrategias seleccionadas:", pruebas_disponibles)
    st.session_state["pruebas_monitoreo"] = pruebas_seleccionadas

# Paso 12: Aplicación de pruebas y productos asociados
if "pruebas_monitoreo" in st.session_state and st.session_state["pruebas_monitoreo"]:
    st.header("📊 Aplicación de pruebas y productos por evaluación")

    productos_estandar = [
        "Informe de resultados",
        "Presentación a actores",
        "Informe técnico consolidado",
        "Devolución a instituciones"
    ]

    configuracion_pruebas = {}

    for prueba in st.session_state["pruebas_monitoreo"]:
        st.subheader(f"🧪 {prueba}")

        incluir_aplicacion = st.radio(
            f"¿Deseas incluir la aplicación de la prueba '{prueba}'?",
            ["Sí", "No"],
            key=f"aplicacion_{prueba}"
        )

        productos_incluidos = st.multiselect(
            f"Selecciona los productos que deseas incluir para '{prueba}':",
            productos_estandar,
            default=productos_estandar,
            key=f"productos_{prueba}"
        )

        configuracion_pruebas[prueba] = {
            "aplicacion": incluir_aplicacion == "Sí",
            "productos": productos_incluidos
        }

    st.session_state["configuracion_pruebas"] = configuracion_pruebas
