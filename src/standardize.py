import json
import logging
from typing import List
from litellm import completion
from jinja2 import Environment, FileSystemLoader
from src.base import StandardizedSections
from src.file_io import load_sections

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(message)s")

v1_sections = load_sections("../data/output/v1_sections.json")
v2_sections = load_sections("../data/output/v2_sections.json")



def standardize_sections() -> List[StandardizedSections]:
    
    env = Environment(loader=FileSystemLoader("../templates"))
    standardize_sections_template = env.get_template("standardize_sections.j2")
    standardize_sections_prompt = standardize_sections_template.render(
        v1_sections=v1_sections, v2_sections=v2_sections
    )

    response = completion(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": standardize_sections_prompt}],
        response_format=StandardizedSections,
    )
    return response.choices[0].message.content
