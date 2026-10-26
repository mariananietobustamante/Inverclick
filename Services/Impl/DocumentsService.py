from datetime import datetime, timezone
from pathlib import Path

from Models.documents import DocumentDTO, DocumentResponseSchema
from Repositories.IDocumentsRepository import IDocumentsRepository
from Repositories.RealEstateRepository import RealEstateRepository
from Repositories.UsuariosRepository import UsersRepository
from Utils.HttpResponses.documentHttpResponses import DocumentHttpResponses
from Utils.enums import INTERNAL_DOCUMENT_ROLE_NAMES
from Utils.external_storage import save_document_bytes

MAX_FILE_SIZE_BYTES = 20 * 1024 * 1024

INTERNAL_EXTENSIONS = {".pdf", ".png", ".jpg", ".jpeg", ".csv", ".xlsx"}
CLIENT_EXTENSIONS = {".pdf"}

EXTENSION_MIME = {
    ".pdf": "application/pdf",
    ".png": "image/png",
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".csv": "text/csv",
    ".xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
}

ALLOWED_MIME_BY_EXTENSION = {
    ".pdf": {"application/pdf"},
    ".png": {"image/png"},
    ".jpg": {"image/jpeg"},
    ".jpeg": {"image/jpeg"},
    ".csv": {"text/csv", "application/csv", "application/vnd.ms-excel"},
    ".xlsx": {
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        "application/vnd.ms-excel",
        "application/octet-stream",
    },
}


class DocumentsService:
    def __init__(
        self,
        repository: IDocumentsRepository,
        users_repository: UsersRepository,
        real_estate_repository: RealEstateRepository,
        http_responses: DocumentHttpResponses | None = None,
    ):
        self.repository = repository
        self.users_repository = users_repository
        self.real_estate_repository = real_estate_repository
        self.http_responses = http_responses or DocumentHttpResponses()

    def _is_internal_role(self, role_name: str | None) -> bool:
        if not role_name:
            return False
        return role_name.casefold() in INTERNAL_DOCUMENT_ROLE_NAMES

    def _allowed_extensions(self, role_name: str | None) -> set[str]:
        if self._is_internal_role(role_name):
            return INTERNAL_EXTENSIONS
        return CLIENT_EXTENSIONS

    def _validate_format(self, filename: str | None, content_type: str | None, role_name: str | None) -> tuple[str, str]:
        if not filename:
            raise self.http_responses.error_invalid_format(sorted(self._allowed_extensions(role_name)))

        extension = Path(filename).suffix.lower()
        allowed = self._allowed_extensions(role_name)
        if extension not in allowed:
            raise self.http_responses.error_invalid_format(sorted(allowed))

        mime = (content_type or "").split(";")[0].strip().lower()
        accepted_mimes = ALLOWED_MIME_BY_EXTENSION[extension]
        if mime and mime not in accepted_mimes:
            raise self.http_responses.error_invalid_format(sorted(allowed))

        document_type = mime if mime in accepted_mimes else EXTENSION_MIME[extension]
        return extension, document_type

    def _to_response(self, document: DocumentDTO) -> DocumentResponseSchema:
        return DocumentResponseSchema.model_validate(document)

    def _filter_for_viewer(self, documents: list[DocumentDTO], role_name: str | None) -> list[DocumentDTO]:
        if self._is_internal_role(role_name):
            return documents
        return [item for item in documents if item.document_type == "application/pdf"]

    def _assert_can_access(self, document: DocumentDTO, user_id: int, role_name: str | None) -> None:
        if document.user_id == user_id:
            return
        if self._is_internal_role(role_name):
            return
        raise self.http_responses.error_forbidden_access()

    def _assert_can_view_type(self, document: DocumentDTO, role_name: str | None) -> None:
        if self._is_internal_role(role_name):
            return
        if document.document_type != "application/pdf":
            raise self.http_responses.error_forbidden_view()

    def upload(
        self,
        *,
        user_id: int,
        role_name: str | None,
        filename: str | None,
        content_type: str | None,
        content: bytes,
        real_estate_id: int | None,
        associate_to_profile: bool,
    ) -> DocumentResponseSchema:
        if not content:
            raise self.http_responses.error_empty_file()
        if len(content) > MAX_FILE_SIZE_BYTES:
            raise self.http_responses.error_file_too_large(MAX_FILE_SIZE_BYTES // (1024 * 1024))

        _, document_type = self._validate_format(filename, content_type, role_name)

        if real_estate_id is not None and self.real_estate_repository.get_by_id(real_estate_id) is None:
            raise self.http_responses.error_property_not_found()

        stored_path = save_document_bytes(user_id, filename or "documento", content)
        document = DocumentDTO(
            user_id=user_id,
            name=Path(filename or "documento").name,
            document_type=document_type,
            location=str(stored_path),
            path=str(stored_path),
            real_estate_id=real_estate_id,
            created_at=datetime.now(timezone.utc),
        )
        created = self.repository.create(document)

        if associate_to_profile:
            self.users_repository.update(user_id, {"document_id": created.id})

        return self._to_response(created)

    def list_own(self, user_id: int, role_name: str | None, skip: int = 0, limit: int = 100) -> list[DocumentResponseSchema]:
        documents = self.repository.list_by_user(user_id, skip=skip, limit=limit)
        return [self._to_response(item) for item in self._filter_for_viewer(documents, role_name)]

    def list_by_property(
        self,
        *,
        user_id: int,
        role_name: str | None,
        real_estate_id: int,
        skip: int = 0,
        limit: int = 100,
    ) -> list[DocumentResponseSchema]:
        if self.real_estate_repository.get_by_id(real_estate_id) is None:
            raise self.http_responses.error_property_not_found()
        documents = self.repository.list_by_real_estate(real_estate_id, skip=skip, limit=limit)
        visible = self._filter_for_viewer(documents, role_name)
        if not self._is_internal_role(role_name):
            visible = [item for item in visible if item.user_id == user_id]
        return [self._to_response(item) for item in visible]

    def get_metadata(self, document_id: int, user_id: int, role_name: str | None) -> DocumentResponseSchema:
        document = self.repository.get_by_id(document_id)
        if document is None:
            raise self.http_responses.error_document_not_found()
        self._assert_can_access(document, user_id, role_name)
        self._assert_can_view_type(document, role_name)
        return self._to_response(document)

    def get_file_for_download(self, document_id: int, user_id: int, role_name: str | None) -> tuple[str, str, str]:
        document = self.repository.get_by_id(document_id)
        if document is None:
            raise self.http_responses.error_document_not_found()
        self._assert_can_access(document, user_id, role_name)
        self._assert_can_view_type(document, role_name)
        path = Path(document.location)
        if not path.is_file():
            raise self.http_responses.error_file_missing()
        return str(path), document.document_type, document.name
