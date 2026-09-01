from Models.users import UserCreateSchema, UserResponseSchema, UserUpdateSchema


class IUsuariosService:
    def get_by_id(self, user_id: int) -> UserResponseSchema:
        pass

    def get_by_email(self, email: str) -> UserResponseSchema:
        pass

    def get_all(self, skip: int = 0, limit: int = 100) -> list[UserResponseSchema]:
        pass

    def create(self, schema: UserCreateSchema) -> UserResponseSchema:
        pass

    def update(self, user_id: int, schema: UserUpdateSchema) -> UserResponseSchema:
        pass

    def delete(self, user_id: int) -> bool:
        pass
