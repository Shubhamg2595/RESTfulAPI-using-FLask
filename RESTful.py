from flask import Flask,request
from flask_restful import Resource,Api,reqparse
from flask_jwt import JWT,jwt_required
from security import authenticate,identity
from user import UserRegistration

app=Flask(__name__)
'create a secret key for your app'
app.secret_key='shubham:)'
api=Api(app)

jwt=JWT(app,authenticate,identity)


items=[]

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price', type=float, required=True, help="this field cannot be left blank")

    # @jwt_required()
    def get(self,name):
        item=next(filter(lambda x:x['name']==name,items),None)
        return {'item':item},200 if item is not None else 404


    def post(self,name):
        if next(filter(lambda x:x['name']==name,items),None):
            return {'Message':'An item with name {} already exists in the itemList'.format(name)},400
        data=Item.parser.parse_args()
        item={'name':name,'price':data['price']}
        items.append(item)
        return item,201


#CREATING A METHOD TO DELETE ITEMS
    def delete(self,name):
        global items
        items=list(filter(lambda x:x['name'] == name ,items))
        return {'message':'items deleted'}
#USING reqparse to make sure ,we can parse the input data in put() method properly.
    #reqparse also helps in making sure that only variable json can be passed and not any other value
    def put(self,name):
        #first we check if item exist or not
        data=Item.parser.parse_args()
        item=next(filter(lambda x:x['name']==name,items),None)
        if item is None:
            item={'name':name,'price':data['price']}
            items.append(item)
        else:
            item.update(data) #item is actually a dictionary that has an updated method...

        return {'message':'itemlist updated'}

class ItemList(Resource):
    def get(self):
        return {'item':items}



api.add_resource(Item,'/item/<string:name>')
api.add_resource(ItemList,'/items')
api.add_resource(UserRegistration,'/register')
if __name__ == '__main__':
    app.run(port=5000,debug=True)