# Guía paso a paso — Pruebas manuales

Esta guía explica cómo probar **cada función implementada** usando Swagger UI. Sirve como complemento de las HUs documentadas en esta carpeta.

---

## 0. Preparación (hacer una sola vez)

### Paso 0.1 — Levantar la API

```bash
cd Inverclick
.\.venv\Scripts\Activate.ps1
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

### Paso 0.2 — Abrir Swagger

1. Abre el navegador en [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
2. Verifica que la API responde (debe cargar la lista de endpoints)

### Paso 0.3 — Verificar variables de entorno

Asegúrate de tener `Inverclick/.env` con al menos:

```env
DATABASE_URL=postgresql://...
JWT_SECRET_KEY=clave-de-desarrollo
JWT_EXPIRE_MINUTES=60
```

### Paso 0.4 — Crear usuario administrador de prueba

> Este usuario se usa en casi todas las pruebas de seguridad. **No requiere token.**

1. En Swagger, abre **`POST /users`**
2. Clic en **Try it out**
3. Pega este body (cambia el email si ya existe):

```json
{
  "name": "Admin",
  "last_name": "Prueba",
  "email": "admin.prueba@inverclick.com",
  "identification": "1098765432",
  "identification_type": "CC",
  "phone_number": "3001112233",
  "desired_description": "Usuario admin para pruebas",
  "user_id_role": 1
}
```

4. Clic en **Execute**
5. **Resultado esperado:** `201 Created` — anota el `id` devuelto (ej. `5`)

### Paso 0.5 — Crear credenciales de login

1. Abre **`POST /users-login`**
2. Body (reemplaza `user_id` con el id del paso anterior):
npx supabase migration new agregar_relacion_constructora
```json
{
  "user_id": 5,
  "user_password": "ClaveSegura123",
  "active": true
}
```

3. **Execute**
4. **Resultado esperado:** `201 Created`

### Paso 0.6 — Obtener token JWT

1. Abre **`POST /users-login/login`**
2. Body:

```json
{
  "email": "admin.prueba@inverclick.com",
  "user_password": "ClaveSegura123"
}
```

3. **Execute**
4. **Resultado esperado:** `200 OK` con `access_token`, `expires_in`, `role`, `modules`
5. **Copia el `access_token`** completo

### Paso 0.7 — Autorizar Swagger

1. Clic en el botón **Authorize** (candado, arriba a la derecha)
2. En el campo **Value**, pega: `Bearer <tu_access_token>`
   - Ejemplo: `Bearer eyJhbGciOiJIUzI1NiIs...`
3. Clic en **Authorize** → **Close**

A partir de aquí, los endpoints protegidos enviarán el token automáticamente.

---

## Cómo leer cada prueba

Cada sección sigue este formato:

| Campo | Significado |
|-------|-------------|
| **Endpoint** | Ruta y método HTTP en Swagger |
| **Token** | Si necesitas estar autorizado en Swagger |
| **Body** | JSON a enviar (si aplica) |
| **Esperado** | Código HTTP y qué validar en la respuesta |

---

## Índice rápido

| Sección | Qué prueba |
|---------|------------|
| [HU Seguridad V2](./hu-seguridad-v2.md#paso-a-paso-por-función) | Roles, Bcrypt, JWT, autorización |
| [HU Validaciones](./hu-validaciones-usuario.md#paso-a-paso-por-función) | Cada validador de campos de usuario |

---

## Tips

- Si recibes **401**, el token expiró o no está en Authorize → repite pasos 0.6 y 0.7.
- Si recibes **403**, el rol no tiene el módulo del endpoint → usa `user_id_role: 1` (admin con `"all"`).
- Si recibes **422**, el JSON tiene formato incorrecto (Pydantic), no es error de negocio.
- Si recibes **400** en usuarios, es una validación de negocio — lee el campo `detail`.
