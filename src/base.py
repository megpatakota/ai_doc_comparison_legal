from pydantic import BaseModel, Field
from typing import List, Optional

# Define a Pydantic model to enforce the JSON structure
class Section(BaseModel):
    title: str
    Purpose: str  # Note: Capital P to match the template output
    line_id: str  # Make sure this field exists
    doc_id: Optional[str] = None  # Document identifier, optional with default None


class Sections(BaseModel):
    sections: List[Section]