from Models.leads import LeadCreateSchema, LeadResponseSchema

class ILeadsService:
    def create(self, schema: LeadCreateSchema) -> LeadResponseSchema:
        pass

    def get_all(self, skip: int = 0, limit: int = 100) -> list[LeadResponseSchema]:
        pass