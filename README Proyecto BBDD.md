# Proyecto BBDD Bootcamp

Proyecto de creación de una base de datos relacional en PostgreSQL a partir de varios CSV con información de alumnos, promociones, profesores, proyectos y evaluaciones.

El objetivo principal es transformar datos iniciales no normalizados en una base de datos relacional funcional, con tablas relacionadas mediante claves primarias y claves foráneas.

---

## Estructura del proyecto

```text
Proyecto/
│
├── data/
│   ├── clase_1.csv
│   ├── clase_2.csv
│   ├── clase_3.csv
│   ├── clase_4.csv
│   └── claustro.csv
│
├── csv_limpios/
│   ├── campus.csv
│   ├── modalidad.csv
│   ├── vertical.csv
│   ├── promocion.csv
│   ├── alumno.csv
│   ├── matricula.csv
│   ├── profesor.csv
│   ├── asignacion_docente.csv
│   ├── proyecto.csv
│   └── evaluacion.csv
│
├── limpiar_csv.py
├── subir_datos_render.py
├── 01_creacion_tablas_proyecto_bbdd.sql
├── 03_consultas_demo_proyecto_bbdd.sql
└── README.md
```

---

## Modelo de datos

La base de datos está formada por las siguientes tablas:

- `campus`
- `modalidad`
- `vertical`
- `promocion`
- `alumno`
- `matricula`
- `profesor`
- `asignacion_docente`
- `proyecto`
- `evaluacion`

La tabla central del modelo es `promocion`.

Desde ella se relacionan los alumnos, profesores, campus, modalidad, vertical y evaluaciones.

---

## Relaciones principales

```text
campus      1 ─── N   promocion
modalidad   1 ─── N   promocion
vertical    1 ─── N   promocion
vertical    1 ─── N   proyecto

alumno      1 ─── N   matricula
promocion   1 ─── N   matricula

profesor    1 ─── N   asignacion_docente
promocion   1 ─── N   asignacion_docente

matricula   1 ─── N   evaluacion
proyecto    1 ─── N   evaluacion
```

---

## Requisitos

Para ejecutar el proyecto se necesita tener instalado:

- Python
- pandas
- sqlalchemy
- psycopg2-binary
- PostgreSQL o una base de datos PostgreSQL alojada en Render
- pgAdmin, opcional pero recomendado

Instalación de librerías:

```bash
pip install pandas sqlalchemy psycopg2-binary
```

---

## Pasos de ejecución

### 1. Crear las tablas en PostgreSQL

Ejecutar en pgAdmin el archivo:

```text
01_creacion_tablas_proyecto_bbdd.sql
```

Este script crea las tablas, claves primarias, claves foráneas y restricciones básicas.

---

### 2. Limpiar los CSV originales

Ejecutar:

```bash
python limpiar_csv.py
```

Este script lee los archivos de la carpeta `data/` y crea los CSV normalizados en la carpeta `csv_limpios/`.

---

### 3. Subir los datos a PostgreSQL

Ejecutar:

```bash
python subir_datos_render.py
```

Este script lee los CSV limpios y los inserta en las tablas de PostgreSQL.

> Nota: no se debe subir a GitHub ningún archivo que contenga contraseñas reales de conexión.

---

### 4. Ejecutar consultas de prueba

Ejecutar en pgAdmin el archivo:

```text
03_consultas_demo_proyecto_bbdd.sql
```

Este archivo contiene consultas para comprobar que la base de datos funciona correctamente.

---

## Consultas incluidas

Algunas consultas de prueba permiten ver:

- número de registros por tabla
- promociones con campus, modalidad y vertical
- alumnos por promoción
- profesores asignados a cada promoción
- evaluaciones por proyecto
- resultados de alumnos por proyecto

---

## Notas sobre los datos

Los CSV originales de alumnos no incluyen la columna `modalidad`.

Para mantener el modelo simple, las promociones de alumnos se han tratado como `Presencial`.

Además, se corrige la errata:

```text
Proyecto_FullSatck → FullStack
```

---

## Objetivo del proyecto

Este proyecto permite practicar:

- diseño de modelo entidad-relación
- creación de modelo lógico
- normalización básica de datos
- creación de tablas SQL
- uso de claves primarias y foráneas
- carga de datos desde Python
- consultas SQL con `JOIN`
- conexión entre PostgreSQL, Render y pgAdmin

---

## Estado del proyecto

Base de datos creada y cargada correctamente.

El proyecto incluye scripts de creación, limpieza, carga y consultas de validación.
