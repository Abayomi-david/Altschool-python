from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel, EmailStr
from fastapi.middleware.cors import CORSMiddleware
import time
import logging

logging.basicConfig(level=logging.INFO)

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8000"], 
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)

@app.middleware("http")
async def log_request_time(request: Request, call_next):
    start_time = time.time()
    
    response = await call_next(request)
    
    process_time = time.time() - start_time
    logging.info(f"Request to {request.url.path} took {process_time:.4f} seconds")
    
    return response

class User(BaseModel):
    First_name: str
    Last_name: str
    Age: int
    Email: EmailStr
    Height: str


User_database = {}


@app.post("/User")
async def create_user(user: User):
    if user.Email in User_database:
        raise HTTPException(status_code=400, detail="User already exists")
    User_database[user.Email] = user.model_dump()
    
    return {"message": "User created", "user": user}
print(User_database)
