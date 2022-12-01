from fastapi import FastAPI, HTTPException, Depends, Request,status
from fastapi.responses import JSONResponse
from hashing import Hash
from jwttoken import create_access_token, get_current_user
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
import model

app = FastAPI(title="CPU & GPU Recommendation")
origins = [
    "http://localhost:3000",
    "http://localhost:8080",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from pymongo import MongoClient
mongodb_uri = 'mongodb+srv://widhys15:l1pW8mRA13f1xHei@apitst.jxllzys.mongodb.net/?retryWrites=true&w=majority'
port = 8000
client = MongoClient(mongodb_uri, port)
db = client["User"]

@app.get("/")
def read_root(current_user:model.User = Depends(get_current_user)):
	return {"data":"Ini udh terautentikasi"}

@app.get("/user/{username}")
def get_userdata(current_user:model.User = Depends(get_current_user)):
	return {
		"nama":"current_user.username"
		}

@app.post('/register')
def create_user(request:model.User):
	hashed_pass = Hash.bcrypt(request.password)
	user_object = dict(request)
	user_object["password"] = hashed_pass
	user_id = db["users"].insert_one(user_object)
	# print(user)
	return {"User":"created"}

@app.post('/login')
def login(request:OAuth2PasswordRequestForm = Depends()):
	user = db["users"].find_one({"username":request.username})
	if not user:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail = f'No user found with this {request.username} username')
	if not Hash.verify(user["password"],request.password):
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail = f'Wrong Username or password')
	access_token = create_access_token(data={"sub": user["username"] })
	return {"access_token": access_token, "token_type": "bearer"}

