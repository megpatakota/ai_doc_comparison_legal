import docx
import logging


# Set up logging configuration
logging.basicConfig(level=logging.INFO, format="%(message)s")


def wrap_lines_with_tags(text):
    # Split the text into lines and wrap each line with a custom tag
    lines = text.splitlines()
    wrapped_lines = [f'<line id="{i}">{line}</line>' for i, line in enumerate(lines)]
    return "\n".join(wrapped_lines)


def extract_text_from_docx(file_path):
    logging.info(f"Starting to extract text from: {file_path}")
    try:
        doc = docx.Document(file_path)
        # Extract text from each paragraph (ignoring empty ones)
        text = "\n".join([para.text for para in doc.paragraphs if para.text.strip()])

        logging.info(f"Successfully extracted {len(text)} characters from document")

        # Wrap each line with custom tags
        text = wrap_lines_with_tags(text)

        return text
    except Exception as e:
        logging.error(f"Error extracting text from {file_path}: {str(e)}")
        raise


def batch_text(text, max_tokens=10000):
    """
    Splits the text into batches based on sentences.
    Note: The wrapped tags will be included, but the LLM output may return a placeholder for line_id.
    """
    sentences = text.replace("\n", " ").split(".")
    current_batch = []
    current_token_count = 0
    batches = []

    for sentence in sentences:
        sentence_tokens = len(sentence.split()) / 0.75
        if current_token_count + sentence_tokens > max_tokens and current_batch:
            batches.append(" ".join(current_batch) + ".")
            current_batch = []
            current_token_count = 0
        current_batch.append(sentence)
        current_token_count += sentence_tokens

    if current_batch:
        batches.append(" ".join(current_batch) + ".")
    return batches
