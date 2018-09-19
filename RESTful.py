from flask import Flask,request
from flask_restful import Resource,Api
from flask_jwt import JWT,jwt_required
from security import authenticate,identity


app=Flask(__name__)
'create a secret key for your app'
app.secret_key='shubham:)'
api=Api(app)

jwt=JWT(app,authenticate,identity)


items=[]

class Item(Resource):
    # @jwt_required
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


#CREATING A METHOD TO DELETE ITEMS
    def delete(self,name):
        global items
        items=list(filter(lambda x:x['name'] == name ,items))
        return {'message':'items deleted'}

# '''
#     reason i used global keyword with items is to ensure python interpreter
#     that the items local variables used at left side is actually the outer vaiable defined above
#
#
#     if we dont use global keyword, the python interpreter will think,
#     items is a local variable
#
#      so what is actually happening is we are replacing the existing items list with a new list
#      that does not contain the name of the item being deleted'''

    def put(self,name):
        data=request.get_json()
        #first we check if item exist or not
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

if __name__ == '__main__':
    app.run(port=5000,debug=True)