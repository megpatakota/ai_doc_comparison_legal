import json
import os
from src.base import Section
import logging

# Configure logging if not already configured
logger = logging.getLogger(__name__)

# save the extracted sections to a JSON file
def save_sections(sections, filename):
    # Convert sections to dictionaries
    section_dicts = [section.model_dump() for section in sections]
    
    # Save to file
    with open(filename, "w") as f:
        json.dump(section_dicts, f, indent=2)
    
    # Log information about the saved file
    file_size = os.path.getsize(filename)
    logger.info(f"Saved {len(sections)} sections to {filename} ({file_size} bytes)")
    print(f"✅ Saved {len(sections)} sections to {filename}")
    
    # Print a preview of the saved data
    if sections:
        print(f"Preview of first section: {section_dicts[0]}")
        if len(sections) > 1:
            print(f"Preview of last section: {section_dicts[-1]}")
    
    return filename


# load the extracted sections from the JSON file
def load_sections(filename):
    with open(filename, "r") as f:
        sections = json.load(f)
    return [Section(**section) for section in sections] 