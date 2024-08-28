from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict
from db import get_database
from bson import ObjectId

ps_update_router = APIRouter()
db = get_database()

class DataModel(BaseModel):
    topic: str
    subTopic: str
    problemStatement: str
    code: Dict[str, str]
    testCases: List[Dict[str, str]]

@ps_update_router.post("/api/saveData")
async def save_data(data: DataModel):
    try:
        # Check if the topic exists
        topic_doc = await db.data.find_one({"topic": data.topic})
        
        if topic_doc:
            # Check if the subTopic exists under the topic
            sub_topic_doc = await db.data.find_one({"topic": data.topic, "subTopics.subTopic": data.subTopic})
            
            if sub_topic_doc:
                # Insert problemStatement, code, testCases under the existing subTopic
                update_result = await db.data.update_one(
                    {"_id": sub_topic_doc["_id"], "subTopics.subTopic": data.subTopic},
                    {"$push": {
                        "subTopics.$.problemStatements": {
                            "_id": ObjectId(),
                            "problemStatement": data.problemStatement,
                            "code": data.code,
                            "testCases": data.testCases
                        }
                    }}
                )
                if update_result.modified_count == 1:
                    return {"message": "Data updated successfully"}
                else:
                    raise HTTPException(status_code=500, detail="Failed to update data")
            else:
                # Insert new subTopic under the existing topic
                new_sub_topic = {
                    "_id": ObjectId(),
                    "subTopic": data.subTopic,
                    "problemStatements": [{
                        "_id": ObjectId(),
                        "problemStatement": data.problemStatement,
                        "code": data.code,
                        "testCases": data.testCases
                    }]
                }
                update_result = await db.data.update_one(
                    {"_id": topic_doc["_id"]},
                    {"$push": {"subTopics": new_sub_topic}}
                )
                if update_result.modified_count == 1:
                    return {"message": "SubTopic added successfully"}
                else:
                    raise HTTPException(status_code=500, detail="Failed to add subTopic")
        else:
            # Insert new topic with subTopic
            new_topic = {
                "_id": ObjectId(),
                "topic": data.topic,
                "subTopics": [{
                    "_id": ObjectId(),
                    "subTopic": data.subTopic,
                    "problemStatements": [{
                        "_id": ObjectId(),
                        "problemStatement": data.problemStatement,
                        "code": data.code,
                        "testCases": data.testCases
                    }]
                }]
            }
            result = await db.data.insert_one(new_topic)
            return {"message": "Topic and SubTopic added successfully", "id": str(result.inserted_id)}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")