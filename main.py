
from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
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


# 顯示新增投稿頁面
@app.get("/author/add")
def add_article_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="article_form.html"
    )


# 接收新增投稿表單

@app.post("/author/add")
def add_article(
    category: str = Form(...),
    title: str = Form(...),
    content: str = Form(...)
):

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO articles
                (author_id, category, title, content)
                VALUES (%s, %s, %s, %s)
            """, (1, category, title, content))

        conn.commit()

    return RedirectResponse(
        url="/author",
        status_code=303
    )

# 顯示編輯投稿頁面
@app.get("/author/edit/{article_id}")
def edit_article_page(request: Request, article_id: int):

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT id, category, title, content, status
                FROM articles
                WHERE id = %s
                  AND author_id = %s
                  AND status = '編輯中'
            """, (article_id, 1))

            article = cur.fetchone()

    if article is None:
        return {"message": "找不到可編輯的文章"}

    return templates.TemplateResponse(
        request=request,
        name="article_edit.html",
        context={"article": article}
    )

# 儲存編輯後的投稿資料
@app.post("/author/edit/{article_id}")
def edit_article(
    article_id: int,
    category: str = Form(...),
    title: str = Form(...),
    content: str = Form(...)
):

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                UPDATE articles
                SET category = %s,
                    title = %s,
                    content = %s
                WHERE id = %s
                  AND author_id = %s
                  AND status = '編輯中'
            """, (category, title, content, article_id, 1))

            updated_count = cur.rowcount

        conn.commit()

    if updated_count == 0:
        return {"message": "文章不存在或目前無法修改"}

    return RedirectResponse(
        url="/author",
        status_code=303
    )

# 刪除編輯中的投稿
@app.post("/author/delete/{article_id}")
def delete_article(article_id: int):

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                DELETE FROM articles
                WHERE id = %s
                  AND author_id = %s
                  AND status = '編輯中'
            """, (article_id, 1))

            deleted_count = cur.rowcount

        conn.commit()

    if deleted_count == 0:
        return {"message": "文章不存在或目前無法刪除"}

    return RedirectResponse(
        url="/author",
        status_code=303
    )

# 作者送出投稿
@app.post("/author/submit/{article_id}")
def submit_article(article_id: int):

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                UPDATE articles
                SET status = '審查中'
                WHERE id = %s
                  AND author_id = %s
                  AND status = '編輯中'
            """, (article_id, 1))

            updated_count = cur.rowcount

        conn.commit()

    if updated_count == 0:
        return {"message": "文章不存在或無法送出投稿"}

    return RedirectResponse(
        url="/author",
        status_code=303
    )
