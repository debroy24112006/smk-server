from flask import Blueprint, request, jsonify

from firebaseSetup import db

category_bp = Blueprint(
    "category_bp",
    __name__
)


# ADD CATEGORY
@category_bp.route(
    '/add-category',
    methods=['POST']
)
def add_category():

    try:

        data = request.get_json()

        category = {

    "name":
    data.get("name"),

    "slug":
    data.get("slug"),

    "status":
    data.get("status"),

    "image":
    data.get("image")
}

        doc_ref = db.collection(
            "Categories"
        ).add(category)

        return jsonify({

            "success": True,

            "message":
            "Category added successfully",

            "id":
            doc_ref[1].id

        }), 201

    except Exception as e:

        return jsonify({

            "success": False,

            "error": str(e)

        }), 500


# GET ALL CATEGORY
@category_bp.route(
    '/get-categories',
    methods=['GET']
)
def get_categories():

    try:

        docs = db.collection(
            "Categories"
        ).stream()

        categories = []

        for doc in docs:

            item = doc.to_dict()

            item["id"] = doc.id

            categories.append(item)

        return jsonify({

            "success": True,

            "count": len(categories),

            "data": categories

        }), 200

    except Exception as e:

        return jsonify({

            "success": False,

            "error": str(e)

        }), 500


# GET SINGLE CATEGORY
@category_bp.route(
    '/get-category/<doc_id>',
    methods=['GET']
)
def get_single_category(doc_id):

    try:

        doc = db.collection(
            "Categories"
        ).document(doc_id).get()

        if not doc.exists:

            return jsonify({

                "success": False,

                "message":
                "Category not found"

            }), 404

        category = doc.to_dict()

        category["id"] = doc.id

        return jsonify({

            "success": True,

            "data": category

        }), 200

    except Exception as e:

        return jsonify({

            "success": False,

            "error": str(e)

        }), 500


# UPDATE CATEGORY
@category_bp.route(
    '/update-category/<doc_id>',
    methods=['PUT']
)
def update_category(doc_id):

    try:

        data = request.get_json()

        ref = db.collection(
            "Categories"
        ).document(doc_id)

        if not ref.get().exists:

            return jsonify({

                "success": False,

                "message":
                "Category not found"

            }), 404

        updated_category = {

    "name":
    data.get("name"),

    "slug":
    data.get("slug"),

    "status":
    data.get("status"),

    "image":
    data.get("image")
}

        ref.update(updated_category)

        return jsonify({

            "success": True,

            "message":
            "Category updated successfully"

        }), 200

    except Exception as e:

        return jsonify({

            "success": False,

            "error": str(e)

        }), 500


# DELETE CATEGORY
@category_bp.route(
    '/delete-category/<doc_id>',
    methods=['DELETE']
)
def delete_category(doc_id):

    try:

        ref = db.collection(
            "Categories"
        ).document(doc_id)

        if not ref.get().exists:

            return jsonify({

                "success": False,

                "message":
                "Category not found"

            }), 404

        ref.delete()

        return jsonify({

            "success": True,

            "message":
            "Category deleted successfully"

        }), 200

    except Exception as e:

        return jsonify({

            "success": False,

            "error": str(e)

        }), 500