# MVP Laboral.AI B2B

## Descripción del Proyecto

**Laboral.AI B2B** conecta empresas con empleados usando inteligencia artificial. Este repositorio contiene el MVP con las siguientes funcionalidades: Login, Registro y Publicación de Empleos. Utilizamos un frontend HTML, CSS y Javascript y un backend basado en Python, Flask con servicios serverless sobre AWS (API Gateway, Lambda, DynamoDB) para proporcionar una solución escalable y flexible. El objetivo del MVP es crear, modificar, listar, y eliminar empleos y usuarios asociados a una empresa, mientras que los datos se almacenan en una base de datos NoSQL utilizando DynamoDB.

## Ejecución del Proyecto

### 1. Clonar el Repositorio

```shell
$ git clone https://github.com/denzelbautista/mvp-laboral-ai
$ cd mvp-laboral-ai
```

### 2. Crear el Entorno Virtual

```shell
$ python3 -m venv .venv
```

### 3. Activar el Entorno Virtual

**Linux/MacOS:**
```shell
$ source .venv/bin/activate
```

**Windows:**
```shell
$ .venv\Scripts\activate
```

### 4. Instalar las Dependencias

```shell
$ pip install -r requirements.txt
```

### 6. Ejecutar el Proyecto

```shell
$ python app.py
```

Esto levantará el servidor local para visualizar el frontend y poder realizar las pruebas de la API con acciones como **registro de empresa, usuario, modificación de empresa, usuario y creación, listado , modificación y eliminación de empleos por parte de una empresa**.

## Esquema de la Base de Datos

### 1. Empresa

- **Partition Key (`empresa_id`)**: Identificador único para la empresa.
- **Sort Key (`detalle_key`)**: `EMPRESA#{empresa_id}`
- **Atributos (flexible)**:
```json
{
  "empresa_id": "12345",
  "detalle_key": "EMPRESA#12345",
  "empresa_datos": {
    "nombre": "Empresa XYZ",
    "ubicacion": "Lima",
    "industria": "Tecnología",
    ...
  }
}
```

### 2. Empleo

- **Partition Key (`empresa_id`)**: `12345`
- **Sort Key (`detalle_key`)**: `EMPLEO#{empleo_id}`
- **Atributos (flexible)**:
```json
{
  "empresa_id": "12345",
  "detalle_key": "EMPLEO#67890",
  "empleo_datos": {
    "titulo": "Desarrollador Backend",
    "descripcion": "Se busca desarrollador con experiencia en Node.js",
    "ubicacion": "Remoto",
    "salario": 5000,
    ...
  }
}
```

### 3. Usuario

- **Partition Key (`empresa_id`)**: `12345`
- **Sort Key (`detalle_key`)**: `USUARIO#{usuario_id}`
- **Atributos (flexible)**:
```json
{
  "empresa_id": "12345",
  "detalle_key": "USUARIO#abcde12345",
  "usuario_datos": {
    "nombre": "Juan Pérez",
    "email": "juan@example.com",
    "rol": "Administrador",
    ...
  }
}
```

## Documentación de las API's

### API Empresa

Base URL: `https://7yvvp7f7s5.execute-api.us-east-1.amazonaws.com/prod/empresa`

#### Endpoints disponibles

#### 1. Crear Empresa

- **URL**: `POST /empresa/crear`
- **Descripción**: Crea una empresa.
- **Body**:
```json
{
  "empresa_datos": {
    "nombre": "Empresa XYZ",
    "ubicacion": "Lima",
    "industria": "Tecnología"
  }
}
```

#### 2. Editar Empresa

- **URL**: `PUT /empresa/modificar`
- **Descripción**: Lista todos los empleos asociados a una empresa.
- **Body**:
```json
{
  "empresa_id": "12345",
  "empresa_datos": {
    "nombre": "Empresa XYA",
    "ubicacion": "Puno",
    "industria": "Tecnología"
  }
}
```

### API Usuario

Base URL: `https://dav4oqy7e9.execute-api.us-east-1.amazonaws.com/prod/usuarios`

#### Endpoints disponibles

#### 1. Crear Usuario

- **URL**: `POST /usuarios/crear`
- **Descripción**: Crea un nuevo usuario asociado a una empresa.
- **Body**:
```json
{
  "empresa_id": "12345",
  "usuario_datos": {
    "nombre": "Juan Pérez",
    "email": "juan@example.com",
    "rol": "Administrador"
  }
}
```

#### 2. Listar Usuarios

- **URL**: `POST /usuarios/listartodos`
- **Descripción**: Lista todos los usuarios asociados a una empresa.
- **Body**:
```json
{}
```

#### 3. Modificar Usuario

- **URL**: `PUT /usuarios/modificar`
- **Descripción**: Modifica un usuario existente.
- **Body**:
```json
{
  "empresa_id": "12345",
  "detalle_key": "USUARIO#435312",
  "usuario_datos": {
    "nombre": "Juan Pérez",
    "email": "juan@example.com",
    "rol": "Administrador"
  }
}
```

#### 4. Eliminar Usuario

- **URL**: `DELETE /usuarios/eliminar`
- **Descripción**: Elimina un usuario existente.
- **Body**:
```json
{
  "empresa_id": "12345",
  "detalle_key": "USUARIO#435312"
}
```

### API Empleo

Base URL: `https://azy1wlrgli.execute-api.us-east-1.amazonaws.com/prod/empleos`

#### Endpoints disponibles

#### 1. Crear Empleo

- **URL**: `POST /empleos/crear`
- **Descripción**: Crea un nuevo empleo asociado a una empresa.
- **Body**:
```json
{
  "empresa_id": "12345",
  "empleo_datos": {
    "titulo": "Desarrollador Backend",
    "descripcion": "Se busca desarrollador con experiencia en Node.js",
    "ubicacion": "Remoto",
    "salario": 5000
  }
}
```

#### 2. Listar Empleos

- **URL**: `POST /empleos/listartodos`
- **Descripción**: Lista todos los empleos asociados a una empresa.
- **Body**:
```json
{}
```

#### 3. Modificar Empleo

- **URL**: `PUT /empleos/modificar`
- **Descripción**: Modifica un empleo existente.
- **Body**:
```json
{
  "empresa_id": "12345",
  "detalle_key": "EMPLEO#435312",
  "empleo_datos": {
    "titulo": "Desarrollador Backend",
    "descripcion": "Se busca desarrollador con experiencia en Node.js",
    "ubicacion": "Remoto",
    "salario": 5000
  }
}
```

#### 4. Eliminar Empleo

- **URL**: `DELETE /empleos/eliminar`
- **Descripción**: Elimina un empleo existente.
- **Body**:
```json
{
  "empresa_id": "12345",
  "detalle_key": "EMPLEO#435312"
}
```

## Consideraciones de Diseño

- **Escalabilidad**: El esquema NoSQL está diseñado para manejar grandes volúmenes de datos y consultas rápidas.
- **Flexibilidad**: Los atributos son flexibles y se adaptan a cambios en los datos de empresas, empleos y usuarios.
- **Desempeño**: El uso de claves de partición y ordenamiento optimiza las consultas para operaciones de CRUD eficientes.
