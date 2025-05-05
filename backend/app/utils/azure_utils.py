import os
from openai import AzureOpenAI
from typing import List
from app.core.config import settings
# Environment variables for security
AZURE_OPENAI_ENDPOINT = settings.AZURE_OPENAI_ENDPOINT
AZURE_OPENAI_KEY = settings.AZURE_OPENAI_KEY
AZURE_DEPLOYMENT_NAME = settings.AZURE_DEPLOYMENT_NAME
AZURE_API_VERSION = settings.AZURE_API_VERSION

client=AzureOpenAI(
            api_key=AZURE_OPENAI_KEY,
            api_version=AZURE_API_VERSION,
            azure_endpoint=AZURE_OPENAI_ENDPOINT,
            azure_deployment=AZURE_DEPLOYMENT_NAME,
            timeout=15
        )

def generate_azure_embeddings(texts: List[str]) -> List[List[float]]:
    response = client.embeddings.create(
        input=texts,
        model=AZURE_DEPLOYMENT_NAME
    )

    embeddings = []
    for item in response.data:
        embeddings.append(item.embedding)

        # Optional: print a short summary
        length = len(item.embedding)
        print(
            f"data[{item.index}]: length={length}, "
            f"[{item.embedding[0]}, ..., {item.embedding[-1]}]"
        )
    print(response.usage)
    return embeddings
