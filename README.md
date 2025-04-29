# Resume-Job Description Matcher

A simple machine learning application that uses BERT embeddings to match resumes against job descriptions. This project provides a FastAPI backend for processing and a Streamlit frontend for user interaction.

## Features

- Upload multiple resumes in PDF format
- Enter job description text
- Rank resumes based on similarity to job description using BERT embeddings
- View similarity scores and text previews of matched resumes

## Project Structure

```
resume-job-matcher/
├── api/               # FastAPI backend
│   ├── __init__.py
│   ├── matcher.py     # Resume matching logic using BERT
│   └── main.py        # FastAPI app and endpoints
├── app/
│   └── streamlit_app.py  # Streamlit frontend
├── models/            # For any additional model files
│   └── __init__.py
├── requirements.txt   # Project dependencies
├── README.md          # Project documentation
└── .gitignore         # Git ignore file
```

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

2. In a separate terminal window, start the Streamlit frontend:
   ```
   streamlit run app/streamlit_app.py
   ```
   The Streamlit app will open in your browser (usually at `http://localhost:8501`).

3. Using the application:
   - Enter a job description in the text area
   - Upload multiple resume PDF files
   - Click the "Match Resumes" button
   - View the ranked results

## How It Works

1. The BERT model generates embeddings for the job description and each resume
2. Cosine similarity is calculated between the job description embedding and each resume embedding
3. Resumes are ranked based on their similarity scores
4. Results are displayed in the Streamlit UI with preview text from each resume

## Requirements

- Python 3.8+
- PyTorch
- Transformers (Hugging Face)
- FastAPI
- Streamlit
- PyPDF2 (for PDF text extraction)
- Other dependencies listed in requirements.txt

## Limitations

- Only supports PDF format for resumes
- BERT has a token limit of 512 tokens, so very long texts will be truncated
- Text extraction from PDFs may not be perfect for all formats

## Future Improvements

- Add support for more file formats (DOCX, TXT)
- Implement more sophisticated text preprocessing
- Add custom model training options
- Improve text extraction from complex PDF formats
- Add user authentication and result saving

## License

MIT

## Acknowledgments

- This project uses the BERT model from Hugging Face's Transformers library
- Built with FastAPI and Streamlit frameworks