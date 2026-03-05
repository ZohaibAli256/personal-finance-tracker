from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import func
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Transaction
from ..schemas import (
    CategoryBreakdown,
    CategoryType,
    SummaryResponse,
    TransactionCreate,
    TransactionResponse,
    TransactionType,
)

router = APIRouter()


@router.get("/transactions", response_model=list[TransactionResponse])
def list_transactions(
    type: TransactionType | None = Query(None),
    category: CategoryType | None = Query(None),
    search: str | None = Query(None),
    db: Session = Depends(get_db),
):
    query = db.query(Transaction)

    if type is not None:
        query = query.filter(Transaction.type == type.value)
    if category is not None:
        query = query.filter(Transaction.category == category.value)
    if search:
        query = query.filter(Transaction.description.ilike(f"%{search}%"))

    return query.order_by(Transaction.date.desc(), Transaction.id.desc()).all()


@router.post(
    "/transactions", response_model=TransactionResponse, status_code=201
)
def create_transaction(data: TransactionCreate, db: Session = Depends(get_db)):
    transaction = Transaction(
        description=data.description,
        amount=data.amount,
        type=data.type.value,
        category=data.category.value,
        date=data.date,
    )
    db.add(transaction)
    db.commit()
    db.refresh(transaction)
    return transaction


@router.get("/transactions/{transaction_id}", response_model=TransactionResponse)
def get_transaction(transaction_id: int, db: Session = Depends(get_db)):
    transaction = db.query(Transaction).filter(Transaction.id == transaction_id).first()
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return transaction


@router.put("/transactions/{transaction_id}", response_model=TransactionResponse)
def update_transaction(
    transaction_id: int, data: TransactionCreate, db: Session = Depends(get_db)
):
    transaction = db.query(Transaction).filter(Transaction.id == transaction_id).first()
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")

    transaction.description = data.description
    transaction.amount = data.amount
    transaction.type = data.type.value
    transaction.category = data.category.value
    transaction.date = data.date

    db.commit()
    db.refresh(transaction)
    return transaction


@router.delete("/transactions/{transaction_id}", status_code=204)
def delete_transaction(transaction_id: int, db: Session = Depends(get_db)):
    transaction = db.query(Transaction).filter(Transaction.id == transaction_id).first()
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")

    db.delete(transaction)
    db.commit()


@router.get("/summary", response_model=SummaryResponse)
def get_summary(db: Session = Depends(get_db)):
    total_income = (
        db.query(func.coalesce(func.sum(Transaction.amount), 0.0))
        .filter(Transaction.type == "income")
        .scalar()
    )
    total_expenses = (
        db.query(func.coalesce(func.sum(Transaction.amount), 0.0))
        .filter(Transaction.type == "expense")
        .scalar()
    )

    breakdown_rows = (
        db.query(Transaction.category, func.sum(Transaction.amount))
        .group_by(Transaction.category)
        .all()
    )
    category_breakdown = [
        CategoryBreakdown(category=row[0], total=row[1]) for row in breakdown_rows
    ]

    return SummaryResponse(
        total_income=total_income,
        total_expenses=total_expenses,
        balance=total_income - total_expenses,
        category_breakdown=category_breakdown,
    )
