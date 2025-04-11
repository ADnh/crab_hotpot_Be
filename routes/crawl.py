### crawl apis
from fastapi import APIRouter

router = APIRouter()

@router.get("/test_crawl")
async def demo():
    return "Hello Duc"