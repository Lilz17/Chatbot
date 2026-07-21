from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.templating import Jinja2Templates

from chatbot import answer_question

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html"
    )

@app.get("/chat")
async def chat(question: str):
    #answer = answer_question(question)
    #return {"answer": answer}
    
    # stream chunks
    return StreamingResponse(answer_question(question), media_type="text/event-stream")
