# database.py
import os

from dotenv import load_dotenv
from fastapi import HTTPException, status
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError, SQLAlchemyError
from sqlalchemy.orm import DeclarativeBase, sessionmaker

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(
    DATABASE_URL,
    echo=True,
    connect_args={"options": "-c search_path=public"} if DATABASE_URL and DATABASE_URL.startswith("postgresql") else {},
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


def _register_models() -> None:
    import Models  # noqa: F401


_register_models()


def get_db():
    db = SessionLocal()
    try:
        from Repositories.seed_reference_data import (
            ensure_admin_all_modules,
            ensure_constructora_role_modules,
            ensure_default_roles,
            ensure_id_types,
            ensure_sso_default_role,
        )

        ensure_id_types(db)
        ensure_default_roles(db)
        ensure_sso_default_role(db)
        ensure_constructora_role_modules(db)
        ensure_admin_all_modules(db)
        yield db
    except OperationalError as exc:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=(
                "No se pudo conectar a PostgreSQL. "
                "Inicia Supabase local (`npx supabase start`) o Docker, "
                "y verifica DATABASE_URL en el archivo .env."
            ),
        ) from exc
    except SQLAlchemyError as exc:
        db.rollback()
        orig = getattr(exc, "orig", None)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(orig or exc),
        ) from exc
    finally:
        db.close()


def verify_db_connection_and_schema():
    from sqlalchemy import inspect, text

    from Models.users import UserDTO

    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
            print("DATABASE: Conexión establecida con éxito.")

            inspector = inspect(engine)
            table_name = UserDTO.__tablename__
            schema = UserDTO.__table__.schema

            if not inspector.has_table(table_name, schema=schema):
                print(f"DATABASE ERROR: La tabla '{table_name}' no existe en la base de datos.")
                return False

            db_columns = {col["name"] for col in inspector.get_columns(table_name, schema=schema)}
            required_columns = {"id", "name", "surname", "email", "id_number", "id_type_id", "role_id"}

            missing = required_columns - db_columns
            if missing:
                print(f"DATABASE ERROR: Faltan columnas en '{table_name}': {', '.join(sorted(missing))}")
                return False

            print(f"DATABASE: Estructura de la tabla '{table_name}' verificada y correcta.")
            return True

    except Exception as e:
        print(f"DATABASE ERROR: Fallo al verificar la conexión o estructura: {e}")
        return False
