from pinecone import Pinecone
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv
import os
from langdetect import detect
from celery import shared_task
import traceback
from langchain_openai import ChatOpenAI
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.chains import LLMChain
import requests


def detect_language(text):
    try:
        language = detect(text)
        return language
    except:
        return None


load_dotenv(override=True)

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_INDEX = os.getenv("PINECONE_INDEX")
OPENAI_KEY = os.getenv("OPENAI_KEY")
HUGGINGFACE_KEY = os.getenv("HUGGINGFACE_KEY")


pc = Pinecone(api_key=PINECONE_API_KEY)
index = pc.Index(PINECONE_INDEX)

model = SentenceTransformer("antoinelouis/biencoder-electra-base-french-mmarcoFR")
llm = ChatOpenAI(openai_api_key=OPENAI_KEY)

out_context = """Votre phrase est hors contexte, ou manque de clarté ce chatbot est dédié à donner des réponses sur la classification 
    de votre infraction au code de la route selon la politique marocaine, veuillez entrer une entrée valide où vous 
    expliquez votre amende et je vous renverrai le type d'amende commise."""

not_french = """Votre phrase d'entrée n'est pas en français. Veuillez fournir une phrase d'entrée en français. 
      Le chatbot ne prend pas encore en charge les langues multiples lorsqu'il s'agit de la politique marocaine de circulation"""


def preprocess(query):
    embeddings = model.encode(query)
    return [tensor.item() for tensor in embeddings]


@shared_task
def upsert_input(pred, embeddings):
    try:
        index_info = index.describe_index_stats()
        # Extract the number of records (vectors) from the index info
        num_records = index_info["total_vector_count"]
        print(num_records)

        vector = {
            "id": f"id{num_records+1}",
            "values": embeddings,
            "metadata": {"class_violation": pred},
        }

        index.upsert(vectors=[vector])
        print("input user upserted to pinecone")

    except Exception as e:
        print(f"Error processing task: {e}")
        traceback.print_exc()


def predict(query):
    valid = False
    language = detect_language(query)
    if not language == "fr":
        return not_french, valid, None

    else:
        embeddings = preprocess(query)
        sentiment_label = sentiment(query)
        result = index.query(vector=embeddings, top_k=1, include_metadata=True)
        score = result["matches"][0]["score"]
        threshold = 0.4

        if float(score) >= threshold:
            valid = True
            return (
                result["matches"][0]["metadata"]["class_violation"],
                valid,
                embeddings,
                sentiment_label,
            )
        else:
            return out_context, valid, embeddings, sentiment_label


def sentiment(input):
    API_URL = (
        "https://api-inference.huggingface.co/models/ac0hik/Sentiment_Analysis_French"
    )
    headers = {"Authorization": HUGGINGFACE_KEY}
    payload = {
        "inputs": input,
    }
    response = requests.post(API_URL, headers=headers, json=payload)
    json_response = response.json()

    """
    [[{"label":"positive","score":0.7034227848052979},{"label":"neutral","score":0.24707841873168945},{"label":"negative","score":0.04949873313307762}]]
    """
    print(max(json_response[0], key=lambda x: x["score"])["label"])
    return max(json_response[0], key=lambda x: x["score"])["label"]


def chain(classes, sentiment):
    system_template = """
                Vous êtes un assistant efficace pour une application web qui identifie le type d'amendement applicable à une infraction au code de la route, votre rôle est d'informer le conducteur sur
                son type d'infraction, et explique sa situation, et fait appel à l'analyse des sentiments dans votre réponse à l'utilisateur. 
                """

    system_message_prompt = SystemMessagePromptTemplate.from_template(system_template)

    # Human question prompt
    human_template = """
                Cette amende appartient à la classe : {classe}
                Les points à retirer : {points}
                Montant à payer en cas de règlement immédiat ou dans les 24 heures suivant l`infraction : {montant_immediat}
                Si le règlement est effectué dans les 15 jours suivants : {montant_suivant}
                sentiment : {sentiment}
                """

    human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)

    chat_prompt = ChatPromptTemplate.from_messages(
        [system_message_prompt, human_message_prompt]
    )

    chain = LLMChain(llm=llm, prompt=chat_prompt)

    try:
        response = chain.run(
            classe=classes[0],
            montant_immediat=classes[1],
            montant_suivant=classes[2],
            points=classes[3],
            sentiment=sentiment,
        )

        response = response.replace("\n", "<br>")
        return response
    except:
        return "open API expired mate"
