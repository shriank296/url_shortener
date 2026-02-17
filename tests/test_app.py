import pytest

from models import Url


def test_create_short_url(client):
    """
    Verifies a successful short url creation.

    :param create_tables: Fixture to create all tables
    :type create_tables: None
    :param client: Test client
    :type client: TestClient
    """
    result = client.post(
        url="/short_url",
        json={"original_url": "http://something.com"},
    )
    data = result.json()
    assert result.status_code == 201, data  # noqa: PLR2004, S101
    assert "short_code" in data  # noqa: S101


@pytest.fixture
def insert_record(db_session):
    url = Url(short_code="test123", original_url="http://test.com")
    db_session.add(url)
    db_session.commit()


def test_get_short_code(insert_record, client):  # noqa: ARG001
    response = client.get("/test123", follow_redirects=False)
    assert response.status_code in (307, 308)  # noqa: S101
    assert response.headers["location"] == "http://test.com"  # noqa: S101
