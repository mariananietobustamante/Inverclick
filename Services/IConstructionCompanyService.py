from Models.construction_companies import ConstructionCompanyCreateSchema


class IConstructionCompanyService:
    def get_all_for_user(self, user_id: int, skip: int = 0, limit: int = 100):
        pass

    def create(self, company: ConstructionCompanyCreateSchema):
        pass
