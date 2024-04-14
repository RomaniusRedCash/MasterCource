from typing import Callable

import uvicorn
from fastapi import FastAPI, Response, status, Request
from fastapi.middleware.cors import CORSMiddleware

from auth.routers import users_router

app = FastAPI()

app.include_router(users_router.router)


@app.middleware("http")
async def show_request(request: Request, call_next: Callable[..., Response]):
    body = await request.body()
    print("body:", body.decode())
    print("headers:", request.headers)
    print("query:", request.path_params)
    print("path:", request.query_params)
    print("client:", request.client)
    print("cookie:", request.cookies)
    response = await call_next(request)
    return response


@app.get("/")
async def ping_test():
    return Response(status_code=status.HTTP_200_OK)


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
