from fastapi import APIRouter

router = APIRouter()

@router.post("/checkout")
def checkout():
    return {"message": "Stripe checkout endpoint"}