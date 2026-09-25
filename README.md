# device_systems

**GA1-220501096-01-AA1-EV07 – Fundamentos de FastAPI**

---

## Descripción

`device_systems` es una API REST construida con FastAPI para administrar usuarios del sistema. Permite listar, consultar, filtrar y registrar usuarios con validaciones de datos usando Pydantic v2.

---

## Instalación de dependencias

```bash
python -m venv venv
venv\Scripts\activate
pip install fastapi uvicorn pydantic[email]
pip freeze > requirements.txt
```

---

## Ejecución del servidor

```bash
uvicorn app.main:app --reload
```

El servidor queda disponible en:

- API: http://127.0.0.1:8000
- Swagger UI: http://127.0.0.1:8000/docs

---

## Estructura del proyecto

```
device_systems/
│── app/
│   │── main.py
│   │── schemas/
│   │   │── __init__.py
│   │   │── user_schema.py
│   │── routes/
│   │   │── __init__.py
│   │   │── user_routes.py
│   │── __init__.py
│── requirements.txt
│── README.md
```

---

## Tabla de endpoints

| Método | Endpoint                | Descripción               |
| ------ | ----------------------- | ------------------------- |
| GET    | `/`                     | Información de la API     |
| GET    | `/users`                | Lista todos los usuarios  |
| GET    | `/users/{user_id}`      | Obtiene un usuario por ID |
| GET    | `/users?role=admin`     | Filtra usuarios por rol   |
| GET    | `/users?is_active=true` | Filtra por estado activo  |
| POST   | `/users`                | Registra un nuevo usuario |

---

## Ejemplos de peticiones

### GET /users

```
GET http://127.0.0.1:8000/users
```

### GET /users/{user_id}

```
GET http://127.0.0.1:8000/users/1
```

### GET con filtro por rol

```
GET http://127.0.0.1:8000/users?role=admin
```

### GET con filtro por estado

```
GET http://127.0.0.1:8000/users?is_active=true
```

### POST /users

```json
POST http://127.0.0.1:8000/users
Content-Type: application/json

{
  "name": "Nicolas Munoz",
  "email": "nicolas@gmail.com",
  "role": "admin",
  "is_active": true
}
```

---

## Cabeceras HTTP personalizadas

Todos los endpoints retornan las cabeceras:

```
X-App-Name: device_systems
X-API-Version: 1.0
```

---

## Modelos Pydantic

### UserCreate (entrada)

| Campo     | Tipo     | Validación            |
| --------- | -------- | --------------------- |
| name      | str      | Mínimo 3 caracteres   |
| email     | EmailStr | Formato válido        |
| role      | str      | admin, support o user |
| is_active | bool     | True o False          |

### UserResponse (salida)

| Campo     | Tipo |
| --------- | ---- |
| id        | int  |
| name      | str  |
| email     | str  |
| role      | str  |
| is_active | bool |

---

## Reflexión

FastAPI permite construir APIs REST de forma rápida y segura. La integración con Pydantic garantiza que los datos siempre lleguen con el formato correcto, y la documentación automática con Swagger UI facilita las pruebas sin necesidad de herramientas externas.

## PANTALLAZOS

![lista-usuario](<image/GET(lista-usuario).png>)
![id-usuario](<image/GET(id-usuario).png>)
![crear-usuario](<image/POST(crear-usuario).png>)
![usario-creado](<image/POST(usuario-creado).png>)
![error-400](<image/POST(error-400).png>)

**GA1-220501096-01-AA1-EV08 – FastAPI Intermedio**

---

## Descripción v2

Esta versión evoluciona la API inicial implementando CRUD completo, manejo profesional de errores, Dependency Injection y documentación automática con Swagger/OpenAPI.

---

## Nuevos endpoints v2

| Método | Endpoint           | Código | Descripción                 |
| ------ | ------------------ | ------ | --------------------------- |
| PUT    | `/users/{user_id}` | 200    | Actualizar usuario completo |
| PATCH  | `/users/{user_id}` | 200    | Actualizar usuario parcial  |
| DELETE | `/users/{user_id}` | 204    | Eliminar usuario            |

---

## Códigos de estado HTTP

| Código | Significado                                     |
| ------ | ----------------------------------------------- |
| 200    | OK - operación exitosa                          |
| 201    | Created - usuario creado                        |
| 204    | No Content - usuario eliminado                  |
| 400    | Bad Request - correo duplicado o PATCH vacío    |
| 404    | Not Found - usuario no existe                   |
| 422    | Unprocessable Entity - datos inválidos Pydantic |

---

## Estructura v2

device_systems/
│── app/
│ │── main.py
│ │── routes/user_routes.py
│ │── schemas/user_schema.py
│ │── services/user_service.py
│ │── dependencies/user_dependencies.py
│ │── data/users_db.py

---

## Dependency Injection con Depends()

Se implementaron dependencias reutilizables en `dependencies/user_dependencies.py`:

- `get_user_or_404` → busca usuario por ID, lanza 404 si no existe
- `validar_email_duplicado` → valida que el correo no esté repetido
- `get_api_config` → retorna configuración general
- `verificar_api_key` → simula autenticación por cabecera

