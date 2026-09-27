from Models.banks import BankCreateSchema, BankResponseSchema

class IBanksService:
    def create(self, schema: BankCreateSchema) -> BankResponseSchema:
        pass

    def get_all(self, skip: int = 0, limit: int = 100) -> list[BankResponseSchema]:
        pass