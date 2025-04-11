### ips apis
from fastapi import APIRouter

router = APIRouter()

@router.get("/test_ips")
async def demo():
    return "Hello Toan"