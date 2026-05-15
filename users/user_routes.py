from flask import Blueprint, request, jsonify

from firebaseSetup import db

user_bp = Blueprint(
    "user_bp",
    __name__
)

# CREATE USER
@user_bp.route(
    "/create-user",
    methods=["POST"]
)
def create_user():

    try:

        data = request.get_json()

        user = {
            "name":
                data.get("name"),

            "email":
                data.get("email"),

            "phone":
                data.get("phone"),

            "photo":
                data.get("photo"),

            "created_at":
                data.get("created_at")
        }

        # CHECK EXISTING
        existing = db.collection(
            "Users"
        ).where(
            "email",
            "==",
            user["email"]
        ).stream()

        if list(existing):

            return jsonify({
                "success": False,
                "message":
                    "User already exists"
            }), 400

        doc_ref = db.collection(
            "Users"
        ).add(user)

        return jsonify({
            "success": True,
            "id":
                doc_ref[1].id
        }), 201

    except Exception as e:

        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


# GET USERS
@user_bp.route(
    "/get-users",
    methods=["GET"]
)
def get_users():

    try:

        docs = db.collection(
            "Users"
        ).stream()

        users = []

        for doc in docs:

            item = doc.to_dict()

            item["id"] = doc.id

            users.append(item)

        return jsonify({
            "success": True,
            "data": users
        })

    except Exception as e:

        return jsonify({
            "success": False,
            "error": str(e)
        }), 500