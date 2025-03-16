import json
import logging
from typing import List
from litellm import completion
from jinja2 import Environment, FileSystemLoader
from src.base import StandardizedSections
from src.file_io import load_sections, save_to_json

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(message)s")


# Log the start of the function
logging.info("Starting the standardization of sections.")

# Log the rendering of the template
logging.info("Rendering the standardize_sections template.")

def standardize_sections_llm(v1_sections, v2_sections) -> List[StandardizedSections]:
    
    env = Environment(loader=FileSystemLoader("./templates"))
    standardize_sections_template = env.get_template("standardize_sections.j2")
    standardize_sections_prompt = standardize_sections_template.render(
        v1_sections=v1_sections, v2_sections=v2_sections
    )

    response = completion(
        model="gpt-4o-mini",
        temperature=1, # Adjust the temperature to control the randomness of the output
        messages=[{"role": "user", "content": standardize_sections_prompt}],
        response_format=StandardizedSections,
    )

    response = json.loads(response.choices[0].message.content)

    print('standard sections:', len(response['sections']))
    print('total mappings:', sum(len(section['mappings']) for section in response['sections']))
    # Log the response from the completion function
    logging.info("Received response from completion function.")

    return response

# Log the end of the function
logging.info("Finished the standardization of sections.")
