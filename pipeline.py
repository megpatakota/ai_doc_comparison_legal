from src.text_process import extract_text_from_docx, batch_text
from src.llm_section_extract import process_batches
from src.file_io import save_sections, save_extract_text_from_docx, load_sections, save_to_json
from src.standardize import standardize_sections_llm
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define input and output directories
input_folder = "data/input"
output_folder = "data/output"
mapping_folder = "data/output/mapping"
input_temp_folder = "data/temp"

# Ensure the output directory exists
os.makedirs(output_folder, exist_ok=True)

def process_docx_files(input_folder, output_folder, input_temp_folder):
    """
    Process .docx files in the input folder, extract sections, and save them to the output folder.
    """
    # Initialize document counter
    doc_counter = 1

    # List all files in the input folder
    input_files = os.listdir(input_folder)

    # Iterate over each file in the input folder
    for file in input_files:
        # Process only .docx files
        if file.endswith(".docx"):
            input_path = os.path.join(input_folder, file)
            logger.info(f"Processing file: {file} (doc_id: {doc_counter})")
            
            # Extract text from the docx file
            text = extract_text_from_docx(input_path)
            # save the extracted text to a text file
            save_extract_text_from_docx(text, os.path.join(input_temp_folder, f"{os.path.splitext(file)[0]}.txt"))

            # Batch the text for processing
            batches = batch_text(text)
            
            # Process each batch to extract sections
            sections = process_batches(batches)
            
            if not sections:
                logger.warning(f"No sections extracted from {file}")
            
            # Add document ID to each section
            updated_sections = []
            for section in sections:
                # Create a new dictionary with all fields plus doc_id
                section_dict = section.model_dump()
                section_dict['doc_id'] = str(doc_counter)  # Convert to string for consistency
                
                # Create a new Section object with the updated dictionary
                updated_section = section.__class__(**section_dict)
                updated_sections.append(updated_section)
            
            # Print out each extracted section's data
            logger.info(f"All extracted sections from {file} (doc_id: {doc_counter}):")
            for section in updated_sections:
                logger.info(f"Section: {section.model_dump()}")
            
            # Define the output file name based on the input file name
            output_file = os.path.join(output_folder, f"{os.path.splitext(file)[0]}_sections.json")
            
            # Save the sections to a JSON file
            save_sections(updated_sections, output_file)
            
            # Increment document counter for next file
            doc_counter += 1


def standardize_sections(output_folder):
    """
    Load extracted sections from JSON files, standardize them, and save the standardized sections.
    """
    # Load the extracted sections from the JSON files
    v1_sections = load_sections(os.path.join(output_folder, "v1_sections.json"))
    v2_sections = load_sections(os.path.join(output_folder, "v2_sections.json"))

    # Standardize the sections
    standardized_sections = standardize_sections_llm(v1_sections, v2_sections)
    save_to_json(standardized_sections, os.path.join(output_folder, "standardized_sections.json"))


# Call the functions as needed
# process_docx_files(input_folder, output_folder, input_temp_folder)
standardize_sections(output_folder)

