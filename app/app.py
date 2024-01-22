#!/usr/bin/env python3

from flask import Flask, make_response, jsonify, request
from flask_migrate import Migrate
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from flask_restful import Api, Resource, reqparse
from flask_marshmallow import Marshmallow
from models import db, Vendor, Sweet, Vendor_Sweets


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
ma = Marshmallow(app)
migrate = Migrate(app, db)
api = Api(app)
db.init_app(app)


class VendorSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Vendor


vendor_schema = VendorSchema()
vendors_schema = VendorSchema(many=True)


class SweetSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Sweet


sweet_schema = SweetSchema()
sweets_schema = SweetSchema(many=True)


class VendorSweetSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Vendor_Sweets


vendor_sweet_schema = VendorSweetSchema()
vendor_sweets_schema = VendorSweetSchema(many=True)


class Home(Resource):
    def get(self):
        return "Welcome to sweet vendors"


api.add_resource(Home, "/")


class VendorResource(Resource):
    def get(self):
        vendors = Vendor.query.all()
        vendors_dict = vendors.to_dict()
        response = make_response(jsonify(vendors_dict), 200)
        return response


api.add_resource(VendorResource, "/vendors")


class VendorByID(Resource):
    def get(self, vendor_id):
        vendor = Vendor.query.filter_by(id=vendor_id).first()

        if vendor:
            vendor_data = vendor_schema.dump(vendor)
            vendor_sweets = Vendor_Sweets.query.filter_by(vendor_id=vendor_id).all()
            vendor_data["vendor_sweets"] = vendor_sweet_schema.dump(vendor_sweets)
            return jsonify(vendor_data)
        else:
            return make_response(jsonify({"error": "Vendor not found"}), 404)


api.add_resource(VendorByID, "/vendors/<int:vendor_id>")

class Sweet(Resource):
    def get(self):
        sweets = Sweet.query.all()
        sweets_dict = sweets.to_dict()

        response = make_response(
            jsonify(sweets_schema.dump(sweets_dict))
        )
        return response
    
api.add_resource(Sweet, '/sweets')
    
class SweetsByID(Resource):
    def get(self, sweet_id):
        sweet= Sweet.query.get(sweet_id)

        if sweet:
            response = jsonify(sweet_schema.dump(sweet))
            return response
        else:
            response = make_response(
                jsonify(
                    {"Error":"Sweet not found"}
                ), 404
            )
            return response

api.add_resource(SweetsByID,'/sweets/<int:sweet_id>')

class VendorSweet(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('price', type=int, required = True)
        parser.add_argument('vendor_id', type=int, required=True)
        parser.add_argument('sweet_id', type = int, required = True)
        args = parser.parse_args()

        sweet = Sweet.query.get(args['sweet_id'])
        vendor = Vendor.query.get(args['vendor_id'])

        if not vendor or not sweet:
            return make_response(jsonify({
                "errors": ["validation errors"]
            }), 400)
        
        vendor_sweet = Vendor_Sweets(price = args['price'], vendor = vendor, sweet = sweet)
        db.session.add(vendor_sweet)
        db.session.commit()

        response = jsonify(vendor_sweet_schema.dump(vendor_sweet))

        return response

api.add_resource(VendorSweet, '/vendor_sweets')

class VendorSweetByID(Resource):
    def delete(self, vendor_sweet_id):
        vendor_sweet = Vendor_Sweets.query.get(vendor_sweet_id)
        if vendor_sweet:
            db.session.delete(vendor_sweet)
            db.session.commit()
            return jsonify({})
        else:
            return make_response(jsonify({
                "error": "VendorSweet not found"
            }), 404)

api.add_resource(VendorSweetByID, '/vendor_sweets/<int:vendor_sweet_id>')



if __name__ == "__main__":
    app.run(port=5555, debug=True)
