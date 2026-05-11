import uuid

from fastapi import APIRouter, HTTPException

from app.api.deps import AllowTodo, CurrentUser
from app.crud import todo as todo_crud
from app.db.database import SessionDependency
from app.models.generic import Message
from app.models.todo import (
    ToDoListCreate,
    ToDoListPublic,
    ToDoListsPublic,
    ToDoListUpdate,
)

router = APIRouter()


@router.post("/", response_model=ToDoListPublic)
async def create_todo(
    session: SessionDependency,
    _allow_todo: AllowTodo,
    current_user: CurrentUser,
    todo_create: ToDoListCreate,
) -> ToDoListPublic:
    todo = await todo_crud.create_todo(
        session=session, todo_create=todo_create, current_user=current_user
    )
    return ToDoListPublic.model_validate(todo)


@router.get("/", response_model=ToDoListsPublic)
async def read_todos(
    session: SessionDependency,
    _allow_todo: AllowTodo,
    current_user: CurrentUser,
) -> ToDoListsPublic:
    return await todo_crud.get_todos(session=session, current_user=current_user)


@router.get("/{id}", response_model=ToDoListPublic)
async def read_todo_by_id(
    session: SessionDependency,
    _allow_todo: AllowTodo,
    current_user: CurrentUser,
    id: uuid.UUID,
) -> ToDoListPublic:
    todo = await todo_crud.get_todo_by_id(
        session=session, id=id, current_user=current_user
    )
    if not todo:
        raise HTTPException(status_code=404, detail="ToDo not found")
    return ToDoListPublic.model_validate(todo)


@router.patch("/{id}", response_model=ToDoListPublic)
async def update_todo(
    session: SessionDependency,
    _allow_todo: AllowTodo,
    current_user: CurrentUser,
    id: uuid.UUID,
    todo_update: ToDoListUpdate,
) -> ToDoListPublic:
    todo = await todo_crud.update_todo(
        session=session,
        id=id,
        todo_update=todo_update,
        current_user=current_user,
    )
    if not todo:
        raise HTTPException(status_code=404, detail="ToDo not found")
    return ToDoListPublic.model_validate(todo)


@router.delete("/{id}", response_model=Message)
async def delete_todo(
    session: SessionDependency,
    _allow_todo: AllowTodo,
    current_user: CurrentUser,
    id: uuid.UUID,
) -> Message:
    deleted = await todo_crud.delete_todo(
        session=session, id=id, current_user=current_user
    )
    if not deleted:
        raise HTTPException(status_code=404, detail="ToDo not found")

    return Message(message="ToDo deleted successfully")
