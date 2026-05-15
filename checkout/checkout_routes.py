from flask import Blueprint, request, jsonify

from firebaseSetup import db

from datetime import datetime

checkout_bp = Blueprint(
    'checkout_bp',
    __name__
)

# SAVE CHECKOUT REQUEST
@checkout_bp.route(
    '/submit-checkout-request',
    methods=['POST']
)
def submit_checkout_request():

    try:

        data = request.get_json()

        checkout_data = {

            'name':
                data.get('name'),

            'phone':
                data.get('phone'),

            'location':
                data.get('location'),

            'products':
                data.get('products'),

            'total':
                data.get('total'),

            'status':
                'Pending',

            'created_at':
                datetime.now()
                .strftime(
                    '%d %b %Y %I:%M %p'
                )
        }

        db.collection(
            'CheckoutRequests'
        ).add(checkout_data)

        return jsonify({

            'success': True,

            'message':
                'Request submitted successfully'

        }), 200

    except Exception as e:

        return jsonify({

            'success': False,

            'error': str(e)

        }), 500


# GET ALL REQUESTS
@checkout_bp.route(
    '/checkout-requests',
    methods=['GET']
)
def get_checkout_requests():

    try:

        docs = db.collection(
            'CheckoutRequests'
        ).stream()

        requests = []

        for doc in docs:

            item = doc.to_dict()

            item['id'] = doc.id

            requests.append(item)

        return jsonify({

            'success': True,

            'data': requests

        }), 200

    except Exception as e:

        return jsonify({

            'success': False,

            'error': str(e)

        }), 500


# UPDATE STATUS
@checkout_bp.route(
    '/update-checkout-status/<id>',
    methods=['PUT']
)
def update_checkout_status(id):

    try:

        data = request.get_json()

        db.collection(
            'CheckoutRequests'
        ).document(id).update({

            'status':
                data.get('status')
        })

        return jsonify({

            'success': True,

            'message':
                'Status updated'

        }), 200

    except Exception as e:

        return jsonify({

            'success': False,

            'error': str(e)

        }), 500