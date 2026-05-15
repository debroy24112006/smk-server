from flask import Blueprint, request, jsonify

from firebaseSetup import db

popup_bp = Blueprint(
    'popup_bp',
    __name__
)

# SAVE POPUP
@popup_bp.route(
    '/save-popup',
    methods=['POST']
)
def save_popup():

    try:

        data = request.get_json()

        popup_data = {

            'title': data.get('title'),

            'description': data.get('description'),

            'discount': data.get('discount'),

            'button_text': data.get('button_text'),

            'button_link': data.get('button_link'),

            'image': data.get('image'),

            'status': data.get('status')
        }

        docs = db.collection(
            'PopupSettings'
        ).stream()

        existing = list(docs)

        # UPDATE EXISTING
        if len(existing) > 0:

            doc_id = existing[0].id

            db.collection(
                'PopupSettings'
            ).document(doc_id).update(
                popup_data
            )

        else:

            db.collection(
                'PopupSettings'
            ).add(popup_data)

        return jsonify({

            'success': True,

            'message': 'Popup updated successfully'

        }), 200

    except Exception as e:

        return jsonify({

            'success': False,

            'error': str(e)

        }), 500


# GET POPUP
@popup_bp.route(
    '/get-popup',
    methods=['GET']
)
def get_popup():

    try:

        docs = db.collection(
            'PopupSettings'
        ).stream()

        popup = None

        for doc in docs:

            popup = doc.to_dict()

            popup['id'] = doc.id

            break

        return jsonify({

            'success': True,

            'data': popup

        }), 200

    except Exception as e:

        return jsonify({

            'success': False,

            'error': str(e)

        }), 500