import requests
import tempfile

def download_resume(file_url: str) -> str:
    response = requests.get(file_url)
    response.raise_for_status()

    suffix = ".pdf" if file_url.endswith(".pdf") else ".docx"
    temp = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)

    temp.write(response.content)
    temp.close()

    return temp.name
