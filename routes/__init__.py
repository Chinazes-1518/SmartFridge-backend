from fastapi import APIRouter

from . import auth, buylist, products

router = APIRouter()

router.include_router(auth.router)
router.include_router(buylist.router)
router.include_router(products.router)
