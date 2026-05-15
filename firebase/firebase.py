from flask import Blueprint, request, jsonify
from firebase_admin import firestore
from firebaseSetup import cred

db = firestore.client()

add_bp = Blueprint("add_bp", __name__)


#here is the function where the document adding to the firebase

@add_bp.route('/add-products', methods=['POST'])
def add_data():
    try:
        data = request.get_json()

        if not data:
            return jsonify({"success": False, "error": "No data"}), 400

        product = {
            "name": data.get("name"),
            "price": data.get("price"),
            "category": data.get("category")
        }

        db.collection("Products").add(product)

        return jsonify({"success": True}), 201

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


#here is the function where the document getting all products from firebase 

@add_bp.route('/get-products', methods=['GET'])
def get_all_products():
    try:
        docs = db.collection("Products").stream()

        product_list = []

        for doc in docs:
            item = doc.to_dict()
            item["id"] = doc.id
            product_list.append(item)

        return jsonify({
            "success": True,
            "data": product_list
        }), 200

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

#here is the function where the document getting update

@add_bp.route('/update-product/<doc_id>', methods=['PUT'])
def update_product(doc_id):
    try:
        data = request.get_json()

        if not data:
            return jsonify({
                "success": False,
                "error": "No data provided"
            }), 400

        ref = db.collection("Products").document(doc_id)

        if not ref.get().exists:
            return jsonify({
                "success": False,
                "error": "Product not found"
            }), 404

        ref.update(data)

        return jsonify({
            "success": True,
            "message": "Product updated successfully"
        }), 200

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


#here is the function where the document getting deleted

@add_bp.route('/delete-product/<doc_id>', methods=['DELETE'])
def delete_product(doc_id):
    try:
        ref = db.collection("Products").document(doc_id)

        if not ref.get().exists:
            return jsonify({
                "success": False,
                "error": "Product not found"
            }), 404

        ref.delete()

        return jsonify({
            "success": True,
            "message": "Product deleted successfully"
        }), 200

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500