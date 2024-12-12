from fastapi import FastAPI, Depends
from fastapi.responses import RedirectResponse
from app.auth import authenticate_user
from app.auth import router as auth_router
from app.payment import router as payment_router
from app.routes.content import router as content_router

app = FastAPI()

# Include routes
# app.include_router(auth_router, prefix="/auth", dependencies=[Depends(authenticate_user)]) -- I think I have to do this for ONE of the routes, but I don't need the user to be authenticated if I'm just Sending the user to be authenticated
app.include_router(auth_router, prefix="/auth")
app.include_router(payment_router, prefix="/payment")
app.include_router(content_router, prefix="/content")

@app.get("/")
def home():
    return RedirectResponse(url="/auth/google-login")