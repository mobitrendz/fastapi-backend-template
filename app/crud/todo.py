import uuid

from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.models.todo import (
    ToDoList,
    ToDoListCreate,
    ToDoListsPublic,
    ToDoListUpdate,
)
from app.models.user import User, UserRole


async def create_todo(
    *, session: AsyncSession, todo_create: ToDoListCreate, current_user: User
) -> ToDoList:
    todo = ToDoList.model_validate(todo_create, update={"user_id": current_user.id})
    session.add(todo)
    await session.commit()
    await session.refresh(todo)
    return todo


async def get_todos(
    *,
    session: AsyncSession,
    current_user: User,
) -> ToDoListsPublic:
    statement = select(ToDoList)
    if current_user.role != UserRole.ADMIN:
        statement = statement.where(ToDoList.user_id == current_user.id)

    result = await session.execute(statement)
    todos = result.scalars().all()
    return ToDoListsPublic(data=todos, count=len(todos))


async def get_todo_by_id(
    *, session: AsyncSession, id: uuid.UUID, current_user: User
) -> ToDoList | None:
    todo = await session.get(ToDoList, id)
    if not todo:
        return None
    if current_user.role != UserRole.ADMIN and todo.user_id != current_user.id:
        return None
    return todo


async def update_todo(
    *,
    session: AsyncSession,
    id: uuid.UUID,
    todo_update: ToDoListUpdate,
    current_user: User,
) -> ToDoList | None:
    todo = await get_todo_by_id(session=session, id=id, current_user=current_user)
    if not todo:
        return None

    update_data = todo_update.model_dump(exclude_unset=True)
    todo.sqlmodel_update(update_data)
    session.add(todo)
    await session.commit()
    await session.refresh(todo)
    return todo


async def delete_todo(
    *, session: AsyncSession, id: uuid.UUID, current_user: User
) -> bool:
    todo = await get_todo_by_id(session=session, id=id, current_user=current_user)
    if not todo:
        return False

    await session.delete(todo)
    await session.commit()
    return True
