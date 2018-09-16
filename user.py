'''

here we will be creating a user object, so that we dont have to keep adding our new users directly in users dictionary
that we created in security.py

'''

class User:
    def __init__(self,_id,username,password):
        self.id=_id
        self.username=username
        self.password=password