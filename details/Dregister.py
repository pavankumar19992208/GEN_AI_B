from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict
from db import get_database
from bson import ObjectId

# Pydantic model for request payload
class DeveloperDetailsCreate(BaseModel):
    name: str
    email: str
    password: str

class DeveloperDetailsSignin(BaseModel):
    email: str
    password: str

class StudentDetails(BaseModel):
    email: str
    id: str
    name: str
    password: str

class CodeSubmission(BaseModel):
    studentDetails: StudentDetails
    topic: str
    subTopic: str
    title: str
    code: str
    language: str

class IDRequest(BaseModel):
    id: str

Dregister_router = APIRouter()
db = get_database()

@Dregister_router.post("/dregister")
async def create_developer_details(details: DeveloperDetailsCreate):
    try:
        # Check if email already exists
        existing_user = await db.developerdetails.find_one({"email": details.email})
        if existing_user:
            return {"message": "Email already registered"}

        # Create new developer details
        developer_data = {
            "_id": ObjectId(),
            "name": details.name,
            "email": details.email,
            "password": details.password
        }
        result = await db.developerdetails.insert_one(developer_data)
        return {"message": "You have been registered successfully", "id": str(result.inserted_id)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {e}")

@Dregister_router.post("/dsignin")
async def signin_developer(details: DeveloperDetailsSignin):
    try:
        # Validate email and password
        user = await db.developerdetails.find_one({"email": details.email, "password": details.password})
        if not user:
            raise HTTPException(status_code=401, detail="Invalid credentials")

        # Return the user details
        user_details = {
            "id": str(user["_id"]),
            "name": user["name"],
            "email": user["email"],
            "password": user["password"]
        }
        return user_details
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {e}")

@Dregister_router.post("/api/addresult")
async def add_code_submission(submission: CodeSubmission):
    try:
        # Check if the student email exists in developerdetails
        student = await db.developerdetails.find_one({"email": submission.studentDetails.email})
        if not student:
            raise HTTPException(status_code=404, detail="Student not found")

        # Check if a code submission already exists for the student
        existing_submission = await db.codesubmissions.find_one({"student_id": student["_id"]})
        if existing_submission:
            # Update the existing submission with the new problem statement
            update_result = await db.codesubmissions.update_one(
                {"student_id": student["_id"]},
                {"$push": {
                    "submissions": {
                        "_id": ObjectId(),
                        "topic": submission.topic,
                        "subTopic": submission.subTopic,
                        "title": submission.title,
                        "code": submission.code,
                        "language": submission.language
                    }
                }}
            )
            if update_result.modified_count == 1:
                return {"message": "Code submission updated successfully"}
            else:
                raise HTTPException(status_code=500, detail="Failed to update code submission")
        else:
            # Create a new code submission document
            code_submission_data = {
                "_id": ObjectId(),
                "student_id": student["_id"],
                "submissions": [{
                    "_id": ObjectId(),
                    "topic": submission.topic,
                    "subTopic": submission.subTopic,
                    "title": submission.title,
                    "code": submission.code,
                    "language": submission.language
                }]
            }
            result = await db.codesubmissions.insert_one(code_submission_data)
            return {"message": "Code submission successful", "id": str(result.inserted_id)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {e}")

@Dregister_router.post("/api/getCodeSubmissions")
async def get_code_submissions(request: IDRequest):
    try:
        # Check if the student ID exists in developerdetails
        student = await db.developerdetails.find_one({"_id": ObjectId(request.id)})
        if not student:
            raise HTTPException(status_code=404, detail="Student not found")

        # Get the code submissions for the student
        submissions = await db.codesubmissions.find_one({"student_id": student["_id"]})
        if not submissions:
            return {"submissions": []}

        # Convert ObjectId to string
        for submission in submissions["submissions"]:
            submission["_id"] = str(submission["_id"])

        return {"submissions": submissions["submissions"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {e}")