from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from Models.auth import AuthContext
from Models.documents import DocumentResponseSchema
from Repositories.DocumentsRepository import DocumentsRepository
from Repositories.RealEstateRepository import RealEstateRepository
from Repositories.UsuariosRepository import UsersRepository
from Repositories.database import get_db
from Services.IDocumentsService import IDocumentsService
from Services.Impl.DocumentsService import DocumentsService
from Services.Security.auth_dependencies import require_module
from Utils.HttpResponses.documentHttpResponses import DocumentHttpResponses
from Utils.enums import AppModule

router = APIRouter(prefix="/documents", tags=["Documents"])


def get_documents_service(db: Session = Depends(get_db)) -> IDocumentsService:
    return DocumentsService(
        repository=DocumentsRepository(db),
        users_repository=UsersRepository(db),
        real_estate_repository=RealEstateRepository(db),
        http_responses=DocumentHttpResponses(),
    )


def _parse_optional_int(value: str | None) -> int | None:
    if value is None or value.strip() == "":
        return None
    try:
        return int(value)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail="real_estate_id debe ser un entero") from exc


@router.post("", status_code=201, response_model=DocumentResponseSchema)
async def upload_document(
    file: UploadFile = File(...),
    real_estate_id: str | None = Form(default=None),
    associate_to_profile: bool = Form(default=False),
    service: IDocumentsService = Depends(get_documents_service),
    auth_context: AuthContext = Depends(require_module(AppModule.DOCUMENTS)),
):
    content = await file.read()
    return service.upload(
        user_id=auth_context.user_id,
        role_name=auth_context.role_name,
        filename=file.filename,
        content_type=file.content_type,
        content=content,
        real_estate_id=_parse_optional_int(real_estate_id),
        associate_to_profile=associate_to_profile,
    )


@router.get("", response_model=list[DocumentResponseSchema])
def list_own_documents(
    skip: int = 0,
    limit: int = 100,
    service: IDocumentsService = Depends(get_documents_service),
    auth_context: AuthContext = Depends(require_module(AppModule.DOCUMENTS)),
):
    return service.list_own(auth_context.user_id, auth_context.role_name, skip=skip, limit=limit)


@router.get("/property/{real_estate_id}", response_model=list[DocumentResponseSchema])
def list_property_documents(
    real_estate_id: int,
    skip: int = 0,
    limit: int = 100,
    service: IDocumentsService = Depends(get_documents_service),
    auth_context: AuthContext = Depends(require_module(AppModule.DOCUMENTS)),
):
    return service.list_by_property(
        user_id=auth_context.user_id,
        role_name=auth_context.role_name,
        real_estate_id=real_estate_id,
        skip=skip,
        limit=limit,
    )


@router.get("/{document_id}", response_model=DocumentResponseSchema)
def get_document(
    document_id: int,
    service: IDocumentsService = Depends(get_documents_service),
    auth_context: AuthContext = Depends(require_module(AppModule.DOCUMENTS)),
):
    return service.get_metadata(document_id, auth_context.user_id, auth_context.role_name)


@router.get("/{document_id}/file")
def download_document(
    document_id: int,
    service: IDocumentsService = Depends(get_documents_service),
    auth_context: AuthContext = Depends(require_module(AppModule.DOCUMENTS)),
):
    path, media_type, filename = service.get_file_for_download(
        document_id, auth_context.user_id, auth_context.role_name
    )
    return FileResponse(path=path, media_type=media_type, filename=filename)
