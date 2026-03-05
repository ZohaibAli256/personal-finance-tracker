from datetime import date, datetime
from enum import Enum

from pydantic import BaseModel, Field


class TransactionType(str, Enum):
    income = "income"
    expense = "expense"


class CategoryType(str, Enum):
    food = "food"
    transport = "transport"
    shopping = "shopping"
    bills = "bills"
    salary = "salary"
    freelance = "freelance"
    entertainment = "entertainment"
    health = "health"
    education = "education"
    other = "other"


class TransactionCreate(BaseModel):
    description: str = Field(..., min_length=1, max_length=255)
    amount: float = Field(..., gt=0)
    type: TransactionType
    category: CategoryType
    date: date


class TransactionResponse(BaseModel):
    id: int
    description: str
    amount: float
    type: TransactionType
    category: CategoryType
    date: date
    created_at: datetime

    model_config = {"from_attributes": True}


class CategoryBreakdown(BaseModel):
    category: str
    total: float


class SummaryResponse(BaseModel):
    total_income: float
    total_expenses: float
    balance: float
    category_breakdown: list[CategoryBreakdown]
