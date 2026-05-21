import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy import text


# ============================================================
# SUBIDA DE CSV LIMPIOS A POSTGRESQL - RENDER
# ============================================================

# Este script lee los CSV de la carpeta csv_limpios
# y los sube a las tablas ya creadas en PostgreSQL.

# IMPORTANTE:
# Esta versión incluye la URL directamente para facilitar la carga local.
# No subas este archivo a GitHub con la contraseña real.


# ============================================================
# 1. CONEXIÓN A LA BASE DE DATOS
# ============================================================

database_url = "postgresql+psycopg2://proyecto_bbdd_user:JYpFWDJQ9zY44uoSgX5YpuZ0n5gxzBku@dpg-d872n0u7r5hc738dpfng-a.oregon-postgres.render.com:5432/proyecto_bbdd_421b"

engine = create_engine(database_url)


# ============================================================
# 2. BORRAR DATOS ANTERIORES
# ============================================================

with engine.begin() as connection:
    connection.execute(text("TRUNCATE TABLE evaluacion RESTART IDENTITY CASCADE;"))
    connection.execute(text("TRUNCATE TABLE asignacion_docente RESTART IDENTITY CASCADE;"))
    connection.execute(text("TRUNCATE TABLE matricula RESTART IDENTITY CASCADE;"))
    connection.execute(text("TRUNCATE TABLE proyecto RESTART IDENTITY CASCADE;"))
    connection.execute(text("TRUNCATE TABLE promocion RESTART IDENTITY CASCADE;"))
    connection.execute(text("TRUNCATE TABLE profesor RESTART IDENTITY CASCADE;"))
    connection.execute(text("TRUNCATE TABLE alumno RESTART IDENTITY CASCADE;"))
    connection.execute(text("TRUNCATE TABLE vertical RESTART IDENTITY CASCADE;"))
    connection.execute(text("TRUNCATE TABLE modalidad RESTART IDENTITY CASCADE;"))
    connection.execute(text("TRUNCATE TABLE campus RESTART IDENTITY CASCADE;"))


# ============================================================
# 3. CARGAR CSV LIMPIOS
# ============================================================

df_campus = pd.read_csv("csv_limpios/campus.csv")
df_modalidad = pd.read_csv("csv_limpios/modalidad.csv")
df_vertical = pd.read_csv("csv_limpios/vertical.csv")
df_profesor = pd.read_csv("csv_limpios/profesor.csv")
df_alumno = pd.read_csv("csv_limpios/alumno.csv")
df_promocion = pd.read_csv("csv_limpios/promocion.csv")
df_proyecto = pd.read_csv("csv_limpios/proyecto.csv")
df_matricula = pd.read_csv("csv_limpios/matricula.csv")
df_asignacion_docente = pd.read_csv("csv_limpios/asignacion_docente.csv")
df_evaluacion = pd.read_csv("csv_limpios/evaluacion.csv")


# ============================================================
# 4. SUBIR CSV A POSTGRESQL
# ============================================================

df_campus.to_sql("campus", engine, if_exists="append", index=False)
df_modalidad.to_sql("modalidad", engine, if_exists="append", index=False)
df_vertical.to_sql("vertical", engine, if_exists="append", index=False)
df_profesor.to_sql("profesor", engine, if_exists="append", index=False)
df_alumno.to_sql("alumno", engine, if_exists="append", index=False)
df_promocion.to_sql("promocion", engine, if_exists="append", index=False)
df_proyecto.to_sql("proyecto", engine, if_exists="append", index=False)
df_matricula.to_sql("matricula", engine, if_exists="append", index=False)
df_asignacion_docente.to_sql("asignacion_docente", engine, if_exists="append", index=False)
df_evaluacion.to_sql("evaluacion", engine, if_exists="append", index=False)


# ============================================================
# 5. COMPROBACIÓN FINAL
# ============================================================

consulta = """
SELECT 'campus' AS tabla, COUNT(*) AS registros FROM campus
UNION ALL
SELECT 'modalidad', COUNT(*) FROM modalidad
UNION ALL
SELECT 'vertical', COUNT(*) FROM vertical
UNION ALL
SELECT 'promocion', COUNT(*) FROM promocion
UNION ALL
SELECT 'alumno', COUNT(*) FROM alumno
UNION ALL
SELECT 'matricula', COUNT(*) FROM matricula
UNION ALL
SELECT 'profesor', COUNT(*) FROM profesor
UNION ALL
SELECT 'asignacion_docente', COUNT(*) FROM asignacion_docente
UNION ALL
SELECT 'proyecto', COUNT(*) FROM proyecto
UNION ALL
SELECT 'evaluacion', COUNT(*) FROM evaluacion;
"""

df_comprobacion = pd.read_sql(consulta, engine)

print(df_comprobacion)
