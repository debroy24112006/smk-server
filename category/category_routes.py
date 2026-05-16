# ================================
# category/category_routes.py
# ================================

from flask import (
    Blueprint,
    request,
    jsonify
)

from firebaseSetup import db

from meili import (
    categories_index
)

from middleware.admin_auth import (
    admin_required
)

category_bp = Blueprint(
    "category_bp",
    __name__
)

# ======================================
# ADD CATEGORY
# ======================================
@category_bp.route(
    "/add-category",
    methods=["POST"]
)
@admin_required
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
                data.get("image"),

            "position":
                int(
                    data.get(
                        "position",
                        0
                    )
                )
        }

        # FIREBASE
        doc_ref = db.collection(
            "Categories"
        ).add(category)

        category_id = (
            doc_ref[1].id
        )

        category["id"] = str(
            category_id
        )

        db.collection(
            "Categories"
        ).document(
            category_id
        ).update({

            "id":
                str(category_id)
        })

        # MEILI
        try:

            categories_index.add_documents(
                [category],
                primary_key="id"
            )

        except Exception as meili_error:

            print(
                "MEILI CATEGORY ADD ERROR:",
                str(meili_error)
            )

        return jsonify({

            "success": True,

            "message":
                "Category added successfully",

            "id":
                category_id

        }), 201

    except Exception as e:

        return jsonify({

            "success": False,

            "error":
                str(e)

        }), 500


# ======================================
# GET CATEGORIES
# ======================================
@category_bp.route(
    "/get-categories",
    methods=["GET"]
)
def get_categories():

    try:

        try:

            results = categories_index.search(
                "",
                {

                    "sort": [
                        "position:asc"
                    ],

                    "limit":
                        1000
                }
            )

            categories = (
                results["hits"]
            )

        except Exception as meili_error:

            print(
                "MEILI CATEGORY SEARCH ERROR:",
                str(meili_error)
            )

            docs = db.collection(
                "Categories"
            ).stream()

            categories = []

            for doc in docs:

                item = doc.to_dict()

                item["id"] = doc.id

                categories.append(
                    item
                )

            categories.sort(
                key=lambda x:
                    x.get(
                        "position",
                        0
                    )
            )

        return jsonify({

            "success": True,

            "count":
                len(categories),

            "data":
                categories

        })

    except Exception as e:

        return jsonify({

            "success": False,

            "error":
                str(e)

        }), 500


# ======================================
# GET SINGLE CATEGORY
# ======================================
@category_bp.route(
    "/get-category/<doc_id>",
    methods=["GET"]
)
def get_single_category(doc_id):

    try:

        doc = db.collection(
            "Categories"
        ).document(
            doc_id
        ).get()

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

            "data":
                category

        })

    except Exception as e:

        return jsonify({

            "success": False,

            "error":
                str(e)

        }), 500


# ======================================
# UPDATE CATEGORY
# ======================================
@category_bp.route(
    "/update-category/<doc_id>",
    methods=["PUT"]
)
@admin_required
def update_category(doc_id):

    try:

        data = request.get_json()

        ref = db.collection(
            "Categories"
        ).document(
            doc_id
        )

        if not ref.get().exists:

            return jsonify({

                "success": False,

                "message":
                    "Category not found"

            }), 404

        updated_category = {

            "id":
                str(doc_id),

            "name":
                data.get("name"),

            "slug":
                data.get("slug"),

            "status":
                data.get("status"),

            "image":
                data.get("image"),

            "position":
                int(
                    data.get(
                        "position",
                        0
                    )
                )
        }

        # FIREBASE
        ref.update(
            updated_category
        )

        # MEILI
        try:

            categories_index.update_documents(
                [updated_category]
            )

        except Exception as meili_error:

            print(
                "MEILI CATEGORY UPDATE ERROR:",
                str(meili_error)
            )

        return jsonify({

            "success": True,

            "message":
                "Category updated successfully"

        })

    except Exception as e:

        return jsonify({

            "success": False,

            "error":
                str(e)

        }), 500


# ======================================
# DELETE CATEGORY
# ======================================
@category_bp.route(
    "/delete-category/<doc_id>",
    methods=["DELETE"]
)
@admin_required
def delete_category(doc_id):

    try:

        ref = db.collection(
            "Categories"
        ).document(
            doc_id
        )

        if not ref.get().exists:

            return jsonify({

                "success": False,

                "message":
                    "Category not found"

            }), 404

        # FIREBASE DELETE
        ref.delete()

        # MEILI DELETE
        try:

            categories_index.delete_document(
                str(doc_id)
            )

        except Exception as meili_error:

            print(
                "MEILI CATEGORY DELETE ERROR:",
                str(meili_error)
            )

        return jsonify({

            "success": True,

            "message":
                "Category deleted successfully"

        })

    except Exception as e:

        return jsonify({

            "success": False,

            "error":
                str(e)

        }), 500