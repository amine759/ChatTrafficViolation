from pinecone import Pinecone
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv
import os
from langdetect import detect


def detect_language(text):
    try:
        language = detect(text)
        return language
    except:
        return None


load_dotenv(override=True)

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_INDEX = os.getenv("PINECONE_INDEX")

pc = Pinecone(api_key=PINECONE_API_KEY)
index = pc.Index(PINECONE_INDEX)

model = SentenceTransformer("antoinelouis/biencoder-electra-base-french-mmarcoFR")

out_context = """Votre phrase est hors contexte, ou manque de clarté ce chatbot est dédié à donner des réponses sur la classification 
    de votre infraction au code de la route selon la politique marocaine, veuillez entrer une entrée valide où vous 
    expliquez votre amende et je vous renverrai le type d'amende commise."""

not_french = """Votre phrase d'entrée n'est pas en français. Veuillez fournir une phrase d'entrée en français. 
      Le chatbot ne prend pas encore en charge les langues multiples lorsqu'il s'agit de la politique marocaine de circulation"""


def upsert_batch_input(queries, preds):
    """
    add user input along the conversation, to optimize cost we will add a batch of the conversation whenever a session is closed
    """
    print(queries)
    index_info = pc.info_index(index)
    # Extract the number of records (vectors) from the index info
    num_records = index_info["stats"]["n"]
    vectors = []

    i = num_records
    for query, pred in zip(queries, preds):
        i += 1
        vector = {"id": f"id{i}", "values": "", "metadata": {"class_violation": ""}}
        vector["metadata"]["class_violation"] = pred
        embeddings = preprocess(query)
        vector["values"] = embeddings

        vectors.append(vector)

    index.upsert(vectors=vectors)


def preprocess(query):
    embeddings = model.encode(query)
    return [tensor.item() for tensor in embeddings]


def predict(query):
    """
    1. embed query
    2. convert
    3. pass to pinecone
    4. get class
    5. custum sentence
    """
    valid = False
    language = detect_language(query)
    if not language == "fr":
        return not_french, valid

    else:
        embeddings = preprocess(query)
        result = index.query(vector=embeddings, top_k=1, include_metadata=True)
        score = result["matches"][0]["score"]
        threshold = 0.4

        if float(score) >= threshold:
            valid = True
            return result["matches"][0]["metadata"]["class_violation"], valid
        else:
            return out_context, valid
