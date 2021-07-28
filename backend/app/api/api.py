"""
api.py
- provides the API endpoints for consuming and producing
  REST requests and responses
"""

from flask import Blueprint, jsonify, request, current_app
from functools import wraps
import jwt
from datetime import datetime, timedelta
from .models import db, Alias, Device, Place, Measurement, Unit, Value, User, Role, Pending_registration
from .config import TELEGRAM_TOKEN_PROD
api = Blueprint('api', __name__)

import telegram
global bot

bot = telegram.Bot(token=TELEGRAM_TOKEN_PROD)

def token_required(f):
    @wraps(f)
    def _verify (*args, **kwargs):
        auth_headers = request.headers.get('Authorization', '').split()

        invalid_msg = {
            'msg': 'Necesita iniciar sesión para acceder al contenido',
            'authenticated': False
        }
        expired_msg = {
            'msg': 'Su sesión ha caducado, vuelva a hacer login',
            'authenticated': False
        }

        if len(auth_headers) != 2:
            return jsonify(invalid_msg), 401
        
        try:
            token = auth_headers[1]
            data = jwt.decode(token, current_app.config['SECRET_KEY'],algorithms="HS256")
            user = User.query.filter_by(email=data['sub']).first()
            if not user:
                raise RuntimeError('User not found')
            return f(user, *args, **kwargs)
        except jwt.ExpiredSignatureError:
            return jsonify(expired_msg), 401 
        except (jwt.InvalidTokenError, Exception) as e:
            print(e)
            return jsonify(invalid_msg), 401
    
    return _verify


@api.route('/places', methods=['GET', 'POST'])
@token_required
def places(current_user): 
    if request.method == 'GET':
        places = Place.query.all() 
        return jsonify({ 'places':[p.to_dict() for p in places] })
    
    elif request.method == 'POST':
        data = request.get_json()
        if Place.query.filter_by(name=data.get('name') ).first() is None:
            print(data['name'])
            place = Place(name=data['name'])
            db.session.add(place)
            db.session.commit()
            return jsonify(place.to_dict()),201
        else:
            return jsonify({
                'error':True,
                'msg':'El recinto ya existe.'
            }),409

@api.route('/places/<int:id>', methods=('GET', 'PUT', 'DELETE'))
@token_required
def place(current_user,id):
    if request.method == 'GET':
        place = Place.query.filter_by(id=id).first_or_404()
        return jsonify(place.to_dict())
    elif request.method == 'PUT':
        data = request.get_json()
        place = Place.query.get(id)
        if Place.query.filter((Place.name == data.get('name')) & (Place.id != place.id)).first() is None:
            place.name = data['name']
            db.session.commit()
            return jsonify ({'msg': 'success'}), 201
        else:
            return jsonify({'error': True, 'msg': 'ya existe un recinto con este nombre'}), 409
    elif request.method == 'DELETE':
        place = Place.query.get(id)
        db.session.delete(place)
        db.session.commit()
        return jsonify ({'msg': 'success'}), 200
    
@api.route('/units', methods=['GET', 'POST'])
@token_required
def units(current_user):
    if request.method == 'GET':
        units = Unit.query.all()
        return jsonify({'units':[u.to_dict() for u in units]})
    elif request.method == 'POST':
        data = request.get_json()
        if Unit.query.filter_by(name=data.get('name')).first() is None:
            new_unit = Unit(
                name=data['name'],
                symbol=data['symbol']
            )
            db.session.add(new_unit)
            db.session.commit()
            return jsonify ({'msg': 'success'}), 201
        else:
            return jsonify({'error':True, 'msg':'Ya existe una unidad con este nombre.'}), 409

@api.route('/units/<int:id>', methods=['GET', 'PUT', 'DELETE'])
@token_required
def unit(current_user,id):
    unit = Unit.query.filter_by(id=id).first()
    
    if request.method == 'PUT':
        data = request.get_json()
        if Unit.query.filter((Unit.name == data.get('name')) & (Unit.id != unit.id) ).first() is None:
            unit.name = data['name']
            unit.symbol = data['symbol']
            db.session.commit()
            return jsonify ({'msg': 'success'}), 200
        else:
            return jsonify({'error':True, 'msg':'Ya existe una unidad con este nombre.'}), 409
    elif request.method == 'DELETE':
        db.session.delete(unit)
        db.session.commit()
        return jsonify ({'msg': 'success'}), 200
    else:
        return jsonify(unit.to_dict())

