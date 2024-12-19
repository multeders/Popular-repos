from utils.cache import get_cache, set_cache
from datetime import datetime
from typing import List, Optional
from models.github_models import Repository
import requests
import hashlib

GITHUB_API_URL: str = "https://api.github.com/search/repositories"

async def fetch_popular_repositories(date: str, limit: int, language: Optional[str] = None) -> List[Repository]:
    """
    Fetch repositories from GitHub API, with Redis caching, using requests library.
    """
    cache_key: str = hashlib.md5(f"{limit}-{language}-{date}".encode()).hexdigest()
    cached_response: Optional[List[dict]] = await get_cache(cache_key)
    if cached_response:
        return [Repository(**repo) for repo in cached_response]

    # No cache found, fetch from GitHub
    query: List[str] = []
    if date:
        query.append(f"created:{date}")
    if language:
        query.append(f"language:{language}")
    query_string: str = "+".join(query)
    url: str = f"{GITHUB_API_URL}?q={query_string}&sort=stars&order=desc&per_page={limit}"

    # Make a GET request
    response = requests.get(url, headers={"Accept": "application/vnd.github.v3+json"})
    response.raise_for_status()
    data = response.json()

    # Transform and cache response
    transformed_data = [
        {
            "id": repo["id"],
            "name": repo["name"],
            "stars": repo["stargazers_count"],
            "language": repo["language"],
            "url": repo["html_url"],
        }
        for repo in data["items"]
    ]

    try:
        selected_date = datetime.strptime(date, "%Y-%m-%d").date()
    except ValueError:
        raise ValueError("Invalid date format. Expected 'YYYY-MM-DD'.")

    today = datetime.today().date()
    if selected_date < today:
        await set_cache(cache_key, transformed_data, None)

    return [Repository(**repo) for repo in transformed_data]
