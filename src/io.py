import json
from src.base import Section


# save the extracted sections to a JSON file
def save_sections(sections, filename):
    with open(filename, "w") as f:
        json.dump([section.dict() for section in sections], f, indent=2)


# load the extracted sections from the JSON file
def load_sections(filename):
    with open(filename, "r") as f:
        sections = json.load(f)
    return [Section(**section) for section in sections]
