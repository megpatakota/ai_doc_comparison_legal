import os
import logging
from dotenv import load_dotenv
import jinja2
from litellm import completion
from src.text_process import extract_text_from_docx
from src.file_io import write_text_to_file

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

# Retrieve API keys
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

def simple_llm():
    try:
        logging.info("Starting LLM processing pipeline")
        
        # Extract text from documents
        logging.info("Extracting text from v1.docx and v2.docx")
        v1 = extract_text_from_docx('data/input/v1.docx')
        v2 = extract_text_from_docx('data/input/v2.docx')
        
        # Load Jinja2 prompt template
        logging.info("Loading and rendering Jinja2 template")
        with open('templates/simple_llm_prompt.jinja2') as f:
            simple_llm_prompt = jinja2.Template(f.read()).render(v1=v1, v2=v2)
        
        # Call LLM API
        logging.info("Calling LLM completion API")
        response = completion(
            model="o1",  # Gemini model = gemini/gemini-1.5-pro
            messages=[{"role": "user", "content": simple_llm_prompt}]
        )
        
        response_content = response.choices[0].message.content
        
        # Write output to file
        output_path = "data/output/compare_output_pipeline2.txt"
        logging.info(f"Writing output to {output_path}")
        write_text_to_file(response_content, output_path)
        
        logging.info("LLM processing pipeline completed successfully")
        return response_content

    except Exception as e:
        logging.error(f"An error occurred: {str(e)}", exc_info=True)
        return None

simple_llm()