@api.route('/devices', methods=['GET', 'POST'])
@token_required
def devices(current_user):
    if request.method == 'POST':
        data = request.get_json()
        device = Device.query.filter_by(unic_id=data['unic_id']).first()
        if device is None:
            new_device = Device(
                name=data['name'],
                unic_id=data['unic_id'],
                place_id=data['place']
            )
            db.session.add(new_device)
            for alias in data['aliases']:
                new_alias = Alias(
                    name=alias['alias'],
                    unit_id=alias['unit']['id'],
                    max_limit=alias['max_limit'], 
                    min_limit=alias['min_limit']
                    )
                new_device.aliases.append(new_alias)
            db.session.commit()
            return jsonify({'msg': 'success'}),200
        else:
            return jsonify({
                'error':True, 
                'msg':'Ya existe un dispositivo con este identificadr unico.'
                }), 409
    else:
        user = User.query.get(request.args.get('user'))
        if 'administrador' in user.role.name:
            devices = Device.query.all()
        else:
            devices = user.devices

        return jsonify({'devices':[
            device.to_dict() for device in devices
        ]})

@api.route('/devices/<int:id>', methods=['GET','PUT','DELETE'])
@token_required
def device(current_user,id):
    device = Device.query.filter_by(id=id).first()
    if request.method == 'PUT':
        data = request.get_json()
        if Device.query.filter((Device.unic_id == data.get('unic_id')) & (Device.id != device.id) ).first() is None:
            device.name = data['name']
            device.unic_id = data['unic_id']
            device.place_id = data['place']
        
            if 'deletedItems' in data:
                for alias in data['deletedItems']:
                    alias_to_delete = Alias.query.get(alias['id'])
                    db.session.delete(alias_to_delete)

            for alias in data['aliases']:
                if not 'id' in alias:
                    new_alias = Alias(
                        name=alias['alias'],
                        unit_id=alias['unit']['id'] if ('id' in alias['unit']) else alias['unit_id'],
                        max_limit=alias['max_limit'], 
                        min_limit=alias['min_limit']
                        )
                    device.aliases.append(new_alias)            
            db.session.commit()
            return jsonify({'msg':'success'}), 201
        else:
            return jsonify({
                'error':True, 
                'msg':'Ya existe un dispositivo con este identificadr unico.'
                }), 409
    
    elif request.method == 'DELETE':
        for alias in device.aliases:
            db.session.delete(alias)
        db.session.delete(device)
        db.session.commit()
        return jsonify({'msg':'success'}), 200

    return jsonify(device.to_dict())

@api.route('/devices/<int:device_id>/data', methods=['GET'])
@token_required
def dump_data(current_user,device_id):
    if 'administrador' in current_user.role.name:
        print('es admin')
        measurements = Measurement.query.filter_by(device_id=device_id).all()
        if measurements is not None:
            return jsonify({"measurements":[measurement.to_dict() for measurement in measurements],"name":measurements[0].device.name if len(measurements) else None}), 200
        return jsonify({
            'measurements': [],
            'name': None
        })
    else:
        print('no es admin')
        for device in current_user.devices:
            if device.id == device_id:
                measurements = Measurement.query.filter_by(device_id=device_id).all()
                if measurements is not None:
                    return jsonify({"measurements":[measurement.to_dict() for measurement in measurements],"name":measurements[0].device.name if len(measurements) else None}), 200
                return jsonify({
                    'measurements': [],
                    'name': None
                })
    return jsonify({'error':True, 'msg':'Algo salió mal'}),500

@api.route('/users', methods=['GET','POST'])
@token_required
def users(current_user):
    if request.method == 'POST':
        data = request.get_json()
        user = User.query.filter_by(email=data['email']).first()
        if user is not None:
            return jsonify({
                'error': True,
                'msg': 'Ya se ha registrado un usuario con este correo.'
            })
        else:
            new_user = User(**data)
            db.session.add(new_user)
            db.session.commit()
            return jsonify(new_user.to_dict()), 201
    
    users = User.query.all()
    return jsonify({'users':[user.to_dict() for user in users]})

