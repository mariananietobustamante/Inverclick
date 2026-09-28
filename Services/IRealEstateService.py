from Models.real_estate import RealEstateCreateSchema


class IRealEstateService:
    def get_properties_for_user(self, user_id: int, skip: int = 0, limit: int = 100):
        pass

    def create_property(self, user_id: int, property_in: RealEstateCreateSchema):
        pass
