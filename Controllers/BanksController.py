from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from Repositories.database import get_db
from Repositories.BanksRepository import BanksRepository
from Services.Impl.BanksService import BanksService
from Services.IBanksService import IBanksService 
from Models.banks import BankCreateSchema, BankResponseSchema

router = APIRouter(prefix="/banks", tags=["Banks"])

def get_banks_service(db: Session = Depends(get_db)) -> IBanksService:
    return BanksService(repository=BanksRepository(db))

@router.post("", status_code=201, response_model=BankResponseSchema)
def create_bank(bank_in: BankCreateSchema, service: IBanksService = Depends(get_banks_service)):
    return service.create(bank_in)

@router.get("", response_model=list[BankResponseSchema])
def get_banks(skip: int = 0, limit: int = 100, service: IBanksService = Depends(get_banks_service)):
    return service.get_all(skip, limit)