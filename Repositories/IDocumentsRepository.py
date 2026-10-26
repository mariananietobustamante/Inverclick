from Models.documents import DocumentDTO


class IDocumentsRepository:
    def get_by_id(self, document_id: int) -> DocumentDTO | None:
        pass

    def list_by_user(self, user_id: int, skip: int = 0, limit: int = 100) -> list[DocumentDTO]:
        pass

    def list_by_real_estate(self, real_estate_id: int, skip: int = 0, limit: int = 100) -> list[DocumentDTO]:
        pass

    def create(self, document: DocumentDTO) -> DocumentDTO:
        pass
