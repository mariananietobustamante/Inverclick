from datetime import datetime, timezone
from fastapi import HTTPException
from Models.leads import LeadCreateSchema, LeadDTO, LeadResponseSchema
from Repositories.LeadsRepository import LeadsRepository
from Repositories.UsuariosRepository import UsersRepository
from Services.ILeadsService import ILeadsService

class LeadsService(ILeadsService):
    def __init__(self, repository: LeadsRepository, users_repository: UsersRepository):
        self.repository = repository
        self.users_repository = users_repository

    def create(self, schema: LeadCreateSchema) -> LeadResponseSchema:
        # Regla de negocio: Validar existencia del usuario asociado
        if not self.users_repository.get_by_id(schema.user_id):
            raise HTTPException(status_code=404, detail="El usuario asignado al lead no existe.")

        lead_dto = LeadDTO(**schema.model_dump(), created_at=datetime.now(timezone.utc))
        created_lead = self.repository.create(lead_dto)
        return LeadResponseSchema.model_validate(created_lead)

    def get_all(self, skip: int = 0, limit: int = 100) -> list[LeadResponseSchema]:
        leads = self.repository.get_all(skip, limit)
        return [LeadResponseSchema.model_validate(l) for l in leads]