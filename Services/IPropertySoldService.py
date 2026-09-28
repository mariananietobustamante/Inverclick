from Models.property_sold import PropertySoldCreateSchema, PropertySoldResponseSchema


class IPropertySoldService:
    def register_sale(self, schema: PropertySoldCreateSchema, current_agent_id: int) -> PropertySoldResponseSchema:
        pass

    def get_all_for_user(self, user_id: int, skip: int = 0, limit: int = 100) -> list[PropertySoldResponseSchema]:
        pass
