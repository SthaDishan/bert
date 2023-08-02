from fastapi import FastAPI,Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from tensorflow import keras
from keras.models import  load_model
import pandas as pd
import tensorflow_hub as hub
from tensorflow import argmax
from tensorflow import maximum
import numpy as np
import tensorflow
from database import Base, SessionLocal, engine
from models import Response
from sqlalchemy.orm import Session
from pydantic import BaseModel


Base.metadata.create_all(bind=engine)

class Chat(BaseModel):
    chat: str

app = FastAPI()
model_dir = "bert-model/bert_intent_clasification.h5"

model = load_model(model_dir,
                          custom_objects={'KerasLayer':hub.KerasLayer}
)


print("model loading...")

origins = ["*"]
methods = ["*"]
headers = ["*"]

app.add_middleware(
    CORSMiddleware, 
    allow_origins = origins,
    allow_credentials = True,
    allow_methods = methods,
    allow_headers = headers    
)
@app.get("/")

def index():
    return {"Hello":"World"}

def get_db():
    print("db init")
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

intents = ['PlayMusic',
 'AddToPlaylist',
 'RateBook',
 'SearchScreeningEvent',
 'BookRestaurant',
 'GetWeather',
 'SearchCreativeWork']

@app.post('/intent')
def intent_classfication(chat:Chat, db:Session=Depends(get_db)):
    msg = [chat.chat]
    pred = model.predict(msg)
    print(pred[0])
    print('Max',max(pred[0]))
    maxm = max(pred[0])
    if maxm < 0.7 :
        return {'reply':'Sorry I cant understand you, please rephrase!','intent':'Unknown'}
    
    intent_id = tensorflow.get_static_value(argmax(pred[0]))
    print(intent_id)
    intent = intents[argmax(pred[0])]
    print(intent)
    print(maxm)

    reply = db.query(Response).filter(Response.id == intent_id + 1 ).first()
    print('id',reply.id)
    print('reply',reply.reply)
    print('intent',reply.intent)
    response = {'reply':reply.reply, 'intent':reply.intent}
    return response
    



@app.get('/all-response')
def get_all_response(db: Session=Depends(get_db)):
    return db.query(Response).all()




