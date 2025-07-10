from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from scripts.pdf_processor import extract_text_from_pdf, chunk_into_clauses, BGE_Encoder
from scripts.qdrant_connector import connect_qdrant, store_embeddings_in_qdrant, search_collection
from scripts.retriever import QueryRequest as Q
from scripts.generator import generate_response

app = FastAPI()

bge = BGE_Encoder()

@app.post("/uploadfile/")
async def upload_file(file: UploadFile = File(...)):
    """
    Endpoint to upload a file.
    Returns the filename and content type of the uploaded file.
    """
    try:
        # Read the file content
        content = await file.read()

        text_content = extract_text_from_pdf(content)

        clauses = chunk_into_clauses(text_content)

        embeddings = bge.encode(clauses, batch_size=32, normalise=True)

        client = connect_qdrant(vector_size=768, recreate=True)
        store_embeddings_in_qdrant(client, embeddings, clauses)
        
        # Return the filename and content type
        return JSONResponse(content={
            "filename": file.filename,
            "content_type": file.content_type,
            "size": len(content)
        })
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
    
@app.post("/query/")
async def query_collection(req: Q):
    """
        Endpoint to query the Qdrant collection.
    """
    try:
        query_vector = bge.encode([req.query], batch_size=1, normalise=True)[0]

        client = connect_qdrant(recreate=False)

        results = search_collection(client, query_vector, top_k=req.top_k)

        response = generate_response(req.query, [r['clause'] for r in results])

        return JSONResponse(content={
            "query": req.query,
            "top_k": req.top_k,
            "results": [r['clause'] for r in results],
            "response": response
        })

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})