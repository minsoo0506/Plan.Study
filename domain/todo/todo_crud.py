from datetime import datetime

from domain.todo.todo_schema import TodoCreate, TodoUpdate
from models import Todo, User
from sqlalchemy import asc, desc, func
from sqlalchemy.orm import Session


def get_todo_list(db: Session, skip: int = 0, limit: int = 10, keyword: str = ''):
    todo_list = db.query(Todo)
    if keyword:
        search = '%%{}%%'.format(keyword)
        todo_list = todo_list \
            .outerjoin(User) \
            .filter(Todo.subject.ilike(search) |  # 질문제목
                    Todo.content.ilike(search) |  # 질문내용
                    User.username.ilike(search)  # 작성자(삭제 예정)
                    )
    total = todo_list.distinct().count()
    todo_list = todo_list.order_by(asc(Todo.completed), desc(Todo.create_date)) \
        .offset(skip).limit(limit).distinct().all() # desc : 내림차순 정렬
    return total, todo_list  # (페이징 적용된 질문 목록, 전체 건수)


def get_todo(db: Session, todo_id: int):
    todo = db.query(Todo).get(todo_id)
    return todo

def get_todos_by_user_id(db: Session, user_id: int):
    return db.query(Todo).filter(Todo.user_id == user_id).all()

def get_user_ranking(db: Session, user_id: int):
    # Get the count of todos for all users
    all_users_todo_count = db.query(User.id, func.count(Todo.id)).join(Todo).group_by(User.id).all()
    # Sort the counts in descending order
    sorted_todo_counts = sorted(all_users_todo_count, key=lambda x: x[1], reverse=True)
    # Find the rank of the current user
    user_rank = [index for index, user in enumerate(sorted_todo_counts) if user[0] == user_id][0] + 1
    return user_rank

def create_todo(db: Session, todo_create: TodoCreate, user: User):
    db_todo = Todo(subject=todo_create.subject,
                   content=todo_create.content,
                   create_date=datetime.now(),
                   user=user,
                   category=todo_create.category)
    db.add(db_todo)
    db.commit()


def update_todo(db: Session, db_todo: Todo, todo_update: TodoUpdate):
    db_todo.subject = todo_update.subject
    db_todo.content = todo_update.content
    db_todo.modify_date = datetime.now()
    db_todo.category = todo_update.category
    db.add(db_todo)
    db.commit()

def update_todo_completed(db: Session, todo_id: int, completed: bool):
    db_todo = db.query(Todo).get(todo_id)
    if db_todo is not None:
        db_todo.completed = completed
        db.commit()

def delete_todo(db: Session, db_todo: Todo):
    db.delete(db_todo)
    db.commit()
