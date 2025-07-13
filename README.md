# Resume-Job Description Matcher

A semantic resume-job matching system powered by SBERT sentence embeddings and FastAPI. Upload job descriptions and multiple resumes (PDF/DOCX/TXT), and the system will return the top-matching resumes ranked by semantic similarity.

## Features

- 🔍 **Semantic Similarity** using Sentence-BERT (MPNet)
- 📄 **Multi-format Resume Parsing**: PDF, DOCX, and TXT
- 🧹 **Text Preprocessing**: Cleanses and optionally prioritizes relevant sections (skills, experience, etc.)
- 🧠 **Cosine Similarity Matching** between resumes and job description
- ⚙️ **REST API** using FastAPI
- 🌐 **Frontend Integration Ready** (PowerApps, Streamlit, etc.)
- ✅ **CORS Enabled** for frontend clients

## Project Structure

```
resume-job-matcher/
├── src/
│  ├── api/               # FastAPI backend
│  │   └── endpoints.py
│  ├── models/
│  │   └── schemas.py 
│  └── resumehrconnect/
│      ├── matcher.py
│      └── pdf_extract.py
├── main.py
├── requirements.txt   # Project dependencies
├── README.md          # Project documentation
└── .gitignore         # Git ignore file
```
## 📦 Tech Stack

- **FastAPI** – for RESTful API
- **sentence-transformers** – for semantic vector embeddings
- **PyPDF2, docx2txt** – for file parsing
- **Pydantic** – for data validation
- **Uvicorn** – for ASGI server
- **PowerApps** – frontend integration (optional)

---
## Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/resume-job-matcher.git
   cd resume-job-matcher
   ```

2. Create a virtual environment and activate it:
   ```
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

## Usage

1. Start the FastAPI backend:
   ```
   uvicorn api.main:app --reload
   ```
   The API will be available at `http://localhost:8000`.
