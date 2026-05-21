import pandas as pd
import os


# ============================================================
# LIMPIEZA CSV - PROYECTO BBDD BOOTCAMP
# ============================================================

# Este script:
# 1. Lee los CSV originales desde la carpeta data.
# 2. Crea los dataframes necesarios para la base de datos.
# 3. Guarda los CSV limpios en la carpeta csv_limpios.

# IMPORTANTE:
# Ejecutar este archivo desde la carpeta principal del proyecto:
# Proyecto/
# ├── data/
# ├── csv_limpios/
# └── limpiar_csv.py


# ============================================================
# 1. CREACIÓN DE CARPETA DE SALIDA
# ============================================================

os.makedirs("csv_limpios", exist_ok=True)


# ============================================================
# 2. CARGA DE CSV ORIGINALES
# ============================================================

df_clase_1 = pd.read_csv("data/clase_1.csv")
df_clase_2 = pd.read_csv("data/clase_2.csv")
df_clase_3 = pd.read_csv("data/clase_3.csv")
df_clase_4 = pd.read_csv("data/clase_4.csv")
df_claustro = pd.read_csv("data/claustro.csv")


# ============================================================
# 3. AÑADIR VERTICAL A CADA CLASE
# ============================================================

df_clase_1["vertical"] = "Data Science"
df_clase_2["vertical"] = "Data Science"

df_clase_3["vertical"] = "Full Stack"
df_clase_4["vertical"] = "Full Stack"


# ============================================================
# 4. UNIR LOS CSV DE ALUMNOS
# ============================================================

df_alumnos = pd.concat(
    [df_clase_1, df_clase_2, df_clase_3, df_clase_4],
    ignore_index=True
)


# ============================================================
# 5. LIMPIEZA BÁSICA DE ALUMNOS
# ============================================================

for columna in df_alumnos.columns:
    if df_alumnos[columna].dtype == "object":
        df_alumnos[columna] = df_alumnos[columna].str.strip()

df_alumnos["Email"] = df_alumnos["Email"].str.lower()

df_alumnos["Fecha_comienzo"] = pd.to_datetime(
    df_alumnos["Fecha_comienzo"],
    dayfirst=True
)

df_alumnos["Fecha_comienzo"] = df_alumnos["Fecha_comienzo"].dt.strftime("%Y-%m-%d")

df_alumnos = df_alumnos.rename(columns={
    "Nombre": "nombre",
    "Email": "email",
    "Promoción": "promocion",
    "Fecha_comienzo": "fecha_comienzo",
    "Campus": "campus"
})


# ============================================================
# 6. LIMPIEZA BÁSICA DE CLAUSTRO
# ============================================================

for columna in df_claustro.columns:
    if df_claustro[columna].dtype == "object":
        df_claustro[columna] = df_claustro[columna].str.strip()

df_claustro = df_claustro.rename(columns={
    "Nombre": "nombre",
    "Rol": "rol",
    "Vertical": "vertical",
    "Promocion": "promocion",
    "Campus": "campus",
    "Modalidad": "modalidad"
})

df_claustro["vertical"] = df_claustro["vertical"].replace({
    "DS": "Data Science",
    "FS": "Full Stack"
})


# ============================================================
# 7. TABLA CAMPUS
# ============================================================

df_campus_1 = df_alumnos[["campus"]].rename(columns={"campus": "nombre"})
df_campus_2 = df_claustro[["campus"]].rename(columns={"campus": "nombre"})

df_campus = pd.concat(
    [df_campus_1, df_campus_2],
    ignore_index=True
)

df_campus = df_campus.drop_duplicates()
df_campus = df_campus.sort_values("nombre").reset_index(drop=True)

df_campus["id_campus"] = df_campus.index + 1
df_campus = df_campus[["id_campus", "nombre"]]

df_campus.to_csv(
    "csv_limpios/campus.csv",
    index=False
)


# ============================================================
# 8. TABLA MODALIDAD
# ============================================================

df_modalidad = pd.DataFrame({
    "id_modalidad": [1, 2],
    "nombre": ["Presencial", "Online"]
})

