import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .Drink.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)

'''
@TODO uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
!! Running this funciton will add one
'''
db_drop_and_create_all()

# ROUTES
'''
@TODO implement endpoint
    GET /drinks
        it should be a public endpoint
        it should contain only the drink.short() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks', method=['GET'])
def get_drinks():
    drinks = Drink.short.query.all()
    return jsonify({
            'success':True,
            'drinks': drinks
            })
    


'''
@TODO implement endpoint
    GET /drinks-detail
        it should require the 'get:drinks-detail' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks-details', method=['GET'])
def get_drinks_details():
    drinks = Drink.long.query.all()
    token = get_token_auth_header()
    payload = verify_decode_jwt(token)
    check_permissions(permission, payload)
    return jsonify({
            'success':True,
            'drinks': drinks
            })

'''
@TODO implement endpoint
    POST /drinks
        it should create a new row in the drinks table
        it should require the 'post:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the newly created drink
        or appropriate status code indicating reason for failure
'''

@app.route('/drinks', method=['POST'])
def create_drinks():
    body = request.get_json()
    new_title = body.get('title', None)
    new_recipe = body.get('recipe', None)
    new_drink = Drink(title=new_title, recipe=new_recipe)
            drink.insert()
    token = get_token_auth_header()
    payload = verify_decode_jwt(token)
    check_permissions(permission, payload)
    return jsonify({
            'success':True,
            'drinks': drinks
            })
'''
@TODO implement endpoint
    PATCH /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should update the corresponding row for <id>
        it should require the 'patch:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the updated drink
        or appropriate status code indicating reason for failure
'''

@app.route('/drinks/<int:drink_id>', method=['PATCH'])
def update_drinks(drink_id):
    try:
       body = request.get_json()
       drink = Drink.query.filter(Drink.id==drink.id).one_or_none()
       
       if drink is None:
          abort error(404)
       new_title = body.get('title', None)
       new_recipe = body.get('recipe', None)
       new_drink = Drink(title=new_title, recipe=new_recipe)
       
       drink = new_drink
       drink.update()
      
       token = get_token_auth_header()
       payload = verify_decode_jwt(token)
       check_permissions(permission, payload)
       return jsonify({
            'success':True,
            'drinks': drinks
            })
    except:abort(404)
'''
@TODO implement endpoint
    DELETE /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should delete the corresponding row for <id>
        it should require the 'delete:drinks' permission
    returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
        or appropriate status code indicating reason for failure
'''
@app.route('/drinkss/<int:drink_id>', methods=['DELETE'])
    def delete_drink(drink_id):
        try:
           drink = Drink.query.filter(Drink.id == Drink_id).one_or_none()
           if drink is None:
               abort(404)
           drink.delete()
           token = get_token_auth_header()
           payload = verify_decode_jwt(token)
           check_permissions(permission, payload)
           return jsonify({
               'success':True,
               'delete':id,
               })
        except:
            abort(404)
            

# Error Handling
'''
Example error handling for unprocessable entity
'''


@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422


'''
@TODO implement error handlers using the @app.errorhandler(error) decorator
    each error handler should return (with approprate messages):
             jsonify({
                    "success": False,
                    "error": 404,
                    "message": "resource not found"
                    }), 404

'''

'''
@TODO implement error handler for 404
    error handler should conform to general task above
'''

 @app.errorhandler(404)
    def not_found(error):
       return jsonify({
           "success": False, 
           "error": 404,
           "message": "Resource Not found"
           }), 404
       
    @app.errorhandler(422)
    def unprocessable(error):
       return jsonify({
           "success": False, 
           "error": 422,
           "message": "unprocessable"
           }), 422

    return app

'''
@TODO implement error handler for AuthError
    error handler should conform to general task above
'''
@app.errorhandler(AuthError)
def handle_error(e):
    response = {
        "message": HTTP_STATUS_CODES.get(e.status_code),
        "description": e.error,
    }
    return response, e.status_code
