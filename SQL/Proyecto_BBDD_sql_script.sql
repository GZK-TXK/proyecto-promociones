CREATE TABLE modalidades (
    id_modalidad SERIAL PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL
);


CREATE TABLE campus (
    id_campus SERIAL PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL
);


CREATE TABLE verticales (
    id_vertical SERIAL PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL
);


CREATE TABLE profesores (
    id_profesor SERIAL PRIMARY KEY,
    nombre VARCHAR(120) NOT NULL
);


CREATE TABLE alumnos (
    id_alumno SERIAL PRIMARY KEY,
    nombre VARCHAR(120) NOT NULL,
    email VARCHAR(150)
);


CREATE TABLE proyectos (
    id_proyecto SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL
);


CREATE TABLE cursos (
    id_curso SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL
);


CREATE TABLE promociones (
    id_promocion SERIAL PRIMARY KEY,
    nombre VARCHAR(30) NOT NULL,
    anio SMALLINT,
    fecha_comienzo DATE,
    aula VARCHAR(50),

    id_curso INTEGER NOT NULL,
    id_campus INTEGER NOT NULL,
    id_modalidad INTEGER NOT NULL,
    id_vertical INTEGER NOT NULL,

    id_profesor_li INTEGER NOT NULL,
    id_profesor_ta INTEGER NOT NULL,

    CONSTRAINT fk_promociones_curso
        FOREIGN KEY (id_curso)
        REFERENCES cursos(id_curso),

    CONSTRAINT fk_promociones_campus
        FOREIGN KEY (id_campus)
        REFERENCES campus(id_campus),

    CONSTRAINT fk_promociones_modalidad
        FOREIGN KEY (id_modalidad)
        REFERENCES modalidades(id_modalidad),

    CONSTRAINT fk_promociones_vertical
        FOREIGN KEY (id_vertical)
        REFERENCES verticales(id_vertical),

    CONSTRAINT fk_promociones_profesor_li
        FOREIGN KEY (id_profesor_li)
        REFERENCES profesores(id_profesor),

    CONSTRAINT fk_promociones_profesor_ta
        FOREIGN KEY (id_profesor_ta)
        REFERENCES profesores(id_profesor)
);


CREATE TABLE matriculas (
    id_matricula SERIAL PRIMARY KEY,
    id_alumno INTEGER NOT NULL,
    id_curso INTEGER NOT NULL,
    fecha_matricula DATE,

    CONSTRAINT fk_matriculas_alumno
        FOREIGN KEY (id_alumno)
        REFERENCES alumnos(id_alumno),

    CONSTRAINT fk_matriculas_curso
        FOREIGN KEY (id_curso)
        REFERENCES cursos(id_curso)
);


CREATE TABLE evaluaciones (
    id_evaluacion SERIAL PRIMARY KEY,
    id_proyecto INTEGER NOT NULL,
    id_alumno INTEGER NOT NULL,
    resultado VARCHAR(20),

    CONSTRAINT fk_evaluaciones_proyecto
        FOREIGN KEY (id_proyecto)
        REFERENCES proyectos(id_proyecto),

    CONSTRAINT fk_evaluaciones_alumno
        FOREIGN KEY (id_alumno)
        REFERENCES alumnos(id_alumno)
);


CREATE TABLE temario (
    id_proyecto INTEGER NOT NULL,
    id_vertical INTEGER NOT NULL,

    PRIMARY KEY (id_proyecto, id_vertical),

    CONSTRAINT fk_temario_proyecto
        FOREIGN KEY (id_proyecto)
        REFERENCES proyectos(id_proyecto),

    CONSTRAINT fk_temario_vertical
        FOREIGN KEY (id_vertical)
        REFERENCES verticales(id_vertical)
);