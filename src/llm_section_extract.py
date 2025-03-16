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
    
    Args:
        batch_text (str): The text batch to analyze for sections.
        
    Returns:
        List[Section]: A list of Section objects containing titles and purposes.
        
    Raises:
        JSONDecodeError: If the LLM response cannot be parsed as JSON.
        ValidationError: If the parsed JSON doesn't match the expected schema.
    """
    try:
        # Load and render the prompt template
        template = env.get_template("extract_sections.j2")
        prompt = template.render(text=batch_text)
        logger.info("Sending request to LLM for section extraction")
        response = completion(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
        )
        
        # Parse the JSON response
        content = response.choices[0].message.content
        logger.debug(f"Raw LLM response: {content}")
        
        try:
            sections_data = json.loads(content)
            # Handle both array format and {sections: [...]} format
            if isinstance(sections_data, list):
                sections = sections_data
            elif isinstance(sections_data, dict) and "sections" in sections_data:
                sections = sections_data["sections"]
            else:
                logger.warning(f"Unexpected response format: {sections_data}")
                sections = []
                
            logger.info(f"Successfully extracted {len(sections)} sections")
            
            # Add detailed logging for each section
            section_objects = []
            for i, section_data in enumerate(sections, 1):
                # Ensure line_id is present
                if "line_id" not in section_data:
                    logger.warning(f"Section {i} missing line_id: {section_data}")
                    section_data["line_id"] = "unknown"
                
                # Create Section object
                try:
                    section = Section(**section_data)
                    print(f"Section {i}: {section_data}")
                    section_objects.append(section)
                except ValidationError as e:
                    logger.error(f"Validation error for section {i}: {e}")
                    logger.debug(f"Section data was: {section_data}")
            
            return section_objects
            
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON response: {e}")
            logger.debug(f"Response content was: {content}")
            return []

    except Exception as e:
        logger.error(f"Unexpected error in extract_titles: {str(e)}")
        return []

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