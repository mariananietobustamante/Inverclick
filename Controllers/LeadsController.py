from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from Repositories.database import get_db
from Repositories.LeadsRepository import LeadsRepository
from Repositories.UsuariosRepository import UsersRepository
from Services.Impl.LeadsService import LeadsService
from Services.ILeadsService import ILeadsService  # <-- Nueva importación de la interfaz
from Models.leads import LeadCreateSchema, LeadResponseSchema

router = APIRouter(prefix="/leads", tags=["Leads"])

def get_leads_service(db: Session = Depends(get_db)) -> ILeadsService:
    return LeadsService(
        repository=LeadsRepository(db),
        users_repository=UsersRepository(db) 
    )

@router.post("", status_code=201, response_model=LeadResponseSchema)
def create_lead(lead_in: LeadCreateSchema, service: ILeadsService = Depends(get_leads_service)):
    return service.create(lead_in)

@router.get("", response_model=list[LeadResponseSchema])
def get_leads(skip: int = 0, limit: int = 100, service: ILeadsService = Depends(get_leads_service)):
    return service.get_all(skip, limit)