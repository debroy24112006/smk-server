from flask import Blueprint, request, jsonify

from firebaseSetup import db

coupon_bp = Blueprint(
    "coupon_bp",
    __name__
)

# CREATE COUPON
@coupon_bp.route(
    "/create-coupon",
    methods=["POST"]
)
def create_coupon():

    try:

        data = request.get_json()

        coupon = {
            "code":
                data.get("code"),

            "discount":
                data.get("discount"),

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
            "error": str(e)
        }), 500


# CLAIM COUPON
@coupon_bp.route(
    "/claim-coupon",
    methods=["POST"]
)
def claim_coupon():

    try:

        data = request.get_json()

        code = data.get("code")

        user_id = data.get("user_id")

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

        # CHECK CLAIMED
        if user_id in coupon_data.get(
            "claimed_users",
            []
        ):

            return jsonify({
                "success": False,
                "message":
                    "Coupon already claimed"
            }), 400

        claimed_users = coupon_data.get(
            "claimed_users",
            []
        )

        claimed_users.append(
            user_id
        )

        db.collection(
            "Coupons"
        ).document(
            coupon_doc.id
        ).update({
            "claimed_users":
                claimed_users
        })

        return jsonify({
            "success": True,
            "discount":
                coupon_data.get(
                    "discount"
                )
        })

    except Exception as e:

        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


# GET COUPONS
@coupon_bp.route(
    "/get-coupons",
    methods=["GET"]
)
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
            "data": coupons
        })

    except Exception as e:

        return jsonify({
            "success": False,
            "error": str(e)
        }), 500