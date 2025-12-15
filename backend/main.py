from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers.coverletter import router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_headers=["*"],
    allow_methods=["*"],
)

app.include_router(router)
