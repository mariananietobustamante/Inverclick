from fastapi import HTTPException


class DocumentHttpResponses:
    @staticmethod
    def error_invalid_format(allowed: list[str]) -> HTTPException:
        return HTTPException(
            status_code=400,
            detail=f"Formato no permitido para este rol. Extensiones válidas: {', '.join(allowed)}",
        )

    @staticmethod
    def error_empty_file() -> HTTPException:
        return HTTPException(status_code=400, detail="El archivo está vacío o no se recibió contenido")

    @staticmethod
    def error_file_too_large(max_mb: int) -> HTTPException:
        return HTTPException(
            status_code=400,
            detail=f"El archivo supera el tamaño máximo permitido ({max_mb} MB)",
        )

    @staticmethod
    def error_property_not_found() -> HTTPException:
        return HTTPException(status_code=404, detail="Propiedad no encontrada")

    @staticmethod
    def error_document_not_found() -> HTTPException:
        return HTTPException(status_code=404, detail="Documento no encontrado")

    @staticmethod
    def error_file_missing() -> HTTPException:
        return HTTPException(status_code=404, detail="El archivo no está disponible en el almacenamiento externo")

    @staticmethod
    def error_forbidden_view() -> HTTPException:
        return HTTPException(
            status_code=403,
            detail="El rol cliente solo puede visualizar documentos en formato PDF",
        )

    @staticmethod
    def error_forbidden_access() -> HTTPException:
        return HTTPException(status_code=403, detail="No tiene permiso para acceder a este documento")
