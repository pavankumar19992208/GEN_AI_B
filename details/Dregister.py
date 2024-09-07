from pydantic import BaseModel
from db import get_db
from fastapi import APIRouter, HTTPException
import mysql.connector
from mysql.connector import Error
# Pydantic model for request payload
class DeveloperDetailsCreate(BaseModel):
    name: str
    email: str
    mobile: str
    password: str

Dregister_router = APIRouter()

@Dregister_router.post("/api/developerdetails")
async def create_developer_details(details: DeveloperDetailsCreate):
    connection = get_db()
    if not connection:
        raise HTTPException(status_code=500, detail="Database connection failed")

    cursor = connection.cursor()
    try:
        # Create table if it doesn't exist
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS developerdetails (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                email VARCHAR(255) NOT NULL UNIQUE,
                mobile VARCHAR(255) NOT NULL UNIQUE,
                password VARCHAR(255) NOT NULL
            )
        """)

        # Check if email or mobile already exists
        cursor.execute("SELECT * FROM developerdetails WHERE email = %s OR mobile = %s", (details.email, details.mobile))
        existing_user = cursor.fetchone()
        if existing_user:
            print("Email or mobile already registered")
            return {"message": "Email or mobile already registered"}

        # Create new developer details
        cursor.execute(
            "INSERT INTO developerdetails (name, email, mobile, password) VALUES (%s, %s, %s, %s)",
            (details.name, details.email, details.mobile, details.password)
        )
        connection.commit()
        return {"message": "Developer details created successfully"}
    except Error as e:
        connection.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {e}")
    finally:
        cursor.close()
        connection.close()