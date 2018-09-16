'''now after creating user class, lets see how what changes we can make to our
security.py
'''
from user import User
from werkzeug.security import safe_str_cmp
users=[User(1,'shubham','1234')]
username_mapping={u.username: u for u in users}
userid_mapping={u.id: u for u in users}

# username_mapping={
#     'bob':{
#         'id':1,
#         'username':'shubham',
#         'password':'1234'
#     }
# }
#
# userid_mapping={1:
#     {
#         'id':1,
#         'username':'shubham',
#         'password':'1234'
#     }
# }
'''
NOTE: '==' NOT ALWAYS WORKS PROPERLY 
TO SOLVE THAT PROBLEM IMPORT SAFE_STR_CMP
THIS WILL WOKG WITH ALL SERVERS AND OLDER VERSIONS'
'''

def authenticate(username,password):
    user=username_mapping.get(username,None)
    if user and safe_str_cmp(user.password,password): # if user and user.password==password:
        return user
def identity(payload):
    user_id=payload['identity']
    return userid_mapping.get(user_id,None)