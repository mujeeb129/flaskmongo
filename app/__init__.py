import logging

from flask import Flask, Blueprint

from .mongo import MongoDB
from .settings import BaseConfig

app = Flask(__name__)
app.config.from_object(BaseConfig)
logger = logging.getLogger("my_logger")
logger.setLevel(logging.INFO)
log_format = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
log_file = "app.log"
file_handler = logging.FileHandler(log_file)
file_handler.setFormatter(log_format)
logger.addHandler(file_handler)

mongo_client = MongoDB("shop")
db = mongo_client.db

products = Blueprint("products", __name__, url_prefix="/products")
users = Blueprint("users", __name__, url_prefix="/users")

from app import routes


app.register_blueprint(products)
app.register_blueprint(users)
