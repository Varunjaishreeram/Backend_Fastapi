from fastapi import APIRouter, HTTPException
from bson import ObjectId
from app.models import Student, StudentUpdate
from app.database import get_collection

router = APIRouter()
students_collection = get_collection("students")

@router.post("/students", status_code=201)
async def create_student(student:Student):
    student_dict = student.dict()
    result = students_collection.insert_one(student_dict)
    return {"id": str(result.inserted_id)}

@router.get("/students")
async def list_students(country: str = None, age: int = None):
    query = {}
    if country:
        query["address.country"] = country
    if age:
        query["age"] = {"$gte": age}
    students = students_collection.find(query)
    print(students,"hello")
        
    return {"data": [{"name": s["name"], "_id": str(s["_id"]) , "age": s["age"], "address": s["address"]} for s in students]}

@router.get("/students/{id}")
async def get_student(id: str):
    student = students_collection.find_one({"_id": ObjectId(id)})
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return {
        "name": student["name"],
        "age": student["age"],
        "address": student["address"]
    }

@router.patch("/students/{id}")
async def update_student(id: str, student: StudentUpdate):
    
    update_data = {}
    for key, value in student.dict().items():
        if value is not None:
            update_data[key] = value


    result = students_collection.update_one({"_id": ObjectId(id)}, {"$set": update_data})
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Student not found")
    return {"detail": "Student updated successfully"}

@router.delete("/students/{id}")
async def delete_student(id: str):
    result = students_collection.delete_one({"_id": ObjectId(id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Student not found")
    return {"detail": "Student deleted successfully"}
