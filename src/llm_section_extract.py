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
            response_format=Sections,
        )
        
        sections = json.loads(response.choices[0].message.content)["sections"]
        logger.info(f"Successfully extracted {len(sections)} sections")
        
        # Add detailed logging for each section
        section_objects = []
        for i, section_data in enumerate(sections, 1):
            section = Section(**section_data)
            # Log the entire section data for debugging
            logger.info(f"Section {i}: {section.model_dump()}")
            section_objects.append(section)
        
        return section_objects

    except (json.JSONDecodeError, ValidationError) as e:
        logger.error(f"Error processing batch: {str(e)}")
        logger.debug(f"Response content was: {response.choices[0].message.content}")
        return []

    except Exception as e:
        logger.error(f"Unexpected error processing batch: {str(e)}")
        logger.debug(f"Response content was: {response.choices[0].message.content}")
        return []

def process_batches(batches: List[str]) -> List[Section]:
    """
    Process multiple text batches to extract sections.
    
    Args:
        batches (List[str]): A list of text batches to process.
        
    Returns:
        List[Section]: A combined list of Section objects extracted from all batches.
    """
    all_titles = []
    total_batches = len(batches)
    
    logger.info(f"Starting to process {total_batches} batches")
    
    for i, batch in enumerate(batches):
        logger.info(f"Processing batch {i+1} of {total_batches}")
        titles = extract_titles(batch)
        
        if not titles:
            logger.error(f"Failed to process batch {i+1}. Stopping processing.")
            break
            
        logger.debug(f"Extracted titles for batch {i+1}: {titles}")
        all_titles.extend(titles)
        
    logger.info(f"Completed processing with {len(all_titles)} total sections extracted")
    return all_titles