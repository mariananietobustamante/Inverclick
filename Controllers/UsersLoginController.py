from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from Models.auth import LoginTokenResponseSchema
from Models.users_login import (
    LoginRequestSchema,
    UserLoginCreateSchema,
    UserLoginResponseSchema,
    UserLoginUpdateSchema,
)
from Repositories.UsersLoginRepository import UsersLoginRepository
from Repositories.UsersRoleRepository import UsersRoleRepository
from Repositories.UsuariosRepository import UsersRepository
from Repositories.database import get_db
from Services.IUsersLoginService import IUsersLoginService
from Services.Impl.UsersLoginService import UsersLoginService
from Services.Security.auth_dependencies import require_module
from Utils.HttpResponses.userLoginHttpResponses import UserLoginHttpResponses
from Utils.enums import AppModule
from Utils.user_login_validator import UserLoginValidator

router = APIRouter(prefix="/users-login", tags=["UsersLogin"])


def get_users_login_service(db: Session = Depends(get_db)) -> IUsersLoginService:
    return UsersLoginService(
        repository=UsersLoginRepository(db),
        http_responses=UserLoginHttpResponses(),
        validator=UserLoginValidator(),
        users_repository=UsersRepository(db),
        roles_repository=UsersRoleRepository(db),
    )


@router.post("/login", response_model=LoginTokenResponseSchema)
def login(credentials: LoginRequestSchema, service: IUsersLoginService = Depends(get_users_login_service)):
    """Autenticación pública: devuelve JWT con expiración y módulos del rol."""
    return service.authenticate(credentials)


@router.get("/{login_id}", response_model=UserLoginResponseSchema)
def get_login_by_id(
    login_id: int,
    service: IUsersLoginService = Depends(get_users_login_service),
    _auth=Depends(require_module(AppModule.USERS_LOGIN)),
):
    return service.get_by_id(login_id)


@router.get("/user/{user_id}", response_model=UserLoginResponseSchema)
def get_login_by_user_id(
    user_id: int,
    service: IUsersLoginService = Depends(get_users_login_service),
    _auth=Depends(require_module(AppModule.USERS_LOGIN)),
):
    return service.get_by_user_id(user_id)


@router.get("/email/{email}", response_model=UserLoginResponseSchema)
def get_login_by_email(
    email: str,
    service: IUsersLoginService = Depends(get_users_login_service),
    _auth=Depends(require_module(AppModule.USERS_LOGIN)),
):
    return service.get_by_email(email)


@router.get("", response_model=list[UserLoginResponseSchema])
def get_all_logins(
    skip: int = 0,
    limit: int = 100,
    service: IUsersLoginService = Depends(get_users_login_service),
    _auth=Depends(require_module(AppModule.USERS_LOGIN)),
):
    return service.get_all(skip=skip, limit=limit)


@router.post("", status_code=201, response_model=UserLoginResponseSchema)
def create_login(login: UserLoginCreateSchema, service: IUsersLoginService = Depends(get_users_login_service)):
    """Público para registro inicial de credenciales (onboarding)."""
    return service.create(login)


@router.put("/{login_id}", response_model=UserLoginResponseSchema)
def update_login(
    login_id: int,
    login: UserLoginUpdateSchema,
    service: IUsersLoginService = Depends(get_users_login_service),
    _auth=Depends(require_module(AppModule.USERS_LOGIN)),
):
    return service.update(login_id, login)


@router.delete("/{login_id}")
def delete_login(
    login_id: int,
    service: IUsersLoginService = Depends(get_users_login_service),
    _auth=Depends(require_module(AppModule.USERS_LOGIN)),
):
    return {"success": service.delete(login_id)}
