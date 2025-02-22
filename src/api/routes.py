from flask import Flask, request, jsonify, url_for, Blueprint, json, render_template
from api.models import db, ma
from api.models import User, Supermarket, Product, Cart
from api.utils import generate_sitemap, APIException

from api.models import UserSchema, ProductSchema, MarketSchema
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, JWTManager
from werkzeug.security import generate_password_hash, check_password_hash
import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

api = Blueprint('api', __name__)

#login route
@api.route('/register', methods=['POST'])
def register():
    name = request.json.get('name')
    email = request.json.get('email')
    password = request.json.get('password')
    location = request.json.get('location')
    is_active = False

    user_email = User.query.filter_by(email = email).first()
    if user_email is None:
        hashed_password = generate_password_hash(password)

        register_info = User(name, email, hashed_password, location, is_active)
        db.session.add(register_info)
        db.session.commit()

        msg = MIMEMultipart('alternative')
        msg['Subject'] = "Bienvenido"

        text = ""
        html = render_template('register.html', name = name)
        part1 = MIMEText(text, 'plain')
        part2 = MIMEText(html, 'html')
        msg.attach(part1)
        msg.attach(part2) 

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(os.getenv("FLASK_EMAIL_APP"), os.getenv("FLASK_EMAIL_PASS"))
        server.sendmail(os.getenv("FLASK_EMAIL_APP"), email, msg.as_string())

        return jsonify({
            "message": "User register succesfully"
        }), 200

    return jsonify({"message": "this email is already exist"}), 400

@api.route('/login', methods=['POST'])
def login():
    email = request.json.get('email', None)
    password = request.json.get('password', None)

    user = User.query.filter_by(email = email).first() 
    if user is None:
        return jsonify({
            "Message": "Email or Password Wrong"
        }), 400

    if check_password_hash(user.password, password):
        access_token = create_access_token(identity=user.id)
        return jsonify(token=access_token), 200
    else:
        return jsonify({"msg": "Email or Password Wrong"}), 400

@api.route('/forgot-password/', methods=['PUT', 'GET'])
def forgot_password():
    pass

@api.route('/user/<int:id>', methods=['GET'])
def get_users(id):
    users = User.query.get(id)
    users_schema = UserSchema()
    output = users_schema.dump(users)
    return jsonify(
        {"Result": output}
    )

@api.route('/market', methods=['GET'])
def get_a_markets():
    markets = Supermarket.query.all()
    markets_schema = MarketSchema(many=True)
    output = markets_schema.dump(markets)
    return jsonify(
        {"Results": output}
    )

@api.route('/market/<int:id>', methods=['GET'])
def get_a_market(id):
    market = Supermarket.query.get(id)
    output = MarketSchema().dump(market)
    return jsonify(
        {"Result": output}
    )

@api.route('/product', methods=['GET'])
def get_products():
    products = Product.query.all()
    products_schema = ProductSchema(many=True)
    output = products_schema.dump(products)
    return jsonify(
        {"Result": output}
    )

@api.route('/product/<int:id>', methods=['GET'])
def get_product(id):
    product = Product.query.get(id)
    output = ProductSchema().dump(product)
    return(
        {"Result": output}
    )

@api.route('/product', methods=['POST'])
def search_products():
    product = request.json.get('product')
    location = request.json.get('location')

    query = db.session.query(Supermarket, Product).join(Product, Product.market_id == Supermarket.id)
    output = [(market.market_name, product.product_name) for market, product in query]
    print(output)
    return 'ok'

@api.route('/cart', methods=['POST', 'GET'])
def cart_add():
    if request.method == 'POST':
        username = request.json.get('username')
        product = request.json.get('product')

        register = Cart(username, product)
        db.session.add(register)
        db.session.commit()
        return jsonify({
            "Message": "new register added susessfully"
        })
    #Handling the GET request
    query = db.session.query(Cart, User, Product).join(User, User.id == Cart.user_id).join(Product, Product.id == Cart.product_id).all() 
    output = [(user.name, product.product_name) for cart, user, product in query]

    return jsonify({
        "Result": output    
    })

@api.route('/sendmail', methods=['GET'])
def send_mail():
    email_to = 'carlosobandoup@gmail.com'
    me = 'cr.globalmarket.app@gmail.com'
    name = 'Carlos'

    msg = MIMEMultipart('alternative')
    msg['Subject'] = "Bienvenido"
    msg['To'] = email_to

    text = ""
    html = render_template('register.html', name = name)

    part1 = MIMEText(text, 'plain')
    part2 = MIMEText(html, 'html')

    msg.attach(part1)
    msg.attach(part2)
    
    email_to = 'carlosobandoup@gmail.com'
    message = render_template('register.html')

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(os.getenv("FLASK_EMAIL_APP"), os.getenv("FLASK_EMAIL_PASS"))
    server.sendmail(os.getenv("FLASK_EMAIL_APP"), email_to, msg.as_string())

    return 'success'