from flask import Flask,request
from flask_restful import Resource,Api
from flask_jwt import JWT,jwt_required
from security import authenticate,identity


app=Flask(__name__)
'create a secret key for your app'
app.secret_key='shubham:)'
api=Api(app)

jwt=JWT(app,authenticate,identity)

'''
here JWT creates a new endpoint that is /auth
when we calll/auth, we send it a username and a password and /auth endpoint send this data
to authenticate() method.

now after  successful authentication, JWT returns an access JW TOKEN
now this token is sent to identity function ,where identity uses received token as paylaod to
fetch the correct user based on given id.

'''


items=[]

class Item(Resource):
    @jwt_required
    def get(self,name):
        item=next(filter(lambda x:x['name']==name,items),None)
        return {'item':item},200 if item is not None else 404

    def post(self,name):
        if next(filter(lambda x:x['name']==name,items),None):
            return {'Message':'An item with name {} already exists in the itemList'.format(name)},400
        data=request.get_json()
        item={'name':name,'price':data['price']}
        items.append(item)
        return item,201

class ItemList(Resource):
    def get(self):
        return {'item':items}



api.add_resource(Item,'/item/<string:name>')
api.add_resource(ItemList,'/items')

if __name__ == '__main__':
    app.run(port=5000,debug=True)