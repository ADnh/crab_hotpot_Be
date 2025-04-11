### crud apis
from fastapi import APIRouter

router = APIRouter()

@router.get("/test_crud")
async def demo():
    return "Hello La"