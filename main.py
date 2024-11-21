from fastapi import FastAPI, Depends, HTTPException
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from controller import item_controller, auth_controller
from config.database_postgre import engine, Base
from utils.jwt import get_current_user
from sqlalchemy.orm import Session
from config.database_postgre import get_db
from service.item_service import get_user_by_id

app = FastAPI()

# Set CORS policy
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize the database
Base.metadata.create_all(bind=engine)

# Include routers
app.include_router(auth_controller.router, prefix="/auth", tags=["auth"])
app.include_router(item_controller.router, prefix="/items", tags=["items"])


# @app.get("/protected-route", tags=['private'])
# def protected_route(user_id: str = Depends(get_current_user)):
#     return {"message": f"Hello, user {user_id}"}

@app.get("/protected-route", tags=['private'])
def protected_route(db: Session = Depends(get_db), user_id: str = Depends(get_current_user)):
    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail='User not found')
    return {"message": f"Hello, User {user.username}"}

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=9105)