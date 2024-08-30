from fastapi import APIRouter, HTTPException, Body
from pydantic import BaseModel
import subprocess
import json

runtests_router = APIRouter()

class TestCase(BaseModel):
    input: str
    expectedOutput: str

class CodePayload(BaseModel):
    code: str
    language: str
    testCases: list[TestCase]

@runtests_router.post("/api/runTests")
async def run_tests(payload: CodePayload):
    try:
        if payload.language == "python":
            from .run_python import run_code
        elif payload.language == "java":
            print("java")
            from .run_java import run_code
        elif payload.language == "javascript":
            print("javascript")
            from .run_javascript import run_code
        elif payload.language == "c":
            from .run_c import run_code
        elif payload.language == "cpp":
            from .run_cpp import run_code
        else:
            raise HTTPException(status_code=400, detail="Unsupported language")

        results = run_code(payload.code, payload.testCases)
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))