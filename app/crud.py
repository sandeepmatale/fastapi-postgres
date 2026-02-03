from sqlalchemy.orm import Session
from fastapi import HTTPException
from app import models, schemas
from app.auth import hash_password, verify_password, create_token

# ---------- AUTH ----------
def register_user(db: Session, user_in: schemas.UserCreate):
    exists = db.query(models.User).filter(models.User.email == user_in.email).first()
    if exists:
        raise HTTPException(400, "Email already registered")

    user = models.User(
        email=user_in.email,
        hashed_password=hash_password(user_in.password),
    )

    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def login_user(db: Session, email: str, password: str):
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(400, "Invalid credentials")

    token = create_token({"sub": user.email})
    return token


# ---------- STUDENT CRUD ----------
def create_student(db: Session, student_in: schemas.StudentCreate):
    student = models.Student(**student_in.dict())
    db.add(student)
    db.commit()
    db.refresh(student)
    return student

def list_students(db: Session):
    return db.query(models.Student).all()

def get_student(db: Session, student_id: int):
    return db.query(models.Student).filter(models.Student.id == student_id).first()

def update_student(db: Session, student_id: int, data: schemas.StudentUpdate):
    student = get_student(db, student_id)
    if not student:
        raise HTTPException(404, "Student not found")

    if data.name is not None:
        student.name = data.name
    if data.age is not None:
        student.age = data.age
    if data.grade is not None:
        student.grade = data.grade

    db.commit()
    db.refresh(student)
    return student

def delete_student(db: Session, student_id: int):
    student = get_student(db, student_id)
    if not student:
        raise HTTPException(404, "Student not found")

    db.delete(student)
    db.commit()
    return True
