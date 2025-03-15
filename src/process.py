import docx
import logging

# Set up logging configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def extract_text_from_docx(file_path):
    """
    Extract plain text content from a Word document (.docx) file.

    Args:
        file_path (str): Path to the Word document file.

    Returns:
        str: Extracted text content with empty paragraphs removed and paragraphs
            joined by newlines.

    Raises:
        Exception: If there's an error reading or processing the document.
            The specific exception depends on the python-docx library.
    """
    logging.info(f"Starting to extract text from: {file_path}")
    try:
        doc = docx.Document(file_path)
        text = "\n".join([para.text for para in doc.paragraphs if para.text.strip()])
        logging.info(f"Successfully extracted {len(text)} characters from document")
        return text
    except Exception as e:
        logging.error(f"Error extracting text from {file_path}: {str(e)}")
        raise

def batch_text(text, max_tokens=2000):
    """
    Split a large text into smaller batches based on token count.

    This function splits the input text into sentences and groups them into
    batches that don't exceed the specified maximum token count. It uses a
    simple approximation of tokens by assuming 1 token ≈ 0.75 words.

    Args:
        text (str): The input text to be split into batches.
        max_tokens (int, optional): Maximum number of tokens per batch. 
            Defaults to 2000.

    Returns:
        list[str]: List of text batches, where each batch is a string
            containing one or more sentences and ends with a period.
            The token count of each batch is approximately less than
            or equal to max_tokens.
    """
    logging.info(f"Starting to batch text with max_tokens={max_tokens}")
    sentences = text.replace('\n', ' ').split('.')
    logging.info(f"Split text into {len(sentences)} sentences")
    
    current_batch = []
    current_token_count = 0
    batches = []
    
    for i, sentence in enumerate(sentences, 1):
        sentence_tokens = len(sentence.split()) / 0.75
        if current_token_count + sentence_tokens > max_tokens and current_batch:
            batches.append(' '.join(current_batch) + '.')
            logging.debug(f"Created batch {len(batches)} with {current_token_count:.0f} tokens")
            current_batch = []
            current_token_count = 0
        current_batch.append(sentence)
        current_token_count += sentence_tokens
    
    if current_batch:
        batches.append(' '.join(current_batch) + '.')
        logging.debug(f"Created final batch {len(batches)} with {current_token_count:.0f} tokens")
    
    logging.info(f"Finished batching text into {len(batches)} batches")
    return batches