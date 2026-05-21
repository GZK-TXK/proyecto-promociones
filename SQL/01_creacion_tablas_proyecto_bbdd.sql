-- ============================================================
-- PUNTO 5: CREACIÓN DE TABLAS
-- Proyecto BBDD Bootcamp
-- Modelo lógico simplificado
--
-- Instrucción de uso:
-- Ejecutar este script en pgAdmin sobre la base de datos PostgreSQL
-- creada en Render.
--
-- Orden:
-- 1. Crear tablas
-- 2. Añadir Primary Keys
-- 3. Añadir Foreign Keys
-- 4. Añadir Unique Constraints
-- 5. Añadir Check Constraints
-- ============================================================


-- ============================================================
-- 1. CREACIÓN DE TABLAS
-- ============================================================

CREATE TABLE campus (
    id_campus SERIAL,
    nombre VARCHAR(50)
);

CREATE TABLE modalidad (
    id_modalidad SERIAL,
    nombre VARCHAR(50)
);

CREATE TABLE vertical (
    id_vertical SERIAL,
    nombre VARCHAR(50)
);

CREATE TABLE promocion (
    id_promocion SERIAL,
    nombre VARCHAR(50),
    fecha_comienzo DATE,
    id_campus INT,
    id_modalidad INT,
    id_vertical INT
);

CREATE TABLE alumno (
    id_alumno SERIAL,
    nombre VARCHAR(120),
    email VARCHAR(150)
);

CREATE TABLE matricula (
    id_matricula SERIAL,
    id_alumno INT,
    id_promocion INT
);

CREATE TABLE profesor (
    id_profesor SERIAL,
    nombre VARCHAR(120)
);

CREATE TABLE asignacion_docente (
    id_asignacion SERIAL,
    id_promocion INT,
    id_profesor INT,
    rol VARCHAR(20)
);

CREATE TABLE proyecto (
    id_proyecto SERIAL,
    nombre VARCHAR(100),
    id_vertical INT
);

CREATE TABLE evaluacion (
    id_evaluacion SERIAL,
    id_matricula INT,
    id_proyecto INT,
    resultado VARCHAR(20)
);


-- ============================================================
-- 2. PRIMARY KEYS
-- ============================================================

ALTER TABLE campus
ADD CONSTRAINT pk_campus
PRIMARY KEY (id_campus);

ALTER TABLE modalidad
ADD CONSTRAINT pk_modalidad
PRIMARY KEY (id_modalidad);

ALTER TABLE vertical
ADD CONSTRAINT pk_vertical
PRIMARY KEY (id_vertical);

ALTER TABLE promocion
ADD CONSTRAINT pk_promocion
PRIMARY KEY (id_promocion);

ALTER TABLE alumno
ADD CONSTRAINT pk_alumno
PRIMARY KEY (id_alumno);

ALTER TABLE matricula
ADD CONSTRAINT pk_matricula
PRIMARY KEY (id_matricula);

ALTER TABLE profesor
ADD CONSTRAINT pk_profesor
PRIMARY KEY (id_profesor);

ALTER TABLE asignacion_docente
ADD CONSTRAINT pk_asignacion_docente
PRIMARY KEY (id_asignacion);

ALTER TABLE proyecto
ADD CONSTRAINT pk_proyecto
PRIMARY KEY (id_proyecto);

ALTER TABLE evaluacion
ADD CONSTRAINT pk_evaluacion
PRIMARY KEY (id_evaluacion);


-- ============================================================
-- 3. FOREIGN KEYS
-- ============================================================

ALTER TABLE promocion
ADD CONSTRAINT fk_promocion_campus
FOREIGN KEY (id_campus)
REFERENCES campus(id_campus);

ALTER TABLE promocion
ADD CONSTRAINT fk_promocion_modalidad
FOREIGN KEY (id_modalidad)
REFERENCES modalidad(id_modalidad);

ALTER TABLE promocion
ADD CONSTRAINT fk_promocion_vertical
FOREIGN KEY (id_vertical)
REFERENCES vertical(id_vertical);

ALTER TABLE matricula
ADD CONSTRAINT fk_matricula_alumno
FOREIGN KEY (id_alumno)
REFERENCES alumno(id_alumno);

ALTER TABLE matricula
ADD CONSTRAINT fk_matricula_promocion
FOREIGN KEY (id_promocion)
REFERENCES promocion(id_promocion);

ALTER TABLE asignacion_docente
ADD CONSTRAINT fk_asignacion_docente_promocion
FOREIGN KEY (id_promocion)
REFERENCES promocion(id_promocion);

ALTER TABLE asignacion_docente
ADD CONSTRAINT fk_asignacion_docente_profesor
FOREIGN KEY (id_profesor)
REFERENCES profesor(id_profesor);

ALTER TABLE proyecto
ADD CONSTRAINT fk_proyecto_vertical
FOREIGN KEY (id_vertical)
REFERENCES vertical(id_vertical);

ALTER TABLE evaluacion
ADD CONSTRAINT fk_evaluacion_matricula
FOREIGN KEY (id_matricula)
REFERENCES matricula(id_matricula);

ALTER TABLE evaluacion
ADD CONSTRAINT fk_evaluacion_proyecto
FOREIGN KEY (id_proyecto)
REFERENCES proyecto(id_proyecto);


-- ============================================================
-- 4. UNIQUE CONSTRAINTS
-- ============================================================

ALTER TABLE campus
ADD CONSTRAINT uq_campus_nombre
UNIQUE (nombre);

ALTER TABLE modalidad
ADD CONSTRAINT uq_modalidad_nombre
UNIQUE (nombre);

ALTER TABLE vertical
ADD CONSTRAINT uq_vertical_nombre
UNIQUE (nombre);

ALTER TABLE alumno
ADD CONSTRAINT uq_alumno_email
UNIQUE (email);

ALTER TABLE profesor
ADD CONSTRAINT uq_profesor_nombre
UNIQUE (nombre);

ALTER TABLE promocion
ADD CONSTRAINT uq_promocion_unica
UNIQUE (nombre, fecha_comienzo, id_campus, id_modalidad, id_vertical);

ALTER TABLE matricula
ADD CONSTRAINT uq_matricula_alumno_promocion
UNIQUE (id_alumno, id_promocion);

ALTER TABLE asignacion_docente
ADD CONSTRAINT uq_asignacion_profesor_promocion
UNIQUE (id_profesor, id_promocion);

ALTER TABLE proyecto
ADD CONSTRAINT uq_proyecto_vertical
UNIQUE (nombre, id_vertical);

ALTER TABLE evaluacion
ADD CONSTRAINT uq_evaluacion_matricula_proyecto
UNIQUE (id_matricula, id_proyecto);


-- ============================================================
-- 5. CHECK CONSTRAINTS
-- ============================================================

ALTER TABLE asignacion_docente
ADD CONSTRAINT chk_asignacion_docente_rol
CHECK (rol IN ('TA', 'LI'));

ALTER TABLE evaluacion
ADD CONSTRAINT chk_evaluacion_resultado
CHECK (resultado IN ('Apto', 'No Apto'));


-- ============================================================
-- 6. VALIDACIÓN RÁPIDA
-- Ejecutar después de crear las tablas para comprobar que existen.
-- ============================================================

SELECT table_name
FROM information_schema.tables
WHERE table_schema = 'public'
ORDER BY table_name;
