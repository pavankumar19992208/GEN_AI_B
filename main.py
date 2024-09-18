from fastapi import FastAPI, APIRouter, HTTPException, Request
from GEN_AI.assist import assist_router
import os
from web.ps_update import ps_update_router
from web.getList import get_list_router
from web.psdetails import ps_details_router
from fastapi.middleware.cors import CORSMiddleware
from details.Dregister import Dregister_router
app = FastAPI(docs_url="/docs")
from runtests.runtests_router import runtests_router

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




@app.get("/")
def read_root():
    return {"Hello": "World"}



app.include_router(runtests_router)
app.include_router(ps_update_router)
app.include_router(get_list_router)
app.include_router(ps_details_router)
app.include_router(Dregister_router)
app.include_router(assist_router)