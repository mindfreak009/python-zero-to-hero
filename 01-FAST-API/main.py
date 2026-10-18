from fastapi import FastAPI
from pydantic import BaseModel, Field 
from contextlib import asynccontextmanager

import db

# @app.on_event("startup")
# def init_logic():

@asynccontextmanager   #converts the async generator into an asynchronous context manager.
async def lifespan(app: FastAPI):
    db.create_table();  # Runs when the application starts
    yield

app = FastAPI(lifespan=lifespan)
base_path = "/api"


# @app.get("/welcome")
# def get_welcome_msg():
#     return {
#         "message": "Welcome to FAST API !"
#     }

# @app.get("/greet")
# def get_greet_msg():
#     return {
#         "message": "Good evening"
#     }


class Student(BaseModel):
    name: str = Field(..., min_length=3, max_length=25)
    course: str = Field(..., min_length=3, max_length=25)
    fee: float = Field(..., gt=0)


@app.post(f"{base_path}/student", status_code=201)
def create_student(student: Student):
    return db.insert_student(student)


@app.get(f"{base_path}/students")
def get_all_students():
    return db.get_all_students()


@app.get(f"{base_path}/students/{{student_id}}")
def get_student_by_id(student_id: int):
    return db.get_student_by_id(student_id)


@app.put(f"{base_path}/student/{{student_id}}/update")
def update_student(student_id: int, student: Student):
    return db.update_student(student_id, student)


@app.delete(f"{base_path}/students/{{student_id}}")
def delete_student_by_id(student_id: int):
    return db.delete_student_by_id(student_id)