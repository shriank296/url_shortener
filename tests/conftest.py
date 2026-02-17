import pytest
from fastapi.testclient import TestClient
from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session, sessionmaker

from db import get_db
from main import app
from models import Base

TEST_DB_URL = "sqlite:///:memory:"

engine: Engine = create_engine(
    url=TEST_DB_URL,
    connect_args={"check_same_thread": False},
)

TestSessionLocal: sessionmaker[Session] = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    expire_on_commit=False,
)


@pytest.fixture
def db_session():
    connection = engine.connect()
    transaction = connection.begin()

    session = TestSessionLocal(bind=connection)

    yield session

    session.close()
    transaction.rollback()
    transaction.close()


@pytest.fixture
def client(db_session, create_tables):  # noqa: ARG001
    test_client = TestClient(app)

    def get_override_db():
        yield db_session

    test_client.app.dependency_overrides[get_db] = get_override_db

    yield test_client

    test_client.app.dependency_overrides.clear()


@pytest.fixture(scope="session")
def create_tables():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
