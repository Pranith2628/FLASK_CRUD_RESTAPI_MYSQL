from flask import Flask, jsonify, request, json
from flask_sqlalchemy import SQLAlchemy
from flask_mysqldb import MySQL
from flask_marshmallow import Marshmallow

app = Flask(__name__)

db = SQLAlchemy()
ma = Marshmallow()

mysql = MySQL(app)


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(15), nullable=False)
    price = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(10), nullable=False)

    def __int__(self, name, price, category):
        self.name = name
        self.price = price
        self.category = category


class ProductSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'price', 'category')


product_schema = ProductSchema()
products_schema = ProductSchema(many=True)


app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:""@localhost/product"
db.init_app(app)
with app.app_context():
    db.create_all()

# 'POST' = creating new data
@app.route('/product/add', methods=['POST'])
def add_product():
    _json = request.json
    name = _json['name']
    price = _json['price']
    category = _json['category']
    new_product = Product(name=name, price=price, category=category)
    db.session.add(new_product)
    db.session.commit()
    return jsonify({"message": "your product has been successfully added"})

# 'GET' = reading all the data from the table
@app.route('/product', methods=['GET'])
def get_product():
    products = []
    data = Product.query.all()
    products = products_schema.dump(data)
    return jsonify(products)

# 'GET' = reading a single product from the table by using <id>
@app.route('/product/<id>', methods=['GET'])
def get_product_byid(id):
    if not str.isdigit(id):
        return jsonify(f"Message: The id of the product cannot be a string")
    else:
        data = []
        product = Product.query.get(id)
        if product is None:
            return jsonify(f"No product was found")
        else:
            data = product_schema.dump(product)
            return jsonify(data)

# 'PUT' = updating a single product from the table by using <id>
@app.route('/product/update/<id>', methods=['PUT'])
def update_product_by_id(id):
    data = request.get_json()
    product = Product.query.get(id)
    if data.get('name'):
        product.name = data['name']
    if data.get('price'):
        product.price = data['price']
    if data.get('category'):
        product.category = data['category']
    db.session.add(product)
    db.session.commit()
    return jsonify({"message": "your product has been successfully updated"})

# 'DELETE' = deleting a single product from the table by using <id>
@app.route('/product/delete/<id>', methods=['DELETE'])
def delete_product_by_id(id):
    product = Product.query.get(id)
    db.session.delete(product)
    db.session.commit()
    return jsonify(f"The product has been deleted")


if __name__ == "__main__":
    app.run(debug=True)
