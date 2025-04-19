from fastapi import APIRouter, HTTPException, Depends
from app.services.unified.schema import User, LoginRequest
from app.services.unified.controller import create_user_account, login_user_account

router = APIRouter()

@router.post("/user/register", status_code=201, tags=["User"])
async def register(payload: User):
    try:
        user_id = await create_user_account(payload)
        if not user_id:
            raise HTTPException(status_code=400, detail="User account creation failed")
        return {"message": "User account created successfully", "data": user_id}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.post("/user/login", status_code=200, tags=["User"])
async def login(payload: LoginRequest):
    try:
        token_response = await login_user_account(payload)
        if not token_response:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        return {"message": "Login successful", "data": token_response}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))