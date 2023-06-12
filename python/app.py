from sre_parse import FLAGS
from flask import Flask, jsonify, request
from flask_restful import Resource, Api
from apispec import APISpec
from marshmallow import Schema, fields
from apispec.ext.marshmallow import MarshmallowPlugin
from flask_apispec.extension import FlaskApiSpec
from flask_apispec.views import MethodResource
from flask_apispec import doc, use_kwargs
import os
from flask_cors import CORS
from cryptotools import *
import secrets
import string
import functools

alphabet = string.ascii_letters + string.digits
secret_key_for_website = ''.join(secrets.choice(alphabet) for i in range(16))

app_key = os.environ['api_key']

app = Flask(__name__)  # Flask app instance initiated
app.config['SECRET_KEY'] = secret_key_for_website
cors = CORS(app, resources={r"/*": {"origins": "*"}})
api = Api(app)  # Flask restful wraps Flask app around it.
app.config.update({
    'APISPEC_SPEC': APISpec(
        title='Crypto API',
        version='v1',
        plugins=[MarshmallowPlugin()],
        openapi_version='2.0.0'
    ),
    'APISPEC_SWAGGER_URL': '/swagger/',  # URI to access API Doc JSON
    'APISPEC_SWAGGER_UI_URL': '/docs/'  # URI to access UI of API Doc
})
docs = FlaskApiSpec(app)


game_description = """ Purpose
- Simple Bitcoin API
"""
# Function to check if API key is valid
def is_api_valid(api_key):
    if os.environ['api_key'] == api_key:
        return True

def api_required(func):
    @functools.wraps(func)
    def decorator(*args, **kwargs):
        if request.headers:
            api_key = request.headers.get("Authorization")
            if is_api_valid(api_key):
                return func(*args, **kwargs)
            else:
                return {"message": "Not Authorized"}, 401
        else:
            return {"message": "Not Authorized"}, 401
        # Check if API key is correct and valid
        
    return decorator

class CheckserFundsSchema(Schema):
    walletname = fields.String(required=True, metadata={'description': "The Wallet Name"}) 

class SendBtcSchema(Schema):
    walletname = fields.String(required=True, metadata={'description': "The Wallet Name"})
    amount = fields.Float(required=True, metadata={'description': "Amount in BTC"})
    address = fields.String(Required=True, metadata={'description': "BTC address"})

class CreatewalletSchema(Schema):
    walletname = fields.String(required=True, metadata={'description': "The Wallet Name"})

class CheckAllTxs(Schema):
    walletname = fields.String(required=True, metadata={'description': "The Wallet Name"})


class NewaddressSchema(Schema):
    walletname = fields.String(required=True, metadata={'description': "The Wallet Name"}) 

class Createwallet(MethodResource, Resource):
    @doc(description='Create Wallet', tags=['Create User Wallet'])
    @use_kwargs(CreatewalletSchema, location=('json'))
    @api_required
    def post(self, **kwargs):
        cud = create_wallet(**kwargs)
        if cud == False:
            return jsonify({'code': 400, 'message': "Unable to create wallet"})
        else:
            return jsonify({'code': 200, 'data': cud, 'message': 'Success!'})


class Newaddress(MethodResource, Resource):
    @doc(description='Get new Adress', tags=['Get new address'])
    @use_kwargs(NewaddressSchema, location=('json'))
    @api_required
    def post(self, **kwargs):
        gna = wallet_addr(**kwargs)
        if gna == False:
            return jsonify({'code': 400, 'message': "Wrong Creds"})
        else:
            return jsonify({'code': 200, 'data': gna, 'message': 'Success!'})

class CheckserFunds(MethodResource, Resource):
    @doc(description='Check the wallet\'s funds', tags=['Check Funds'])
    @use_kwargs(CheckserFundsSchema, location=('json'))
    @api_required
    def post(self, **kwargs):
        wb = get_wallet_balance(**kwargs)
        if wb == None:
            return jsonify({'code': 400, 'message': "Unable to get wallet balance"})
        else:
            return jsonify({'code': 200, 'data': wb, 'message': 'Success!'})

class SendBtc(MethodResource, Resource):
    @doc(description='Cash out funds', tags=['Cash out'])
    @use_kwargs(SendBtcSchema, location=('json'))
    @api_required
    def post(self, **kwargs):
        sbtc, out = send_btc(**kwargs)
        if sbtc == False:
            return jsonify({'code': 400, 'data': out, 'message': "Insufficient Funds"})
        else:
            return jsonify({'code': 200, 'data': out, 'message': 'Success!'})
            

class CheckTx(MethodResource, Resource):
    @doc(description='Get Transactions for wallet', tags=['TxID'])
    @use_kwargs(CheckAllTxs, location=('json'))
    @api_required
    def post(self, **kwargs):
        tx = get_all_tx(**kwargs)
        if tx == False:
            return jsonify({'code': 400, 'message': "No Transactions Yet"})
        else:
            return jsonify({'code': 200, 'data': tx, 'message': "Success!"})




api.add_resource(CheckserFunds, '/funds/')
api.add_resource(SendBtc, '/send/')
api.add_resource(Createwallet, '/create_wallet/')
api.add_resource(CheckTx, '/tx/')
api.add_resource(Newaddress, '/new_address/')
docs.register(CheckserFunds)
docs.register(SendBtc)
docs.register(Createwallet)
docs.register(CheckTx)
docs.register(Newaddress)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8086)