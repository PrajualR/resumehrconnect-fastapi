from fastapi import FastAPI, File, Form, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import uvicorn
from .matcher import ResumeMatcher

# Initialize FastAPI app
app = FastAPI(title="Resume-Job Description Matcher API")

# Add CORS middleware to allow requests from Streamlit
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize the resume matcher
matcher = ResumeMatcher()


@app.get("/")
def read_root():
    return {"message": "Welcome to the Resume-Job Description Matcher API"}


@app.post("/match")
async def match_resumes(
        job_description: str = Form(...),
        resumes: List[UploadFile] = File(...)
):
    """
    Match resumes against a job description.

    Args:
        job_description: The job description text
        resumes: List of resume files (PDF format)

    Returns:
        List of ranked resumes with similarity scores
    """
    try:
        # Read resume files content
        resume_contents = []
        for resume in resumes:
            content = await resume.read()
            resume_contents.append(content)

        # Calculate similarities
        results = matcher.calculate_similarity(job_description, resume_contents)

        # Return results with file names
        named_results = []
        for i, result in enumerate(results):
            named_results.append({
                "rank": i + 1,
                "filename": resumes[result["index"]].filename,
                "similarity_score": result["similarity_score"],
                "preview": result["preview"]
            })

        return named_results

    except Exception as e:
        return {"error": str(e)}


if __name__ == "__main__":
    uvicorn.run("api.main:app", host="0.0.0.0", port=8000, reload=True)