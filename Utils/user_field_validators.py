import re
from typing import Any, Optional

from Utils.enums import IdentificationTypeEnum

TIPOS_DOCUMENTO_VALIDOS: set[str] = {item.value for item in IdentificationTypeEnum}


def validar_tipo_documento(tipo_documento: str) -> tuple[bool, Optional[str]]:
    """
    Valida que el tipo de documento esté dentro de los permitidos.
    """
    if not tipo_documento:
        return False, "El tipo de documento no puede estar vacío."

    tipo_normalizado = tipo_documento.strip().upper()

    if tipo_normalizado not in TIPOS_DOCUMENTO_VALIDOS:
        opciones = ", ".join(sorted(TIPOS_DOCUMENTO_VALIDOS))
        return (
            False,
            f"'{tipo_normalizado}' no es un tipo de documento válido. Opciones válidas: {opciones}",
        )

    return True, None


def validar_identificacion(
    identificacion: str,
    longitud_min: int = 6,
    longitud_max: int = 15,
) -> tuple[bool, Optional[str]]:
    if not identificacion:
        return False, "La identificación no puede estar vacía."

    identificacion = identificacion.strip()

    if not identificacion.isdigit():
        return False, "La identificación solo debe contener números."

    if not (longitud_min <= len(identificacion) <= longitud_max):
        return (
            False,
            f"La identificación debe tener entre {longitud_min} y {longitud_max} dígitos.",
        )

    return True, None


def validar_correo(correo: str) -> tuple[bool, Optional[str]]:
    """
    Valida que el correo tenga un '@' y un '.' después del @.
    """
    if not correo:
        return False, "El correo no puede estar vacío."

    correo = correo.strip()
    patron = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"

    if not re.match(patron, correo):
        return False, "El correo no tiene un formato válido (ejemplo: usuario@dominio.com)."

    return True, None


def validar_nombre(
    nombre: str,
    longitud_min: int = 2,
    longitud_max: int = 50,
) -> tuple[bool, Optional[str]]:
    if not nombre:
        return False, "El nombre no puede estar vacío."

    nombre = nombre.strip()
    patron = r"^[A-Za-zÁÉÍÓÚáéíóúÑñ\s]+$"

    if not re.match(patron, nombre):
        return False, "El nombre solo debe contener letras y espacios."

    if not (longitud_min <= len(nombre) <= longitud_max):
        return (
            False,
            f"El nombre debe tener entre {longitud_min} y {longitud_max} caracteres.",
        )

    return True, None


def validar_celular(
    celular: str,
    longitud_min: int = 7,
    longitud_max: int = 10,
) -> tuple[bool, Optional[str]]:
    """
    Valida que el número de celular solo contenga números y tenga longitud permitida.
    """
    if not celular:
        return False, "El celular no puede estar vacío."

    celular = celular.strip()

    if not celular.isdigit():
        return False, "El celular solo debe contener números."

    if not (longitud_min <= len(celular) <= longitud_max):
        return (
            False,
            f"El celular debe tener entre {longitud_min} y {longitud_max} dígitos.",
        )

    return True, None


def validar_usuario(
    nombre: str,
    tipo_documento: str,
    identificacion: str,
    correo: str,
    celular: str,
) -> tuple[bool, Optional[str]]:
    """
    Ejecuta todas las validaciones de negocio para un usuario.
    """
    validaciones = [
        validar_nombre(nombre),
        validar_tipo_documento(tipo_documento),
        validar_identificacion(identificacion),
        validar_correo(correo),
        validar_celular(celular),
    ]

    for es_valido, mensaje in validaciones:
        if not es_valido:
            return False, mensaje

    return True, None


def _first_error(validaciones: list[tuple[bool, Optional[str]]]) -> Optional[str]:
    for es_valido, mensaje in validaciones:
        if not es_valido:
            return mensaje
    return None


def validar_campos_usuario(data: dict[str, Any], *, is_create: bool = False) -> Optional[str]:
    """
    Valida campos del API (name, last_name, identification_type, etc.)
    y devuelve el primer mensaje de error encontrado.
    """
    if is_create:
        es_valido, mensaje = validar_usuario(
            nombre=str(data.get("name", "")),
            tipo_documento=str(data.get("identification_type", "")),
            identificacion=str(data.get("identification", "")),
            correo=str(data.get("email", "")),
            celular=str(data.get("phone_number", "")),
        )
        if not es_valido:
            return mensaje

        es_valido, mensaje = validar_nombre(str(data.get("last_name", "")))
        if not es_valido:
            return f"Apellido: {mensaje}"
        return None

    validaciones: list[tuple[bool, Optional[str]]] = []

    if "name" in data and data["name"] is not None:
        validaciones.append(validar_nombre(str(data["name"])))
    if "last_name" in data and data["last_name"] is not None:
        validaciones.append(validar_nombre(str(data["last_name"])))
    if "identification_type" in data and data["identification_type"] is not None:
        validaciones.append(validar_tipo_documento(str(data["identification_type"])))
    if "identification" in data and data["identification"] is not None:
        validaciones.append(validar_identificacion(str(data["identification"])))
    if "email" in data and data["email"] is not None:
        validaciones.append(validar_correo(str(data["email"])))
    if "phone_number" in data and data["phone_number"] is not None:
        validaciones.append(validar_celular(str(data["phone_number"])))

    return _first_error(validaciones)
