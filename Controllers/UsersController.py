from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session



from Models.users import UserCreateSchema, UserResponseSchema, UserUpdateSchema

from Repositories.CountriesRepository import CountriesRepository

from Repositories.ConstructionCompanyRepository import ConstructionCompanyRepository

from Repositories.IdTypesRepository import IdTypesRepository

from Repositories.PrefixRepository import PrefixRepository

from Repositories.UsersRoleRepository import UsersRoleRepository

from Repositories.UsuariosRepository import UsersRepository

from Repositories.database import get_db

from Services.IUsuariosService import IUsuariosService

from Services.Impl.UsuariosService import UsuariosService

from Services.Security.auth_dependencies import require_module

from Utils.HttpResponses.userHttpResponses import UserHttpResponses

from Utils.enums import AppModule

from Utils.user_validator import UserValidator



router = APIRouter(prefix="/users", tags=["Users"])





def get_usuarios_service(db: Session = Depends(get_db)) -> IUsuariosService:

    return UsuariosService(

        repository=UsersRepository(db),

        countries_repository=CountriesRepository(db),

        prefix_repository=PrefixRepository(db),

        roles_repository=UsersRoleRepository(db),

        id_types_repository=IdTypesRepository(db),

        construction_company_repository=ConstructionCompanyRepository(db),

        http_responses=UserHttpResponses(),

        validator=UserValidator(),

    )





@router.get("/{usuario_id}", response_model=UserResponseSchema)

def get_user_by_id(

    usuario_id: int,

    service: IUsuariosService = Depends(get_usuarios_service),

    _auth=Depends(require_module(AppModule.USERS)),

):

    return service.get_by_id(usuario_id)





@router.get("/email/{email}", response_model=UserResponseSchema)

def get_user_by_email(

    email: str,

    service: IUsuariosService = Depends(get_usuarios_service),

    _auth=Depends(require_module(AppModule.USERS)),

):

    return service.get_by_email(email)





@router.get("", response_model=list[UserResponseSchema])

def get_all_users(

    skip: int = 0,

    limit: int = 100,

    service: IUsuariosService = Depends(get_usuarios_service),

    _auth=Depends(require_module(AppModule.USERS)),

):

    return service.get_all(skip=skip, limit=limit)





@router.post("", status_code=201, response_model=UserResponseSchema)

def create_user(user: UserCreateSchema, service: IUsuariosService = Depends(get_usuarios_service)):

    """Público para registro inicial de usuarios (onboarding)."""

    return service.create(user)





@router.put("/{usuario_id}", response_model=UserResponseSchema)

def update_user(

    usuario_id: int,

    user: UserUpdateSchema,

    service: IUsuariosService = Depends(get_usuarios_service),

    _auth=Depends(require_module(AppModule.USERS)),

):

    return service.update(usuario_id, user)





@router.delete("/{usuario_id}")

def delete_user(

    usuario_id: int,

    service: IUsuariosService = Depends(get_usuarios_service),

    _auth=Depends(require_module(AppModule.USERS)),

):

    return {"success": service.delete(usuario_id)}


