from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session, sessionmaker

DB_URL = "sqlite:///./urls.db"

engine: Engine = create_engine(url=DB_URL, connect_args={"check_same_thread": False})

SessionLocal: sessionmaker[Session] = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    expire_on_commit=False,
)


def get_db():
    with SessionLocal() as session:
        yield session
