'''
now we are making appropriate changes in this file after modifications done in user class for database access

'''


from user import User
from werkzeug.security import safe_str_cmp

def authenticate(username,password):
    user=User.findByUsername(username)
    if user and safe_str_cmp(user.password,password): # if user and user.password==password:
        return user
def identity(payload):
    user_id=payload['identity']
    return User.findByUseId(user_id)