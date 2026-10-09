from pydantic import BaseModel, Field
from typing import Optional, Literal, Dict, Any

class DocumentRequestBase(BaseModel):
    document_type: Literal["NDA", "Employment", "Lease"]
    
class NDARequest(BaseModel):
    disclosing_party: str
    receiving_party: str
    effective_date: str
    jurisdiction: str
    confidentiality_period: str

class EmploymentRequest(BaseModel):
    employer: str
    employee: str
    role: str
    compensation: str
    start_date: str
    termination_terms: str

class LeaseRequest(BaseModel):
    landlord: str
    tenant: str
    property_address: str
    rent: str
    security_deposit: str
    lease_duration: str

class GenerateRequest(BaseModel):
    document_type: Literal["NDA", "Employment", "Lease"]
    data: Dict[str, Any]  # Will hold the specific request data

class GenerateResponse(BaseModel):
    markdown_content: str
    term_table: str

class ExportRequest(BaseModel):
    markdown_content: str
    chart_base64: Optional[str] = None
    chart_image: Optional[str] = None  # base64 encoded chart image
