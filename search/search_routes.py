from flask import (
    Blueprint,
    jsonify
)

from firebaseSetup import db

from meili import (
    products_index,
    categories_index
)

import json

search_bp = Blueprint(
    "search_bp",
    __name__
)

# SAFE SERIALIZER
def clean_data(data):

    return json.loads(
        json.dumps(
            data,
            default=str
        )
    )

# REBUILD PRODUCTS INDEX
@search_bp.route(
    "/rebuild-products-index",
    methods=["GET", "POST"]
)
def rebuild_products_index():

    try:

        docs = db.collection(
            "Products"
        ).stream()

        products = []

        for doc in docs:

            item = doc.to_dict()

            item["id"] = doc.id

            # CLEAN FIREBASE TYPES
            item = clean_data(item)

            products.append(item)

        print(
            "TOTAL PRODUCTS:",
            len(products)
        )

        # DELETE OLD INDEX
        products_index.delete_all_documents()

        # ADD AGAIN
        task = products_index.add_documents(
            products,
            primary_key="id"
        )

        return jsonify({

            "success": True,

            "count":
                len(products),

            "taskUid":
                task.task_uid,

            "message":
                "Products index rebuilt"

        })

    except Exception as e:

        print(
            "REBUILD ERROR:",
            str(e)
        )

        return jsonify({

            "success": False,

            "error":
                str(e)

        }), 500


@search_bp.route(
    "/rebuild-categories-index",
    methods=["GET", "POST"]
)
def rebuild_categories_index():

    try:

        docs = db.collection(
            "Categories"
        ).stream()

        categories = []

        for doc in docs:

            item = doc.to_dict()

            item["id"] = str(doc.id)

            categories.append(item)

        # CLEAR
        categories_index.delete_all_documents()

        # ADD AGAIN
        categories_index.add_documents(
            categories,
            primary_key="id"
        )

        return jsonify({

            "success": True,

            "count":
                len(categories),

            "message":
                "Categories rebuilt"

        })

    except Exception as e:

        return jsonify({

            "success": False,

            "error":
                str(e)

        }), 500