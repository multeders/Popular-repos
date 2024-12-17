from utils.cache import get_cache, set_cache
from datetime import datetime
import requests
import hashlib

GITHUB_API_URL = "https://api.github.com/search/repositories"

async def fetch_popular_repositories(date: str, limit: int, language: str = None):
    """
    Fetch repositories from GitHub API, with Redis caching, using requests library.
    """
    cache_key = hashlib.md5(f"{limit}-{language}-{date}".encode()).hexdigest()
    cached_response = await get_cache(cache_key) 
    if cached_response:
        return cached_response

    # No cache found, fetch from GitHub
    query = []
    if date:
        query.append(f"created:{date}")
    if language:
        query.append(f"language:{language}")
    query_string = "+".join(query)
    url = f"{GITHUB_API_URL}?q={query_string}&sort=stars&order=desc&per_page={limit}"

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
        
    return transformed_data
