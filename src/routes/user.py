from fastapi import APIRouter


user_route = APIRouter(prefix="/users",tags=["users"])


class UserRoutes:
  
    @staticmethod
    @user_route.get("/")
    def get_users():
        
        
        return {"data":"User Data!!"}
      
    @staticmethod
    @user_route.post("/")
    def create_user():
      
      return {"message":"User Created Successful!!"}
    
    
    @staticmethod
    @user_route.put("/{user_id}")
    def update_user(user_id:str):
      
        return {"message":"User Updated Successful!!"}
      
    
    @staticmethod
    @user_route.delete("/{user_id}")
    def delete_user(user_id:str):
      
        return {"message":"User deleted Successful!!"}
      