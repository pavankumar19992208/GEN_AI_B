from fastapi import APIRouter, HTTPException
from db import get_database
from bson import ObjectId
import logging

get_list_router = APIRouter()
db = get_database()

@get_list_router.get("/api/getList")
async def get_data():
    try:
        # Fetch all topics with their subtopics
        topics_cursor = db.data.find({}, {"topic": 1, "subTopics.subTopic": 1})
        topics = await topics_cursor.to_list(length=None)
        
        # Format the data
        formatted_data = {}
        for topic in topics:
            topic_name = topic["topic"]
            subtopics = [subtopic["subTopic"] for subtopic in topic.get("subTopics", [])]
            formatted_data[topic_name] = subtopics
        return formatted_data
    except Exception as e:
        logging.error(f"Error in get_data: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@get_list_router.get("/api/getFullList")
async def get_full_list():
    try:
        # Fetch all topics with their subtopics and problem statements
        topics_cursor = db.data.find({}, {"topic": 1, "subTopics": 1})
        topics = await topics_cursor.to_list(length=None)
        
        # Format the data
        formatted_data = {}
        for topic in topics:
            topic_name = topic["topic"]
            subtopics = []
            for subtopic in topic.get("subTopics", []):
                subtopic_info = {
                    "subTopic": subtopic["subTopic"],
                    "problemStatements": [
                        {
                            "id": str(problem["_id"]),
                            "title": problem.get("problemStatementTitle", "No Title"),
                            "problemStatement": problem.get("problemStatement", "No Problem Statement"),
                            "code": problem.get("code", {}),
                            "testCases": problem.get("testCases", [])
                        }
                        for problem in subtopic.get("problemStatements", [])
                    ]
                }
                subtopics.append(subtopic_info)
            formatted_data[topic_name] = subtopics
        return formatted_data
    except Exception as e:
        logging.error(f"Error in get_full_list: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")