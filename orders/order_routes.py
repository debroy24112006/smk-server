from flask import (
    Blueprint,
    request,
    jsonify
)

from firebaseSetup import db

from datetime import datetime

from middleware.admin_auth import (
    admin_required
)

order_bp = Blueprint(
    "order_bp",
    __name__
)

# =========================================
# PLACE ORDER
# =========================================
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

            "coupon":
                data.get("coupon"),

            "discount":
                data.get("discount"),

            "status":
                "Pending",

            "created_at":
                datetime.utcnow()
                .isoformat()
        }

        doc_ref = db.collection(
            "Orders"
        ).add(order)

        order_id = (
            doc_ref[1].id
        )

        return jsonify({

            "success": True,

            "message":
                "Order placed successfully",

            "id":
                order_id

        }), 201

    except Exception as e:

        return jsonify({

            "success": False,

            "error":
                str(e)

        }), 500


# =========================================
# GET ALL ORDERS
# =========================================
@order_bp.route(
    "/get-orders",
    methods=["GET"]
)
@admin_required
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

        # LATEST FIRST
        orders.sort(

            key=lambda x:
                x.get(
                    "created_at",
                    ""
                ),

            reverse=True
        )

        return jsonify({

            "success": True,

            "data":
                orders

        }), 200

    except Exception as e:

        return jsonify({

            "success": False,

            "error":
                str(e)

        }), 500


# =========================================
# GET USER ORDERS
# =========================================
@order_bp.route(
    "/get-user-orders/<user_id>",
    methods=["GET"]
)
def get_user_orders(user_id):

    try:

        docs = db.collection(
            "Orders"
        ).where(
            "user_id",
            "==",
            user_id
        ).stream()

        orders = []

        for doc in docs:

            item = doc.to_dict()

            item["id"] = doc.id

            orders.append(item)

        orders.sort(

            key=lambda x:
                x.get(
                    "created_at",
                    ""
                ),

            reverse=True
        )

        return jsonify({

            "success": True,

            "data":
                orders

        })

    except Exception as e:

        return jsonify({

            "success": False,

            "error":
                str(e)

        }), 500


# =========================================
# UPDATE ORDER STATUS
# =========================================
@order_bp.route(
    "/update-order/<id>",
    methods=["PUT"]
)
@admin_required
def update_order(id):

    try:

        data = request.get_json()

        status = data.get(
            "status"
        )

        ref = db.collection(
            "Orders"
        ).document(id)

        # CHECK ORDER EXISTS
        if not ref.get().exists:

            return jsonify({

                "success": False,

                "message":
                    "Order not found"

            }), 404

        # UPDATE STATUS
        ref.update({

            "status":
                status
        })

        return jsonify({

            "success": True,

            "message":
                "Order updated successfully"

        })

    except Exception as e:

        return jsonify({

            "success": False,

            "error":
                str(e)

        }), 500


# =========================================
# DELETE ORDER
# =========================================
@order_bp.route(
    "/delete-order/<id>",
    methods=["DELETE"]
)
@admin_required
def delete_order(id):

    try:

        ref = db.collection(
            "Orders"
        ).document(id)

        if not ref.get().exists:

            return jsonify({

                "success": False,

                "message":
                    "Order not found"

            }), 404

        ref.delete()

        return jsonify({

            "success": True,

            "message":
                "Order deleted"

        })

    except Exception as e:

        return jsonify({

            "success": False,

            "error":
                str(e)

        }), 500