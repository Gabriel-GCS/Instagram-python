from fastapi import FastAPI
from routes.UserRoute import router as user_route
from routes.AuthRoute import router as login_route

app = FastAPI()

app.include_router(user_route, tags=["User"], prefix="/api/user")
app.include_router(login_route, tags=["Login"], prefix="/api/login")


@app.get("/api/health", tags=["Health"])
async def heath():
    return{
        "status": "ok"
    }
