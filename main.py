from flask import Flask
from blueprints import product_bp, review_bp
import preprocess
from settings import APP_HOST, APP_PORT
app = Flask(__name__)

app.register_blueprint(product_bp, url_prefix="/product")
app.register_blueprint(review_bp, url_prefix="/review")


if __name__ == "__main__":
    app.run(host=APP_HOST,
            port=APP_PORT)
