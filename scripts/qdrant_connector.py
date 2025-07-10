from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from dotenv import load_dotenv
import os
import uuid

constants = {
    "collection_name": "default_user",
}

def connect_qdrant(collection_name=constants["collection_name"], vector_size=768, recreate=True):
    """
    Connect to the Qdrant database using the API key from environment variables.
    """
    load_dotenv()  # Load environment variables from .env file
    # Ensure the QDRANT_API_KEY is set in your .env file
    if not os.getenv("QDRANT_API_KEY"):
        raise ValueError("QDRANT_API_KEY is not set in the environment variables.")
    
    # Create a Qdrant client instance
    qdrant = QdrantClient(
        url="https://3d8455d3-309c-4ab7-9124-8f7d9ed4db5f.us-east-1-0.aws.cloud.qdrant.io:6333", 
        api_key=os.getenv("QDRANT_API_KEY")
    )

    if recreate:
        # Recreate the collection if it already exists
        qdrant.recreate_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(size=vector_size, distance=Distance.COSINE)
        )
    return qdrant

def store_embeddings_in_qdrant(client, embeddings, clauses, collection_name=constants["collection_name"]):
    """
    Store embeddings and their corresponding clauses in the Qdrant collection.
    
    Args:
        client (QdrantClient): The Qdrant client instance.
        collection_name (str): The name of the collection to store data in.
        embeddings (list): List of embeddings to store.
        clauses (list): List of clauses corresponding to the embeddings.
    """
    points = []
    for i, (clause, vector) in enumerate(zip(clauses, embeddings)):
        points.append(
            PointStruct(
            id = str(uuid.uuid4()),  # Use index as ID for simplicity
            vector = vector,
            payload = {"text": clause}
        )
    )
    
    client.upsert(
        collection_name=collection_name,
        points=points
    )

    print(f"Stored {len(points)} clauses in Qdrant.")

def search_collection(client, query_vector, top_k=5, collection_name=constants["collection_name"]):
    """
    Search the Qdrant collection for the most similar clauses to the query vector.
    
    Args:
        client (QdrantClient): The Qdrant client instance.
        query_vector (list): The vector representation of the query.
        top_k (int): The number of top results to return.
        collection_name (str): The name of the collection to search in.
        
    Returns:
        list: A list of tuples containing the clause text and its similarity score.
    """
    results = client.search(
        collection_name=collection_name,
        query_vector=query_vector,
        limit=top_k
    )
    
    return [{"clause": result.payload["text"], "score": result.score} for result in results]