import uuid

from datetime import datetime
from fastapi import HTTPException
from sqlmodel import Session

from app.modules.permiso_usuario.infrastructure.permiso_usuario_model import PermisoUsuarioModel
from app.modules.permiso_usuario.interfaces.permiso_usuario_schema import PermisoUsuarioCreate, PermisoUsuarioRead, PermisoUsuarioUpdate
from app.modules.permiso_usuario.infrastructure.permiso_usuario_repository import PermisoUsuarioRepository
from app.modules.usuario.infrastructure.usuario_repository import UsuarioRepository
from app.modules.pantalla.infrastructure.pantalla_repository import PantallaRepository
from app.modules.permiso.infrastructure.permiso_repository import PermisoRepository


class PermisoUsuarioService:
    def __init__(self, db: Session):
        self.db = db
        self.permiso_usuario_repository = PermisoUsuarioRepository(db)
        self.pantalla_repository = PantallaRepository(db)
        self.usuario_repository = UsuarioRepository(db)
        self.permiso_repository = PermisoRepository(db)

    def crear(self, payload: PermisoUsuarioCreate, user_id: str) -> PermisoUsuarioRead:
        usuario_crea = self.usuario_repository.validar_usuario(user_id)
        usuario = self.usuario_repository.validar_usuario(payload.usuario_id)

        pantalla = self.pantalla_repository.obtener_por_tracking_id(
            payload.pantalla_id)
        if not pantalla:
            raise HTTPException(
                status_code=404, detail="La pantalla no se encuentra registrada.")

        permiso = self.permiso_repository.obtener_por_tracking_id(
            payload.permiso_id)
        if not permiso:
            raise HTTPException(
                status_code=404, detail="El permiso no se encuentra registrado.")

        permiso_usuario = PermisoUsuarioModel(
            tracking_id=str(uuid.uuid4()),
            usuario_id=usuario.usuario_id,
            pantalla_id=pantalla.pantalla_id,
            permiso_id=permiso.permiso_id,
            registrado_por=usuario_crea.usuario_id
        )

        self._validar_permiso_existe(
            permiso_usuario, usuario.nombre, pantalla.pantalla, permiso.permiso)

        permiso_usuario = self.permiso_usuario_repository.crear(
            permiso_usuario)
        return self._map_to_read(permiso_usuario)

    def actualizar(self, payload: PermisoUsuarioUpdate, user_id: str) -> PermisoUsuarioRead:
        usuario_crea = self.usuario_repository.validar_usuario(user_id)
        usuario = self.usuario_repository.validar_usuario(payload.usuario_id)

        permiso_usuario = self.permiso_usuario_repository.obtener_por_tracking_id(
            payload.tracking_id)
        if not permiso_usuario:
            raise HTTPException(
                status_code=404, detail="El permiso no se encuentra registrado.")

        pantalla = self.pantalla_repository.obtener_por_tracking_id(
            payload.pantalla_id)
        if not pantalla:
            raise HTTPException(
                status_code=404, detail="La pantalla no se encuentra registrada.")

        permiso = self.permiso_repository.obtener_por_tracking_id(
            payload.permiso_id)
        if not permiso:
            raise HTTPException(
                status_code=404, detail="El permiso no se encuentra registrado.")

        permiso_usuario.usuario_id = usuario.usuario_id
        permiso_usuario.pantalla_id = pantalla.pantalla_id
        permiso_usuario.permiso_id = permiso.permiso_id
        permiso_usuario.modificado_por = usuario_crea.usuario_id
        permiso_usuario.fecha_modificacion = datetime.now()
        permiso_usuario = self.permiso_usuario_repository.actualizar(
            permiso_usuario)

        return self._map_to_read(permiso_usuario)

    def eliminar(self, tracking_id: str, user_id: str) -> None:
        self.usuario_repository.validar_usuario(user_id)

        permiso_usuario = self.permiso_usuario_repository.obtener_por_tracking_id(
            tracking_id)
        if not permiso_usuario:
            raise HTTPException(
                status_code=404, detail="El permiso no se encuentra registrado")

        self.permiso_usuario_repository.eliminar(permiso_usuario)

    def obtener_por_permiso_usuario_id(self, permiso_usuario_id: int) -> PermisoUsuarioRead:
        permiso_usuario = self.permiso_usuario_repository.obtener_por_permiso_usuario_id(
            permiso_usuario_id)
        return self._map_to_read(permiso_usuario)

    def obtener_por_tracking_id(self, tracking_id: str) -> PermisoUsuarioRead:
        permiso_usuario = self.permiso_usuario_repository.obtener_por_tracking_id(
            tracking_id)
        return self._map_to_read(permiso_usuario)

    def obtener_por_usuario_pantalla(self, usuario_id: int, pantalla_id: int) -> PermisoUsuarioRead:
        permiso_usuario = self.permiso_usuario_repository.obtener_por_usuario_pantalla(
            usuario_id, pantalla_id)
        return self._map_to_read(permiso_usuario)

    def obtener_por_usuario_modulo(self, usuario_id: int, modulo_id: int) -> list[PermisoUsuarioRead]:
        permiso_usuarios = self.permiso_usuario_repository.obtener_por_usuario_modulo(
            usuario_id, modulo_id)
        return [self._map_to_read(permiso_usuario) for permiso_usuario in permiso_usuarios]

    def obtener_todos(self, activo: bool) -> list[PermisoUsuarioRead]:
        permiso_usuarios = self.permiso_usuario_repository.obtener_todos(
            activo)
        return [self._map_to_read(permiso_usuario) for permiso_usuario in permiso_usuarios]

    def _map_to_read(self, permiso_usuario: PermisoUsuarioModel) -> PermisoUsuarioRead:
        usuario = self.usuario_repository.obtener_por_usuario_id(
            permiso_usuario.usuario_id)
        pantalla = self.pantalla_repository.obtener_por_pantalla_id(
            permiso_usuario.pantalla_id)
        permiso = self.permiso_repository.obtener_por_permiso_id(
            permiso_usuario.permiso_id)

        return PermisoUsuarioRead(
            tracking_id=permiso_usuario.tracking_id,
            usuario_id=usuario.user_id,
            usuario=usuario.nombre,
            pantalla_id=pantalla.tracking_id,
            pantalla=pantalla.pantalla,
            permiso_id=permiso.tracking_id,
            permiso=permiso.permiso
        )

    def _validar_permiso_existe(self, permiso_usuario: PermisoUsuarioModel, usuario: str, pantalla: str, permiso: str):
        if self.permiso_usuario_repository.obtener_por_usuario_pantalla_permiso(
                permiso_usuario.usuario_id,
                permiso_usuario.pantalla_id,
                permiso_usuario.permiso_id):
            raise HTTPException(
                status_code=409, detail=f"El permiso {permiso.lower()} ya existe para el usuario {usuario.lower()} en la pantalla {pantalla.lower()}.")
