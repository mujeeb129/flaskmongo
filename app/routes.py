from flask import jsonify, request, abort

import jwt
from datetime import datetime, timedelta

from app import products, db, logger, users
from app.authentication import authenticate, create_token


@products.route("/", methods=["GET"])
@authenticate
def products_list():
    products = db.products
    products_list = list(
        products.find(
            {},
        )
    )
    logger.info("products_list: %s", products_list)
    return jsonify({"products": products_list})


@products.route("/", methods=["POST"])
def product_create():
    try:
        products_collection = db.products
        data = request.get_json()
        data["_id"] = (
            products_collection.count_documents({})
            if products_collection.count_documents({})
            else 1
        )
        products_collection.insert_one(data)
        db.client.close()
        return jsonify({"message": "product created"}), 201
    except Exception as e:
        logger.error("Error: %s", str(e))
        return jsonify({"message": f"something went wrong: {str(e)}"}), 500


@products.route("/<product_id>", methods=["GET"])
def get_product(product_id):
    products_collection = db.products
    product = products_collection.find_one({"_id": int(product_id)}, {"_id": 0})
    if product:
        db.client.close()
        return jsonify({"product": product})
    return jsonify({"message": "product not found"}), 404


@products.route("/<product_id>", methods=["PUT", "PATCH"])
def update_product(product_id):
    try:
        products_collection = db.products
        data = request.get_json()
        products_collection.update_one({"_id": int(product_id)}, {"$set": data})
        return jsonify({"message": "product updated"}), 200
    except Exception as e:
        logger.error(f"Caught an exception: {str(e)}")
        return jsonify({"message": f"Caught an exception: {str(e)}"}), 500
    

@products.route("/<product_id>", methods=["DELETE"])
def delete_product(product_id):
    try:
        products_collection = db.products
        products_collection.delete_one({"_id": int(product_id)})
        return jsonify({"message": "product deleted"}), 200
    except Exception as e:
        logger.error(f"Caught an exception: {str(e)}")
        return jsonify({"message": f"Caught an exception: {str(e)}"}), 500
    

@users.route("/login", methods=["GET"])
def login():
    data = request.json
    try:
        user_collection = db.user
        user = user_collection.find_one({"username": data["username"]})
        if user and user["password"] == data["password"]:
            success, access_token = create_token(user)
            if success:
                return jsonify({"message": "Login successful", "data": access_token}), 200
            return jsonify({"message": f"something went wrong: {str(access_token)}"}), 500
        return abort(401, description="Invalid credentials")
    
    except Exception as e:
        return jsonify({"message": f"something went wrong: {str(e)}"}), 500
    

@users.route("/register", methods=["POST"])
def register():
    data = request.json
    try:
        user_collection = db.user
        user = user_collection.find_one({"username": data["username"]})
        if user:
            return abort(409, description="Username already exists")
        user_id = user_collection.count_documents({}) + 1
        user_details = {
            "_id": user_id,
            "username": data["username"],
            "password": data["password"],
            "user_role": data["user_role"],
            "is_active": True,
            "orders": [],
            "wishlist": [],
        }
        user_collection.insert_one(user_details)
        success, tokens = create_token(user_details)
        if success:
            return jsonify({"message": "User created", "data": {"user"}}), 201
        abort(500, description=f"Something went wrong: {tokens}")

    except Exception as e:
        return abort(500, description=str(e))
    