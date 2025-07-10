from openai import OpenAI
from dotenv import load_dotenv
import os
load_dotenv()

def generate_response(query: str, clauses, model: str = "mistralai/mistral-7b-instruct"):
    """
    Generate a response from the OpenAI API based on the provided prompt.

    :param query: The input text to generate a response for.
    :param clauses: The relevant clauses to include in the response.
    :param model: The model to use for generating the response.
    :return: The generated response text.
    """
    open_router_key = os.getenv("OPEN_ROUTER_KEY")
    client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=open_router_key)
    
    prompt = f"""You are a legal assistant. Answer the following legal question using the clauses below.
    Question: {query}

Relevant Clauses:
{chr(10).join(f"- {c}" for c in clauses)}

Be precise, avoid hallucinations, and cite only what’s present.

Answer:"""
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )
    print(f"Generated response: {response}")
    return response.choices[0].message.content