
# Red Social Académica

## Descripción

**Red Social Académica** es una plataforma web tipo red social enfocada a entornos educativos, diseñada bajo una arquitectura de microservicios, permitiendo funcionalidades como gestión de usuarios, foros, grupos y chat en tiempo real. El sistema es modular, escalable y seguro, pensado para adaptarse tanto a entornos académicos como profesionales.

---

## Arquitectura General

El sistema utiliza **arquitectura de microservicios** orquestados mediante contenedores Docker y coordinados a través de un **API Gateway** implementado con Nginx. Cada microservicio tiene su propia base de datos, lo que garantiza la independencia y escalabilidad de cada módulo. El frontend es una SPA (Single Page Application) desarrollada en Vue.js.

### Diagrama General

```
[ SPA Vue.js ]
      |
   [Nginx API Gateway]
      |
----------------------------------------------------------
|         |         |          |           
Users  Community  Publications  Chat   
(Django) (Django)   (Django)   (Go)  
 Postgres  Postgres  Postgres  MongoDB  
```

### Microservicios Principales

- **Users:** Gestión de usuarios, autenticación JWT, registro, perfil, actualización, etc.
- **Community:** Gestión de grupos, inscripción, eliminación y consulta de miembros.
- **Publications:** Gestión de publicaciones y tareas en foros y grupos, comentarios, calificaciones y subida de archivos.
- **Chat:** Chat en tiempo real mediante WebSocket, con cifrado y persistencia en MongoDB.
- **Frontend:** SPA en Vue.js que consume los servicios expuestos por el API Gateway.

---

## Estructura de Carpetas

Un ejemplo de cómo podría estar organizado el proyecto a nivel raíz:

```
/red-social-academica/
├── services/
│   ├── users/           # Microservicio de usuarios (Django + Postgres)
│   ├── community/       # Microservicio de comunidades (Django + Postgres)
│   ├── publications/    # Microservicio de publicaciones y tareas (Django + Postgres)
│   ├── chat/            # Microservicio de chat (Go + MongoDB)
│   └── frontend/        # Aplicación Vue.js (SPA)
├── nginx/               # Configuración de Nginx (API Gateway, Websocket proxy)
├── docker-compose.yml   # Orquestación de todos los servicios
├── README.md            # Este archivo
└── docs/                # Documentación y especificaciones
```

Cada microservicio incluye su propio código fuente, configuración de base de datos, migraciones y documentación técnica específica.

---

## Funcionalidades Principales

### 1. Gestión de Usuarios
- Registro y autenticación segura (JWT).
- Cambio de contraseña y actualización de perfil.
- Validaciones estrictas de correo, nombre y contraseña.
- Generación de avatar dinámico a partir del nombre.

### 2. Grupos y Foros
- Creación y administración de grupos y foros.
- Inscripción mediante código o búsqueda.
- Gestión de miembros, roles y permisos.
- Eliminación y salida de grupos o foros.

### 3. Publicaciones y Tareas
- Creación, edición y eliminación de publicaciones.
- Soporte para comentarios y ordenamiento.
- Gestión de tareas (asignación, entrega, calificación).
- Subida de archivos (Word, PDF, PowerPoint, Excel).

### 4. Chat en tiempo real
- Mensajería privada mediante WebSocket.
- Lista de chats recientes y búsqueda de usuarios.
- Persistencia de mensajes en MongoDB.

---

## Instalación y Montaje en Local

### Prerrequisitos

- [Docker](https://www.docker.com/) y [Docker Compose](https://docs.docker.com/compose/)
- Node.js (para desarrollo frontend local)
- Git

### 1. Clona el repositorio

```bash
git clone https://github.com/tu_usuario/red-social-academica.git
cd red-social-academica
```

### 2. Configura variables de entorno

Cada microservicio puede requerir su propio archivo `.env`. Consulta la documentación interna de cada uno en `services/<microservicio>/.env.example` y crea los archivos necesarios.

### 3. Levanta los servicios con Docker Compose

```bash
docker-compose up --build
```

Esto construirá y levantará todos los microservicios, bases de datos y el frontend. Nginx se encargará del enrutamiento entre servicios.

### 4. Accede a la aplicación

Abre tu navegador y entra a:  
```
http://localhost:8080
```
o la URL indicada por el frontend.

### 5. Desarrollo local del Frontend (opcional)

Si quieres trabajar solo en el frontend:

```bash
cd services/frontend
npm install
npm run serve
```
El frontend se conectará a los endpoints del backend si los servicios están corriendo.

---

## Documentación Adicional

- **[Requisitos funcionales y no funcionales](./requisitos/requisitos.pdf):** Especificaciones completas del sistema.
- **[Arquitectura y diagramas](./arquitectura/arquitectura-final.pdf):** Diagramas C4, flujos y detalle técnico de cada microservicio.

---

## Licencia

Este proyecto es únicamente para fines académicos. Prohibida su reproducción, distribución o transformación sin consentimiento.

---
