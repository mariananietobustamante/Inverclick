from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from Models.auth import AuthContext
from Models.leads import LeadCreateSchema, LeadResponseSchema
from Repositories.LeadsRepository import LeadsRepository
from Repositories.UsuariosRepository import UsersRepository
from Repositories.database import get_db
from Services.ILeadsService import ILeadsService
from Services.Impl.LeadsService import LeadsService
from Services.Security.auth_dependencies import require_module
from Utils.enums import AppModule

router = APIRouter(prefix="/leads", tags=["Leads"])


def get_leads_service(db: Session = Depends(get_db)) -> ILeadsService:
    return LeadsService(
        repository=LeadsRepository(db),
        users_repository=UsersRepository(db),
    )


@router.post("", status_code=201, response_model=LeadResponseSchema)
def create_lead(
    lead_in: LeadCreateSchema,
    service: ILeadsService = Depends(get_leads_service),
    _auth: AuthContext = Depends(require_module(AppModule.LEADS)),
):
    return service.create(lead_in)


@router.get("", response_model=list[LeadResponseSchema])
def get_leads(
    skip: int = 0,
    limit: int = 100,
    service: ILeadsService = Depends(get_leads_service),
    _auth: AuthContext = Depends(require_module(AppModule.LEADS)),
):
    return service.get_all(skip, limit)
