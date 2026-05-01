from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from enum import Enum

app = FastAPI(title="Employee Management System API")

# -----------------------------
# ENUM FOR DEPARTMENT
# -----------------------------

class Department(str, Enum):
    hr = "HR"
    it = "IT"
    finance = "Finance"
    marketing = "Marketing"

# -----------------------------
# DATA MODEL
# -----------------------------

class Employee(BaseModel):
    id: int
    name: str
    age: int
    department: Department
    salary: float
    is_active: Optional[bool] = True

# -----------------------------
# TEMPORARY DATABASE
# -----------------------------

employees: List[Employee] = []

# -----------------------------
# CREATE EMPLOYEE
# -----------------------------

@app.post("/employees/", response_model=Employee)
def create_employee(employee: Employee):

    for emp in employees:
        if emp.id == employee.id:
            raise HTTPException(
                status_code=400,
                detail="Employee with this ID already exists"
            )

    employees.append(employee)

    return employee


# -----------------------------
# READ ALL EMPLOYEES
# -----------------------------

@app.get("/employees/", response_model=List[Employee])
def get_employees():

    return employees


# -----------------------------
# READ SINGLE EMPLOYEE
# -----------------------------

@app.get("/employees/{employee_id}", response_model=Employee)
def get_employee(employee_id: int):

    for emp in employees:
        if emp.id == employee_id:
            return emp

    raise HTTPException(
        status_code=404,
        detail="Employee not found"
    )


# -----------------------------
# UPDATE EMPLOYEE
# -----------------------------

@app.put("/employees/{employee_id}", response_model=Employee)
def update_employee(employee_id: int, updated_employee: Employee):

    for index, emp in enumerate(employees):

        if emp.id == employee_id:

            employees[index] = updated_employee

            return updated_employee

    raise HTTPException(
        status_code=404,
        detail="Employee not found"
    )


# -----------------------------
# DELETE EMPLOYEE
# -----------------------------

@app.delete("/employees/{employee_id}")
def delete_employee(employee_id: int):

    for index, emp in enumerate(employees):

        if emp.id == employee_id:

            deleted_employee = employees.pop(index)

            return {
                "message": "Employee deleted successfully",
                "employee": deleted_employee
            }

    raise HTTPException(
        status_code=404,
        detail="Employee not found"
    )