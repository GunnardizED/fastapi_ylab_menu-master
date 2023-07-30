from typing import Any, Generic, Optional, Type, TypeVar

from fastapi import status
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse
from pydantic.types import UUID4
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.db.models import DefaultBase, DefaultCreateBase, DefaultUpdateBase

ModelType = TypeVar("ModelType", bound=DefaultBase)
CreateSchemaType = TypeVar("CreateSchemaType", bound=DefaultCreateBase)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=DefaultUpdateBase)


class BaseService(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):

#Basic CRUD class

    def __init__(self, model: Type[ModelType], db_session: AsyncSession):
        self.model = model
        self.db_session = db_session

    async def list(self, **kwargs: Any) -> list[ModelType]:

    # list function returns all ModelType objects in the database.
    #
    #Args:
    #    kwargs:: The id of the object
    #
    #Returns:
    #    list of objects that are ModelType

        statement = select(self.model).filter_by(**kwargs)
        result = await self.db_session.execute(statement)
        objs: list[ModelType] = result.scalars().all()
        return objs

    async def get(self, id_: UUID4) -> Optional[ModelType]:

        #function is used to retrieve a single object from the database.
        #functoin takes an id and returns object, or raises an
        #HTTP 404 error if no matching object exists.
        #
        #Args:
        #   id_:UUID4: The id of the object
        #
        #Returns:
        #   The object of ModelType with param id primary key


        statement = select(self.model).where(self.model.id == id_)
        result = await self.db_session.execute(statement)
        try:
            obj: Optional[ModelType] = result.scalar_one()
            return obj
        except NoResultFound:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"{self.model.__name__.lower()} not found",
            )

    async def create(
            self, obj: CreateSchemaType, **kwargs
    ) -> Optional[ModelType]:

        #function makes a new object of the type specified in the
        #CreateSchemaType parameter. It takes an argument of obj which is an
        #instance of CreateSchemaType and returns a ModelType object.
        #
        #Args:
        #    obj:CreateSchemaType: Specify the schema to use for validation
        #
        #Returns:
        #    The created ModelType object

        db_obj: ModelType = self.model(**dict(**obj.dict(), **kwargs))
        self.db_session.add(db_obj)
        await self.db_session.commit()
        return await self.get(db_obj.id)

    async def update(
            self, id_: UUID4, obj: UpdateSchemaType
    ) -> Optional[ModelType]:

        #function updates an existing object in the database.
        #takes two arguments, id_ and obj. The id_ argument is the unique
        #ID of object in database
        # obj is a dictionary containing all the columns to be updated for that object.
        #
        #Args:
        #    id_:UUID4: Identify the object to update
        #    obj:UpdateSchemaType: Specify the schema for data validation
        #
        #Returns:
        #    The updated object


        db_obj = await self.get(id_)
        for column, value in obj.dict(exclude_unset=True).items():
            setattr(db_obj, column, value)
        await self.db_session.commit()
        return db_obj

    async def delete(self, id_: UUID4) -> JSONResponse:


        #function is used to delete an item from the database.
        #It takes a UUID4 as an argument and deletes the object with ID
        #from the database.function returns a JSONResponse containing a
        #message confirming delete.
        #
        #Args:
        #    id_:UUID4: Get the id of the object that is to be deleted
        #
        #Returns:
        #    A JSONResponse containing a message confirming that it was deleted


        db_obj = await self.get(id_)
        await self.db_session.delete(db_obj)
        await self.db_session.commit()
        item_data = {
            "status": True,
            "message": f"The {self.model.__name__.lower()} has been deleted",
        }
        return JSONResponse(content=item_data)
