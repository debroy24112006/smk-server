from functools import wraps

from flask import (
    request,
    jsonify
)

ADMIN_USERNAME = "Smk@World"

ADMIN_PASSWORD = "Smk@2k26"

def admin_required(f):

    @wraps(f)
    def decorated(
        *args,
        **kwargs
    ):

        username = request.headers.get(
            "x-admin-username"
        )

        password = request.headers.get(
            "x-admin-password"
        )

        if (

            username !=
                ADMIN_USERNAME or

            password !=
                ADMIN_PASSWORD
        ):

            return jsonify({

                "success": False,

                "message":
                    "Unauthorized Access"

            }), 401

        return f(
            *args,
            **kwargs
        )

    return decorated