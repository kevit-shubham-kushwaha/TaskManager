from fastapi import FastAPI
import uvicorn



app = FastAPI()



@app.get("/")
def root():
  return "Main APP"


if __name__=="__main__":
  
  uvicorn.run("src.app:app",port=5000,host="127.0.0.1")