import json
import logging
from pathlib import Path
from jinja2 import Environment, FileSystemLoader
from litellm import completion
from pydantic import BaseModel, ValidationError
from typing import List
import os
from dotenv import load_dotenv
from src.base import Section, Sections

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Setup Jinja2 environment
template_dir = "templates"
env = Environment(loader=FileSystemLoader(template_dir))

def extract_titles(batch_text: str) -> List[Section]:
    """
    Extract section titles and their purposes from a batch of text using LLM.
    
    Raises:
        json.JSONDecodeError: If the LLM response cannot be parsed as JSON.
        ValidationError: If any section fails pydantic validation.
    """
    # Render the prompt (assumes the template exists and is valid)
    template = env.get_template("extract_sections.j2")
    prompt = template.render(text=batch_text)
    logger.info("Sending request to LLM for section extraction")
    
    # Send prompt to LLM
    response = completion(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        response_format=Sections
    )
    content = response.choices[0].message.content
    logger.debug("Raw LLM response: %s", content)
    
    # Parse the JSON response
    try:
        sections_data = json.loads(content)
    except json.JSONDecodeError as e:
        logger.error("Failed to parse JSON response: %s", e)
        raise
    
    # Handle both list format and dictionary with "sections" key
    sections = sections_data if isinstance(sections_data, list) else sections_data.get("sections", [])
    if not sections:
        logger.warning("No sections found in response")
        return []
    
    logger.info("Successfully extracted %d sections", len(sections))
    
    # Validate and parse sections using pydantic
    try:
        sections_obj = Sections(sections=sections)
    except ValidationError as e:
        logger.error("Validation error: %s", e)
        raise
    
    return sections_obj.sections

def process_batches(batches: List[str]) -> List[Section]:
    """
    Process multiple text batches to extract sections.
    
    Args:
        batches (List[str]): A list of text batches to process.
        
    Returns:
        List[Section]: A combined list of Section objects extracted from all batches.
    """
    all_sections = []
    total_batches = len(batches)
    
    logger.info(f"Starting to process {total_batches} batches")
    
    for i, batch in enumerate(batches):
        logger.info(f"Processing batch {i+1} of {total_batches}")
        # Get the sections for this batch - already as Section objects
        batch_sections = extract_titles(batch)
        
        # Add these sections to our combined list
        all_sections.extend(batch_sections)
    
    logger.info(f"Completed processing with {len(all_sections)} total sections extracted")
    return all_sections