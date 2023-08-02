from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from pydantic import BaseModel
import os
from haystack.document_stores import ElasticsearchDocumentStore
from haystack.utils import fetch_archive_from_http
from haystack import Pipeline
from haystack.nodes import TextConverter, PreProcessor
import json
from haystack.nodes import BM25Retriever
from haystack.nodes import FARMReader
from pprint import pprint
from haystack.utils import print_answers


app = FastAPI()

class Question(BaseModel):
    query: str
    
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
async def root():
    return {"message": "Hello World"}




host = os.environ.get("ELASTICSEARCH_HOST", "localhost")
os.environ["TOKENIZERS_PARALLELISM"] = "false"
document_store = ElasticsearchDocumentStore(host=host, username="", password="", index="squad")
retriever = BM25Retriever(document_store=document_store)
reader = FARMReader(model_name_or_path="deepset/roberta-base-squad2", use_gpu=True)
querying_pipeline = Pipeline()
querying_pipeline.add_node(component=retriever, name="Retriever", inputs=["Query"])
querying_pipeline.add_node(component=reader, name="Reader", inputs=["Retriever"])

@app.post('/intent')
async def get_answer(q:Question):
    
    prediction = querying_pipeline.run(
    query=q.query, params={"Retriever": {"top_k": 1}, "Reader": {"top_k": 5}}
)
    print_answers(prediction, details="minimum")  ## Choose from `minimum`, `medium` and `all`
    # ans = prediction["answers"]
    # jsonString = json.dumps(prediction)
    # print(jsonString)
    # print(type(ans))
    # print(ans[0])
    # print(type(ans[0]))
    # for key, value in prediction.items() :
    #     print (key)
    return prediction