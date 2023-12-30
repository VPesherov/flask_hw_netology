import atexit
import datetime

from sqlalchemy import create_engine, String, DateTime, func
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Mapped, mapped_column

# задаём данные для подключения к бд
POSTGRES_USER = 'postgres'
POSTGRES_PASSWORD = '123'
POSTGRES_DB = 'flask_hw'
POSTGRES_HOST = '127.0.0.1'
POSTGRES_PORT = '5431'

# создаём подключение к бд
PG_DSN = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
engine = create_engine(PG_DSN)
# создаём сессию
Session = sessionmaker(bind=engine)

# это функция закроет подключение, если оно не закроется само
atexit.register(engine.dispose)


class Base(DeclarativeBase):
    pass


class Ad(Base):
    __tablename__ = "app_ads"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100), index=True, nullable=False)
    description: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=func.now())
    owner_ad: Mapped[int] = mapped_column(nullable=False)

    @property
    def ads_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'created_at': self.created_at.isoformat(),
            'owner_ad': self.owner_ad
        }


Base.metadata.create_all(bind=engine)
