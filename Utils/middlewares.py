import os
import jwt
from datetime import datetime, timezone
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

from Repositories.database import SessionLocal # Asegúrate de importar tu generador de sesiones
from Models.audit_logs import AuditLogDTO

class AuditLogMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # 1. Dejar que la petición siga su curso normal y obtener la respuesta
        response = await call_next(request)

        # 2. CA4: Filtrar acciones críticas (Creación=POST, Edición=PUT, Eliminación=DELETE)
        if request.method in ["POST", "PUT", "DELETE"]:
            path = request.url.path
            
            # 3. CA4: Filtrar módulos específicos (Constructoras, Propiedades, Leads, Ventas)
            target_modules = ["/construction-companies", "/real-estate", "/leads", "/sales"]
            if any(module in path for module in target_modules):
                self._save_log(request, path)

        return response

    def _save_log(self, request: Request, path: str):
        user_id = None
        auth_header = request.headers.get("Authorization")
        
        # DEBUG: Ver si Swagger realmente nos está enviando el token
        print(f"--- MIDDLEWARE DEBUG ---")
        print(f"Token recibido en Header: {'Sí' if auth_header else 'No'}")

        db = SessionLocal()
        try:
            if auth_header and auth_header.startswith("Bearer "):
                token = auth_header.split(" ")[1]
                try:
                    payload = jwt.decode(token, options={"verify_signature": False})
                    print(f"Contenido del Token: {payload}")
                    
                    # 1. Intentar sacar 'user_id' o 'id' directo
                    user_id = payload.get("user_id") or payload.get("id")
                    
                    # 2. Revisar si viene en 'sub'
                    if not user_id and payload.get("sub"):
                        sub_val = str(payload.get("sub"))
                        if sub_val.isdigit():
                            # Si el sub es un número (ej. "2"), es el ID directamente
                            user_id = int(sub_val)
                        else:
                            # Si no es número, asumimos que es el email y buscamos el ID
                            from Models.users import UserDTO
                            user = db.query(UserDTO).filter(UserDTO.email == sub_val).first()
                            if user:
                                user_id = user.id
                except Exception as e:
                    print(f"Error decodificando token: {e}")

            print(f"ID Usuario a guardar: {user_id}")
            print(f"------------------------")

            # Guardar el log
            log_entry = AuditLogDTO(
                user_id=user_id,
                action=request.method,
                route=path,
                created_at=datetime.now(timezone.utc)
            )
            db.add(log_entry)
            db.commit()
        except Exception as e:
            db.rollback()
            print(f"Error en BD Middleware: {e}")
        finally:
            db.close()