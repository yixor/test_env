from typing import Optional
from pydantic import (
    BaseModel,
    Field,
    model_validator
)
from sqlalchemy.orm import Session
from db import pg_engine
from .tables import Product


class ReviewPayload(BaseModel):
    asin: str = Field(...)
    product_id: Optional[str] = None

    @model_validator(mode='after')
    def validate_asin(self):
        with Session(pg_engine) as session:
            result = session.query(Product).\
                filter_by(asin=self.asin).first()
        if not result:
            raise Exception(
                "The given value 'asin' does not exist."
            )
        self.product_id = result.id

    title: str = Field(min_length=5, max_length=64)
    review: str = Field(...)
