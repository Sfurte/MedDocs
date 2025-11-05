from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.future import select
from sqlalchemy import delete, func
from app.database import async_session_maker


class BaseDAO:
    model = None

    @classmethod
    async def count(cls, **filter_by):
        async with async_session_maker() as session:
            query = select(func.count()).select_from(cls.model).filter_by(**filter_by)
            result = await session.execute(query)
            return result.scalar()  # Returns a single integer value

    @classmethod
    async def clear(cls):
        async with async_session_maker() as session:
            async with session.begin():
                query = delete(cls.model)
                result = await session.execute(query)
                await session.commit()
                return result.rowcount

    @classmethod
    async def find_all(cls, **filter_by):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**filter_by)
            result = await session.execute(query)
            return result.scalars().all()

    @classmethod
    async def find_one_or_none(cls, **filter_by):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**filter_by)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def add(cls, **values):
        async with async_session_maker() as session:
            async with session.begin():
                new_instance = cls.model(**values)
                session.add(new_instance)
                try:
                    await session.commit()
                except SQLAlchemyError as e:
                    await session.rollback()
                    raise e
                return new_instance
