from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTableUUID
from app.auth.models.base import Base


class User(SQLAlchemyBaseUserTableUUID, Base):
    pass