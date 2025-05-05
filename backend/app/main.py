from fastapi import FastAPI
from app.api import users
from app.api import auth, users
from app.api import documents
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()
# Allow CORS for your frontend
origins = [
    "http://localhost:4200"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # or ["*"] to allow all origins (not recommended in production)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get("/")
def read_root():
    return {"message": "Hello, World!"}
app.include_router(users.router)
app.include_router(auth.router, prefix="/api/auth", tags=["Auth"])
app.include_router(documents.router, prefix="/api/document", tags=["Document"])
