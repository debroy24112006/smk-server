from flask import (
    Blueprint,
    request,
    jsonify
)

from firebaseSetup import db

from middleware.admin_auth import (
    admin_required
)

coupon_bp = Blueprint(
    "coupon_bp",
    __name__
)

# =========================================
# CREATE COUPON
# =========================================
@coupon_bp.route(
    "/create-coupon",
    methods=["POST"]
)
@admin_required
def create_coupon():

    try:

        data = request.get_json()

        code = (
            data.get("code", "")
            .strip()
            .upper()
        )

        # CHECK EXISTING
        existing = db.collection(
            "Coupons"
        ).where(
            "code",
            "==",
            code
        ).stream()

        for item in existing:

            return jsonify({

                "success": False,

                "message":
                    "Coupon already exists"

            }), 400

        coupon = {

            "code":
                code,

            # FLAT AMOUNT
            "discount":
                int(
                    data.get(
                        "discount",
                        0
                    )
                ),

            "expiry":
                data.get("expiry"),

            "usage_limit":
                data.get(
                    "usage_limit",
                    "unlimited"
                ),

            "status":
                data.get(
                    "status",
                    "Active"
                ),

            # USER CLAIM TRACK
            "claimed_users":
                []
        }

        db.collection(
            "Coupons"
        ).add(coupon)

        return jsonify({

            "success": True,

            "message":
                "Coupon created"

        })

    except Exception as e:

        return jsonify({

            "success": False,

            "error":
                str(e)

        }), 500


# =========================================
# CLAIM COUPON
# =========================================
@coupon_bp.route(
    "/claim-coupon",
    methods=["POST"]
)
def claim_coupon():

    try:

        data = request.get_json()

        coupon_id = data.get(
            "coupon_id"
        )

        user_id = data.get(
            "user_id"
        )

        coupon_ref = db.collection(
            "Coupons"
        ).document(
            coupon_id
        )

        coupon_doc = (
            coupon_ref.get()
        )

        if not coupon_doc.exists:

            return jsonify({

                "success": False,

                "message":
                    "Coupon not found"

            }), 404

        coupon_data = (
            coupon_doc.to_dict()
        )

        claimed_users = coupon_data.get(
            "claimed_users",
            []
        )

        # PREVENT DUPLICATE
        if user_id not in claimed_users:

            claimed_users.append(
                user_id
            )

            coupon_ref.update({

                "claimed_users":
                    claimed_users
            })

        return jsonify({

            "success": True,

            "message":
                "Coupon claimed"

        })

    except Exception as e:

        return jsonify({

            "success": False,

            "error":
                str(e)

        }), 500


# =========================================
# VALIDATE COUPON
# =========================================
@coupon_bp.route(
    "/validate-coupon",
    methods=["POST"]
)
def validate_coupon():

    try:

        data = request.get_json()

        code = (
            data.get("code", "")
            .strip()
            .upper()
        )

        user_id = data.get(
            "user_id"
        )

        docs = db.collection(
            "Coupons"
        ).where(
            "code",
            "==",
            code
        ).stream()

        coupon_doc = None

        for doc in docs:

            coupon_doc = doc

        if not coupon_doc:

            return jsonify({

                "success": False,

                "message":
                    "Coupon not found"

            }), 404

        coupon_data = (
            coupon_doc.to_dict()
        )

        # STATUS CHECK
        if coupon_data.get(
            "status"
        ) != "Active":

            return jsonify({

                "success": False,

                "message":
                    "Coupon inactive"

            }), 400

        claimed_users = coupon_data.get(
            "claimed_users",
            []
        )

        # CHECK USER
        if user_id in claimed_users:

            return jsonify({

                "success": False,

                "message":
                    "Coupon already used"

            }), 400

        return jsonify({

            "success": True,

            "discount":
                coupon_data.get(
                    "discount"
                ),

            "coupon_id":
                coupon_doc.id

        })

    except Exception as e:

        return jsonify({

            "success": False,

            "error":
                str(e)

        }), 500


# =========================================
# GET COUPONS
# =========================================
@coupon_bp.route(
    "/get-coupons",
    methods=["GET"]
)
@admin_required
def get_coupons():

    try:

        docs = db.collection(
            "Coupons"
        ).stream()

        coupons = []

        for doc in docs:

            item = doc.to_dict()

            item["id"] = doc.id

            coupons.append(item)

        return jsonify({

            "success": True,

            "data":
                coupons

        })

    except Exception as e:

        return jsonify({

            "success": False,

            "error":
                str(e)

        }), 500


# =========================================
# DELETE COUPON
# =========================================
@coupon_bp.route(
    "/delete-coupon/<id>",
    methods=["DELETE"]
)
@admin_required
def delete_coupon(id):

    try:

        db.collection(
            "Coupons"
        ).document(id).delete()

        return jsonify({

            "success": True,

            "message":
                "Coupon deleted"

        })

    except Exception as e:

        return jsonify({

            "success": False,

            "error":
                str(e)

        }), 500