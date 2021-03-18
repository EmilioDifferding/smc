"""
api.py
- provides the API endpoints for consuming and producing
  REST requests and responses
"""

from flask import Blueprint, jsonify, request

from .models import db, Alias, Device, Place, Measurement, Unit, Value

api = Blueprint('api', __name__)

@api.route('/places', methods=['GET', 'POST'])
def places():
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
def place(id):
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
        place = place.query.get(id)
        db.session.delete(place)
        db.session.commit()
        return jsonify ({'msg': 'success'}), 200
    
@api.route('/units', methods=['GET', 'POST'])
def units():
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
def unit(id):
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
def devices():
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
        for v in x.values():
            if search_string in v:
                return False
        return True
    return filter(iterator_func, aliases)

@api.route('/devices/<int:id>', methods=['GET','PUT','DELETE'])
def device(id):
    device = Device.query.filter_by(id=id).first()
    if request.method == 'PUT':
        data = request.get_json()
        device.name = data['name']
        device.unic_id = data['unic_id']
        device.place_id = data['place']

        for alias in device.aliases:
            db.session.delete(alias)     

        for alias in data['aliases']:
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
def dump_data(device_id):
    measurements = Measurement.query.filter_by(device_id=device_id).all()
    return jsonify({"measurements":[measurement.to_dict() for measurement in measurements],"name":measurements[0].device.name})

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
                    value=value['value'],
                    alias=alias,
                )
                new_measurement.values.append(value_to_add)
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