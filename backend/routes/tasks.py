from fastapi import APIRouter, Depends
from schemas.tasks import TaskCreate, TaskResponse, TaskUpdate
from services.tasks import TaskService, AsyncSession
from core.database import get_db1
from core.utils.response import Response
from uuid import UUID
from models.tasks import List  # assuming your status enum is here

router = APIRouter()


@router.post("/tasks/", response_model=TaskResponse)
async def create_task_route(task: TaskCreate, db: AsyncSession = Depends(get_db1)):
    try:
        # Call the service to create the task
        result = await TaskService.create_task(db=db, task_data=task)
        return Response(data=result, message="Task created successfully", code=201)
    except Exception as e:
        # If something goes wrong, return an error response
        return Response(message="Failed to create task", error=str(e), code=500)


@router.get("/tasks/", response_model=List[TaskResponse])
async def get_all_tasks_route(db: AsyncSession = Depends(get_db1)):
    try:
        # Call the service to get all tasks with pagination
        tasks = await TaskService.get_all_tasks(db)
        return Response(data=tasks, message="Tasks fetched successfully", code=200)
    except Exception as e:
        # Handle any errors while fetching tasks
        return Response(message="Failed to fetch tasks", error=str(e), code=500)


@router.get("/tasks/{task_id}", response_model=TaskResponse)
async def get_task_by_id_route(task_id: UUID, db: AsyncSession = Depends(get_db1)):
    try:
        # Call the service to fetch a task by its ID
        result = await TaskService.get_task_by_id(db=db, task_id=task_id)
        if not result:
            # Return 404 if the task is not found
            return Response(message="Task not found", code=404)
        return Response(data=result, message="Task fetched successfully", code=200)
    except Exception as e:
        # Handle errors while fetching the task
        return Response(message="Failed to fetch task", error=str(e), code=500)

@router.put("/tasks/{task_id}/status", response_model=Response)
async def update_task_status_route(task_id: UUID, task_update: TaskUpdate, db: AsyncSession = Depends(get_db1)):
    try:
        # Call the service to update the task protection status
        result = await TaskService.update_task_status(db=db, task_id=task_id, status_update=task_update)
        return Response(data=result, message="Task status updated successfully", code=200)
    except Exception as e:
        # Handle exceptions during the update process
        return Response(message="Failed to update Task status", error=str(e), code=500)


@router.delete("/tasks/{task_id}", response_model=Response)
async def delete_task_by_id(task_id: UUID, db: AsyncSession = Depends(get_db1)):
    try:
        result = await TaskService.get_task_by_id(db=db, task_id=task_id)
        if not result:
            # Return 404 if the task is not found
            return Response(message="Task not found", error="Task with the provided ID doesn't exist", code=404)
        # Call the service to delete the task by its ID
        result = await TaskService.delete_task(db=db, task_id=task_id)
        
        return Response(message="Task deleted successfully", code=200)
    except Exception as e:
        # Handle errors during the deletion process
        return Response(message="Failed to delete task", error=str(e), code=500)
