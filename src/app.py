from fastapi import FastAPI
import uvicorn
from src.routes.user import user_route



app = FastAPI()



@app.get("/")
def root():
  return "Main APP"

app.include_router(user_route)


if __name__=="__main__":
  
  uvicorn.run("src.app:app",port=5000,host="127.0.0.1")