# HU03 — Constructoras, propiedades, leads, ventas y auditoría

Historia de usuario: registrar constructoras aliadas (con usuarios y permisos), gestionar el catálogo de propiedades y convertir leads en ventas trazables, con log de acciones críticas.

Complementa el arranque general del [`README`](../README). Esta guía asume que la API ya corre en `http://127.0.0.1:8000` y que tienes un token **admin** en Swagger (Authorize / BearerAuth).

---

## Criterios cubiertos

| Criterio | Qué hace la API |
|----------|-----------------|
| CA1 | Tabla `construction_companies`, rol `constructora`, usuarios con `construction_company_id`. Un usuario constructora solo ve su empresa, sus propiedades y sus ventas. |
| CA2 | Nombre y dirección únicos; `cost` obligatorio; FK a constructora. |
| CA3 | Venta con comprador (`user_id`), agente autenticado (`agent_id`), `lead_id` y `real_estate_id`. Bloquea venta duplicada y propiedad inexistente. El catálogo no lista lotes ya vendidos. |
| CA4 | Middleware registra creación (POST) en constructoras, propiedades, leads y ventas: usuario, fecha, ruta y resumen (`Creación`). Tabla `audit_logs`. |
| CA5 | Validaciones en Services; acceso a Postgres solo desde Repositories. |

No hay PUT/DELETE de constructoras, propiedades ni leads: el log de **edición/eliminación** queda listo si se agregan esos métodos después.

---

## Datos que debes tener

1. Rol **admin** (id típico `1` si el seed corrió sobre `user_roles` vacío).
2. Rol **constructora**. `GET /users-role` (con token admin) y anota su `id` (no es el `3` de forma fija).
3. Migración `supabase/migrations/20260928120000_hu03_ventas_auditoria.sql` aplicada.

---

## Paso a paso de prueba

### 1. Crear constructora (admin)

**Endpoint:** `POST /construction-companies`  
**Token:** sí (módulo `construction-companies`)

```json
{
  "name": "Constructora Andes",
  "rating": 4.5
}
```

**Esperado:** `201` con `id` (ej. `1`). Un segundo POST con el mismo `name` debe devolver `400`.

### 2. Crear usuario constructora ligado a esa empresa

**Endpoint:** `POST /users` (público)

Sustituye `user_id_role` por el id del rol `constructora` y `construction_company_id` por el id del paso 1.

```json
{
  "name": "Laura",
  "last_name": "Gomez",
  "email": "laura.constructora@inverclick.com",
  "identification": "1122334455",
  "identification_type": "CC",
  "phone_number": "3002223344",
  "desired_description": "Usuario de constructora aliada",
  "user_id_role": 5,
  "construction_company_id": 1
}
```

**Esperado:** `201` y la respuesta incluye `construction_company_id`. Un `construction_company_id` inexistente debe devolver `404`.

Crea login (`POST /users-login`) y token (`POST /users-login/login`) para este usuario. Guarda ese token aparte del admin.

### 3. Aislamiento (token constructora)

Autoriza Swagger con el token de Laura.

- `GET /construction-companies` → solo su empresa.
- `GET /real-estate` → vacío o solo propiedades de su empresa.
- `GET /leads` → `403` (el rol constructora no tiene módulo `leads`).

Vuelve a autorizar con **admin**.

### 4. Registrar propiedad (admin)

**Endpoint:** `POST /real-estate`

```json
{
  "name": "Torre Norte 101",
  "cost": 350000000,
  "address": "Calle 10 # 20-30",
  "stock": 1,
  "construction_company_id": 1
}
```

**Esperado:** `201`. Repetir el mismo `name` o la misma `address` → `400`. Omitir `construction_company_id` como admin → `400`.

Con token constructora, el backend ignora un `construction_company_id` ajeno y asigna el de su usuario.

### 5. Lead de un comprador (admin)

Crea un usuario comprador (`POST /users`, rol `cliente` o `Usuario`) y anota su `id` (ej. `10`).

**Endpoint:** `POST /leads`  
**Token:** admin (módulo `leads`)

```json
{
  "user_id": 10,
  "state": "Nuevo",
  "description": "Interesado en Torre Norte 101"
}
```

**Esperado:** `201` con `id` del lead (ej. `1`). Sin token → `401`.

### 6. Registrar venta (admin)

**Endpoint:** `POST /sales`

```json
{
  "user_id": 10,
  "lead_id": 1,
  "real_estate_id": 1
}
```

**Esperado:** `201` con `agent_id` igual al usuario del token, más `lead_id` y `real_estate_id`.

Casos que deben fallar:

| Body / situación | Esperado |
|------------------|----------|
| `real_estate_id` inexistente | `404` no listada |
| Misma propiedad otra vez | `400` ya vendida |
| `lead_id` inexistente | `404` |
| `user_id` distinto al del lead | `400` |

Tras una venta exitosa, `GET /real-estate` **no** debe devolver esa propiedad (ya no está en el catálogo disponible). `GET /sales` sí la muestra.

Con token constructora, `GET /sales` solo incluye ventas de propiedades de su empresa.

### 7. Auditoría

Tras los POST anteriores, en Postgres:

```sql
SELECT id, user_id, action, route, created_at
FROM audit_logs
ORDER BY id DESC
LIMIT 20;
```

Deben aparecer filas con `action = 'Creación'` y `route` en `/construction-companies`, `/real-estate`, `/leads` o `/sales`, con `user_id` del token cuando el JWT era válido.

---

## Archivos principales

| Pieza | Ruta |
|-------|------|
| Aislamiento por nombre de rol | `Utils/role_access.py` |
| Constructoras | `Services/Impl/ConstructionCompanyService.py` |
| Propiedades | `Services/Impl/RealEstateService.py` |
| Ventas | `Services/Impl/PropertySoldService.py` |
| Logs | `Utils/middlewares.py`, `Repositories/AuditLogRepository.py` |
| Migración | `supabase/migrations/20260928120000_hu03_ventas_auditoria.sql` |
