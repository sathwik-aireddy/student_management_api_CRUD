from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, EmailStr, Field


app = FastAPI()



#  Response Model

class Student(BaseModel):
    id: int
    name: str 
    email: EmailStr
    course: str
    age: int



# Student Request Model


class StudentCreate(BaseModel):
    id:int
    name: str
    email: EmailStr
    course: str
    age: int


students = []

next_id = 1

# CREATE STUDENT


@app.post(
    "/students",
    response_model=Student,
    status_code=status.HTTP_201_CREATED
)
def create_student(student: StudentCreate):

    global next_id

    # Check if email already exists
    for existing_student in students:
        if existing_student["email"].lower() == student.email.lower():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Student with this email already exists"
            )

    # Create new student
    new_student = {
        "id": next_id,
        "name": student.name,
        "email": student.email,
        "course": student.course,
        "age": student.age
    }

    students.append(new_student)

    next_id += 1

    return new_student

#  GET ALL STUDENTS

@app.get(
    "/students",
    response_model=list[Student],
    status_code=status.HTTP_200_OK
)
def get_students():

    return students


# GET STUDENT BY ID

@app.get(
    "/students/{student_id}",
    response_model=Student,
    status_code=status.HTTP_200_OK
)
def get_student(student_id: int):

    for student in students:

        if student["id"] == student_id:
            return student

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Student not found"
    )


# UPDATE STUDENT

@app.put(
    "/students/{student_id}",
    response_model=Student,
    status_code=status.HTTP_200_OK
)
def update_student(
    student_id: int,
    student: StudentCreate
):

    for index, existing_student in enumerate(students):

        if existing_student["id"] == student_id:

            updated_student = {
                "id": student_id,
                "name": student.name,
                "email": student.email,
                "course": student.course,
                "age": student.age
            }

            students[index] = updated_student

            return updated_student

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Student not found"
    )


#delete student 

@app.delete(
    "/students/{student_id}",
    status_code=status.HTTP_200_OK
)
def delete_student(student_id: int):

    for index, student in enumerate(students):

        if student["id"] == student_id:

            students.pop(index)

            return {
                "message": "Student deleted successfully"
            }

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Student not found"
    )



#  SEARCH STUDENTS BY COURSE


@app.get(
    "/students/search",
    response_model=list[Student],
    status_code=status.HTTP_200_OK
)
def search_students(course: str):

    results = []

    for student in students:

        if course.lower() in student["course"].lower():
            results.append(student)

    return results