df_modalidad.to_csv(
    "csv_limpios/modalidad.csv",
    index=False
)


# ============================================================
# 9. TABLA VERTICAL
# ============================================================

df_vertical = pd.DataFrame({
    "id_vertical": [1, 2],
    "nombre": ["Data Science", "Full Stack"]
})

df_vertical.to_csv(
    "csv_limpios/vertical.csv",
    index=False
)


# ============================================================
# 10. MAPAS DE IDS PARA RELACIONAR TABLAS
# ============================================================

mapa_campus = dict(zip(df_campus["nombre"], df_campus["id_campus"]))
mapa_modalidad = dict(zip(df_modalidad["nombre"], df_modalidad["id_modalidad"]))
mapa_vertical = dict(zip(df_vertical["nombre"], df_vertical["id_vertical"]))


# ============================================================
# 11. TABLA PROMOCION
# ============================================================

df_promocion_alumnos = df_alumnos[[
    "promocion",
    "fecha_comienzo",
    "campus",
    "vertical"
]].copy()

df_promocion_alumnos = df_promocion_alumnos.drop_duplicates()
df_promocion_alumnos["modalidad"] = "Presencial"


# Fechas por promoción para poder completar datos del claustro.
df_fechas = df_alumnos[["promocion", "fecha_comienzo"]].drop_duplicates()
mapa_fechas = dict(zip(df_fechas["promocion"], df_fechas["fecha_comienzo"]))


df_promocion_claustro = df_claustro[[
    "promocion",
    "campus",
    "vertical"
]].copy()

df_promocion_claustro = df_promocion_claustro.drop_duplicates()
df_promocion_claustro["fecha_comienzo"] = df_promocion_claustro["promocion"].map(mapa_fechas)
df_promocion_claustro["modalidad"] = "Presencial"


df_promocion = pd.concat(
    [df_promocion_alumnos, df_promocion_claustro],
    ignore_index=True
)

df_promocion = df_promocion.drop_duplicates(
    subset=["promocion", "fecha_comienzo", "campus", "vertical"]
)

df_promocion = df_promocion.sort_values([
    "vertical",
    "promocion",
    "campus"
]).reset_index(drop=True)

df_promocion["id_promocion"] = df_promocion.index + 1
df_promocion["id_campus"] = df_promocion["campus"].map(mapa_campus)
df_promocion["id_modalidad"] = df_promocion["modalidad"].map(mapa_modalidad)
df_promocion["id_vertical"] = df_promocion["vertical"].map(mapa_vertical)

df_promocion = df_promocion.rename(columns={
    "promocion": "nombre"
})

df_promocion["clave_promocion"] = (
    df_promocion["nombre"] + "|" +
    df_promocion["fecha_comienzo"] + "|" +
    df_promocion["campus"] + "|" +
    df_promocion["vertical"]
)

mapa_promocion = dict(zip(
    df_promocion["clave_promocion"],
    df_promocion["id_promocion"]
))

df_promocion_final = df_promocion[[
    "id_promocion",
    "nombre",
    "fecha_comienzo",
    "id_campus",
    "id_modalidad",
    "id_vertical"
]]

df_promocion_final.to_csv(
    "csv_limpios/promocion.csv",
    index=False
)


# ============================================================
# 12. TABLA ALUMNO
# ============================================================

df_alumno = df_alumnos[["nombre", "email"]].copy()

df_alumno = df_alumno.drop_duplicates(subset=["email"])
df_alumno = df_alumno.sort_values("email").reset_index(drop=True)

df_alumno["id_alumno"] = df_alumno.index + 1
df_alumno = df_alumno[["id_alumno", "nombre", "email"]]

mapa_alumno = dict(zip(df_alumno["email"], df_alumno["id_alumno"]))

df_alumno.to_csv(
    "csv_limpios/alumno.csv",
    index=False
)


# ============================================================
# 13. TABLA MATRICULA
# ============================================================

