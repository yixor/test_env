from flask import Blueprint, Response, request
from caching.redis_connect import Cache
from models.payloads import ReviewPayload
from models.tables import Review
from db import pg_engine
from sqlalchemy.orm import Session

review_bp = Blueprint('review', __name__)


@review_bp.route('/add', methods=['POST'])
def add_review():
    try:
        payload = ReviewPayload(**request.get_json())
        with Session(pg_engine) as s:
            review_obj = Review(asin=payload.asin,
                                title=payload.title,
                                review=payload.review)
            s.add(review_obj)
            s.commit()
        Cache().flush_cache(f"product/{payload.product_id}/")
        return Response(status=201)
    except Exception as e:
        return Response(response=f"Error: {e}",
                        status=400)