Ejemplo de uso:

```python
@router.get("/{user_id}")
def obtener_usuario(usuario=Depends(get_user_or_404)):
    return usuario
```

---

## Manejo de errores

| Error                    | Código |
| ------------------------ | ------ |
| Usuario no encontrado    | 404    |
| Correo duplicado         | 400    |
| PATCH sin datos          | 400    |
| Datos inválidos Pydantic | 422    |

---

## Capturas Swagger UI v2

![GET filtro](image/GET-filtro-role-isactive.png)
![POST crear](image/POST-crear-201.png)
![GET por ID](image/GET-id-usuario.png)
![PUT actualizar](image/PUT-actualizar-200.png)
![PATCH parcial](image/PATCH-parcial-200.png)
![DELETE 204](image/DELETE-204-respuesta.png)
![GET 404](image/GET-404-no-encontrado.png)
![PATCH 400](image/PATCH-400-vacio.png)

---

## Reflexión final

Evolucionar la API permitió entender cómo separar responsabilidades en capas. El uso de Dependency Injection evita repetir lógica y hace el código más limpio y mantenible.

## PANTALLAZOS

![GET-filtro-role-isactive](image/GET-filtro-role-isactive.png)
![image/GET-id-usuario2](image/GET-id-usuario2.png)
![image/GET-404-no-encontrado](image/GET-404-no-encontrado.png)
![image/POST-crear-formulario](image/POST-crear-formulario.png)
![image/POST-crear-201](image/POST-crear-201.png)
![image/PATCH-parcial-200](image/PATCH-parcial-200.png)
![image/PATCH-400-vacio](image/PATCH-400-vacio.png)
![image/GET-id-usuario](image/GET-id-usuario.png)
![image/DELETE-204-formulario](image/DELETE-204-formulario.png)
![image/DELETE-204-respuesta](image/DELETE-204-respuesta.png)

**GA1-220501096-01-AA1-EV09 – FastAPI con SQLAlchemy**

## Descripción v3

Esta versión reemplaza el almacenamiento en memoria por una base de datos real usando SQLAlchemy con SQLite. Los usuarios ahora se persisten en `device_systems.db`.

---

## Nuevas dependencias

```bash
pip install sqlalchemy
pip freeze > requirements.txt
```

---

## Estructura v3

device_systems/
│── app/
│ │── database/
│ │ │── connection.py
│ │── models/
│ │ │── user_model.py
│ │── schemas/
│ │ │── user_schema.py
│ │── services/
│ │ │── user_service.py
│ │── dependencies/
│ │ │── database_dependency.py
│ │── routes/
│ │ │── user_routes.py
│ │── main.py

---

## Diferencia entre modelo SQLAlchemy y schema Pydantic

|                | Modelo SQLAlchemy                       | Schema Pydantic                                |
| -------------- | --------------------------------------- | ---------------------------------------------- |
| Archivo        | `models/user_model.py`                  | `schemas/user_schema.py`                       |
| Para qué sirve | Representa la tabla en la base de datos | Valida los datos de entrada y salida de la API |
| Dónde vive     | En la base de datos                     | En las peticiones HTTP                         |
| Ejemplo        | `Column(String, nullable=False)`        | `name: str` con validadores                    |

---

## Dependencia get_db con Depends()

