from fastapi import HTTPException
from Repositories.RealEstateRepository import RealEstateRepository
from Repositories.UsuariosRepository import UsersRepository # Importamos el repositorio de usuarios

class RealEstateService:
    def __init__(self, repository: RealEstateRepository, users_repository: UsersRepository):
        self.repository = repository
        self.users_repository = users_repository

    def get_properties_for_user(self, user_id: int, skip: int = 0, limit: int = 100):
        # 1. El servicio asume la responsabilidad de buscar al usuario
        current_user = self.users_repository.get_by_id(user_id)
        if not current_user:
            raise HTTPException(status_code=404, detail="Usuario no encontrado en la base de datos")

        # 2. Lógica de negocio intacta
        if current_user.role_id == 3:
            if not current_user.construction_company_id:
                return []
            return self.repository.get_by_company(current_user.construction_company_id, skip, limit)
        
        return self.repository.get_all(skip, limit)

    def create_property(self, user_id: int, property_in):
        current_user = self.users_repository.get_by_id(user_id)
        if not current_user:
            raise HTTPException(status_code=404, detail="Usuario no encontrado en la base de datos")

        if current_user.role_id not in [1, 3]:
            raise HTTPException(status_code=403, detail="Tu rol no tiene permisos para crear propiedades.")
        
        data_dict = property_in.model_dump()

        # Validación 1: Constructora obligatoria
        if current_user.role_id == 3:
            if not current_user.construction_company_id:
                raise HTTPException(status_code=403, detail="El usuario no tiene una empresa constructora asignada.")
            data_dict["construction_company_id"] = current_user.construction_company_id
        elif current_user.role_id == 1:
            # Si un Admin intenta crearla, DEBE enviar el ID de la constructora en el JSON
            if not data_dict.get("construction_company_id"):
                raise HTTPException(status_code=400, detail="El ID de la constructora es obligatorio para registrar la propiedad.")

        # Validación 2: Unicidad de Nombre y Dirección
        if self.repository.get_by_name(data_dict["name"]):
            raise HTTPException(status_code=400, detail="Ya existe una propiedad registrada con este nombre.")
        
        if self.repository.get_by_address(data_dict["address"]):
            raise HTTPException(status_code=400, detail="Ya existe una propiedad registrada con esta dirección exacta.")

        return self.repository.create(data_dict)