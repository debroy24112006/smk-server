from flask import Flask

from flask_cors import CORS

# PRODUCT
from products.product_routes import (
    product_bp
)

# CATEGORY
from category.category_routes import (
    category_bp
)

# ORDERS
from orders.order_routes import (
    order_bp
)

# COUPONS
from coupons.coupon_routes import (
    coupon_bp
)

# USERS
from users.user_routes import (
    user_bp
)

# POPUP
from popup.popup_routes import (
    popup_bp
)

# CHECKOUT
from checkout.checkout_routes import (
    checkout_bp
)

# SEARCH
from search.search_routes import (
    search_bp
)

# MEILISEARCH INIT
from meili import (
    products_index,
    categories_index
)

app = Flask(__name__)

# CORS
CORS(
    app,
    resources={
        r"/*": {
            "origins": "*"
        }
    }
)

# REGISTER ROUTES
app.register_blueprint(
    product_bp
)

app.register_blueprint(
    category_bp
)

app.register_blueprint(
    order_bp
)

app.register_blueprint(
    coupon_bp
)

app.register_blueprint(
    user_bp
)

app.register_blueprint(
    popup_bp
)

app.register_blueprint(
    checkout_bp
)

app.register_blueprint(
    search_bp
)

# ROOT
@app.route("/")
def home():

    return {

        "success": True,

        "message":
            "SMK Backend Running",

        "services": {

            "firebase":
                "connected",

            "meilisearch":
                "connected"
        }
    }

# HEALTH CHECK
@app.route("/health")
def health():

    return {

        "success": True,

        "status":
            "healthy"
    }

# START SERVER
if __name__ == "__main__":

    print(
        "\n=================================="
    )

    print(
        " SMK BACKEND STARTED "
    )

    print(
        "=================================="
    )

    print(
        "Server: http://0.0.0.0:5000"
    )

    print(
        "Meilisearch: http://127.0.0.1:7700"
    )

    print(
        "==================================\n"
    )

    app.run(

        host="0.0.0.0",

        port=5000,

        debug=True,

        threaded=True
    )