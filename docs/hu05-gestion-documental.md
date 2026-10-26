# HU05 — Gestión documental y almacenamiento externo

Historia de usuario: subir, asociar y visualizar documentos de respaldo del perfil y de las propiedades, con formatos controlados por rol y archivos fuera del directorio del código fuente.

Complementa el arranque general del [`README`](../README). Esta guía asume que la API ya corre en `http://127.0.0.1:8000` y que tienes un token en Swagger (Authorize / BearerAuth). Tras cambiar módulos de rol, vuelve a hacer login para que el JWT incluya `documents`.

---

## Criterios cubiertos

| Criterio | Qué hace la API |
|----------|-----------------|
| CA1 | Admin, constructora y ventas pueden subir PDF, PNG, JPG, CSV y XLSX. El rol cliente solo PDF; cualquier otro formato se rechaza con `400`. Al visualizar, el cliente tampoco ve ni descarga formatos distintos de PDF. |
| CA2 | Los binarios se guardan en una carpeta aislada (`DOCUMENTS_STORAGE_PATH` o, por defecto, `~/inverclick-external-storage`). En Postgres solo queda la ruta (`location`). |
| CA3 | Tabla `documents`: `id`, `user_id` (quién subió), `name`, `document_type` (MIME), `location`. `real_estate_id` es opcional para asociar a una propiedad. |
| CA4 | Columna `users.document_id` (FK a `documents`) para vincular un documento de perfil. Se llena con `associate_to_profile=true` en la carga. |
| CA5 | Validación de extensión y MIME en `DocumentsService`. El controlador solo recibe HTTP y delega. |

---

## Datos que debes tener

1. Migración `supabase/migrations/20261026120000_hu05_gestion_documental.sql` aplicada (`npx supabase db push`).
2. Dependencia `python-multipart` (`pip install -r requirements.txt`).
3. Token de **admin** (módulo `documents` se agrega al rol admin al arrancar la API).
4. Un usuario **cliente** con login. Tras el seed, el rol `cliente` incluye el módulo `documents`.
5. (Opcional) Rol **ventas** (se crea si no existe) y una propiedad (`POST /real-estate`) para asociar archivos.

---

## Paso a paso de prueba

### 1. Carga interna (admin): PNG o PDF

**Endpoint:** `POST /documents` (multipart)  
**Token:** admin

Campos de formulario:

- `file`: un `.png` o `.pdf`
- `associate_to_profile`: `true` (opcional)
- `real_estate_id`: vacío, o el id de una propiedad existente

**Esperado:** `201` con `id`, `user_id`, `name`, `document_type`, `location` (ruta externa, no dentro del repo). `GET /users/{id}` debe mostrar `document_id` si asociaste al perfil.

### 2. Carga interna: CSV / XLSX

Con el mismo token admin, sube un `.csv` o `.xlsx`.

**Esperado:** `201`.

### 3. Cliente: solo PDF

Autoriza con token de un usuario rol `cliente`.

- `POST /documents` con un PDF → `201`.
- `POST /documents` con PNG, JPG, CSV o XLSX → `400` (`Formato no permitido para este rol`).

`GET /documents` del cliente solo lista PDFs. `GET /documents/{id}/file` de un PDF propio descarga el archivo.

### 4. Asociación a propiedad

Con token admin o ventas, `POST /documents` con `real_estate_id` de una propiedad existente.

**Esperado:** `201` y `GET /documents/property/{real_estate_id}` incluye ese documento.

Un `real_estate_id` inexistente → `404`.

### 5. Almacenamiento externo

Abre la carpeta de `DOCUMENTS_STORAGE_PATH` (o `~/inverclick-external-storage`). Debe existir el archivo físico. No debe crearse nada bajo `Controllers/`, `Services/` ni el resto del código fuente.

---

## Endpoints

| Método | Ruta | Descripción |
|--------|------|-------------|
| POST | `/documents` | Subir archivo (multipart) |
| GET | `/documents` | Listar documentos del usuario autenticado |
| GET | `/documents/property/{real_estate_id}` | Listar documentos de una propiedad |
| GET | `/documents/{id}` | Metadatos |
| GET | `/documents/{id}/file` | Descargar / visualizar el archivo |

| Formulario POST | Tipo | Notas |
|-----------------|------|--------|
| `file` | archivo | Obligatorio |
| `real_estate_id` | texto/número | Opcional; asocia a propiedad |
| `associate_to_profile` | bool | Si `true`, actualiza `users.document_id` |

---

## Formatos por rol

| Rol | Extensiones |
|-----|-------------|
| `admin`, `constructora`, `ventas` | `.pdf`, `.png`, `.jpg` / `.jpeg`, `.csv`, `.xlsx` |
| `cliente` (y el resto de roles no internos) | `.pdf` |

---

## Archivos clave

| Capa | Archivo |
|------|---------|
| Migración | `supabase/migrations/20261026120000_hu05_gestion_documental.sql` |
| Controller | `Controllers/DocumentsController.py` |
| Service | `Services/Impl/DocumentsService.py` |
| Repository | `Repositories/DocumentsRepository.py` |
| Storage | `Utils/external_storage.py` |
