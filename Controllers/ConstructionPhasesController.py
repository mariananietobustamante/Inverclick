from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from Repositories.database import get_db
from Repositories.ConstructionPhasesRepository import ConstructionPhasesRepository
from Services.IConstructionPhasesService import IConstructionPhasesService
from Services.Impl.ConstructionPhasesService import ConstructionPhasesService
from Models.construction_phases import ConstructionPhaseCreateSchema, ConstructionPhaseResponseSchema
from Services.Security.auth_dependencies import require_module
from Utils.enums import AppModule

router = APIRouter(prefix="/construction-phases", tags=["Construction Phases"])

def get_phases_service(db: Session = Depends(get_db)) -> IConstructionPhasesService:
    return ConstructionPhasesService(repository=ConstructionPhasesRepository(db))

@router.get("", response_model=list[ConstructionPhaseResponseSchema])
def get_all_phases(
    skip: int = 0, 
    limit: int = 100, 
    service: IConstructionPhasesService = Depends(get_phases_service),
    _auth=Depends(require_module(AppModule.REAL_ESTATE))
):
    return service.get_all(skip=skip, limit=limit)

@router.post("", status_code=201, response_model=ConstructionPhaseResponseSchema)
def create_phase(
    phase_in: ConstructionPhaseCreateSchema,
    service: IConstructionPhasesService = Depends(get_phases_service),
    _auth=Depends(require_module(AppModule.REAL_ESTATE))
):
    return service.create(phase_in)