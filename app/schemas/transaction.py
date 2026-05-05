from pydantic import BaseModel

class Transaction(BaseModel):
    amount: float
    description: str