from app.config import PG_USER, PG_PASSWORD

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Строка подключения для SQLite
DATABASE_URL = "sqlite:///ecommerce.db"

# Создаём Engine
engine = create_engine(DATABASE_URL, echo=True)

# Настраиваем фабрику сеансов
SessionLocal = sessionmaker(bind=engine)

# --------------- Асинхронное подключение к PostgreSQL -------------------------

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession, AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, declared_attr

# Строка подключения для postgresql
DATABASE_URL = f"postgresql+asyncpg://{PG_USER}:{PG_PASSWORD}@localhost:5432/ecommerce_db"

# Создаём Engine
async_engine = create_async_engine(DATABASE_URL, echo=True)

# Настраиваем фабрику сеансов
async_session_maker = async_sessionmaker(async_engine, expire_on_commit=False, class_=AsyncSession)


from sqlalchemy import Integer
from sqlalchemy.orm import Mapped, mapped_column


class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

#    @declared_attr.directive
#    def __tablename__(cls) -> str:
#        return cls.__name__.lower() + 's'