from Repositories.IPrefixRepository import IPrefixRepository
from Models.prefix import Prefix


class PrefixService:
    def __init__(self, repository: IPrefixRepository):
        self.repository = repository

    def get_by_id(self, prefix_id: int) -> Prefix:
        prefix = self.repository.get_by_id(prefix_id)
        if prefix is None:
            raise ValueError("Prefix no encontrado")
        return prefix

    def get_by_prefix(self, prefix: str) -> Prefix:
        result = self.repository.get_by_prefix(prefix)
        if result is None:
            raise ValueError("Prefijo no encontrado")
        return result

    def get_all(self, skip: int = 0, limit: int = 100) -> list[Prefix]:
        return self.repository.get_all(skip, limit)
