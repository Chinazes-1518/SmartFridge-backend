from fastapi import APIRouter

from . import auth, buylist

router = APIRouter()

router.include_router(auth.router)
router.include_router(buylist.router)
