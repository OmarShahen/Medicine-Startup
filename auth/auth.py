from datetime import date
import traceback
from flask import Blueprint, request, jsonify
from mongoengine.queryset.visitor import Q
from input_checkers.auth_checkers import Verification
import bcrypt
from models.user import Users
from models.verification_code import Verification_codes
from api.sms import send_verification_sms
import random
from datetime import datetime
import jwt
from config.config import Config

auth_bp = Blueprint('auth_bp', __name__)

verification = Verification()


@auth_bp.route('/register-user', methods=['POST'])
def register_user():
    try:

        if not verification.is_name_valid(request.form['name']):
            return jsonify({
                'accepted': False,
                'message': 'invalid entry values',
                'field': 'username'
            }), 406


        if not verification.is_email_valid(request.form['email']):
            return jsonify({
                'accepted': False,
                'message': 'invalid entry values',
                'field': 'email'
            })

        if len(Users.objects(email=request.form['email'])) != 0:
            return jsonify({
                'accepted': False,
                'message': 'this email is already taken',
                'field': 'email'
            }), 406

        if not verification.is_phone_number_valid(request.form['phone']):
            return jsonify({
                'accepted': False,
                'message': 'invalid entry values',
                'field': 'phone number'
            }), 406
        
        if len(Users.objects(phone_number=request.form['phone'])) != 0:
            return jsonify({
                'accepted': False,
                'message': 'this phone number is already taken',
                'field': 'phone number'
            }), 406

        if not verification.is_password_valid(request.form['password']):
            return jsonify({
                'accepted': False,
                'message': 'invalid entry values',
                'field': 'password'
            }), 406

        if request.form['password'] != request.form['confirmPassword']:
            return jsonify({
                'accepted': False,
                'message': 'invalid entry values',
                'field': 'confirm password'
            }), 406

        if not request.form['dateOfBirth']:
            return jsonify({
                'accepted': False,
                'message': 'invalid entry values',
                'field': 'date of birth'
            }), 406
        
        if not request.form['countryCode']:
            return jsonify({
                'accepted': False,
                'message': 'invalid entry values',
                'field': 'country code'
            }), 406
        
        if not request.form['gender']:
            return jsonify({
                'accepted': False,
                'message': 'invalid entry values',
                'field': 'gender'
            }), 406


        user_pass_hash = bcrypt.hashpw(request.form['password'].encode(), bcrypt.gensalt())

        Users(
            name=request.form['name'],
            email=request.form['email'],
            phone_number = request.form['phone'],
            date_of_birth= request.form['dateOfBirth'],
            country_iso= request.form['countryCode'],
            token= user_pass_hash,
            gender= request.form['gender']
        ).save()

        user_data = Users.objects(phone_number=request.form['phone'])
        access_token = jwt.encode({'user_id': str(user_data[0].id)}, Config.SECRET_KEY).decode()

        return jsonify({
            'accepted': True,
            'message': 'account created successfully',
            'accessToken': access_token
        }), 200
    

    
    except Exception:
        traceback.print_exc()
        return jsonify({
            'accepted': False,
            'message': 'internal server error, please try again later',
        }), 500

@auth_bp.route('/check-email', methods=['POST'])
def check_email():
    try:
        if len(Users.objects(email=request.form['email'])) != 0:
            return jsonify({
                'accepted': False,
                'message': 'this email is already taken'
            }), 406

        return jsonify({
            'accepted':True,
            'message': 'this email is valid'
        }), 200

    except Exception:
        traceback.print_exc()
        return jsonify({
            'accepted': False,
            'message': 'internal server error, please try again later'
        }), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        
        user = Users.objects(phone_number=request.form['phone'])
        if len(user) == 0:
            return jsonify({
                'accepted': False,
                'message': 'this number does not exist'
            }), 406
        
        if not bcrypt.checkpw(request.form['password'].encode(), user[0].token.encode()):
            return jsonify({
                'accepted': False,
                'message': 'invalid credentials'
            }), 406
        
        user_data = Users.objects(phone_number=request.form['phone'])
        access_token = jwt.encode({'user_id': str(user_data[0].id)}, Config.SECRET_KEY).decode()

        return jsonify({
            'accepted': True,
            'message': 'valid credentials',
            'access_token': access_token
        }), 200

    except Exception:
        traceback.print_exc()
        return jsonify({
            'accepted': False,
            'message': 'internal server error, please try again later'
        }), 500

@auth_bp.route('/phone-number/verification-code', methods=['POST'])
def check_phone_number():
    try:
        
        user = Users.objects(phone_number=request.form['phone'])
        if len(user) != 0:
            return jsonify({
                'accepted': False,
                'message': 'this phone number is already taken'
            }), 406

        verification_code = random.randint(1000, 10000)
        is_message_sent = send_verification_sms(request.form['country_code'] + (request.form['phone'][1:]), verification_code)
        Verification_codes(
            code = verification_code,
            phone_number = request.form['phone'],
            creation_date = datetime.now()
        ).save()
        
        if is_message_sent:
            return jsonify({
                'accepted': True,
                'message': 'sms sent successfully'
            }), 200

    except Exception:
        traceback.print_exc()
        return jsonify({
            'accepted': False,
            'message': 'internal server error, please try agin later'
        }), 500

@auth_bp.route('/phone-number/verifiy', methods=['POST'])
def verifiy_phone():

    try:

        phone_number = Verification_codes.objects.filter(Q(phone_number=request.form['phone']) & Q(code=request.form['code']))
        if len(phone_number) == 0:
            return jsonify({
                'accepted': False,
                'message': 'invalid code'
            }), 406
        
        return jsonify({
            'accepted': True,
            'message': 'valid code'
        }), 200
        
    except Exception:
        traceback.print_exc()
        return jsonify({
            'accepted': False,
            'message': 'internal server error, please try again later'
        }), 500
































