
from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from db import get_connection

app = FastAPI()

templates = Jinja2Templates(directory="templates")


# 首頁
@app.get("/")
def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html"
    )


# 作者投稿清單
@app.get("/author")
def author_page(request: Request):

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT id, category, title, status
                FROM articles
                WHERE author_id = %s
                ORDER BY id DESC
            """, (1,))

            articles = cur.fetchall()

    return templates.TemplateResponse(
        request=request,
        name="author.html",
        context={"articles": articles}
    )


# 顯示新增投稿表單
@app.get("/author/add")
def add_article_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="article_form.html"
    )


# 接收新增投稿資料
@app.post("/author/add")
def add_article(
    category: str = Form(...),
    title: str = Form(...),
    content: str = Form(...)
):
    return {
        "message": "成功接收到投稿資料",
        "category": category,
        "title": title,
        "content": content,
        "status": "編輯中"
    }
