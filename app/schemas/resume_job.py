from pydantic import BaseModel

class ResumeJobPayload(BaseModel):
    resume_id: str
    upload_file_id: str
    file_url: str
    file_type: str
    tenant_id: str
