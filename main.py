from fastapi import FastAPI
from search_util import search_collocation

app = FastAPI()

@app.get("/search")
async def search(word: str, limit: int = None):
    return search_collocation(word, limit)

@app.get("/")
async def health_check():
    return {}
