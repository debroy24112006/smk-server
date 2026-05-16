# ================================
# products/product_routes.py
# ================================

from flask import (
    Blueprint,
    request,
    jsonify
)

from firebaseSetup import db

from meili import (
    products_index
)

from middleware.admin_auth import (
    admin_required
)

import json

product_bp = Blueprint(
    "product_bp",
    __name__
)

# CLEAN FIREBASE TYPES
def clean_data(data):

    return json.loads(
        json.dumps(
            data,
            default=str
        )
    )

# ======================================
# ADD PRODUCT
# ======================================
@product_bp.route(
    "/add-product",
    methods=["POST"]
)
@admin_required
def add_product():

    try:

        data = request.get_json()

        product = {

            "name":
                data.get("name"),

            "description":
                data.get("description"),

            "category":
                data.get("category"),

            "brand":
                data.get("brand"),

            "images":
                data.get("images", []),

            "mrp":
                data.get("mrp"),

            "offer_price":
                data.get("offer_price"),

            "market_price":
                data.get("market_price"),

            "stock":
                data.get("stock"),

            "status":
                data.get("status")
        }

        # FIREBASE SAVE
        doc_ref = db.collection(
            "Products"
        ).add(product)

        product_id = (
            doc_ref[1].id
        )

        product["id"] = str(
            product_id
        )

        # UPDATE ID
        db.collection(
            "Products"
        ).document(
            product_id
        ).update({

            "id":
                str(product_id)
        })

        # CLEAN
        product = clean_data(
            product
        )

        # SAVE TO MEILI
        try:

            products_index.add_documents(
                [product],
                primary_key="id"
            )

        except Exception as meili_error:

            print(
                "MEILI ADD ERROR:",
                str(meili_error)
            )

        return jsonify({

            "success": True,

            "message":
                "Product added successfully",

            "id":
                product_id

        }), 201

    except Exception as e:

        return jsonify({

            "success": False,

            "error":
                str(e)

        }), 500


# ======================================
# GET PRODUCTS
# ======================================
@product_bp.route(
    "/get-products",
    methods=["GET"]
)
def get_products():

    try:

        query = request.args.get(
            "q",
            ""
        )

        category = request.args.get(
            "category"
        )

        filters = []

        if category:

            filters.append(
                f'category = "{category}"'
            )

        search_options = {

            "limit": 1000
        }

        if filters:

            search_options[
                "filter"
            ] = " AND ".join(
                filters
            )

        # SEARCH
        results = products_index.search(
            query,
            search_options
        )

        products = results["hits"]

        return jsonify({

            "success": True,

            "count":
                len(products),

            "data":
                products

        })

    except Exception as meili_error:

        print(
            "MEILI SEARCH ERROR:",
            str(meili_error)
        )

        # FIREBASE FALLBACK
        try:

            docs = db.collection(
                "Products"
            ).stream()

            products = []

            for doc in docs:

                item = doc.to_dict()

                item["id"] = doc.id

                products.append(
                    item
                )

            return jsonify({

                "success": True,

                "count":
                    len(products),

                "data":
                    products

            })

        except Exception as e:

            return jsonify({

                "success": False,

                "error":
                    str(e)

            }), 500


# ======================================
# GET SINGLE PRODUCT
# ======================================
@product_bp.route(
    "/get-product/<doc_id>",
    methods=["GET"]
)
def get_product(doc_id):

    try:

        doc = db.collection(
            "Products"
        ).document(
            doc_id
        ).get()

        if not doc.exists:

            return jsonify({

                "success": False,

                "message":
                    "Product not found"

            }), 404

        product = doc.to_dict()

        product["id"] = doc.id

        return jsonify({

            "success": True,

            "data":
                product

        })

    except Exception as e:

        return jsonify({

            "success": False,

            "error":
                str(e)

        }), 500


# ======================================
# UPDATE PRODUCT
# ======================================
@product_bp.route(
    "/update-product/<doc_id>",
    methods=["PUT"]
)
@admin_required
def update_product(doc_id):

    try:

        data = request.get_json()

        ref = db.collection(
            "Products"
        ).document(
            doc_id
        )

        if not ref.get().exists:

            return jsonify({

                "success": False,

                "message":
                    "Product not found"

            }), 404

        updated_product = {

            "id":
                str(doc_id),

            "name":
                data.get("name"),

            "description":
                data.get("description"),

            "category":
                data.get("category"),

            "brand":
                data.get("brand"),

            "images":
                data.get("images", []),

            "mrp":
                data.get("mrp"),

            "offer_price":
                data.get("offer_price"),

            "market_price":
                data.get("market_price"),

            "stock":
                data.get("stock"),

            "status":
                data.get("status")
        }

        # FIREBASE
        ref.update(
            updated_product
        )

        # CLEAN
        updated_product = clean_data(
            updated_product
        )

        # MEILI UPDATE
        try:

            products_index.update_documents(
                [updated_product]
            )

        except Exception as meili_error:

            print(
                "MEILI UPDATE ERROR:",
                str(meili_error)
            )

        return jsonify({

            "success": True,

            "message":
                "Product updated successfully"

        })

    except Exception as e:

        return jsonify({

            "success": False,

            "error":
                str(e)

        }), 500


# ======================================
# DELETE PRODUCT
# ======================================
@product_bp.route(
    "/delete-product/<doc_id>",
    methods=["DELETE"]
)
@admin_required
def delete_product(doc_id):

    try:

        ref = db.collection(
            "Products"
        ).document(
            doc_id
        )

        if not ref.get().exists:

            return jsonify({

                "success": False,

                "message":
                    "Product not found"

            }), 404

        # FIREBASE DELETE
        ref.delete()

        # DELETE FROM MEILI
        try:

            products_index.delete_document(
                str(doc_id)
            )

        except Exception as meili_error:

            print(
                "MEILI DELETE ERROR:",
                str(meili_error)
            )

        return jsonify({

            "success": True,

            "message":
                "Product deleted successfully"

        })

    except Exception as e:

        return jsonify({

            "success": False,

            "error":
                str(e)

        }), 500