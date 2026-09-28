from datetime import datetime, timezone
from fastapi import HTTPException
from Models.banks import BankCreateSchema, BankDTO, BankResponseSchema
from Repositories.BanksRepository import BanksRepository
from Services.IBanksService import IBanksService

class BanksService(IBanksService):
    def __init__(self, repository: BanksRepository):
        self.repository = repository

    def create(self, schema: BankCreateSchema) -> BankResponseSchema:
        if self.repository.get_by_name(schema.name):
            raise HTTPException(status_code=400, detail="Ya existe un banco registrado con este nombre.")

        bank_dto = BankDTO(**schema.model_dump(), created_at=datetime.now(timezone.utc))
        created_bank = self.repository.create(bank_dto)
        return BankResponseSchema.model_validate(created_bank)

    def get_all(self, skip: int = 0, limit: int = 100) -> list[BankResponseSchema]:
        banks = self.repository.get_all(skip, limit)
        return [BankResponseSchema.model_validate(b) for b in banks]