@api.route('/users/<int:id>', methods=['GET', 'DELETE', 'PUT'])
@token_required
def user(current_user, id):
    user = User.query.filter_by(id=id).first()
    if request.method == 'PUT':
        data = request.get_json()
        try:
            user.name = data['name']
            user.email=data['email']
            user.role_id=data['role']
            user.devices=[]
            for device in data['devices']:
                d = Device.query.filter_by(id=device['id']).first()
                if user.devices:
                    for user_device in user.devices:
                        if d.id != user_device.id:
                            user.devices.append(d) 
                else:
                    user.devices.append(d)
            tele_id = data.get('telegram_id')
            if tele_id:
                user.telegram_id = tele_id
            else:
                user.telegram_id = None
                
            if 'password' in data:
                user.__init__(name=data['name'],email=data['email'],password=data['password'], role=data['role'])
            db.session.commit()
            return jsonify(user.to_dict()),201
        
        except Exception:
            return jsonify({
                'error': True,
                'msg': 'Ya se ha registrado un usuario con este correo.'
            }), 409
    elif request.method == 'DELETE':
            db.session.delete(user)
            db.session.commit()
            return jsonify({'msg':'success'}), 200
        
    else:
        return jsonify(user.to_dict())

@api.route('/users/pendings')
@token_required
def get_pending_registrations(current_user):
    pending = Pending_registration.query.filter_by(user_id=current_user.id).first()
    if pending is not None:
        return jsonify({
            "is_pending":True,
            "telegram_id": pending.telegram_id
            })
    else:
        return jsonify({
        "is_pending":False,
        "telegram_id": None
        })

@api.route('/users/pendings/apply', methods=['POST'])
@token_required
def apply_bot_registration(current_user):
    if request.method == 'POST':
        registration_code = request.get_json()['telegram_id']
        pending = Pending_registration.query.filter_by(telegram_id=registration_code).first()
        if pending is not None and pending.user_id == current_user.id:
            current_user.telegram_id = registration_code
            db.session.delete(pending)
            db.session.commit()
    return jsonify({'msg': 'Cuenta de Telegram registrada con exito!'})
        

@api.route('/roles', methods=['GET'])
def roles():
    roles = Role.query.all()
    return jsonify({'roles':[role.to_dict(False) for role in roles]})

@api.route('/login',methods=['POST'])
def login():
    data = request.get_json()
    user = User.authenticate(**data)

    if not user:
        return jsonify({
            'msg': 'Las credenciales no son válidas',
            'error':True,
            'authenticated':False
        }), 401
    token = jwt.encode({
        'sub':user.email,
        'iat': datetime.utcnow(),
        'exp': datetime.utcnow() + timedelta(days=1)},
        current_app.config['SECRET_KEY'])
    json = { 
        'token': token,
        'user': user.to_dict(),
        'authenticated':True
         }
    return jsonify(json)

@api.route('/showme', methods=['GET'])
@token_required
def me(current_user):
    return jsonify(current_user.to_dict()),200

###############################
# API section only for devices#
###############################
@api.route('/store-data', methods=['POST'])
def store_data():
    response = {}
    data = request.get_json()
    device = Device.query.filter_by(unic_id=data['unic_id']).first()
    if device is not None:
        new_measurement = Measurement(device_id=device.id)
        db.session.add(new_measurement)
        for value in data['values']:
            alias = Alias.query.filter_by(name=value['alias']).filter_by(device_id=device.id).first()
            if alias is not None:
                value_to_add = Value(
                    value=float(value['value']),
                    alias=alias,
                )
                new_measurement.values.append(value_to_add)
                message=''
                if alias.min_limit is not False and value_to_add.value <= alias.min_limit:
                    message = 'Algo está mal con {d}, {a} está por debajo del valor establecido ({ml}), Valor actual: {v}'.format(d=alias.device.name,ml=alias.min_limit, a=alias.name, v=value_to_add.value)
                if alias.max_limit is not False and value_to_add.value >= alias.max_limit:
                    message = 'Algo está mal con {d}, {a} está por encima del valor establecido ({ml}), Valor actual: {v}'.format(d=alias.device.name,ml=alias.max_limit, a=alias.name, v=value_to_add.value)
                if message:
                    for user in device.users:
                        if user.telegram_id:
                            bot.send_message(chat_id=user.telegram_id, text=message)
        db.session.commit()
        response = {
            "msg": "Data was stored",
            "error":False
        }
    else:
        response = {
            "msg":"device not listed",
            "error": True
        }
    
    return jsonify(response)