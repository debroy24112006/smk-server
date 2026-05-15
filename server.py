from flask import Flask
from flask_cors import CORS

# PRODUCT
from products.product_routes import product_bp

# CATEGORY
from category.category_routes import category_bp

# ORDERS
from orders.order_routes import order_bp

# COUPONS
from coupons.coupon_routes import coupon_bp

# USERS
from users.user_routes import user_bp
from popup.popup_routes import popup_bp
from checkout.checkout_routes import checkout_bp

app = Flask(__name__)

# ENABLE CORS
CORS(app)

# REGISTER ROUTES
app.register_blueprint(product_bp)
app.register_blueprint(category_bp)
app.register_blueprint(order_bp)
app.register_blueprint(coupon_bp)
app.register_blueprint(user_bp)
app.register_blueprint(popup_bp)
app.register_blueprint(checkout_bp)

@app.route("/")
def home():

    return {
        "success": True,
        "message": "Backend Running"
    }

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )