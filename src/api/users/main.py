from fastapi import APIRouter, HTTPException, Depends, Request
from sqlalchemy.orm import Session
from src.models.library_models import User
from src.utils.db_utils import get_db

router = APIRouter()

@router.get("/users")
def get_users(db: Session = Depends(get_db)):
    return db.query(User).all()

@router.post("/users")
async def create_user(request: Request, db: Session = Depends(get_db)):
    user_data = await request.json()
    name = user_data.get("name")
    email = user_data.get("email")
    phone = user_data.get("phone")

    if not name or not email or not phone:
        raise HTTPException(status_code=400, detail="Missing required fields")

    new_user = User(name=name, email=email, phone=phone)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"id": new_user.id, "name": new_user.name, "email": new_user.email, "phone": new_user.phone}