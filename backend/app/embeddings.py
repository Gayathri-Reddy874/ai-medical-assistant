import boto3
import json
from langchain_core.embeddings import Embeddings
from app.config import (
    AWS_REGION,
    EMBEDDING_MODEL_ID,
    AWS_ACCESS_KEY_ID,
    AWS_SECRET_ACCESS_KEY
)

class BedrockEmbeddings(Embeddings):
    def __init__(self):
        self.client = boto3.client(
            "bedrock-runtime",
            region_name=AWS_REGION,
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY
        )

    def embed_documents(self, texts):
        embeddings = []
        for text in texts:
            response = self.client.invoke_model(
                modelId=EMBEDDING_MODEL_ID,
                body=json.dumps({"inputText": text}),
                contentType="application/json",
                accept="application/json"
            )
            result = json.loads(response["body"].read())
            embeddings.append(result["embedding"])
        return embeddings

    def embed_query(self, text):
        response = self.client.invoke_model(
            modelId=EMBEDDING_MODEL_ID,
            body=json.dumps({"inputText": text}),
            contentType="application/json",
            accept="application/json"
        )
        result = json.loads(response["body"].read())
        return result["embedding"]