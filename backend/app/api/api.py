"""
api.py
- provides the API endpoints for consuming and producing
  REST requests and responses
"""

from flask import Blueprint, jsonify, request, current_app
from functools import wraps
import jwt
from datetime import datetime, timedelta
from .models import db, Alias, Device, Place, Measurement, Unit, Value, User, Role
api = Blueprint('api', __name__)

import telegram
global chat_id
global bot
chat_id=75150392

bot = telegram.Bot(token="1647818581:AAGzhsza7cUAfEtv-yAyqT2XLeqjo2hz8LQ")

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
        place = Place(name=data['name'])
        db.session.add(place)
        db.session.commit()
        return jsonify(place.to_dict()),201


@api.route('/places/<int:id>', methods=('GET', 'PUT', 'DELETE'))
@token_required
def place(current_user,id):
    if request.method == 'GET':
        place = Place.query.filter_by(id=id).first_or_404()
        return jsonify(place.to_dict())
    elif request.method == 'PUT':
        data = request.get_json()
        place = Place.query.get(id)
        place.name = data['name']
        print(data)
        db.session.commit()
        return jsonify ({'msg': 'success'}), 201
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
        new_unit = Unit(
            name=data['name'],
            symbol=data['symbol']
        )
        db.session.add(new_unit)
        db.session.commit()
        return jsonify ({'msg': 'success'}), 201

@api.route('/units/<int:id>', methods=['GET', 'PUT', 'DELETE'])
@token_required
def unit(current_user,id):
    unit = Unit.query.filter_by(id=id).first_or_404()
    
    if request.method == 'PUT':
        data = request.get_json()
        unit.name = data['name']
        unit.symbol = data['symbol']
        db.session.commit()
        return jsonify ({'msg': 'success'}), 200
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
        print(data)
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
                    #TODO: ver si es de unit o de alias en el JSON en DeviceForm.vue
                    max_limit=alias['max_limit'], 
                    min_limit=alias['min_limit']
                    )
                new_device.aliases.append(new_alias)
            db.session.commit()
            return jsonify({'msg': 'success'}),200
    else:
        devices = Device.query.all()
        return jsonify({'devices':[
            device.to_dict() for device in devices
        ]})

# solo para pruebas por el momento.
def filter_set(aliases, search_string):
    def iterator_func(x):
        if search_string == x.id:
            return False
        return True
    return filter(iterator_func, aliases)

@api.route('/devices/<int:id>', methods=['GET','PUT','DELETE'])
@token_required
def device(current_user,id):
    device = Device.query.filter_by(id=id).first()
    if request.method == 'PUT':
        data = request.get_json()
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
        return jsonify({'msg':'success'}), 200
    
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
    measurements = Measurement.query.filter_by(device_id=device_id).all()
    print(measurements)
    if measurements is not None:
        return jsonify({"measurements":[measurement.to_dict() for measurement in measurements],"name":measurements[0].device.name if len(measurements) else None}), 200
    return jsonify({
        'measurements': [],
        'name': None
    })

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
        print(data)
        user.name = data['name']
        user.email=data['email']
        user.role_id=data['role']
        user.telegram_id = data['telegram_id'] if 'telegram_id' in data else None
        if 'password' in data:
            user.__init__(name=data['name'],email=data['email'],password=data['password'])
        db.session.commit()
        return jsonify(user.to_dict()),201
    elif request.method == 'DELETE':
        db.session.delete(user)
        db.session.commit()
        return jsonify({'msg':'success'}), 200
    else:
        return jsonify(user.to_dict())

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
    print(json)
    return jsonify(json)

@api.route('/showme', methods=['GET'])
@token_required
def me(current_user):
    print(current_user.to_dict())
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
                print('VALORRRR: {}'.format(alias.min_limit) )
                print('VALOR LEIDO {}'.format(type(value_to_add.value)))
                if alias.min_limit is not False and value_to_add.value <= alias.min_limit:
                    message = 'Algo está mal con {d}, {a} está por debajo del valor establecido ({ml}), Valor actual: {v}'.format(d=alias.device.name,ml=alias.min_limit, a=alias.name, v=value_to_add.value)
                if alias.max_limit is not False and value_to_add.value >= alias.max_limit:
                    message = 'Algo está mal con {d}, {a} está por encima del valor establecido ({ml}), Valor actual: {v}'.format(d=alias.device.name,ml=alias.max_limit, a=alias.name, v=value_to_add.value)
                if message:
                    bot.send_message(chat_id=chat_id, text=message)
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
    
    print(data)
    return jsonify(response)