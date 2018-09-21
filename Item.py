import sqlite3
from flask_restful import Resource,reqparse
from flask_jwt import jwt_required

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price', type=float, required=True, help="this field cannot be left blank")

# '''instead of fetching items data in get() method, we will create a classmethod() to ' \
# 'do the same thing and then we will this class method in our get() ,post() and other methods as per requirement '''

    @classmethod
    def findItemByName(cls,name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "select * from items where name=?"
        result = cursor.execute(query, (name,))
        row = result.fetchone()
        connection.close()

        if row is not None:
            return {"item":{'name':row[0],'price':row[1]}}


    # @jwt_required()
    def get(self,name):
        item=self.findItemByName(name)
        if item:
            return item
        return {"message":"item not found"},404


    def post(self,name):
        if self.findItemByName(name):
            return {"message":"an item with name {} already exists in the itemList.".format(name)}

        data=Item.parser.parse_args()

        item={'name':name,'price':data['price']}
        try:
            self.insert(item)
        except:
            return {"message":"An error occured inserting the item"},500

        return item,201


    @classmethod
    def insert(cls,item):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "insert into items values (?,?)"
        cursor.execute(query, (item['name'], item['price']))

        connection.commit()
        connection.close()

    """REASON I AM CREATING A SEPERATE METHOD TO INSERT ITEM IS BECAUSE
    TILL NOW, I WAS SIMPLY WOKRING WITH THE LISTS AND IT WAS EASY TO APPEND A NEW ITEM
    
    NOW I AM WORKING  WITH DATABASES, NOW I NEED TO INSERT DATA PROPERLY USING SQL QUERIES...
    so i cannot write the insert logic once for post() and once for PUT()
    so i am simply creating a classmethod() to insert a item in dB and will call it in 
    put() and post() 
    """


    def delete(self,name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "Delete from items where name=?"
        cursor.execute(query,(name,))

        connection.commit()
        connection.close()

        return {'message':'items deleted'}

#USING reqparse to make sure ,we can parse the input data in put() method properly.
    #reqparse also helps in making sure that only variable json can be passed and not any other value
    def put(self,name):
        #first we check if item exist or not
        data=Item.parser.parse_args()
        item=self.findItemByName(name)
        updated_item={'name':name,'price':data['price']}

        if item is None:
            try:
                self.insert(updated_item)
            except:
                return {"message":"an error occured while inserting the data"},500
        else:
            try:
                self.update(updated_item) #item is actually a dictionary that has an updated method...
            except:
                return {"message":"An error occured while updating the item"},500
        return updated_item

    @classmethod
    def update(cls,item):
        connection=sqlite3.connect('data.db')
        cursor=connection.cursor()

        upd_query="update items set price=? where name=?"
        cursor.execute(upd_query,(item['price'],item['name']))



class ItemList(Resource):
    def get(self):
        connection=sqlite3.connect('data.db')
        cursor=connection.cursor()

        fetchAll_query="select * from items"
        result=cursor.execute(fetchAll_query)

        items=[]
        for row in result:
            items.append({'name':row[0],'price':row[1]})

        connection.close()

        return {'ITEM_LIST':items}