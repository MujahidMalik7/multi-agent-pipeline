from fastapi import FastAPI
from graph import pipeline
from pydantic import BaseModel

class ArticleRequest(BaseModel):
    topic: str

app = FastAPI()

@app.post("/generate-article")
def generate_article(request: ArticleRequest):
    result = pipeline.invoke(
        {
            "topic": request.topic,
            "research": None,
            "outline": None,
            "draft": None,
            "decision": None,
            "reason": None,
            "revision_count": 0
        }

    )
    return {
        "article": result["draft"]
    }