from datetime import date
from typing import List, Optional
from pydantic import BaseModel, Field


class LineItem(BaseModel):
    description: str = Field(
        ..., 
        description="Description of the item or service purchased"
    )
    quantity: Optional[float] = Field(
        default=1.0, 
        description="Quantity of the item purchased, defaults to 1.0 if not specified"
    )
    unit_price: Optional[float] = Field(
        default=None, 
        description="Price per single unit if available"
    )
    total_price: float = Field(
        ..., 
        description="Total cost for this line item"
    )


class ReceiptData(BaseModel):
    merchant_name: str = Field(
        ..., 
        description="Name of the business or merchant issuing the receipt"
    )
    transaction_date: Optional[date] = Field(
        default=None, 
        description="Date of transaction formatted as YYYY-MM-DD"
    )
    line_items: List[LineItem] = Field(
        default_factory=list, 
        description="List of purchased line items extracted from the receipt"
    )
    subtotal: Optional[float] = Field(
        default=None, 
        description="Subtotal before tax/tip"
    )
    tax_amount: Optional[float] = Field(
        default=0.0, 
        description="Total tax applied"
    )
    tip_amount: Optional[float] = Field(
        default=0.0, 
        description="Tip or gratuity amount, defaults to 0.0"
    )
    total_amount: float = Field(
        ..., 
        description="Final total amount paid"
    )
    currency: str = Field(
        default="USD", 
        description="3-letter ISO currency code e.g PKR, USD"
    )


if __name__ == "__main__":
    # Local quick sanity check to verify JSON Schema generation
    import json
    print(json.dumps(ReceiptData.model_json_schema(), indent=2))