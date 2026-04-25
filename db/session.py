from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from db.models import Base

engine = create_engine("sqlite:///teaching.db",echo=False)
Sessionlocal= sessionmaker(bind=engine)

def init_db() -> None:
    Base.metadata.create_all(engine)

def get_session() -> Session:
    return Sessionlocal()

