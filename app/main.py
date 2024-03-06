import uvicorn
from fastapi import FastAPI, Response, status

from auth.routers import users_router

app = FastAPI()

app.include_router(users_router.router)


@app.get("/")
async def ping_test():
    return Response(status_code=status.HTTP_200_OK)


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
