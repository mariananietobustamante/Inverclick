from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from Repositories.database import get_db
from Repositories.ConstructionCompanyRepository import ConstructionCompanyRepository

from Services.IConstructionCompanyService import IConstructionCompanyService
from Services.Impl.ConstructionCompanyService import ConstructionCompanyService
from Models.construction_companies import ConstructionCompanyCreateSchema, ConstructionCompanyResponseSchema

# Importamos las dependencias de seguridad (Igual que en los otros controladores)
from Services.Security.auth_dependencies import require_module
from Utils.enums import AppModule

router = APIRouter(prefix="/construction-companies", tags=["Construction Companies"])

def get_company_service(db: Session = Depends(get_db)) -> IConstructionCompanyService:
    return ConstructionCompanyService(repository=ConstructionCompanyRepository(db))

@router.get("", response_model=list[ConstructionCompanyResponseSchema])
def get_all_companies(
    skip: int = 0, 
    limit: int = 100, 
    service: IConstructionCompanyService = Depends(get_company_service),
    _auth=Depends(require_module(AppModule.CONSTRUCTION_COMPANIES)),
):
    return service.get_all(skip=skip, limit=limit)

@router.post("", status_code=201, response_model=ConstructionCompanyResponseSchema)
def create_company(
    company: ConstructionCompanyCreateSchema, 
    service: IConstructionCompanyService = Depends(get_company_service),
    _auth=Depends(require_module(AppModule.CONSTRUCTION_COMPANIES)),
):
    return service.create(company)