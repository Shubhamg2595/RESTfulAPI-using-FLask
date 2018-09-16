from flask import Flask,request
from flask_restful import Resource,Api


app=Flask(__name__)
api=Api(app)

#here an api works with a resource and each resource must be a class

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