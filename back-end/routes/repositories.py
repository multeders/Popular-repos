from fastapi import APIRouter, Query
from services.github_service import fetch_popular_repositories

router = APIRouter()

@router.get("/popular")
async def get_popular_repositories(
    date: str,
    limit: int = Query(10, ge=1, le=100),
    language: str = Query(None)
):
    """
    Fetch the most popular repositories.
    """
    return await fetch_popular_repositories(date=date, limit=limit, language=language)
