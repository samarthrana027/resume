from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from datetime import date
from enum import Enum

app = FastAPI(title="Task Manager API")

class Priority(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"

class Status(str, Enum):
    pending = "pending"
    in_progress = "in_progress"
    done = "done"

class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    priority: Priority = Priority.medium
    due_date: Optional[date] = None

class Task(TaskCreate):
    id: int
    status: Status = Status.pending

tasks_db: dict = {}
counter = 1

@app.get("/tasks", response_model=List[Task])
def get_tasks(status: Optional[Status] = None, priority: Optional[Priority] = None):
    tasks = list(tasks_db.values())
    if status: tasks = [t for t in tasks if t.status == status]
    if priority: tasks = [t for t in tasks if t.priority == priority]
    return tasks

@app.post("/tasks", response_model=Task, status_code=201)
def create_task(data: TaskCreate):
    global counter
    task = Task(id=counter, **data.dict())
    tasks_db[counter] = task
    counter += 1
    return task

@app.patch("/tasks/{task_id}/status")
def update_status(task_id: int, status: Status):
    if task_id not in tasks_db:
        raise HTTPException(status_code=404, detail="Task not found")
    tasks_db[task_id].status = status
    return tasks_db[task_id]

@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int):
    if task_id not in tasks_db:
        raise HTTPException(status_code=404, detail="Task not found")
    del tasks_db[task_id]