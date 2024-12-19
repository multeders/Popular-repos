import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, MagicMock, patch
from typing import Generator
from main import app

client = TestClient(app)


@pytest.fixture
def mock_redis() -> Generator[AsyncMock, None, None]:
    """Mock Redis connection."""
    with patch("utils.cache.get_redis_connection") as mock_redis_conn:
        redis_mock: AsyncMock = AsyncMock()
        mock_redis_conn.return_value = redis_mock

        # Mock async get and set methods
        redis_mock.get = AsyncMock(return_value=None)
        redis_mock.set = AsyncMock()

        yield redis_mock


@pytest.fixture
def mock_requests() -> Generator[MagicMock, None, None]:
    """Mock the requests library."""
    with patch("services.github_service.requests") as mock_requests_lib:
        yield mock_requests_lib


@pytest.mark.asyncio
async def test_get_popular_repositories_with_cache(mock_redis: AsyncMock) -> None:
    # Arrange: Simulate cache hit
    mock_redis.get.return_value = '[{"id": 1, "name": "test-repo", "stars": 100, "language": "Python", "url": ""}]'

    # Act
    response = client.get("/repositories/popular?date=2020-01-01&limit=10")

    # Assert
    assert response.status_code == 200
    response_data = response.json()
    assert isinstance(response_data, list)
    assert response_data[0]["name"] == "test-repo"
    assert response_data[0]["stars"] == 100
    assert response_data[0]["language"] == "Python"


def test_get_popular_repositories_no_cache(
    mock_redis: AsyncMock, mock_requests: MagicMock
) -> None:
    # Arrange: Simulate cache miss and mock API response
    mock_redis.get.return_value = None
    mock_requests.get.return_value = MagicMock(
        status_code=200,
        json=MagicMock(
            return_value={
                "items": [
                    {
                        "id": 1,
                        "name": "test-repo",
                        "stargazers_count": 100,
                        "language": "Python",
                        "html_url": "https://github.com/test-repo",
                    }
                ]
            }
        ),
    )

    # Act
    response = client.get("/repositories/popular?date=2020-01-01&limit=5")

    # Assert
    assert response.status_code == 200
    response_data = response.json()
    assert isinstance(response_data, list)
    assert len(response_data) == 1
    assert response_data[0]["name"] == "test-repo"

    # Ensure Redis was updated and API was called
    mock_redis.get.assert_called_once()
    mock_requests.get.assert_called_once()
