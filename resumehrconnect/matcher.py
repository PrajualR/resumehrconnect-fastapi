from sentence_transformers import SentenceTransformer, util
import re

class ResumeMatcher:
    def __init__(self):
        self.model = SentenceTransformer('all-mpnet-base-v2')

    def clean_text(self, text: str) -> str:
        text = re.sub(r'\s+', ' ', text)
        text = re.sub(r'[^\w\s.,\-:/()]', '', text)
        return text.strip()

    def embed(self, text: str):
        return self.model.encode(text, convert_to_tensor=True)

    def get_match_level(self, score: float) -> str:
        if score >= 80:
            return "High"
        elif score >= 60:
            return "Medium"
        else:
            return "Low"

    def match(self, job_description: str, resumes: list[str], filenames: list[str]):
        jd_embedding = self.embed(self.clean_text(job_description))
        results = []

        for i, resume in enumerate(resumes):
            try:
                resume_embedding = self.embed(self.clean_text(resume))
                score = float(util.pytorch_cos_sim(jd_embedding, resume_embedding).item()) * 100

                results.append({
                    'filename': filenames[i],
                    'similarity': round(score, 2),
                    'match_level': self.get_match_level(score)
                })
            except Exception as e:
                results.append({
                    'filename': filenames[i],
                    'similarity': 0.0,
                    'match_level': "Error",
                    'error': str(e)
                })

        sorted_results = sorted(results, key=lambda x: x['similarity'], reverse=True)
        return sorted_results[:10]