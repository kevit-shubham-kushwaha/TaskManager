class BaseRepository:
    def __init__(self, collection):
        self.collection = collection
          
    def get_name(self):
      return self.collection.name
  
    def insert_one(self,doc):
      return self.collection.insert_one(doc)
      
    def insert_many(self,docs):
      return self.collection.insert_many(docs)
      
    def find_one(self,query):
      return self.collection.find_one(query)
    
    def find_many(self,query):
      return self.collection.find(query)
    
    def update_one(self,query, upsert):
     return self.collection.update_one(query, upsert)
      
    def update_many(self,query, upsert):
      return self.collection.update_many(query, upsert)
      
    def delete_one(self, query):
        return self.collection.delete_one(query)

    def delete_many(self, query):
        return self.collection.delete_many(query)
      
    def distinct(self, field):
      return self.collection.distinct(field)
    