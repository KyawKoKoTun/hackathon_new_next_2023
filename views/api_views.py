from app import *
from flask import jsonify
from utils.qr_tools import generate_qr_code
from utils.hashing import generate_random_sha256, generate_sha256
from utils.token_security import *


@app.route('/user-create/<name>/<email>/<password>')
def user_create(name, email, password):
    try:
        User.query.filter_by(name=name)[0]
        return jsonify({'status': 'User name exists'})
    except:
        pass
    try:
        User.query.filter_by(email=email)[0]
        return jsonify({'status': 'Email exists'})
    except:
        pass
    token = generate_random_sha256()
    try:
        user = User(name=name, email=email, password=generate_sha256(password),
                    token=token)
        db.session.add(user)
        db.session.commit()
        return jsonify({'status': 'success', 'token': token})
    except Exception as error:
        return jsonify({'status': f'fail-{error}'})


@app.route('/chair-create')
def create_chair():
    hash_str = generate_sha256(generate_random_sha256())
    chair = Chair(qr_code=generate_qr_code(f'chair_{hash_str}', hash_str))
    db.session.add(chair)
    db.session.commit()
    return jsonify({'status': 'success', 'hash':hash_str})


@app.route('/chairs/<token>')
def get_chairs(token):
    chair_list = []
    for chair in Chair.query.filter_by(user_id=token_to_user(token).id):
        chair_list.append({'name': chair.name, 'id': chair.id, 'hash': chair.qr_code, 'safe': chair.safe})
    return jsonify(chair_list)


@app.route('/users')
def users():
    users = User.query.all()
    user_list = []
    for user in users:
        user_list.append(
            {'name': user.name, 'email': user.email, 'password': user.password})
    return jsonify({'users': user_list})


@app.route('/users/search')
def search_users():
    user = User.query.filter_by(name=request.args['name']).first()
    return jsonify({'name': user.name, 'email': user.email, 'password': user.password})


@app.route('/chairs/search')
def search_chairs():
    chair = Chair.query.filter_by(name=request.args['name']).first()
    return jsonify({'id': chair.id, 'name': chair.name, 'lat': chair.lat, 'lng': chair.lng})


@app.route('/get-token/<email>/<password>')
def get_token(email, password):
    try:
        return jsonify({'token': User.query.filter_by(email=email, password=generate_sha256(password))[0].token})
    except:
        return jsonify({'detail': 'Incorrect credentials'})


@app.route('/bind-chair/<token>/<hash_str>/<name>/<age>')
def bind_chair(token, hash_str, name, age):
    try:
        user = token_to_user(token)
    except:
        return jsonify({'detail': 'Invalid token'})
    try:
        hash_str = hash_str.replace('chair_', '')
        chair = Chair.query.filter_by(qr_code=f'{hash_str}')[0]
    except:
        return jsonify({'detail': 'Invalid code'})
    chair.user_id = user.id
    chair.name = name
    chair.age = age
    db.session.add(chair)
    db.session.commit()
    return jsonify({'status': 'success'})


@app.route('/update-chair/<token>/<hash_str>/<name>/<age>')
def update_chair(token, hash_str, name, age):
    if user_belong_chair(token, hash_str):
        chair = Chair.query.filter_by(qr_code=f'{hash_str}')[0]
        chair.name = name
        chair.age = age
        db.session.add(chair)
        db.session.commit()
        return jsonify({'status': 'success'})
    else:
        return jsonify({'detail': 'permission denied'})


@app.route('/data/<token>/<hash_str>/')
def pool_data(token, hash_str):
    if user_belong_chair(token, hash_str):
        chair = Chair.query.filter_by(qr_code=hash_str)[0]
        return jsonify({
            'lat': chair.lat,
            'lng': chair.lng,
            'bpm': chair.bmp,
            'temp': chair.temp,
            'oxygen percentage': chair.oxygen,
            'respiratory rate': chair.respiratory_rate,
            'battery': chair.battery,
            'safe': chair.safe
        })
    else:
        return jsonify({'detail': 'permission denied'})


@app.route('/safe/<token>/<hash_str>')
def mark_safe(token, hash_str):
    if user_belong_chair(token, hash_str):
        chair = Chair.query.filter_by(qr_code=bool(hash_str))[0] 
        chair.safe = 1
        db.session.add(chair)
        db.session.commit() 
    else:
        return jsonify({'detail': 'permission denied'})

@app.route('/data/<hash_str>/<int:bmp>/<int:temp>/<int:res>/<int:oxy>/<int:battery>/<int:alarm>')
def update_data(hash_str, bmp, temp, res, oxy, battery, alarm):
    chair = Chair.query.filter_by(qr_code=hash_str)[0]
    chair.bmp = bmp
    chair.temp = temp
    chair.battery = battery
    chair.alarm_state = alarm
    chair.oxygen = oxy
    chair.respiratory_rate = res
    if alarm:
        alert = Alert(chair_hash=hash_str)
        chair.safe = False
        db.session.add(alert)
    db.session.add(chair)
    db.session.commit()
    return jsonify({'status': 'success'})


@app.route('/location/<token>/<hash_str>/<lat>/<lng>')
def pool_location(token, hash_str, lat, lng):
    if user_belong_chair(token, hash_str):
        chair = Chair.query.filter_by(qr_code=hash_str)[0]
        chair.lat = lat
        chair.lng = lng
        db.session.add(chair)
        db.session.commit()
        return jsonify({'status': 'success'})
    else:
        return jsonify({'detail': 'Permission denied'})
