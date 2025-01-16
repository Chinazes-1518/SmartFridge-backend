from fastapi import APIRouter

router = APIRouter(prefix='/auth')


@router.get('/login')
async def login(auth: str) -> str:
    pass
