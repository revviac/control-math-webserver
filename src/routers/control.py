from fastapi import APIRouter

router = APIRouter()


@router.get("/hi")
async def hi(name: str):
    return f"Hi {name}"
