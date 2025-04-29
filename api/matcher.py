import torch
from transformers import BertTokenizer, BertModel
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import PyPDF2
import io


class ResumeMatcher:
    def __init__(self):
        # Load pre-trained model and tokenizer
        self.tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
        self.model = BertModel.from_pretrained('bert-base-uncased')
        self.model.eval()  # Set the model to evaluation mode

    def extract_text_from_pdf(self, pdf_file):
        """Extract text content from a PDF file"""
        try:
            pdf_reader = PyPDF2.PdfReader(io.BytesIO(pdf_file))
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text()
            return text
        except Exception as e:
            print(f"Error extracting text from PDF: {e}")
            return ""

    def get_bert_embedding(self, text):
        """Generate BERT embeddings for the given text"""
        # Truncate text to avoid exceeding BERT's maximum length
        max_length = 512
        if len(text.split()) > max_length:
            text = ' '.join(text.split()[:max_length])

        # Tokenize and convert to tensor
        inputs = self.tokenizer(text, return_tensors='pt',
                                padding=True, truncation=True, max_length=max_length)

        # Generate embeddings
        with torch.no_grad():
            outputs = self.model(**inputs)

        # Use [CLS] token embedding as the document embedding
        embeddings = outputs.last_hidden_state[:, 0, :].numpy()
        return embeddings[0]

    def calculate_similarity(self, job_description, resumes):
        """Calculate similarity scores between job description and resumes"""
        # Get embedding for job description
        job_embedding = self.get_bert_embedding(job_description)

        # Process each resume
        resume_embeddings = []
        resume_texts = []

        for resume in resumes:
            resume_text = self.extract_text_from_pdf(resume)
            if resume_text:
                resume_texts.append(resume_text)
                embedding = self.get_bert_embedding(resume_text)
                resume_embeddings.append(embedding)

        if not resume_embeddings:
            return []

        # Calculate cosine similarity scores
        similarities = cosine_similarity([job_embedding], resume_embeddings)[0]

        # Create result with resume index, text preview, and similarity score
        results = []
        for i, score in enumerate(similarities):
            preview = resume_texts[i][:200] + "..." if len(resume_texts[i]) > 200 else resume_texts[i]
            results.append({
                "index": i,
                "preview": preview,
                "similarity_score": float(score)
            })

        # Sort by similarity score in descending order
        results.sort(key=lambda x: x["similarity_score"], reverse=True)

        return results