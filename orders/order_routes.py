from flask import Blueprint, request, jsonify

from firebaseSetup import db

from datetime import datetime

order_bp = Blueprint(
    "order_bp",
    __name__
)

# PLACE ORDER
@order_bp.route(
    "/place-order",
    methods=["POST"]
)
def place_order():

    try:

        data = request.get_json()

        order = {
            "user_id":
                data.get("user_id"),

            "products":
                data.get("products"),

            "total":
                data.get("total"),

            "address":
                data.get("address"),

            "payment_method":
                data.get("payment_method"),

            "status":
                "Pending",

            "created_at":
                datetime.utcnow()
                .isoformat()
        }

        doc_ref = db.collection(
            "Orders"
        ).add(order)

        return jsonify({
            "success": True,
            "message":
                "Order placed successfully",
            "id":
                doc_ref[1].id
        }), 201

    except Exception as e:

        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


# GET ALL ORDERS
@order_bp.route(
    "/get-orders",
    methods=["GET"]
)
def get_orders():

    try:

        docs = db.collection(
            "Orders"
        ).stream()

        orders = []

        for doc in docs:

            item = doc.to_dict()

            item["id"] = doc.id

            orders.append(item)

        return jsonify({
            "success": True,
            "data": orders
        }), 200

    except Exception as e:

        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


# UPDATE ORDER STATUS
@order_bp.route(
    "/update-order/<id>",
    methods=["PUT"]
)
def update_order(id):

    try:

        data = request.get_json()

        ref = db.collection(
            "Orders"
        ).document(id)

        ref.update({
            "status":
                data.get("status")
        })

        return jsonify({
            "success": True,
            "message":
                "Order updated"
        })

    except Exception as e:

        return jsonify({
            "success": False,
            "error": str(e)
        }), 500