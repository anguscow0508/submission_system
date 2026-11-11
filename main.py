
from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates

app = FastAPI()

templates = Jinja2Templates(directory="templates")


@app.get("/")
def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html"
    )

@app.get("/author")
def author_page(request: Request):

    articles = [
        {
            "category": "科技",
            "title": "人工智慧的發展",
            "status": "編輯中"
        },
        {
            "category": "生活",
            "title": "我的大學生活",
            "status": "審查中"
        },
        {
            "category": "教育",
            "title": "未來的學習方式",
            "status": "已通過"
        }
    ]

    return templates.TemplateResponse(
        request=request,
        name="author.html",
        context={"articles": articles}
    )
# 顯示新增投稿頁面
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

