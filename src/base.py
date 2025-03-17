from pydantic import BaseModel, Field
from typing import List, Optional

# Define a Pydantic model to enforce the JSON structure
class Section(BaseModel):
    title: str
    description: str  
    start_id: str
    end_id: str 
    doc_id: Optional[str] = None  # Document identifier, optional with default None


class Sections(BaseModel):
    sections: List[Section]

# class Mapping(BaseModel):
#     title: str
#     line_id: str
#     doc_id: str

class StandardizedSection(BaseModel):
    doc_a_section: Section
    reasoning: str
    doc_b_sections: Optional[List[Section]] = None
    standardised_title: str

class StandardizedSections(BaseModel):
    sections: List[StandardizedSection]

class EvaluationResult(BaseModel):
    criterion: str
    reasoning: str
    score: int

class EvaluationResults(BaseModel):
    results: List[EvaluationResult]
