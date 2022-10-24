from database import engine
import models
from database import SessionLocal
from sqlalchemy.orm import Session

from fastapi import Depends, FastAPI
app = FastAPI()


models.Base.metadata.create_all(engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()    


#CRUD   
#Create Records
@app.post("/create_user")
def create(email, db: Session = Depends(get_db)):
    new_user = models.User(email = email)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user 

#Update a record
@app.put("/update_user")
def update(user_id: int, updated_email: str, db: Session = Depends(get_db)):
    updated_user = db.query(models.User).filter(models.User.id == user_id).update({"email":updated_email})
    db.commit()
    return updated_user

#Read all records
@app.get("/get_all")
def get_all(db: Session = Depends(get_db)):
    all_users = db.query(models.User).filter(models.User.id > 1).all()
    return all_users

#Read a user
@app.get("/get_user/")
def get_all(user_id: int, db: Session = Depends(get_db)):
    users = db.query(models.User).filter(models.User.id == int(user_id)).first()
    return users

@app.delete("/delete")
def get_all(id, db: Session = Depends(get_db)):
    deletd_user = db.query(models.User).filter(models.User.id == id).delete(synchronize_session=False)
    db.commit()
    return deletd_user 
