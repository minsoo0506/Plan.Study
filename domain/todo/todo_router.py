from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from database import get_db
from domain.todo import todo_schema, todo_crud
from domain.user.user_router import get_current_user
from models import User

router = APIRouter(
    prefix="/api/todo",
)

@router.get("/list", response_model=todo_schema.TodoList)
def todo_list(db: Session = Depends(get_db), page: int = 0, size: int = 10, keyword: str = ''):
    total, _todo_list = todo_crud.get_todo_list(
        db, skip=page * size, limit=size, keyword=keyword)
    return {
        'total': total,
        'todo_list': _todo_list
    }

@router.get("/detail/{todo_id}", response_model=todo_schema.Todo)
def todo_detail(todo_id: int, db: Session = Depends(get_db)):
    todo = todo_crud.get_todo(db, todo_id=todo_id)
    return todo

@router.get("/user-data/{username}")
def get_user_data(username: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    todos = todo_crud.get_todos_by_user_id(db, user.id)
    total_list_count = len(todos)
    completed_count = sum(1 for todo in todos if todo.completed)
    completion_rate = completed_count / total_list_count * 100 if total_list_count > 0 else 0
    category_counts = {}
    for todo in todos:
        if todo.category in category_counts:
            category_counts[todo.category] += 1
        else:
            category_counts[todo.category] = 1
    user_rank = todo_crud.get_user_ranking(db, user.id)
    return {
        'username': user.username,
        'userId': user.id,
        'totalListCount': total_list_count,
        'completionRate': completion_rate,
        'categoryCounts': category_counts,
        'userRank': user_rank,
    }

@router.post("/create", status_code=status.HTTP_204_NO_CONTENT)
def todo_create(_todo_create: todo_schema.TodoCreate,
                db: Session = Depends(get_db),
                current_user: User = Depends(get_current_user)):
    todo_crud.create_todo(db=db, todo_create=_todo_create, user=current_user)


@router.put("/update", status_code=status.HTTP_204_NO_CONTENT)
def todo_update(_todo_update: todo_schema.TodoUpdate,
                db: Session = Depends(get_db),
                current_user: User = Depends(get_current_user)):
    db_todo = todo_crud.get_todo(db, todo_id=_todo_update.todo_id)
    if not db_todo:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="데이터를 찾을수 없습니다.")
    if current_user.id != db_todo.user.id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="수정 권한이 없습니다.")
    todo_crud.update_todo(db=db, db_todo=db_todo,todo_update=_todo_update)

@router.put("/update_completed", status_code=status.HTTP_204_NO_CONTENT)
def update_completed(_todo_update_completed: todo_schema.TodoUpdateCompleted,
                     db: Session = Depends(get_db),
                     current_user: User = Depends(get_current_user)):
    db_todo = todo_crud.get_todo(db, todo_id=_todo_update_completed.todo_id)
    if not db_todo:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="데이터를 찾을수 없습니다.")
    if current_user.id != db_todo.user.id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="수정 권한이 없습니다.")
    todo_crud.update_todo_completed(db=db, todo_id=_todo_update_completed.todo_id, completed=_todo_update_completed.completed)


@router.delete("/delete", status_code=status.HTTP_204_NO_CONTENT)
def todo_delete(_todo_delete: todo_schema.TodoDelete,
                db: Session = Depends(get_db),
                current_user: User = Depends(get_current_user)):
    db_todo = todo_crud.get_todo(db, todo_id=_todo_delete.todo_id)
    if not db_todo:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="데이터를 찾을수 없습니다.")
    if current_user.id != db_todo.user.id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="삭제 권한이 없습니다.")
    todo_crud.delete_todo(db=db, db_todo=db_todo)
