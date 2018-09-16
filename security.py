users=[
    {
        'id':1,
        'username':'shubham',
        'password':'1234'
    }
]

username_mapping={
    'bob':{
        'id':1,
        'username':'shubham',
        'password':'1234'
    }
}

userid_mapping={1:
    {
        'id':1,
        'username':'shubham',
        'password':'1234'
    }
}

'userid and username mapping are onlyy useful when we want to extract data about specific user' \
'bases on their names or their ids'

'''
NOW WE WILL CREATE A FUNCTION TO AUTHENTICATE A USER FROM OUR ABOVE LIST
'''

def authenticate(username,password):
    user=username_mapping.get(username,None)
    if user and user.password==password:
        return user


'here identity function is unique to FLASK-JWT...' \
'here identity takes in a payload as input where PAYLOAD IS' \
'THE CONTENT OF THE JWT TOKEN' \
'AND WE ARE USING IT TO FETCH THE USER ID FROM THE PAYLOAD AND BASED ON THAT ID ' \
'WE CAN RETIRVE THE SPECIFIC USER,THAT MATCHES THIS PAYLOAD' \
''
def identity(payload):
    user_id=payload['identity']
    return userid_mapping.get(user_id,None)