df_matricula = df_alumnos[[
    "email",
    "promocion",
    "fecha_comienzo",
    "campus",
    "vertical"
]].copy()

df_matricula["id_alumno"] = df_matricula["email"].map(mapa_alumno)

df_matricula["clave_promocion"] = (
    df_matricula["promocion"] + "|" +
    df_matricula["fecha_comienzo"] + "|" +
    df_matricula["campus"] + "|" +
    df_matricula["vertical"]
)

df_matricula["id_promocion"] = df_matricula["clave_promocion"].map(mapa_promocion)

df_matricula = df_matricula[["id_alumno", "id_promocion"]]
df_matricula = df_matricula.drop_duplicates()
df_matricula = df_matricula.sort_values([
    "id_promocion",
    "id_alumno"
]).reset_index(drop=True)

df_matricula["id_matricula"] = df_matricula.index + 1
df_matricula = df_matricula[[
    "id_matricula",
    "id_alumno",
    "id_promocion"
]]

df_matricula["clave_matricula"] = (
    df_matricula["id_alumno"].astype(str) + "|" +
    df_matricula["id_promocion"].astype(str)
)

mapa_matricula = dict(zip(
    df_matricula["clave_matricula"],
    df_matricula["id_matricula"]
))

df_matricula_final = df_matricula[[
    "id_matricula",
    "id_alumno",
    "id_promocion"
]]

df_matricula_final.to_csv(
    "csv_limpios/matricula.csv",
    index=False
)


# ============================================================
# 14. TABLA PROFESOR
# ============================================================

df_profesor = df_claustro[["nombre"]].copy()

df_profesor = df_profesor.drop_duplicates()
df_profesor = df_profesor.sort_values("nombre").reset_index(drop=True)

df_profesor["id_profesor"] = df_profesor.index + 1
df_profesor = df_profesor[["id_profesor", "nombre"]]

mapa_profesor = dict(zip(
    df_profesor["nombre"],
    df_profesor["id_profesor"]
))

df_profesor.to_csv(
    "csv_limpios/profesor.csv",
    index=False
)


# ============================================================
# 15. TABLA ASIGNACION_DOCENTE
# ============================================================

df_asignacion_docente = df_claustro[[
    "nombre",
    "rol",
    "promocion",
    "campus",
    "vertical"
]].copy()

df_asignacion_docente["id_profesor"] = df_asignacion_docente["nombre"].map(mapa_profesor)
df_asignacion_docente["fecha_comienzo"] = df_asignacion_docente["promocion"].map(mapa_fechas)

df_asignacion_docente["clave_promocion"] = (
    df_asignacion_docente["promocion"] + "|" +
    df_asignacion_docente["fecha_comienzo"] + "|" +
    df_asignacion_docente["campus"] + "|" +
    df_asignacion_docente["vertical"]
)

df_asignacion_docente["id_promocion"] = df_asignacion_docente["clave_promocion"].map(mapa_promocion)

df_asignacion_docente = df_asignacion_docente[[
    "id_promocion",
    "id_profesor",
    "rol"
]]

df_asignacion_docente = df_asignacion_docente.drop_duplicates()
df_asignacion_docente = df_asignacion_docente.sort_values([
    "id_promocion",
    "id_profesor"
]).reset_index(drop=True)

df_asignacion_docente["id_asignacion"] = df_asignacion_docente.index + 1

df_asignacion_docente = df_asignacion_docente[[
    "id_asignacion",
    "id_promocion",
    "id_profesor",
    "rol"
]]

df_asignacion_docente.to_csv(
    "csv_limpios/asignacion_docente.csv",
    index=False
)


# ============================================================
# 16. TABLA PROYECTO
# ============================================================

df_proyecto_ds = pd.DataFrame({
    "nombre": ["HLF", "EDA", "BBDD", "ML", "Deployment"],
    "vertical": ["Data Science", "Data Science", "Data Science", "Data Science", "Data Science"]
})

df_proyecto_fs = pd.DataFrame({
    "nombre": ["WebDev", "FrontEnd", "Backend", "React", "FullStack"],
    "vertical": ["Full Stack", "Full Stack", "Full Stack", "Full Stack", "Full Stack"]
})

