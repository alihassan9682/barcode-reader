from quart import Quart, jsonify, request
from quart_cors import cors
from flask_sqlalchemy import SQLAlchemy
from QR_codes import *

app = Quart(__name__)
app = cors(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///items.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    items = db.relationship('Item', backref='product', lazy=True)

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    status = db.Column(db.Boolean, default=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)

    def __init__(self, name, product_id):
        self.name = name
        self.product_id = product_id

db.create_all()

@app.before_first_request
async def create_items():
    if not Product.query.all():
        product1 = Product(name="Product 1")
        product2 = Product(name="Product 2")
        db.session.add(product1)
        db.session.add(product2)
        db.session.commit()

        db.session.add(Item(name="Item 1", product_id=product1.id))
        db.session.add(Item(name="Item 2", product_id=product1.id))
        db.session.add(Item(name="Item 3", product_id=product2.id))
        db.session.commit()

@app.route("/report", methods=["GET"])
async def get_Menu():
    report = request.args.get("report_data")
    if report:
        base64_code = generate_qr_code_from_json(report)
        return jsonify({"report": base64_code})
    else:
        return jsonify({"error": "No report provided"}), 400

@app.route("/test", methods=["GET"])
async def get_test():
    return jsonify([{"name": "eman", "id": "1"}, {"name": "eman", "id": "2"},{"name": "eman", "id": "3"}])


@app.route("/barCodes", methods=["GET"])
async def get_barCode():
    id = request.args.get("barCodeid")
    if id:
        item = Item.query.get(id)
        if item:
            item.status = not item.status
            db.session.commit()
            product_id = item.product_id
            product = Product.query.get(product_id)
            product_items_count = Item.query.filter_by(product_id=product_id, status=True).count()
            return jsonify({
                "id": item.id,
                "name": item.name,
                "status": item.status,
                "product": product.name,
                "product_items_true_status_count": product_items_count
            })
        else:
            return jsonify({"error": "Item not found"}), 404
    else:
        return jsonify({"error": "No barcode ID provided"}), 400


if __name__ == "__main__":
    app.run(debug=True)
