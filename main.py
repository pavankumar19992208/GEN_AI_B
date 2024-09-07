from fastapi import FastAPI, APIRouter, HTTPException, Request
import google.generativeai as genai
import os
from fastapi import FastAPI, APIRouter
from web.ps_update import ps_update_router
from web.getList import get_list_router
from web.psdetails import ps_details_router
from fastapi.middleware.cors import CORSMiddleware
from details.Dregister import Dregister_router
app = FastAPI(docs_url="/docs")
from runtests.runtests_router import runtests_router
from content_generator import generate_content
origins = [
    "*",  # Allow all origins
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allow specific origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)



assist_router = APIRouter()
@app.get("/")
def read_root():
    return {"Hello": "World"}

@assist_router.post("/assist")
async def assist(request: Request):
    try:
        # Get the data from the request
        data = await request.json()
        code = data.get("code")
        problem_statement = data.get("problemStatement")
        error = data.get("results")  # Assuming 'results' contains error information

        # Prepare the prompt for the Gemini API
        prompt = f"Code: {code}\nProblem Statement: {problem_statement}\nError: {error}\n"

        # Use the Gemini API to generate content
        response_text = generate_content(prompt)
        print(response_text)
        # Return the response from the Gemini API to the frontend
        return {"response": response_text}
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

app.include_router(runtests_router)
app.include_router(ps_update_router)
app.include_router(get_list_router)
app.include_router(ps_details_router)
app.include_router(Dregister_router)
app.include_router(assist_router)