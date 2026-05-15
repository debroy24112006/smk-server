from flask import Blueprint, request, jsonify

from firebaseSetup import db

product_bp = Blueprint(
    "product_bp",
    __name__
)


# ADD PRODUCT
@product_bp.route(
    '/add-product',
    methods=['POST']
)
def add_product():

    try:

        data = request.get_json()

        product = {

            "name":
            data.get("name"),

            "description":
            data.get("description"),

            "mrp":
            data.get("mrp"),

            "market_price":
            data.get("market_price"),

            "offer_price":
            data.get("offer_price"),

            "category": data.get("category"),
            "brand": data.get("brand"),
            "stock": data.get("stock"),
            "status": data.get("status"),

            "images":
            data.get("images", [])

        }

        doc_ref = db.collection(
            "Products"
        ).add(product)

        return jsonify({

            "success": True,

            "message":
            "Product added successfully",

            "id":
            doc_ref[1].id

        }), 201

    except Exception as e:

        return jsonify({

            "success": False,

            "error": str(e)

        }), 500


# GET ALL PRODUCTS
@product_bp.route(
    '/get-products',
    methods=['GET']
)
def get_products():

    try:

        docs = db.collection(
            "Products"
        ).stream()

        products = []

        for doc in docs:

            item = doc.to_dict()

            item["id"] = doc.id

            products.append(item)

        return jsonify({

            "success": True,

            "count": len(products),

            "data": products

        }), 200

    except Exception as e:

        return jsonify({

            "success": False,

            "error": str(e)

        }), 500


# GET SINGLE PRODUCT
@product_bp.route(
    '/get-product/<doc_id>',
    methods=['GET']
)
def get_single_product(doc_id):

    try:

        doc = db.collection(
            "Products"
        ).document(doc_id).get()

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

            "data": product

        }), 200

    except Exception as e:

        return jsonify({

            "success": False,

            "error": str(e)

        }), 500


# UPDATE PRODUCT
@product_bp.route(
    '/update-product/<doc_id>',
    methods=['PUT']
)
def update_product(doc_id):

    try:

        data = request.get_json()

        ref = db.collection(
            "Products"
        ).document(doc_id)

        if not ref.get().exists:

            return jsonify({

                "success": False,

                "message":
                "Product not found"

            }), 404

        updated_product = {

            "name":
            data.get("name"),

            "description":
            data.get("description"),

            "mrp":
            data.get("mrp"),

            "market_price":
            data.get("market_price"),

            "offer_price":
            data.get("offer_price"),

            "category": data.get("category"),
            "brand": data.get("brand"),
            "stock": data.get("stock"),
            "status": data.get("status"),

            "images":
            data.get("images", [])

        }

        ref.update(updated_product)

        return jsonify({

            "success": True,

            "message":
            "Product updated successfully"

        }), 200

    except Exception as e:

        return jsonify({

            "success": False,

            "error": str(e)

        }), 500


# DELETE PRODUCT
@product_bp.route(
    '/delete-product/<doc_id>',
    methods=['DELETE']
)
def delete_product(doc_id):

    try:

        ref = db.collection(
            "Products"
        ).document(doc_id)

        doc = ref.get()

        if not doc.exists:

            return jsonify({

                "success": False,

                "message":
                "Product not found"

            }), 404

        product = doc.to_dict()

        images = product.get(
            "images",
            []
        )

        return jsonify({

            "success": True,

            "images": images,

            "message":
            "Delete images first"

        }), 200

    except Exception as e:

        return jsonify({

            "success": False,

            "error": str(e)

        }), 500


# FINAL DELETE
@product_bp.route(
    '/final-delete-product/<doc_id>',
    methods=['DELETE']
)
def final_delete_product(doc_id):

    try:

        ref = db.collection(
            "Products"
        ).document(doc_id)

        if not ref.get().exists:

            return jsonify({

                "success": False,

                "message":
                "Product not found"

            }), 404

        ref.delete()

        return jsonify({

            "success": True,

            "message":
            "Product deleted successfully"

        }), 200

    except Exception as e:

        return jsonify({

            "success": False,

            "error": str(e)

        }), 500