```python
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

Se inyecta en cada endpoint con `db: Session = Depends(get_db)` para abrir y cerrar la sesión automáticamente.

---

## Modelo SQLAlchemy User

| Campo      | Tipo     | Restricción                 |
| ---------- | -------- | --------------------------- |
| id         | Integer  | Primary Key                 |
| name       | String   | nullable=False              |
| email      | String   | unique=True, nullable=False |
| role       | String   | nullable=False              |
| is_active  | Boolean  | default=True                |
| created_at | DateTime | default=datetime.utcnow     |

---

## Capturas Swagger UI v3

![GET usuarios](image/GET-filtro-role-isactive.png)
![POST crear](image/POST-crear-201.png)
![GET por ID](image/GET-id-usuario.png)
![PUT actualizar](image/PUT-actualizar-200.png)
![PATCH parcial](image/PATCH-parcial-200.png)
![DELETE 204](image/DELETE-204-respuesta.png)
![GET 404](image/GET-404-no-encontrado.png)
![PATCH 400](image/PATCH-400-vacio.png)

---

## Reflexión final

Usar persistencia real con SQLAlchemy permite que los datos no se pierdan cuando el servidor se reinicia. El ORM facilita trabajar con la base de datos usando Python puro sin escribir SQL directamente, y la separación entre modelos SQLAlchemy y schemas Pydantic mantiene el código organizado y seguro.

## PANTALLAZOS

![EV09-POST-crear](image/EV09-POST-crear.png)
![EV09-POST-email-duplicado](image/EV09-POST-email-duplicado.png)
![GET-filtro-activo](image/EV09-GET-filtro-activo.png)
![EV09-GET-404](image/EV09-GET-404.png)
![EV09-GET-eliminado-404](image/EV09-GET-eliminado-404.png)
![EV09-DELETE-404](image/EV09-DELETE-404.png)
![EV09-GET-filtro-role](image/EV09-GET-filtro-role.png)
![EV09-GET-id](image/EV09-GET-id.png)
![EV09-GET-lista](image/EV09-GET-lista.png)
![EV09-PATCH-parcial](image/EV09-PATCH-parcial.png)
![EV09-PUT-actualizar](image/EV09-PUT-actualizar.png)

**GA1-220501096-01-AA1-EV10 – Alembic, Relaciones y Consultas Avanzadas**

---

## Descripción

Esta versión agrega persistencia relacional con tres modelos relacionados: User, Device y Loan. Se implementaron migraciones con Alembic, relaciones One-to-Many y consultas con joins y filtros avanzados.

---

## Nuevas dependencias

```bash
pip install alembic
pip freeze > requirements.txt
```

---

## Configuración de Alembic

```bash
alembic init alembic
alembic revision --autogenerate -m "create devices and loans tables"
alembic upgrade head
alembic history
```

---

## Nuevos recursos

| Recurso              | Descripción                    |
| -------------------- | ------------------------------ |
| `/devices`           | CRUD completo de dispositivos  |
| `/loans`             | Gestión de préstamos con joins |
| `/users/{id}/loans`  | Préstamos de un usuario        |
| `/loans/{id}/return` | Devolución de dispositivo      |

---

## Tabla de endpoints v4

| Método | Endpoint             | Código | Descripción             |
| ------ | -------------------- | ------ | ----------------------- |
| GET    | `/devices`           | 200    | Listar dispositivos     |
| POST   | `/devices`           | 201    | Crear dispositivo       |
| GET    | `/devices/{id}`      | 200    | Obtener por ID          |
| PUT    | `/devices/{id}`      | 200    | Actualizar completo     |
| PATCH  | `/devices/{id}`      | 200    | Actualizar parcial      |
| DELETE | `/devices/{id}`      | 204    | Eliminar                |
| GET    | `/loans`             | 200    | Listar préstamos        |
| POST   | `/loans`             | 201    | Crear préstamo          |
| GET    | `/loans/details`     | 200    | Préstamos con detalle   |
| PATCH  | `/loans/{id}/return` | 200    | Devolver dispositivo    |
| GET    | `/users/{id}/loans`  | 200    | Préstamos de un usuario |

---

## Relaciones entre modelos

User ──────── Loan ──────── Device
(1) (N) (N) (1)
un usuario muchos préstamos un dispositivo

- `User` → `loans = relationship("Loan", back_populates="user")`
- `Device` → `loans = relationship("Loan", back_populates="device")`
- `Loan` → `ForeignKey("users.id")` y `ForeignKey("devices.id")`

---

## Consultas con joins

```python
query = db.query(Loan).options(
    joinedload(Loan.user),
    joinedload(Loan.device)
).filter(Loan.status == status).all()
```

---

## Filtros avanzados disponibles

| Filtro      | Ejemplo                                  |
| ----------- | ---------------------------------------- |
| Por estado  | `GET /loans?status=active`               |
| Por email   | `GET /loans?user_email=nicolas@mail.com` |
| Por tipo    | `GET /loans?device_type=laptop`          |
| Disponibles | `GET /devices?is_available=true`         |
| Por marca   | `GET /devices?brand=lenovo`              |
| Búsqueda    | `GET /devices?search=thinkpad`           |

---

## Capturas EV10

![GET user loans](image/EV10-GET-user-loans.png)
![POST device](image/EV10-POST-device.png)
![GET devices disponibles](image/EV10-GET-devices-disponibles.png)
![GET devices tipo](image/EV10-GET-devices-tipo.png)
![POST loan](image/EV10-POST-loan.png)
![GET loans detalle](image/EV10-GET-loans.png)
![GET loans status](image/EV10-GET-loans-status.png)
![PATCH return](image/EV10-PATCH-return.png)

---

## Reflexión final

Alembic permite versionar los cambios de la base de datos de forma controlada, lo que facilita el trabajo en equipo y evita errores al evolucionar el esquema. Las relaciones entre modelos permiten construir consultas más poderosas con joins, y los filtros avanzados hacen la API mucho más flexible y útil para el frontend.

![EV10-GET-device-disponible](image/EV10-GET-device-disponible.png)
![EV10-GET-devices-disponibles](image/EV10-GET-devices-disponibles.png)
![EV10-GET-devices-tipo](image/EV10-GET-devices-tipo.png)
![EV10-GET-loans-status](image/EV10-GET-loans-status.png)
![EV10-GET-loans](image/EV10-GET-loans.png)
![EV10-GET-user-loans](image/EV10-GET-user-loans.png)
![EV10-PATCH-return](image/EV10-PATCH-return.png)
![EV10-POST-device](image/EV10-POST-device.png)
![EV10-POST-loan-404](image/EV10-POST-loan-404.png)
![EV10-POST-loan-409](image/EV10-POST-loan-409.png)
![EV10-POST-loan](image/EV10-POST-loan.png)
