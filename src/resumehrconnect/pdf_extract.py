import PyPDF2
import docx2txt
import io
import re

SECTION_PATTERNS = {
    'summary': [r'summary', r'profile', r'career summary'],
    'skills': [r'skills?', r'technical skills', r'key skills', r'tools', r'tech stack'],
    'experience': [r'experience', r'work experience', r'professional experience'],
    'projects': [r'projects', r'key projects', r'project experience'],
}

def extract_text(file_bytes: bytes, filename: str) -> str:
    filename = filename.lower()
    if filename.endswith(".pdf"):
        return extract_pdf_text(file_bytes)
    elif filename.endswith(".docx"):
        return extract_docx_text(file_bytes)
    elif filename.endswith(".txt"):
        return file_bytes.decode("utf-8")
    else:
        return ""

def extract_pdf_text(file_bytes: bytes) -> str:
    try:
        reader = PyPDF2.PdfReader(io.BytesIO(file_bytes))
        text = ""
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
        return text
    except Exception as e:
        return ""

def extract_docx_text(file_bytes: bytes) -> str:
    try:
        return docx2txt.process(io.BytesIO(file_bytes))
    except Exception as e:
        return ""

def preprocess_resume_text(text: str) -> str:
    """Extracts and concatenates prioritized sections if available, else returns full cleaned text."""
    sections = detect_sections(text)
    prioritized = []

    for key in ['summary', 'skills', 'experience', 'projects']:
        if key in sections:
            prioritized.append(sections[key])

    if not prioritized and 'full_text' in sections:
        prioritized.append(sections['full_text'])

    clean_text = ' '.join(prioritized)
    clean_text = re.sub(r'\s+', ' ', clean_text)
    return clean_text.strip()

def detect_sections(text: str) -> dict:
    lines = text.split('\n')
    headers = []

    for i, line in enumerate(lines):
        line_lower = line.strip().lower()
        for section, patterns in SECTION_PATTERNS.items():
            if any(re.search(rf'\b{pattern}\b', line_lower) for pattern in patterns):
                headers.append((i, section))
                break

    headers.sort()
    sections = {}

    for idx, (start_idx, section_name) in enumerate(headers):
        end_idx = headers[idx + 1][0] if idx + 1 < len(headers) else len(lines)
        content = '\n'.join(lines[start_idx + 1:end_idx]).strip()
        sections[section_name] = content

    if not sections:
        sections['full_text'] = text.strip()

    return sections