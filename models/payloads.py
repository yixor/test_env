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
    asin: Optional[str] = None
    product_id: Optional[int] = None

    @model_validator(mode='after')
    def validate_asin(self):
        if self.asin == None:
            with Session(pg_engine) as session:
                result = session.query(Product).\
                    filter(Product.id == self.product_id).one_or_none()
            if not result:
                raise Exception(
                    "The given value Product 'id' does not exist."
                )
            self.asin = result.asin
    title: str = Field(min_length=5, max_length=64)
    review: str = Field(...)
