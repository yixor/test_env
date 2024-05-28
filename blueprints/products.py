from flask import Blueprint, Response, request
import orjson
from caching.redis_connect import Cache
from models.tables import Product, Review
from sqlalchemy.orm import Session
from db import pg_engine
from settings import REVIEWS_PER_PAGE
from utils.responses import JSONResponse

product_bp = Blueprint('product', __name__)


@product_bp.route('/<int:id>', methods=['GET'])
def get_product(id: int):
    reviews_page = request.args.get("page", type=int)
    if reviews_page and reviews_page > 1:
        offset = (reviews_page - 1) * REVIEWS_PER_PAGE
    else:
        offset = 0
        reviews_page = 1

    url = f"product/{id}/"
    cache = Cache()
    cached_page = cache.get_page(url=url, page=reviews_page)
    if cached_page:
        return JSONResponse(response=cached_page)

    with Session(pg_engine) as s:
        product = s.query(Product).\
            filter(Product.id == id).\
            one_or_none()
        if product:
            reviews = s.query(Review).\
                filter(Review.asin == product.asin).\
                limit(REVIEWS_PER_PAGE).offset(offset).all()
            product_dict = product.to_dict()
            product_dict["reviewsPage"] = reviews_page
            product_dict["reviewsCount"] = len(reviews)
            product_dict["reviews"] = [review.to_dict()
                                       for review in reviews]
            product_json = orjson.dumps(product_dict)
            cache.cache_page(url=url,
                             content=product_json,
                             page=reviews_page)
            return JSONResponse(product_json)
        return Response(response="Not found", status=404)
