from pydantic import BaseModel

# ---------- USER ----------
class UserCreate(BaseModel):
    email: str
    password: str

class UserOut(BaseModel):
    id: int
    email: str

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str


# ---------- STUDENTS ----------
class StudentBase(BaseModel):
    name: str
    age: int
    grade: str

class StudentCreate(StudentBase):
    pass

class StudentUpdate(BaseModel):
    name: str | None = None
    age: int | None = None
    grade: str | None = None

class StudentOut(StudentBase):
    id: int

    class Config:
        orm_mode = True
