"""Standard session independent pass-through service."""

from ..config.db_config import async_session
from ..types_app import TypeModel, TypePK
from . import service_session_dependent as service


async def get_all(model: TypeModel) -> list[TypeModel]:
    async with async_session() as session:
        return await service.get_all(session, model)


async def get(model: TypeModel, **filter_data) -> TypeModel:
    async with async_session() as session:
        return await service.get(session, model, **filter_data)


async def create(entity: TypeModel | object, **create_data) -> TypeModel:
    async with async_session.begin() as session:
        return await service.create(session, entity, **create_data)


async def update(model: TypeModel, id: TypePK, **update_data) -> TypeModel:
    async with async_session.begin() as session:
        return await service.update(session, model, id, **update_data)


async def delete(model: TypeModel, id: TypePK) -> TypeModel:
    async with async_session.begin() as session:
        return await service.delete(session, model, id)
