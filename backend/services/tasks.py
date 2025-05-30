from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError, NoResultFound
from uuid import UUID
from models.tasks import Task
from schemas.tasks import TaskCreate, TaskUpdate, TaskResponse
from datetime import datetime, timezone

class TaskService:

    @staticmethod
    async def create_task(db: AsyncSession, task_data: TaskCreate) -> TaskResponse:
        
        new_task = Task(
            title=task_data.title,
            description=task_data.description,
            status=task_data.status.value,
            due_date=task_data.due_date,
        )

        db.add(new_task)
        await db.commit()
        await db.refresh(new_task)
        return new_task.to_dict()

    @staticmethod
    async def get_all_tasks(db: AsyncSession) -> list[TaskResponse]:
        result = await db.execute(select(Task))
        tasks = result.scalars().all()
        return [task.to_dict() for task in tasks]

    @staticmethod
    async def get_task_by_id(db: AsyncSession, task_id: UUID) -> TaskResponse:
        result = await db.execute(select(Task).filter(Task.id == str(task_id)))
        print(result,'++++++++++++++++')
        task = result.scalar_one_or_none()
        if not task:
            raise ValueError(f"Task with id {task_id} not found")
        return task.to_dict()

    @staticmethod
    async def update_task_status(db: AsyncSession, task_id: UUID, status_update: TaskUpdate) -> TaskResponse:
        result = await db.execute(select(Task).filter(Task.id == str(task_id)))
        task = result.scalar_one_or_none()
        if not task:
            raise ValueError(f"Task with id {task_id} not found")

        task.status = status_update.status.value
        task.updated_at = datetime.now(timezone.utc)
        db.add(task)
        await db.commit()
        await db.refresh(task)
        return task.to_dict()

    @staticmethod
    async def delete_task(db: AsyncSession, task_id: UUID) -> None:
        result = await db.execute(select(Task).filter(Task.id == str(task_id)))
        task = result.scalar_one_or_none()
        if not task:
            raise ValueError(f"Task with id {task_id} not found")
        await db.delete(task)
        await db.commit()
