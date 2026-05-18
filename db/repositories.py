from sqlalchemy import select

from .engine import Session
from .models import SyncUserData, AsyncUserData

# Insert synchronous user data and immediately return persisted values
def create_and_get_sync_user_data(name: str, surname: str) -> dict:
    with Session.begin() as session:
        user_data = SyncUserData(name=name, surname=surname)
        session.add(user_data)
        session.flush()
        stmt = select(SyncUserData).where(SyncUserData.id == user_data.id)
        confirmed_user_data: SyncUserData = session.execute(stmt).scalars().one()
        return {"name": confirmed_user_data.name, "surname": confirmed_user_data.surname}

# Insert asynchronously processed user data
def create_async_user_data(username: str, phone_number: str) -> int:
    with Session.begin() as session:
        async_user_data = AsyncUserData(username=username, phone_number=phone_number)
        session.add(async_user_data)
        session.flush()
        return async_user_data.id

# Retrieve asynchronous user data by database identifier
def get_async_user_data_by_id(user_id: int) -> dict:
    with Session.begin() as session:
        stmt = select(AsyncUserData).where(AsyncUserData.id == user_id)
        user_data: AsyncUserData = session.execute(stmt).scalars().one()
        return {"username": user_data.username, "phone_number": user_data.phone_number}