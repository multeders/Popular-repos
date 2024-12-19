from fastapi import APIRouter, Query
from typing import Optional
from models.github_models import Repository
from services.github_service import fetch_popular_repositories

router = APIRouter()

@router.get("/popular", response_model=list[Repository])
async def get_popular_repositories(
    date: str,
    limit: int = Query(10, ge=1, le=100),
    language: Optional[str] = Query(None)
):
    """
    Fetch the most popular repositories.
    """
    repositories = await fetch_popular_repositories(date=date, limit=limit, language=language)
    return repositories
