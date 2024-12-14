'''файл с функциями для добавления данных'''

from sqlalchemy.orm import Session
from models import User, Post


def create_user(db: Session, username: str, email: str, password: str):
    '''Добавление нового пользователя'''
    user = User(username=username, email=email, password=password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def create_post(db: Session, title: str, content: str, user_id: int):
    '''Добавление нового поста'''
    post = Post(title=title, content=content, user_id=user_id)
    db.add(post)
    db.commit()
    db.refresh(post)
    return post


def get_users(db: Session):
    '''Получение всех пользователей'''
    return db.query(User).all()


def get_posts(db: Session):
    '''Получение всех постов'''
    return db.query(Post).all()


def get_user_posts(db: Session, user_id: int):
    '''Получение постов конкретного пользователя'''
    return db.query(Post).filter(Post.user_id == user_id).all()


def update_user_email(db: Session, user_id: int, new_email: str):
    '''Обновление email пользователя'''
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        user.email = new_email
        db.commit()
        db.refresh(user)
    return user


def update_post_content(db: Session, post_id: int, new_content: str):
    '''Обновление контента поста'''
    post = db.query(Post).filter(Post.id == post_id).first()
    if post:
        post.content = new_content
        db.commit()
        db.refresh(post)
    return post


def delete_post(db: Session, post_id: int):
    '''Удаление поста'''
    post = db.query(Post).filter(Post.id == post_id).first()
    if post:
        db.delete(post)
        db.commit()


def delete_user_and_posts(db: Session, user_id: int):
    '''Удаление пользователя и его постов'''
    db.query(Post).filter(Post.user_id == user_id).delete()
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        db.delete(user)
        db.commit()
