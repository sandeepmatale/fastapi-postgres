from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from app.database import Base, engine, get_db
from app import crud, schemas
from app.auth import get_current_user

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Student Management System API")

# ---------- AUTH ----------
@app.post("/signup", response_model=schemas.UserOut)
def signup(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.register_user(db, user)

@app.post("/login", response_model=schemas.Token)
def login(user: schemas.UserCreate, db: Session = Depends(get_db)):
    token = crud.login_user(db, user.email, user.password)
    return {"access_token": token, "token_type": "bearer"}


# ---------- STUDENTS ----------
@app.post("/students/", response_model=schemas.StudentOut)
def create_student(
    student: schemas.StudentCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return crud.create_student(db, student)

@app.get("/students/", response_model=list[schemas.StudentOut])
def get_students(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return crud.list_students(db)

@app.get("/students/{student_id}", response_model=schemas.StudentOut)
def get_student(
    student_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    student = crud.get_student(db, student_id)
    if not student:
        from fastapi import HTTPException
        raise HTTPException(404, "Student not found")
    return student

@app.put("/students/{student_id}", response_model=schemas.StudentOut)
def update_student(
    student_id: int,
    data: schemas.StudentUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return crud.update_student(db, student_id, data)

@app.delete("/students/{student_id}")
def delete_student(
    student_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    crud.delete_student(db, student_id)
    return {"message": "Student deleted successfully"}
