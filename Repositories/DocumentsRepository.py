from sqlalchemy import select
from sqlalchemy.orm import Session

from Models.documents import DocumentDTO
from Repositories.IDocumentsRepository import IDocumentsRepository


class DocumentsRepository(IDocumentsRepository):
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, document_id: int) -> DocumentDTO | None:
        statement = select(DocumentDTO).where(DocumentDTO.id == document_id)
        return self.db.execute(statement).scalar_one_or_none()

    def list_by_user(self, user_id: int, skip: int = 0, limit: int = 100) -> list[DocumentDTO]:
        statement = (
            select(DocumentDTO)
            .where(DocumentDTO.user_id == user_id)
            .offset(skip)
            .limit(limit)
        )
        return list(self.db.execute(statement).scalars().all())

    def list_by_real_estate(self, real_estate_id: int, skip: int = 0, limit: int = 100) -> list[DocumentDTO]:
        statement = (
            select(DocumentDTO)
            .where(DocumentDTO.real_estate_id == real_estate_id)
            .offset(skip)
            .limit(limit)
        )
        return list(self.db.execute(statement).scalars().all())

    def create(self, document: DocumentDTO) -> DocumentDTO:
        self.db.add(document)
        self.db.commit()
        self.db.refresh(document)
        return document
