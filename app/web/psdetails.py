from fastapi import APIRouter, HTTPException, Body
from db import get_database
from bson import ObjectId

ps_details_router = APIRouter()
db = get_database()

@ps_details_router.post("/api/psDetails")
async def get_ps_details(id: str = Body(..., embed=True)):
    print(id)
    print("hello")
    try:
        # Fetch the problem statement details by ID
        problem_statement = await db.data.find_one(
            {"subTopics.problemStatements._id": ObjectId(id)},
            {"subTopics.problemStatements.$": 1}
        )
        
        if not problem_statement:
            raise HTTPException(status_code=404, detail="Problem statement not found")
        
        # Extract the problem statement details
        for subtopic in problem_statement.get("subTopics", []):
            for problem in subtopic.get("problemStatements", []):
                if str(problem["_id"]) == id:
                    return {
                        "title": problem["problemStatementTitle"],
                        "problemStatement": problem["problemStatement"],
                        "code": problem["code"],
                        "testCases": problem["testCases"]
                    }
        
        raise HTTPException(status_code=404, detail="Problem statement not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")