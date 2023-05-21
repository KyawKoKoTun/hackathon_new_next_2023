from models import *


def token_to_user(token):
    try:
        return User.query.filter_by(token=token)[0]
    except:
        assert False


def user_belong_chair(token, hash_str):
    try:
        user = token_to_user(token)
        try:
            chair = Chair.query.filter_by(qr_code=hash_str)[0]
        except:
            return False
        if chair.user_id == user.id:
            return True
        else:
            return False
    except:
        return False
