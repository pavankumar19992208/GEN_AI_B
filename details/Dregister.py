from pydantic import BaseModel
from db import get_db
from fastapi import APIRouter, HTTPException
import mysql.connector
from mysql.connector import Error

# Pydantic model for request payload
class DeveloperDetailsCreate(BaseModel):
    name: str
    email: str
    password: str

class DeveloperDetailsSignin(BaseModel):
    email: str
    password: str

Dregister_router = APIRouter()

@Dregister_router.post("/dregister")
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
                password VARCHAR(255) NOT NULL
            )
        """)

        # Check if email already exists
        cursor.execute("SELECT * FROM developerdetails WHERE email = %s", (details.email,))
        existing_user = cursor.fetchone()
        if existing_user:
            return {"message": "Email already registered"}

        # Create new developer details
        cursor.execute(
            "INSERT INTO developerdetails (name, email, password) VALUES (%s, %s, %s)",
            (details.name, details.email, details.password)
        )
        connection.commit()
        return {"message": "you have been registered successfully"}
    except Error as e:
        connection.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {e}")
    finally:
        cursor.close()
        connection.close()

@Dregister_router.post("/dsignin")
async def signin_developer(details: DeveloperDetailsSignin):
    connection = get_db()
    if not connection:
        raise HTTPException(status_code=500, detail="Database connection failed")

    cursor = connection.cursor()
    try:
        # Validate email and password
        cursor.execute("SELECT * FROM developerdetails WHERE email = %s AND password = %s", (details.email, details.password))
        user = cursor.fetchone()
        if not user:
            raise HTTPException(status_code=401, detail="Invalid credentials")

        # Return the user details
        user_details = {
            "id": user[0],
            "name": user[1],
            "email": user[2],
            "password": user[3]
        }
        return user_details
    except Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")
    finally:
        cursor.close()
        connection.close()