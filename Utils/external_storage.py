import os
import re
import uuid
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

_DEFAULT_STORAGE_DIR = Path.home() / "inverclick-external-storage"
_UNSAFE_FILENAME = re.compile(r"[^A-Za-z0-9._-]+")


def get_documents_storage_root() -> Path:
    """Carpeta aislada del código fuente. Configurable con DOCUMENTS_STORAGE_PATH."""
    configured = os.getenv("DOCUMENTS_STORAGE_PATH")
    root = Path(configured).expanduser() if configured else _DEFAULT_STORAGE_DIR
    root.mkdir(parents=True, exist_ok=True)
    return root.resolve()


def sanitize_filename(filename: str) -> str:
    name = Path(filename).name
    cleaned = _UNSAFE_FILENAME.sub("_", name).strip("._")
    return cleaned or "documento"


def save_document_bytes(user_id: int, original_filename: str, content: bytes) -> Path:
    root = get_documents_storage_root()
    user_dir = root / str(user_id)
    user_dir.mkdir(parents=True, exist_ok=True)
    stored_name = f"{uuid.uuid4().hex}_{sanitize_filename(original_filename)}"
    destination = user_dir / stored_name
    destination.write_bytes(content)
    return destination
