
from pydantic import BaseModel
from typing import List

# Define a Pydantic model to enforce the JSON structure
class Section(BaseModel):
    title: str
    Purpose: str


class Sections(BaseModel):
    sections: List[Section]