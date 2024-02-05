from pinecone import Pinecone
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv
import os

load_dotenv(override=True)

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_INDEX = os.getenv("PINECONE_INDEX")

pc = Pinecone(api_key=PINECONE_API_KEY)
index = pc.Index(PINECONE_INDEX)

model = SentenceTransformer('antoinelouis/biencoder-electra-base-french-mmarcoFR')

def predict(query):
  '''
  1. embed query
  2. convert 
  3. pass to pinecone 
  4. get class
  5. custum sentence 
  '''
  embedding = model.encode(query)
  embedding =  [tensor.item() for tensor in embedding]
  result = index.query(vector=embedding, top_k=1,include_metadata=True)
  return result['matches'][0]['metadata']['class_violation']