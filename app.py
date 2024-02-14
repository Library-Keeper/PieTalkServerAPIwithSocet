import uvicorn
from fastapi import FastAPI


app = FastAPI()

@app.get('/')
def home():
    return "Hello"

print(f"main.py with :{app}")


if __name__ == "__main__":
    uvicorn.run("main:app", port=8000)