df_proyecto = pd.concat(
    [df_proyecto_ds, df_proyecto_fs],
    ignore_index=True
)

df_proyecto["id_vertical"] = df_proyecto["vertical"].map(mapa_vertical)
df_proyecto["id_proyecto"] = df_proyecto.index + 1

df_proyecto["clave_proyecto"] = (
    df_proyecto["nombre"] + "|" +
    df_proyecto["id_vertical"].astype(str)
)

mapa_proyecto = dict(zip(
    df_proyecto["clave_proyecto"],
    df_proyecto["id_proyecto"]
))

df_proyecto_final = df_proyecto[[
    "id_proyecto",
    "nombre",
    "id_vertical"
]]

df_proyecto_final.to_csv(
    "csv_limpios/proyecto.csv",
    index=False
)


# ============================================================
# 17. TABLA EVALUACION
# ============================================================

columnas_proyectos = [
    "Proyecto_HLF",
    "Proyecto_EDA",
    "Proyecto_BBDD",
    "Proyecto_ML",
    "Proyecto_Deployment",
    "Proyecto_WebDev",
    "Proyecto_FrontEnd",
    "Proyecto_Backend",
    "Proyecto_React",
    "Proyecto_FullSatck"
]

df_evaluacion = df_alumnos.melt(
    id_vars=[
        "nombre",
        "email",
        "promocion",
        "fecha_comienzo",
        "campus",
        "vertical"
    ],
    value_vars=columnas_proyectos,
    var_name="columna_proyecto",
    value_name="resultado"
)

df_evaluacion = df_evaluacion.dropna(subset=["resultado"])

mapa_nombre_proyecto = {
    "Proyecto_HLF": "HLF",
    "Proyecto_EDA": "EDA",
    "Proyecto_BBDD": "BBDD",
    "Proyecto_ML": "ML",
    "Proyecto_Deployment": "Deployment",
    "Proyecto_WebDev": "WebDev",
    "Proyecto_FrontEnd": "FrontEnd",
    "Proyecto_Backend": "Backend",
    "Proyecto_React": "React",
    "Proyecto_FullSatck": "FullStack"
}

df_evaluacion["proyecto"] = df_evaluacion["columna_proyecto"].map(mapa_nombre_proyecto)
df_evaluacion["id_alumno"] = df_evaluacion["email"].map(mapa_alumno)

df_evaluacion["clave_promocion"] = (
    df_evaluacion["promocion"] + "|" +
    df_evaluacion["fecha_comienzo"] + "|" +
    df_evaluacion["campus"] + "|" +
    df_evaluacion["vertical"]
)

df_evaluacion["id_promocion"] = df_evaluacion["clave_promocion"].map(mapa_promocion)

df_evaluacion["clave_matricula"] = (
    df_evaluacion["id_alumno"].astype(str) + "|" +
    df_evaluacion["id_promocion"].astype(str)
)

df_evaluacion["id_matricula"] = df_evaluacion["clave_matricula"].map(mapa_matricula)
df_evaluacion["id_vertical"] = df_evaluacion["vertical"].map(mapa_vertical)

df_evaluacion["clave_proyecto"] = (
    df_evaluacion["proyecto"] + "|" +
    df_evaluacion["id_vertical"].astype(str)
)

df_evaluacion["id_proyecto"] = df_evaluacion["clave_proyecto"].map(mapa_proyecto)

df_evaluacion = df_evaluacion[[
    "id_matricula",
    "id_proyecto",
    "resultado"
]]

df_evaluacion = df_evaluacion.sort_values([
    "id_matricula",
    "id_proyecto"
]).reset_index(drop=True)

df_evaluacion["id_evaluacion"] = df_evaluacion.index + 1

df_evaluacion = df_evaluacion[[
    "id_evaluacion",
    "id_matricula",
    "id_proyecto",
    "resultado"
]]

df_evaluacion.to_csv(
    "csv_limpios/evaluacion.csv",
    index=False
)
