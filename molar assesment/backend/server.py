from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from simple_nl2sql import question_to_sql
from db import run_readonly_sql

app = FastAPI(title="GenAI E-commerce Chat Demo")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class AskBody(BaseModel):
    question: str

@app.post("/ask")
def ask(body: AskBody):
    sql = question_to_sql(body.question)
    data = run_readonly_sql(sql)
    return {"sql": sql, "data": data}
