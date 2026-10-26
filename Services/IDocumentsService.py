from Models.documents import DocumentResponseSchema


class IDocumentsService:
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
        pass

    def list_own(self, user_id: int, role_name: str | None, skip: int = 0, limit: int = 100) -> list[DocumentResponseSchema]:
        pass

    def list_by_property(
        self,
        *,
        user_id: int,
        role_name: str | None,
        real_estate_id: int,
        skip: int = 0,
        limit: int = 100,
    ) -> list[DocumentResponseSchema]:
        pass

    def get_metadata(self, document_id: int, user_id: int, role_name: str | None) -> DocumentResponseSchema:
        pass

    def get_file_for_download(
        self, document_id: int, user_id: int, role_name: str | None
    ) -> tuple[str, str, str]:
        pass
