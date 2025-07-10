import fitz
import re
from sentence_transformers import SentenceTransformer
import torch
from tqdm import tqdm

def extract_text_from_pdf(file_content):
    """
    Extract text from a PDF file content.
    
    Args:
        file_content (bytes): The content of the PDF file.
        
    Returns:
        list: A list of extracted clauses.
    """
    clauses = ""
    try:
        # Open the PDF file
        pdf_document = fitz.open(stream=file_content, filetype="pdf")
        
        # Iterate through each page in the PDF
        for page in pdf_document:
            text = page.get_text()
            clauses += text + "\n"
        
        pdf_document.close()
    except Exception as e:
        print(f"Error processing PDF: {e}")
    
    return clauses

def chunk_into_clauses(text, min_length=250):
    """
    Split the text into clauses based on a minimum length.
    
    Args:
        text (str): The text to be split into clauses.
        min_length (int): The minimum length of each clause.
        
    Returns:
        list: A list of clauses.
    """
    clauses = []
    clause_pattern = re.compile(
        r"(?:(?:\d{1,2}(\.\d{1,2})*)|(?:[A-Z][a-z\s]{3,40}):?)\s+(.*?)(?=(?:\n\d{1,2}(\.\d{1,2})*\s)|(?:\n[A-Z][a-z\s]{3,40}:)|$)",
        re.DOTALL
    )
   
    matches = clause_pattern.findall(text)

    for match in matches:
        body = match[1].strip().replace("\n", " ")
        if len(body) >= min_length:
            clauses.append(body)
    
    # Fallback to splitting by newlines if no clauses found
    # Split the text into lines and filter by minimum length
    if not clauses:
        clauses = [line.strip() for line in text.splitlines() if len(line.strip()) >= min_length]

    return clauses

class BGE_Encoder:
    def __init__(self, model_name='BAAI/bge-small-en-v1.5'):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model = SentenceTransformer(model_name, device=self.device)

    def encode(self, clauses: list[str], batch_size: int = 32, normalise=True) -> list[list[float]]:
        """
        Encode a list of clauses into embeddings.
        
        :param clauses: List of strings (clauses) to be encoded.
        :return: Tensor of shape (num_clauses, embedding_dim).
        """
        with torch.no_grad():
            embeddings = self.model.encode(
                clauses,
                batch_size=batch_size,
                show_progress_bar=True,
                normalize_embeddings=normalise
            )
        return embeddings