from flask import Flask,request
from flask_restful import Resource,Api


# working nwith authentication
'install flaskj jwt'
'''
jst: stands for json web token
it helps in encoding some data
for example to send private messages,we can encode such messages,so that the reciever with corredt decryption key
can access it

'''
app=Flask(__name__)
'create a secret key for your app'
app.secret_key='shubham:)'
api=Api(app)


items=[]

class Item(Resource):
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