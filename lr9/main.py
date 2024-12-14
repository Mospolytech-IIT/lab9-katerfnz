'''Маршруты'''

from fastapi import FastAPI, Depends, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from database import SessionLocal
import crud
from models import User, Post

app = FastAPI()

# Подключение шаблонов и статических файлов
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


def get_db():
    '''получение сессии с БД'''
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/users/", response_class=HTMLResponse)
def list_users(request: Request, db: Session = Depends(get_db)):
    '''Список пользователей'''
    users = crud.get_users(db)
    return templates.TemplateResponse("users/list.html", {"request": request, "users": users})


@app.get("/users/create/", response_class=HTMLResponse)
def create_user_form(request: Request):
    '''Форма создания пользователя'''
    return templates.TemplateResponse("users/create.html", {"request": request})


@app.post("/users/create/")
def create_user(db: Session = Depends(get_db), username: str = Form(...), email: str = Form(...), password: str = Form(...)):
    '''Обработка создания пользователя'''
    crud.create_user(db, username=username, email=email, password=password)
    return RedirectResponse(url="/users/", status_code=303)


@app.get("/users/edit/{user_id}", response_class=HTMLResponse)
def edit_user_form(request: Request, user_id: int, db: Session = Depends(get_db)):
    '''Форма редактирования пользователя'''
    user = db.query(User).filter(User.id == user_id).first()
    return templates.TemplateResponse("users/edit.html", {"request": request, "user": user})


@app.post("/users/edit/{user_id}")
def edit_user(user_id: int, db: Session = Depends(get_db), username: str = Form(...), email: str = Form(...)):
    '''Обработка редактирования пользователя'''
    crud.update_user_email(db, user_id=user_id, new_email=email)
    return RedirectResponse(url="/users/", status_code=303)


@app.post("/users/delete/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    '''Удаление пользователя'''
    crud.delete_user_and_posts(db, user_id=user_id)
    return RedirectResponse(url="/users/", status_code=303)


@app.get("/posts/", response_class=HTMLResponse)
def list_posts(request: Request, db: Session = Depends(get_db)):
    '''Список постов'''
    posts = crud.get_posts(db)
    return templates.TemplateResponse("posts/list.html", {"request": request, "posts": posts})


@app.get("/posts/create/", response_class=HTMLResponse)
def create_post_form(request: Request):
    '''Форма создания поста'''
    return templates.TemplateResponse("posts/create.html", {"request": request})


@app.post("/posts/create/")
def create_post(
    db: Session = Depends(get_db),
    title: str = Form(...),
    content: str = Form(...),
    user_id: int = Form(...),
):
    '''Обработка создания поста'''
    crud.create_post(db, title=title, content=content, user_id=user_id)
    return RedirectResponse(url="/posts/", status_code=303)


@app.get("/posts/edit/{post_id}", response_class=HTMLResponse)
def edit_post_form(request: Request, post_id: int, db: Session = Depends(get_db)):
    '''Форма редактирования поста'''
    post = db.query(Post).filter(Post.id == post_id).first()
    return templates.TemplateResponse("posts/edit.html", {"request": request, "post": post})


@app.post("/posts/edit/{post_id}")
def edit_post(
    post_id: int,
    db: Session = Depends(get_db),
    title: str = Form(...),
    content: str = Form(...),
):
    '''Обработка редактирования поста'''
    crud.update_post_content(db, post_id=post_id, new_content=content)
    return RedirectResponse(url="/posts/", status_code=303)


@app.post("/posts/delete/{post_id}")
def delete_post(post_id: int, db: Session = Depends(get_db)):
    '''Удаление поста'''
    crud.delete_post(db, post_id=post_id)
    return RedirectResponse(url="/posts/", status_code=303)


@app.get("/users/{user_id}/posts", response_class=HTMLResponse)
def list_user_posts(user_id: int, request: Request, db: Session = Depends(get_db)):
    '''Поиск постов пользователя'''
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return templates.TemplateResponse("404.html", {"request": request, "message": "User not found"})

    posts = crud.get_user_posts(db, user_id=user_id)
    return templates.TemplateResponse("posts/user_posts.html", {"request": request, "user": user, "posts": posts})
