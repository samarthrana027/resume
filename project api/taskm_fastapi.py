from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from enum import Enum
from datetime import date

app = FastAPI(title="Task Manager API")

# -----------------------------
# ENUMS
# -----------------------------

class Priority(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"

class Status(str, Enum):
    pending = "pending"
    in_progress = "in_progress"
    done = "done"

# -----------------------------
# DATA MODEL
# -----------------------------

class Task(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    due_date: date
    priority: Priority
    status: Status

# -----------------------------
# DATABASE (Temporary Storage)
# -----------------------------

tasks: List[Task] = []

# -----------------------------
# CREATE TASK
# -----------------------------

@app.post("/tasks/", response_model=Task)
def create_task(task: Task):

    for t in tasks:
        if t.id == task.id:
            raise HTTPException(
                status_code=400,
                detail="Task with this ID already exists"
            )

    tasks.append(task)

    return task

# -----------------------------
# READ ALL TASKS
# -----------------------------

@app.get("/tasks/", response_model=List[Task])
def get_tasks():

    return tasks

# -----------------------------
# READ SINGLE TASK
# -----------------------------

@app.get("/tasks/{task_id}", response_model=Task)
def get_task(task_id: int):

    for task in tasks:
        if task.id == task_id:
            return task

    raise HTTPException(
        status_code=404,
        detail="Task not found"
    )

# -----------------------------
# UPDATE TASK
# -----------------------------

@app.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: int, updated_task: Task):

    for index, task in enumerate(tasks):

        if task.id == task_id:

            tasks[index] = updated_task

            return updated_task

    raise HTTPException(
        status_code=404,
        detail="Task not found"
    )

# -----------------------------
# DELETE TASK
# -----------------------------

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):

    for index, task in enumerate(tasks):

        if task.id == task_id:

            deleted_task = tasks.pop(index)

            return {
                "message": "Task deleted successfully",
                "task": deleted_task
            }

    raise HTTPException(
        status_code=404,
        detail="Task not found"
    )