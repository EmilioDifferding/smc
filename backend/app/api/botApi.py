from flask import Blueprint, jsonify, request
from .models import db, User, Device, Pending_registration

bot = Blueprint('bot', __name__)

@bot.route('/', methods=['GET','POST'])
def generate_user_resgistration():
    if request.method == 'GET':
        return jsonify({"msg": 'Hola'})
    else:
        data = request.get_json()
        # recibir username desde le bot, el telegram_id y correo electronico 
        try:
            user = User.query.filter_by(email=data.get('email')).first()
            telegram_id = data.get('telegram_id')
            print(user)
            print(data)
            if user is not None:
                registration = Pending_registration(user_id=user.id, telegram_id=telegram_id)
                print(f'uID: {registration.user_id}, TID: {registration.telegram_id}')
                db.session.add(registration)
                db.session.commit()
                return jsonify({
                    'found': True
                })
            else:
                return jsonify({
                    'found': False
                })
        except:
            return jsonify({'msg':'error'}),500

@bot.route('/verify/<telegram_id>',methods=['GET'])
def verify(telegram_id):
    user = User.query.filter_by(telegram_id=telegram_id).first()
    status = False
    if user is not None:
        status = True
    else:
        status = False
    return jsonify({'is_registered':status})